"""MasteryTrend — deterministic mastery direction from Twin and evidence.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md
Concept
    Mastery Trend
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.progress_evaluation.enums import TrendDirection


@dataclass(frozen=True, slots=True)
class MasteryTrend(EducationalValueObject):
    """Immutable mastery trend explained from concept memory and evidence.

    ``delta_millipoints`` is second-half − first-half mastery signal on a
    −1000…1000 scale. Regression is true when direction is DECLINING.
    """

    direction: TrendDirection
    current_millipoints: int
    delta_millipoints: int
    sample_size: int
    regression_detected: bool
    explanation: str

    def _validate(self) -> None:
        if not isinstance(self.direction, TrendDirection):
            raise EducationalInvariantViolation(
                "direction must be a TrendDirection",
                invariant="MasteryTrend.direction.type",
            )
        for name, value in (
            ("current_millipoints", self.current_millipoints),
            ("delta_millipoints", self.delta_millipoints),
            ("sample_size", self.sample_size),
        ):
            if not isinstance(value, int) or isinstance(value, bool):
                raise EducationalInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"MasteryTrend.{name}.type",
                )
        if self.current_millipoints < 0 or self.current_millipoints > 1000:
            raise EducationalInvariantViolation(
                "current_millipoints must be between 0 and 1000 inclusive",
                invariant="MasteryTrend.current_millipoints.range",
            )
        if self.delta_millipoints < -1000 or self.delta_millipoints > 1000:
            raise EducationalInvariantViolation(
                "delta_millipoints must be between -1000 and 1000 inclusive",
                invariant="MasteryTrend.delta_millipoints.range",
            )
        if self.sample_size < 0:
            raise EducationalInvariantViolation(
                "sample_size must be non-negative",
                invariant="MasteryTrend.sample_size.non_negative",
            )
        if not isinstance(self.regression_detected, bool):
            raise EducationalInvariantViolation(
                "regression_detected must be a boolean",
                invariant="MasteryTrend.regression_detected.type",
            )
        if self.regression_detected and self.direction is not TrendDirection.DECLINING:
            raise EducationalInvariantViolation(
                "regression requires declining mastery direction",
                invariant="MasteryTrend.regression_detected.align",
            )
        if (
            self.direction is TrendDirection.DECLINING
            and not self.regression_detected
        ):
            raise EducationalInvariantViolation(
                "declining mastery must mark regression_detected",
                invariant="MasteryTrend.regression_detected.declining",
            )
        object.__setattr__(
            self,
            "explanation",
            require_non_empty_text(self.explanation, "explanation"),
        )

    @property
    def is_improving(self) -> bool:
        return self.direction is TrendDirection.IMPROVING

    @property
    def is_declining(self) -> bool:
        return self.direction is TrendDirection.DECLINING
