"""ReadinessCard — current readiness projection (never a new estimate)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from application.student_experience.readiness.enums import (
    ReadinessCategory,
    ReadinessDirection,
)
from application.student_experience.readiness.errors import (
    ReadinessInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class ReadinessCard:
    """Immutable current readiness card — projects existing assessment signals.

    This is a projection only. It never estimates mastery or forecasts exams.
    """

    available: bool
    readiness_percent: float | None
    readiness_category: ReadinessCategory
    readiness_label: str
    direction: ReadinessDirection
    direction_message: str
    target_exam_label: str | None
    exam_date: date | None
    days_remaining: int | None

    def __post_init__(self) -> None:
        if not isinstance(self.readiness_category, ReadinessCategory):
            raise ReadinessInvariantViolation(
                "readiness_category must be a ReadinessCategory",
                invariant="ReadinessCard.readiness_category.type",
            )
        label = (self.readiness_label or "").strip()
        if not label:
            raise ReadinessInvariantViolation(
                "readiness_label must be a non-empty string",
                invariant="ReadinessCard.readiness_label.required",
            )
        object.__setattr__(self, "readiness_label", label)
        if self.readiness_percent is not None:
            if isinstance(self.readiness_percent, bool) or not isinstance(
                self.readiness_percent, int | float
            ):
                raise ReadinessInvariantViolation(
                    "readiness_percent must be a real number when provided",
                    invariant="ReadinessCard.readiness_percent.type",
                )
            pct = round(float(self.readiness_percent), 2)
            if pct < 0.0 or pct > 100.0:
                raise ReadinessInvariantViolation(
                    "readiness_percent must be in [0, 100]",
                    invariant="ReadinessCard.readiness_percent.range",
                )
            object.__setattr__(self, "readiness_percent", pct)
        if not isinstance(self.direction, ReadinessDirection):
            raise ReadinessInvariantViolation(
                "direction must be a ReadinessDirection",
                invariant="ReadinessCard.direction.type",
            )
        direction_message = (self.direction_message or "").strip()
        if not direction_message:
            raise ReadinessInvariantViolation(
                "direction_message must be a non-empty string",
                invariant="ReadinessCard.direction_message.required",
            )
        object.__setattr__(self, "direction_message", direction_message)
        object.__setattr__(
            self,
            "target_exam_label",
            (self.target_exam_label or "").strip() or None,
        )
        if self.exam_date is not None and not isinstance(self.exam_date, date):
            raise ReadinessInvariantViolation(
                "exam_date must be a date when provided",
                invariant="ReadinessCard.exam_date.type",
            )
        if self.days_remaining is not None:
            if isinstance(self.days_remaining, bool) or not isinstance(
                self.days_remaining, int
            ):
                raise ReadinessInvariantViolation(
                    "days_remaining must be an integer when provided",
                    invariant="ReadinessCard.days_remaining.type",
                )
