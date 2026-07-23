"""Specification: Student Educational State is internally consistent.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    StudentEducationalStateIsConsistentSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.student_state.aggregates.student_educational_state import (
        StudentEducationalState,
    )


class StudentEducationalStateIsConsistentSpecification:
    """True when the aggregate's collections and summaries remain coherent.

    Consistency is structural integrity — not educational correctness of
    mastery, confidence, or health judgements.
    """

    def is_satisfied_by(self, state: StudentEducationalState) -> bool:
        if not state.student_id:
            return False
        if state.mastery_summary is None or state.confidence_summary is None:
            return False
        if state.educational_health is None:
            return False
        subject_ids = [s.subject_id.value for s in state.subject_states]
        if len(subject_ids) != len(set(subject_ids)):
            return False
        competency_ids = [c.competency_id.value for c in state.competency_states]
        if len(competency_ids) != len(set(competency_ids)):
            return False
        return True

    def assert_satisfied_by(self, state: StudentEducationalState) -> None:
        if not self.is_satisfied_by(state):
            raise EducationalInvariantViolation(
                "student educational state is not consistent",
                invariant="StudentEducationalStateIsConsistentSpecification.unsatisfied",
            )
