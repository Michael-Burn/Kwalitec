"""Immutable ReleaseSnapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ReleaseSnapshot:
    """Read-only release / release-notes view."""

    version_id: str
    subject_id: str
    version_label: str
    display_name: str
    publication_state: str
    notes_id: str | None = None
    headline: str = ""
    entry_count: int = 0
    entries: tuple[str, ...] = field(default_factory=tuple)
    is_published: bool = False
    published_at: str | None = None
