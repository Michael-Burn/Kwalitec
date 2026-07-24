"""Application factory for Kwalitec."""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from flask import Flask, jsonify, redirect, render_template, request, url_for

from app.config import (
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    _sqlalchemy_driver_prefix,
)
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


_INSECURE_SECRET_KEYS = frozenset(
    {
        "",
        "dev-change-this-secret-key",
        "change-this-secret-key",
        "change-me",
        "secret",
        "changeme",
        "test-secret-key-for-testing-only",
    }
)


def _validate_env_vars(config_object: type) -> None:
    """Validate required environment variables at startup.

    Rejects insecure ``SECRET_KEY`` values whenever production config is
    selected (via ``APP_ENV`` or ``FLASK_ENV``), not only when ``APP_ENV``
    is literally ``production``.
    """
    issues: list[str] = []

    secret_key = os.getenv("SECRET_KEY", "dev-change-this-secret-key")
    is_production_config = config_object is ProductionConfig
    if secret_key.strip() in _INSECURE_SECRET_KEYS:
        if is_production_config:
            issues.append(
                "SECRET_KEY is using an insecure default/placeholder with "
                "ProductionConfig active!"
            )
        else:
            logger.warning(
                "SECRET_KEY is using the default value. "
                "Set a strong key for production use."
            )
    elif is_production_config and len(secret_key.strip()) < 32:
        issues.append(
            "SECRET_KEY must be at least 32 characters in production."
        )

    flask_env = os.getenv("FLASK_ENV", "development")
    app_env = os.getenv("APP_ENV", flask_env)
    logger.info(
        "Environment: APP_ENV=%s, FLASK_ENV=%s, config=%s",
        app_env,
        flask_env,
        config_object.__name__,
    )

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        logger.info("Using external database (DATABASE_URL is set)")
    else:
        if is_production_config:
            issues.append(
                "DATABASE_URL is required when ProductionConfig is active "
                "(SQLite is not supported for production)."
            )
        else:
            logger.info("Using local SQLite database (DATABASE_URL is not set)")

    if is_production_config:
        admin_email = (os.getenv("ADMIN_EMAIL") or "").strip()
        admin_password = (os.getenv("ADMIN_PASSWORD") or "").strip()
        if not admin_email or not admin_password:
            logger.warning(
                "ADMIN_EMAIL / ADMIN_PASSWORD not fully set; "
                "bootstrap admin creation may be skipped."
            )
        csrf_enabled = True
        try:
            csrf_enabled = bool(getattr(config_object, "WTF_CSRF_ENABLED", True))
        except Exception:  # noqa: BLE001
            csrf_enabled = True
        if not csrf_enabled:
            issues.append("WTF_CSRF_ENABLED must remain True in production.")

    # Temporary diagnostic: log only the SQLAlchemy driver prefix (no credentials)
    try:
        driver_prefix = _sqlalchemy_driver_prefix()
        logger.info("SQLAlchemy database driver prefix: %s", driver_prefix)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not determine SQLAlchemy driver prefix: %s", exc)

    if issues:
        for issue in issues:
            logger.error("CONFIGURATION ERROR: %s", issue)
        if is_production_config:
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
    from app.infrastructure.diagnostics.http_observability import (
        allocate_error_reference_id,
    )

    @app.errorhandler(403)
    def forbidden(error):
        reference_id = allocate_error_reference_id()
        logger.warning(
            "403 Forbidden: %s %s correlation_id=%s",
            request.method,
            request.path,
            reference_id,
        )
        return (
            render_template(
                "errors/403.html",
                title="Access Denied",
                error_reference_id=reference_id,
            ),
            403,
        )

    @app.errorhandler(404)
    def page_not_found(error):
        reference_id = allocate_error_reference_id()
        logger.info(
            "404 Not Found: %s %s correlation_id=%s",
            request.method,
            request.path,
            reference_id,
        )
        return (
            render_template(
                "errors/404.html",
                title="Page Not Found",
                error_reference_id=reference_id,
            ),
            404,
        )

    if not app.config.get("PROPAGATE_EXCEPTIONS", False):

        @app.errorhandler(500)
        def internal_server_error(error):
            reference_id = allocate_error_reference_id()
            logger.exception(
                "500 Internal Server Error at %s %s correlation_id=%s",
                request.method,
                request.path,
                reference_id,
            )
            db.session.rollback()
            return (
                render_template(
                    "errors/500.html",
                    title="Error",
                    error_reference_id=reference_id,
                ),
                500,
            )


def _register_health_check(app: Flask) -> None:
    """Register liveness, readiness, and detailed health endpoints (PR-001)."""
    from app.services.health_service import HealthService
    from app.services.job_runner import dead_letters
    from app.services.release_info_service import ReleaseInfoService
    from app.version import APP_VERSION

    @app.get("/health")
    def health_check():
        """Compatibility probe — application + database summary."""
        payload = HealthService.aggregate(ready=False)
        db_component = payload.get("components", {}).get("database", {})
        db_status = db_component.get("status", "error")
        # Historical contract: top-level status reflects DB connectivity.
        if db_status == "ok":
            payload["status"] = "ok"
            payload["database"] = "connected"
            status_code = 200
        else:
            payload["status"] = "degraded" if db_status == "degraded" else "error"
            payload["database"] = "error"
            status_code = 503
        return jsonify(payload), status_code

    @app.get("/health/live")
    def health_live():
        """Process liveness — always 200 when the worker can answer."""
        release = ReleaseInfoService.current()
        return jsonify(
            {
                "status": "ok",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "version": APP_VERSION,
                "commit": release.commit,
            }
        )

    @app.get("/health/ready")
    def health_ready():
        """Readiness — database connected and migrations at head."""
        payload = HealthService.aggregate(ready=True)
        ready = bool(payload.get("ready"))
        status_code = 200 if ready else 503
        return jsonify(payload), status_code

    @app.get("/health/details")
    def health_details():
        """Operator-oriented health including dead-letter summary."""
        payload = HealthService.aggregate(ready=True)
        letters = dead_letters(limit=20)
        payload["dead_letters"] = [
            {
                "job_name": item.job_name,
                "attempts": item.attempts,
                "error": item.error,
                "failed_at": item.failed_at,
            }
            for item in letters
        ]
        payload["alerts"] = {
            "slow_request_threshold_ms": app.config.get(
                "SLOW_REQUEST_THRESHOLD_MS", 1000
            ),
            "db_latency_alert_ms": app.config.get(
                "HEALTH_ALERT_DB_LATENCY_MS", 500
            ),
        }
        status_code = 200 if payload["status"] != "error" else 503
        return jsonify(payload), status_code


def _is_static_response() -> bool:
    """Return True when the current request serves a static asset."""
    endpoint = request.endpoint or ""
    if endpoint == "static" or endpoint.endswith(".static"):
        return True
    path = request.path or ""
    return path.startswith("/static/")


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
        # 'unsafe-inline' is required for current templates (Analytics Chart.js
        # bootstrap, Product Check-in, Study Plan wizard step 4, and onsubmit
        # confirms). Prefer nonces/hashes + external JS in a later hardening pass.
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
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

    # Authenticated HTML stays uncached; versioned static assets may be cached.
    if _is_static_response():
        max_age = int(
            response.cache_control.max_age
            if response.cache_control.max_age is not None
            else 31_536_000
        )
        response.headers["Cache-Control"] = (
            f"public, max-age={max_age}, immutable"
        )
    else:
        response.headers["Cache-Control"] = "no-store"

    return response


def create_app(config_object: type | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    if config_object is None:
        config_object = _select_config()

    app.config.from_object(config_object)

    from app.version import STATIC_ASSET_VERSION

    # IAHF-005 — single source of truth for static cache-busting.
    app.config.setdefault("STATIC_ASSET_VERSION", STATIC_ASSET_VERSION)

    _configure_logging(app)
    _validate_env_vars(config_object)
    _init_extensions(app)
    _register_template_context(app)
    _register_blueprints(app)
    _register_cli_commands(app)
    _register_routes(app)
    _register_error_handlers(app)
    _register_health_check(app)
    from app.infrastructure.diagnostics.http_observability import (
        register_http_observability,
    )

    register_http_observability(app)
    from app.infrastructure.diagnostics.query_profiling import (
        register_query_profiling,
    )

    register_query_profiling(app)
    app.after_request(_add_security_headers)

    @app.url_defaults
    def _static_cache_bust(endpoint: str | None, values: dict) -> None:
        """Append ``v=`` fingerprint to static asset URLs (IAHF-005 safety net).

        Templates should use ``versioned_static()``; this also covers any
        remaining ``url_for('….static', …)`` calls in Python or Jinja.
        """
        if not endpoint:
            return
        if endpoint != "static" and not endpoint.endswith(".static"):
            return
        values.setdefault("v", app.config["STATIC_ASSET_VERSION"])

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
    if app_env in {"testing", "test"}:
        return TestingConfig

    return DevelopmentConfig


def _apply_proxy_fix(app: Flask) -> None:
    """Trust ``X-Forwarded-*`` headers from the configured proxy hop count."""
    hops = int(app.config.get("TRUSTED_PROXY_HOPS", 0) or 0)
    if hops <= 0:
        return
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(  # type: ignore[method-assign]
        app.wsgi_app,
        x_for=hops,
        x_proto=hops,
        x_host=hops,
        x_prefix=hops,
    )
    logger.info("Trusted proxy support enabled (hops=%s)", hops)


def _init_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    preferred_scheme = app.config.get("PREFERRED_URL_SCHEME")
    if preferred_scheme:
        app.config.setdefault("PREFERRED_URL_SCHEME", preferred_scheme)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    _apply_proxy_fix(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = ""
    login_manager.login_message_category = "info"

    # Import models to register them with SQLAlchemy
    from app.models import (  # noqa: F401
        AlphaFeedbackSubmission,
        Curriculum,
        Decision,
        LearningObjective,
        Mission,
        MissionTask,
        Mistake,
        PresentationEvent,
        ResearchContribution,
        ResearchContributorBadge,
        ResearchFeedbackReview,
        ResearchFeedbackSubmission,
        StudyAttempt,
        StudyPlan,
        Subject,
        Topic,
        TopicProgress,
        TwinSnapshot,
        User,
        UserCapability,
        UserRole,
        V2AggregateDocument,
        V2AggregateSnapshot,
        V2EvidenceEvent,
        VisionEntry,
        WeekPlan,
    )


def _resolve_v2_flags_for_templates():
    """Resolve V2 feature flags for dual-run template links."""
    from app.application.config.v2_flags import resolve_v2_feature_flags

    return resolve_v2_feature_flags()


def _register_template_context(app: Flask) -> None:
    """Inject shared presentation context into all templates."""
    from app.static_assets import versioned_static

    # IAHF-005 — reusable Jinja helper for cache-busted static URLs.
    app.jinja_env.globals["versioned_static"] = versioned_static

    @app.context_processor
    def inject_global_template_context():
        from app.brand_identity import (
            APPROVED_LOGO_ALT,
            APPROVED_LOGO_STATIC_PATH,
            CONSOLE_HOME_LABEL,
            FOUNDER_COMMAND_CENTRE_LABEL,
            FOUNDING_COHORT_LABEL,
            INTERNAL_ALPHA_BUILD_LABEL,
            INTERNAL_ALPHA_LABEL,
            KWALITEC_CONSOLE_LABEL,
            LEARNING_WORKSPACE_LABEL,
            PRODUCT_DESCRIPTOR,
            PRODUCT_NAME,
            PRODUCT_VALUE_PROPOSITION,
            REVISION_WORKSPACE_LABEL,
            STUDENT_DASHBOARD_LABEL,
        )
        from app.services.product_communication_service import (
            ProductCommunicationService,
        )
        from app.services.release_info_service import ReleaseInfoService
        from app.version import APP_VERSION, PRODUCT_TAGLINE, STATIC_ASSET_VERSION

        release_info = ReleaseInfoService.current()
        from app.security.authorization import (
            user_capabilities,
            user_has_capability,
            user_has_permission,
            user_has_role,
            user_permissions,
            user_roles,
        )
        from flask_login import current_user

        return {
            "app_version": APP_VERSION,
            "static_asset_version": STATIC_ASSET_VERSION,
            "product_tagline": PRODUCT_TAGLINE,
            "product_name": PRODUCT_NAME,
            "product_descriptor": PRODUCT_DESCRIPTOR,
            "product_value_proposition": PRODUCT_VALUE_PROPOSITION,
            "pcs": ProductCommunicationService,
            "internal_alpha_label": INTERNAL_ALPHA_LABEL,
            "founding_cohort_label": FOUNDING_COHORT_LABEL,
            "internal_alpha_build_label": INTERNAL_ALPHA_BUILD_LABEL,
            "founder_command_centre_label": FOUNDER_COMMAND_CENTRE_LABEL,
            "kwalitec_console_label": KWALITEC_CONSOLE_LABEL,
            "console_home_label": CONSOLE_HOME_LABEL,
            "learning_workspace_label": LEARNING_WORKSPACE_LABEL,
            "revision_workspace_label": REVISION_WORKSPACE_LABEL,
            "student_dashboard_label": STUDENT_DASHBOARD_LABEL,
            "approved_logo_static_path": APPROVED_LOGO_STATIC_PATH,
            "approved_logo_alt": APPROVED_LOGO_ALT,
            "versioned_static": versioned_static,
            "v2_flags": _resolve_v2_flags_for_templates(),
            "release_info": release_info,
            "support_contact": release_info.support_contact,
            # PR-001 — permission helpers only; no auth logic in templates.
            "can": lambda permission: user_has_permission(current_user, permission),
            "has_role": lambda role: user_has_role(current_user, role),
            "has_capability": lambda capability: user_has_capability(
                current_user, capability
            ),
            "current_user_roles": user_roles(current_user),
            "current_user_permissions": user_permissions(current_user),
            "current_user_capabilities": user_capabilities(current_user),
        }


def _register_cli_commands(app: Flask) -> None:
    """Register custom CLI commands."""
    from app.cli import (
        backfill_sections_command,
        create_admin_command,
        create_test_user_command,
        internal_alpha_reset_command,
    )
    from app.infrastructure.analytics.cli import (
        analytics_delete_user_command,
        analytics_export_audit_command,
        analytics_export_user_command,
        analytics_metrics_command,
        analytics_replay_command,
        analytics_retention_command,
        analytics_verify_consent_command,
        analytics_worker_once_command,
    )

    app.cli.add_command(create_admin_command)
    app.cli.add_command(create_test_user_command)
    app.cli.add_command(backfill_sections_command)
    app.cli.add_command(internal_alpha_reset_command)
    app.cli.add_command(analytics_worker_once_command)
    app.cli.add_command(analytics_replay_command)
    app.cli.add_command(analytics_retention_command)
    app.cli.add_command(analytics_delete_user_command)
    app.cli.add_command(analytics_export_user_command)
    app.cli.add_command(analytics_export_audit_command)
    app.cli.add_command(analytics_metrics_command)
    app.cli.add_command(analytics_verify_consent_command)


def _register_blueprints(app: Flask) -> None:
    """Register application blueprints."""
    from app.alpha import alpha_bp
    from app.analytics.routes import analytics_bp
    from app.auth.routes import auth_bp
    from app.calibration import calibration_bp
    from app.dashboard.routes import dashboard_bp
    from app.founder.dashboard import founder_dashboard_bp
    from app.mission.routes import mission_bp
    from app.presentation.session import load_routes as load_session_routes
    from app.presentation.session import session_bp
    from app.presentation.student import load_routes, student_bp
    from app.research import research_bp
    from app.settings.routes import settings_bp
    from app.study_plan.routes import study_plan_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(mission_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(study_plan_bp)
    app.register_blueprint(calibration_bp)
    app.register_blueprint(founder_dashboard_bp)
    app.register_blueprint(research_bp)
    app.register_blueprint(alpha_bp)

    load_routes()
    load_session_routes()
    from app.presentation.curriculum_studio import load_routes as load_studio_routes
    from app.presentation.curriculum_studio import studio_bp

    load_studio_routes()
    # Student Experience production adapters are wired lazily on first
    # ``get_experience_service()`` call (see presentation factory).
    # Session Experience service is wired lazily on first
    # ``get_session_experience_service()`` call.
    app.register_blueprint(student_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(studio_bp)


def _register_routes(app: Flask) -> None:
    """Register simple application-level routes."""

    @app.get("/")
    def index():
        from app.application.config.v2_flags import resolve_v2_feature_flags

        flags = resolve_v2_feature_flags()
        if flags.SOLE_RUNTIME:
            return redirect(url_for("student.home"))
        return redirect(url_for("dashboard.index"))

    # CONSOLE-001 — preserve bookmarks to the former /founder portal.
    @app.route("/founder/", defaults={"path": ""}, methods=["GET", "POST"])
    @app.route("/founder/<path:path>", methods=["GET", "POST"])
    def legacy_founder_to_console(path: str):
        target = f"/console/{path}" if path else "/console/"
        qs = request.query_string.decode("utf-8") if request.query_string else ""
        if qs:
            target = f"{target}?{qs}"
        return redirect(target, code=308)
