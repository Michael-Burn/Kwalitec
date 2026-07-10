"""Configuration classes for the Kwalitec Flask application."""

from __future__ import annotations

import logging
import os
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


class BaseConfig:
    """Shared application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-this-secret-key")
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}