"""Immutable point-in-time projection of an orchestration execution."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from app.domain.learning_orchestrator.orchestration_result import (
    OrchestrationResult,
)
from app.domain.learning_orchestrator.orchestration_state import (
    OrchestrationState,
)
from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName


@dataclass(frozen=True)
class OrchestrationSnapshot:
    """Read-only projection for callers, health, and regression tests."""

    orchestration_id: str
    event_id: str
    learner_id: str
    event_type: str
    state: OrchestrationState
    success: bool
    executed_stages: tuple[str, ...]
    stage_outcomes: MappingProxyType
    duration_ms: float
    warnings: tuple[str, ...]
    error: str | None = None
    failed_stages: tuple[str, ...] = ()
    skipped_stages: tuple[str, ...] = ()
    correlation_id: str | None = None
    diagnostics: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "executed_stages", tuple(self.executed_stages)
        )
        object.__setattr__(self, "warnings", tuple(self.warnings))
        object.__setattr__(self, "failed_stages", tuple(self.failed_stages))
        object.__setattr__(
            self, "skipped_stages", tuple(self.skipped_stages)
        )
        if not isinstance(self.stage_outcomes, MappingProxyType):
            object.__setattr__(
                self,
                "stage_outcomes",
                MappingProxyType(dict(self.stage_outcomes)),
            )
        if self.diagnostics is None:
            object.__setattr__(self, "diagnostics", MappingProxyType({}))
        elif not isinstance(self.diagnostics, MappingProxyType):
            object.__setattr__(
                self,
                "diagnostics",
                MappingProxyType(dict(self.diagnostics)),
            )

    @classmethod
    def from_result(cls, result: OrchestrationResult) -> OrchestrationSnapshot:
        """Project an ``OrchestrationResult`` into a snapshot."""
        outcomes = {
            r.stage.value: r.outcome.value for r in result.stage_results
        }
        return cls(
            orchestration_id=result.orchestration_id,
            event_id=result.event_id,
            learner_id=result.learner_id,
            event_type=result.event_type,
            state=result.state,
            success=result.success,
            executed_stages=tuple(s.value for s in result.executed_stages),
            stage_outcomes=MappingProxyType(outcomes),
            duration_ms=result.duration_ms,
            warnings=result.warnings,
            error=result.error,
            failed_stages=tuple(s.value for s in result.failed_stages),
            skipped_stages=tuple(s.value for s in result.skipped_stages),
            correlation_id=result.correlation_id,
            diagnostics=result.diagnostics,
        )

    @classmethod
    def from_stages(
        cls,
        *,
        orchestration_id: str,
        event_id: str,
        learner_id: str,
        event_type: str,
        state: OrchestrationState,
        stage_results: tuple[PipelineResult, ...],
        duration_ms: float,
        warnings: tuple[str, ...] = (),
        error: str | None = None,
        correlation_id: str | None = None,
    ) -> OrchestrationSnapshot:
        """Build a snapshot directly from stage results."""
        executed: list[str] = []
        failed: list[str] = []
        skipped: list[str] = []
        outcomes: dict[str, str] = {}
        for result in stage_results:
            name = result.stage.value
            outcomes[name] = result.outcome.value
            if result.skipped:
                skipped.append(name)
            elif result.failed:
                failed.append(name)
                executed.append(name)
            else:
                executed.append(name)
        success = state == OrchestrationState.COMPLETED and not failed
        return cls(
            orchestration_id=orchestration_id,
            event_id=event_id,
            learner_id=learner_id,
            event_type=event_type,
            state=state,
            success=success,
            executed_stages=tuple(executed),
            stage_outcomes=MappingProxyType(outcomes),
            duration_ms=duration_ms,
            warnings=warnings,
            error=error,
            failed_stages=tuple(failed),
            skipped_stages=tuple(skipped),
            correlation_id=correlation_id,
        )

    def stage_outcome(self, stage: PipelineStageName | str) -> str | None:
        """Return the outcome token for ``stage``, if present."""
        key = stage.value if isinstance(stage, PipelineStageName) else stage
        return self.stage_outcomes.get(key)
