"""Immutable plan describing a Learning Session to execute."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate


@dataclass(frozen=True)
class LearningSessionPlan:
    """Deterministic session plan produced by the Learning Session Planner.

    Attributes:
        session_id: Identity assigned to the planned session (may be provisional).
        journey_id: Parent Learning Journey identity.
        topic_id: Curriculum topic the session addresses.
        sequence_index: 0-based ordering within the journey.
        objective_ids: Ordered objective identities in educational focus.
        estimated_effort: Planned educational effort band.
        recommended_activities: Structural activity tags (not study content).
        previous_evidence_count: Count of prior evidence informing the plan.
        rationale_tags: Explainable planning rationale tags.
    """

    session_id: str
    journey_id: str
    topic_id: str
    sequence_index: int
    objective_ids: tuple[str, ...]
    estimated_effort: EffortEstimate
    recommended_activities: tuple[str, ...]
    previous_evidence_count: int
    rationale_tags: tuple[str, ...]
