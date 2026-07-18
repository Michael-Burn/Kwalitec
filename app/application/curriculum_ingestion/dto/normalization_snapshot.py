"""Immutable NormalizationSnapshot DTO."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class NormalizedSectionSnapshot:
    """Read-only normalised section."""

    section_id: str
    title: str
    number: str
    order_index: int
    parent_section_id: str | None = None
    source_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class NormalizedTopicSnapshot:
    """Read-only normalised topic."""

    topic_id: str
    title: str
    section_id: str
    number: str
    order_index: int
    prerequisite_ids: tuple[str, ...] = field(default_factory=tuple)
    source_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class NormalizedObjectiveSnapshot:
    """Read-only normalised objective."""

    objective_id: str
    text: str
    topic_id: str
    number: str
    order_index: int
    source_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class NormalizationSnapshot:
    """Read-only normalisation result view."""

    result_id: str
    extraction_result_id: str
    section_count: int = 0
    topic_count: int = 0
    objective_count: int = 0
    sections: tuple[NormalizedSectionSnapshot, ...] = field(default_factory=tuple)
    topics: tuple[NormalizedTopicSnapshot, ...] = field(default_factory=tuple)
    objectives: tuple[NormalizedObjectiveSnapshot, ...] = field(
        default_factory=tuple
    )
    prerequisite_edges: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
