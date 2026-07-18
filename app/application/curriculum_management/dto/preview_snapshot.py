"""Immutable PreviewSnapshot DTO — preview only, never publishes."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PreviewSnapshot:
    """Immutable preview of a subject version for Curriculum Studio.

    Preview only. Never publishes. Never mutates publication state.
    """

    preview_id: str
    version_id: str
    subject_id: str
    version_label: str
    display_name: str
    publication_state: str
    asset_count: int = 0
    assignment_count: int = 0
    section_refs: tuple[str, ...] = field(default_factory=tuple)
    assignment_sections: tuple[str, ...] = field(default_factory=tuple)
    asset_labels: tuple[str, ...] = field(default_factory=tuple)
    release_note_texts: tuple[str, ...] = field(default_factory=tuple)
    validation_passed: bool | None = None
    ready_for_approval: bool = False
