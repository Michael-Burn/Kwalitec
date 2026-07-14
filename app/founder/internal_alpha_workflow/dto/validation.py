"""Validation DTOs for Internal Alpha Live Workflow (FSI-003)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowValidationIssue:
    """One structural or stage validation finding."""

    code: str
    message: str
    path: str | None = None


@dataclass(frozen=True)
class WorkflowValidationReport:
    """Immutable validation report for week structure or workflow cargo."""

    ok: bool
    issues: tuple[WorkflowValidationIssue, ...] = ()


class WorkflowError(Exception):
    """Raised when week discovery or preconditions fail hard."""

    def __init__(self, message: str, *, code: str = "workflow_error") -> None:
        super().__init__(message)
        self.code = code
        self.message = message
