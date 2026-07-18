"""Immutable SubjectSnapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SubjectSnapshot:
    """Read-only view of a curriculum subject product."""

    subject_id: str
    code: str
    title: str
    description: str = ""
    exam_board: str | None = None
    academic_year: str | None = None
    locale: str = "en-GB"
    tags: tuple[str, ...] = field(default_factory=tuple)
    version_ids: tuple[str, ...] = field(default_factory=tuple)
    active_version_id: str | None = None
    version_count: int = 0
