"""Observational telemetry for the History Read Adapter.

Events do not mutate educational state.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    HISTORY_BRIDGE_FAILURE,
    HISTORY_BRIDGE_LATENCY,
    HISTORY_BRIDGE_REQUESTED,
    HISTORY_BRIDGE_SUCCESS,
)

HISTORY_BRIDGE_EVENT_TYPES: tuple[str, ...] = (
    HISTORY_BRIDGE_REQUESTED,
    HISTORY_BRIDGE_SUCCESS,
    HISTORY_BRIDGE_FAILURE,
    HISTORY_BRIDGE_LATENCY,
)

_SOURCE = "history_adapter"


def emit_history_bridge_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational History Bridge event."""
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
    method: str = "project_history",
) -> IntegrationEvent:
    """Emit HISTORY_BRIDGE_REQUESTED."""
    return emit_history_bridge_event(
        events,
        HISTORY_BRIDGE_REQUESTED,
        {"student_id": student_id, "method": method, "adapter_id": _SOURCE},
    )


def emit_success(
    events: EventRegistry,
    *,
    student_id: str,
    session_count: int | None = None,
    error_code: str | None = None,
    fallback_used: bool = False,
) -> IntegrationEvent:
    """Emit HISTORY_BRIDGE_SUCCESS (includes empty-history outcomes)."""
    return emit_history_bridge_event(
        events,
        HISTORY_BRIDGE_SUCCESS,
        {
            "student_id": student_id,
            "session_count": session_count,
            "error_code": error_code,
            "fallback_used": bool(fallback_used),
            "adapter_id": _SOURCE,
            "authority": "history_bridge",
        },
    )


def emit_failure(
    events: EventRegistry,
    *,
    student_id: str,
    error_code: str,
    message: str | None = None,
) -> IntegrationEvent:
    """Emit HISTORY_BRIDGE_FAILURE."""
    return emit_history_bridge_event(
        events,
        HISTORY_BRIDGE_FAILURE,
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
    method: str = "project_history",
) -> IntegrationEvent:
    """Emit HISTORY_BRIDGE_LATENCY."""
    return emit_history_bridge_event(
        events,
        HISTORY_BRIDGE_LATENCY,
        {
            "student_id": student_id,
            "latency_ms": round(float(latency_ms), 3),
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "method": method,
        },
    )
