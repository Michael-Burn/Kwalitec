"""SessionOutcomeAssembler — DayExperience → SessionOutcome (P2-MS005).

Builds the canonical post-session presentation object. No educational
metrics, mastery values, or Programme I mutations.
"""

from __future__ import annotations

from app.application.unified_journey.contracts import COMPLETION_COMPLETE
from app.application.unified_journey.day_experience import DayExperience
from app.application.unified_journey.session_outcome import (
    SessionOutcome,
    completion_status_for_outcome,
    empty_session_outcome,
)
from app.application.unified_journey.session_phases import SessionPhase


class SessionOutcomeAssembler:
    """Assemble immutable SessionOutcome after a guided study session.

    Responsibilities:
    - Surface mission title + presentation completion status
    - Set reflection_available when post-session
    - Prepare concise summary / next transition / upcoming action

    Non-responsibilities:
    - Educational metrics / mastery
    - Persistence / evidence writes
    - Engine calls
    """

    def assemble(self, day: DayExperience | None) -> SessionOutcome:
        """Derive SessionOutcome from DayExperience when post-session."""
        if day is None:
            return empty_session_outcome()

        phase = day.current_phase
        if phase not in {SessionPhase.WRAPPING_UP, SessionPhase.COMPLETE}:
            return empty_session_outcome()

        mission = day.daily_mission
        title = (mission.title or "").strip() or "Today's Mission"
        wrapping = phase is SessionPhase.WRAPPING_UP
        completion = completion_status_for_outcome(wrapping_up=wrapping)
        if day.daily_mission.is_completed:
            completion = COMPLETION_COMPLETE

        return SessionOutcome(
            mission_title=title,
            completion_status=completion,
            reflection_available=True,
            summary_message=_summary_message(title=title, wrapping_up=wrapping),
            next_transition=_next_transition(wrapping_up=wrapping),
            upcoming_action=_upcoming_action(wrapping_up=wrapping),
            metadata=day.metadata
            + (
                ("phase", phase.value),
                ("via", "session_outcome_assembler"),
            ),
        )

    def assemble_placeholder(self) -> SessionOutcome:
        """Explicit placeholder SessionOutcome."""
        return empty_session_outcome()


def _summary_message(*, title: str, wrapping_up: bool) -> str:
    if wrapping_up:
        return f"Wrapping up {title}"
    return f"You finished {title}"


def _next_transition(*, wrapping_up: bool) -> str:
    if wrapping_up:
        return "Complete today's session, then reflect briefly"
    return "Take a brief moment to reflect"


def _upcoming_action(*, wrapping_up: bool) -> str:
    if wrapping_up:
        return "Finish session"
    return "Reflect briefly"
