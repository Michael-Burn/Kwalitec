"""Validation report — immutable readiness capture for a subject version."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ValidationSeverity(StrEnum):
    """Severity of a validation finding."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    BLOCKING = "blocking"


class ValidationIssueCode(StrEnum):
    """Canonical validation issue codes."""

    MISSING_SYLLABUS = "missing_syllabus"
    MISSING_CMP = "missing_cmp"
    MISSING_LEARNING_OBJECTIVES = "missing_learning_objectives"
    MISSING_BLUEPRINT_ASSIGNMENT = "missing_blueprint_assignment"
    DUPLICATE_TOPIC = "duplicate_topic"
    DUPLICATE_SECTION = "duplicate_section"
    EMPTY_PACKAGE = "empty_package"
    PUBLICATION_BLOCKED = "publication_blocked"
    INVALID_REFERENCE = "invalid_reference"
    OTHER = "other"


@dataclass(frozen=True)
class ValidationIssue:
    """Single immutable validation finding."""

    code: ValidationIssueCode
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    section_ref: str | None = None

    @classmethod
    def create(
        cls,
        code: ValidationIssueCode | str,
        message: str,
        *,
        severity: ValidationSeverity | str = ValidationSeverity.ERROR,
        section_ref: str | None = None,
    ) -> ValidationIssue:
        """Construct a ValidationIssue after validating invariants."""
        resolved_code = (
            code
            if isinstance(code, ValidationIssueCode)
            else ValidationIssueCode(str(code).strip().lower())
        )
        resolved_severity = (
            severity
            if isinstance(severity, ValidationSeverity)
            else ValidationSeverity(str(severity).strip().lower())
        )
        msg = _require_non_empty(message, "message")
        section = (
            None
            if section_ref is None
            else _require_non_empty(section_ref, "section_ref")
        )
        return cls(
            code=resolved_code,
            message=msg,
            severity=resolved_severity,
            section_ref=section,
        )

    @property
    def is_blocking(self) -> bool:
        """True when this issue alone blocks publication."""
        return self.severity is ValidationSeverity.BLOCKING or (
            self.severity is ValidationSeverity.ERROR
            and self.code
            in {
                ValidationIssueCode.MISSING_SYLLABUS,
                ValidationIssueCode.MISSING_BLUEPRINT_ASSIGNMENT,
                ValidationIssueCode.PUBLICATION_BLOCKED,
                ValidationIssueCode.EMPTY_PACKAGE,
            }
        )


@dataclass(frozen=True)
class ValidationReport:
    """Immutable readiness report for a subject version.

    Once created, reports are never mutated — re-validate produces a new report.
    """

    report_id: str
    version_id: str
    issues: tuple[ValidationIssue, ...] = field(default_factory=tuple)
    passed: bool = False
    summary: str = ""

    @classmethod
    def create(
        cls,
        report_id: str,
        version_id: str,
        *,
        issues: list[ValidationIssue] | tuple[ValidationIssue, ...] | None = None,
        summary: str = "",
    ) -> ValidationReport:
        """Construct a ValidationReport; ``passed`` is derived from issues."""
        rid = _require_non_empty(report_id, "report_id")
        vid = _require_non_empty(version_id, "version_id")
        issues_t = tuple(issues or ())
        blocking = any(issue.is_blocking for issue in issues_t)
        passed = not blocking
        text = (summary or "").strip()
        if not text:
            text = "validation_passed" if passed else "validation_failed"
        return cls(
            report_id=rid,
            version_id=vid,
            issues=issues_t,
            passed=passed,
            summary=text,
        )

    @property
    def issue_count(self) -> int:
        """Number of findings."""
        return len(self.issues)

    @property
    def blocking_issues(self) -> tuple[ValidationIssue, ...]:
        """Findings that block publication."""
        return tuple(i for i in self.issues if i.is_blocking)

    @property
    def blocks_publication(self) -> bool:
        """True when publication must not proceed."""
        return not self.passed


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
