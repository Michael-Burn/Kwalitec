"""Stateless validation rules for the Educational Composition Layer.

Ensures registration integrity and workflow readiness. No educational logic.
"""

from __future__ import annotations

from app.application.education_platform.exceptions import ValidationError
from app.application.education_platform.policies.orchestration_policy import (
    ALL_WORKFLOWS,
    DEPENDENCY_CHAIN,
    OrchestrationPolicy,
)


class ValidationPolicy:
    """Composition integrity rules (stateless)."""

    REQUIRED_PORTS: tuple[str, ...] = DEPENDENCY_CHAIN

    @staticmethod
    def assert_port_name(name: str) -> None:
        """Raise when ``name`` is not a known Educational Core port."""
        if name not in DEPENDENCY_CHAIN:
            raise ValidationError(
                f"Unknown port name: {name!r}; "
                f"expected one of {DEPENDENCY_CHAIN}"
            )

    @staticmethod
    def assert_no_duplicate(
        name: str,
        *,
        registered: frozenset[str] | set[str],
        allow_replace: bool = False,
    ) -> None:
        """Raise when registering a port that is already present.

        Args:
            name: Port name being registered.
            registered: Currently registered port names.
            allow_replace: When True, duplicates are permitted (replace path).
        """
        if not allow_replace and name in registered:
            raise ValidationError(f"Duplicate port registration: {name!r}")

    @staticmethod
    def assert_required_ports_present(
        registered: frozenset[str] | set[str],
        *,
        required: tuple[str, ...] | None = None,
    ) -> None:
        """Raise when any required port is missing from ``registered``."""
        need = required if required is not None else ValidationPolicy.REQUIRED_PORTS
        missing = tuple(p for p in need if p not in registered)
        if missing:
            raise ValidationError(
                f"Missing required ports: {missing}"
            )

    @staticmethod
    def assert_workflow_known(workflow: str) -> None:
        """Raise when ``workflow`` is not a supported platform workflow."""
        if workflow not in ALL_WORKFLOWS:
            raise ValidationError(f"Unknown workflow: {workflow!r}")

    @staticmethod
    def assert_workflow_ready(
        workflow: str,
        *,
        registered: frozenset[str] | set[str],
    ) -> None:
        """Raise when ``workflow`` cannot run under current registrations."""
        ValidationPolicy.assert_workflow_known(workflow)
        if not OrchestrationPolicy.workflow_ready(
            workflow, registered=registered
        ):
            required = OrchestrationPolicy.required_ports(workflow)
            missing = tuple(sorted(required - set(registered)))
            raise ValidationError(
                f"Workflow {workflow!r} not ready; missing ports: {missing}"
            )

    @staticmethod
    def assert_composition_integrity(
        registered: frozenset[str] | set[str],
        *,
        available: dict[str, bool] | None = None,
    ) -> tuple[str, ...]:
        """Validate full composition; return issue messages (empty if ok).

        When ``strict`` failures are needed, callers should raise on non-empty
        issues. This method itself raises only for structural impossibilities
        (unknown names in ``available``).
        """
        issues: list[str] = []
        for name in registered:
            if name not in DEPENDENCY_CHAIN:
                issues.append(f"unknown_registered_port:{name}")
        for name in ValidationPolicy.REQUIRED_PORTS:
            if name not in registered:
                issues.append(f"missing_port:{name}")
        if available is not None:
            for name, is_up in available.items():
                if name not in DEPENDENCY_CHAIN:
                    raise ValidationError(
                        f"Unknown port in availability map: {name!r}"
                    )
                if name in registered and not is_up:
                    issues.append(f"port_unavailable:{name}")
        for workflow in sorted(ALL_WORKFLOWS):
            if not OrchestrationPolicy.workflow_ready(
                workflow, registered=registered
            ):
                # validate_platform itself needs no ports
                if OrchestrationPolicy.required_ports(workflow):
                    issues.append(f"workflow_not_ready:{workflow}")
        return tuple(issues)

    @staticmethod
    def missing_ports(
        registered: frozenset[str] | set[str],
        *,
        required: tuple[str, ...] | None = None,
    ) -> tuple[str, ...]:
        """Return required ports absent from ``registered`` (stable order)."""
        need = required if required is not None else ValidationPolicy.REQUIRED_PORTS
        return tuple(p for p in need if p not in registered)
