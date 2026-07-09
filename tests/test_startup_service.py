"""Tests for the StartupService automatic database initialization."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from unittest.mock import patch

import pytest
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy.exc import OperationalError, ProgrammingError

from app import create_app
from app.config import ProductionConfig
from app.extensions import db
from app.models.user import User
from app.services.startup_service import StartupService

# Env vars we save/restore around each test so the session-scoped conftest
# environment is never polluted.
_ENV_KEYS = [
    "APP_ENV",
    "SECRET_KEY",
    "ADMIN_EMAIL",
    "ADMIN_PASSWORD",
    "DATABASE_URL",
    "FLASK_ENV",
]


@pytest.fixture(scope="function")
def fresh_prod_app(tmp_path):
    """Create a Flask app backed by a fresh empty SQLite database.

    The app is created with ``APP_ENV=testing`` so that ``StartupService``
    does **not** run during ``create_app()``.  Each test then sets
    ``APP_ENV=production`` and calls ``StartupService.run(app)`` directly,
    giving full control over the pre-init state of the database.
    """
    db_path = tmp_path / "fresh.sqlite3"

    saved_env = {key: os.environ.get(key) for key in _ENV_KEYS}

    os.environ["APP_ENV"] = "testing"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
    os.environ["FLASK_ENV"] = "testing"
    os.environ.pop("ADMIN_EMAIL", None)
    os.environ.pop("ADMIN_PASSWORD", None)
    os.environ.pop("DATABASE_URL", None)

    class _FreshConfig(ProductionConfig):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
        SECRET_KEY = "test-secret-key-for-testing-only"

    app = create_app(_FreshConfig)

    yield app

    # Teardown — clean up the scoped session and drop tables
    with app.app_context():
        db.session.remove()
        db.drop_all()

    # Restore the original environment
    for key, val in saved_env.items():
        if val is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = val


# ── Helpers ────────────────────────────────────────────────────────────────


def _head_revision(app) -> str | None:
    """Return the head migration revision from the scripts directory."""
    migrate_ext = app.extensions["migrate"]
    migrations_dir = Path(app.root_path).parent / migrate_ext.directory
    return ScriptDirectory(str(migrations_dir)).get_current_head()


def _current_revision(app) -> str | None:
    """Return the Alembic revision stamped in the database right now."""
    with db.engine.connect() as connection:
        context = MigrationContext.configure(connection)
        return context.get_current_revision()


def _capture_logs():
    """Return a (records_list, handler) pair attached to the startup logger."""
    startup_logger = logging.getLogger("app.services.startup_service")
    records: list[logging.LogRecord] = []

    class _CaptureHandler(logging.Handler):
        def emit(self, record):
            records.append(record)

    handler = _CaptureHandler(level=logging.DEBUG)
    startup_logger.addHandler(handler)
    return records, handler


def _stop_logs(handler):
    """Remove a previously attached capture handler."""
    logging.getLogger("app.services.startup_service").removeHandler(handler)


# ── Tests ──────────────────────────────────────────────────────────────────


class TestStartupService:
    """Comprehensive tests for StartupService automatic initialization."""

    # ── Empty database ──────────────────────────────────────────────────

    def test_empty_database_applies_migrations_and_creates_admin(
        self, fresh_prod_app
    ):
        """A fresh empty database gets migrations applied and admin created."""
        app = fresh_prod_app
        os.environ["APP_ENV"] = "production"
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ["ADMIN_PASSWORD"] = "securepassword123"

        records, handler = _capture_logs()
        try:
            StartupService.run(app)
        finally:
            _stop_logs(handler)

        messages = [r.getMessage() for r in records]

        # Migrations were applied
        with app.app_context():
            assert _current_revision(app) == _head_revision(app)

            # Admin user was created
            user = db.session.query(User).filter_by(
                email="admin@kwalitec.example"
            ).first()
            assert user is not None
            assert user.check_password("securepassword123") is True
            assert user.is_active_user is True

        # Structured log messages
        assert "Startup initialization beginning..." in messages
        assert "Applying migrations..." in messages
        assert "Migrations complete." in messages
        assert "Admin created." in messages
        assert "Startup initialization complete." in messages

    # ── Already migrated ────────────────────────────────────────────────

    def test_already_migrated_database_skips_migrations(self, fresh_prod_app):
        """An already-migrated database does not reapply migrations."""
        app = fresh_prod_app

        # First run — apply migrations + create admin
        os.environ["APP_ENV"] = "production"
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ["ADMIN_PASSWORD"] = "securepassword123"
        StartupService.run(app)

        # Second run — should find DB up to date
        records, handler = _capture_logs()
        try:
            StartupService.run(app)
        finally:
            _stop_logs(handler)

        messages = [r.getMessage() for r in records]

        assert "Database schema up to date." in messages
        assert "Applying migrations..." not in messages
        assert "Admin already exists." in messages

    # ── Existing admin ──────────────────────────────────────────────────

    def test_existing_admin_not_recreated(self, fresh_prod_app):
        """An existing admin user is never recreated."""
        app = fresh_prod_app

        # First run — create admin
        os.environ["APP_ENV"] = "production"
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ["ADMIN_PASSWORD"] = "securepassword123"
        StartupService.run(app)

        # Second run
        records, handler = _capture_logs()
        try:
            StartupService.run(app)
        finally:
            _stop_logs(handler)

        messages = [r.getMessage() for r in records]

        assert "Admin already exists." in messages
        assert "Admin created." not in messages

        # Still only one user
        with app.app_context():
            assert db.session.query(User).count() == 1

    # ── Missing admin credentials ───────────────────────────────────────

    def test_missing_admin_credentials_logs_warning(self, fresh_prod_app):
        """Missing ADMIN_EMAIL/ADMIN_PASSWORD logs a warning, no crash."""
        app = fresh_prod_app
        os.environ["APP_ENV"] = "production"
        os.environ.pop("ADMIN_EMAIL", None)
        os.environ.pop("ADMIN_PASSWORD", None)

        records, handler = _capture_logs()
        try:
            StartupService.run(app)
        finally:
            _stop_logs(handler)

        messages = [r.getMessage() for r in records]

        # Migrations were still applied
        with app.app_context():
            assert _current_revision(app) == _head_revision(app)
            assert db.session.query(User).count() == 0

        # Warning logged for both missing vars
        assert any("ADMIN_EMAIL" in m and "ADMIN_PASSWORD" in m for m in messages)
        # Startup completed without crashing
        assert "Startup initialization complete." in messages

    def test_missing_only_email_logs_warning(self, fresh_prod_app):
        """Missing ADMIN_EMAIL (but password present) logs a warning."""
        app = fresh_prod_app
        os.environ["APP_ENV"] = "production"
        os.environ.pop("ADMIN_EMAIL", None)
        os.environ["ADMIN_PASSWORD"] = "securepassword123"

        records, handler = _capture_logs()
        try:
            StartupService.run(app)
        finally:
            _stop_logs(handler)

        messages = [r.getMessage() for r in records]
        assert any("ADMIN_EMAIL" in m for m in messages)

        with app.app_context():
            assert db.session.query(User).count() == 0

    def test_missing_only_password_logs_warning(self, fresh_prod_app):
        """Missing ADMIN_PASSWORD (but email present) logs a warning."""
        app = fresh_prod_app
        os.environ["APP_ENV"] = "production"
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ.pop("ADMIN_PASSWORD", None)

        records, handler = _capture_logs()
        try:
            StartupService.run(app)
        finally:
            _stop_logs(handler)

        messages = [r.getMessage() for r in records]
        assert any("ADMIN_PASSWORD" in m for m in messages)

        with app.app_context():
            assert db.session.query(User).count() == 0

    # ── Migration failure ───────────────────────────────────────────────

    def test_migration_failure_does_not_crash(self, fresh_prod_app):
        """A migration failure is caught and does not prevent startup."""
        app = fresh_prod_app
        os.environ["APP_ENV"] = "production"
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ["ADMIN_PASSWORD"] = "securepassword123"

        records, handler = _capture_logs()
        try:
            with patch(
                "app.services.startup_service.command.upgrade",
                side_effect=RuntimeError("simulated migration failure"),
            ):
                StartupService.run(app)
        finally:
            _stop_logs(handler)

        messages = [r.getMessage() for r in records]

        # Function returned normally (app can still start)
        assert any("Startup initialization failed" in m for m in messages)

        # No admin user created (migrations failed before admin step).
        # The users table may not exist because migrations were mocked to
        # fail, so we guard the query against that.
        with app.app_context():
            try:
                assert db.session.query(User).count() == 0
            except (OperationalError, ProgrammingError):
                # Table doesn't exist — exactly what we expect when
                # migrations never ran.
                pass

    # ── Idempotent repeated startup ─────────────────────────────────────

    def test_idempotent_repeated_startup(self, fresh_prod_app):
        """Running startup multiple times is idempotent."""
        app = fresh_prod_app
        os.environ["APP_ENV"] = "production"
        os.environ["ADMIN_EMAIL"] = "admin@kwalitec.example"
        os.environ["ADMIN_PASSWORD"] = "securepassword123"

        # Run three times
        for _ in range(3):
            StartupService.run(app)

        with app.app_context():
            # Only one admin user
            assert db.session.query(User).count() == 1
            user = db.session.query(User).filter_by(
                email="admin@kwalitec.example"
            ).first()
            assert user is not None
            assert user.check_password("securepassword123") is True

    # ── Environment gating ──────────────────────────────────────────────

    def test_no_op_in_development(self, fresh_prod_app):
        """StartupService is a no-op when APP_ENV is development."""
        app = fresh_prod_app
        os.environ["APP_ENV"] = "development"

        records, handler = _capture_logs()
        try:
            StartupService.run(app)
        finally:
            _stop_logs(handler)

        messages = [r.getMessage() for r in records]
        assert "Startup initialization beginning..." not in messages

        # The service is a no-op, so no tables were created.  Querying the
        # users table would raise; instead we verify via the Alembic
        # revision that nothing was applied.
        with app.app_context():
            assert _current_revision(app) is None

    def test_no_op_in_testing(self, fresh_prod_app):
        """StartupService is a no-op when APP_ENV is testing."""
        app = fresh_prod_app
        os.environ["APP_ENV"] = "testing"

        records, handler = _capture_logs()
        try:
            StartupService.run(app)
        finally:
            _stop_logs(handler)

        messages = [r.getMessage() for r in records]
        assert "Startup initialization beginning..." not in messages

    # ── Unit tests for _should_run ──────────────────────────────────────

    def test_should_run_true_for_production(self):
        """_should_run returns True when APP_ENV is production."""
        os.environ["APP_ENV"] = "production"
        assert StartupService._should_run() is True

    def test_should_run_false_for_development(self):
        """_should_run returns False when APP_ENV is development."""
        os.environ["APP_ENV"] = "development"
        assert StartupService._should_run() is False

    def test_should_run_false_for_testing(self):
        """_should_run returns False when APP_ENV is testing."""
        os.environ["APP_ENV"] = "testing"
        assert StartupService._should_run() is False

    def test_should_run_false_when_unset(self):
        """_should_run returns False when APP_ENV is not set."""
        os.environ.pop("APP_ENV", None)
        assert StartupService._should_run() is False

    def test_should_run_case_insensitive(self):
        """_should_run is case-insensitive."""
        os.environ["APP_ENV"] = "Production"
        assert StartupService._should_run() is True

        os.environ["APP_ENV"] = "PRODUCTION"
        assert StartupService._should_run() is True

