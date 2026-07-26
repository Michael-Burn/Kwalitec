"""Structured telemetry for EP-001 consumer-chain ``build_*`` APIs.

Reuses ``StructuredLogger``, ``CorrelationContext``, and optional
``EventRegistry`` — does not invent a second telemetry framework.
Events are observational only and never influence student-facing responses.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.adapters.consumer_chain.contracts import (
    LOG_CONSUMER_CHAIN_COMPLETED,
    LOG_CONSUMER_CHAIN_CUTOVER,
    LOG_CONSUMER_CHAIN_DUAL_RUN,
    LOG_CONSUMER_CHAIN_FAILED,
    LOG_CONSUMER_CHAIN_INVOKED,
    LOG_FOUNDATION_ASSEMBLE,
)
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.base import IntegrationEvent
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    CONSUMER_CHAIN_COMPLETED,
    CONSUMER_CHAIN_CUTOVER,
    CONSUMER_CHAIN_DUAL_RUN,
    CONSUMER_CHAIN_FAILED,
    CONSUMER_CHAIN_FOUNDATION_ASSEMBLE,
    CONSUMER_CHAIN_LATENCY,
    CONSUMER_CHAIN_REQUESTED,
)

_SOURCE = "consumer_chain_observability"


class ConsumerChainTelemetry:
    """Emit structured invocation / outcome / latency for ``build_*`` APIs."""

    def __init__(
        self,
        *,
        structured: StructuredLogger | None = None,
        events: EventRegistry | None = None,
        enabled: bool = True,
    ) -> None:
        self._structured = structured or StructuredLogger(
            "kwalitec.consumer_chain"
        )
        self._events = events if events is not None else EventRegistry()
        self._enabled = bool(enabled)

    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def structured(self) -> StructuredLogger:
        return self._structured

    @property
    def events(self) -> EventRegistry:
        return self._events

    @property
    def records(self) -> tuple[dict[str, Any], ...]:
        return self._structured.records

    def clear(self) -> None:
        self._structured.clear()
        self._events.clear()

    def _base_fields(self, **fields: Any) -> dict[str, Any]:
        ids = CorrelationContext.current()
        payload = {
            "influences_student": False,
            "source": _SOURCE,
            "correlation_id": ids.correlation_id or "",
            "causation_id": ids.causation_id or "",
            **fields,
        }
        return payload

    def _emit_integration(
        self, event_type: str, payload: dict[str, Any]
    ) -> IntegrationEvent | None:
        if not self._enabled:
            return None
        ids = CorrelationContext.current()
        event = IntegrationEvent.create(
            event_type,
            dict(payload),
            correlation_id=ids.correlation_id or "",
            source=_SOURCE,
        )
        self._events.publish(event)
        return event

    def emit_requested(
        self,
        *,
        service_name: str,
        api_name: str,
        student_id: str,
        twin_enabled: bool,
        authority_enabled: bool,
        timestamp: str | None = None,
    ) -> dict[str, Any] | None:
        """Record that a ``build_*`` API was invoked."""
        if not self._enabled:
            return None
        fields = self._base_fields(
            service_name=service_name,
            api_name=api_name,
            student_id=str(student_id),
            twin_enabled=bool(twin_enabled),
            authority_enabled=bool(authority_enabled),
            timestamp=timestamp or "",
            event_kind="requested",
        )
        record = self._structured.info(LOG_CONSUMER_CHAIN_INVOKED, **fields)
        self._emit_integration(CONSUMER_CHAIN_REQUESTED, fields)
        return record

    def emit_completed(
        self,
        *,
        service_name: str,
        api_name: str,
        student_id: str,
        twin_enabled: bool,
        authority_enabled: bool,
        outcome: str,
        duration_ms: float,
        returned_none: bool,
        limitation_codes: tuple[str, ...] | list[str] | None = None,
        confidence_available: bool | None = None,
        timestamp: str | None = None,
    ) -> dict[str, Any] | None:
        """Record successful observation of a ``build_*`` completion."""
        if not self._enabled:
            return None
        codes = tuple(limitation_codes or ())
        fields = self._base_fields(
            service_name=service_name,
            api_name=api_name,
            student_id=str(student_id),
            twin_enabled=bool(twin_enabled),
            authority_enabled=bool(authority_enabled),
            outcome=outcome,
            duration_ms=round(float(duration_ms), 3),
            returned_none=bool(returned_none),
            limitation_codes=list(codes),
            limitation_codes_present=bool(codes),
            confidence_available=confidence_available,
            timestamp=timestamp or "",
            event_kind="completed",
        )
        record = self._structured.info(LOG_CONSUMER_CHAIN_COMPLETED, **fields)
        self._emit_integration(CONSUMER_CHAIN_COMPLETED, fields)
        self._emit_integration(
            CONSUMER_CHAIN_LATENCY,
            {
                "service_name": service_name,
                "api_name": api_name,
                "student_id": str(student_id),
                "duration_ms": fields["duration_ms"],
                "outcome": outcome,
                "influences_student": False,
                "source": _SOURCE,
            },
        )
        return record

    def emit_failed(
        self,
        *,
        service_name: str,
        api_name: str,
        student_id: str,
        twin_enabled: bool,
        authority_enabled: bool,
        duration_ms: float,
        error_code: str,
        error_message: str | None = None,
        timestamp: str | None = None,
    ) -> dict[str, Any] | None:
        """Record an exception outcome (observational; does not swallow)."""
        if not self._enabled:
            return None
        fields = self._base_fields(
            service_name=service_name,
            api_name=api_name,
            student_id=str(student_id),
            twin_enabled=bool(twin_enabled),
            authority_enabled=bool(authority_enabled),
            outcome="exception",
            duration_ms=round(float(duration_ms), 3),
            returned_none=True,
            error_code=error_code,
            error_message=(error_message or "")[:256],
            timestamp=timestamp or "",
            event_kind="failed",
        )
        record = self._structured.error(LOG_CONSUMER_CHAIN_FAILED, **fields)
        self._emit_integration(CONSUMER_CHAIN_FAILED, fields)
        return record

    def emit_dual_run(
        self,
        *,
        api_name: str,
        student_id: str,
        twin_enabled: bool,
        authority_enabled: bool,
        legacy_fingerprint: str,
        build_fingerprint: str,
        fingerprints_match: bool,
        environment: str,
        legacy_latency_ms: float | None = None,
        twin_latency_ms: float | None = None,
        legacy_unavailable: bool | None = None,
        twin_unavailable: bool | None = None,
        limitation_codes: tuple[str, ...] | list[str] | None = None,
        confidence_level: str | None = None,
        confidence_available: bool | None = None,
        legacy_categories: tuple[str, ...] | list[str] | None = None,
        twin_field_ids: tuple[str, ...] | list[str] | None = None,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> dict[str, Any] | None:
        """Record a non-production diagnostic legacy vs ``build_*`` compare."""
        if not self._enabled:
            return None
        fields = self._base_fields(
            api_name=api_name,
            student_id=str(student_id),
            twin_enabled=bool(twin_enabled),
            authority_enabled=bool(authority_enabled),
            legacy_fingerprint=legacy_fingerprint,
            build_fingerprint=build_fingerprint,
            fingerprints_match=bool(fingerprints_match),
            environment=environment,
            diagnostic_only=True,
            influences_student=False,
            event_kind="dual_run",
            legacy_latency_ms=legacy_latency_ms,
            twin_latency_ms=twin_latency_ms,
            legacy_unavailable=legacy_unavailable,
            twin_unavailable=twin_unavailable,
            limitation_codes=list(limitation_codes or ()),
            confidence_level=confidence_level or "",
            confidence_available=confidence_available,
            legacy_categories=list(legacy_categories or ()),
            twin_field_ids=list(twin_field_ids or ()),
        )
        if correlation_id is not None:
            fields["correlation_id"] = correlation_id
        if causation_id is not None:
            fields["causation_id"] = causation_id
        record = self._structured.info(LOG_CONSUMER_CHAIN_DUAL_RUN, **fields)
        self._emit_integration(CONSUMER_CHAIN_DUAL_RUN, fields)
        return record

    def emit_cutover(
        self,
        *,
        api_name: str,
        student_id: str,
        environment: str,
        cutover_attempted: bool,
        cutover_served: bool,
        influences_student: bool,
        fallback_reason: str = "",
        alignment_status: str = "",
        aligned: bool = False,
        mismatched: bool = False,
        twin_topic_ids: list[str] | tuple[str, ...] | None = None,
        limitation_codes: list[str] | tuple[str, ...] | None = None,
        legacy_latency_ms: float | None = None,
        twin_latency_ms: float | None = None,
        twin_enabled: bool = False,
        authority_enabled: bool = False,
        cutover_enabled: bool = False,
        twin_exception: bool = False,
        correlation_id: str | None = None,
        causation_id: str | None = None,
    ) -> dict[str, Any] | None:
        """Record an EP-002.5 Study Insights HTTP cutover decision."""
        if not self._enabled:
            return None
        fields = self._base_fields(
            api_name=api_name,
            student_id=str(student_id),
            environment=environment,
            cutover_attempted=bool(cutover_attempted),
            cutover_served=bool(cutover_served),
            influences_student=bool(influences_student),
            fallback_reason=fallback_reason or "",
            alignment_status=alignment_status or "",
            aligned=bool(aligned),
            mismatched=bool(mismatched),
            twin_topic_ids=list(twin_topic_ids or ()),
            limitation_codes=list(limitation_codes or ()),
            legacy_latency_ms=legacy_latency_ms,
            twin_latency_ms=twin_latency_ms,
            twin_enabled=bool(twin_enabled),
            authority_enabled=bool(authority_enabled),
            cutover_enabled=bool(cutover_enabled),
            twin_exception=bool(twin_exception),
            event_kind="cutover",
        )
        if correlation_id is not None:
            fields["correlation_id"] = correlation_id
        if causation_id is not None:
            fields["causation_id"] = causation_id
        record = self._structured.info(LOG_CONSUMER_CHAIN_CUTOVER, **fields)
        self._emit_integration(CONSUMER_CHAIN_CUTOVER, fields)
        return record

    def emit_foundation_assemble(
        self,
        *,
        service_name: str,
        api_name: str,
        student_id: str,
        assemble_source: str,
        assembled: bool,
    ) -> dict[str, Any] | None:
        """Record Foundation CLS assemble vs composition-local share-hit.

        Observational only (EP-002.2). ``assembled=True`` means
        ``Foundation.assemble`` ran; ``False`` means an injected CLS was reused.
        """
        if not self._enabled:
            return None
        fields = self._base_fields(
            service_name=service_name,
            api_name=api_name,
            student_id=str(student_id),
            assemble_source=assemble_source,
            assembled=bool(assembled),
            event_kind="foundation_assemble",
        )
        record = self._structured.info(LOG_FOUNDATION_ASSEMBLE, **fields)
        self._emit_integration(CONSUMER_CHAIN_FOUNDATION_ASSEMBLE, fields)
        return record


_DEFAULT: ConsumerChainTelemetry | None = None


def get_consumer_chain_telemetry() -> ConsumerChainTelemetry:
    """Return the process-default consumer-chain telemetry sink."""
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = ConsumerChainTelemetry()
    return _DEFAULT


def set_consumer_chain_telemetry(
    telemetry: ConsumerChainTelemetry | None,
) -> ConsumerChainTelemetry | None:
    """Replace the process-default sink (tests). Returns previous."""
    global _DEFAULT
    previous = _DEFAULT
    _DEFAULT = telemetry
    return previous


def build_consumer_chain_telemetry(
    *,
    enabled: bool = True,
    structured: StructuredLogger | None = None,
    events: EventRegistry | None = None,
) -> ConsumerChainTelemetry:
    """Factory for a consumer-chain telemetry instance."""
    return ConsumerChainTelemetry(
        structured=structured,
        events=events,
        enabled=enabled,
    )
