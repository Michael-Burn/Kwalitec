"""ProgressCard — student-facing progress projection."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.home.enums import MasteryTrendLabel
from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class ProgressCard:
    """Immutable progress card — never raw domain objects."""

    mastery_trend: MasteryTrendLabel
    mastery_message: str
    completed_missions: int
    study_consistency_percent: float
    hours_studied: float
    weekly_growth_message: str
    has_progress_data: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.mastery_trend, MasteryTrendLabel):
            raise HomeInvariantViolation(
                "mastery_trend must be a MasteryTrendLabel",
                invariant="ProgressCard.mastery_trend.type",
            )
        message = (self.mastery_message or "").strip()
        if not message:
            raise HomeInvariantViolation(
                "mastery_message must be a non-empty string",
                invariant="ProgressCard.mastery_message.required",
            )
        object.__setattr__(self, "mastery_message", message)
        if isinstance(self.completed_missions, bool) or not isinstance(
            self.completed_missions, int
        ):
            raise HomeInvariantViolation(
                "completed_missions must be an integer",
                invariant="ProgressCard.completed_missions.type",
            )
        if self.completed_missions < 0:
            raise HomeInvariantViolation(
                "completed_missions must be >= 0",
                invariant="ProgressCard.completed_missions.range",
            )
        if isinstance(self.study_consistency_percent, bool) or not isinstance(
            self.study_consistency_percent, int | float
        ):
            raise HomeInvariantViolation(
                "study_consistency_percent must be a real number",
                invariant="ProgressCard.study_consistency_percent.type",
            )
        consistency = round(float(self.study_consistency_percent), 2)
        if consistency < 0.0 or consistency > 100.0:
            raise HomeInvariantViolation(
                "study_consistency_percent must be in [0, 100]",
                invariant="ProgressCard.study_consistency_percent.range",
            )
        object.__setattr__(self, "study_consistency_percent", consistency)
        if isinstance(self.hours_studied, bool) or not isinstance(
            self.hours_studied, int | float
        ):
            raise HomeInvariantViolation(
                "hours_studied must be a real number",
                invariant="ProgressCard.hours_studied.type",
            )
        hours = round(float(self.hours_studied), 2)
        if hours < 0.0:
            raise HomeInvariantViolation(
                "hours_studied must be >= 0",
                invariant="ProgressCard.hours_studied.range",
            )
        object.__setattr__(self, "hours_studied", hours)
        growth = (self.weekly_growth_message or "").strip()
        if not growth:
            raise HomeInvariantViolation(
                "weekly_growth_message must be a non-empty string",
                invariant="ProgressCard.weekly_growth_message.required",
            )
        object.__setattr__(self, "weekly_growth_message", growth)
