"""ExecutionProgress — step progress derived from completed steps only."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_execution.enums import StepOutcome
from application.education.mission_execution.errors import (
    MissionExecutionInvariantViolation,
)
from application.education.mission_generation.ids import MissionStepId


@dataclass(frozen=True, slots=True)
class ExecutionProgress:
    """Immutable progress view derived solely from completed / skipped steps.

    Completion percentage is computed from completed steps only — skipped
    steps do not count as progress toward completion.
    """

    total_steps: int
    completed_step_ids: tuple[MissionStepId, ...]
    skipped_step_ids: tuple[MissionStepId, ...]
    current_step_id: MissionStepId | None
    step_outcomes: tuple[tuple[MissionStepId, StepOutcome], ...]

    def __post_init__(self) -> None:
        if isinstance(self.total_steps, bool) or not isinstance(self.total_steps, int):
            raise MissionExecutionInvariantViolation(
                "total_steps must be an integer",
                invariant="ExecutionProgress.total_steps.type",
            )
        if self.total_steps < 0:
            raise MissionExecutionInvariantViolation(
                "total_steps must be >= 0",
                invariant="ExecutionProgress.total_steps.non_negative",
            )
        object.__setattr__(
            self, "completed_step_ids", tuple(self.completed_step_ids)
        )
        object.__setattr__(self, "skipped_step_ids", tuple(self.skipped_step_ids))
        object.__setattr__(self, "step_outcomes", tuple(self.step_outcomes))

    @property
    def completed_count(self) -> int:
        return len(self.completed_step_ids)

    @property
    def skipped_count(self) -> int:
        return len(self.skipped_step_ids)

    @property
    def completion_percentage(self) -> float:
        """Percentage of steps completed (0–100). Skipped steps excluded."""
        if self.total_steps == 0:
            return 100.0
        return round(100.0 * self.completed_count / self.total_steps, 4)

    @property
    def remaining_count(self) -> int:
        resolved = self.completed_count + self.skipped_count
        return max(0, self.total_steps - resolved)

    def is_fully_resolved(self) -> bool:
        return self.remaining_count == 0
