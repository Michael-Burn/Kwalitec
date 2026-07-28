"""Factory helpers for Runtime Integration Preferred Authority (RI-001)."""

from __future__ import annotations

from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.runtime_integration.service import RuntimeIntegrationService
from app.application.runtime_integration.telemetry import DEFAULT_TELEMETRY


def is_runtime_integration_enabled(*, environ: dict[str, str] | None = None) -> bool:
    """Return whether preferred-authority routing is enabled (default ON)."""
    flags = resolve_v2_feature_flags(environ=environ)
    return bool(flags.ENABLE_RUNTIME_INTEGRATION)


def build_runtime_integration_service(
    *,
    runtime_a_fallback: Any | None = None,
    integration_enabled: bool | None = None,
    telemetry: Any | None = None,
    environ: dict[str, str] | None = None,
) -> RuntimeIntegrationService:
    """Construct a RuntimeIntegrationService for production or tests."""
    enabled = (
        is_runtime_integration_enabled(environ=environ)
        if integration_enabled is None
        else bool(integration_enabled)
    )
    return RuntimeIntegrationService(
        runtime_a_fallback=runtime_a_fallback,
        integration_enabled=enabled,
        telemetry=telemetry or DEFAULT_TELEMETRY,
    )
