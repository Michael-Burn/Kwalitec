"""WeeklySummary — one-week historical learning summary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class WeeklySummary:
    """Immutable weekly summary projected from educational history."""

    week_start: date
    week_end: date
    missions_completed: int
    sessions_completed: int
    study_minutes: float
    study_days: int
    summary_message: str
    has_activity: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.week_start, date):
            raise JourneyInvariantViolation(
                "week_start must be a date",
                invariant="WeeklySummary.week_start.type",
            )
        if not isinstance(self.week_end, date):
            raise JourneyInvariantViolation(
                "week_end must be a date",
                invariant="WeeklySummary.week_end.type",
            )
        if self.week_end < self.week_start:
            raise JourneyInvariantViolation(
                "week_end must be on or after week_start",
                invariant="WeeklySummary.week_range",
            )
        for name in ("missions_completed", "sessions_completed", "study_days"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise JourneyInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"WeeklySummary.{name}.type",
                )
            if value < 0:
                raise JourneyInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"WeeklySummary.{name}.range",
                )
        if isinstance(self.study_minutes, bool) or not isinstance(
            self.study_minutes, int | float
        ):
            raise JourneyInvariantViolation(
                "study_minutes must be a real number",
                invariant="WeeklySummary.study_minutes.type",
            )
        minutes = round(float(self.study_minutes), 2)
        if minutes < 0.0:
            raise JourneyInvariantViolation(
                "study_minutes must be >= 0",
                invariant="WeeklySummary.study_minutes.range",
            )
        object.__setattr__(self, "study_minutes", minutes)
        message = (self.summary_message or "").strip()
        if not message:
            raise JourneyInvariantViolation(
                "summary_message must be a non-empty string",
                invariant="WeeklySummary.summary_message.required",
            )
        object.__setattr__(self, "summary_message", message)
        object.__setattr__(
            self,
            "has_activity",
            self.missions_completed > 0
            or self.sessions_completed > 0
            or self.study_minutes > 0.0
            or self.study_days > 0,
        )
