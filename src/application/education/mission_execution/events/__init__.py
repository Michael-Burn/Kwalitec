"""Immutable mission execution events (application objects, not persistence)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from application.education.mission_execution.enums import (
    ExecutionEventKind,
    ExecutionStatus,
)
from application.education.mission_execution.errors import (
    MissionExecutionInvariantViolation,
)
from application.education.mission_execution.ids import ExecutionId
from application.education.mission_generation.ids import MissionId, MissionStepId
from domain.education.foundation.enums import ConfidenceLevel


def _validate_common(
    *,
    kind: ExecutionEventKind,
    execution_id: ExecutionId,
    mission_id: MissionId,
    student_id: str,
    occurred_at: datetime,
    sequence: int,
    status_after: ExecutionStatus,
) -> str:
    if not isinstance(kind, ExecutionEventKind):
        raise MissionExecutionInvariantViolation(
            "kind must be an ExecutionEventKind",
            invariant="MissionExecutionEvent.kind.type",
        )
    if not isinstance(execution_id, ExecutionId):
        raise MissionExecutionInvariantViolation(
            "execution_id must be an ExecutionId",
            invariant="MissionExecutionEvent.execution_id.type",
        )
    if not isinstance(mission_id, MissionId):
        raise MissionExecutionInvariantViolation(
            "mission_id must be a MissionId",
            invariant="MissionExecutionEvent.mission_id.type",
        )
    cleaned = (student_id or "").strip()
    if not cleaned:
        raise MissionExecutionInvariantViolation(
            "student_id must be non-empty",
            invariant="MissionExecutionEvent.student_id.required",
        )
    if not isinstance(occurred_at, datetime):
        raise MissionExecutionInvariantViolation(
            "occurred_at must be a datetime",
            invariant="MissionExecutionEvent.occurred_at.type",
        )
    if isinstance(sequence, bool) or not isinstance(sequence, int):
        raise MissionExecutionInvariantViolation(
            "sequence must be an integer",
            invariant="MissionExecutionEvent.sequence.type",
        )
    if sequence < 1:
        raise MissionExecutionInvariantViolation(
            "sequence must be >= 1",
            invariant="MissionExecutionEvent.sequence.positive",
        )
    if not isinstance(status_after, ExecutionStatus):
        raise MissionExecutionInvariantViolation(
            "status_after must be an ExecutionStatus",
            invariant="MissionExecutionEvent.status_after.type",
        )
    return cleaned


@dataclass(frozen=True, slots=True)
class MissionStarted:
    """Mission execution transitioned PLANNED → STARTED."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    occurred_at: datetime
    sequence: int
    kind: ExecutionEventKind = ExecutionEventKind.MISSION_STARTED
    status_after: ExecutionStatus = ExecutionStatus.STARTED

    def __post_init__(self) -> None:
        cleaned = _validate_common(
            kind=self.kind,
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id,
            occurred_at=self.occurred_at,
            sequence=self.sequence,
            status_after=self.status_after,
        )
        object.__setattr__(self, "student_id", cleaned)
        if self.kind is not ExecutionEventKind.MISSION_STARTED:
            raise MissionExecutionInvariantViolation(
                "MissionStarted.kind must be MISSION_STARTED",
                invariant="MissionStarted.kind.fixed",
            )


@dataclass(frozen=True, slots=True)
class MissionPaused:
    """Mission execution transitioned to PAUSED."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    occurred_at: datetime
    sequence: int
    kind: ExecutionEventKind = ExecutionEventKind.MISSION_PAUSED
    status_after: ExecutionStatus = ExecutionStatus.PAUSED

    def __post_init__(self) -> None:
        cleaned = _validate_common(
            kind=self.kind,
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id,
            occurred_at=self.occurred_at,
            sequence=self.sequence,
            status_after=self.status_after,
        )
        object.__setattr__(self, "student_id", cleaned)


@dataclass(frozen=True, slots=True)
class MissionResumed:
    """Mission execution transitioned PAUSED → RESUMED."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    occurred_at: datetime
    sequence: int
    kind: ExecutionEventKind = ExecutionEventKind.MISSION_RESUMED
    status_after: ExecutionStatus = ExecutionStatus.RESUMED

    def __post_init__(self) -> None:
        cleaned = _validate_common(
            kind=self.kind,
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id,
            occurred_at=self.occurred_at,
            sequence=self.sequence,
            status_after=self.status_after,
        )
        object.__setattr__(self, "student_id", cleaned)


@dataclass(frozen=True, slots=True)
class StepCompleted:
    """A mission step was completed."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    occurred_at: datetime
    sequence: int
    status_after: ExecutionStatus
    step_id: MissionStepId
    kind: ExecutionEventKind = ExecutionEventKind.STEP_COMPLETED

    def __post_init__(self) -> None:
        cleaned = _validate_common(
            kind=self.kind,
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id,
            occurred_at=self.occurred_at,
            sequence=self.sequence,
            status_after=self.status_after,
        )
        object.__setattr__(self, "student_id", cleaned)
        if not isinstance(self.step_id, MissionStepId):
            raise MissionExecutionInvariantViolation(
                "step_id must be a MissionStepId",
                invariant="StepCompleted.step_id.type",
            )


@dataclass(frozen=True, slots=True)
class StepSkipped:
    """A mission step was skipped."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    occurred_at: datetime
    sequence: int
    status_after: ExecutionStatus
    step_id: MissionStepId
    kind: ExecutionEventKind = ExecutionEventKind.STEP_SKIPPED

    def __post_init__(self) -> None:
        cleaned = _validate_common(
            kind=self.kind,
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id,
            occurred_at=self.occurred_at,
            sequence=self.sequence,
            status_after=self.status_after,
        )
        object.__setattr__(self, "student_id", cleaned)
        if not isinstance(self.step_id, MissionStepId):
            raise MissionExecutionInvariantViolation(
                "step_id must be a MissionStepId",
                invariant="StepSkipped.step_id.type",
            )


@dataclass(frozen=True, slots=True)
class ConfidenceRecorded:
    """Student confidence was recorded during execution."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    occurred_at: datetime
    sequence: int
    status_after: ExecutionStatus
    level: ConfidenceLevel
    step_id: MissionStepId | None = None
    kind: ExecutionEventKind = ExecutionEventKind.CONFIDENCE_RECORDED

    def __post_init__(self) -> None:
        cleaned = _validate_common(
            kind=self.kind,
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id,
            occurred_at=self.occurred_at,
            sequence=self.sequence,
            status_after=self.status_after,
        )
        object.__setattr__(self, "student_id", cleaned)
        if not isinstance(self.level, ConfidenceLevel):
            raise MissionExecutionInvariantViolation(
                "level must be a ConfidenceLevel",
                invariant="ConfidenceRecorded.level.type",
            )


@dataclass(frozen=True, slots=True)
class ReflectionRecorded:
    """Student reflection was recorded during execution."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    occurred_at: datetime
    sequence: int
    status_after: ExecutionStatus
    text: str
    step_id: MissionStepId | None = None
    kind: ExecutionEventKind = ExecutionEventKind.REFLECTION_RECORDED

    def __post_init__(self) -> None:
        cleaned = _validate_common(
            kind=self.kind,
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id,
            occurred_at=self.occurred_at,
            sequence=self.sequence,
            status_after=self.status_after,
        )
        object.__setattr__(self, "student_id", cleaned)
        text = (self.text or "").strip()
        if not text:
            raise MissionExecutionInvariantViolation(
                "reflection text must be non-empty",
                invariant="ReflectionRecorded.text.required",
            )
        object.__setattr__(self, "text", text)


@dataclass(frozen=True, slots=True)
class MissionCompleted:
    """Mission execution reached COMPLETED."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    occurred_at: datetime
    sequence: int
    kind: ExecutionEventKind = ExecutionEventKind.MISSION_COMPLETED
    status_after: ExecutionStatus = ExecutionStatus.COMPLETED

    def __post_init__(self) -> None:
        cleaned = _validate_common(
            kind=self.kind,
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id,
            occurred_at=self.occurred_at,
            sequence=self.sequence,
            status_after=self.status_after,
        )
        object.__setattr__(self, "student_id", cleaned)


@dataclass(frozen=True, slots=True)
class MissionAbandoned:
    """Mission execution reached ABANDONED."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    occurred_at: datetime
    sequence: int
    kind: ExecutionEventKind = ExecutionEventKind.MISSION_ABANDONED
    status_after: ExecutionStatus = ExecutionStatus.ABANDONED

    def __post_init__(self) -> None:
        cleaned = _validate_common(
            kind=self.kind,
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id,
            occurred_at=self.occurred_at,
            sequence=self.sequence,
            status_after=self.status_after,
        )
        object.__setattr__(self, "student_id", cleaned)


@dataclass(frozen=True, slots=True)
class MissionExpired:
    """Mission execution reached EXPIRED."""

    execution_id: ExecutionId
    mission_id: MissionId
    student_id: str
    occurred_at: datetime
    sequence: int
    kind: ExecutionEventKind = ExecutionEventKind.MISSION_EXPIRED
    status_after: ExecutionStatus = ExecutionStatus.EXPIRED

    def __post_init__(self) -> None:
        cleaned = _validate_common(
            kind=self.kind,
            execution_id=self.execution_id,
            mission_id=self.mission_id,
            student_id=self.student_id,
            occurred_at=self.occurred_at,
            sequence=self.sequence,
            status_after=self.status_after,
        )
        object.__setattr__(self, "student_id", cleaned)


MissionExecutionEvent = (
    MissionStarted
    | MissionPaused
    | MissionResumed
    | StepCompleted
    | StepSkipped
    | ConfidenceRecorded
    | ReflectionRecorded
    | MissionCompleted
    | MissionAbandoned
    | MissionExpired
)
