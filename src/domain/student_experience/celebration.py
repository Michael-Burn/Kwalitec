"""Celebration — presentation progress celebration.

Architecture Source
    EXP-001 Student Experience Engine
Concept
    Celebration
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.student_experience.enums import CelebrationKind
from domain.student_experience.ids import AchievementId, CelebrationId


@dataclass(frozen=True, slots=True)
class Celebration(EducationalValueObject):
    """Immutable presentation celebration derived from experience recognition.

    Celebrations are engagement chrome. They must not invent educational
    readiness, mastery, or recommendation changes.
    """

    celebration_id: CelebrationId
    kind: CelebrationKind
    headline: str
    detail: str
    sequence: int
    related_achievement_id: AchievementId | None = None

    def _validate(self) -> None:
        if not isinstance(self.celebration_id, CelebrationId):
            raise EducationalInvariantViolation(
                "celebration_id must be a CelebrationId",
                invariant="Celebration.celebration_id.type",
            )
        if not isinstance(self.kind, CelebrationKind):
            raise EducationalInvariantViolation(
                "kind must be a CelebrationKind",
                invariant="Celebration.kind.type",
            )
        object.__setattr__(
            self,
            "headline",
            require_non_empty_text(self.headline, "headline"),
        )
        object.__setattr__(
            self,
            "detail",
            require_non_empty_text(self.detail, "detail"),
        )
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise EducationalInvariantViolation(
                "sequence must be an integer",
                invariant="Celebration.sequence.type",
            )
        if self.sequence < 1:
            raise EducationalInvariantViolation(
                "sequence must be a positive integer",
                invariant="Celebration.sequence.positive",
            )
        if self.related_achievement_id is not None and not isinstance(
            self.related_achievement_id, AchievementId
        ):
            raise EducationalInvariantViolation(
                "related_achievement_id must be an AchievementId when provided",
                invariant="Celebration.related_achievement_id.type",
            )
        if (
            self.kind is CelebrationKind.ACHIEVEMENT
            and self.related_achievement_id is None
        ):
            raise EducationalInvariantViolation(
                "achievement celebrations require related_achievement_id",
                invariant="Celebration.achievement.requires_related",
            )
