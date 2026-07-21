"""Alembic environment for Education OS SQLAlchemy persistence (INF-009)."""

from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from infrastructure.persistence.sqlalchemy import models as _models  # noqa: F401
from infrastructure.persistence.sqlalchemy.metadata import metadata

config = context.config

if config.config_file_name is not None:
    # Keep application loggers (e.g. StartupService) enabled when Alembic
    # configures its own handlers — disable_existing_loggers=True would
    # silence them for the rest of the process.
    fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = metadata


def _database_url() -> str:
    url = config.get_main_option("sqlalchemy.url")
    if url:
        return url
    return os.environ.get(
        "EOS_DATABASE_URL",
        "sqlite:///instance/eos_persistence.sqlite3",
    )


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""
    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = _database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
