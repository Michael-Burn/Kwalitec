"""Immutable result of educational progression coordination."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_objective import LearningObjective
from app.domain.learning_journey.value_objects.journey_state import JourneyState


@dataclass(frozen=True)
class ProgressionResult:
    """Outcome of applying educational progression to a journey.

    Attributes:
        journey: Updated Learning Journey aggregate (caller may persist).
        previous_state: Journey state before progression.
        current_state: Journey state after progression.
        unlocked_objectives: Objectives newly addressed by this step.
        next_actions: Structural next-action tags for consumers.
        state_changed: Whether journey lifecycle state changed.
        progress_recalculated: Whether JourneyProgress was refreshed.
        meets_completion_criteria: Post-progression completion eligibility.
    """

    journey: LearningJourney
    previous_state: JourneyState
    current_state: JourneyState
    unlocked_objectives: tuple[LearningObjective, ...]
    next_actions: tuple[str, ...]
    state_changed: bool
    progress_recalculated: bool
    meets_completion_criteria: bool
