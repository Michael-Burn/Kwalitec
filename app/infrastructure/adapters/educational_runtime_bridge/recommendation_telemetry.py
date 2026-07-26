"""Observational telemetry for the Recommendation Read Adapter.

Events do not mutate educational state.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    RECOMMENDATION_BRIDGE_FAILURE,
    RECOMMENDATION_BRIDGE_LATENCY,
    RECOMMENDATION_BRIDGE_REQUESTED,
    RECOMMENDATION_BRIDGE_SUCCESS,
)

RECOMMENDATION_BRIDGE_EVENT_TYPES: tuple[str, ...] = (
    RECOMMENDATION_BRIDGE_REQUESTED,
    RECOMMENDATION_BRIDGE_SUCCESS,
    RECOMMENDATION_BRIDGE_FAILURE,
    RECOMMENDATION_BRIDGE_LATENCY,
)

_SOURCE = "recommendation_adapter"


def emit_recommendation_bridge_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Recommendation Bridge event."""
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
    method: str = "get_todays_recommendation",
) -> IntegrationEvent:
    """Emit RECOMMENDATION_BRIDGE_REQUESTED."""
    return emit_recommendation_bridge_event(
        events,
        RECOMMENDATION_BRIDGE_REQUESTED,
        {"student_id": student_id, "method": method, "adapter_id": _SOURCE},
    )


def emit_success(
    events: EventRegistry,
    *,
    student_id: str,
    decision_id: str | None = None,
    mission_id: str | None = None,
    mission_aligned: bool | None = None,
    error_code: str | None = None,
    fallback_used: bool = False,
) -> IntegrationEvent:
    """Emit RECOMMENDATION_BRIDGE_SUCCESS (includes empty-recommendation outcomes)."""
    return emit_recommendation_bridge_event(
        events,
        RECOMMENDATION_BRIDGE_SUCCESS,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "mission_id": mission_id,
            "mission_aligned": mission_aligned,
            "error_code": error_code,
            "fallback_used": bool(fallback_used),
            "adapter_id": _SOURCE,
            "authority": "recommendation_service",
        },
    )


def emit_failure(
    events: EventRegistry,
    *,
    student_id: str,
    error_code: str,
    message: str | None = None,
) -> IntegrationEvent:
    """Emit RECOMMENDATION_BRIDGE_FAILURE."""
    return emit_recommendation_bridge_event(
        events,
        RECOMMENDATION_BRIDGE_FAILURE,
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
    """Emit RECOMMENDATION_BRIDGE_LATENCY."""
    return emit_recommendation_bridge_event(
        events,
        RECOMMENDATION_BRIDGE_LATENCY,
        {
            "student_id": student_id,
            "latency_ms": round(float(latency_ms), 3),
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "method": "get_todays_recommendation",
        },
    )
