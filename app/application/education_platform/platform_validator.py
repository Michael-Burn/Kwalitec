"""Platform validator — composition integrity checks.

Ensures required ports, no illegal duplicates (via registry), workflow
availability, and composition integrity. Never mutates registrations.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.exceptions import ValidationError
from app.application.education_platform.policies.orchestration_policy import (
    ALL_WORKFLOWS,
    OrchestrationPolicy,
)
from app.application.education_platform.policies.validation_policy import (
    ValidationPolicy,
)


@dataclass(frozen=True)
class PlatformValidationResult:
    """Immutable validation outcome."""

    passed: bool
    issues: tuple[str, ...]
    registered_ports: tuple[str, ...]
    missing_ports: tuple[str, ...]
    workflow_readiness: MappingProxyType

    def __post_init__(self) -> None:
        object.__setattr__(self, "issues", tuple(self.issues))
        object.__setattr__(
            self, "registered_ports", tuple(self.registered_ports)
        )
        object.__setattr__(self, "missing_ports", tuple(self.missing_ports))
        if not isinstance(self.workflow_readiness, MappingProxyType):
            object.__setattr__(
                self,
                "workflow_readiness",
                MappingProxyType(dict(self.workflow_readiness)),
            )


class PlatformValidator:
    """Validate Educational Composition integrity (no mutation)."""

    def validate(self, registry: DependencyRegistry) -> PlatformValidationResult:
        """Run full composition validation against ``registry``."""
        registered = set(registry.registered_names())
        available: dict[str, bool] = {}
        for name in registry.registered_names():
            port = registry.get(name)
            probe = getattr(port, "is_available", None)
            available[name] = bool(probe()) if callable(probe) else True
        issues = ValidationPolicy.assert_composition_integrity(
            registered, available=available
        )
        readiness = {
            wf: OrchestrationPolicy.workflow_ready(wf, registered=registered)
            for wf in sorted(ALL_WORKFLOWS)
        }
        return PlatformValidationResult(
            passed=len(issues) == 0,
            issues=issues,
            registered_ports=registry.registered_names(),
            missing_ports=registry.missing_names(),
            workflow_readiness=MappingProxyType(readiness),
        )

    def require_valid(self, registry: DependencyRegistry) -> PlatformValidationResult:
        """Validate and raise ``ValidationError`` when composition fails."""
        result = self.validate(registry)
        if not result.passed:
            raise ValidationError(
                f"Platform composition invalid: {result.issues}"
            )
        return result

    def require_workflow(
        self,
        registry: DependencyRegistry,
        workflow: str,
    ) -> None:
        """Raise when ``workflow`` is not ready under ``registry``."""
        registered = set(registry.registered_names())
        try:
            ValidationPolicy.assert_workflow_ready(
                workflow, registered=registered
            )
        except ValidationError:
            raise
        # Also ensure registered ports report available.
        for name in OrchestrationPolicy.required_ports(workflow):
            port = registry.get(name)
            probe = getattr(port, "is_available", None)
            if callable(probe) and not probe():
                raise ValidationError(f"Port unavailable for workflow: {name!r}")
