"""CompletionMetrics — recorded outcome of a completed study session."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.revision_planner.errors import ScheduleInvariantViolation


@dataclass(frozen=True, slots=True)
class CompletionMetrics:
    """Immutable completion figures for a finished StudySession."""

    actual_duration_minutes: int
    missions_completed: int = 0
    missions_partial: int = 0
    objectives_met: int = 0

    def __post_init__(self) -> None:
        if isinstance(self.actual_duration_minutes, bool) or not isinstance(
            self.actual_duration_minutes, int
        ):
            raise ScheduleInvariantViolation(
                "actual_duration_minutes must be an integer",
                invariant="CompletionMetrics.actual_duration_minutes.type",
            )
        if self.actual_duration_minutes < 0:
            raise ScheduleInvariantViolation(
                "actual_duration_minutes must be >= 0",
                invariant="CompletionMetrics.actual_duration_minutes.non_negative",
            )
        for name, value in (
            ("missions_completed", self.missions_completed),
            ("missions_partial", self.missions_partial),
            ("objectives_met", self.objectives_met),
        ):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ScheduleInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"CompletionMetrics.{name}.type",
                )
            if value < 0:
                raise ScheduleInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"CompletionMetrics.{name}.non_negative",
                )
