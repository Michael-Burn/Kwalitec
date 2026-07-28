"""Runtime Integration — Preferred Authority orchestration (RI-001).

Educational Intelligence (EI-007 → EX-001) is preferred whenever an active SCI
has Educational Decisions. Runtime A is temporary compatibility only.
"""

from __future__ import annotations

from app.application.runtime_integration.adapters import (
    map_coach_context,
    map_daily_mission,
    map_dashboard_card,
    map_dashboard_recommendation,
    map_revision_entry,
    map_session_briefing,
)
from app.application.runtime_integration.dto import (
    AuthoritySource,
    FallbackReason,
    IntegrationResult,
    IntegrationSurface,
    SurfaceExperienceBundle,
    TelemetrySnapshot,
)
from app.application.runtime_integration.exceptions import (
    IntegrationUnavailableError,
    RuntimeIntegrationError,
)
from app.application.runtime_integration.factory import (
    build_runtime_integration_service,
    is_runtime_integration_enabled,
)
from app.application.runtime_integration.service import RuntimeIntegrationService
from app.application.runtime_integration.telemetry import (
    DEFAULT_TELEMETRY,
    RuntimeIntegrationTelemetry,
)

__all__ = [
    "AUTHORITY_SOURCE_EI",
    "AuthoritySource",
    "DEFAULT_TELEMETRY",
    "FallbackReason",
    "IntegrationResult",
    "IntegrationSurface",
    "IntegrationUnavailableError",
    "RuntimeIntegrationError",
    "RuntimeIntegrationService",
    "RuntimeIntegrationTelemetry",
    "SurfaceExperienceBundle",
    "TelemetrySnapshot",
    "build_runtime_integration_service",
    "is_runtime_integration_enabled",
    "map_coach_context",
    "map_daily_mission",
    "map_dashboard_card",
    "map_dashboard_recommendation",
    "map_revision_entry",
    "map_session_briefing",
]

AUTHORITY_SOURCE_EI = AuthoritySource.EDUCATIONAL_INTELLIGENCE
