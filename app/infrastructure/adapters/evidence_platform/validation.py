"""Evidence Platform validation (MS-006 E1).

Validates ObservedEvent / CollectedObservation / EvidenceRecord structural
integrity. Does not estimate missing educational state, score outcomes, or
mutate inputs.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    AVAILABILITY_VALUES,
    CLAIM_BOUNDARIES,
    EVIDENCE_CLASSES,
    QUALITY_RESULTS,
    EvidenceContext,
    EvidenceQuality,
    EvidenceRecord,
    ObservationRef,
    ObservedEvent,
)

# Forbidden payload keys — privacy / secrets fail closed.
FORBIDDEN_PAYLOAD_KEYS = frozenset(
    {
        "password",
        "secret",
        "secret_key",
        "token",
        "cookie",
        "session_cookie",
        "authorization",
        "database_url",
        "db_url",
        "raw_answer",
        "raw_answers",
    }
)


class EvidenceValidationError(ValueError):
    """Raised when evidence collection artefacts fail structural validation."""


class EvidenceValidator:
    """Structural validator for E1 evidence collection artefacts."""

    VALIDATOR_ID = "evidence_validator"
    VALIDATOR_VERSION = "1.0.0-e1"

    @property
    def validator_id(self) -> str:
        return self.VALIDATOR_ID

    @property
    def validator_version(self) -> str:
        return self.VALIDATOR_VERSION

    def validate_student_id(self, student_id: str) -> str:
        """Return stripped non-empty student_id or raise."""
        return validate_student_id(student_id)

    def validate_clock(self, value: str | None, *, label: str) -> str | None:
        """Validate optional ISO clock (never invent wall-clock)."""
        return validate_clock(value, label=label)

    def validate_source_refs(
        self,
        refs: tuple[ObservationRef, ...] | list[ObservationRef],
        *,
        student_id: str,
    ) -> tuple[ObservationRef, ...]:
        """Validate ObservationRefs and enforce single-student scope."""
        return validate_source_refs(refs, student_id=student_id)

    def validate_payload_privacy(self, payload: Mapping[str, Any] | None) -> None:
        """Fail closed when forbidden secret / raw-answer keys appear."""
        validate_payload_privacy(payload)

    def validate_observed_event(self, event: ObservedEvent) -> ObservedEvent:
        """Validate an ObservedEvent before collection."""
        if not isinstance(event, ObservedEvent):
            raise EvidenceValidationError("event must be an ObservedEvent")
        validate_student_id(event.student_id)
        validate_clock(event.observed_at, label="observed_at")
        validate_clock(event.ingested_at, label="ingested_at")
        validate_clock(event.as_of, label="as_of")
        validate_source_refs(event.source_refs, student_id=event.student_id)
        validate_payload_privacy(event.payload_summary)
        for block_name in ("runtime_a", "experience", "strategy", "adaptive", "twin"):
            validate_payload_privacy(getattr(event, block_name))
        return event

    def validate_evidence_context(self, context: EvidenceContext) -> EvidenceContext:
        """Validate an EvidenceContext used as collection input."""
        if not isinstance(context, EvidenceContext):
            raise EvidenceValidationError("context must be an EvidenceContext")
        validate_student_id(context.student_id)
        validate_clock(context.as_of, label="as_of")
        validate_source_refs(context.source_refs, student_id=context.student_id)
        return context

    def validate_evidence_record(self, record: EvidenceRecord) -> EvidenceRecord:
        """Validate a collected EvidenceRecord structure."""
        if not isinstance(record, EvidenceRecord):
            raise EvidenceValidationError("record must be an EvidenceRecord")
        if not (record.evidence_id or "").strip():
            raise EvidenceValidationError("evidence_id must be a non-empty string")
        validate_student_id(record.student_id)
        validate_clock(record.observed_at, label="observed_at")
        validate_clock(record.ingested_at, label="ingested_at")
        validate_clock(record.as_of, label="as_of")
        validate_source_refs(record.source_refs, student_id=record.student_id)
        if record.evidence_class and record.evidence_class not in EVIDENCE_CLASSES:
            raise EvidenceValidationError(
                f"unknown evidence_class: {record.evidence_class}"
            )
        if record.claim_boundary and record.claim_boundary not in CLAIM_BOUNDARIES:
            raise EvidenceValidationError(
                f"unknown claim_boundary: {record.claim_boundary}"
            )
        if not isinstance(record.quality, EvidenceQuality):
            raise EvidenceValidationError("quality must be an EvidenceQuality")
        if record.quality.result and record.quality.result not in QUALITY_RESULTS:
            raise EvidenceValidationError(
                f"unknown quality.result: {record.quality.result}"
            )
        if record.availability not in AVAILABILITY_VALUES:
            raise EvidenceValidationError(
                "availability must be 'available', 'unavailable', or empty"
            )
        if record.availability == "unavailable" and not (
            record.unavailable_reason or ""
        ).strip():
            raise EvidenceValidationError(
                "unavailable_reason required when availability is unavailable"
            )
        validate_payload_privacy(record.payload_summary)
        validate_payload_privacy(record.provenance)
        return record


def validate_student_id(student_id: str) -> str:
    """Return stripped non-empty student_id or raise EvidenceValidationError."""
    sid = (student_id or "").strip()
    if not sid:
        raise EvidenceValidationError("student_id must be a non-empty string")
    return sid


def validate_clock(value: str | None, *, label: str) -> str | None:
    """Validate optional ISO clock string (never invent wall-clock)."""
    if value is None:
        return None
    if not isinstance(value, str):
        raise EvidenceValidationError(f"{label} must be an ISO string or None")
    clock = value.strip()
    return clock or None


def validate_source_refs(
    refs: tuple[ObservationRef, ...] | list[ObservationRef],
    *,
    student_id: str,
) -> tuple[ObservationRef, ...]:
    """Validate ObservationRefs and enforce single-student scope."""
    sid = validate_student_id(student_id)
    frozen = tuple(refs or ())
    for ref in frozen:
        if not isinstance(ref, ObservationRef):
            raise EvidenceValidationError("source_refs must contain ObservationRef")
        ref_sid = (ref.student_id or "").strip()
        if ref_sid and ref_sid != sid:
            raise EvidenceValidationError(
                "CROSS_STUDENT_FORBIDDEN: ObservationRef.student_id mismatch"
            )
    return frozen


def validate_payload_privacy(payload: Mapping[str, Any] | None) -> None:
    """Fail closed when forbidden secret / raw-answer keys appear."""
    if not payload:
        return
    for key in payload:
        normalised = str(key).strip().lower()
        if normalised in FORBIDDEN_PAYLOAD_KEYS:
            raise EvidenceValidationError(
                f"forbidden payload key for evidence artefacts: {key}"
            )
        value = payload[key]
        if isinstance(value, Mapping):
            validate_payload_privacy(value)


def build_evidence_validator() -> EvidenceValidator:
    """DI helper — construct EvidenceValidator."""
    return EvidenceValidator()
