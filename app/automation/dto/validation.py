"""Validation cargo for the Automation Framework."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    """One explicit validation failure."""

    code: str
    message: str
    field: str | None = None


@dataclass(frozen=True)
class ValidationReport:
    """Aggregated validation outcome."""

    ok: bool
    issues: tuple[ValidationIssue, ...]

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return self.issues


class AutomationValidationError(ValueError):
    """Raised when framework or workflow validation fails hard."""

    def __init__(self, report: ValidationReport) -> None:
        self.report = report
        codes = ", ".join(issue.code for issue in report.issues) or "unknown"
        super().__init__(f"automation validation failed: {codes}")


class DuplicateWorkflowError(ValueError):
    """Raised when registering a workflow id that already exists."""

    def __init__(self, workflow_id: str) -> None:
        self.workflow_id = workflow_id
        super().__init__(
            f"automation workflow already registered: {workflow_id!r}"
        )


class UnknownWorkflowError(ValueError):
    """Raised when looking up a workflow id that is not registered."""

    def __init__(self, workflow_id: str) -> None:
        self.workflow_id = workflow_id
        super().__init__(f"unknown automation workflow: {workflow_id!r}")
