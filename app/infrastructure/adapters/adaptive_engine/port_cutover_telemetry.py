"""Observational telemetry for Adaptive Experience Port Cutover (MS-003 A4).

Events do not mutate educational state. Fallback events record when Experience
returns RecommendationService output after an adaptive attempt.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    ADAPTIVE_ENGINE_FAILURE,
    ADAPTIVE_ENGINE_FALLBACK,
    ADAPTIVE_ENGINE_LATENCY,
    ADAPTIVE_ENGINE_REQUESTED,
    ADAPTIVE_ENGINE_SUCCESS,
)

ADAPTIVE_ENGINE_EVENT_TYPES: tuple[str, ...] = (
    ADAPTIVE_ENGINE_REQUESTED,
    ADAPTIVE_ENGINE_SUCCESS,
    ADAPTIVE_ENGINE_FAILURE,
    ADAPTIVE_ENGINE_FALLBACK,
    ADAPTIVE_ENGINE_LATENCY,
)

_SOURCE = "adaptive_experience_port_router"


def emit_adaptive_engine_event(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any] | None = None,
) -> IntegrationEvent:
    """Publish one observational Adaptive Engine cutover event."""
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
) -> IntegrationEvent:
    return emit_adaptive_engine_event(
        events,
        ADAPTIVE_ENGINE_REQUESTED,
        {
            "student_id": student_id,
            "authority": "adaptive_engine",
            "phase": "a4_experience_cutover",
        },
    )


def emit_success(
    events: EventRegistry,
    *,
    student_id: str,
    decision_id: str = "",
    confidence_band: str = "",
    topic_code: str = "",
) -> IntegrationEvent:
    return emit_adaptive_engine_event(
        events,
        ADAPTIVE_ENGINE_SUCCESS,
        {
            "student_id": student_id,
            "decision_id": decision_id,
            "confidence_band": confidence_band,
            "topic_code": topic_code,
            "authority": "adaptive_engine",
            "fallback_used": False,
        },
    )


def emit_failure(
    events: EventRegistry,
    *,
    student_id: str,
    error_code: str,
    message: str = "",
) -> IntegrationEvent:
    return emit_adaptive_engine_event(
        events,
        ADAPTIVE_ENGINE_FAILURE,
        {
            "student_id": student_id,
            "error_code": error_code,
            "message": message,
            "authority": "adaptive_engine",
        },
    )


def emit_fallback(
    events: EventRegistry,
    *,
    student_id: str,
    reason: str,
    error_code: str | None = None,
    decision_id: str = "",
) -> IntegrationEvent:
    return emit_adaptive_engine_event(
        events,
        ADAPTIVE_ENGINE_FALLBACK,
        {
            "student_id": student_id,
            "reason": reason,
            "error_code": error_code,
            "decision_id": decision_id,
            "fallback_target": "recommendation_service",
            "authority": "recommendation_bridge",
        },
    )


def emit_latency(
    events: EventRegistry,
    *,
    student_id: str,
    latency_ms: float,
    fallback_used: bool,
) -> IntegrationEvent:
    return emit_adaptive_engine_event(
        events,
        ADAPTIVE_ENGINE_LATENCY,
        {
            "student_id": student_id,
            "latency_ms": round(float(latency_ms), 3),
            "fallback_used": bool(fallback_used),
            "authority": "adaptive_engine",
        },
    )


__all__ = [
    "ADAPTIVE_ENGINE_EVENT_TYPES",
    "emit_adaptive_engine_event",
    "emit_failure",
    "emit_fallback",
    "emit_latency",
    "emit_requested",
    "emit_success",
]
