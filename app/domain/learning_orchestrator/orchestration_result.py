"""Immutable final result of an orchestration execution."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from app.domain.learning_orchestrator.orchestration_state import (
    OrchestrationState,
)
from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName


@dataclass(frozen=True)
class OrchestrationResult:
    """Terminal coordination outcome for one learner event.

    Reports executed stages, durations, diagnostics, and warnings.
    Does not recover or mutate educational state.
    """

    orchestration_id: str
    event_id: str
    learner_id: str
    event_type: str
    state: OrchestrationState
    success: bool
    stage_results: tuple[PipelineResult, ...] = ()
    executed_stages: tuple[PipelineStageName, ...] = ()
    duration_ms: float = 0.0
    warnings: tuple[str, ...] = ()
    error: str | None = None
    diagnostics: MappingProxyType | None = None
    correlation_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage_results", tuple(self.stage_results))
        object.__setattr__(
            self, "executed_stages", tuple(self.executed_stages)
        )
        object.__setattr__(self, "warnings", tuple(self.warnings))
        if self.diagnostics is None:
            object.__setattr__(self, "diagnostics", MappingProxyType({}))
        elif not isinstance(self.diagnostics, MappingProxyType):
            object.__setattr__(
                self,
                "diagnostics",
                MappingProxyType(dict(self.diagnostics)),
            )

    @property
    def failed_stages(self) -> tuple[PipelineStageName, ...]:
        """Stages that reported failure."""
        return tuple(r.stage for r in self.stage_results if r.failed)

    @property
    def skipped_stages(self) -> tuple[PipelineStageName, ...]:
        """Stages that were skipped."""
        return tuple(r.stage for r in self.stage_results if r.skipped)

    @classmethod
    def from_context(
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
        diagnostics: dict | MappingProxyType | None = None,
        correlation_id: str | None = None,
    ) -> OrchestrationResult:
        """Build a result from accumulated stage outcomes."""
        executed = tuple(r.stage for r in stage_results if not r.skipped)
        any_failure = any(r.failed for r in stage_results)
        all_success = stage_results and all(
            r.succeeded or r.skipped for r in stage_results
        )
        success = bool(all_success) and not any_failure and state in {
            OrchestrationState.COMPLETED,
            OrchestrationState.PARTIAL,
        }
        if state == OrchestrationState.FAILED:
            success = False
        elif state == OrchestrationState.COMPLETED and not any_failure:
            success = True
        elif state == OrchestrationState.PARTIAL:
            success = False
        return cls(
            orchestration_id=orchestration_id,
            event_id=event_id,
            learner_id=learner_id,
            event_type=event_type,
            state=state,
            success=success,
            stage_results=stage_results,
            executed_stages=executed,
            duration_ms=duration_ms,
            warnings=warnings,
            error=error,
            diagnostics=diagnostics,  # type: ignore[arg-type]
            correlation_id=correlation_id,
        )
