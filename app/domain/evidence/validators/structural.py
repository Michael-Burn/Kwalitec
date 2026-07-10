"""Structural validators for Evidence Candidates.

These rules check presence and type of required fields only. They do not
encode educational, scoring, or Twin-update business logic.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.domain.evidence.evidence_candidate import EvidenceCandidate
from app.domain.evidence.evidence_category import EvidenceCategory
from app.domain.evidence.validation_message import ValidationMessage
from app.domain.evidence.validation_severity import ValidationSeverity
from app.domain.evidence.validators.base_validator import BaseValidator
from app.domain.learning_events.learning_event import LearningEvent


def _error(code: str, message: str, field: str) -> ValidationMessage:
    return ValidationMessage(
        code=code,
        message=message,
        severity=ValidationSeverity.ERROR,
        field=field,
    )


class IdentifierPresentValidator(BaseValidator):
    """Require a non-empty candidate identifier string."""

    def validate(self, candidate: EvidenceCandidate) -> list[ValidationMessage]:
        identifier = candidate.identifier
        if not isinstance(identifier, str) or not identifier.strip():
            return [
                _error(
                    "missing_identifier",
                    "Evidence Candidate identifier must be a non-empty string.",
                    "identifier",
                )
            ]
        return []


class CategoryPresentValidator(BaseValidator):
    """Require a recognised EvidenceCategory value."""

    def validate(self, candidate: EvidenceCandidate) -> list[ValidationMessage]:
        category = candidate.category
        if not isinstance(category, EvidenceCategory):
            return [
                _error(
                    "missing_category",
                    "Evidence Candidate category must be an EvidenceCategory.",
                    "category",
                )
            ]
        return []


class TimestampPresentValidator(BaseValidator):
    """Require a datetime timestamp on the candidate."""

    def validate(self, candidate: EvidenceCandidate) -> list[ValidationMessage]:
        timestamp = candidate.timestamp
        if not isinstance(timestamp, datetime):
            return [
                _error(
                    "missing_timestamp",
                    "Evidence Candidate timestamp must be a datetime.",
                    "timestamp",
                )
            ]
        return []


class OriginatingEventPresentValidator(BaseValidator):
    """Require a LearningEvent as the originating event."""

    def validate(self, candidate: EvidenceCandidate) -> list[ValidationMessage]:
        event = candidate.originating_event
        if not isinstance(event, LearningEvent):
            return [
                _error(
                    "missing_originating_event",
                    "Evidence Candidate originating_event must be a LearningEvent.",
                    "originating_event",
                )
            ]
        return []


class SourcePresentValidator(BaseValidator):
    """Require non-empty provenance (source attribution) on the candidate."""

    def validate(self, candidate: EvidenceCandidate) -> list[ValidationMessage]:
        provenance = candidate.provenance
        if not isinstance(provenance, str) or not provenance.strip():
            return [
                _error(
                    "missing_source",
                    "Evidence Candidate provenance (source) must be non-empty.",
                    "provenance",
                )
            ]
        return []


class MetadataPresentValidator(BaseValidator):
    """Require a metadata mapping object on the candidate."""

    def validate(self, candidate: EvidenceCandidate) -> list[ValidationMessage]:
        metadata = candidate.metadata
        if not isinstance(metadata, dict):
            return [
                _error(
                    "missing_metadata",
                    "Evidence Candidate metadata must be a dict object.",
                    "metadata",
                )
            ]
        return []


class PayloadPresentValidator(BaseValidator):
    """Require a payload mapping when the candidate carries a payload field.

    Empty payloads are structurally valid. A missing or non-mapping payload
    is rejected. Educational rules about *what* the payload must contain are
    out of scope.
    """

    def validate(self, candidate: EvidenceCandidate) -> list[ValidationMessage]:
        payload: Any = candidate.payload
        if not isinstance(payload, dict):
            return [
                _error(
                    "missing_payload",
                    "Evidence Candidate payload must be a dict when present.",
                    "payload",
                )
            ]
        return []


def default_structural_validators() -> list[BaseValidator]:
    """Return the standard structural validator set in evaluation order."""
    return [
        IdentifierPresentValidator(),
        CategoryPresentValidator(),
        TimestampPresentValidator(),
        OriginatingEventPresentValidator(),
        SourcePresentValidator(),
        MetadataPresentValidator(),
        PayloadPresentValidator(),
    ]
