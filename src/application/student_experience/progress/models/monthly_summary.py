"""MonthlySummary — one-month historical learning summary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class MonthlySummary:
    """Immutable monthly summary projected from educational history."""

    month_start: date
    month_end: date
    missions_completed: int
    sessions_completed: int
    study_minutes: float
    study_days: int
    summary_message: str
    has_activity: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.month_start, date):
            raise JourneyInvariantViolation(
                "month_start must be a date",
                invariant="MonthlySummary.month_start.type",
            )
        if not isinstance(self.month_end, date):
            raise JourneyInvariantViolation(
                "month_end must be a date",
                invariant="MonthlySummary.month_end.type",
            )
        if self.month_end < self.month_start:
            raise JourneyInvariantViolation(
                "month_end must be on or after month_start",
                invariant="MonthlySummary.month_range",
            )
        for name in ("missions_completed", "sessions_completed", "study_days"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise JourneyInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"MonthlySummary.{name}.type",
                )
            if value < 0:
                raise JourneyInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"MonthlySummary.{name}.range",
                )
        if isinstance(self.study_minutes, bool) or not isinstance(
            self.study_minutes, int | float
        ):
            raise JourneyInvariantViolation(
                "study_minutes must be a real number",
                invariant="MonthlySummary.study_minutes.type",
            )
        minutes = round(float(self.study_minutes), 2)
        if minutes < 0.0:
            raise JourneyInvariantViolation(
                "study_minutes must be >= 0",
                invariant="MonthlySummary.study_minutes.range",
            )
        object.__setattr__(self, "study_minutes", minutes)
        message = (self.summary_message or "").strip()
        if not message:
            raise JourneyInvariantViolation(
                "summary_message must be a non-empty string",
                invariant="MonthlySummary.summary_message.required",
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
