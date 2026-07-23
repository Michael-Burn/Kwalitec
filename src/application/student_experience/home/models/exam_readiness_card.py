"""ExamReadinessCard — exam readiness projection (never a new estimate)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.student_experience.home.enums import ReadinessTrend
from application.student_experience.home.errors import HomeInvariantViolation


@dataclass(frozen=True, slots=True)
class ExamReadinessCard:
    """Immutable exam readiness card — projects existing assessment signals.

    This is a projection only. It never estimates mastery or readiness.
    """

    available: bool
    readiness_label: str
    readiness_percent: float | None
    trend: ReadinessTrend
    trend_message: str
    target_exam_label: str | None
    exam_date: date | None
    days_remaining: int | None
    next_milestone: str | None = None

    def __post_init__(self) -> None:
        label = (self.readiness_label or "").strip()
        if not label:
            raise HomeInvariantViolation(
                "readiness_label must be a non-empty string",
                invariant="ExamReadinessCard.readiness_label.required",
            )
        object.__setattr__(self, "readiness_label", label)
        if self.readiness_percent is not None:
            if isinstance(self.readiness_percent, bool) or not isinstance(
                self.readiness_percent, int | float
            ):
                raise HomeInvariantViolation(
                    "readiness_percent must be a real number when provided",
                    invariant="ExamReadinessCard.readiness_percent.type",
                )
            pct = round(float(self.readiness_percent), 2)
            if pct < 0.0 or pct > 100.0:
                raise HomeInvariantViolation(
                    "readiness_percent must be in [0, 100]",
                    invariant="ExamReadinessCard.readiness_percent.range",
                )
            object.__setattr__(self, "readiness_percent", pct)
        if not isinstance(self.trend, ReadinessTrend):
            raise HomeInvariantViolation(
                "trend must be a ReadinessTrend",
                invariant="ExamReadinessCard.trend.type",
            )
        trend_message = (self.trend_message or "").strip()
        if not trend_message:
            raise HomeInvariantViolation(
                "trend_message must be a non-empty string",
                invariant="ExamReadinessCard.trend_message.required",
            )
        object.__setattr__(self, "trend_message", trend_message)
        object.__setattr__(
            self,
            "target_exam_label",
            (self.target_exam_label or "").strip() or None,
        )
        if self.exam_date is not None and not isinstance(self.exam_date, date):
            raise HomeInvariantViolation(
                "exam_date must be a date when provided",
                invariant="ExamReadinessCard.exam_date.type",
            )
        if self.days_remaining is not None:
            if isinstance(self.days_remaining, bool) or not isinstance(
                self.days_remaining, int
            ):
                raise HomeInvariantViolation(
                    "days_remaining must be an integer when provided",
                    invariant="ExamReadinessCard.days_remaining.type",
                )
        object.__setattr__(
            self, "next_milestone", (self.next_milestone or "").strip() or None
        )
