"""Application factory for Kwalitec."""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from flask import Flask, jsonify, redirect, render_template, request, url_for

from app.config import DevelopmentConfig, ProductionConfig, _sqlalchemy_driver_prefix
from app.extensions import csrf, db, login_manager, migrate

logger = logging.getLogger(__name__)


def _configure_logging(app: Flask) -> None:
    """Configure application logging based on environment."""
    log_level = logging.DEBUG if app.debug else logging.INFO
    log_format = (
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        if not app.debug
        else "[%(levelname)s] %(name)s: %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(log_format))

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    # Remove existing handlers to avoid duplicates in dev reload
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Silence noisy libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    logger.info("Kwalitec logging configured at level %s", logging.getLevelName(log_level))


def _validate_env_vars() -> None:
    """Validate required environment variables at startup.

    Logs warnings for missing or default values that need attention.
    """
    issues = []

    secret_key = os.getenv("SECRET_KEY", "dev-change-this-secret-key")
    if secret_key == "dev-change-this-secret-key":
        app_env = os.getenv("APP_ENV", "development")
        if app_env == "production":
            issues.append("SECRET_KEY is using the default insecure value in production!")
        else:
            logger.warning("SECRET_KEY is using the default value. Set a strong key for production use.")

    flask_env = os.getenv("FLASK_ENV", "development")
    app_env = os.getenv("APP_ENV", flask_env)
    logger.info("Environment: APP_ENV=%s, FLASK_ENV=%s", app_env, flask_env)

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        logger.info("Using external database (DATABASE_URL is set)")
    else:
        logger.info("Using local SQLite database (DATABASE_URL is not set)")

    # Temporary diagnostic: log only the SQLAlchemy driver prefix (no credentials)
    try:
        driver_prefix = _sqlalchemy_driver_prefix()
        logger.info("SQLAlchemy database driver prefix: %s", driver_prefix)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not determine SQLAlchemy driver prefix: %s", exc)

    if issues:
        for issue in issues:
            logger.error("CONFIGURATION ERROR: %s", issue)
        # In production, raise to prevent insecure deployment
        if app_env == "production":
            raise RuntimeError("Configuration validation failed: " + "; ".join(issues))


def _log_migration_state(app: Flask) -> None:
    """Log the current Alembic revision and whether migrations are up to date.

    This is a read-only diagnostic: it never applies migrations. It compares
    the revision stored in the database (``alembic_version`` table) against
    the head revision in the migration scripts directory and logs the result
    so deployment issues can be diagnosed from the startup log.
    """
    try:
        with app.app_context():
            migrate_cfg = app.extensions["migrate"]
            migrations_dir = Path(app.root_path).parent / migrate_cfg.directory

            # Head revision from the migration scripts on disk
            script_dir = ScriptDirectory(str(migrations_dir))
            head_revision = script_dir.get_current_head()

            # Current revision stamped in the database
            with db.engine.connect() as connection:
                context = MigrationContext.configure(connection)
                current_revision = context.get_current_revision()

        if current_revision is None:
            logger.warning(
                "Alembic: no revision recorded in database "
                "(alembic_version table empty or missing). "
                "Migrations have NOT been applied."
            )
        else:
            logger.info("Alembic: current database revision = %s", current_revision)

        if head_revision is not None:
            logger.info("Alembic: head script revision = %s", head_revision)
            if current_revision == head_revision:
                logger.info("Alembic: database is up to date.")
            else:
                logger.warning(
                    "Alembic: database is BEHIND head "
                    "(db=%s, head=%s). Migrations need to be applied.",
                    current_revision,
                    head_revision,
                )
        else:
            logger.warning("Alembic: no migration scripts found on disk.")
    except Exception as exc:  # noqa: BLE001
        logger.warning(
            "Alembic: could not determine migration state (%s: %s)",
            exc.__class__.__name__,
            exc,
        )


def _register_error_handlers(app: Flask) -> None:
    """Register custom error handlers for HTTP error codes.

    The 500 handler is only registered when exceptions are not being
    propagated (i.e. production).  In development/debug mode exceptions
    are allowed to propagate so the interactive debugger can display the
    traceback instead of swallowing the error with a custom page.
    """

    @app.errorhandler(403)
    def forbidden(error):
        logger.warning("403 Forbidden: %s %s", request.method, request.path)
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        logger.info("404 Not Found: %s %s", request.method, request.path)
        return render_template("errors/404.html"), 404

    if not app.config.get("PROPAGATE_EXCEPTIONS", False):

        @app.errorhandler(500)
        def internal_server_error(error):
            logger.exception("500 Internal Server Error at %s %s", request.method, request.path)
            db.session.rollback()
            return render_template("errors/500.html"), 500


def _register_health_check(app: Flask) -> None:
    """Register a health-check endpoint."""

    @app.get("/health")
    def health_check():
        db_status = "connected"
        try:
            db.session.execute(db.text("SELECT 1"))
        except Exception as exc:
            db_status = "error"
            logger.error("Health check database error: %s", exc)

        return jsonify(
            {
                "status": "ok" if db_status == "connected" else "degraded",
                "database": db_status,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "version": "1.0.0",
            }
        )


def _add_security_headers(response):
    """Add security headers to every response."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "0"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
        "magnetometer=(), microphone=(), payment=(), usb=()"
    )

    # Content-Security-Policy
    app_env = os.getenv("APP_ENV", "development")
    is_production = app_env == "production"

    if is_production:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'"
        )
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
    else:
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "connect-src 'self'"
        )

    response.headers["Cache-Control"] = "no-store"

    return response


def create_app(config_object: type | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    if config_object is None:
        config_object = _select_config()

    app.config.from_object(config_object)

    _configure_logging(app)
    _validate_env_vars()
    _init_extensions(app)
    _register_blueprints(app)
    _register_cli_commands(app)
    _register_routes(app)
    _register_error_handlers(app)
    _register_health_check(app)
    app.after_request(_add_security_headers)

    # Diagnose migration state at startup (read-only; never applies migrations)
    _log_migration_state(app)

    # Production-only: apply migrations and bootstrap the admin user on the
    # first application startup. Safe, idempotent, and never prevents the app
    # from starting. No-op in development and testing.
    from app.services.startup_service import StartupService

    StartupService.run(app)

    logger.info("Kwalitec application created successfully")
    return app


def _select_config() -> type:
    """Select the correct configuration based on the environment."""
    flask_env = os.getenv("FLASK_ENV", "development").lower()
    app_env = os.getenv("APP_ENV", flask_env).lower()

    if app_env == "production":
        return ProductionConfig

    return DevelopmentConfig


def _init_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = ""
    login_manager.login_message_category = "info"

    # Import models to register them with SQLAlchemy
    from app.models import (  # noqa: F401
        Curriculum,
        Decision,
        LearningObjective,
        Mission,
        MissionTask,
        Mistake,
        StudyAttempt,
        StudyPlan,
        Subject,
        Topic,
        TopicProgress,
        TwinSnapshot,
        User,
        WeekPlan,
    )


def _register_cli_commands(app: Flask) -> None:
    """Register custom CLI commands."""
    from app.cli import (
        backfill_sections_command,
        create_admin_command,
        create_test_user_command,
    )

    app.cli.add_command(create_admin_command)
    app.cli.add_command(create_test_user_command)
    app.cli.add_command(backfill_sections_command)


def _register_blueprints(app: Flask) -> None:
    """Register application blueprints."""
    from app.analytics.routes import analytics_bp
    from app.auth.routes import auth_bp
    from app.calibration import calibration_bp
    from app.dashboard.routes import dashboard_bp
    from app.mission.routes import mission_bp
    from app.settings.routes import settings_bp
    from app.study_plan.routes import study_plan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(mission_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(study_plan_bp)
    app.register_blueprint(calibration_bp)


def _register_routes(app: Flask) -> None:
    """Register simple application-level routes."""

    @app.get("/")
    def index():
        return redirect(url_for("dashboard.index"))
