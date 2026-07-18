"""Health service — read-only Educational Composition health reports.

Reports registered components, missing dependencies, workflow readiness,
platform status, and version information. Never mutates the registry.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import MappingProxyType

from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.platform_context import PlatformContext
from app.application.education_platform.policies.orchestration_policy import (
    ALL_WORKFLOWS,
    OrchestrationPolicy,
)


class HealthService:
    """Observe platform health without mutating composition."""

    def __init__(
        self,
        *,
        registry: DependencyRegistry,
        platform_version: str,
        clock=None,
    ) -> None:
        self._registry = registry
        self._platform_version = platform_version
        self._clock = clock or (lambda: datetime.now(tz=UTC))

    def status(self) -> dict[str, object]:
        """Return a read-only health payload."""
        ctx = PlatformContext.from_registry(
            self._registry, platform_version=self._platform_version
        )
        registered = set(ctx.registered_ports)
        components: dict[str, dict[str, object]] = {}
        for name in ctx.registered_ports:
            port = self._registry.get(name)
            available = True
            probe = getattr(port, "is_available", None)
            if callable(probe):
                available = bool(probe())
            components[name] = {
                "component_id": getattr(port, "component_id", name),
                "component_version": ctx.component_versions.get(name, "unknown"),
                "available": available,
            }
        readiness = {
            wf: OrchestrationPolicy.workflow_ready(wf, registered=registered)
            for wf in sorted(ALL_WORKFLOWS)
        }
        all_ready = all(readiness.values())
        missing = ctx.missing_ports
        if not missing and all(
            c["available"] for c in components.values()
        ):
            platform_status = "healthy"
        elif missing:
            platform_status = "degraded"
        else:
            platform_status = "unhealthy"

        return {
            "platform_version": self._platform_version,
            "platform_status": platform_status,
            "observed_at": self._clock().isoformat(),
            "registered_components": tuple(ctx.registered_ports),
            "missing_dependencies": missing,
            "components": MappingProxyType(components),
            "workflow_readiness": MappingProxyType(readiness),
            "all_workflows_ready": all_ready,
            "dependency_graph": ctx.dependency_graph,
            "component_versions": ctx.component_versions,
        }
