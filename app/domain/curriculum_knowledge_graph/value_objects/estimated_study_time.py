"""Estimated study effort in minutes (structural estimate, not mastery)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class EstimatedStudyTime:
    """Non-negative structural study-time estimate in minutes."""

    minutes: int

    def __post_init__(self) -> None:
        if not isinstance(self.minutes, int) or isinstance(self.minutes, bool):
            raise ValueError("EstimatedStudyTime.minutes must be an int")
        if self.minutes < 0:
            raise ValueError("EstimatedStudyTime.minutes must be non-negative")

    @classmethod
    def of(cls, minutes: int | EstimatedStudyTime) -> EstimatedStudyTime:
        """Coerce an int or EstimatedStudyTime."""
        if isinstance(minutes, EstimatedStudyTime):
            return minutes
        return cls(minutes)

    def __int__(self) -> int:
        return self.minutes
