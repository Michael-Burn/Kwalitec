"""ProgressSummary — compact progress projection used by summarise_progress."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.home.enums import MasteryTrendLabel
from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class ProgressSummary:
    """Compact immutable progress summary derived from Education OS outputs."""

    student_id: str
    mastery_trend: MasteryTrendLabel
    mastery_message: str
    completed_missions: int
    abandoned_missions: int
    in_progress_missions: int
    study_consistency_percent: float
    hours_studied: float
    weekly_growth_message: str
    knowledge_gap_count: int
    recommendation_count: int

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise HomeInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ProgressSummary.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.mastery_trend, MasteryTrendLabel):
            raise HomeInvariantViolation(
                "mastery_trend must be a MasteryTrendLabel",
                invariant="ProgressSummary.mastery_trend.type",
            )
        message = (self.mastery_message or "").strip()
        if not message:
            raise HomeInvariantViolation(
                "mastery_message must be a non-empty string",
                invariant="ProgressSummary.mastery_message.required",
            )
        object.__setattr__(self, "mastery_message", message)
        for name in (
            "completed_missions",
            "abandoned_missions",
            "in_progress_missions",
            "knowledge_gap_count",
            "recommendation_count",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise HomeInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"ProgressSummary.{name}.type",
                )
            if value < 0:
                raise HomeInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"ProgressSummary.{name}.range",
                )
        if isinstance(self.study_consistency_percent, bool) or not isinstance(
            self.study_consistency_percent, int | float
        ):
            raise HomeInvariantViolation(
                "study_consistency_percent must be a real number",
                invariant="ProgressSummary.study_consistency_percent.type",
            )
        object.__setattr__(
            self,
            "study_consistency_percent",
            round(float(self.study_consistency_percent), 2),
        )
        if isinstance(self.hours_studied, bool) or not isinstance(
            self.hours_studied, int | float
        ):
            raise HomeInvariantViolation(
                "hours_studied must be a real number",
                invariant="ProgressSummary.hours_studied.type",
            )
        object.__setattr__(self, "hours_studied", round(float(self.hours_studied), 2))
        growth = (self.weekly_growth_message or "").strip()
        if not growth:
            raise HomeInvariantViolation(
                "weekly_growth_message must be a non-empty string",
                invariant="ProgressSummary.weekly_growth_message.required",
            )
        object.__setattr__(self, "weekly_growth_message", growth)
