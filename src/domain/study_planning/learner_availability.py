"""LearnerAvailability — learner capacity constraints for study planning.

Architecture Source
    SESSION_ASSEMBLY_MODEL.md (capacity honesty)
Concept
    Learner Availability

Relative day indices only. No wall-clock calendar APIs.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class AvailabilityWindow(EducationalValueObject):
    """Capacity available on one relative planning day."""

    day_index: int
    available_minutes: int

    def _validate(self) -> None:
        if not isinstance(self.day_index, int) or isinstance(self.day_index, bool):
            raise EducationalInvariantViolation(
                "day_index must be an integer",
                invariant="AvailabilityWindow.day_index.type",
            )
        if self.day_index < 0:
            raise EducationalInvariantViolation(
                "day_index must be non-negative",
                invariant="AvailabilityWindow.day_index.non_negative",
            )
        if not isinstance(self.available_minutes, int) or isinstance(
            self.available_minutes, bool
        ):
            raise EducationalInvariantViolation(
                "available_minutes must be an integer",
                invariant="AvailabilityWindow.available_minutes.type",
            )
        if self.available_minutes <= 0:
            raise EducationalInvariantViolation(
                "available_minutes must be positive",
                invariant="AvailabilityWindow.available_minutes.positive",
            )


@dataclass(frozen=True, slots=True)
class LearnerAvailability(EducationalValueObject):
    """Immutable learner capacity map over relative planning days.

    Windows must declare unique day indices and are stored in ascending
    day-index order. This is a pure constraint object — not a calendar product.
    """

    student_id: str
    windows: tuple[AvailabilityWindow, ...]

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "student_id",
            require_non_empty_text(self.student_id, "student_id"),
        )
        if not isinstance(self.windows, tuple) or not self.windows:
            raise EducationalInvariantViolation(
                "windows must be a non-empty tuple",
                invariant="LearnerAvailability.windows.min_one",
            )
        seen: set[int] = set()
        previous = -1
        for window in self.windows:
            if not isinstance(window, AvailabilityWindow):
                raise EducationalInvariantViolation(
                    "windows must contain AvailabilityWindow values",
                    invariant="LearnerAvailability.windows.item_type",
                )
            if window.day_index in seen:
                raise EducationalInvariantViolation(
                    "availability windows must declare unique day indices",
                    invariant="LearnerAvailability.windows.unique_day",
                )
            if window.day_index < previous:
                raise EducationalInvariantViolation(
                    "availability windows must be ordered by ascending day_index",
                    invariant="LearnerAvailability.windows.order",
                )
            seen.add(window.day_index)
            previous = window.day_index

    @classmethod
    def of(
        cls,
        student_id: str,
        *windows: AvailabilityWindow,
    ) -> LearnerAvailability:
        ordered = tuple(sorted(windows, key=lambda w: w.day_index))
        return cls(student_id=student_id, windows=ordered)

    def day_indices(self) -> tuple[int, ...]:
        return tuple(window.day_index for window in self.windows)

    def minutes_on(self, day_index: int) -> int:
        for window in self.windows:
            if window.day_index == day_index:
                return window.available_minutes
        return 0

    def total_available_minutes(self) -> int:
        return sum(window.available_minutes for window in self.windows)

    def fingerprint(self) -> str:
        """Deterministic capacity fingerprint for plan identity."""
        parts = [
            f"{window.day_index}:{window.available_minutes}"
            for window in self.windows
        ]
        return "avail-" + "-".join(parts)
