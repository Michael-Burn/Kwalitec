"""Observational telemetry for Adaptive Shadow Soak (MS-003 A6).

Events do not mutate educational state. Soak outputs are measured only.
"""

from __future__ import annotations

import logging
from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_ENGINE_SHADOW_COMPARE,
    ADAPTIVE_SOAK_COMPARE,
    ADAPTIVE_SOAK_COMPLETED,
    ADAPTIVE_SOAK_DRIFT,
    ADAPTIVE_SOAK_FAILED,
    ADAPTIVE_SOAK_HEALTH,
    ADAPTIVE_SOAK_LATENCY,
    ADAPTIVE_SOAK_REQUESTED,
    ADAPTIVE_SOAK_ROLLBACK_VERIFIED,
)

logger = logging.getLogger(__name__)

ADAPTIVE_SOAK_EVENT_TYPES: tuple[str, ...] = (
    ADAPTIVE_SOAK_REQUESTED,
    ADAPTIVE_SOAK_COMPLETED,
    ADAPTIVE_SOAK_FAILED,
    ADAPTIVE_SOAK_COMPARE,
    ADAPTIVE_ENGINE_SHADOW_COMPARE,
    ADAPTIVE_SOAK_DRIFT,
    ADAPTIVE_SOAK_LATENCY,
    ADAPTIVE_SOAK_HEALTH,
    ADAPTIVE_SOAK_ROLLBACK_VERIFIED,
)

_SOURCE = "adaptive_shadow_soak"


def emit_adaptive_soak_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Adaptive Shadow Soak event."""
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
    return emit_adaptive_soak_event(
        events,
        ADAPTIVE_SOAK_REQUESTED,
        {
            "student_id": student_id,
            "as_of": as_of,
            "adapter_id": _SOURCE,
            "mode": "shadow_soak",
            "influences_student": False,
        },
    )


def emit_completed(
    events: EventRegistry,
    *,
    student_id: str,
    decision_id: str | None = None,
    agreed: bool | None = None,
    explainability_passed: bool = False,
    trace_created: bool = False,
    determinism_success: bool | None = None,
    drift_count: int = 0,
) -> IntegrationEvent:
    return emit_adaptive_soak_event(
        events,
        ADAPTIVE_SOAK_COMPLETED,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "agreed": agreed,
            "explainability_passed": bool(explainability_passed),
            "trace_created": bool(trace_created),
            "determinism_success": determinism_success,
            "drift_count": int(drift_count),
            "adapter_id": _SOURCE,
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
    return emit_adaptive_soak_event(
        events,
        ADAPTIVE_SOAK_FAILED,
        {
            "student_id": student_id,
            "error_code": error_code,
            "message": (message or "")[:256],
            "adapter_id": _SOURCE,
        },
    )


def emit_compare(
    events: EventRegistry,
    *,
    student_id: str,
    comparison: dict[str, Any],
    explainability_passed: bool | None = None,
) -> tuple[IntegrationEvent, IntegrationEvent]:
    """Emit soak compare + architecture ADAPTIVE_ENGINE_SHADOW_COMPARE.

    Also emits one greppable INFO log for Render/ops log viewers. Logging is
    observational only — same fail-open path as the event publish.
    """
    cmp = dict(comparison)
    payload = {
        "student_id": student_id,
        "adapter_id": _SOURCE,
        "phase": "a6_shadow_soak",
        **cmp,
    }
    # Prefer explicit kwarg; fall back if already present on the comparison dict.
    expl = explainability_passed
    if expl is None and "explainability_passed" in cmp:
        expl = cmp.get("explainability_passed")
    logger.info(
        "ADAPTIVE_SHADOW_COMPARE student_id=%s agreed=%s "
        "baseline_topic_code=%s adaptive_topic_code=%s divergence_reason=%s "
        "explainability_passed=%s",
        student_id,
        cmp.get("agreed"),
        cmp.get("baseline_topic_code") or "",
        cmp.get("adaptive_topic_code") or "",
        cmp.get("divergence_reason") or "",
        expl,
    )
    soak = emit_adaptive_soak_event(events, ADAPTIVE_SOAK_COMPARE, payload)
    legacy = emit_adaptive_soak_event(
        events, ADAPTIVE_ENGINE_SHADOW_COMPARE, payload
    )
    return soak, legacy


def emit_drift(
    events: EventRegistry,
    *,
    student_id: str,
    signals: list[dict[str, Any]],
) -> IntegrationEvent:
    return emit_adaptive_soak_event(
        events,
        ADAPTIVE_SOAK_DRIFT,
        {
            "student_id": student_id,
            "signal_count": len(signals),
            "signals": list(signals),
            "adapter_id": _SOURCE,
            "auto_correction": False,
        },
    )


def emit_latency(
    events: EventRegistry,
    *,
    student_id: str,
    latency_ms: float,
    ok: bool,
) -> IntegrationEvent:
    return emit_adaptive_soak_event(
        events,
        ADAPTIVE_SOAK_LATENCY,
        {
            "student_id": student_id,
            "latency_ms": round(float(latency_ms), 3),
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "method": "execute_soak",
        },
    )


def emit_health(
    events: EventRegistry,
    *,
    snapshot: dict[str, Any],
) -> IntegrationEvent:
    return emit_adaptive_soak_event(
        events,
        ADAPTIVE_SOAK_HEALTH,
        {
            "adapter_id": _SOURCE,
            "phase": "a6_shadow_soak",
            "health": dict(snapshot),
        },
    )


def emit_rollback_verified(
    events: EventRegistry,
    *,
    ok: bool,
    details: list[str] | tuple[str, ...] | None = None,
) -> IntegrationEvent:
    return emit_adaptive_soak_event(
        events,
        ADAPTIVE_SOAK_ROLLBACK_VERIFIED,
        {
            "ok": bool(ok),
            "details": list(details or ()),
            "adapter_id": _SOURCE,
            "phase": "a6_rollback_verification",
        },
    )


__all__ = [
    "ADAPTIVE_SOAK_EVENT_TYPES",
    "emit_adaptive_soak_event",
    "emit_compare",
    "emit_completed",
    "emit_drift",
    "emit_failed",
    "emit_health",
    "emit_latency",
    "emit_requested",
    "emit_rollback_verified",
]
