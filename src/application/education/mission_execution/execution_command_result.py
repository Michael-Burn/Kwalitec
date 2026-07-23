"""Command result DTO for MissionExecutionEngine operations."""

from __future__ import annotations

from dataclasses import dataclass

from application.education.mission_execution.errors import MissionExecutionError
from application.education.mission_execution.events import MissionExecutionEvent
from application.education.mission_execution.models.execution_snapshot import (
    ExecutionSnapshot,
)
from application.education.mission_execution.models.mission_execution import (
    MissionExecution,
)
from domain.education.educational_evidence.aggregates.educational_evidence import (
    EducationalEvidence,
)


@dataclass(frozen=True, slots=True)
class ExecutionCommandResult:
    """Outcome of a MissionExecutionEngine command.

    Expected lifecycle / state violations set ``ok=False`` and populate
    ``error`` — they are never raised as exceptions.
    """

    ok: bool
    execution: MissionExecution | None = None
    events: tuple[MissionExecutionEvent, ...] = ()
    evidence: tuple[EducationalEvidence, ...] = ()
    snapshot: ExecutionSnapshot | None = None
    error: MissionExecutionError | None = None

    @classmethod
    def success(
        cls,
        execution: MissionExecution,
        *,
        events: tuple[MissionExecutionEvent, ...] = (),
        evidence: tuple[EducationalEvidence, ...] = (),
        snapshot: ExecutionSnapshot | None = None,
    ) -> ExecutionCommandResult:
        return cls(
            ok=True,
            execution=execution,
            events=events,
            evidence=evidence,
            snapshot=snapshot,
        )

    @classmethod
    def failure(cls, error: MissionExecutionError) -> ExecutionCommandResult:
        return cls(ok=False, error=error)
