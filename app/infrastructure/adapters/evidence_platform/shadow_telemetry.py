"""Observational telemetry for Evidence Shadow Validation (MS-006 E5).

Events do not mutate educational state. Shadow outputs are measured only.
No policy deployment. No governance auto-promotion.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVIDENCE_SHADOW_COMPLETED,
    EVIDENCE_SHADOW_DRIFT,
    EVIDENCE_SHADOW_FAILED,
    EVIDENCE_SHADOW_HEALTH,
    EVIDENCE_SHADOW_LATENCY,
    EVIDENCE_SHADOW_READINESS,
    EVIDENCE_SHADOW_REQUESTED,
    EVIDENCE_SHADOW_ROLLBACK_VERIFIED,
    EVIDENCE_SHADOW_STABILITY,
)

EVIDENCE_SHADOW_EVENT_TYPES: tuple[str, ...] = (
    EVIDENCE_SHADOW_REQUESTED,
    EVIDENCE_SHADOW_COMPLETED,
    EVIDENCE_SHADOW_FAILED,
    EVIDENCE_SHADOW_STABILITY,
    EVIDENCE_SHADOW_DRIFT,
    EVIDENCE_SHADOW_LATENCY,
    EVIDENCE_SHADOW_HEALTH,
    EVIDENCE_SHADOW_ROLLBACK_VERIFIED,
    EVIDENCE_SHADOW_READINESS,
)

_SOURCE = "evidence_shadow_validator"


def emit_evidence_shadow_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Evidence Shadow Validation event."""
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
    report_id: str | None = None,
    as_of: str | None = None,
    coverage: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Emit EVIDENCE_SHADOW_REQUESTED."""
    return emit_evidence_shadow_event(
        events,
        EVIDENCE_SHADOW_REQUESTED,
        {
            "report_id": report_id,
            "as_of": as_of,
            "coverage": dict(coverage or {}),
            "adapter_id": _SOURCE,
            "mode": "shadow_validation",
            "influences_student": False,
            "deploys_policy": False,
        },
    )


def emit_completed(
    events: EventRegistry,
    *,
    report_id: str,
    ok: bool,
    determinism_ok: bool,
    readiness_status: str,
    coverage: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Emit EVIDENCE_SHADOW_COMPLETED."""
    return emit_evidence_shadow_event(
        events,
        EVIDENCE_SHADOW_COMPLETED,
        {
            "report_id": report_id,
            "ok": bool(ok),
            "determinism_ok": bool(determinism_ok),
            "readiness_status": readiness_status,
            "coverage": dict(coverage or {}),
            "adapter_id": _SOURCE,
            "authority": "evidence_platform",
            "discarded_for_ux": True,
            "influences_student": False,
            "deploys_policy": False,
        },
    )


def emit_failed(
    events: EventRegistry,
    *,
    error_code: str,
    message: str | None = None,
    report_id: str | None = None,
) -> IntegrationEvent:
    """Emit EVIDENCE_SHADOW_FAILED."""
    return emit_evidence_shadow_event(
        events,
        EVIDENCE_SHADOW_FAILED,
        {
            "report_id": report_id,
            "error_code": error_code,
            "message": (message or "")[:256],
            "adapter_id": _SOURCE,
        },
    )


def emit_stability(
    events: EventRegistry,
    *,
    report_id: str,
    evidence_stable: bool,
    observation_stable: bool,
    evaluation_stable: bool,
    analytics_stable: bool,
    projection_stable: bool,
    detail: str = "",
) -> IntegrationEvent:
    """Emit EVIDENCE_SHADOW_STABILITY."""
    return emit_evidence_shadow_event(
        events,
        EVIDENCE_SHADOW_STABILITY,
        {
            "report_id": report_id,
            "evidence_stable": bool(evidence_stable),
            "observation_stable": bool(observation_stable),
            "evaluation_stable": bool(evaluation_stable),
            "analytics_stable": bool(analytics_stable),
            "projection_stable": bool(projection_stable),
            "detail": (detail or "")[:256],
            "adapter_id": _SOURCE,
        },
    )


def emit_drift(
    events: EventRegistry,
    *,
    report_id: str,
    drift_signals: tuple[dict[str, Any], ...] | list[dict[str, Any]],
) -> IntegrationEvent:
    """Emit EVIDENCE_SHADOW_DRIFT."""
    return emit_evidence_shadow_event(
        events,
        EVIDENCE_SHADOW_DRIFT,
        {
            "report_id": report_id,
            "drift_signals": list(drift_signals),
            "drift_count": len(drift_signals),
            "adapter_id": _SOURCE,
        },
    )


def emit_latency(
    events: EventRegistry,
    *,
    report_id: str,
    latency_ms: float,
    ok: bool,
) -> IntegrationEvent:
    """Emit EVIDENCE_SHADOW_LATENCY."""
    return emit_evidence_shadow_event(
        events,
        EVIDENCE_SHADOW_LATENCY,
        {
            "report_id": report_id,
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
    """Emit EVIDENCE_SHADOW_HEALTH."""
    return emit_evidence_shadow_event(
        events,
        EVIDENCE_SHADOW_HEALTH,
        {
            "health": dict(health),
            "adapter_id": _SOURCE,
            "influences_student": False,
            "deploys_policy": False,
        },
    )


def emit_rollback_verified(
    events: EventRegistry,
    *,
    ok: bool,
    details: tuple[str, ...] | list[str] = (),
) -> IntegrationEvent:
    """Emit EVIDENCE_SHADOW_ROLLBACK_VERIFIED."""
    return emit_evidence_shadow_event(
        events,
        EVIDENCE_SHADOW_ROLLBACK_VERIFIED,
        {
            "ok": bool(ok),
            "details": list(details),
            "adapter_id": _SOURCE,
            "flag": "KWALITEC_EVIDENCE_PLATFORM",
        },
    )


def emit_readiness(
    events: EventRegistry,
    *,
    report: dict[str, Any],
) -> IntegrationEvent:
    """Emit EVIDENCE_SHADOW_READINESS."""
    return emit_evidence_shadow_event(
        events,
        EVIDENCE_SHADOW_READINESS,
        {
            "report": dict(report),
            "adapter_id": _SOURCE,
            "influences_student": False,
            "deploys_policy": False,
        },
    )


__all__ = [
    "EVIDENCE_SHADOW_EVENT_TYPES",
    "emit_completed",
    "emit_drift",
    "emit_evidence_shadow_event",
    "emit_failed",
    "emit_health",
    "emit_latency",
    "emit_readiness",
    "emit_requested",
    "emit_rollback_verified",
    "emit_stability",
]
