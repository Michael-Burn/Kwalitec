"""Ingestion report — immutable validation / pipeline findings."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class IngestionIssueSeverity(StrEnum):
    """Severity of an ingestion finding."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    BLOCKING = "blocking"


class IngestionIssueCode(StrEnum):
    """Canonical ingestion validation issue codes."""

    MISSING_OBJECTIVES = "missing_objectives"
    DUPLICATE_TOPIC = "duplicate_topic"
    UNKNOWN_SECTION = "unknown_section"
    MALFORMED_HIERARCHY = "malformed_hierarchy"
    INCONSISTENT_NUMBERING = "inconsistent_numbering"
    MISSING_METADATA = "missing_metadata"
    EMPTY_DOCUMENT = "empty_document"
    UNKNOWN_DOCUMENT_KIND = "unknown_document_kind"
    DUPLICATE_SECTION = "duplicate_section"
    DUPLICATE_OBJECTIVE = "duplicate_objective"
    ORPHAN_OBJECTIVE = "orphan_objective"
    DANGLING_PREREQUISITE = "dangling_prerequisite"
    OTHER = "other"


@dataclass(frozen=True)
class IngestionIssue:
    """Single immutable ingestion finding."""

    code: IngestionIssueCode
    message: str
    severity: IngestionIssueSeverity = IngestionIssueSeverity.ERROR
    path: str | None = None

    @classmethod
    def create(
        cls,
        code: IngestionIssueCode | str,
        message: str,
        *,
        severity: IngestionIssueSeverity | str = IngestionIssueSeverity.ERROR,
        path: str | None = None,
    ) -> IngestionIssue:
        """Construct an IngestionIssue after validating invariants."""
        resolved_code = (
            code
            if isinstance(code, IngestionIssueCode)
            else IngestionIssueCode(str(code).strip().lower())
        )
        resolved_severity = (
            severity
            if isinstance(severity, IngestionIssueSeverity)
            else IngestionIssueSeverity(str(severity).strip().lower())
        )
        msg = _require_non_empty(message, "message")
        loc = None if path is None else _require_non_empty(path, "path")
        return cls(
            code=resolved_code,
            message=msg,
            severity=resolved_severity,
            path=loc,
        )

    @property
    def is_blocking(self) -> bool:
        """True when this issue alone blocks successful ingestion."""
        if self.severity is IngestionIssueSeverity.BLOCKING:
            return True
        return self.severity is IngestionIssueSeverity.ERROR and self.code in {
            IngestionIssueCode.MISSING_OBJECTIVES,
            IngestionIssueCode.DUPLICATE_TOPIC,
            IngestionIssueCode.UNKNOWN_SECTION,
            IngestionIssueCode.MALFORMED_HIERARCHY,
            IngestionIssueCode.EMPTY_DOCUMENT,
            IngestionIssueCode.ORPHAN_OBJECTIVE,
        }


@dataclass(frozen=True)
class IngestionReport:
    """Immutable ingestion validation / pipeline report.

    Once created, reports are never mutated — re-validate produces a new report.
    """

    report_id: str
    job_id: str
    issues: tuple[IngestionIssue, ...] = field(default_factory=tuple)
    passed: bool = False
    summary: str = ""

    @classmethod
    def create(
        cls,
        report_id: str,
        job_id: str,
        *,
        issues: list[IngestionIssue] | tuple[IngestionIssue, ...] | None = None,
        summary: str = "",
    ) -> IngestionReport:
        """Construct an IngestionReport; ``passed`` is derived from issues."""
        rid = _require_non_empty(report_id, "report_id")
        jid = _require_non_empty(job_id, "job_id")
        issues_t = tuple(issues or ())
        blocking = any(issue.is_blocking for issue in issues_t)
        passed = not blocking
        text = (summary or "").strip()
        if not text:
            text = "ingestion_passed" if passed else "ingestion_failed"
        return cls(
            report_id=rid,
            job_id=jid,
            issues=issues_t,
            passed=passed,
            summary=text,
        )

    @property
    def issue_count(self) -> int:
        """Number of findings."""
        return len(self.issues)

    @property
    def blocking_issues(self) -> tuple[IngestionIssue, ...]:
        """Findings that block successful ingestion."""
        return tuple(i for i in self.issues if i.is_blocking)

    @property
    def blocks_ingestion(self) -> bool:
        """True when the pipeline must not complete successfully."""
        return not self.passed


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
