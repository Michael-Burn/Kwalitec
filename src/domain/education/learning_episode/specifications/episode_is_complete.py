"""Specification: Learning Episode can complete / is complete.

Architecture Source
    LEARNING_EPISODE_LIFECYCLE.md / LEARNING_EPISODE_INVARIANTS.md (E3, E6)
Concept
    EpisodeCanCompleteSpecification / EpisodeIsCompleteSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.learning_episode.enums import EpisodeStatus
from domain.education.learning_episode.policies.sequencing_policy import (
    SequencingPolicy,
)

if TYPE_CHECKING:
    from domain.education.learning_episode.aggregates.learning_episode import (
        LearningEpisode,
    )


class EpisodeCanCompleteSpecification:
    """True when an in-progress episode may lawfully complete.

    Requires: IN_PROGRESS status, required steps done, reflection present,
    and at least one evidence item (E3, E6).
    """

    def is_satisfied_by(self, episode: LearningEpisode) -> bool:
        if episode.status is not EpisodeStatus.IN_PROGRESS:
            return False
        if not SequencingPolicy.required_steps_complete(episode.steps):
            return False
        if episode.reflection is None:
            return False
        if not episode.evidence_ids:
            return False
        return True

    def assert_satisfied_by(self, episode: LearningEpisode) -> None:
        if not self.is_satisfied_by(episode):
            raise EducationalInvariantViolation(
                "episode cannot complete under current educational state",
                invariant="EpisodeCanCompleteSpecification.unsatisfied",
            )


class EpisodeIsCompleteSpecification:
    """True when the episode has already reached COMPLETED status."""

    def is_satisfied_by(self, episode: LearningEpisode) -> bool:
        return episode.status is EpisodeStatus.COMPLETED and episode.outcome is not None

    def assert_satisfied_by(self, episode: LearningEpisode) -> None:
        if not self.is_satisfied_by(episode):
            raise EducationalInvariantViolation(
                "episode is not complete",
                invariant="EpisodeIsCompleteSpecification.unsatisfied",
            )


class EpisodeSupportsReflectionSpecification:
    """True when the episode can accept a reflection recording."""

    def is_satisfied_by(self, episode: LearningEpisode) -> bool:
        if episode.status is not EpisodeStatus.IN_PROGRESS:
            return False
        if episode.reflection is not None:
            return False
        return True

    def assert_satisfied_by(self, episode: LearningEpisode) -> None:
        if not self.is_satisfied_by(episode):
            raise EducationalInvariantViolation(
                "episode does not support reflection recording in current state",
                invariant="EpisodeSupportsReflectionSpecification.unsatisfied",
            )
