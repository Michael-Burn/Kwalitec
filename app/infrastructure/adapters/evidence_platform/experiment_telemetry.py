"""Observational telemetry for Experiment Framework (MS-006 E2).

Events do not mutate educational state. Assignment outputs are measured only.
No scoring, winner declaration, policy evaluation, or analytics aggregation.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EXPERIMENT_ASSIGNMENT_COMPLETED,
    EXPERIMENT_ASSIGNMENT_FAILED,
    EXPERIMENT_ASSIGNMENT_LATENCY,
    EXPERIMENT_ASSIGNMENT_REQUESTED,
)

EXPERIMENT_ASSIGNMENT_EVENT_TYPES: tuple[str, ...] = (
    EXPERIMENT_ASSIGNMENT_REQUESTED,
    EXPERIMENT_ASSIGNMENT_COMPLETED,
    EXPERIMENT_ASSIGNMENT_FAILED,
    EXPERIMENT_ASSIGNMENT_LATENCY,
)

_SOURCE = "experiment_framework"


def emit_experiment_assignment_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Experiment Assignment event."""
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
    experiment_id: str = "",
    evidence_id: str = "",
) -> IntegrationEvent:
    """Emit EXPERIMENT_ASSIGNMENT_REQUESTED."""
    return emit_experiment_assignment_event(
        events,
        EXPERIMENT_ASSIGNMENT_REQUESTED,
        {
            "student_id": student_id,
            "experiment_id": experiment_id,
            "evidence_id": evidence_id,
            "adapter_id": _SOURCE,
            "mode": "assignment",
            "influences_student": False,
        },
    )


def emit_completed(
    events: EventRegistry,
    *,
    student_id: str,
    experiment_id: str = "",
    experiment_version: str = "",
    arm_id: str = "",
    cohort: str = "",
    evidence_id: str = "",
    observation_id: str = "",
    assignment_mechanism: str = "",
) -> IntegrationEvent:
    """Emit EXPERIMENT_ASSIGNMENT_COMPLETED."""
    return emit_experiment_assignment_event(
        events,
        EXPERIMENT_ASSIGNMENT_COMPLETED,
        {
            "student_id": student_id,
            "experiment_id": experiment_id,
            "experiment_version": experiment_version,
            "arm_id": arm_id,
            "cohort": cohort,
            "evidence_id": evidence_id,
            "observation_id": observation_id,
            "assignment_mechanism": assignment_mechanism,
            "adapter_id": _SOURCE,
            "authority": "evidence_platform",
            "influences_student": False,
        },
    )


def emit_failed(
    events: EventRegistry,
    *,
    student_id: str,
    experiment_id: str = "",
    evidence_id: str = "",
    error_code: str = "INVALID_STATE",
    message: str = "",
) -> IntegrationEvent:
    """Emit EXPERIMENT_ASSIGNMENT_FAILED."""
    return emit_experiment_assignment_event(
        events,
        EXPERIMENT_ASSIGNMENT_FAILED,
        {
            "student_id": student_id,
            "experiment_id": experiment_id,
            "evidence_id": evidence_id,
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
    experiment_id: str = "",
    duration_ms: float | int | None = None,
    ok: bool = True,
) -> IntegrationEvent:
    """Emit EXPERIMENT_ASSIGNMENT_LATENCY."""
    return emit_experiment_assignment_event(
        events,
        EXPERIMENT_ASSIGNMENT_LATENCY,
        {
            "student_id": student_id,
            "experiment_id": experiment_id,
            "duration_ms": duration_ms,
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "influences_student": False,
        },
    )
