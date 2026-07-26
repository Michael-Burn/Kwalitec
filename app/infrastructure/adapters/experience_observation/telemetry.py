"""Structured logging / telemetry for Experience Observation (P2-MS007).

Logs JourneyEvent publication, ExperienceObservation publication, and
Evidence intake acknowledgement. Correlation IDs only — no PII, no
educational conclusions.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    EXPERIENCE_DIAG_EVIDENCE_ACK,
    EXPERIENCE_DIAG_JOURNEY_EVENT,
    EXPERIENCE_DIAG_OBSERVATION_PUBLISHED,
)

_SOURCE = "experience_diagnostics"

LOG_JOURNEY_EVENT = "experience_diagnostics.journey_event"
LOG_OBSERVATION_PUBLISHED = "experience_diagnostics.observation_published"
LOG_EVIDENCE_ACK = "experience_diagnostics.evidence_ack"


def _base_fields(**fields: Any) -> dict[str, Any]:
    """Operational fields with hard privacy / authority invariants."""
    payload = {
        "influences_student": False,
        "source": _SOURCE,
        **fields,
    }
    # Defence in depth — never allow student identifiers into diagnostics logs.
    payload.pop("student_id", None)
    payload.pop("email", None)
    payload.pop("user_id", None)
    return payload


class ExperienceDiagnosticsLogger:
    """Structured operational logger for the observation pipeline."""

    def __init__(
        self,
        *,
        structured: StructuredLogger | None = None,
        events: EventRegistry | None = None,
        enabled: bool = True,
    ) -> None:
        self._structured = structured or StructuredLogger(
            "kwalitec.experience_diagnostics"
        )
        self._events = events
        self._enabled = bool(enabled)

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def structured(self) -> StructuredLogger:
        return self._structured

    @property
    def records(self) -> tuple[dict[str, Any], ...]:
        return self._structured.records

    def clear(self) -> None:
        self._structured.clear()

    def _emit_integration(
        self, event_type: str, payload: dict[str, Any]
    ) -> IntegrationEvent | None:
        if self._events is None:
            return None
        ids = CorrelationContext.current()
        event = IntegrationEvent.create(
            event_type,
            dict(payload),
            correlation_id=ids.correlation_id or payload.get("correlation_id", ""),
            source=_SOURCE,
        )
        self._events.publish(event)
        return event

    def log_journey_event(
        self,
        *,
        correlation_id: str,
        journey_stage: str,
        experience_event: str,
        trace_id: str = "",
        pipeline_stage: str = "",
    ) -> dict[str, Any] | None:
        """Log JourneyEvent entry into the observation pipeline."""
        if not self._enabled:
            return None
        fields = _base_fields(
            correlation_id=(correlation_id or "").strip(),
            journey_stage=(journey_stage or "").strip().lower(),
            experience_event=(experience_event or "").strip().lower(),
            trace_id=(trace_id or "").strip(),
            pipeline_stage=(pipeline_stage or "").strip().lower(),
            event_kind="journey_event",
        )
        record = self._structured.info(LOG_JOURNEY_EVENT, **fields)
        self._emit_integration(EXPERIENCE_DIAG_JOURNEY_EVENT, fields)
        return record

    def log_observation_published(
        self,
        *,
        correlation_id: str,
        journey_stage: str,
        experience_event: str,
        observation_status: str,
        observation_id: str = "",
        reason: str = "",
        trace_id: str = "",
        latency_ms: float | None = None,
    ) -> dict[str, Any] | None:
        """Log ExperienceObservation publish attempt outcome."""
        if not self._enabled:
            return None
        fields = _base_fields(
            correlation_id=(correlation_id or "").strip(),
            journey_stage=(journey_stage or "").strip().lower(),
            experience_event=(experience_event or "").strip().lower(),
            observation_status=(observation_status or "").strip().lower(),
            observation_id=(observation_id or "").strip(),
            reason=(reason or "").strip(),
            trace_id=(trace_id or "").strip(),
            latency_ms=latency_ms,
            event_kind="observation_published",
        )
        record = self._structured.info(LOG_OBSERVATION_PUBLISHED, **fields)
        self._emit_integration(EXPERIENCE_DIAG_OBSERVATION_PUBLISHED, fields)
        return record

    def log_evidence_ack(
        self,
        *,
        correlation_id: str,
        experience_event: str,
        observation_id: str = "",
        evidence_id: str = "",
        observation_status: str = "",
        reason: str = "",
        trace_id: str = "",
        latency_ms: float | None = None,
    ) -> dict[str, Any] | None:
        """Log Evidence intake acknowledgement (accept / reject / skip)."""
        if not self._enabled:
            return None
        fields = _base_fields(
            correlation_id=(correlation_id or "").strip(),
            experience_event=(experience_event or "").strip().lower(),
            observation_id=(observation_id or "").strip(),
            evidence_id=(evidence_id or "").strip(),
            observation_status=(observation_status or "").strip().lower(),
            reason=(reason or "").strip(),
            trace_id=(trace_id or "").strip(),
            latency_ms=latency_ms,
            event_kind="evidence_ack",
        )
        record = self._structured.info(LOG_EVIDENCE_ACK, **fields)
        self._emit_integration(EXPERIENCE_DIAG_EVIDENCE_ACK, fields)
        return record


def build_experience_diagnostics_logger(
    *,
    enabled: bool = True,
    structured: StructuredLogger | None = None,
    events: EventRegistry | None = None,
) -> ExperienceDiagnosticsLogger:
    """DI helper for ExperienceDiagnosticsLogger."""
    return ExperienceDiagnosticsLogger(
        structured=structured,
        events=events,
        enabled=enabled,
    )
