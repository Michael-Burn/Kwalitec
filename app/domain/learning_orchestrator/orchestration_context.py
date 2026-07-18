"""Immutable execution context carried through the orchestration pipeline."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from types import MappingProxyType

from app.domain.learning_orchestrator.orchestration_event import (
    OrchestrationEvent,
)
from app.domain.learning_orchestrator.orchestration_state import (
    OrchestrationState,
)
from app.domain.learning_orchestrator.pipeline_result import PipelineResult
from app.domain.learning_orchestrator.pipeline_stage import PipelineStageName


@dataclass(frozen=True)
class OrchestrationContext:
    """Accumulated coordination context for one orchestration run.

    Carries event identity, lifecycle state, and prior stage payloads.
    Never mutates Twin, curriculum, or educational aggregates — only
    records opaque structural payloads returned by ports.
    """

    event: OrchestrationEvent
    orchestration_id: str
    state: OrchestrationState
    started_at: datetime
    stage_results: tuple[PipelineResult, ...] = ()
    stage_payloads: MappingProxyType | None = None
    warnings: tuple[str, ...] = ()
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "stage_results", tuple(self.stage_results))
        object.__setattr__(self, "warnings", tuple(self.warnings))
        if self.stage_payloads is None:
            object.__setattr__(self, "stage_payloads", MappingProxyType({}))
        elif not isinstance(self.stage_payloads, MappingProxyType):
            object.__setattr__(
                self,
                "stage_payloads",
                MappingProxyType(dict(self.stage_payloads)),
            )
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self, "metadata", MappingProxyType(dict(self.metadata))
            )

    @property
    def learner_id(self) -> str:
        """Learner identity from the source event."""
        return self.event.learner_id

    @property
    def executed_stages(self) -> tuple[PipelineStageName, ...]:
        """Stages that produced a non-skipped result."""
        return tuple(
            r.stage for r in self.stage_results if not r.skipped
        )

    def payload_for(self, stage: PipelineStageName) -> MappingProxyType:
        """Return the opaque payload recorded for ``stage`` (may be empty)."""
        raw = self.stage_payloads.get(stage.value, {})  # type: ignore[union-attr]
        if isinstance(raw, MappingProxyType):
            return raw
        return MappingProxyType(dict(raw) if raw else {})

    def with_state(self, state: OrchestrationState) -> OrchestrationContext:
        """Return a copy with updated lifecycle state."""
        return replace(self, state=state)

    def with_result(self, result: PipelineResult) -> OrchestrationContext:
        """Return a copy appending ``result`` and merging its payload."""
        payloads = dict(self.stage_payloads or {})
        payloads[result.stage.value] = dict(result.payload or {})
        warnings = self.warnings + result.warnings
        return replace(
            self,
            stage_results=self.stage_results + (result,),
            stage_payloads=MappingProxyType(payloads),
            warnings=warnings,
        )

    def with_warning(self, warning: str) -> OrchestrationContext:
        """Return a copy with an additional orchestration-level warning."""
        return replace(self, warnings=self.warnings + (warning,))
