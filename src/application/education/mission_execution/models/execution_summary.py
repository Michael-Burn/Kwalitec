"""ExecutionSummary — compact read model of a MissionExecution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.mission_execution.enums import ExecutionStatus
from application.education.mission_execution.errors import (
    MissionExecutionInvariantViolation,
)
from application.education.mission_execution.ids import ExecutionId
from application.education.mission_generation.ids import MissionId


@dataclass(frozen=True, slots=True)
class ExecutionSummary:
    """Compact immutable summary of a MissionExecution."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    status: ExecutionStatus
    completed_steps: int
    skipped_steps: int
    total_steps: int
    completion_percentage: float
    elapsed_study_time_seconds: float
    reflection_count: int
    confidence_count: int
    started_at: datetime | None = None
    finished_at: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.execution_id, ExecutionId):
            raise MissionExecutionInvariantViolation(
                "execution_id must be an ExecutionId",
                invariant="ExecutionSummary.execution_id.type",
            )
        if not isinstance(self.mission_id, MissionId):
            raise MissionExecutionInvariantViolation(
                "mission_id must be a MissionId",
                invariant="ExecutionSummary.mission_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise MissionExecutionInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ExecutionSummary.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.status, ExecutionStatus):
            raise MissionExecutionInvariantViolation(
                "status must be an ExecutionStatus",
                invariant="ExecutionSummary.status.type",
            )

    def is_terminal(self) -> bool:
        return self.status in {
            ExecutionStatus.COMPLETED,
            ExecutionStatus.ABANDONED,
            ExecutionStatus.EXPIRED,
        }
