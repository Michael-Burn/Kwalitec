"""Specification: EducationalPriority ordering is stable.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    PriorityIsStableSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.enums import PriorityStatus
from domain.education.priority.policies.priority_calculation_policy import (
    PriorityCalculationPolicy,
)

if TYPE_CHECKING:
    from domain.education.priority.aggregates.educational_priority import (
        EducationalPriority,
    )


class PriorityIsStableSpecification:
    """True when priority ordering is locked and recalculation agrees.

    Stability means status is STABILISED and recomputing from current factors
    yields the same score band, urgency level, and impact level. Stable
    priorities remain recalculable — recalculation reopens ordering.
    """

    def is_satisfied_by(self, priority: EducationalPriority) -> bool:
        if priority.status is not PriorityStatus.STABILISED:
            return False
        if not priority.factors:
            return False
        try:
            score, urgency, impact = PriorityCalculationPolicy.calculate(
                priority.factors
            )
        except EducationalInvariantViolation:
            return False
        if score.band is not priority.score.band:
            return False
        if urgency.level is not priority.urgency.level:
            return False
        if impact.level is not priority.instructional_impact.level:
            return False
        return True

    def assert_satisfied_by(self, priority: EducationalPriority) -> None:
        if not self.is_satisfied_by(priority):
            raise EducationalInvariantViolation(
                "priority is not stable",
                invariant="PriorityIsStableSpecification.unsatisfied",
            )
