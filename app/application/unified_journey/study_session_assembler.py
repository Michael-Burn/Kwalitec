"""StudySessionAssembler — DayExperience → StudySession (P2-MS004).

Prepares student-facing wording, exposes one current objective, and
determines the next presentation transition. No educational calculations.
"""

from __future__ import annotations

import re

from app.application.unified_journey.day_experience import (
    DayExperience,
    empty_day_experience,
)
from app.application.unified_journey.session_phases import (
    SessionPhase,
    elapsed_state_for_phase,
)
from app.application.unified_journey.study_session import (
    StudySession,
    completion_state_for_phase,
    empty_study_session,
)

# Soften subsystem terms that may still appear in pass-through copy.
_SUBSYSTEM_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = tuple(
    (
        re.compile(pattern, re.IGNORECASE),
        replacement,
    )
    for pattern, replacement in (
        (r"\bdigital\s+twin\b", "learning profile"),
        (r"\bstudent\s+twin\b", "learning profile"),
        (r"\badaptive\s+(?:engine|decision|recommendation)s?\b", "study guidance"),
        (r"\blearning\s+orchestrator\b", "study plan"),
        (r"\bmission\s+engine\b", "study plan"),
        (r"\bstrategy\s+engine\b", "study plan"),
        (r"\bevidence\s+platform\b", "learning progress"),
        (r"\bruntime\s+a\b", "learning system"),
    )
)
_WHITESPACE = re.compile(r"\s+")

_START_TIME_LABELS: dict[SessionPhase, str] = {
    SessionPhase.READY: "",
    SessionPhase.STUDYING: "Session in progress",
    SessionPhase.WRAPPING_UP: "Session wrapping up",
    SessionPhase.COMPLETE: "Session finished",
}


class StudySessionAssembler:
    """Transform DayExperience into a student-facing StudySession.

    Responsibilities:
    - Prepare student-facing wording
    - Expose one current learning objective
    - Determine the next presentation transition

    Non-responsibilities:
    - Timing / duration calculations
    - Educational recommendations
    - Persistence / evidence / engine calls
    """

    def assemble(self, day: DayExperience | None) -> StudySession:
        """Derive an immutable StudySession from DayExperience."""
        if day is None:
            return empty_study_session()

        mission = day.daily_mission
        phase = day.current_phase
        title = _student_copy(mission.title) or "Today's Mission"
        objective = _current_objective(day)
        duration = (mission.estimated_duration or "").strip()
        next_step = (day.upcoming_transition or "").strip() or _default_next_step(
            phase
        )

        return StudySession(
            mission_title=title,
            learning_objective=objective,
            estimated_duration=duration,
            current_phase=phase,
            start_time=_START_TIME_LABELS.get(phase, ""),
            elapsed_state=elapsed_state_for_phase(phase),
            completion_state=completion_state_for_phase(phase),
            next_step=next_step,
            metadata=day.metadata
            + (
                ("phase", phase.value),
                ("via", "study_session_assembler"),
            ),
        )

    def assemble_placeholder(self) -> StudySession:
        """Assemble from an explicit placeholder DayExperience."""
        return self.assemble(empty_day_experience())


def _current_objective(day: DayExperience) -> str:
    """One current student-facing objective — presentation only."""
    mission = day.daily_mission
    if mission.expected_outcome:
        return _student_copy(mission.expected_outcome)
    if mission.mission_summary:
        return _student_copy(mission.mission_summary)
    if mission.reason:
        return _student_copy(mission.reason)
    if mission.title:
        return _student_copy(mission.title)
    return ""


def _default_next_step(phase: SessionPhase) -> str:
    if phase is SessionPhase.READY:
        return "Start today's study session"
    if phase is SessionPhase.STUDYING:
        return "Finish when ready to wrap up"
    if phase is SessionPhase.WRAPPING_UP:
        return "Complete today's session"
    return "Today's session is complete"


def _student_copy(text: str) -> str:
    value = (text or "").strip()
    if not value:
        return ""
    for pattern, replacement in _SUBSYSTEM_PATTERNS:
        value = pattern.sub(replacement, value)
    return _WHITESPACE.sub(" ", value).strip(" -–,;")
