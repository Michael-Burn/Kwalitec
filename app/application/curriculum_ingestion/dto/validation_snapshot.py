"""Immutable ValidationSnapshot DTO for ingestion reports."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ValidationIssueSnapshot:
    """Read-only ingestion validation finding."""

    code: str
    message: str
    severity: str
    path: str | None = None
    is_blocking: bool = False


@dataclass(frozen=True)
class ValidationSnapshot:
    """Read-only ingestion validation report view."""

    report_id: str
    job_id: str
    passed: bool
    summary: str
    issue_count: int = 0
    blocking_count: int = 0
    blocks_ingestion: bool = False
    issues: tuple[ValidationIssueSnapshot, ...] = field(default_factory=tuple)
