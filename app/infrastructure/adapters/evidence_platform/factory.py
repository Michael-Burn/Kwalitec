"""Evidence Factory (MS-006 E1).

Deterministic EvidenceRecord construction: collect → assemble → validate →
assign evidence_id. Emits collection telemetry. No persistence, policy
evaluation, analytics, or upstream educational writes. Experiment assignment
is owned by ExperimentFramework (E2), not this factory.
"""

from __future__ import annotations

import hashlib
import time
from collections.abc import Mapping
from dataclasses import replace
from typing import Any

from app.infrastructure.adapters.evidence_platform.assembler import EvidenceAssembler
from app.infrastructure.adapters.evidence_platform.collection_telemetry import (
    emit_completed,
    emit_failed,
    emit_latency,
    emit_requested,
)
from app.infrastructure.adapters.evidence_platform.collector import EvidenceCollector
from app.infrastructure.adapters.evidence_platform.contracts import (
    EVIDENCE_VERSION_E1,
    EvidenceContext,
    EvidenceRecord,
    ObservedEvent,
    serialize_canonical,
)
from app.infrastructure.adapters.evidence_platform.validation import (
    EvidenceValidationError,
    EvidenceValidator,
)
from app.infrastructure.events.registry import EventRegistry


class EvidenceFactory:
    """Create immutable EvidenceRecords from observed educational events.

    Identical observed event material + engine version → identical EvidenceRecord
    (including evidence_id) every execution.
    """

    FACTORY_ID = "evidence_factory"
    FACTORY_VERSION = "1.0.0-e1"
    ENGINE_VERSION = EVIDENCE_VERSION_E1

    def __init__(
        self,
        *,
        collector: EvidenceCollector | None = None,
        assembler: EvidenceAssembler | None = None,
        validator: EvidenceValidator | None = None,
        events: EventRegistry | None = None,
        enabled: bool = True,
    ) -> None:
        self._validator = validator or EvidenceValidator()
        self._collector = collector or EvidenceCollector(validator=self._validator)
        self._assembler = assembler or EvidenceAssembler(validator=self._validator)
        self._events = events
        self._enabled = bool(enabled)

    @property
    def factory_id(self) -> str:
        return self.FACTORY_ID

    @property
    def factory_version(self) -> str:
        return self.FACTORY_VERSION

    @property
    def collector(self) -> EvidenceCollector:
        return self._collector

    @property
    def assembler(self) -> EvidenceAssembler:
        return self._assembler

    @property
    def validator(self) -> EvidenceValidator:
        return self._validator

    def is_enabled(self) -> bool:
        return self._enabled

    def create(
        self,
        event: ObservedEvent | EvidenceContext | Mapping[str, Any],
    ) -> EvidenceRecord:
        """Collect → assemble → validate → assign deterministic evidence_id."""
        if not self._enabled:
            raise EvidenceValidationError(
                "EvidenceFactory is disabled (feature flag OFF)"
            )

        student_id = _peek_student_id(event)
        event_type = _peek_event_type(event)
        as_of = _peek_as_of(event)
        started = time.perf_counter()
        if self._events is not None:
            emit_requested(
                self._events,
                student_id=student_id or "",
                event_type=event_type,
                as_of=as_of,
            )
        try:
            observation = self._collector.collect(event)
            draft = self._assembler.assemble(observation)
            evidence_id = deterministic_evidence_id(draft)
            record = replace(draft, evidence_id=evidence_id)
            validated = self._validator.validate_evidence_record(record)
            if self._events is not None:
                emit_completed(
                    self._events,
                    student_id=validated.student_id,
                    evidence_id=validated.evidence_id,
                    evidence_class=validated.evidence_class,
                    event_type=validated.event_type,
                    quality_result=validated.quality.result,
                    runtime_a_ref_present=validated.quality.runtime_a_ref_present,
                )
                emit_latency(
                    self._events,
                    student_id=validated.student_id,
                    duration_ms=round((time.perf_counter() - started) * 1000, 3),
                    ok=True,
                )
            return validated
        except Exception as exc:
            if self._events is not None:
                emit_failed(
                    self._events,
                    student_id=student_id or "",
                    error_code=type(exc).__name__,
                    message=str(exc),
                )
                emit_latency(
                    self._events,
                    student_id=student_id or "",
                    duration_ms=round((time.perf_counter() - started) * 1000, 3),
                    ok=False,
                )
            raise

    def create_from_context(self, context: EvidenceContext) -> EvidenceRecord:
        """Convenience: create EvidenceRecord from EvidenceContext."""
        if not isinstance(context, EvidenceContext):
            raise EvidenceValidationError("context must be an EvidenceContext")
        return self.create(context)

    def create_from_observed_event(self, event: ObservedEvent) -> EvidenceRecord:
        """Convenience: create EvidenceRecord from ObservedEvent."""
        if not isinstance(event, ObservedEvent):
            raise EvidenceValidationError("event must be an ObservedEvent")
        return self.create(event)


def deterministic_evidence_id(record: EvidenceRecord) -> str:
    """Derive evidence_id from material fields + engine version (excludes id)."""
    material = {
        "as_of": record.as_of,
        "claim_boundary": record.claim_boundary,
        "engine_version": record.engine_version or EVIDENCE_VERSION_E1,
        "event_type": record.event_type,
        "evidence_class": record.evidence_class,
        "evidence_version": record.evidence_version or EVIDENCE_VERSION_E1,
        "ingested_at": record.ingested_at,
        "limitations": list(record.limitations),
        "observed_at": record.observed_at,
        "payload_summary": dict(record.payload_summary),
        "provenance": dict(record.provenance),
        "quality": record.quality.to_canonical_dict(),
        "source_refs": [ref.to_canonical_dict() for ref in record.source_refs],
        "student_id": record.student_id,
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()
    return f"ev-{digest[:24]}"


def build_evidence_factory(
    *,
    enabled: bool,
    collector: EvidenceCollector | None = None,
    assembler: EvidenceAssembler | None = None,
    validator: EvidenceValidator | None = None,
    events: EventRegistry | None = None,
) -> EvidenceFactory | None:
    """DI helper — construct EvidenceFactory only when the flag is on."""
    if not enabled:
        return None
    return EvidenceFactory(
        collector=collector,
        assembler=assembler,
        validator=validator,
        events=events,
        enabled=True,
    )


def _peek_student_id(
    event: ObservedEvent | EvidenceContext | Mapping[str, Any],
) -> str:
    if isinstance(event, ObservedEvent | EvidenceContext):
        return event.student_id
    if isinstance(event, Mapping):
        return str(event.get("student_id") or "")
    return ""


def _peek_event_type(
    event: ObservedEvent | EvidenceContext | Mapping[str, Any],
) -> str:
    if isinstance(event, ObservedEvent):
        return event.event_type
    if isinstance(event, EvidenceContext):
        return event.evidence_class.lower() if event.evidence_class else ""
    if isinstance(event, Mapping):
        return str(event.get("event_type") or "")
    return ""


def _peek_as_of(
    event: ObservedEvent | EvidenceContext | Mapping[str, Any],
) -> str | None:
    if isinstance(event, ObservedEvent | EvidenceContext):
        return event.as_of
    if isinstance(event, Mapping):
        value = event.get("as_of")
        return value if isinstance(value, str) else None
    return None
