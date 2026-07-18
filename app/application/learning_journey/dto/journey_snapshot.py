"""Immutable snapshot of a Learning Journey for consumers outside the engine."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_journey.entities.journey_recommendation import (
    JourneyRecommendation,
)
from app.domain.learning_journey.entities.learning_objective import LearningObjective
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.completion_status import CompletionStatus
from app.domain.learning_journey.value_objects.journey_state import JourneyState


@dataclass(frozen=True)
class EvidenceSummary:
    """Compact evidence posture for a journey snapshot."""

    evidence_count: int
    evidence_confidence: str
    sessions_with_evidence: int


@dataclass(frozen=True)
class ReflectionSummary:
    """Compact reflection posture for a journey snapshot."""

    reflections_captured: int
    reflections_pending: int
    completed_sessions_owing_reflection: int


@dataclass(frozen=True)
class JourneySnapshot:
    """Read-only educational snapshot of a Learning Journey.

    Attributes:
        journey_id: Aggregate identity.
        learner_id: Owning learner.
        topic_id: Curriculum topic.
        curriculum_id: Curriculum identity.
        state: Current journey lifecycle posture.
        completion_status: Derived completion posture.
        meets_completion_criteria: Whether READY_FOR_COMPLETION is warranted.
        current_objective: Objective currently in focus, if any.
        sessions: Ordered sessions.
        evidence_summary: Aggregated evidence posture.
        reflection_summary: Aggregated reflection posture.
        recommendation: Latest advisory recommendation, if any.
        objectives_total: Bound objectives count.
        objectives_addressed: Objectives with session or evidence contact.
        sessions_completed: Completed session count.
    """

    journey_id: str
    learner_id: str
    topic_id: str
    curriculum_id: str
    state: JourneyState
    completion_status: CompletionStatus
    meets_completion_criteria: bool
    current_objective: LearningObjective | None
    sessions: tuple[LearningSession, ...]
    evidence_summary: EvidenceSummary
    reflection_summary: ReflectionSummary
    recommendation: JourneyRecommendation | None
    objectives_total: int
    objectives_addressed: int
    sessions_completed: int
