"""Evidence snapshot — immutable, accurate read model of one evidence record.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    Evidence Snapshot
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.educational_evidence.enums import EvidenceType
from domain.education.educational_evidence.ids import EvidenceId
from domain.education.educational_evidence.value_objects.evidence_context import (
    EvidenceContext,
)
from domain.education.educational_evidence.value_objects.evidence_metadata import (
    EvidenceMetadata,
)
from domain.education.educational_evidence.value_objects.evidence_source import (
    EvidenceSource,
)
from domain.education.educational_evidence.value_objects.evidence_timestamp import (
    EvidenceTimestamp,
)
from domain.education.educational_evidence.value_objects.evidence_weight import (
    EvidenceWeight,
)
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class EvidenceSnapshot(EducationalValueObject):
    """Immutable, accurate capture of an ``EducationalEvidence`` record.

    A snapshot is a read model produced for downstream consumers. It does
    not diagnose, estimate, or recompute — it faithfully mirrors the
    evidence at the moment it was produced.
    """

    evidence_id: EvidenceId
    student_id: str
    evidence_type: EvidenceType
    occurred_at: EvidenceTimestamp
    source: EvidenceSource
    context: EvidenceContext
    weight: EvidenceWeight
    metadata: EvidenceMetadata

    def _validate(self) -> None:
        if not isinstance(self.evidence_id, EvidenceId):
            raise EducationalInvariantViolation(
                "evidence_id must be an EvidenceId",
                invariant="EvidenceSnapshot.evidence_id.type",
            )
        if not isinstance(self.student_id, str) or not self.student_id.strip():
            raise EducationalInvariantViolation(
                "student_id must be a non-empty string",
                invariant="EvidenceSnapshot.student_id.required",
            )
        if not isinstance(self.evidence_type, EvidenceType):
            raise EducationalInvariantViolation(
                "evidence_type must be an EvidenceType",
                invariant="EvidenceSnapshot.evidence_type.type",
            )
        if not isinstance(self.occurred_at, EvidenceTimestamp):
            raise EducationalInvariantViolation(
                "occurred_at must be an EvidenceTimestamp",
                invariant="EvidenceSnapshot.occurred_at.type",
            )
        if not isinstance(self.source, EvidenceSource):
            raise EducationalInvariantViolation(
                "source must be an EvidenceSource",
                invariant="EvidenceSnapshot.source.type",
            )
        if not isinstance(self.context, EvidenceContext):
            raise EducationalInvariantViolation(
                "context must be an EvidenceContext",
                invariant="EvidenceSnapshot.context.type",
            )
        if not isinstance(self.weight, EvidenceWeight):
            raise EducationalInvariantViolation(
                "weight must be an EvidenceWeight",
                invariant="EvidenceSnapshot.weight.type",
            )
        if not isinstance(self.metadata, EvidenceMetadata):
            raise EducationalInvariantViolation(
                "metadata must be EvidenceMetadata",
                invariant="EvidenceSnapshot.metadata.type",
            )
