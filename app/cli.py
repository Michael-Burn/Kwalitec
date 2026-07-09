"""Custom Flask CLI commands for Kwalitec administration tasks."""

from __future__ import annotations

import logging
import os
import sys

import click
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.extensions import db
from app.models.user import User

logger = logging.getLogger(__name__)


def _users_table_exists() -> bool:
    """Return True if the ``users`` table exists in the current database.

    On a fresh database (before migrations have run) the table will be
    absent.  We probe with a lightweight query and interpret any
    schema-level error as "table missing" so the caller can degrade
    gracefully instead of crashing the deploy.
    """
    try:
        db.session.execute(db.text("SELECT 1 FROM users LIMIT 1"))
        return True
    except (OperationalError, ProgrammingError) as exc:
        logger.warning(
            "create-admin: users table not available (%s); "
            "assuming migrations have not run yet",
            exc.__class__.__name__,
        )
        return False


@click.command("create-admin")
def create_admin_command() -> None:
    """Create the initial administrator user from environment variables.

    Reads ADMIN_EMAIL and ADMIN_PASSWORD from the environment. If any
    User record already exists the command exits successfully without
    modifying the database.

    If the ``users`` table does not yet exist (migrations have not been
    applied) the command logs a warning and exits successfully, assuming
    migrations will be applied separately. This keeps the command safe
    to run on every deploy regardless of migration ordering.

    Environment Variables:
        ADMIN_EMAIL:    Administrator email address (required on first run)
        ADMIN_PASSWORD: Administrator plaintext password (required on first run)

    Exit codes:
        0 – Administrator already exists, was created, or migrations are pending
        1 – Required environment variable is missing
    """
    logger.info("Starting create-admin command")

    # If the schema is not present yet, do not crash the deploy.
    # Migrations are expected to run separately (e.g. via `db upgrade`).
    if not _users_table_exists():
        click.echo(
            "users table not found – skipping create-admin "
            "(migrations may not have run yet)."
        )
        logger.warning(
            "create-admin: users table missing; skipping creation. "
            "Run `flask --app wsgi.py db upgrade` before create-admin."
        )
        return

    # Check whether any users already exist
    user_count: int = db.session.query(User).count()
    if user_count > 0:
        click.echo("Administrator already exists.")
        logger.info(
            "create-admin: %d existing user(s) found – skipping creation",
            user_count,
        )
        return

    # Read credentials from the environment
    email: str | None = os.getenv("ADMIN_EMAIL")
    password: str | None = os.getenv("ADMIN_PASSWORD")

    # Validate that both are present
    missing: list[str] = []
    if not email:
        missing.append("ADMIN_EMAIL")
    if not password:
        missing.append("ADMIN_PASSWORD")

    if missing:
        msg = (
            "Missing required environment variable(s): "
            + ", ".join(missing)
            + ". Set these variables and retry."
        )
        click.echo(f"Error: {msg}", err=True)
        logger.error("create-admin: %s", msg)
        sys.exit(1)

    # Create the administrator
    user = User(email=email, is_active_user=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    click.echo("Administrator created successfully.")
    logger.info(
        "create-admin: administrator created for email=%s", email
    )