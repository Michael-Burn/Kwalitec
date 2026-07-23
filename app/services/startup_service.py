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
import sys
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

        The curriculum import runs in **all** environments so that bundled
        official curricula are available automatically on a fresh database.
        Migrations and admin creation remain production-only.
        """
        try:
            with app.app_context():
                logger.info("Startup initialization beginning...")
                if StartupService._should_run():
                    StartupService._apply_migrations(app)
                    StartupService._ensure_admin()
                StartupService._run_curriculum_import(app)
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
    def _is_flask_cli_command() -> bool:
        """Return True if the current process is a Flask CLI command.
        
        Detects Flask CLI commands (flask db upgrade, flask db migrate,
        flask shell, flask routes, etc.) to prevent curriculum import
        from running during database migrations or other CLI operations.
        """
        # Check if we're running via the flask command
        if sys.argv[0].endswith("flask") or "flask" in sys.argv[0]:
            return True
        
        # Check if the first argument is a flask subcommand
        if len(sys.argv) > 1 and sys.argv[1] in (
            "db", "shell", "routes", "run", "test", "test-discovery"
        ):
            return True
        
        return False

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

        # Create the administrator with Founder + Console RBAC (PR-001).
        user = User(email=email.strip().lower(), is_active_user=True)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        from app.services.identity_service import IdentityService

        IdentityService.ensure_founder_admin(user)
        logger.info("Admin created with Founder RBAC.")


    @staticmethod
    def _table_exists(table_name: str) -> bool:
        """Check if a database table exists.
        
        Uses SQLAlchemy's inspector to safely check table existence without
        raising exceptions.
        """
        from sqlalchemy import inspect
        
        try:
            inspector = inspect(db.engine)
            return inspector.has_table(table_name)
        except Exception as exc:  # noqa: BLE001
            logger.debug(
                "Could not check if table '%s' exists (%s: %s)",
                table_name,
                exc.__class__.__name__,
                exc,
            )
            return False

    @staticmethod
    def _run_curriculum_import(app: Flask) -> None:
        """Idempotently import bundled curricula into the database.
        
        Skips import if:
        - The curricula table does not yet exist (e.g., during ``flask db upgrade``)
        - The process is a Flask CLI command (to avoid interfering with migrations)
        
        Curriculum import only runs when the web application actually starts
        serving requests, not during Flask CLI commands.
        """
        # Skip if running a Flask CLI command (db upgrade, migrate, shell, etc.)
        if StartupService._is_flask_cli_command():
            logger.debug(
                "Skipping curriculum import during Flask CLI command. "
                "Import will run on next normal application startup."
            )
            return
        
        # Skip if the curricula table doesn't exist yet
        if not StartupService._table_exists("curricula"):
            logger.debug(
                "Curricula table does not exist yet; skipping curriculum import. "
                "Import will run on next normal application startup."
            )
            return
        
        try:
            from app.services.curriculum_service import CurriculumService
            count = CurriculumService.import_curricula()
            if count:
                logger.info("Imported %d new curricula.", count)
            else:
                logger.debug("All curricula already present.")
        except Exception as exc:
            logger.exception("Curriculum import failed: %s", exc)
