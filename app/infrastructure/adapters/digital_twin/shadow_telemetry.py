"""Observational telemetry for Twin Shadow Validation (MS-004 T6).

Events do not mutate educational state. Shadow outputs are measured only.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    TWIN_SHADOW_COMPLETED,
    TWIN_SHADOW_DRIFT,
    TWIN_SHADOW_FAILED,
    TWIN_SHADOW_HEALTH,
    TWIN_SHADOW_LATENCY,
    TWIN_SHADOW_REQUESTED,
    TWIN_SHADOW_ROLLBACK_VERIFIED,
    TWIN_SHADOW_STABILITY,
)

TWIN_SHADOW_EVENT_TYPES: tuple[str, ...] = (
    TWIN_SHADOW_REQUESTED,
    TWIN_SHADOW_COMPLETED,
    TWIN_SHADOW_FAILED,
    TWIN_SHADOW_STABILITY,
    TWIN_SHADOW_DRIFT,
    TWIN_SHADOW_LATENCY,
    TWIN_SHADOW_HEALTH,
    TWIN_SHADOW_ROLLBACK_VERIFIED,
)

_SOURCE = "twin_shadow_validator"


def emit_twin_shadow_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Twin Shadow Validation event."""
    ids = CorrelationContext.current()
    event = IntegrationEvent.create(
        event_type,
        dict(payload or {}),
        correlation_id=ids.correlation_id or "",
        source=_SOURCE,
    )
    events.publish(event)
    return event


def emit_requested(
    events: EventRegistry,
    *,
    student_id: str,
    as_of: str | None = None,
) -> IntegrationEvent:
    """Emit TWIN_SHADOW_REQUESTED."""
    return emit_twin_shadow_event(
        events,
        TWIN_SHADOW_REQUESTED,
        {
            "student_id": student_id,
            "as_of": as_of,
            "adapter_id": _SOURCE,
            "mode": "shadow_validation",
            "influences_student": False,
        },
    )


def emit_completed(
    events: EventRegistry,
    *,
    student_id: str,
    twin_id: str | None = None,
    snapshot_ok: bool = False,
    projection_ok: bool = False,
    explainability_ok: bool = False,
    unavailable_facet_count: int = 0,
    determinism_ok: bool | None = None,
) -> IntegrationEvent:
    """Emit TWIN_SHADOW_COMPLETED."""
    return emit_twin_shadow_event(
        events,
        TWIN_SHADOW_COMPLETED,
        {
            "student_id": student_id,
            "twin_id": twin_id,
            "snapshot_ok": bool(snapshot_ok),
            "projection_ok": bool(projection_ok),
            "explainability_ok": bool(explainability_ok),
            "unavailable_facet_count": int(unavailable_facet_count),
            "determinism_ok": determinism_ok,
            "adapter_id": _SOURCE,
            "authority": "digital_twin",
            "discarded_for_ux": True,
            "influences_student": False,
        },
    )


def emit_failed(
    events: EventRegistry,
    *,
    student_id: str,
    error_code: str,
    message: str | None = None,
) -> IntegrationEvent:
    """Emit TWIN_SHADOW_FAILED."""
    return emit_twin_shadow_event(
        events,
        TWIN_SHADOW_FAILED,
        {
            "student_id": student_id,
            "error_code": error_code,
            "message": (message or "")[:256],
            "adapter_id": _SOURCE,
        },
    )


def emit_stability(
    events: EventRegistry,
    *,
    student_id: str,
    snapshot_stable: bool,
    projection_stable: bool,
    explainability_stable: bool,
    detail: str = "",
) -> IntegrationEvent:
    """Emit TWIN_SHADOW_STABILITY."""
    return emit_twin_shadow_event(
        events,
        TWIN_SHADOW_STABILITY,
        {
            "student_id": student_id,
            "snapshot_stable": bool(snapshot_stable),
            "projection_stable": bool(projection_stable),
            "explainability_stable": bool(explainability_stable),
            "detail": (detail or "")[:256],
            "adapter_id": _SOURCE,
        },
    )


def emit_drift(
    events: EventRegistry,
    *,
    student_id: str,
    drift_signals: tuple[dict[str, Any], ...] | list[dict[str, Any]],
) -> IntegrationEvent:
    """Emit TWIN_SHADOW_DRIFT."""
    return emit_twin_shadow_event(
        events,
        TWIN_SHADOW_DRIFT,
        {
            "student_id": student_id,
            "drift_signals": list(drift_signals),
            "drift_count": len(drift_signals),
            "adapter_id": _SOURCE,
        },
    )


def emit_latency(
    events: EventRegistry,
    *,
    student_id: str,
    latency_ms: float,
    ok: bool,
) -> IntegrationEvent:
    """Emit TWIN_SHADOW_LATENCY."""
    return emit_twin_shadow_event(
        events,
        TWIN_SHADOW_LATENCY,
        {
            "student_id": student_id,
            "latency_ms": round(float(latency_ms), 3),
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "method": "validate_shadow",
        },
    )


def emit_health(
    events: EventRegistry,
    *,
    health: dict[str, Any],
) -> IntegrationEvent:
    """Emit TWIN_SHADOW_HEALTH."""
    return emit_twin_shadow_event(
        events,
        TWIN_SHADOW_HEALTH,
        {
            "health": dict(health),
            "adapter_id": _SOURCE,
            "influences_student": False,
        },
    )


def emit_rollback_verified(
    events: EventRegistry,
    *,
    ok: bool,
    details: tuple[str, ...] | list[str] = (),
) -> IntegrationEvent:
    """Emit TWIN_SHADOW_ROLLBACK_VERIFIED."""
    return emit_twin_shadow_event(
        events,
        TWIN_SHADOW_ROLLBACK_VERIFIED,
        {
            "ok": bool(ok),
            "details": list(details),
            "adapter_id": _SOURCE,
            "flag": "KWALITEC_DIGITAL_TWIN",
        },
    )


__all__ = [
    "TWIN_SHADOW_EVENT_TYPES",
    "emit_completed",
    "emit_drift",
    "emit_failed",
    "emit_health",
    "emit_latency",
    "emit_requested",
    "emit_rollback_verified",
    "emit_stability",
    "emit_twin_shadow_event",
]
