"""Episode progress — sequence advancement snapshot.

Architecture Source
    LEARNING_EPISODE_LIFECYCLE.md
Concept
    Episode Progress
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class EpisodeProgress(EducationalValueObject):
    """Immutable snapshot of how far an episode has advanced through steps."""

    current_index: int
    completed_steps: int
    total_steps: int
    completed_required_steps: int
    total_required_steps: int

    def _validate(self) -> None:
        for name, value in (
            ("current_index", self.current_index),
            ("completed_steps", self.completed_steps),
            ("total_steps", self.total_steps),
            ("completed_required_steps", self.completed_required_steps),
            ("total_required_steps", self.total_required_steps),
        ):
            if not isinstance(value, int):
                raise EducationalInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"EpisodeProgress.{name}.type",
                )
            if value < 0:
                raise EducationalInvariantViolation(
                    f"{name} must be non-negative",
                    invariant=f"EpisodeProgress.{name}.non_negative",
                )
        if self.total_steps < 1:
            raise EducationalInvariantViolation(
                "total_steps must be at least 1",
                invariant="EpisodeProgress.total_steps.min",
            )
        if self.completed_steps > self.total_steps:
            raise EducationalInvariantViolation(
                "completed_steps cannot exceed total_steps",
                invariant="EpisodeProgress.completed_steps.bounds",
            )
        if self.completed_required_steps > self.total_required_steps:
            raise EducationalInvariantViolation(
                "completed_required_steps cannot exceed total_required_steps",
                invariant="EpisodeProgress.completed_required.bounds",
            )
        if self.current_index > self.total_steps:
            raise EducationalInvariantViolation(
                "current_index cannot exceed total_steps",
                invariant="EpisodeProgress.current_index.bounds",
            )

    @property
    def required_sequence_complete(self) -> bool:
        """True when every required step is completed."""
        return (
            self.total_required_steps > 0
            and self.completed_required_steps >= self.total_required_steps
        )

    @property
    def all_steps_complete(self) -> bool:
        """True when every step (required and optional) is completed."""
        return self.completed_steps >= self.total_steps

    @property
    def ratio(self) -> float:
        """Fraction of total steps completed in [0, 1]."""
        if self.total_steps == 0:
            return 0.0
        return self.completed_steps / self.total_steps
