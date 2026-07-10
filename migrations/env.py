"""Alembic environment for Flask-Migrate."""

from __future__ import annotations

import logging
from logging.config import fileConfig

from alembic import context
from flask import current_app

config = context.config
# Guard fileConfig: when Alembic runs programmatically (e.g. via
# StartupService) config_file_name may be None, and re-applying the
# alembic.ini logging config would clobber the application's logging setup.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_db = current_app.extensions["migrate"].db
target_metadata = target_db.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""
    connectable = target_db.get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            **current_app.extensions["migrate"].configure_args,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()