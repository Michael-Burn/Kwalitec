"""Episode goal — exactly one deliberate educational improvement.

Architecture Source
    LEARNING_EPISODE_ARCHITECTURE.md / EDUCATIONAL_ATOMICITY.md
Concept
    Teaching Goal / Episode Goal
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class EpisodeGoalId(EducationalValueObject):
    """Identity of a teaching goal owned by a Learning Episode."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "EpisodeGoalId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class EpisodeGoal(EducationalEntity):
    """Single deliberate educational improvement sought by an episode.

    Exactly one EpisodeGoal per Learning Episode (Invariant E1). Names one
    primary learning dimension (Invariant E12). Never declares mastery.
    """

    goal_id: EpisodeGoalId
    statement: str
    educational_purpose: str
    primary_dimension: LearningDimension

    @property
    def entity_id(self) -> EpisodeGoalId:
        return self.goal_id

    def _validate(self) -> None:
        if not isinstance(self.goal_id, EpisodeGoalId):
            raise EducationalInvariantViolation(
                "goal_id must be an EpisodeGoalId",
                invariant="EpisodeGoal.goal_id.type",
            )
        object.__setattr__(
            self,
            "statement",
            require_non_empty_text(self.statement, "statement"),
        )
        object.__setattr__(
            self,
            "educational_purpose",
            require_non_empty_text(self.educational_purpose, "educational_purpose"),
        )
        if not isinstance(self.primary_dimension, LearningDimension):
            raise EducationalInvariantViolation(
                "primary_dimension must be a LearningDimension",
                invariant="EpisodeGoal.primary_dimension.type",
            )
        lowered = self.statement.casefold()
        if "master" in lowered:
            raise EducationalInvariantViolation(
                "teaching goal must not declare mastery as the episode outcome",
                invariant="EpisodeGoal.no_mastery",
            )
