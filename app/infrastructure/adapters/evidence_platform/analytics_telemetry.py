"""Observational telemetry for Analytics & Projection (MS-006 E4).

Events do not mutate educational state. Analytics outputs are
governance-facing only. No policy promotion or educational behaviour change.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EVIDENCE_ANALYTICS_COMPLETED,
    EVIDENCE_ANALYTICS_FAILED,
    EVIDENCE_ANALYTICS_LATENCY,
    EVIDENCE_ANALYTICS_REQUESTED,
)

EVIDENCE_ANALYTICS_EVENT_TYPES: tuple[str, ...] = (
    EVIDENCE_ANALYTICS_REQUESTED,
    EVIDENCE_ANALYTICS_COMPLETED,
    EVIDENCE_ANALYTICS_FAILED,
    EVIDENCE_ANALYTICS_LATENCY,
)

_SOURCE = "analytics_projection"


def emit_evidence_analytics_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Analytics & Projection event."""
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
    audience: str = "governance",
    evaluation_count: int = 0,
    observation_count: int = 0,
    evidence_count: int = 0,
) -> IntegrationEvent:
    """Emit EVIDENCE_ANALYTICS_REQUESTED."""
    return emit_evidence_analytics_event(
        events,
        EVIDENCE_ANALYTICS_REQUESTED,
        {
            "audience": audience,
            "evaluation_count": evaluation_count,
            "observation_count": observation_count,
            "evidence_count": evidence_count,
            "adapter_id": _SOURCE,
            "mode": "analytics",
            "influences_student": False,
        },
    )


def emit_completed(
    events: EventRegistry,
    *,
    summary_id: str = "",
    projection_id: str = "",
    audience: str = "governance",
    evaluation_count: int = 0,
    observation_count: int = 0,
    evidence_count: int = 0,
    metric_count: int = 0,
    contents_ref: str = "",
) -> IntegrationEvent:
    """Emit EVIDENCE_ANALYTICS_COMPLETED."""
    return emit_evidence_analytics_event(
        events,
        EVIDENCE_ANALYTICS_COMPLETED,
        {
            "summary_id": summary_id,
            "projection_id": projection_id,
            "audience": audience,
            "evaluation_count": evaluation_count,
            "observation_count": observation_count,
            "evidence_count": evidence_count,
            "metric_count": metric_count,
            "contents_ref": contents_ref,
            "adapter_id": _SOURCE,
            "authority": "evidence_platform",
            "influences_student": False,
            "promotes_policy": False,
        },
    )


def emit_failed(
    events: EventRegistry,
    *,
    audience: str = "governance",
    error_code: str = "INVALID_STATE",
    message: str = "",
) -> IntegrationEvent:
    """Emit EVIDENCE_ANALYTICS_FAILED."""
    return emit_evidence_analytics_event(
        events,
        EVIDENCE_ANALYTICS_FAILED,
        {
            "audience": audience,
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
    audience: str = "governance",
    duration_ms: float | int | None = None,
    ok: bool = True,
) -> IntegrationEvent:
    """Emit EVIDENCE_ANALYTICS_LATENCY."""
    return emit_evidence_analytics_event(
        events,
        EVIDENCE_ANALYTICS_LATENCY,
        {
            "audience": audience,
            "duration_ms": duration_ms,
            "ok": bool(ok),
            "adapter_id": _SOURCE,
            "influences_student": False,
        },
    )
