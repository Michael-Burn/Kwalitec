"""MomentumCard — streak and consistency projection."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class MomentumCard:
    """Immutable momentum card — streak, consistency, completion rate."""

    current_streak_days: int
    weekly_consistency_percent: float
    recent_completion_rate_percent: float
    average_session_duration_minutes: float
    momentum_message: str
    has_momentum_data: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.current_streak_days, bool) or not isinstance(
            self.current_streak_days, int
        ):
            raise HomeInvariantViolation(
                "current_streak_days must be an integer",
                invariant="MomentumCard.current_streak_days.type",
            )
        if self.current_streak_days < 0:
            raise HomeInvariantViolation(
                "current_streak_days must be >= 0",
                invariant="MomentumCard.current_streak_days.range",
            )
        for name in (
            "weekly_consistency_percent",
            "recent_completion_rate_percent",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise HomeInvariantViolation(
                    f"{name} must be a real number",
                    invariant=f"MomentumCard.{name}.type",
                )
            rounded = round(float(value), 2)
            if rounded < 0.0 or rounded > 100.0:
                raise HomeInvariantViolation(
                    f"{name} must be in [0, 100]",
                    invariant=f"MomentumCard.{name}.range",
                )
            object.__setattr__(self, name, rounded)
        if isinstance(self.average_session_duration_minutes, bool) or not isinstance(
            self.average_session_duration_minutes, int | float
        ):
            raise HomeInvariantViolation(
                "average_session_duration_minutes must be a real number",
                invariant="MomentumCard.average_session_duration_minutes.type",
            )
        avg = round(float(self.average_session_duration_minutes), 2)
        if avg < 0.0:
            raise HomeInvariantViolation(
                "average_session_duration_minutes must be >= 0",
                invariant="MomentumCard.average_session_duration_minutes.range",
            )
        object.__setattr__(self, "average_session_duration_minutes", avg)
        message = (self.momentum_message or "").strip()
        if not message:
            raise HomeInvariantViolation(
                "momentum_message must be a non-empty string",
                invariant="MomentumCard.momentum_message.required",
            )
        object.__setattr__(self, "momentum_message", message)
