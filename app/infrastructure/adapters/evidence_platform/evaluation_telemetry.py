"""Observational telemetry for Policy Evaluation (MS-006 E3).

Events do not mutate educational state. Evaluation outputs are governance
recommendations only. No policy promotion, analytics aggregation, or
educational behaviour change.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVIDENCE_EVAL_COMPLETED,
    EVIDENCE_EVAL_FAILED,
    EVIDENCE_EVAL_LATENCY,
    EVIDENCE_EVAL_REQUESTED,
)

EVIDENCE_EVAL_EVENT_TYPES: tuple[str, ...] = (
    EVIDENCE_EVAL_REQUESTED,
    EVIDENCE_EVAL_COMPLETED,
    EVIDENCE_EVAL_FAILED,
    EVIDENCE_EVAL_LATENCY,
)

_SOURCE = "policy_evaluation"


def emit_evidence_eval_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Policy Evaluation event."""
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
    policy_id: str,
    policy_version: str = "",
    observation_count: int = 0,
) -> IntegrationEvent:
    """Emit EVIDENCE_EVAL_REQUESTED."""
    return emit_evidence_eval_event(
        events,
        EVIDENCE_EVAL_REQUESTED,
        {
            "policy_id": policy_id,
            "policy_version": policy_version,
            "observation_count": observation_count,
            "adapter_id": _SOURCE,
            "mode": "evaluation",
            "influences_student": False,
        },
    )


def emit_completed(
    events: EventRegistry,
    *,
    policy_id: str,
    policy_version: str = "",
    evaluation_id: str = "",
    gate_result: str = "",
    recommendation: str = "",
    confidence_band: str = "",
    experiment_refs: tuple[str, ...] | list[str] | None = None,
    evidence_refs: tuple[str, ...] | list[str] | None = None,
) -> IntegrationEvent:
    """Emit EVIDENCE_EVAL_COMPLETED."""
    return emit_evidence_eval_event(
        events,
        EVIDENCE_EVAL_COMPLETED,
        {
            "policy_id": policy_id,
            "policy_version": policy_version,
            "evaluation_id": evaluation_id,
            "gate_result": gate_result,
            "recommendation": recommendation,
            "confidence_band": confidence_band,
            "experiment_refs": list(experiment_refs or ()),
            "evidence_refs": list(evidence_refs or ()),
            "adapter_id": _SOURCE,
            "authority": "evidence_platform",
            "influences_student": False,
            "promotes_policy": False,
        },
    )


def emit_failed(
    events: EventRegistry,
    *,
    policy_id: str,
    policy_version: str = "",
    error_code: str = "INVALID_STATE",
    message: str = "",
) -> IntegrationEvent:
    """Emit EVIDENCE_EVAL_FAILED."""
    return emit_evidence_eval_event(
        events,
        EVIDENCE_EVAL_FAILED,
        {
            "policy_id": policy_id,
            "policy_version": policy_version,
            "error_code": error_code,
            "message": message,
            "adapter_id": _SOURCE,
            "influences_student": False,
            "promotes_policy": False,
        },
    )


def emit_latency(
    events: EventRegistry,
    *,
    policy_id: str,
    duration_ms: float | int | None = None,
    ok: bool = True,
) -> IntegrationEvent:
    """Emit EVIDENCE_EVAL_LATENCY."""
    return emit_evidence_eval_event(
        events,
        EVIDENCE_EVAL_LATENCY,
        {
            "policy_id": policy_id,
            "duration_ms": duration_ms,
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "influences_student": False,
        },
    )
