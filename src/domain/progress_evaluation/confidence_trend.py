"""ConfidenceTrend — deterministic confidence direction from Twin and evidence.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Confidence Trend
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.progress_evaluation.enums import TrendDirection


@dataclass(frozen=True, slots=True)
class ConfidenceTrend(EducationalValueObject):
    """Immutable confidence trend explained from Twin posture and evidence."""

    direction: TrendDirection
    current_level: ConfidenceLevel
    current_millipoints: int
    delta_millipoints: int
    sample_size: int
    explanation: str

    def _validate(self) -> None:
        if not isinstance(self.direction, TrendDirection):
            raise EducationalInvariantViolation(
                "direction must be a TrendDirection",
                invariant="ConfidenceTrend.direction.type",
            )
        if not isinstance(self.current_level, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "current_level must be a ConfidenceLevel",
                invariant="ConfidenceTrend.current_level.type",
            )
        for name, value in (
            ("current_millipoints", self.current_millipoints),
            ("delta_millipoints", self.delta_millipoints),
            ("sample_size", self.sample_size),
        ):
            if not isinstance(value, int) or isinstance(value, bool):
                raise EducationalInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"ConfidenceTrend.{name}.type",
                )
        if self.current_millipoints < 0 or self.current_millipoints > 1000:
            raise EducationalInvariantViolation(
                "current_millipoints must be between 0 and 1000 inclusive",
                invariant="ConfidenceTrend.current_millipoints.range",
            )
        if self.delta_millipoints < -1000 or self.delta_millipoints > 1000:
            raise EducationalInvariantViolation(
                "delta_millipoints must be between -1000 and 1000 inclusive",
                invariant="ConfidenceTrend.delta_millipoints.range",
            )
        if self.sample_size < 0:
            raise EducationalInvariantViolation(
                "sample_size must be non-negative",
                invariant="ConfidenceTrend.sample_size.non_negative",
            )
        object.__setattr__(
            self,
            "explanation",
            require_non_empty_text(self.explanation, "explanation"),
        )
