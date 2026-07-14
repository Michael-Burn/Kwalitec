"""Validation cargo for Founder Weekly Briefing (FOS-007)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    """One explicit validation failure for a weekly briefing."""

    code: str
    message: str
    field: str | None = None


@dataclass(frozen=True)
class ValidationReport:
    """Aggregated validation outcome for a FounderWeeklyBrief."""

    ok: bool
    issues: tuple[ValidationIssue, ...]

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return self.issues


class BriefingValidationError(ValueError):
    """Raised when a weekly briefing fails structural validation."""

    def __init__(self, report: ValidationReport) -> None:
        self.report = report
        codes = ", ".join(issue.code for issue in report.issues) or "unknown"
        super().__init__(f"briefing validation failed: {codes}")
