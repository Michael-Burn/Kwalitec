"""Teaching plan application DTOs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TeachingPlanStepDTO:
    """One step in a teaching plan projection."""

    step_id: str
    kind: str
    sequence_index: int
    label: str
    required: bool
    status: str


@dataclass(frozen=True, slots=True)
class TeachingPlanDTO:
    """Application projection of a planned learning episode.

    Educational decisions (strategy, goal, steps) are supplied by domain;
    this DTO only projects persisted coordination state.
    """

    plan_id: str
    episode_id: str
    student_id: str
    teaching_goal_statement: str
    teaching_strategy_id: str
    primary_dimension: str
    status: str
    learning_objective_ids: tuple[str, ...]
    concept_ids: tuple[str, ...]
    steps: tuple[TeachingPlanStepDTO, ...]
