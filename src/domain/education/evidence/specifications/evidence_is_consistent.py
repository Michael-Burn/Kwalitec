"""Specification: EvidenceRecord is educationally consistent.

Architecture Source
    EDUCATIONAL_EVIDENCE_MODEL.md
Concept
    EvidenceIsConsistentSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.evidence.enums import EvidenceRecordStatus
from domain.education.evidence.policies.evidence_consistency_policy import (
    EvidenceConsistencyPolicy,
)
from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.evidence.aggregates.evidence_record import EvidenceRecord


class EvidenceIsConsistentSpecification:
    """True when source, items, strength, and confidence align educationally."""

    def is_satisfied_by(self, record: EvidenceRecord) -> bool:
        if record.status is EvidenceRecordStatus.INVALIDATED:
            return False
        try:
            EvidenceConsistencyPolicy.assert_consistent(
                record.source,
                record.items,
                record.strength,
                record.confidence,
            )
        except EducationalInvariantViolation:
            return False
        return True

    def assert_satisfied_by(self, record: EvidenceRecord) -> None:
        if not self.is_satisfied_by(record):
            raise EducationalInvariantViolation(
                "evidence record is not educationally consistent",
                invariant="EvidenceIsConsistentSpecification.unsatisfied",
            )
