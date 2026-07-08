"""Tests for application configuration."""

from __future__ import annotations


class TestConfig:
    """Tests for config loading and environment variable handling."""

    def test_development_config_defaults(self, app):
        from app.config import DevelopmentConfig

        config = DevelopmentConfig()
        assert config.DEBUG is True
        assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False
        assert config.WTF_CSRF_ENABLED is True

    def test_production_config_defaults(self, app):
        from app.config import ProductionConfig

        config = ProductionConfig()
        assert config.DEBUG is False

    def test_database_uri_sqlite_default(self, app):
        from app.config import _database_uri
        import os

        # Remove DATABASE_URL to force SQLite fallback
        old_url = os.environ.pop("DATABASE_URL", None)
        try:
            uri = _database_uri()
            assert uri.endswith(".sqlite3") or "sqlite" in uri
        finally:
            if old_url:
                os.environ["DATABASE_URL"] = old_url

    def test_postgres_url_rewrite_legacy_scheme(self):
        """Verify that postgres:// is rewritten to postgresql+psycopg://."""
        from app.config import _normalize_postgres_url

        url = "postgres://user:pass@host:5432/db"
        result = _normalize_postgres_url(url)
        assert result == "postgresql+psycopg://user:pass@host:5432/db"

    def test_postgres_url_rewrite_modern_scheme(self):
        """Verify that postgresql:// (Render's format) is rewritten to psycopg v3."""
        from app.config import _normalize_postgres_url

        url = "postgresql://user:pass@host:5432/db"
        result = _normalize_postgres_url(url)
        assert result == "postgresql+psycopg://user:pass@host:5432/db"

    def test_postgres_url_already_has_psycopg_driver(self):
        """Verify that an explicit psycopg driver is left untouched."""
        from app.config import _normalize_postgres_url

        url = "postgresql+psycopg://user:pass@host:5432/db"
        result = _normalize_postgres_url(url)
        assert result == "postgresql+psycopg://user:pass@host:5432/db"

    def test_sqlalchemy_driver_prefix_safe(self):
        """Verify the driver prefix helper exposes no credentials."""
        from app.config import _sqlalchemy_driver_prefix

        assert _sqlalchemy_driver_prefix(
            "postgresql+psycopg://user:pass@host:5432/db"
        ) == "postgresql+psycopg://"
        assert _sqlalchemy_driver_prefix(
            "postgresql://user:pass@host:5432/db"
        ) == "postgresql://"
        assert "pass" not in _sqlalchemy_driver_prefix(
            "postgresql+psycopg://user:pass@host:5432/db"
        )

    def test_secret_key_default(self, app):
        from app.config import BaseConfig
        import os

        old_key = os.environ.pop("SECRET_KEY", None)
        try:
            config = BaseConfig()
            assert len(config.SECRET_KEY) > 0
        finally:
            if old_key:
                os.environ["SECRET_KEY"] = old_key


class TestApplicationFactory:
    """Tests for the application factory."""

    def test_create_app_returns_flask_app(self, app):
        from flask import Flask

        assert isinstance(app, Flask)

    def test_app_is_testing(self, app):
        assert app.config["TESTING"] is True

    def test_root_route_redirects(self, app):
        with app.test_client() as client:
            resp = client.get("/")
            assert resp.status_code in (301, 302)

    def test_extensions_initialized(self, app):
        from app.extensions import db, migrate, login_manager, csrf

        assert db is not None
        assert migrate is not None
        assert login_manager is not None
        assert csrf is not None

    def test_blueprints_registered(self, app):
        blueprints = [bp.name for bp in app.iter_blueprints()]
        assert "auth" in blueprints
        assert "dashboard" in blueprints
        assert "analytics" in blueprints
        assert "mission" in blueprints
        assert "study_plan" in blueprints
        assert "settings" in blueprints