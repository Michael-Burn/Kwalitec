"""Diagnostics — immutable Learning Orchestrator diagnostic reports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType

from app.application.learning_orchestrator.dto.execution_summary import (
    ExecutionSummary,
)
from app.application.learning_orchestrator.pipeline_engine import PipelineEngine
from app.application.learning_orchestrator.policies.orchestration_policy import (
    DEPENDENCY_CHAIN,
    OrchestrationPolicy,
)


@dataclass(frozen=True)
class DiagnosticReport:
    """Immutable diagnostic snapshot of the Learning Orchestrator."""

    orchestrator_version: str
    generated_at: str
    registered_ports: tuple[str, ...]
    missing_ports: tuple[str, ...]
    dependency_status: MappingProxyType
    event_readiness: MappingProxyType
    execution_timings: MappingProxyType
    canonical_pipeline: tuple[str, ...]
    recent_warnings: tuple[str, ...]
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "registered_ports", tuple(self.registered_ports)
        )
        object.__setattr__(self, "missing_ports", tuple(self.missing_ports))
        object.__setattr__(
            self, "canonical_pipeline", tuple(self.canonical_pipeline)
        )
        object.__setattr__(
            self, "recent_warnings", tuple(self.recent_warnings)
        )
        if not isinstance(self.dependency_status, MappingProxyType):
            object.__setattr__(
                self,
                "dependency_status",
                MappingProxyType(dict(self.dependency_status)),
            )
        if not isinstance(self.event_readiness, MappingProxyType):
            object.__setattr__(
                self,
                "event_readiness",
                MappingProxyType(dict(self.event_readiness)),
            )
        if not isinstance(self.execution_timings, MappingProxyType):
            object.__setattr__(
                self,
                "execution_timings",
                MappingProxyType(dict(self.execution_timings)),
            )
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self, "metadata", MappingProxyType(dict(self.metadata))
            )


class Diagnostics:
    """Build immutable diagnostic reports (no mutation of composition)."""

    def __init__(
        self,
        *,
        engine: PipelineEngine,
        orchestrator_version: str,
        clock=None,
    ) -> None:
        self._engine = engine
        self._orchestrator_version = orchestrator_version
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._timings: dict[str, float] = {}
        self._warnings: list[str] = []

    def record_execution(self, summary: ExecutionSummary) -> None:
        """Record the latest duration for ``summary.event_type`` (in-memory)."""
        self._timings[summary.event_type] = float(summary.duration_ms)
        self._warnings.extend(summary.warnings)
        # Keep a bounded recent warning window for diagnostics.
        if len(self._warnings) > 50:
            self._warnings = self._warnings[-50:]

    def report(self) -> DiagnosticReport:
        """Produce an immutable diagnostic report."""
        deps = self._engine.dependency_status()
        registered = tuple(
            name
            for name, info in deps.items()
            if isinstance(info, dict) and info.get("bound")
        )
        missing = tuple(
            name
            for name in OrchestrationPolicy.port_names()
            if name not in registered
        )
        registered_set = set(registered)
        readiness = {
            event: OrchestrationPolicy.event_ready(
                event, registered=registered_set
            )
            for event in sorted(OrchestrationPolicy.known_event_types())
        }
        return DiagnosticReport(
            orchestrator_version=self._orchestrator_version,
            generated_at=self._clock().isoformat(),
            registered_ports=registered,
            missing_ports=missing,
            dependency_status=MappingProxyType(deps),
            event_readiness=MappingProxyType(readiness),
            execution_timings=MappingProxyType(dict(self._timings)),
            canonical_pipeline=DEPENDENCY_CHAIN,
            recent_warnings=tuple(self._warnings),
        )
