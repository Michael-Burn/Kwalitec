"""Custom Flask CLI commands for Kwalitec administration tasks."""

from __future__ import annotations

import logging
import os
import sys

import click

from app.extensions import db
from app.models.user import User

logger = logging.getLogger(__name__)


@click.command("create-admin")
def create_admin_command() -> None:
    """Create the initial administrator user from environment variables.

    Reads ADMIN_EMAIL and ADMIN_PASSWORD from the environment. If any
    User record already exists the command exits successfully without
    modifying the database.

    Environment Variables:
        ADMIN_EMAIL:    Administrator email address (required on first run)
        ADMIN_PASSWORD: Administrator plaintext password (required on first run)

    Exit codes:
        0 – Administrator already exists or was successfully created
        1 – Required environment variable is missing
    """
    logger.info("Starting create-admin command")

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