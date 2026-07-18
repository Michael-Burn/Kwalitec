"""Immutable VersionSnapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class VersionSnapshot:
    """Read-only view of a subject version release."""

    version_id: str
    subject_id: str
    version_label: str
    display_name: str
    publication_state: str
    asset_count: int = 0
    assignment_count: int = 0
    section_count: int = 0
    validation_passed: bool | None = None
    approval_decision: str | None = None
    package_id: str | None = None
    publication_id: str | None = None
    has_release_notes: bool = False
    section_refs: tuple[str, ...] = field(default_factory=tuple)
    asset_kinds: tuple[str, ...] = field(default_factory=tuple)
