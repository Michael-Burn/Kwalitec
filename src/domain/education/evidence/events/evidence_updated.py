"""Domain event: educational evidence was updated.

Architecture Source
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md
Concept
    EvidenceUpdated
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.evidence.enums import EvidenceRecordStatus
from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId


@dataclass(frozen=True, slots=True)
class EvidenceUpdated(EducationalValueObject):
    """Immutable record that an EvidenceRecord observationally changed.

    Updates cover amend, invalidate, merge absorption, and context attachment.
    Events themselves never mutate.
    """

    evidence_id: EvidenceId
    student_id: str
    status: EvidenceRecordStatus
    change_kind: str

    def _validate(self) -> None:
        if not isinstance(self.evidence_id, EvidenceId):
            raise EducationalInvariantViolation(
                "evidence_id must be an EvidenceId",
                invariant="EvidenceUpdated.evidence_id.type",
            )
        cleaned = (self.student_id or "").strip()
        if not cleaned:
            raise EducationalInvariantViolation(
                "student_id is required",
                invariant="EvidenceUpdated.student_id.required",
            )
        object.__setattr__(self, "student_id", cleaned)
        if not isinstance(self.status, EvidenceRecordStatus):
            raise EducationalInvariantViolation(
                "status must be an EvidenceRecordStatus",
                invariant="EvidenceUpdated.status.type",
            )
        object.__setattr__(
            self,
            "change_kind",
            require_non_empty_text(self.change_kind, "change_kind"),
        )
