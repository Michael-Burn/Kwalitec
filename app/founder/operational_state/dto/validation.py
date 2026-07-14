"""Validation cargo for Founder Operational State (FOS-005)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    """One explicit validation failure for an operational snapshot."""

    code: str
    message: str
    field: str | None = None


@dataclass(frozen=True)
class ValidationReport:
    """Aggregated validation outcome for a FounderOperationalState."""

    ok: bool
    issues: tuple[ValidationIssue, ...]

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return self.issues


class OperationalStateValidationError(ValueError):
    """Raised when an operational snapshot fails completeness validation."""

    def __init__(self, report: ValidationReport) -> None:
        self.report = report
        codes = ", ".join(issue.code for issue in report.issues) or "unknown"
        super().__init__(f"operational state validation failed: {codes}")
