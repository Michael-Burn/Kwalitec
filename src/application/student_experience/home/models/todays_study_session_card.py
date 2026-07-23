"""TodaysStudySessionCard — today's scheduled study session projection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time

from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class TodaysStudySessionCard:
    """Immutable card for today's scheduled study session, if any."""

    session_date: date
    start_time: time | None
    end_time: time | None
    estimated_duration_minutes: int
    mission_count: int
    status_label: str
    session_id: str | None = None
    has_session: bool = False
    objectives_summary: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.session_date, date):
            raise HomeInvariantViolation(
                "session_date must be a date",
                invariant="TodaysStudySessionCard.session_date.type",
            )
        if isinstance(self.estimated_duration_minutes, bool) or not isinstance(
            self.estimated_duration_minutes, int
        ):
            raise HomeInvariantViolation(
                "estimated_duration_minutes must be an integer",
                invariant="TodaysStudySessionCard.estimated_duration_minutes.type",
            )
        if self.estimated_duration_minutes < 0:
            raise HomeInvariantViolation(
                "estimated_duration_minutes must be >= 0",
                invariant="TodaysStudySessionCard.estimated_duration_minutes.range",
            )
        if isinstance(self.mission_count, bool) or not isinstance(
            self.mission_count, int
        ):
            raise HomeInvariantViolation(
                "mission_count must be an integer",
                invariant="TodaysStudySessionCard.mission_count.type",
            )
        if self.mission_count < 0:
            raise HomeInvariantViolation(
                "mission_count must be >= 0",
                invariant="TodaysStudySessionCard.mission_count.range",
            )
        status = (self.status_label or "").strip()
        if not status:
            raise HomeInvariantViolation(
                "status_label must be a non-empty string",
                invariant="TodaysStudySessionCard.status_label.required",
            )
        object.__setattr__(self, "status_label", status)
        object.__setattr__(
            self, "session_id", (self.session_id or "").strip() or None
        )
        object.__setattr__(
            self,
            "objectives_summary",
            (self.objectives_summary or "").strip() or None,
        )
