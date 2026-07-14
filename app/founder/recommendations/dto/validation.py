"""Validation cargo for Founder Recommendation Engine (FOS-006)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    """One explicit validation failure for a recommendation set."""

    code: str
    message: str
    field: str | None = None


@dataclass(frozen=True)
class ValidationReport:
    """Aggregated validation outcome for a RecommendationSet."""

    ok: bool
    issues: tuple[ValidationIssue, ...]

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return self.issues


class RecommendationValidationError(ValueError):
    """Raised when a recommendation set fails structural validation."""

    def __init__(self, report: ValidationReport) -> None:
        self.report = report
        codes = ", ".join(issue.code for issue in report.issues) or "unknown"
        super().__init__(f"recommendation validation failed: {codes}")
