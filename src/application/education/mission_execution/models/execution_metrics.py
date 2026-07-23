"""ExecutionMetrics — deterministic runtime metrics for a mission run."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_execution.enums import ConfidenceTrend
from application.education.mission_execution.errors import (
    MissionExecutionInvariantViolation,
)


@dataclass(frozen=True, slots=True)
class ExecutionMetrics:
    """Immutable, deterministic metrics for a MissionExecution.

    All values are pure functions of recorded execution state — never
    estimated or randomised.
    """

    elapsed_study_time_seconds: float
    paused_duration_seconds: float
    mission_duration_seconds: float
    completion_percentage: float
    step_completion_rate: float
    skipped_steps: int
    reflection_count: int
    confidence_count: int
    confidence_trend: ConfidenceTrend

    def __post_init__(self) -> None:
        for name in (
            "elapsed_study_time_seconds",
            "paused_duration_seconds",
            "mission_duration_seconds",
            "completion_percentage",
            "step_completion_rate",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise MissionExecutionInvariantViolation(
                    f"{name} must be a real number",
                    invariant=f"ExecutionMetrics.{name}.type",
                )
            if float(value) < 0:
                raise MissionExecutionInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"ExecutionMetrics.{name}.non_negative",
                )
        for name in ("skipped_steps", "reflection_count", "confidence_count"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise MissionExecutionInvariantViolation(
                    f"{name} must be an integer",
                    invariant=f"ExecutionMetrics.{name}.type",
                )
            if value < 0:
                raise MissionExecutionInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"ExecutionMetrics.{name}.non_negative",
                )
        if not isinstance(self.confidence_trend, ConfidenceTrend):
            raise MissionExecutionInvariantViolation(
                "confidence_trend must be a ConfidenceTrend",
                invariant="ExecutionMetrics.confidence_trend.type",
            )
        object.__setattr__(
            self,
            "elapsed_study_time_seconds",
            round(float(self.elapsed_study_time_seconds), 4),
        )
        object.__setattr__(
            self,
            "paused_duration_seconds",
            round(float(self.paused_duration_seconds), 4),
        )
        object.__setattr__(
            self,
            "mission_duration_seconds",
            round(float(self.mission_duration_seconds), 4),
        )
        object.__setattr__(
            self,
            "completion_percentage",
            round(float(self.completion_percentage), 4),
        )
        object.__setattr__(
            self,
            "step_completion_rate",
            round(float(self.step_completion_rate), 4),
        )
