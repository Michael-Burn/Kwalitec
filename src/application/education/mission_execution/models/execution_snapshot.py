"""ExecutionSnapshot — immutable mirror of a MissionExecution."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.mission_execution.enums import ExecutionStatus
from application.education.mission_execution.errors import (
    MissionExecutionInvariantViolation,
)
from application.education.mission_execution.ids import ExecutionId
from application.education.mission_execution.models.confidence_record import (
    ConfidenceRecord,
)
from application.education.mission_execution.models.execution_metrics import (
    ExecutionMetrics,
)
from application.education.mission_execution.models.execution_progress import (
    ExecutionProgress,
)
from application.education.mission_execution.models.execution_summary import (
    ExecutionSummary,
)
from application.education.mission_execution.models.reflection_record import (
    ReflectionRecord,
)
from application.education.mission_generation.ids import MissionId, MissionPlanId
from application.education.mission_generation.models.mission import Mission


@dataclass(frozen=True, slots=True)
class ExecutionSnapshot:
    """Immutable, accurate capture of a MissionExecution.

    A snapshot is a read model. It does not re-execute or estimate —
    it faithfully mirrors execution state at the moment it was produced.
    """

    execution_id: ExecutionId
    mission_id: MissionId
    plan_id: MissionPlanId
    student_id: str
    status: ExecutionStatus
    mission: Mission
    progress: ExecutionProgress
    metrics: ExecutionMetrics
    summary: ExecutionSummary
    confidence_history: tuple[ConfidenceRecord, ...]
    reflection_history: tuple[ReflectionRecord, ...]
    started_at: datetime | None
    finished_at: datetime | None
    captured_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.execution_id, ExecutionId):
            raise MissionExecutionInvariantViolation(
                "execution_id must be an ExecutionId",
                invariant="ExecutionSnapshot.execution_id.type",
            )
        if not isinstance(self.mission_id, MissionId):
            raise MissionExecutionInvariantViolation(
                "mission_id must be a MissionId",
                invariant="ExecutionSnapshot.mission_id.type",
            )
        if not isinstance(self.plan_id, MissionPlanId):
            raise MissionExecutionInvariantViolation(
                "plan_id must be a MissionPlanId",
                invariant="ExecutionSnapshot.plan_id.type",
            )
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise MissionExecutionInvariantViolation(
                "student_id must be a non-empty string",
                invariant="ExecutionSnapshot.student_id.required",
            )
        object.__setattr__(self, "student_id", student_id)
        if not isinstance(self.status, ExecutionStatus):
            raise MissionExecutionInvariantViolation(
                "status must be an ExecutionStatus",
                invariant="ExecutionSnapshot.status.type",
            )
        if not isinstance(self.mission, Mission):
            raise MissionExecutionInvariantViolation(
                "mission must be a Mission",
                invariant="ExecutionSnapshot.mission.type",
            )
        if not isinstance(self.progress, ExecutionProgress):
            raise MissionExecutionInvariantViolation(
                "progress must be an ExecutionProgress",
                invariant="ExecutionSnapshot.progress.type",
            )
        if not isinstance(self.metrics, ExecutionMetrics):
            raise MissionExecutionInvariantViolation(
                "metrics must be an ExecutionMetrics",
                invariant="ExecutionSnapshot.metrics.type",
            )
        if not isinstance(self.summary, ExecutionSummary):
            raise MissionExecutionInvariantViolation(
                "summary must be an ExecutionSummary",
                invariant="ExecutionSnapshot.summary.type",
            )
        if not isinstance(self.captured_at, datetime):
            raise MissionExecutionInvariantViolation(
                "captured_at must be a datetime",
                invariant="ExecutionSnapshot.captured_at.type",
            )
        object.__setattr__(
            self, "confidence_history", tuple(self.confidence_history)
        )
        object.__setattr__(
            self, "reflection_history", tuple(self.reflection_history)
        )
