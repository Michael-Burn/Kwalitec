"""GrowthCard — weekly and monthly growth projection."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.progress.enums import TrendDirection
from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class GrowthCard:
    """Immutable growth summary projected from historical assessments."""

    weekly_missions_completed: int
    monthly_missions_completed: int
    weekly_mastery_delta: float | None
    monthly_mastery_delta: float | None
    weekly_growth_message: str
    monthly_growth_message: str
    mastery_trend: TrendDirection
    has_growth_data: bool = False

    def __post_init__(self) -> None:
        for name in ("weekly_missions_completed", "monthly_missions_completed"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise JourneyInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"GrowthCard.{name}.type",
                )
            if value < 0:
                raise JourneyInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"GrowthCard.{name}.range",
                )
        for name in ("weekly_mastery_delta", "monthly_mastery_delta"):
            value = getattr(self, name)
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise JourneyInvariantViolation(
                    f"{name} must be a real number when provided",
                    invariant=f"GrowthCard.{name}.type",
                )
            object.__setattr__(self, name, round(float(value), 4))
        for name in ("weekly_growth_message", "monthly_growth_message"):
            message = (getattr(self, name) or "").strip()
            if not message:
                raise JourneyInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"GrowthCard.{name}.required",
                )
            object.__setattr__(self, name, message)
        if not isinstance(self.mastery_trend, TrendDirection):
            raise JourneyInvariantViolation(
                "mastery_trend must be a TrendDirection",
                invariant="GrowthCard.mastery_trend.type",
            )
