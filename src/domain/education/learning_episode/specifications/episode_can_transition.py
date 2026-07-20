"""Specification: Learning Episode may perform a lifecycle transition.

Architecture Source
    LEARNING_EPISODE_LIFECYCLE.md
Concept
    EpisodeCanTransitionSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.learning_episode.enums import EpisodeStatus

if TYPE_CHECKING:
    from domain.education.learning_episode.aggregates.learning_episode import (
        LearningEpisode,
    )


class EpisodeCanTransitionSpecification:
    """Judges whether a named lifecycle transition is educationally lawful."""

    def can_start(self, episode: LearningEpisode) -> bool:
        return episode.status is EpisodeStatus.PLANNED

    def can_advance_step(self, episode: LearningEpisode) -> bool:
        return episode.status is EpisodeStatus.IN_PROGRESS

    def can_attach_evidence(self, episode: LearningEpisode) -> bool:
        return episode.status is EpisodeStatus.IN_PROGRESS

    def can_record_reflection(self, episode: LearningEpisode) -> bool:
        return (
            episode.status is EpisodeStatus.IN_PROGRESS
            and episode.reflection is None
        )

    def can_complete(self, episode: LearningEpisode) -> bool:
        from domain.education.learning_episode.specifications import (
            episode_is_complete as complete_specs,
        )

        return complete_specs.EpisodeCanCompleteSpecification().is_satisfied_by(
            episode
        )

    def can_interrupt(self, episode: LearningEpisode) -> bool:
        return episode.status in {
            EpisodeStatus.PLANNED,
            EpisodeStatus.IN_PROGRESS,
        }

    def is_satisfied_by(self, episode: LearningEpisode, transition: str) -> bool:
        mapping = {
            "start": self.can_start,
            "advance_step": self.can_advance_step,
            "attach_evidence": self.can_attach_evidence,
            "record_reflection": self.can_record_reflection,
            "complete": self.can_complete,
            "interrupt": self.can_interrupt,
        }
        checker = mapping.get(transition)
        if checker is None:
            raise EducationalInvariantViolation(
                f"unknown episode transition: {transition}",
                invariant="EpisodeCanTransitionSpecification.unknown",
            )
        return checker(episode)

    def assert_satisfied_by(self, episode: LearningEpisode, transition: str) -> None:
        if not self.is_satisfied_by(episode, transition):
            raise EducationalInvariantViolation(
                f"episode cannot transition via {transition}",
                invariant=f"EpisodeCanTransitionSpecification.{transition}",
            )
