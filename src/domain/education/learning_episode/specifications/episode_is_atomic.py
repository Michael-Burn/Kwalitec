"""Specification: Learning Episode is educationally atomic.

Architecture Source
    EDUCATIONAL_ATOMICITY.md / LEARNING_EPISODE_INVARIANTS.md (E1, E11)
Concept
    EpisodeIsAtomicSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.learning_episode.policies.atomicity_policy import AtomicityPolicy

if TYPE_CHECKING:
    from domain.education.learning_episode.aggregates.learning_episode import (
        LearningEpisode,
    )
    from domain.education.learning_episode.entities.episode_goal import EpisodeGoal


class EpisodeIsAtomicSpecification:
    """True when the episode's teaching goal scopes one educational capability."""

    def is_satisfied_by(self, episode: LearningEpisode) -> bool:
        return AtomicityPolicy.is_atomic_statement(episode.teaching_goal.statement)

    def is_satisfied_by_goal(self, goal: EpisodeGoal) -> bool:
        return AtomicityPolicy.is_atomic_statement(goal.statement)

    def assert_satisfied_by(self, episode: LearningEpisode) -> None:
        AtomicityPolicy.assert_atomic_goal(episode.teaching_goal)
