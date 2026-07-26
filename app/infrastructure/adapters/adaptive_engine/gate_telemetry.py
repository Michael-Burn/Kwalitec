"""Observational telemetry for Explainability Gate (MS-003 A3).

Events do not mutate educational state and must not influence adaptive
decision computation.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EXPLAINABILITY_GATE_FAILED,
    EXPLAINABILITY_GATE_LATENCY,
    EXPLAINABILITY_GATE_PASSED,
    EXPLAINABILITY_GATE_REQUESTED,
)

EXPLAINABILITY_GATE_EVENT_TYPES: tuple[str, ...] = (
    EXPLAINABILITY_GATE_REQUESTED,
    EXPLAINABILITY_GATE_PASSED,
    EXPLAINABILITY_GATE_FAILED,
    EXPLAINABILITY_GATE_LATENCY,
)

_SOURCE = "explainability_gate"


def emit_explainability_gate_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Explainability Gate event."""
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
    student_id: str = "",
    decision_id: str = "",
) -> IntegrationEvent:
    """Emit EXPLAINABILITY_GATE_REQUESTED."""
    return emit_explainability_gate_event(
        events,
        EXPLAINABILITY_GATE_REQUESTED,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "adapter_id": _SOURCE,
            "mode": "quality_validator",
        },
    )


def emit_passed(
    events: EventRegistry,
    *,
    student_id: str = "",
    decision_id: str = "",
    topic_code: str | None = None,
    decision_kind: str | None = None,
    confidence_band: str | None = None,
) -> IntegrationEvent:
    """Emit EXPLAINABILITY_GATE_PASSED."""
    return emit_explainability_gate_event(
        events,
        EXPLAINABILITY_GATE_PASSED,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "topic_code": topic_code,
            "decision_kind": decision_kind,
            "confidence_band": confidence_band,
            "eligible_for_future_authority": True,
            "observational_only": True,
            "adapter_id": _SOURCE,
            "authority": "adaptive_engine",
        },
    )


def emit_failed(
    events: EventRegistry,
    *,
    student_id: str = "",
    decision_id: str = "",
    error_code: str,
    violation_rule_ids: tuple[str, ...] = (),
    message: str | None = None,
) -> IntegrationEvent:
    """Emit EXPLAINABILITY_GATE_FAILED."""
    return emit_explainability_gate_event(
        events,
        EXPLAINABILITY_GATE_FAILED,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "error_code": error_code,
            "violation_rule_ids": list(violation_rule_ids),
            "message": (message or "")[:256],
            "eligible_for_future_authority": False,
            "observational_only": True,
            "adapter_id": _SOURCE,
        },
    )


def emit_latency(
    events: EventRegistry,
    *,
    student_id: str = "",
    decision_id: str = "",
    latency_ms: float,
    passed: bool,
) -> IntegrationEvent:
    """Emit EXPLAINABILITY_GATE_LATENCY.

    Latency uses wall-clock for observation only — never folded into
    AdaptiveOutputBundle decision material fields.
    """
    return emit_explainability_gate_event(
        events,
        EXPLAINABILITY_GATE_LATENCY,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "latency_ms": round(float(latency_ms), 3),
            "passed": bool(passed),
            "adapter_id": _SOURCE,
            "method": "validate",
        },
    )
