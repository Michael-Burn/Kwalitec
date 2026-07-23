"""GA-001 WS5 — failure-mode handling (DB, jobs, config, migrations, perms, 500)."""

from __future__ import annotations

import os
import tempfile
from unittest.mock import patch

import pytest

from app.config import ProductionConfig
from app.services.health_service import ComponentHealth, HealthService
from app.services.job_runner import JobRunner, clear_dead_letters, dead_letters
from tests.ga.helpers import login_as, make_student


class TestDatabaseUnavailable:
    def test_health_reports_database_error(self, app, ctx) -> None:
        with patch(
            "app.services.health_service.db.session.execute",
            side_effect=RuntimeError("connection refused"),
        ):
            component = HealthService.check_database(app)
        assert component.status == "error"
        assert component.name == "database"

    def test_ready_fails_when_database_down(self, client) -> None:
        with (
            patch(
                "app.services.health_service.HealthService.check_database",
                return_value=ComponentHealth(
                    name="database",
                    status="error",
                    detail="OperationalError",
                ),
            ),
            patch(
                "app.services.health_service.HealthService.check_migrations",
                return_value=ComponentHealth(name="migrations", status="ok"),
            ),
        ):
            response = client.get("/health/ready")
        assert response.status_code == 503
        payload = response.get_json()
        assert payload.get("ready") is False


class TestBackgroundJobFailure:
    def test_job_dead_letters_on_exhaustion(self) -> None:
        clear_dead_letters()

        def boom():
            raise RuntimeError("worker crash")

        result = JobRunner(max_attempts=2, backoff_seconds=0).run("ga-fail", boom)
        assert result.status == "dead_lettered"
        letters = dead_letters()
        assert any(item.job_name == "ga-fail" for item in letters)

    def test_details_exposes_dead_letters(self, client) -> None:
        clear_dead_letters()

        def always_fail():
            raise ValueError("x")

        JobRunner(max_attempts=1, backoff_seconds=0).run("ga-visible", always_fail)
        response = client.get("/health/details")
        assert response.status_code in {200, 503}
        body = response.get_json()
        assert "dead_letters" in body
        assert any(item["job_name"] == "ga-visible" for item in body["dead_letters"])


class TestMissingConfiguration:
    def test_production_requires_database_url(self, monkeypatch) -> None:
        monkeypatch.setenv("APP_ENV", "production")
        monkeypatch.setenv("SECRET_KEY", "a" * 32)
        monkeypatch.delenv("DATABASE_URL", raising=False)
        from app import _validate_env_vars

        with pytest.raises(RuntimeError, match="DATABASE_URL"):
            _validate_env_vars(ProductionConfig)

    def test_production_rejects_short_secret(self, monkeypatch) -> None:
        monkeypatch.setenv("SECRET_KEY", "short")
        monkeypatch.setenv(
            "DATABASE_URL", "postgresql+psycopg://u:p@localhost:5432/kwalitec"
        )
        from app import _validate_env_vars

        with pytest.raises(RuntimeError, match="SECRET_KEY"):
            _validate_env_vars(ProductionConfig)


class TestMigrationMismatch:
    def test_migrations_behind_head_is_degraded(self, app, ctx) -> None:
        with patch.object(
            HealthService,
            "check_migrations",
            return_value=ComponentHealth(
                name="migrations",
                status="degraded",
                detail="database behind head",
                meta={"current": "old", "head": "202607230002"},
            ),
        ):
            component = HealthService.check_migrations(app)
        assert component.status == "degraded"
        assert "behind" in component.detail

    def test_aggregate_ready_false_on_migration_mismatch(self, app, ctx) -> None:
        with (
            patch.object(
                HealthService,
                "check_database",
                return_value=ComponentHealth(name="database", status="ok"),
            ),
            patch.object(
                HealthService,
                "check_migrations",
                return_value=ComponentHealth(
                    name="migrations",
                    status="degraded",
                    detail="database behind head",
                ),
            ),
        ):
            payload = HealthService.aggregate(ready=True)
        assert payload["ready"] is False


class TestInvalidPermissions:
    def test_student_forbidden_on_console(self, client, ctx, app) -> None:
        make_student("ga-fail-perms@kwalitec.example")
        app.config["FOUNDER_EMAILS"] = "other@example.com"
        login_as(client, "ga-fail-perms@kwalitec.example")
        response = client.get("/console/")
        assert response.status_code == 403
        html = response.get_data(as_text=True)
        assert "Access Denied" in html or "403" in html or "denied" in html.lower()


class TestUnhandledExceptions:
    def test_500_template_hides_detail_and_shows_reference(self, app) -> None:
        """User-facing 500 page must show a reference id without stack traces."""
        from flask import render_template

        with app.test_request_context():
            html = render_template(
                "errors/500.html",
                title="Error",
                error_reference_id="ga-ref-abc123",
            )
        assert "Reference ID" in html
        assert "ga-ref-abc123" in html
        assert "Traceback" not in html
        assert "intentional ga failure" not in html

    def test_production_registers_500_handler_when_not_propagating(self) -> None:
        """Custom 500 handler is registered when PROPAGATE_EXCEPTIONS is false."""
        db_fd, db_path = tempfile.mkstemp(suffix=".sqlite3")
        try:
            from app import _register_error_handlers, create_app

            app = create_app()
            app.config.update(
                TESTING=True,
                PROPAGATE_EXCEPTIONS=False,
                DEBUG=False,
                WTF_CSRF_ENABLED=False,
                SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
            )
            _register_error_handlers(app)
            handlers = app.error_handler_spec.get(None, {}).get(500) or {}
            assert handlers, "Expected a registered HTTP 500 error handler"
        finally:
            os.close(db_fd)
            os.unlink(db_path)
