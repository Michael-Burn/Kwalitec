"""LearningStreak — consecutive study-day recognition for presentation.

Architecture Source
    EXP-001 Student Experience Engine
Concept
    Learning Streak
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.student_experience.enums import StreakBand


@dataclass(frozen=True, slots=True)
class LearningStreak(EducationalValueObject):
    """Immutable consecutive-activity streak derived from plan days and progress.

    Streaks are presentation recognition of study continuity. They do not
    invent mastery, alter recommendations, or consult wall-clock time.
    """

    current_days: int
    longest_days: int
    active_day_indices: tuple[int, ...]
    band: StreakBand
    explanation: str

    def _validate(self) -> None:
        for name, value in (
            ("current_days", self.current_days),
            ("longest_days", self.longest_days),
        ):
            if not isinstance(value, int) or isinstance(value, bool):
                raise EducationalInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"LearningStreak.{name}.type",
                )
            if value < 0:
                raise EducationalInvariantViolation(
                    f"{name} must be non-negative",
                    invariant=f"LearningStreak.{name}.non_negative",
                )
        if self.current_days > self.longest_days:
            raise EducationalInvariantViolation(
                "current_days cannot exceed longest_days",
                invariant="LearningStreak.current_vs_longest",
            )
        if not isinstance(self.active_day_indices, tuple):
            raise EducationalInvariantViolation(
                "active_day_indices must be a tuple",
                invariant="LearningStreak.active_day_indices.type",
            )
        previous: int | None = None
        for day in self.active_day_indices:
            if not isinstance(day, int) or isinstance(day, bool):
                raise EducationalInvariantViolation(
                    "active_day_indices must contain integers",
                    invariant="LearningStreak.active_day_indices.item_type",
                )
            if day < 0:
                raise EducationalInvariantViolation(
                    "active_day_indices must be non-negative",
                    invariant="LearningStreak.active_day_indices.non_negative",
                )
            if previous is not None and day <= previous:
                raise EducationalInvariantViolation(
                    "active_day_indices must be strictly ascending",
                    invariant="LearningStreak.active_day_indices.ordered",
                )
            previous = day
        if len(self.active_day_indices) < self.current_days:
            raise EducationalInvariantViolation(
                "active_day_indices must cover current streak length",
                invariant="LearningStreak.active_day_indices.cover_current",
            )
        if not isinstance(self.band, StreakBand):
            raise EducationalInvariantViolation(
                "band must be a StreakBand",
                invariant="LearningStreak.band.type",
            )
        if self.band is not self.band_for(self.current_days):
            raise EducationalInvariantViolation(
                "band must match current_days",
                invariant="LearningStreak.band.align",
            )
        object.__setattr__(
            self,
            "explanation",
            require_non_empty_text(self.explanation, "explanation"),
        )

    @staticmethod
    def band_for(current_days: int) -> StreakBand:
        """Map streak length to a deterministic presentation band."""
        if current_days <= 0:
            return StreakBand.NONE
        if current_days <= 2:
            return StreakBand.STARTING
        if current_days <= 6:
            return StreakBand.BUILDING
        return StreakBand.STRONG

    @property
    def is_active(self) -> bool:
        return self.current_days > 0
