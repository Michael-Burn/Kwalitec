"""Observational telemetry for Adaptive Decision Traceability (MS-003 A5).

Events do not mutate educational state. Traces are audit artefacts only.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_TRACE_CREATED,
    ADAPTIVE_TRACE_FAILED,
    ADAPTIVE_TRACE_RECONSTRUCTED,
)

ADAPTIVE_TRACE_EVENT_TYPES: tuple[str, ...] = (
    ADAPTIVE_TRACE_CREATED,
    ADAPTIVE_TRACE_FAILED,
    ADAPTIVE_TRACE_RECONSTRUCTED,
)

_SOURCE = "adaptive_traceability_service"


def emit_adaptive_trace_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
    *,
    correlation_id: str | None = None,
) -> IntegrationEvent:
    """Publish one observational Adaptive Trace event."""
    ids = CorrelationContext.current()
    corr = (correlation_id or "").strip() or ids.correlation_id or ""
    event = IntegrationEvent.create(
        event_type,
        dict(payload or {}),
        correlation_id=corr,
        source=_SOURCE,
    )
    events.publish(event)
    return event


def emit_created(
    events: EventRegistry,
    *,
    student_id: str,
    decision_id: str,
    correlation_id: str,
    authority_status: str,
    runtime_a_snapshot_id: str = "",
) -> IntegrationEvent:
    """Emit ADAPTIVE_TRACE_CREATED."""
    return emit_adaptive_trace_event(
        events,
        ADAPTIVE_TRACE_CREATED,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "correlation_id": correlation_id,
            "authority_status": authority_status,
            "runtime_a_snapshot_id": runtime_a_snapshot_id,
            "adapter_id": _SOURCE,
            "phase": "a5_observational_traceability",
            "observational_only": True,
        },
        correlation_id=correlation_id,
    )


def emit_failed(
    events: EventRegistry,
    *,
    student_id: str,
    correlation_id: str,
    error_code: str,
    message: str = "",
    decision_id: str = "",
) -> IntegrationEvent:
    """Emit ADAPTIVE_TRACE_FAILED."""
    return emit_adaptive_trace_event(
        events,
        ADAPTIVE_TRACE_FAILED,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "correlation_id": correlation_id,
            "error_code": error_code,
            "message": (message or "")[:256],
            "adapter_id": _SOURCE,
            "observational_only": True,
        },
        correlation_id=correlation_id,
    )


def emit_reconstructed(
    events: EventRegistry,
    *,
    student_id: str,
    decision_id: str,
    correlation_id: str,
    lineage_stages: tuple[str, ...] | list[str] = (),
) -> IntegrationEvent:
    """Emit ADAPTIVE_TRACE_RECONSTRUCTED."""
    return emit_adaptive_trace_event(
        events,
        ADAPTIVE_TRACE_RECONSTRUCTED,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "correlation_id": correlation_id,
            "lineage_stages": list(lineage_stages),
            "adapter_id": _SOURCE,
            "observational_only": True,
        },
        correlation_id=correlation_id,
    )


__all__ = [
    "ADAPTIVE_TRACE_EVENT_TYPES",
    "emit_adaptive_trace_event",
    "emit_created",
    "emit_failed",
    "emit_reconstructed",
]
