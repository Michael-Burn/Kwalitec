"""Observational telemetry for Evidence Collection (MS-006 E1).

Events do not mutate educational state. Collection outputs are measured only.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVIDENCE_COLLECTION_COMPLETED,
    EVIDENCE_COLLECTION_FAILED,
    EVIDENCE_COLLECTION_LATENCY,
    EVIDENCE_COLLECTION_REQUESTED,
)

EVIDENCE_COLLECTION_EVENT_TYPES: tuple[str, ...] = (
    EVIDENCE_COLLECTION_REQUESTED,
    EVIDENCE_COLLECTION_COMPLETED,
    EVIDENCE_COLLECTION_FAILED,
    EVIDENCE_COLLECTION_LATENCY,
)

_SOURCE = "evidence_collector"


def emit_evidence_collection_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Evidence Collection event."""
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
    event_type: str = "",
    as_of: str | None = None,
) -> IntegrationEvent:
    """Emit EVIDENCE_COLLECTION_REQUESTED."""
    return emit_evidence_collection_event(
        events,
        EVIDENCE_COLLECTION_REQUESTED,
        {
            "student_id": student_id,
            "event_type": event_type,
            "as_of": as_of,
            "adapter_id": _SOURCE,
            "mode": "collection",
            "influences_student": False,
        },
    )


def emit_completed(
    events: EventRegistry,
    *,
    student_id: str,
    evidence_id: str | None = None,
    evidence_class: str = "",
    event_type: str = "",
    quality_result: str = "",
    runtime_a_ref_present: bool = False,
) -> IntegrationEvent:
    """Emit EVIDENCE_COLLECTION_COMPLETED."""
    return emit_evidence_collection_event(
        events,
        EVIDENCE_COLLECTION_COMPLETED,
        {
            "student_id": student_id,
            "evidence_id": evidence_id,
            "evidence_class": evidence_class,
            "event_type": event_type,
            "quality_result": quality_result,
            "runtime_a_ref_present": bool(runtime_a_ref_present),
            "adapter_id": _SOURCE,
            "authority": "evidence_platform",
            "influences_student": False,
        },
    )


def emit_failed(
    events: EventRegistry,
    *,
    student_id: str,
    error_code: str = "INVALID_STATE",
    message: str = "",
) -> IntegrationEvent:
    """Emit EVIDENCE_COLLECTION_FAILED."""
    return emit_evidence_collection_event(
        events,
        EVIDENCE_COLLECTION_FAILED,
        {
            "student_id": student_id,
            "error_code": error_code,
            "message": message,
            "adapter_id": _SOURCE,
            "influences_student": False,
        },
    )


def emit_latency(
    events: EventRegistry,
    *,
    student_id: str,
    duration_ms: float | int | None = None,
    ok: bool = True,
) -> IntegrationEvent:
    """Emit EVIDENCE_COLLECTION_LATENCY."""
    return emit_evidence_collection_event(
        events,
        EVIDENCE_COLLECTION_LATENCY,
        {
            "student_id": student_id,
            "duration_ms": duration_ms,
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "influences_student": False,
        },
    )
