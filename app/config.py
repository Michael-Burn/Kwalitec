"""Configuration classes for the Kwalitec Flask application."""

from __future__ import annotations

import logging
import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"

logger = logging.getLogger(__name__)


def _normalize_postgres_url(url: str) -> str:
    """Normalize a PostgreSQL URL to use the psycopg v3 driver.

    Render (and some other hosts) expose ``DATABASE_URL`` using either the
    legacy ``postgres://`` scheme or the modern ``postgresql://`` scheme, both
    without an explicit DBAPI driver.  When SQLAlchemy receives a bare
    ``postgresql://`` URL it defaults to the ``psycopg2`` dialect, which is not
    installed in this project (we use ``psycopg`` v3 exclusively).

    This helper rewrites both bare schemes to ``postgresql+psycopg://`` so
    SQLAlchemy selects the psycopg v3 dialect.  URLs that already specify a
    driver (e.g. ``postgresql+psycopg://``) are left untouched.
    """
    parts = urlsplit(url)
    scheme = parts.scheme.lower()

    if scheme in {"postgres", "postgresql"}:
        # Replace only the scheme, preserving everything else (credentials,
        # host, port, path, query, fragment) exactly as provided.
        return url.replace(f"{scheme}://", "postgresql+psycopg://", 1)

    return url


def _database_uri() -> str:
    """Return the configured database URI.

    PostgreSQL is used automatically when DATABASE_URL exists. Otherwise the
    development SQLite database in the instance folder is used.
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return _normalize_postgres_url(database_url)

    return f"sqlite:///{INSTANCE_DIR / 'kwalitec.sqlite3'}"


def _sqlalchemy_driver_prefix(uri: str | None = None) -> str:
    """Return the SQLAlchemy driver prefix of a URI, without credentials.

    For example::

        postgresql+psycopg://user:pass@host:5432/db  ->  "postgresql+psycopg://"
        postgresql://user:pass@host:5432/db          ->  "postgresql://"
        sqlite:///path/to.db                         ->  "sqlite:///"

    This is safe to log because it contains no host, credentials, or path.
    """
    if uri is None:
        uri = _database_uri()
    parts = urlsplit(uri)
    if parts.scheme:
        return f"{parts.scheme}://"
    # Fallback: everything up to the first "://" (covers malformed inputs).
    if "://" in uri:
        return uri.split("://", 1)[0] + "://"
    return uri


def _is_postgres_uri(uri: str | None = None) -> bool:
    """Return True when the configured URI uses a PostgreSQL dialect."""
    prefix = _sqlalchemy_driver_prefix(uri).lower()
    return prefix.startswith("postgresql") or prefix.startswith("postgres")


def _engine_options() -> dict:
    """Return SQLAlchemy engine options (pool tuning for PostgreSQL)."""
    if not _is_postgres_uri():
        return {}
    return {
        "pool_pre_ping": True,
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "1800")),
        "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
    }


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not str(raw).strip():
        return default
    try:
        return int(raw)
    except ValueError:
        return default


class BaseConfig:
    """Shared application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-this-secret-key")
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = _engine_options()
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # session-bound tokens; audit in production docs

    # Session defaults (overridden for production hardening).
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(
        hours=_env_int("SESSION_LIFETIME_HOURS", 12)
    )

    # Trusted reverse-proxy hop count (Render / nginx). 0 disables ProxyFix.
    TRUSTED_PROXY_HOPS = _env_int("TRUSTED_PROXY_HOPS", 0)

    # Prefer HTTPS URL generation when behind TLS termination.
    PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", "http")

    # Observability thresholds (ms).
    SLOW_REQUEST_THRESHOLD_MS = _env_int("SLOW_REQUEST_THRESHOLD_MS", 1000)
    HEALTH_ALERT_DB_LATENCY_MS = _env_int("HEALTH_ALERT_DB_LATENCY_MS", 500)


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(BaseConfig):
    """Isolated configuration for automated tests."""

    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ENGINE_OPTIONS = {}
    TRUSTED_PROXY_HOPS = 0


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False
    PREFERRED_URL_SCHEME = "https"
    TRUSTED_PROXY_HOPS = _env_int("TRUSTED_PROXY_HOPS", 1)

    # Session cookie hardening (HTTPS deployments; Render terminates TLS).
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Flask-Login remember-me cookie — mirror session flags.
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"

    # Browser-cache fingerprinted / versioned static assets for one year.
    # HTML responses still receive Cache-Control: no-store via middleware.
    SEND_FILE_MAX_AGE_DEFAULT = 31_536_000


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
