"""Achievement — presentation milestone recognition.

Architecture Source
    EXP-001 Student Experience Engine
Concept
    Achievement
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.student_experience.enums import AchievementKind, MilestoneKind
from domain.student_experience.ids import AchievementId


@dataclass(frozen=True, slots=True)
class Achievement(EducationalValueObject):
    """Immutable presentation achievement recognised from Educational OS outputs.

    Achievements celebrate continuity and progress signals already present in
    educational projections. They never declare mastery or change educational
    decisions.
    """

    achievement_id: AchievementId
    kind: AchievementKind
    milestone: MilestoneKind
    title: str
    message: str
    sequence: int

    def _validate(self) -> None:
        if not isinstance(self.achievement_id, AchievementId):
            raise EducationalInvariantViolation(
                "achievement_id must be an AchievementId",
                invariant="Achievement.achievement_id.type",
            )
        if not isinstance(self.kind, AchievementKind):
            raise EducationalInvariantViolation(
                "kind must be an AchievementKind",
                invariant="Achievement.kind.type",
            )
        if not isinstance(self.milestone, MilestoneKind):
            raise EducationalInvariantViolation(
                "milestone must be a MilestoneKind",
                invariant="Achievement.milestone.type",
            )
        object.__setattr__(
            self,
            "title",
            require_non_empty_text(self.title, "title"),
        )
        object.__setattr__(
            self,
            "message",
            require_non_empty_text(self.message, "message"),
        )
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise EducationalInvariantViolation(
                "sequence must be an integer",
                invariant="Achievement.sequence.type",
            )
        if self.sequence < 1:
            raise EducationalInvariantViolation(
                "sequence must be a positive integer",
                invariant="Achievement.sequence.positive",
            )
