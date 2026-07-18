"""Stateless completion eligibility rules for Learning Journeys.

Completion never follows solely from session completion, time spent, or
percentage of sessions finished. Educational criteria from the domain
progress service are required.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.services.journey_progress_service import (
    JourneyProgressService,
)
from app.domain.learning_journey.value_objects.journey_state import JourneyState


@dataclass(frozen=True)
class CompletionEvaluation:
    """Result of evaluating completion eligibility."""

    eligible_for_ready: bool
    eligible_for_confirm: bool
    meets_completion_criteria: bool
    blockers: tuple[str, ...]
    reason: str


class CompletionPolicy:
    """Educational completion rules (stateless)."""

    MIN_COMPLETED_SESSIONS = JourneyProgressService.DEFAULT_MIN_COMPLETED_SESSIONS
    REQUIRE_REFLECTIONS = (
        JourneyProgressService.DEFAULT_REQUIRE_REFLECTIONS_FOR_COMPLETED
    )

    @staticmethod
    def evaluate(
        journey: LearningJourney,
        *,
        min_completed_sessions: int = MIN_COMPLETED_SESSIONS,
        require_reflections: bool = REQUIRE_REFLECTIONS,
    ) -> CompletionEvaluation:
        """Evaluate whether the journey may enter / confirm completion.

        Args:
            journey: Aggregate under evaluation.
            min_completed_sessions: Structural session floor (not a %).
            require_reflections: Require CAPTURED reflections on completed
                sessions.

        Returns:
            CompletionEvaluation with blockers and eligibility flags.
        """
        blockers: list[str] = []

        if journey.state == JourneyState.COMPLETED:
            return CompletionEvaluation(
                eligible_for_ready=False,
                eligible_for_confirm=False,
                meets_completion_criteria=True,
                blockers=("journey_already_completed",),
                reason="Journey is already Topic Complete",
            )

        if journey.state in {
            JourneyState.ABANDONED,
            JourneyState.ARCHIVED,
            JourneyState.DEFERRED,
        }:
            return CompletionEvaluation(
                eligible_for_ready=False,
                eligible_for_confirm=False,
                meets_completion_criteria=False,
                blockers=(f"journey_state_{journey.state.value}",),
                reason=f"Journey state {journey.state.value} cannot complete",
            )

        progress = JourneyProgressService.calculate(
            journey,
            min_completed_sessions=min_completed_sessions,
            require_reflections=require_reflections,
        )

        if progress.sessions_completed < min_completed_sessions:
            blockers.append("insufficient_completed_sessions")
        if (
            progress.objectives_total > 0
            and progress.objectives_addressed < progress.objectives_total
        ):
            blockers.append("objectives_not_fully_addressed")

        from app.application.learning_journey.policies.progression_policy import (
            ProgressionPolicy,
        )

        if require_reflections and ProgressionPolicy.pending_reflection_sessions(
            journey
        ):
            blockers.append("pending_reflections")

        meets = progress.meets_completion_criteria

        # Session-complete alone is never enough — enforce multi-session floor.
        if progress.sessions_completed < min_completed_sessions:
            meets = False
        if progress.sessions_completed == 1:
            blockers.append("single_session_insufficient")
            meets = False

        if not meets and not blockers:
            blockers.append("completion_criteria_not_met")

        if journey.state == JourneyState.PAUSED:
            blockers.append("journey_paused")

        # Confirm path: state already READY and criteria still hold.
        if journey.state == JourneyState.READY_FOR_COMPLETION and meets:
            return CompletionEvaluation(
                eligible_for_ready=False,
                eligible_for_confirm=True,
                meets_completion_criteria=True,
                blockers=(),
                reason="Ready for Topic Complete confirmation",
            )

        eligible_for_ready = meets and journey.state in {
            JourneyState.ACTIVE,
            JourneyState.RESUMED,
        }
        eligible_for_confirm = False

        reason = (
            "Educational completion criteria are met"
            if meets and not blockers
            else "Educational completion criteria are not met"
        )

        return CompletionEvaluation(
            eligible_for_ready=eligible_for_ready,
            eligible_for_confirm=eligible_for_confirm,
            meets_completion_criteria=meets,
            blockers=tuple(dict.fromkeys(blockers)),
            reason=reason,
        )

    @staticmethod
    def rejects_session_only_completion(journey: LearningJourney) -> bool:
        """True when completion would rest only on session finish count.

        Educational guard: one completed session never warrants Topic Complete.
        """
        completed = sum(
            1 for s in journey.sessions if s.state.value == "completed"
        )
        return completed < CompletionPolicy.MIN_COMPLETED_SESSIONS

    @staticmethod
    def rejects_time_or_percentage_alone() -> bool:
        """Time spent and percentage metrics never authorize completion."""
        return True
