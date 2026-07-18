"""Immutable OrchestrationResponse — output of every orchestrator run."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from app.application.learning_orchestrator.dto.execution_summary import (
    ExecutionSummary,
)
from app.application.learning_orchestrator.dto.pipeline_snapshot import (
    PipelineSnapshot,
)


@dataclass(frozen=True)
class OrchestrationResponse:
    """Unified response envelope for Learning Orchestrator executions.

    Carries structural stage outcomes only. Never invents educational
    content or mastery conclusions.
    """

    orchestration_id: str
    event_id: str
    learner_id: str
    event_type: str
    success: bool
    state: str
    pipeline_snapshots: tuple[PipelineSnapshot, ...] = ()
    execution_summary: ExecutionSummary | None = None
    warnings: tuple[str, ...] = ()
    error: str | None = None
    correlation_id: str | None = None
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "pipeline_snapshots", tuple(self.pipeline_snapshots)
        )
        object.__setattr__(self, "warnings", tuple(self.warnings))
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self, "metadata", MappingProxyType(dict(self.metadata))
            )

    @property
    def executed_stages(self) -> tuple[str, ...]:
        """Stage names that produced a non-skipped snapshot."""
        return tuple(
            s.stage for s in self.pipeline_snapshots if s.outcome != "skipped"
        )

    @property
    def failed_stages(self) -> tuple[str, ...]:
        """Stage names that reported failure."""
        return tuple(
            s.stage for s in self.pipeline_snapshots if s.outcome == "failure"
        )
