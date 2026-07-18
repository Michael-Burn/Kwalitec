"""Immutable ValidationSnapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ValidationIssueSnapshot:
    """Read-only validation finding."""

    code: str
    message: str
    severity: str
    section_ref: str | None = None
    is_blocking: bool = False


@dataclass(frozen=True)
class ValidationSnapshot:
    """Read-only validation report view."""

    report_id: str
    version_id: str
    passed: bool
    summary: str
    issue_count: int = 0
    blocking_count: int = 0
    blocks_publication: bool = False
    issues: tuple[ValidationIssueSnapshot, ...] = field(default_factory=tuple)
