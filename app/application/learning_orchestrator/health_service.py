"""Health service — read-only Learning Orchestrator health reports.

Reports bound ports, availability, event readiness, and version.
Never mutates port bindings or educational state.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType

from app.application.learning_orchestrator.pipeline_engine import PipelineEngine
from app.application.learning_orchestrator.policies.orchestration_policy import (
    PORT_NAMES,
    OrchestrationPolicy,
)


class HealthService:
    """Observe orchestrator health without mutating composition."""

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

    def status(self) -> dict[str, object]:
        """Return a read-only health payload."""
        deps = self._engine.dependency_status()
        registered = {
            name
            for name, info in deps.items()
            if isinstance(info, dict) and info.get("bound")
        }
        readiness = {
            event: OrchestrationPolicy.event_ready(
                event, registered=registered
            )
            for event in sorted(OrchestrationPolicy.known_event_types())
        }
        components = MappingProxyType(deps)
        missing = tuple(n for n in PORT_NAMES if n not in registered)
        unavailable = tuple(
            name
            for name, info in deps.items()
            if isinstance(info, dict)
            and info.get("bound")
            and not info.get("available")
        )
        if not missing and not unavailable:
            orchestrator_status = "healthy"
        elif missing:
            orchestrator_status = "degraded"
        else:
            orchestrator_status = "unhealthy"

        return {
            "orchestrator_version": self._orchestrator_version,
            "orchestrator_status": orchestrator_status,
            "observed_at": self._clock().isoformat(),
            "registered_components": tuple(
                n for n in PORT_NAMES if n in registered
            ),
            "missing_dependencies": missing,
            "unavailable_dependencies": unavailable,
            "components": components,
            "event_readiness": MappingProxyType(readiness),
            "all_events_ready": all(readiness.values()),
            "dependency_chain": OrchestrationPolicy.dependency_chain(),
        }
