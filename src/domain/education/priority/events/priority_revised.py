"""Domain event: educational priority was revised.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    PriorityRevised
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
    PriorityRevisionKind,
    PriorityScoreBand,
    UrgencyLevel,
)


@dataclass(frozen=True, slots=True)
class PriorityRevised(EducationalValueObject):
    """Immutable record that an EducationalPriority was revised."""

    priority_id: PriorityId
    student_id: str
    score_band: PriorityScoreBand
    urgency_level: UrgencyLevel
    impact_level: InstructionalImpactLevel
    revision_kind: PriorityRevisionKind

    def _validate(self) -> None:
        if not isinstance(self.priority_id, PriorityId):
            raise EducationalInvariantViolation(
                "priority_id must be a PriorityId",
                invariant="PriorityRevised.priority_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.score_band, PriorityScoreBand):
            raise EducationalInvariantViolation(
                "score_band must be a PriorityScoreBand",
                invariant="PriorityRevised.score_band.type",
            )
        if not isinstance(self.urgency_level, UrgencyLevel):
            raise EducationalInvariantViolation(
                "urgency_level must be an UrgencyLevel",
                invariant="PriorityRevised.urgency_level.type",
            )
        if not isinstance(self.impact_level, InstructionalImpactLevel):
            raise EducationalInvariantViolation(
                "impact_level must be an InstructionalImpactLevel",
                invariant="PriorityRevised.impact_level.type",
            )
        if not isinstance(self.revision_kind, PriorityRevisionKind):
            raise EducationalInvariantViolation(
                "revision_kind must be a PriorityRevisionKind",
                invariant="PriorityRevised.revision_kind.type",
            )
