"""GenerateTeachingPlan command."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TeachingPlanStepSpec:
    """Application input describing one planned episode step.

    Step kinds and ordering are educational decisions made upstream; application
    only assembles the domain aggregate and persists it.
    """

    step_id: str
    kind: str
    sequence_index: int
    label: str
    required: bool = True


@dataclass(frozen=True, slots=True)
class GenerateTeachingPlan:
    """Generate (persist) a teaching plan as a planned Learning Episode.

    Strategy, goal, objectives, and steps are domain decisions supplied as
    inputs. Application validates concept existence via ports, constructs the
    episode aggregate, commits, and returns a TeachingPlanDTO.
    """

    plan_id: str
    episode_id: str
    student_id: str
    goal_id: str
    goal_statement: str
    goal_purpose: str
    primary_dimension: str
    teaching_strategy_id: str
    learning_objective_ids: tuple[str, ...]
    steps: tuple[TeachingPlanStepSpec, ...]
    concept_ids: tuple[str, ...] = ()
    selection_rationale: str | None = None
