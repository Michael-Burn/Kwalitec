"""Observational telemetry for Adaptive Shadow Execution (MS-003 A2).

Events do not mutate educational state. Outputs are logged/measured only.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_SHADOW_COMPLETED,
    ADAPTIVE_SHADOW_FAILED,
    ADAPTIVE_SHADOW_LATENCY,
    ADAPTIVE_SHADOW_REQUESTED,
)

ADAPTIVE_SHADOW_EVENT_TYPES: tuple[str, ...] = (
    ADAPTIVE_SHADOW_REQUESTED,
    ADAPTIVE_SHADOW_COMPLETED,
    ADAPTIVE_SHADOW_FAILED,
    ADAPTIVE_SHADOW_LATENCY,
)

_SOURCE = "adaptive_shadow_orchestrator"


def emit_adaptive_shadow_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Adaptive Shadow event."""
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
    """Emit ADAPTIVE_SHADOW_REQUESTED."""
    return emit_adaptive_shadow_event(
        events,
        ADAPTIVE_SHADOW_REQUESTED,
        {
            "student_id": student_id,
            "as_of": as_of,
            "adapter_id": _SOURCE,
            "mode": "shadow",
        },
    )


def emit_completed(
    events: EventRegistry,
    *,
    student_id: str,
    decision_id: str | None = None,
    topic_code: str | None = None,
    decision_kind: str | None = None,
    confidence_band: str | None = None,
    explainability_complete: bool = True,
) -> IntegrationEvent:
    """Emit ADAPTIVE_SHADOW_COMPLETED."""
    return emit_adaptive_shadow_event(
        events,
        ADAPTIVE_SHADOW_COMPLETED,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "topic_code": topic_code,
            "decision_kind": decision_kind,
            "confidence_band": confidence_band,
            "explainability_complete": bool(explainability_complete),
            "adapter_id": _SOURCE,
            "authority": "adaptive_engine",
            "discarded_for_ux": True,
        },
    )


def emit_failed(
    events: EventRegistry,
    *,
    student_id: str,
    error_code: str,
    message: str | None = None,
) -> IntegrationEvent:
    """Emit ADAPTIVE_SHADOW_FAILED."""
    return emit_adaptive_shadow_event(
        events,
        ADAPTIVE_SHADOW_FAILED,
        {
            "student_id": student_id,
            "error_code": error_code,
            "message": (message or "")[:256],
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
    """Emit ADAPTIVE_SHADOW_LATENCY.

    Latency uses wall-clock for observation only — it is never folded into
    AdaptiveOutputBundle decision material fields.
    """
    return emit_adaptive_shadow_event(
        events,
        ADAPTIVE_SHADOW_LATENCY,
        {
            "student_id": student_id,
            "latency_ms": round(float(latency_ms), 3),
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "method": "execute_shadow",
        },
    )
