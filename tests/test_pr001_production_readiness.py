"""PR-001 production readiness — RBAC, health, jobs, config."""

from __future__ import annotations

import pytest

from app.config import ProductionConfig, TestingConfig
from app.extensions import db
from app.models.user import User
from app.security.capabilities import Capability
from app.security.permissions import Permission, permissions_for_roles
from app.security.roles import Role
from app.services.identity_service import IdentityService
from app.services.job_runner import JobRunner, clear_dead_letters, dead_letters


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


class TestRbacMatrix:
    def test_founder_has_all_permissions(self) -> None:
        perms = permissions_for_roles({Role.FOUNDER})
        assert Permission.CONSOLE_ACCESS in perms
        assert Permission.USERS_MANAGE in perms
        assert Permission.API_ACCESS in perms

    def test_student_is_portal_only(self) -> None:
        perms = permissions_for_roles({Role.STUDENT})
        assert perms == frozenset({Permission.STUDENT_PORTAL})

    def test_identity_grants_roles_and_capabilities(self, ctx) -> None:
        user = _make_user("learner@kwalitec.example")
        IdentityService.ensure_student_defaults(user)
        db.session.refresh(user)
        assert Role.STUDENT in user.get_roles()
        assert Capability.STUDENT_PORTAL in user.get_capabilities()
        assert Capability.CONSOLE not in user.get_capabilities()

    def test_founder_admin_bootstrap(self, ctx) -> None:
        user = _make_user("founder-rbac@kwalitec.example")
        IdentityService.ensure_founder_admin(user)
        db.session.refresh(user)
        assert Role.FOUNDER in user.get_roles()
        assert Role.ADMINISTRATOR in user.get_roles()
        assert Capability.CONSOLE in user.get_capabilities()
        from app.security.authorization import user_has_permission

        assert user_has_permission(user, Permission.CONSOLE_ACCESS)


class TestFounderAccessBridge:
    def test_rbac_founder_allowed_without_allowlist(self, client, ctx, app) -> None:
        app.config["FOUNDER_EMAILS"] = ""
        user = _make_user("rbac-founder@kwalitec.example")
        IdentityService.ensure_founder_admin(user)
        client.post(
            "/auth/login",
            data={
                "email": "rbac-founder@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        response = client.get("/console/")
        assert response.status_code == 200

    def test_student_forbidden_without_console_capability(
        self, client, ctx, app
    ) -> None:
        app.config["FOUNDER_EMAILS"] = "other@kwalitec.example"
        user = _make_user("student-rbac@kwalitec.example")
        IdentityService.ensure_student_defaults(user)
        client.post(
            "/auth/login",
            data={
                "email": "student-rbac@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        response = client.get("/console/")
        assert response.status_code == 403

    def test_legacy_allowlist_still_grants_access(self, client, ctx, app) -> None:
        app.config["FOUNDER_EMAILS"] = "legacy@kwalitec.example"
        _make_user("legacy@kwalitec.example")
        client.post(
            "/auth/login",
            data={
                "email": "legacy@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        response = client.get("/console/")
        assert response.status_code == 200


class TestHealthEndpoints:
    def test_live_ready_and_details(self, client) -> None:
        live = client.get("/health/live")
        assert live.status_code == 200
        assert live.get_json()["status"] == "ok"

        health = client.get("/health")
        assert health.status_code == 200
        payload = health.get_json()
        assert "components" in payload
        assert payload["database"] == "connected"

        details = client.get("/health/details")
        assert details.status_code in {200, 503}
        body = details.get_json()
        assert "dead_letters" in body
        assert "alerts" in body


class TestJobRunner:
    def test_retries_then_succeeds(self) -> None:
        clear_dead_letters()
        state = {"n": 0}

        def flaky():
            state["n"] += 1
            if state["n"] < 3:
                raise RuntimeError("transient")
            return "ok"

        result = JobRunner(max_attempts=3, backoff_seconds=0).run("flaky", flaky)
        assert result.status == "succeeded"
        assert result.value == "ok"
        assert result.attempts == 3

    def test_dead_letter_on_exhaustion(self) -> None:
        clear_dead_letters()

        def always_fail():
            raise ValueError("boom")

        result = JobRunner(max_attempts=2, backoff_seconds=0).run(
            "fail-job", always_fail
        )
        assert result.status == "dead_lettered"
        assert len(dead_letters()) == 1
        assert dead_letters()[0].job_name == "fail-job"


class TestProductionConfig:
    def test_testing_config_selected(self, app) -> None:
        # Session fixture sets APP_ENV=testing
        assert app.config["TESTING"] is True

    def test_production_rejects_insecure_secret(self, monkeypatch) -> None:
        monkeypatch.setenv("SECRET_KEY", "change-this-secret-key")
        monkeypatch.setenv(
            "DATABASE_URL", "postgresql+psycopg://u:p@localhost:5432/kwalitec"
        )
        from app import _validate_env_vars

        with pytest.raises(RuntimeError, match="SECRET_KEY"):
            _validate_env_vars(ProductionConfig)

    def test_production_requires_database_url(self, monkeypatch) -> None:
        monkeypatch.setenv("APP_ENV", "production")
        monkeypatch.setenv("SECRET_KEY", "a" * 32)
        monkeypatch.delenv("DATABASE_URL", raising=False)
        from app import _validate_env_vars

        with pytest.raises(RuntimeError, match="DATABASE_URL"):
            _validate_env_vars(ProductionConfig)

    def test_testing_config_class(self) -> None:
        assert TestingConfig.WTF_CSRF_ENABLED is False
        assert TestingConfig.TESTING is True
