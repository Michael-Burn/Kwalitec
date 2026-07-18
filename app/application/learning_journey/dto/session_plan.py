"""Immutable plan describing the next (or current) learning session."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_journey.entities.learning_objective import LearningObjective
from app.domain.learning_journey.value_objects.effort_estimate import EffortEstimate


@dataclass(frozen=True)
class SessionPlan:
    """Deterministic session plan produced by the Learning Journey Engine.

    Attributes:
        session_number: 1-based educational session ordinal (sequence + 1).
        sequence_index: 0-based domain sequence index.
        session_id: Existing session identity when selecting an extant session.
        objective: Primary objective for the session, if known.
        expected_effort: Planned educational effort band.
        recommended_activities: Short structural activity tags (not content).
        is_existing_session: True when plan targets an existing session.
    """

    session_number: int
    sequence_index: int
    session_id: str | None
    objective: LearningObjective | None
    expected_effort: EffortEstimate
    recommended_activities: tuple[str, ...]
    is_existing_session: bool = True
