"""Observational telemetry for Twin & Authority soak (EP-002.3).

Events do not mutate educational state or influence student UX.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.adapters.consumer_chain.soak_contracts import (
    LOG_SOAK_COMPLETED,
    LOG_SOAK_FAILED,
    LOG_SOAK_HEALTH,
    LOG_SOAK_MATRIX,
    LOG_SOAK_REQUESTED,
    LOG_SOAK_ROLLBACK,
    SOAK_ADAPTER_ID,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    CONSUMER_CHAIN_SOAK_COMPLETED,
    CONSUMER_CHAIN_SOAK_FAILED,
    CONSUMER_CHAIN_SOAK_HEALTH,
    CONSUMER_CHAIN_SOAK_MATRIX,
    CONSUMER_CHAIN_SOAK_REQUESTED,
    CONSUMER_CHAIN_SOAK_ROLLBACK_VERIFIED,
)

_SOURCE = SOAK_ADAPTER_ID


def _emit_integration(
    events: EventRegistry,
    event_type: str,
    payload: dict[str, Any],
) -> IntegrationEvent:
    ids = CorrelationContext.current()
    event = IntegrationEvent.create(
        event_type,
        dict(payload),
        correlation_id=ids.correlation_id or "",
        source=_SOURCE,
    )
    events.publish(event)
    return event


def emit_requested(
    *,
    structured: StructuredLogger,
    events: EventRegistry,
    student_id: str,
    cell_id: str = "",
) -> None:
    fields = {
        "adapter_id": _SOURCE,
        "cell_id": cell_id,
        "influences_student": False,
        "mode": "twin_authority_soak",
        "student_id": student_id,
    }
    structured.info(LOG_SOAK_REQUESTED, **fields)
    _emit_integration(events, CONSUMER_CHAIN_SOAK_REQUESTED, fields)


def emit_completed(
    *,
    structured: StructuredLogger,
    events: EventRegistry,
    student_id: str,
    api_name: str,
    outcome: str,
    latency_ms: float,
    twin_enabled: bool,
    authority_enabled: bool,
) -> None:
    fields = {
        "adapter_id": _SOURCE,
        "api_name": api_name,
        "authority_enabled": bool(authority_enabled),
        "influences_student": False,
        "latency_ms": round(float(latency_ms), 3),
        "mode": "twin_authority_soak",
        "outcome": outcome,
        "student_id": student_id,
        "twin_enabled": bool(twin_enabled),
    }
    structured.info(LOG_SOAK_COMPLETED, **fields)
    _emit_integration(events, CONSUMER_CHAIN_SOAK_COMPLETED, fields)


def emit_failed(
    *,
    structured: StructuredLogger,
    events: EventRegistry,
    student_id: str,
    api_name: str,
    error_code: str,
    latency_ms: float,
) -> None:
    fields = {
        "adapter_id": _SOURCE,
        "api_name": api_name,
        "error_code": error_code,
        "influences_student": False,
        "latency_ms": round(float(latency_ms), 3),
        "mode": "twin_authority_soak",
        "student_id": student_id,
    }
    structured.warning(LOG_SOAK_FAILED, **fields)
    _emit_integration(events, CONSUMER_CHAIN_SOAK_FAILED, fields)


def emit_health(
    *,
    structured: StructuredLogger,
    events: EventRegistry,
    snapshot: dict[str, Any],
) -> None:
    fields = {
        "adapter_id": _SOURCE,
        "influences_student": False,
        "mode": "twin_authority_soak",
        **snapshot,
    }
    structured.info(LOG_SOAK_HEALTH, **fields)
    _emit_integration(events, CONSUMER_CHAIN_SOAK_HEALTH, fields)


def emit_matrix_cell(
    *,
    structured: StructuredLogger,
    events: EventRegistry,
    cell: dict[str, Any],
) -> None:
    fields = {
        "adapter_id": _SOURCE,
        "influences_student": False,
        "mode": "twin_authority_soak",
        **cell,
    }
    structured.info(LOG_SOAK_MATRIX, **fields)
    _emit_integration(events, CONSUMER_CHAIN_SOAK_MATRIX, fields)


def emit_rollback_verified(
    *,
    structured: StructuredLogger,
    events: EventRegistry,
    ok: bool,
    details: tuple[str, ...] | list[str],
) -> None:
    fields = {
        "adapter_id": _SOURCE,
        "details": list(details),
        "influences_student": False,
        "mode": "twin_authority_soak",
        "ok": bool(ok),
    }
    structured.info(LOG_SOAK_ROLLBACK, **fields)
    _emit_integration(events, CONSUMER_CHAIN_SOAK_ROLLBACK_VERIFIED, fields)


__all__ = [
    "emit_completed",
    "emit_failed",
    "emit_health",
    "emit_matrix_cell",
    "emit_requested",
    "emit_rollback_verified",
]
