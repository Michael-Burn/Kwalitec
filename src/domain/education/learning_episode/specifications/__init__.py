"""Learning Episode specifications."""

from __future__ import annotations

from domain.education.learning_episode.specifications.episode_can_transition import (
    EpisodeCanTransitionSpecification,
)
from domain.education.learning_episode.specifications.episode_is_atomic import (
    EpisodeIsAtomicSpecification,
)
from domain.education.learning_episode.specifications.episode_is_complete import (
    EpisodeCanCompleteSpecification,
    EpisodeIsCompleteSpecification,
    EpisodeSupportsReflectionSpecification,
)

__all__ = [
    "EpisodeIsAtomicSpecification",
    "EpisodeCanCompleteSpecification",
    "EpisodeIsCompleteSpecification",
    "EpisodeSupportsReflectionSpecification",
    "EpisodeCanTransitionSpecification",
]
