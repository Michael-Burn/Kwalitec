"""Immutable StudySession presentation DTO (P2-MS004).

Student-facing guided session view model. Experience state only —
does not calculate timings or own educational authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.unified_journey.contracts import (
    COMPLETION_COMPLETE,
    COMPLETION_IN_PROGRESS,
    COMPLETION_NOT_STARTED,
    COMPLETION_UNKNOWN,
    COMPLETION_VALUES,
    CONTRACT_VERSION,
)
from app.application.unified_journey.session_phases import (
    ELAPSED_STATE_VALUES,
    SessionPhase,
    elapsed_state_for_phase,
    resolve_session_phase,
)


@dataclass(frozen=True)
class StudySession:
    """Immutable guided study session view model (Experience Layer).

    Distinct from educational ``StudySession`` models in revision planning
    / domain study planning. Presentation fields only — no timers.
    """

    mission_title: str = ""
    learning_objective: str = ""
    estimated_duration: str = ""
    current_phase: SessionPhase = SessionPhase.READY
    start_time: str = ""  # Presentation label only — never a live clock.
    elapsed_state: str = ""  # Presentation state only — never computed duration.
    completion_state: str = COMPLETION_UNKNOWN
    next_step: str = ""
    contract_version: str = CONTRACT_VERSION
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        phase = resolve_session_phase(self.current_phase)
        object.__setattr__(self, "current_phase", phase)
        object.__setattr__(
            self, "mission_title", (self.mission_title or "").strip()
        )
        object.__setattr__(
            self, "learning_objective", (self.learning_objective or "").strip()
        )
        object.__setattr__(
            self, "estimated_duration", (self.estimated_duration or "").strip()
        )
        object.__setattr__(self, "start_time", (self.start_time or "").strip())
        object.__setattr__(self, "next_step", (self.next_step or "").strip())
        elapsed = (self.elapsed_state or "").strip().lower()
        if not elapsed:
            elapsed = elapsed_state_for_phase(phase)
        if elapsed not in ELAPSED_STATE_VALUES:
            raise ValueError(f"unknown study session elapsed_state: {elapsed!r}")
        object.__setattr__(self, "elapsed_state", elapsed)
        completion = (self.completion_state or "").strip().lower()
        if completion not in COMPLETION_VALUES:
            raise ValueError(
                f"unknown study session completion_state: "
                f"{self.completion_state!r}"
            )
        object.__setattr__(self, "completion_state", completion)

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


def empty_study_session() -> StudySession:
    """Placeholder StudySession when DayExperience is unavailable."""
    return StudySession(
        mission_title="Today's Mission",
        learning_objective="",
        estimated_duration="",
        current_phase=SessionPhase.READY,
        start_time="",
        elapsed_state=elapsed_state_for_phase(SessionPhase.READY),
        completion_state=COMPLETION_NOT_STARTED,
        next_step="Start today's study session",
        metadata=(("availability", "placeholder"),),
    )


def completion_state_for_phase(phase: SessionPhase | str) -> str:
    """Map presentation phase onto completion_state vocabulary."""
    resolved = resolve_session_phase(phase)
    if resolved is SessionPhase.READY:
        return COMPLETION_NOT_STARTED
    if resolved is SessionPhase.STUDYING:
        return COMPLETION_IN_PROGRESS
    if resolved is SessionPhase.WRAPPING_UP:
        return COMPLETION_IN_PROGRESS
    return COMPLETION_COMPLETE
