"""ConsistencyCard — streak and study frequency projection."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class ConsistencyCard:
    """Immutable consistency projection — streak, frequency, completion."""

    current_streak_days: int
    longest_streak_days: int
    study_frequency_message: str
    average_weekly_sessions: float
    average_completion_rate_percent: float
    consistency_message: str
    has_consistency_data: bool = False

    def __post_init__(self) -> None:
        for name in ("current_streak_days", "longest_streak_days"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise JourneyInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"ConsistencyCard.{name}.type",
                )
            if value < 0:
                raise JourneyInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"ConsistencyCard.{name}.range",
                )
        for name in ("study_frequency_message", "consistency_message"):
            message = (getattr(self, name) or "").strip()
            if not message:
                raise JourneyInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ConsistencyCard.{name}.required",
                )
            object.__setattr__(self, name, message)
        if isinstance(self.average_weekly_sessions, bool) or not isinstance(
            self.average_weekly_sessions, int | float
        ):
            raise JourneyInvariantViolation(
                "average_weekly_sessions must be a real number",
                invariant="ConsistencyCard.average_weekly_sessions.type",
            )
        avg = round(float(self.average_weekly_sessions), 2)
        if avg < 0.0:
            raise JourneyInvariantViolation(
                "average_weekly_sessions must be >= 0",
                invariant="ConsistencyCard.average_weekly_sessions.range",
            )
        object.__setattr__(self, "average_weekly_sessions", avg)
        if isinstance(self.average_completion_rate_percent, bool) or not isinstance(
            self.average_completion_rate_percent, int | float
        ):
            raise JourneyInvariantViolation(
                "average_completion_rate_percent must be a real number",
                invariant="ConsistencyCard.average_completion_rate_percent.type",
            )
        rate = round(float(self.average_completion_rate_percent), 2)
        if rate < 0.0 or rate > 100.0:
            raise JourneyInvariantViolation(
                "average_completion_rate_percent must be in [0, 100]",
                invariant="ConsistencyCard.average_completion_rate_percent.range",
            )
        object.__setattr__(self, "average_completion_rate_percent", rate)
