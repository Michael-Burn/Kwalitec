"""Domain event: educational evidence was recorded.

Architecture Source
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md /
    knowledge/version2/PRODUCTION_INTEGRATION.md
Concept
    EvidenceRecorded
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.evidence.enums import EvidenceStrengthLevel
from domain.education.evidence.value_objects.evidence_timestamp import EvidenceTimestamp
from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId


@dataclass(frozen=True, slots=True)
class EvidenceRecorded(EducationalValueObject):
    """Immutable record that an EvidenceRecord was created as observation."""

    evidence_id: EvidenceId
    student_id: str
    item_count: int
    strength_level: EvidenceStrengthLevel
    recorded_at: EvidenceTimestamp

    def _validate(self) -> None:
        if not isinstance(self.evidence_id, EvidenceId):
            raise EducationalInvariantViolation(
                "evidence_id must be an EvidenceId",
                invariant="EvidenceRecorded.evidence_id.type",
            )
        cleaned = (self.student_id or "").strip()
        if not cleaned:
            raise EducationalInvariantViolation(
                "student_id is required",
                invariant="EvidenceRecorded.student_id.required",
            )
        object.__setattr__(self, "student_id", cleaned)
        if not isinstance(self.item_count, int) or self.item_count < 1:
            raise EducationalInvariantViolation(
                "item_count must be a positive integer",
                invariant="EvidenceRecorded.item_count.positive",
            )
        if not isinstance(self.strength_level, EvidenceStrengthLevel):
            raise EducationalInvariantViolation(
                "strength_level must be an EvidenceStrengthLevel",
                invariant="EvidenceRecorded.strength_level.type",
            )
        if not isinstance(self.recorded_at, EvidenceTimestamp):
            raise EducationalInvariantViolation(
                "recorded_at must be an EvidenceTimestamp",
                invariant="EvidenceRecorded.recorded_at.type",
            )
