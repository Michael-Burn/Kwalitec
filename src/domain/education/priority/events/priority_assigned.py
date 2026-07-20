"""Domain event: educational priority was assigned.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    PriorityAssigned
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import PriorityId
from domain.education.priority.enums import (
    InstructionalImpactLevel,
    PriorityScoreBand,
    UrgencyLevel,
)


@dataclass(frozen=True, slots=True)
class PriorityAssigned(EducationalValueObject):
    """Immutable record that an EducationalPriority was assigned."""

    priority_id: PriorityId
    student_id: str
    score_band: PriorityScoreBand
    urgency_level: UrgencyLevel
    impact_level: InstructionalImpactLevel
    factor_count: int
    diagnosis_count: int
    hypothesis_count: int

    def _validate(self) -> None:
        if not isinstance(self.priority_id, PriorityId):
            raise EducationalInvariantViolation(
                "priority_id must be a PriorityId",
                invariant="PriorityAssigned.priority_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.score_band, PriorityScoreBand):
            raise EducationalInvariantViolation(
                "score_band must be a PriorityScoreBand",
                invariant="PriorityAssigned.score_band.type",
            )
        if not isinstance(self.urgency_level, UrgencyLevel):
            raise EducationalInvariantViolation(
                "urgency_level must be an UrgencyLevel",
                invariant="PriorityAssigned.urgency_level.type",
            )
        if not isinstance(self.impact_level, InstructionalImpactLevel):
            raise EducationalInvariantViolation(
                "impact_level must be an InstructionalImpactLevel",
                invariant="PriorityAssigned.impact_level.type",
            )
        if not isinstance(self.factor_count, int) or self.factor_count < 1:
            raise EducationalInvariantViolation(
                "factor_count must be a positive integer",
                invariant="PriorityAssigned.factor_count.positive",
            )
        if not isinstance(self.diagnosis_count, int) or self.diagnosis_count < 1:
            raise EducationalInvariantViolation(
                "diagnosis_count must be a positive integer",
                invariant="PriorityAssigned.diagnosis_count.positive",
            )
        if not isinstance(self.hypothesis_count, int) or self.hypothesis_count < 1:
            raise EducationalInvariantViolation(
                "hypothesis_count must be a positive integer",
                invariant="PriorityAssigned.hypothesis_count.positive",
            )
