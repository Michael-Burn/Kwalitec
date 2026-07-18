"""Diagnostics — immutable Educational Composition diagnostic reports."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from types import MappingProxyType

from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.dto.workflow_result import WorkflowResult
from app.application.education_platform.platform_context import PlatformContext
from app.application.education_platform.platform_validator import (
    PlatformValidationResult,
    PlatformValidator,
)
from app.application.education_platform.policies.orchestration_policy import (
    DEPENDENCY_CHAIN,
)


@dataclass(frozen=True)
class DiagnosticReport:
    """Immutable diagnostic snapshot of the composed platform."""

    platform_version: str
    generated_at: str
    registered_engines: tuple[str, ...]
    missing_ports: tuple[str, ...]
    dependency_graph: tuple[tuple[str, str], ...]
    component_versions: MappingProxyType
    validation_passed: bool
    validation_issues: tuple[str, ...]
    workflow_readiness: MappingProxyType
    workflow_timings: MappingProxyType
    canonical_chain: tuple[str, ...]
    metadata: MappingProxyType | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "registered_engines", tuple(self.registered_engines)
        )
        object.__setattr__(self, "missing_ports", tuple(self.missing_ports))
        object.__setattr__(
            self, "dependency_graph", tuple(self.dependency_graph)
        )
        object.__setattr__(
            self, "validation_issues", tuple(self.validation_issues)
        )
        object.__setattr__(self, "canonical_chain", tuple(self.canonical_chain))
        if not isinstance(self.component_versions, MappingProxyType):
            object.__setattr__(
                self,
                "component_versions",
                MappingProxyType(dict(self.component_versions)),
            )
        if not isinstance(self.workflow_readiness, MappingProxyType):
            object.__setattr__(
                self,
                "workflow_readiness",
                MappingProxyType(dict(self.workflow_readiness)),
            )
        if not isinstance(self.workflow_timings, MappingProxyType):
            object.__setattr__(
                self,
                "workflow_timings",
                MappingProxyType(dict(self.workflow_timings)),
            )
        if self.metadata is None:
            object.__setattr__(self, "metadata", MappingProxyType({}))
        elif not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self,
                "metadata",
                MappingProxyType(dict(self.metadata)),
            )


class Diagnostics:
    """Build immutable diagnostic reports (no mutation of composition)."""

    def __init__(
        self,
        *,
        registry: DependencyRegistry,
        platform_version: str,
        validator: PlatformValidator | None = None,
        clock=None,
    ) -> None:
        self._registry = registry
        self._platform_version = platform_version
        self._validator = validator or PlatformValidator()
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._timings: dict[str, float] = {}

    def record_workflow_timing(self, result: WorkflowResult) -> None:
        """Record the latest duration for ``result.workflow`` (in-memory)."""
        self._timings[result.workflow] = float(result.duration_ms)

    def report(
        self,
        *,
        validation: PlatformValidationResult | None = None,
    ) -> DiagnosticReport:
        """Produce an immutable diagnostic report."""
        ctx = PlatformContext.from_registry(
            self._registry, platform_version=self._platform_version
        )
        validation = validation or self._validator.validate(self._registry)
        return DiagnosticReport(
            platform_version=self._platform_version,
            generated_at=self._clock().isoformat(),
            registered_engines=ctx.registered_ports,
            missing_ports=ctx.missing_ports,
            dependency_graph=ctx.dependency_graph,
            component_versions=ctx.component_versions,
            validation_passed=validation.passed,
            validation_issues=validation.issues,
            workflow_readiness=validation.workflow_readiness,
            workflow_timings=MappingProxyType(dict(self._timings)),
            canonical_chain=DEPENDENCY_CHAIN,
        )
