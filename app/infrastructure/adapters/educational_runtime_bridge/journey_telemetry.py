"""Observational telemetry for the Journey Read Adapter.

Events do not mutate educational state.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    JOURNEY_BRIDGE_FAILURE,
    JOURNEY_BRIDGE_LATENCY,
    JOURNEY_BRIDGE_REQUESTED,
    JOURNEY_BRIDGE_SUCCESS,
)

JOURNEY_BRIDGE_EVENT_TYPES: tuple[str, ...] = (
    JOURNEY_BRIDGE_REQUESTED,
    JOURNEY_BRIDGE_SUCCESS,
    JOURNEY_BRIDGE_FAILURE,
    JOURNEY_BRIDGE_LATENCY,
)

_SOURCE = "journey_adapter"


def emit_journey_bridge_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Journey Bridge event."""
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
    method: str = "project_journey",
) -> IntegrationEvent:
    """Emit JOURNEY_BRIDGE_REQUESTED."""
    return emit_journey_bridge_event(
        events,
        JOURNEY_BRIDGE_REQUESTED,
        {"student_id": student_id, "method": method, "adapter_id": _SOURCE},
    )


def emit_success(
    events: EventRegistry,
    *,
    student_id: str,
    has_journey: bool | None = None,
    error_code: str | None = None,
    fallback_used: bool = False,
) -> IntegrationEvent:
    """Emit JOURNEY_BRIDGE_SUCCESS (includes empty-journey outcomes)."""
    return emit_journey_bridge_event(
        events,
        JOURNEY_BRIDGE_SUCCESS,
        {
            "student_id": student_id,
            "has_journey": has_journey,
            "error_code": error_code,
            "fallback_used": bool(fallback_used),
            "adapter_id": _SOURCE,
            "authority": "journey_bridge",
        },
    )


def emit_failure(
    events: EventRegistry,
    *,
    student_id: str,
    error_code: str,
    message: str | None = None,
) -> IntegrationEvent:
    """Emit JOURNEY_BRIDGE_FAILURE."""
    return emit_journey_bridge_event(
        events,
        JOURNEY_BRIDGE_FAILURE,
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
    """Emit JOURNEY_BRIDGE_LATENCY."""
    return emit_journey_bridge_event(
        events,
        JOURNEY_BRIDGE_LATENCY,
        {
            "student_id": student_id,
            "latency_ms": round(float(latency_ms), 3),
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "method": "project_journey",
        },
    )
