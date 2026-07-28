"""Validation report for draft Curriculum Knowledge Graph candidates."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class IssueSeverity(StrEnum):
    """Validation issue severity."""

    BLOCKER = "blocker"
    WARNING = "warning"


@dataclass(frozen=True)
class ValidationIssue:
    """One validation finding against a draft graph candidate."""

    code: str
    severity: IssueSeverity
    message: str
    stable_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "stable_id": self.stable_id,
        }


@dataclass(frozen=True)
class ValidationReport:
    """Structured validation outcome. Blockers prevent draft persistence."""

    issues: tuple[ValidationIssue, ...] = ()
    diagnostics: tuple[str, ...] = ()

    @property
    def blockers(self) -> tuple[ValidationIssue, ...]:
        return tuple(
            i for i in self.issues if i.severity is IssueSeverity.BLOCKER
        )

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(
            i for i in self.issues if i.severity is IssueSeverity.WARNING
        )

    @property
    def passed(self) -> bool:
        return not self.blockers

    @property
    def issue_count(self) -> int:
        return len(self.issues)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "issue_count": self.issue_count,
            "issues": [i.to_dict() for i in self.issues],
            "diagnostics": list(self.diagnostics),
        }

    def with_issues(self, *extra: ValidationIssue) -> ValidationReport:
        return ValidationReport(
            issues=self.issues + extra,
            diagnostics=self.diagnostics,
        )

    def with_diagnostics(self, *extra: str) -> ValidationReport:
        return ValidationReport(
            issues=self.issues,
            diagnostics=self.diagnostics + extra,
        )


@dataclass
class ValidationReportBuilder:
    """Mutable builder used by the validation stage."""

    _issues: list[ValidationIssue] = field(default_factory=list)
    _diagnostics: list[str] = field(default_factory=list)

    def blocker(
        self,
        code: str,
        message: str,
        *,
        stable_id: str | None = None,
    ) -> None:
        self._issues.append(
            ValidationIssue(
                code=code,
                severity=IssueSeverity.BLOCKER,
                message=message,
                stable_id=stable_id,
            )
        )

    def warning(
        self,
        code: str,
        message: str,
        *,
        stable_id: str | None = None,
    ) -> None:
        self._issues.append(
            ValidationIssue(
                code=code,
                severity=IssueSeverity.WARNING,
                message=message,
                stable_id=stable_id,
            )
        )

    def diagnostic(self, message: str) -> None:
        self._diagnostics.append(message)

    def build(self) -> ValidationReport:
        return ValidationReport(
            issues=tuple(self._issues),
            diagnostics=tuple(self._diagnostics),
        )
