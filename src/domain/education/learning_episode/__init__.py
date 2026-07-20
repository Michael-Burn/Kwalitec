"""Learning Episode bounded context — pure educational domain model.

IMP-003 implementation of the Learning Episode Architecture.

Pure Domain-Driven Design only: aggregates, entities, value objects, policies,
specifications, and lightweight domain events. No persistence, Flask,
SQLAlchemy, APIs, repositories, serialization, or DTOs.
"""

from __future__ import annotations

from domain.education.learning_episode.aggregates.learning_episode import (
    LearningEpisode,
)
from domain.education.learning_episode.entities.episode_goal import (
    EpisodeGoal,
    EpisodeGoalId,
)
from domain.education.learning_episode.entities.episode_outcome import (
    EpisodeOutcome,
    EpisodeOutcomeId,
)
from domain.education.learning_episode.entities.episode_reflection import (
    EpisodeReflection,
)
from domain.education.learning_episode.entities.episode_step import EpisodeStep
from domain.education.learning_episode.enums import (
    DurationBand,
    EpisodeOutcomeKind,
    EpisodeStatus,
    EpisodeStepStatus,
)
from domain.education.learning_episode.events.episode_completed import EpisodeCompleted
from domain.education.learning_episode.events.episode_started import EpisodeStarted
from domain.education.learning_episode.events.reflection_recorded import (
    ReflectionRecorded,
)
from domain.education.learning_episode.policies.atomicity_policy import AtomicityPolicy
from domain.education.learning_episode.policies.episode_validation_policy import (
    EpisodeValidationPolicy,
)
from domain.education.learning_episode.policies.sequencing_policy import (
    SequencingPolicy,
)
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
from domain.education.learning_episode.value_objects.episode_duration import (
    EpisodeDuration,
)
from domain.education.learning_episode.value_objects.episode_progress import (
    EpisodeProgress,
)
from domain.education.learning_episode.value_objects.episode_sequence import (
    EpisodeSequence,
    EpisodeStepId,
    EpisodeStepKind,
)

__all__ = [
    # Aggregate
    "LearningEpisode",
    # Entities
    "EpisodeGoal",
    "EpisodeGoalId",
    "EpisodeStep",
    "EpisodeReflection",
    "EpisodeOutcome",
    "EpisodeOutcomeId",
    # Value objects
    "EpisodeStepId",
    "EpisodeStepKind",
    "EpisodeSequence",
    "EpisodeDuration",
    "EpisodeProgress",
    # Enums
    "EpisodeStatus",
    "EpisodeStepStatus",
    "EpisodeOutcomeKind",
    "DurationBand",
    # Policies
    "EpisodeValidationPolicy",
    "AtomicityPolicy",
    "SequencingPolicy",
    # Specifications
    "EpisodeIsAtomicSpecification",
    "EpisodeCanCompleteSpecification",
    "EpisodeIsCompleteSpecification",
    "EpisodeSupportsReflectionSpecification",
    "EpisodeCanTransitionSpecification",
    # Events
    "EpisodeStarted",
    "EpisodeCompleted",
    "ReflectionRecorded",
]
