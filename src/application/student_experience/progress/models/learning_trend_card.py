"""LearningTrendCard — historical learning trends only (no forecasting)."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.progress.enums import TrendDirection
from application.student_experience.progress.errors import JourneyInvariantViolation


@dataclass(frozen=True, slots=True)
class LearningTrendCard:
    """Immutable historical trend projection — never forecasts."""

    mastery_trend: TrendDirection
    mastery_trend_message: str
    confidence_trend: TrendDirection
    confidence_trend_message: str
    consistency_trend: TrendDirection
    consistency_trend_message: str
    mission_completion_trend: TrendDirection
    mission_completion_trend_message: str
    has_trend_data: bool = False

    def __post_init__(self) -> None:
        pairs = (
            ("mastery_trend", "mastery_trend_message"),
            ("confidence_trend", "confidence_trend_message"),
            ("consistency_trend", "consistency_trend_message"),
            ("mission_completion_trend", "mission_completion_trend_message"),
        )
        for trend_name, message_name in pairs:
            trend = getattr(self, trend_name)
            if not isinstance(trend, TrendDirection):
                raise JourneyInvariantViolation(
                    f"{trend_name} must be a TrendDirection",
                    invariant=f"LearningTrendCard.{trend_name}.type",
                )
            message = (getattr(self, message_name) or "").strip()
            if not message:
                raise JourneyInvariantViolation(
                    f"{message_name} must be a non-empty string",
                    invariant=f"LearningTrendCard.{message_name}.required",
                )
            object.__setattr__(self, message_name, message)
