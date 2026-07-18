"""Immutable VersionSnapshot DTO for Curriculum Studio."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class VersionRecordSnapshot:
    """Read-only version record projection."""

    version_id: str
    workspace_id: str
    subject_code: str
    version_label: str
    status: str
    created_at: str = ""
    published_at: str | None = None
    archived_at: str | None = None
    parent_version_id: str | None = None
    rollback_snapshot_id: str | None = None
    rollback_eligible: bool = False
    notes: str = ""


@dataclass(frozen=True)
class VersionSnapshot:
    """Read-only version history projection for a subject."""

    subject_code: str
    version_count: int = 0
    published_count: int = 0
    draft_count: int = 0
    archived_count: int = 0
    current_published_id: str | None = None
    records: tuple[VersionRecordSnapshot, ...] = field(default_factory=tuple)
