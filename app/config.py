"""Configuration classes for the Kwalitec Flask application."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"


def _database_uri() -> str:
    """Return the configured database URI.

    PostgreSQL is used automatically when DATABASE_URL exists. Otherwise the
    development SQLite database in the instance folder is used.
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)

    return f"sqlite:///{INSTANCE_DIR / 'kwalitec.sqlite3'}"


class BaseConfig:
    """Shared application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-this-secret-key")
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
