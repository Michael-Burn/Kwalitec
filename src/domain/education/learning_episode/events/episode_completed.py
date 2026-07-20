"""Domain event: a Learning Episode completed.

Architecture Source
    LEARNING_EPISODE_LIFECYCLE.md
Concept
    EpisodeCompleted
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import LearningEpisodeId
from domain.education.learning_episode.entities.episode_outcome import EpisodeOutcomeId
from domain.education.learning_episode.enums import EpisodeOutcomeKind


@dataclass(frozen=True, slots=True)
class EpisodeCompleted(EducationalValueObject):
    """Immutable record that a Learning Episode reached COMPLETED."""

    episode_id: LearningEpisodeId
    outcome_id: EpisodeOutcomeId
    outcome_kind: EpisodeOutcomeKind

    def _validate(self) -> None:
        if not isinstance(self.episode_id, LearningEpisodeId):
            raise EducationalInvariantViolation(
                "episode_id must be a LearningEpisodeId",
                invariant="EpisodeCompleted.episode_id.type",
            )
        if not isinstance(self.outcome_id, EpisodeOutcomeId):
            raise EducationalInvariantViolation(
                "outcome_id must be an EpisodeOutcomeId",
                invariant="EpisodeCompleted.outcome_id.type",
            )
        if not isinstance(self.outcome_kind, EpisodeOutcomeKind):
            raise EducationalInvariantViolation(
                "outcome_kind must be an EpisodeOutcomeKind",
                invariant="EpisodeCompleted.outcome_kind.type",
            )
        if self.outcome_kind is EpisodeOutcomeKind.INTERRUPTED:
            raise EducationalInvariantViolation(
                "EpisodeCompleted cannot carry an INTERRUPTED outcome",
                invariant="EpisodeCompleted.outcome_kind.not_interrupted",
            )
