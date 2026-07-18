"""Immutable ExecutionSummary — observability report for one run."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from app.application.learning_orchestrator.dto.pipeline_snapshot import (
    PipelineSnapshot,
)
from app.domain.learning_orchestrator.orchestration_result import (
    OrchestrationResult,
)


@dataclass(frozen=True)
class ExecutionSummary:
    """Immutable execution report for observability and regression.

    Includes executed stages, duration, pipeline diagnostics, dependency
    status, and warnings. Never mutates educational state.
    """

    orchestration_id: str
    event_id: str
    learner_id: str
    event_type: str
    state: str
    success: bool
    executed_stages: tuple[str, ...]
    duration_ms: float
    stage_timings_ms: MappingProxyType
    pipeline_diagnostics: tuple[PipelineSnapshot, ...]
    dependency_status: MappingProxyType
    warnings: tuple[str, ...]
    error: str | None = None
    failed_stages: tuple[str, ...] = ()
    skipped_stages: tuple[str, ...] = ()
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "executed_stages", tuple(self.executed_stages)
        )
        object.__setattr__(
            self, "pipeline_diagnostics", tuple(self.pipeline_diagnostics)
        )
        object.__setattr__(self, "warnings", tuple(self.warnings))
        object.__setattr__(self, "failed_stages", tuple(self.failed_stages))
        object.__setattr__(
            self, "skipped_stages", tuple(self.skipped_stages)
        )
        if not isinstance(self.stage_timings_ms, MappingProxyType):
            object.__setattr__(
                self,
                "stage_timings_ms",
                MappingProxyType(dict(self.stage_timings_ms)),
            )
        if not isinstance(self.dependency_status, MappingProxyType):
            object.__setattr__(
                self,
                "dependency_status",
                MappingProxyType(dict(self.dependency_status)),
            )

    @classmethod
    def from_result(
        cls,
        result: OrchestrationResult,
        *,
        dependency_status: dict[str, object] | MappingProxyType | None = None,
        pipeline_snapshots: tuple[PipelineSnapshot, ...] | None = None,
    ) -> ExecutionSummary:
        """Build an execution summary from a domain orchestration result."""
        snapshots = pipeline_snapshots or tuple(
            PipelineSnapshot.from_result(r) for r in result.stage_results
        )
        timings = {r.stage.value: r.duration_ms for r in result.stage_results}
        deps = dependency_status or {}
        return cls(
            orchestration_id=result.orchestration_id,
            event_id=result.event_id,
            learner_id=result.learner_id,
            event_type=result.event_type,
            state=result.state.value,
            success=result.success,
            executed_stages=tuple(s.value for s in result.executed_stages),
            duration_ms=result.duration_ms,
            stage_timings_ms=MappingProxyType(timings),
            pipeline_diagnostics=snapshots,
            dependency_status=MappingProxyType(dict(deps)),
            warnings=result.warnings,
            error=result.error,
            failed_stages=tuple(s.value for s in result.failed_stages),
            skipped_stages=tuple(s.value for s in result.skipped_stages),
            correlation_id=result.correlation_id,
        )
