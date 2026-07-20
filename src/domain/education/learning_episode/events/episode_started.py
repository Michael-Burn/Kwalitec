"""Domain event: a Learning Episode started.

Architecture Source
    LEARNING_EPISODE_LIFECYCLE.md
Concept
    EpisodeStarted
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.learning_episode.entities.episode_goal import EpisodeGoalId
from domain.education.learning_episode.value_objects.episode_sequence import (
    EpisodeStepId,
)


@dataclass(frozen=True, slots=True)
class EpisodeStarted(EducationalValueObject):
    """Immutable record that a Learning Episode entered IN_PROGRESS."""

    episode_id: LearningEpisodeId
    teaching_goal_id: EpisodeGoalId
    first_step_id: EpisodeStepId

    def _validate(self) -> None:
        if not isinstance(self.episode_id, LearningEpisodeId):
            raise EducationalInvariantViolation(
                "episode_id must be a LearningEpisodeId",
                invariant="EpisodeStarted.episode_id.type",
            )
        if not isinstance(self.teaching_goal_id, EpisodeGoalId):
            raise EducationalInvariantViolation(
                "teaching_goal_id must be an EpisodeGoalId",
                invariant="EpisodeStarted.teaching_goal_id.type",
            )
        if not isinstance(self.first_step_id, EpisodeStepId):
            raise EducationalInvariantViolation(
                "first_step_id must be an EpisodeStepId",
                invariant="EpisodeStarted.first_step_id.type",
            )
