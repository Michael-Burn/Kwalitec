"""Immutable SubjectSummary DTO — compact listing view."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubjectSummary:
    """Compact subject listing row."""

    subject_id: str
    code: str
    title: str
    version_count: int = 0
    active_version_id: str | None = None
    active_version_label: str | None = None
    publication_state: str | None = None
