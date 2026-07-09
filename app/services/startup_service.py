"""Startup initialization service for production deployments.

On first application startup in production, this service:

1. Applies pending Alembic migrations (equivalent to ``flask db upgrade``)
   using Alembic's Python API rather than a subprocess.
2. Creates the initial administrator user from the ``ADMIN_EMAIL`` and
   ``ADMIN_PASSWORD`` environment variables.

The service is **idempotent**, never drops tables, never recreates existing
users, never rerun migrations unnecessarily, and catches every exception so
the Flask application can always start.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from alembic import command
from alembic.config import Config as AlembicConfig
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from flask import Flask
from sqlalchemy.exc import OperationalError, ProgrammingError

from app.extensions import db

logger = logging.getLogger(__name__)


class StartupService:
    """Production-safe startup initializer.

    Runs exactly once when the application factory creates the app, but
    only performs work when ``APP_ENV == production``. In all other
    environments (development, testing) it is a no-op.
    """

    # ── Public API ────────────────────────────────────────────────────────

    @staticmethod
    def run(app: Flask) -> None:
        """Execute startup initialization.

        This is the single entry point called from the application factory.
        It never raises — all exceptions are caught and logged so the Flask
        application can always start.
        """
        if not StartupService._should_run():
            return

        try:
            with app.app_context():
                logger.info("Startup initialization beginning...")
                StartupService._apply_migrations(app)
                StartupService._ensure_admin()
                logger.info("Startup initialization complete.")
        except Exception as exc:  # noqa: BLE001
            logger.exception(
                "Startup initialization failed: %s: %s",
                exc.__class__.__name__,
                exc,
            )

    # ── Internal helpers ──────────────────────────────────────────────────

    @staticmethod
    def _should_run() -> bool:
        """Return True only when ``APP_ENV`` is production."""
        return os.getenv("APP_ENV", "development").lower() == "production"

    @staticmethod
    def _apply_migrations(app: Flask) -> None:
        """Apply pending Alembic migrations if the database is behind head.

        Compares the revision stamped in the database against the head
        revision from the migration scripts directory. If they match (or
        there are no scripts) the method returns immediately. Otherwise it
        runs ``alembic upgrade head`` programmatically.
        """
        migrate_ext = app.extensions["migrate"]
        migrations_dir = Path(app.root_path).parent / migrate_ext.directory

        # Head revision from the migration scripts on disk
        script_dir = ScriptDirectory(str(migrations_dir))
        try:
            head_revision = script_dir.get_current_head()
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Could not determine migration head revision: %s", exc
            )
            return

        if head_revision is None:
            logger.warning("No migration scripts found; skipping migrations.")
            return

        # Current revision stamped in the database
        try:
            with db.engine.connect() as connection:
                context = MigrationContext.configure(connection)
                current_revision = context.get_current_revision()
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Could not determine current migration revision (%s); "
                "assuming migrations have not been applied.",
                exc,
            )
            current_revision = None

        if current_revision == head_revision:
            logger.info("Database schema up to date.")
            return

        logger.info("Applying migrations...")
        cfg = StartupService._build_alembic_config(migrations_dir)
        command.upgrade(cfg, "head")
        logger.info("Migrations complete.")

    @staticmethod
    def _build_alembic_config(migrations_dir: Path) -> AlembicConfig:
        """Build an Alembic ``Config`` suitable for a programmatic upgrade.

        The ``env.py`` script reads the database URL from ``current_app`` at
        runtime, so we only need ``script_location``. We set
        ``sqlalchemy.url`` as well for completeness and offline-mode
        compatibility.
        """
        cfg = AlembicConfig()
        cfg.set_main_option("script_location", str(migrations_dir))
        url = str(db.engine.url).replace("%", "%%")
        cfg.set_main_option("sqlalchemy.url", url)
        return cfg

    @staticmethod
    def _ensure_admin() -> None:
        """Create the initial admin user if none exists.

        If any ``User`` record already exists the method returns immediately
        (idempotent — never recreates existing users). If no user exists but
        ``ADMIN_EMAIL`` or ``ADMIN_PASSWORD`` is missing, a warning is logged
        and startup continues without crashing.
        """
        from app.models.user import User

        # Check whether any user already exists
        try:
            user_count: int = db.session.query(User).count()
        except (OperationalError, ProgrammingError) as exc:
            logger.warning(
                "Could not query users table (%s); skipping admin creation.",
                exc.__class__.__name__,
            )
            return

        if user_count > 0:
            logger.info("Admin already exists.")
            return

        # Read credentials from the environment
        email = os.getenv("ADMIN_EMAIL")
        password = os.getenv("ADMIN_PASSWORD")

        if not email or not password:
            missing: list[str] = []
            if not email:
                missing.append("ADMIN_EMAIL")
            if not password:
                missing.append("ADMIN_PASSWORD")
            logger.warning(
                "No admin user exists and missing environment variable(s): "
                "%s. Skipping admin creation. Set these variables and "
                "restart to create the admin user.",
                ", ".join(missing),
            )
            return

        # Create the administrator
        user = User(email=email, is_active_user=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        logger.info("Admin created.")
