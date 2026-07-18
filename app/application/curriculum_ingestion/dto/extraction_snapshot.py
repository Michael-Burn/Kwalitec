"""Immutable ExtractionSnapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExtractedSectionSnapshot:
    """Read-only extracted section."""

    section_id: str
    title: str
    number: str | None = None
    source_entry_id: str | None = None
    parent_section_id: str | None = None


@dataclass(frozen=True)
class ExtractedTopicSnapshot:
    """Read-only extracted topic."""

    topic_id: str
    title: str
    section_ref: str | None = None
    number: str | None = None
    source_entry_id: str | None = None
    prerequisite_refs: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ExtractedObjectiveSnapshot:
    """Read-only extracted objective."""

    objective_id: str
    text: str
    topic_ref: str | None = None
    number: str | None = None
    source_entry_id: str | None = None


@dataclass(frozen=True)
class ExtractionSnapshot:
    """Read-only extraction result view."""

    result_id: str
    document_ids: tuple[str, ...]
    document_kinds: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    section_count: int = 0
    topic_count: int = 0
    objective_count: int = 0
    sections: tuple[ExtractedSectionSnapshot, ...] = field(default_factory=tuple)
    topics: tuple[ExtractedTopicSnapshot, ...] = field(default_factory=tuple)
    objectives: tuple[ExtractedObjectiveSnapshot, ...] = field(
        default_factory=tuple
    )
    prerequisite_refs: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)
