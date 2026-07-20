"""Learning session / episode application DTOs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LearningEpisodeDTO:
    """Projection of a LearningEpisode aggregate."""

    episode_id: str
    student_id: str
    status: str
    teaching_goal_statement: str
    teaching_strategy_id: str
    primary_dimension: str
    step_count: int
    evidence_count: int
    has_reflection: bool
    outcome_kind: str | None


@dataclass(frozen=True, slots=True)
class LearningSessionDTO:
    """Projection returned when a learning session is started."""

    episode_id: str
    student_id: str
    status: str
    first_active_step_id: str | None
