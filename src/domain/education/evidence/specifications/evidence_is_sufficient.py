"""Specification: EvidenceRecord is educationally sufficient.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md /
    CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md
Concept
    EvidenceIsSufficientSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.evidence.enums import EvidenceRecordStatus
from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.evidence.aggregates.evidence_record import EvidenceRecord


class EvidenceIsSufficientSpecification:
    """True when an EvidenceRecord is structurally complete as observation.

    Sufficiency means the record is ACTIVE and possesses required observational
    constituents (items, source, context, confidence, strength, timestamp,
    student). It does not mean the evidence is strong enough to diagnose,
    recommend, or prioritise.
    """

    def is_satisfied_by(self, record: EvidenceRecord) -> bool:
        if record.status is not EvidenceRecordStatus.ACTIVE:
            return False
        if not record.items:
            return False
        if record.source is None:
            return False
        if record.context is None:
            return False
        if record.confidence is None:
            return False
        if record.strength is None:
            return False
        if record.timestamp is None:
            return False
        if not record.student_id:
            return False
        return True

    def assert_satisfied_by(self, record: EvidenceRecord) -> None:
        if not self.is_satisfied_by(record):
            raise EducationalInvariantViolation(
                "evidence record is not educationally sufficient",
                invariant="EvidenceIsSufficientSpecification.unsatisfied",
            )
