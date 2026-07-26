"""Observational telemetry for the Session Completion Adapter.

Events do not mutate educational state.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    SESSION_COMPLETION_BRIDGE_FAILURE,
    SESSION_COMPLETION_BRIDGE_LATENCY,
    SESSION_COMPLETION_BRIDGE_REQUESTED,
    SESSION_COMPLETION_BRIDGE_SUCCESS,
)

SESSION_COMPLETION_BRIDGE_EVENT_TYPES: tuple[str, ...] = (
    SESSION_COMPLETION_BRIDGE_REQUESTED,
    SESSION_COMPLETION_BRIDGE_SUCCESS,
    SESSION_COMPLETION_BRIDGE_FAILURE,
    SESSION_COMPLETION_BRIDGE_LATENCY,
)

_SOURCE = "session_completion_adapter"


def emit_session_completion_bridge_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Session Completion Bridge event."""
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
    method: str = "complete_session",
) -> IntegrationEvent:
    """Emit SESSION_COMPLETION_BRIDGE_REQUESTED."""
    return emit_session_completion_bridge_event(
        events,
        SESSION_COMPLETION_BRIDGE_REQUESTED,
        {"student_id": student_id, "method": method, "adapter_id": _SOURCE},
    )


def emit_success(
    events: EventRegistry,
    *,
    student_id: str,
    mission_id: str | None = None,
    session_id: str | None = None,
    error_code: str | None = None,
    evidence_accepted: bool | None = None,
) -> IntegrationEvent:
    """Emit SESSION_COMPLETION_BRIDGE_SUCCESS."""
    return emit_session_completion_bridge_event(
        events,
        SESSION_COMPLETION_BRIDGE_SUCCESS,
        {
            "student_id": student_id,
            "mission_id": mission_id,
            "session_id": session_id,
            "error_code": error_code,
            "evidence_accepted": evidence_accepted,
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
    """Emit SESSION_COMPLETION_BRIDGE_FAILURE."""
    return emit_session_completion_bridge_event(
        events,
        SESSION_COMPLETION_BRIDGE_FAILURE,
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
    """Emit SESSION_COMPLETION_BRIDGE_LATENCY."""
    return emit_session_completion_bridge_event(
        events,
        SESSION_COMPLETION_BRIDGE_LATENCY,
        {
            "student_id": student_id,
            "latency_ms": round(float(latency_ms), 3),
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "method": "complete_session",
        },
    )
