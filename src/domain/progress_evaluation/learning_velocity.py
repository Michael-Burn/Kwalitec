"""LearningVelocity — rate of educational progress from evidence and missions.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Learning Velocity
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.progress_evaluation.enums import VelocityBand


@dataclass(frozen=True, slots=True)
class LearningVelocity(EducationalValueObject):
    """Immutable learning velocity explained from evidence chronology.

    Velocity uses integer millipoints so identical inputs yield identical
    reports. ``events_per_day_millipoints`` is events/day × 1000.
    """

    band: VelocityBand
    events_per_day_millipoints: int
    mastery_delta_millipoints: int
    missions_completed: int
    window_days: int
    explanation: str

    def _validate(self) -> None:
        if not isinstance(self.band, VelocityBand):
            raise EducationalInvariantViolation(
                "band must be a VelocityBand",
                invariant="LearningVelocity.band.type",
            )
        for name, value in (
            ("events_per_day_millipoints", self.events_per_day_millipoints),
            ("mastery_delta_millipoints", self.mastery_delta_millipoints),
            ("missions_completed", self.missions_completed),
            ("window_days", self.window_days),
        ):
            if not isinstance(value, int) or isinstance(value, bool):
                raise EducationalInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"LearningVelocity.{name}.type",
                )
        if self.events_per_day_millipoints < 0:
            raise EducationalInvariantViolation(
                "events_per_day_millipoints must be non-negative",
                invariant="LearningVelocity.events_per_day_millipoints.non_negative",
            )
        if (
            self.mastery_delta_millipoints < -1000
            or self.mastery_delta_millipoints > 1000
        ):
            raise EducationalInvariantViolation(
                "mastery_delta_millipoints must be between -1000 and 1000 inclusive",
                invariant="LearningVelocity.mastery_delta_millipoints.range",
            )
        if self.missions_completed < 0:
            raise EducationalInvariantViolation(
                "missions_completed must be non-negative",
                invariant="LearningVelocity.missions_completed.non_negative",
            )
        if self.window_days < 0:
            raise EducationalInvariantViolation(
                "window_days must be non-negative",
                invariant="LearningVelocity.window_days.non_negative",
            )
        object.__setattr__(
            self,
            "explanation",
            require_non_empty_text(self.explanation, "explanation"),
        )

    @property
    def is_active(self) -> bool:
        return self.events_per_day_millipoints > 0

    @property
    def is_improving(self) -> bool:
        return self.mastery_delta_millipoints > 0
