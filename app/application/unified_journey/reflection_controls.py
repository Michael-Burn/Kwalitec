"""Guided Reflection presentation controls (P2-MS005).

Start / Complete / Skip update Experience reflection state only.
No persistence. No evidence writes. No educational authority changes.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.unified_journey.day_experience import DayExperience
from app.application.unified_journey.events import (
    JourneyEvent,
    reflection_completed,
    reflection_skipped,
    reflection_started,
)
from app.application.unified_journey.reflection_states import (
    ReflectionControl,
    ReflectionState,
    resolve_reflection_control,
    resolve_reflection_state,
)
from app.application.unified_journey.session_outcome import SessionOutcome
from app.application.unified_journey.stages import JourneyStage


@dataclass(frozen=True)
class ReflectionControlResult:
    """Result of applying a presentation-only reflection control."""

    day_experience: DayExperience
    event: JourneyEvent | None = None
    applied: bool = False
    reason: str = ""


def apply_reflection_control(
    day: DayExperience,
    control: ReflectionControl | str,
) -> ReflectionControlResult:
    """Apply Start / Complete / Skip to DayExperience (pure, no side effects).

    Returns a new DayExperience and an optional JourneyEvent. Does not
    persist responses, write evidence, or call educational engines.
    """
    action = resolve_reflection_control(control)
    state = resolve_reflection_state(day.reflection_state)
    outcome = day.session_outcome

    if outcome is None or not outcome.reflection_available:
        return ReflectionControlResult(
            day_experience=day,
            event=None,
            applied=False,
            reason="reflection_not_available",
        )

    if action is ReflectionControl.START:
        if state is ReflectionState.IN_PROGRESS:
            return ReflectionControlResult(
                day_experience=day,
                event=reflection_started(
                    stage=JourneyStage.SESSION_REFLECTION,
                    message="Reflection already in progress",
                ),
                applied=True,
                reason="already_in_progress",
            )
        if state is not ReflectionState.AVAILABLE:
            return ReflectionControlResult(
                day_experience=day,
                event=None,
                applied=False,
                reason="start_requires_available",
            )
        return _transition(
            day,
            ReflectionState.IN_PROGRESS,
            event=reflection_started(
                stage=JourneyStage.SESSION_REFLECTION,
                message="Reflection started",
            ),
        )

    if action is ReflectionControl.COMPLETE:
        if state not in {
            ReflectionState.AVAILABLE,
            ReflectionState.IN_PROGRESS,
        }:
            return ReflectionControlResult(
                day_experience=day,
                event=None,
                applied=False,
                reason="complete_requires_active_reflection",
            )
        return _transition(
            day,
            ReflectionState.COMPLETED,
            event=reflection_completed(
                stage=JourneyStage.SESSION_REFLECTION,
                message="Reflection completed",
            ),
        )

    if action is ReflectionControl.SKIP:
        if state not in {
            ReflectionState.AVAILABLE,
            ReflectionState.IN_PROGRESS,
        }:
            return ReflectionControlResult(
                day_experience=day,
                event=None,
                applied=False,
                reason="skip_requires_active_reflection",
            )
        return _transition(
            day,
            ReflectionState.SKIPPED,
            event=reflection_skipped(
                stage=JourneyStage.SESSION_REFLECTION,
                message="Reflection skipped",
            ),
        )

    return ReflectionControlResult(
        day_experience=day,
        event=None,
        applied=False,
        reason="unknown_control",
    )


def _transition(
    day: DayExperience,
    state: ReflectionState,
    *,
    event: JourneyEvent,
) -> ReflectionControlResult:
    outcome: SessionOutcome | None = day.session_outcome
    updated = DayExperience(
        daily_mission=day.daily_mission,
        timeline=day.timeline,
        current_phase=day.current_phase,
        session_status=day.session_status,
        reflection_available=day.reflection_available,
        upcoming_transition=_upcoming_for_reflection(state),
        progress_summary=day.progress_summary,
        session_outcome=outcome,
        reflection_state=state,
        metadata=day.metadata
        + (
            ("reflection_state", state.value),
            ("via", "reflection_controls"),
        ),
    )
    return ReflectionControlResult(
        day_experience=updated,
        event=event,
        applied=True,
        reason="",
    )


def _upcoming_for_reflection(state: ReflectionState) -> str:
    if state is ReflectionState.AVAILABLE:
        return "Take a brief moment to reflect"
    if state is ReflectionState.IN_PROGRESS:
        return "Finish or skip when ready"
    return "Today's learning day is complete"
