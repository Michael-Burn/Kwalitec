"""Guided session presentation controls (P2-MS004 / P2-MS005).

Start / Resume / Finish update Experience phase state only.
No persistence. No evidence writes. No educational authority changes.
Never triggers Runtime A or Strategy recalculations.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.unified_journey.day_experience import (
    DayExperience,
    progress_summary_for,
    upcoming_transition_for_phase,
)
from app.application.unified_journey.events import (
    JourneyEvent,
    session_completed,
    session_resumed,
    session_started,
    wrap_up_started,
)
from app.application.unified_journey.reflection_states import ReflectionState
from app.application.unified_journey.session_phases import (
    SessionControl,
    SessionPhase,
    resolve_session_control,
    session_status_label,
)
from app.application.unified_journey.stages import JourneyStage
from app.application.unified_journey.timeline import timeline_with_reflection


@dataclass(frozen=True)
class SessionControlResult:
    """Result of applying a presentation-only session control."""

    day_experience: DayExperience
    event: JourneyEvent | None = None
    applied: bool = False
    reason: str = ""


def apply_session_control(
    day: DayExperience,
    control: SessionControl | str,
) -> SessionControlResult:
    """Apply Start / Resume / Finish to DayExperience (pure, no side effects).

    Returns a new DayExperience and an optional JourneyEvent. Does not
    mutate Programme I outputs, write evidence, or call educational engines.
    """
    action = resolve_session_control(control)
    phase = day.current_phase

    if action is SessionControl.START:
        if phase is not SessionPhase.READY:
            return SessionControlResult(
                day_experience=day,
                event=None,
                applied=False,
                reason="start_requires_ready",
            )
        return _transition(
            day,
            SessionPhase.STUDYING,
            event=session_started(
                stage=JourneyStage.STUDY_SESSION,
                message="Study session started",
            ),
        )

    if action is SessionControl.RESUME:
        if phase is SessionPhase.STUDYING:
            # Already studying — emit resume for presentation bookkeeping.
            return SessionControlResult(
                day_experience=day,
                event=session_resumed(
                    stage=JourneyStage.STUDY_SESSION,
                    message="Study session resumed",
                ),
                applied=True,
                reason="already_studying",
            )
        if phase not in {SessionPhase.READY, SessionPhase.WRAPPING_UP}:
            return SessionControlResult(
                day_experience=day,
                event=None,
                applied=False,
                reason="resume_not_available",
            )
        return _transition(
            day,
            SessionPhase.STUDYING,
            event=session_resumed(
                stage=JourneyStage.STUDY_SESSION,
                message="Study session resumed",
            ),
        )

    if action is SessionControl.FINISH:
        if phase is SessionPhase.STUDYING:
            return _transition(
                day,
                SessionPhase.WRAPPING_UP,
                event=wrap_up_started(
                    stage=JourneyStage.STUDY_SESSION,
                    message="Wrapping up study session",
                ),
            )
        if phase is SessionPhase.WRAPPING_UP:
            return _transition(
                day,
                SessionPhase.COMPLETE,
                event=session_completed(
                    stage=JourneyStage.STUDY_SESSION,
                    message="Study session completed",
                ),
                unlock_reflection=True,
            )
        return SessionControlResult(
            day_experience=day,
            event=None,
            applied=False,
            reason="finish_requires_active_session",
        )

    return SessionControlResult(
        day_experience=day,
        event=None,
        applied=False,
        reason="unknown_control",
    )


def _transition(
    day: DayExperience,
    phase: SessionPhase,
    *,
    event: JourneyEvent,
    unlock_reflection: bool = False,
) -> SessionControlResult:
    mission = day.daily_mission
    post_session = phase in {SessionPhase.WRAPPING_UP, SessionPhase.COMPLETE}
    reflection_state = None
    session_outcome = None
    timeline = day.timeline
    upcoming = upcoming_transition_for_phase(phase)

    if post_session:
        from app.application.unified_journey.session_outcome_assembler import (
            SessionOutcomeAssembler,
        )

        shell = DayExperience(
            daily_mission=mission,
            timeline=day.timeline,
            current_phase=phase,
            session_status=session_status_label(phase),
            reflection_available=True,
            upcoming_transition=upcoming,
            progress_summary=progress_summary_for(mission=mission, phase=phase),
        )
        session_outcome = SessionOutcomeAssembler().assemble(shell)

    if unlock_reflection and session_outcome is not None:
        reflection_state = ReflectionState.AVAILABLE
        upcoming = "Take a brief moment to reflect"
        timeline = timeline_with_reflection(mission)

    updated = DayExperience(
        daily_mission=mission,
        timeline=timeline,
        current_phase=phase,
        session_status=session_status_label(phase),
        reflection_available=post_session,
        upcoming_transition=upcoming,
        progress_summary=progress_summary_for(mission=mission, phase=phase),
        session_outcome=session_outcome,
        reflection_state=reflection_state,
        metadata=day.metadata
        + (
            ("phase", phase.value),
            ("via", "session_controls"),
        ),
    )
    return SessionControlResult(
        day_experience=updated,
        event=event,
        applied=True,
        reason="",
    )
