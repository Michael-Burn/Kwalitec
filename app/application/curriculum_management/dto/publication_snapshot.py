"""Immutable PublicationSnapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PublicationSnapshot:
    """Read-only publication lifecycle view."""

    publication_id: str
    version_id: str
    state: str
    is_published: bool = False
    is_archived: bool = False
    is_terminal: bool = False
    published_at: str | None = None
    archived_at: str | None = None
    history_count: int = 0
    latest_event: str | None = None
    history_events: tuple[str, ...] = field(default_factory=tuple)
