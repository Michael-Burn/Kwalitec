"""Specification: evidence belongs to a given student.

Architecture Source
    STUDENT_DIGITAL_TWIN.md (Learning Evidence Model)
Concept
    EvidenceBelongsToStudentSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.educational_evidence.aggregates.educational_evidence import (
        EducationalEvidence,
    )


class EvidenceBelongsToStudentSpecification:
    """True when evidence is attributed to exactly the given student.

    Guards against evidence being attached to the wrong student's Twin —
    every evidence record must belong to one student.
    """

    def is_satisfied_by(self, evidence: EducationalEvidence, student_id: str) -> bool:
        if not isinstance(student_id, str) or not student_id.strip():
            return False
        return evidence.student_id == student_id

    def assert_satisfied_by(
        self, evidence: EducationalEvidence, student_id: str
    ) -> None:
        if not self.is_satisfied_by(evidence, student_id):
            raise EducationalInvariantViolation(
                "evidence does not belong to the given student",
                invariant="EvidenceBelongsToStudentSpecification.unsatisfied",
            )
