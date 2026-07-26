"""Immutable DayExperience DTO (P2-MS004 / P2-MS005).

Canonical representation of today's student Experience. Assembled from
Programme I outputs via DailyMission / ExperienceTimeline. Owns no
educational logic, persistence, or engine authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.unified_journey.contracts import CONTRACT_VERSION
from app.application.unified_journey.daily_mission import (
    DailyMission,
    empty_daily_mission,
)
from app.application.unified_journey.reflection_states import (
    ReflectionState,
    reflection_is_active,
    resolve_reflection_state,
)
from app.application.unified_journey.session_outcome import SessionOutcome
from app.application.unified_journey.session_phases import (
    SessionPhase,
    resolve_session_phase,
    session_status_label,
)
from app.application.unified_journey.timeline import (
    ExperienceTimeline,
    empty_experience_timeline,
)


@dataclass(frozen=True)
class DayExperience:
    """Canonical daily presentation object for the guided student journey.

    Presentation-only. Never invents educational recommendations or
    modifies Programme I outputs.
    """

    daily_mission: DailyMission = field(default_factory=empty_daily_mission)
    timeline: ExperienceTimeline = field(
        default_factory=empty_experience_timeline
    )
    current_phase: SessionPhase = SessionPhase.READY
    session_status: str = "Ready"
    reflection_available: bool = False
    upcoming_transition: str = ""
    progress_summary: str = ""
    # P2-MS005 Guided Reflection (presentation only).
    session_outcome: SessionOutcome | None = None
    reflection_state: ReflectionState | None = None
    contract_version: str = CONTRACT_VERSION
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not isinstance(self.daily_mission, DailyMission):
            raise TypeError("daily_mission must be a DailyMission")
        if not isinstance(self.timeline, ExperienceTimeline):
            raise TypeError("timeline must be an ExperienceTimeline")
        if self.session_outcome is not None and not isinstance(
            self.session_outcome, SessionOutcome
        ):
            raise TypeError("session_outcome must be a SessionOutcome or None")
        phase = resolve_session_phase(self.current_phase)
        object.__setattr__(self, "current_phase", phase)
        status = (self.session_status or "").strip() or session_status_label(
            phase
        )
        object.__setattr__(self, "session_status", status)
        object.__setattr__(
            self, "upcoming_transition", (self.upcoming_transition or "").strip()
        )
        object.__setattr__(
            self, "progress_summary", (self.progress_summary or "").strip()
        )
        object.__setattr__(
            self, "reflection_available", bool(self.reflection_available)
        )
        object.__setattr__(
            self,
            "reflection_state",
            resolve_reflection_state(self.reflection_state),
        )

    @property
    def is_ready(self) -> bool:
        return self.current_phase is SessionPhase.READY

    @property
    def is_studying(self) -> bool:
        return self.current_phase is SessionPhase.STUDYING

    @property
    def is_wrapping_up(self) -> bool:
        return self.current_phase is SessionPhase.WRAPPING_UP

    @property
    def is_complete(self) -> bool:
        return self.current_phase is SessionPhase.COMPLETE

    @property
    def reflection_active(self) -> bool:
        """True when Guided Reflection should present before day completion."""
        if not self.reflection_available:
            return False
        if self.session_outcome is None:
            return False
        if not self.session_outcome.reflection_available:
            return False
        return reflection_is_active(self.reflection_state)

    @property
    def mission_active(self) -> bool:
        """True when today's mission can be guided (presentation only)."""
        if self.daily_mission.is_completed:
            return False
        if self.current_phase is SessionPhase.COMPLETE:
            return False
        title = (self.daily_mission.title or "").strip()
        if not title:
            return False
        availability = dict(self.daily_mission.metadata).get("availability", "")
        if availability == "placeholder":
            return False
        return self.current_phase in {
            SessionPhase.READY,
            SessionPhase.STUDYING,
            SessionPhase.WRAPPING_UP,
        }


def empty_day_experience() -> DayExperience:
    """Placeholder DayExperience when Programme I inputs are unavailable."""
    return DayExperience(
        daily_mission=empty_daily_mission(),
        timeline=empty_experience_timeline(),
        current_phase=SessionPhase.READY,
        session_status=session_status_label(SessionPhase.READY),
        reflection_available=False,
        upcoming_transition="Start today's mission when ready",
        progress_summary="",
        session_outcome=None,
        reflection_state=None,
        metadata=(("availability", "placeholder"),),
    )


def upcoming_transition_for_phase(phase: SessionPhase | str) -> str:
    """Student-facing next presentation transition (no educational decisions)."""
    resolved = resolve_session_phase(phase)
    if resolved is SessionPhase.READY:
        return "Start today's study session"
    if resolved is SessionPhase.STUDYING:
        return "Finish when ready to wrap up"
    if resolved is SessionPhase.WRAPPING_UP:
        return "Complete today's session"
    return "Take a brief moment to reflect"


def progress_summary_for(
    *,
    mission: DailyMission,
    phase: SessionPhase | str,
) -> str:
    """Concise presentation progress line from existing mission fields."""
    resolved = resolve_session_phase(phase)
    title = (mission.title or "").strip() or "Today's Mission"
    if resolved is SessionPhase.READY:
        if mission.mission_summary:
            return mission.mission_summary
        return f"Ready to begin: {title}"
    if resolved is SessionPhase.STUDYING:
        return f"Studying: {title}"
    if resolved is SessionPhase.WRAPPING_UP:
        return f"Wrapping up: {title}"
    return f"Completed: {title}"


def phase_from_completion_status(completion_status: str) -> SessionPhase:
    """Map DailyMission UI completion onto an initial session phase."""
    status = (completion_status or "").strip().lower()
    if status == "complete":
        return SessionPhase.COMPLETE
    if status == "in_progress":
        return SessionPhase.STUDYING
    return SessionPhase.READY
