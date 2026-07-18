"""Immutable ApprovalSnapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ApprovalSnapshot:
    """Read-only approval record view."""

    approval_id: str
    version_id: str
    reviewer_id: str
    decision: str
    rationale: str = ""
    decided_at: str | None = None
    is_approved: bool = False
