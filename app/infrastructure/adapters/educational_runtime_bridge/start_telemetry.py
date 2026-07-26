"""Observational telemetry for the Mission Start Adapter.

Events do not mutate educational state.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    MISSION_START_BRIDGE_FAILURE,
    MISSION_START_BRIDGE_LATENCY,
    MISSION_START_BRIDGE_REQUESTED,
    MISSION_START_BRIDGE_SUCCESS,
)

MISSION_START_BRIDGE_EVENT_TYPES: tuple[str, ...] = (
    MISSION_START_BRIDGE_REQUESTED,
    MISSION_START_BRIDGE_SUCCESS,
    MISSION_START_BRIDGE_FAILURE,
    MISSION_START_BRIDGE_LATENCY,
)

_SOURCE = "mission_start_adapter"


def emit_mission_start_bridge_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Mission Start Bridge event."""
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
    method: str = "start_session",
) -> IntegrationEvent:
    """Emit MISSION_START_BRIDGE_REQUESTED."""
    return emit_mission_start_bridge_event(
        events,
        MISSION_START_BRIDGE_REQUESTED,
        {"student_id": student_id, "method": method, "adapter_id": _SOURCE},
    )


def emit_success(
    events: EventRegistry,
    *,
    student_id: str,
    mission_id: str | None = None,
    error_code: str | None = None,
) -> IntegrationEvent:
    """Emit MISSION_START_BRIDGE_SUCCESS."""
    return emit_mission_start_bridge_event(
        events,
        MISSION_START_BRIDGE_SUCCESS,
        {
            "student_id": student_id,
            "mission_id": mission_id,
            "error_code": error_code,
            "adapter_id": _SOURCE,
            "authority": "study_session_service",
        },
    )


def emit_failure(
    events: EventRegistry,
    *,
    student_id: str,
    error_code: str,
    message: str | None = None,
) -> IntegrationEvent:
    """Emit MISSION_START_BRIDGE_FAILURE."""
    return emit_mission_start_bridge_event(
        events,
        MISSION_START_BRIDGE_FAILURE,
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
    """Emit MISSION_START_BRIDGE_LATENCY."""
    return emit_mission_start_bridge_event(
        events,
        MISSION_START_BRIDGE_LATENCY,
        {
            "student_id": student_id,
            "latency_ms": round(float(latency_ms), 3),
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "method": "start_session",
        },
    )
