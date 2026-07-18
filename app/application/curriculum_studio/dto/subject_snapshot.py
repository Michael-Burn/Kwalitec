"""Immutable SubjectSnapshot DTO for Curriculum Studio."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SubjectSnapshot:
    """Read-only subject projection from Curriculum Management."""

    subject_code: str
    title: str = ""
    subject_id: str | None = None
    active_version_id: str | None = None
    version_count: int = 0
    publication_state: str | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
