"""Flask application factory for the Educational Operating System."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from flask import Blueprint, Flask, current_app

from adapters.flask import wire_adapter_layer
from application.composition import ApplicationContainer, create_application
from application.evidence_capture.captured_evidence import CapturedEvidence
from infrastructure.config.settings import (
    AppSettings,
    ConfigurationError,
    load_settings,
    validate_settings,
)
from infrastructure.observability.logging import configure_structured_logging
from infrastructure.observability.metrics import PipelineMetrics
from infrastructure.observability.pipeline_observer import ObservedEducationalPipeline
from web.blueprints import dashboard_bp, learning_bp
from web.lifecycle import get_services
from web.middleware import register_middleware

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check() -> tuple[dict[str, Any], int]:
    """Liveness probe — process is up and composition root is loaded."""
    container = current_app.extensions.get("container")
    settings: AppSettings | None = current_app.extensions.get("settings")
    return (
        {
            "status": "ok",
            "composition_root": container is not None,
            "version": getattr(settings, "version", None)
            or current_app.config.get("APP_VERSION"),
        },
        200,
    )


@health_bp.get("/health/ready")
def readiness_check() -> tuple[dict[str, Any], int]:
    """Readiness probe — configuration validated and pipeline metrics available."""
    container = current_app.extensions.get("container")
    settings: AppSettings | None = current_app.extensions.get("settings")
    metrics: PipelineMetrics | None = current_app.extensions.get("pipeline_metrics")
    config_errors = current_app.extensions.get("config_errors") or ()

    ready = container is not None and not config_errors
    payload: dict[str, Any] = {
        "status": "ready" if ready else "not_ready",
        "composition_root": container is not None,
        "configuration_ok": not config_errors,
        "version": getattr(settings, "version", None),
        "ai_enrichment_enabled": bool(
            settings and settings.ai and settings.ai.enabled
        ),
        "pipeline_metrics": metrics.snapshot() if metrics is not None else {},
    }
    if config_errors:
        payload["configuration_errors"] = list(config_errors)
    return payload, 200 if ready else 503


@dataclass(frozen=True, slots=True)
class WebConfig:
    """Environment-backed configuration for the Education OS web runtime."""

    database_url: str = "sqlite+pysqlite:///:memory:"
    secret_key: str = "dev-change-this-secret-key"
    testing: bool = False
    environment: str = "development"
    version: str = "2.0.0"

    @classmethod
    def from_settings(cls, settings: AppSettings) -> WebConfig:
        return cls(
            database_url=settings.database_url,
            secret_key=settings.secret_key,
            testing=settings.is_testing,
            environment=settings.environment,
            version=settings.version,
        )

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any] | None) -> WebConfig:
        if values is None:
            return cls()
        return cls(
            database_url=str(
                values.get("database_url", values.get("DATABASE_URL", cls.database_url))
            ),
            secret_key=str(
                values.get("secret_key", values.get("SECRET_KEY", cls.secret_key))
            ),
            testing=bool(values.get("testing", values.get("TESTING", cls.testing))),
            environment=str(
                values.get(
                    "environment",
                    values.get("APP_ENV", cls.environment),
                )
            ),
            version=str(values.get("version", values.get("APP_VERSION", cls.version))),
        )

    @classmethod
    def from_env(cls) -> WebConfig:
        return cls.from_settings(load_settings(validate=False))


def _load_config(
    config: WebConfig | AppSettings | Mapping[str, Any] | None,
) -> tuple[WebConfig, AppSettings]:
    if isinstance(config, AppSettings):
        return WebConfig.from_settings(config), config
    if isinstance(config, WebConfig):
        settings = load_settings(validate=False)
        # Prefer explicit WebConfig overrides for tests.
        settings = AppSettings(
            environment="testing" if config.testing else config.environment,
            secret_key=config.secret_key,
            database_url=config.database_url,
            testing=config.testing,
            version=config.version,
            ai=settings.ai,
            log_level=settings.log_level,
            structured_logging=settings.structured_logging,
        )
        return config, settings
    if config is None:
        settings = load_settings(validate=False)
        return WebConfig.from_settings(settings), settings
    web = WebConfig.from_mapping(config)
    settings = AppSettings(
        environment="testing" if web.testing else web.environment,
        secret_key=web.secret_key,
        database_url=web.database_url,
        testing=web.testing,
        version=web.version,
        ai=load_settings(validate=False).ai,
    )
    return web, settings


def _apply_config(app: Flask, config: WebConfig) -> None:
    app.config.update(
        SECRET_KEY=config.secret_key,
        TESTING=config.testing,
        EOS_DATABASE_URL=config.database_url,
        APP_ENV=config.environment,
        APP_VERSION=config.version,
    )


def register_blueprints(app: Flask) -> None:
    """Register HTTP blueprints for the Education OS web surface."""
    app.register_blueprint(health_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(dashboard_bp)


def create_app(
    config: WebConfig | AppSettings | Mapping[str, Any] | None = None,
    *,
    container: ApplicationContainer | None = None,
) -> Flask:
    """Create and configure the Education OS Flask application.

    Validates configuration at startup. Production configuration errors fail fast.
    """
    resolved_config, settings = _load_config(config)

    # Graceful validation for non-production; fail-fast in production.
    try:
        config_errors = validate_settings(settings, fail_fast=settings.is_production)
    except ConfigurationError:
        raise

    if not settings.is_testing:
        configure_structured_logging(
            level=settings.log_level,
            structured=settings.structured_logging,
        )

    app = Flask(__name__)
    _apply_config(app, resolved_config)

    metrics = PipelineMetrics()
    resolved_container = container or create_application(
        resolved_config.database_url,
        settings=settings,
        pipeline_metrics=metrics,
    )
    # Prefer metrics already attached during assemble when container injected.
    pipeline = resolved_container.educational_pipeline
    attached = pipeline.__dict__.get("pipeline_metrics")
    if isinstance(attached, PipelineMetrics):
        metrics = attached

    app.extensions["container"] = resolved_container
    app.extensions["settings"] = settings
    app.extensions["config_errors"] = config_errors
    app.extensions["pipeline_metrics"] = metrics
    app.extensions["observed_pipeline"] = ObservedEducationalPipeline(
        pipeline, metrics=metrics
    )

    register_middleware(app)
    register_blueprints(app)

    def _update_evidence(captured: CapturedEvidence) -> object:
        return resolved_container.product.evidence_update.update(captured)

    app.extensions["eos_evidence_updater"] = _update_evidence
    wire_adapter_layer(
        app,
        resolved_container,
        update_evidence=_update_evidence,
    )

    @app.get("/")
    def root() -> tuple[dict[str, str], int]:
        services = get_services()
        return (
            {
                "status": "ok",
                "service": type(services.learning).__name__,
                "version": settings.version,
            },
            200,
        )

    return app
