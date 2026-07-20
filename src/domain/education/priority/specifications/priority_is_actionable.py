"""Specification: EducationalPriority is instructional-actionable.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    PriorityIsActionableSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.enums import PriorityScoreBand, PriorityStatus
from domain.education.priority.policies.priority_validation_policy import (
    PriorityValidationPolicy,
)

if TYPE_CHECKING:
    from domain.education.priority.aggregates.educational_priority import (
        EducationalPriority,
    )


class PriorityIsActionableSpecification:
    """True when a priority is structurally ready to govern instruction.

    Actionability means the priority is ASSIGNED or REVISED (not only
    stabilised-as-historical), references diagnosis and hypothesis, possesses
    score/urgency/impact, has factors, and does not contradict constraints.
    It does **not** mean a teaching strategy or intention has been selected.
    """

    def is_satisfied_by(self, priority: EducationalPriority) -> bool:
        if priority.status not in {
            PriorityStatus.ASSIGNED,
            PriorityStatus.REVISED,
            PriorityStatus.STABILISED,
        }:
            return False
        if not priority.diagnosis_references:
            return False
        if not priority.hypothesis_references:
            return False
        if not priority.factors:
            return False
        if priority.score.band is PriorityScoreBand.NEGLIGIBLE:
            return False
        if not priority.urgency:
            return False
        if not priority.instructional_impact.statement:
            return False
        if not priority.scope.statement:
            return False
        if not priority.student_id:
            return False
        try:
            PriorityValidationPolicy.assert_constraints_satisfied(
                priority.constraints,
                priority.factors,
                priority.score,
                priority.urgency,
            )
        except EducationalInvariantViolation:
            return False
        return True

    def assert_satisfied_by(self, priority: EducationalPriority) -> None:
        if not self.is_satisfied_by(priority):
            raise EducationalInvariantViolation(
                "priority is not instructional-actionable",
                invariant="PriorityIsActionableSpecification.unsatisfied",
            )
