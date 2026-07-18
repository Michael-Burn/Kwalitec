"""Normalization result — immutable normalised educational structures."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class NormalizedSection:
    """Canonical section after normalisation."""

    section_id: str
    title: str
    number: str
    order_index: int
    parent_section_id: str | None = None
    source_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        section_id: str,
        title: str,
        number: str,
        order_index: int,
        *,
        parent_section_id: str | None = None,
        source_ids: list[str] | tuple[str, ...] | None = None,
    ) -> NormalizedSection:
        """Construct a NormalizedSection after validating invariants."""
        if not isinstance(order_index, int) or order_index < 0:
            raise ValueError("order_index must be a non-negative int")
        parent = (
            None
            if parent_section_id is None
            else _require_non_empty(parent_section_id, "parent_section_id")
        )
        return cls(
            section_id=_require_non_empty(section_id, "section_id"),
            title=_require_non_empty(title, "title"),
            number=_require_non_empty(number, "number"),
            order_index=order_index,
            parent_section_id=parent,
            source_ids=tuple(source_ids or ()),
        )


@dataclass(frozen=True)
class NormalizedTopic:
    """Canonical topic after normalisation."""

    topic_id: str
    title: str
    section_id: str
    number: str
    order_index: int
    prerequisite_ids: tuple[str, ...] = field(default_factory=tuple)
    source_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        topic_id: str,
        title: str,
        section_id: str,
        number: str,
        order_index: int,
        *,
        prerequisite_ids: list[str] | tuple[str, ...] | None = None,
        source_ids: list[str] | tuple[str, ...] | None = None,
    ) -> NormalizedTopic:
        """Construct a NormalizedTopic after validating invariants."""
        if not isinstance(order_index, int) or order_index < 0:
            raise ValueError("order_index must be a non-negative int")
        return cls(
            topic_id=_require_non_empty(topic_id, "topic_id"),
            title=_require_non_empty(title, "title"),
            section_id=_require_non_empty(section_id, "section_id"),
            number=_require_non_empty(number, "number"),
            order_index=order_index,
            prerequisite_ids=tuple(
                _require_non_empty(p, "prerequisite_id")
                for p in (prerequisite_ids or ())
            ),
            source_ids=tuple(source_ids or ()),
        )


@dataclass(frozen=True)
class NormalizedObjective:
    """Canonical learning objective after normalisation."""

    objective_id: str
    text: str
    topic_id: str
    number: str
    order_index: int
    source_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        objective_id: str,
        text: str,
        topic_id: str,
        number: str,
        order_index: int,
        *,
        source_ids: list[str] | tuple[str, ...] | None = None,
    ) -> NormalizedObjective:
        """Construct a NormalizedObjective after validating invariants."""
        if not isinstance(order_index, int) or order_index < 0:
            raise ValueError("order_index must be a non-negative int")
        return cls(
            objective_id=_require_non_empty(objective_id, "objective_id"),
            text=_require_non_empty(text, "text"),
            topic_id=_require_non_empty(topic_id, "topic_id"),
            number=_require_non_empty(number, "number"),
            order_index=order_index,
            source_ids=tuple(source_ids or ()),
        )


@dataclass(frozen=True)
class NormalizationResult:
    """Immutable normalised curriculum structures for one ingestion run.

    Output is structural only — never sessions, activities, or missions.
    """

    result_id: str
    extraction_result_id: str
    sections: tuple[NormalizedSection, ...] = field(default_factory=tuple)
    topics: tuple[NormalizedTopic, ...] = field(default_factory=tuple)
    objectives: tuple[NormalizedObjective, ...] = field(default_factory=tuple)
    prerequisite_edges: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        result_id: str,
        extraction_result_id: str,
        *,
        sections: list[NormalizedSection]
        | tuple[NormalizedSection, ...]
        | None = None,
        topics: list[NormalizedTopic] | tuple[NormalizedTopic, ...] | None = None,
        objectives: list[NormalizedObjective]
        | tuple[NormalizedObjective, ...]
        | None = None,
        prerequisite_edges: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
        metadata: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
    ) -> NormalizationResult:
        """Construct a NormalizationResult after validating invariants."""
        return cls(
            result_id=_require_non_empty(result_id, "result_id"),
            extraction_result_id=_require_non_empty(
                extraction_result_id, "extraction_result_id"
            ),
            sections=tuple(sections or ()),
            topics=tuple(topics or ()),
            objectives=tuple(objectives or ()),
            prerequisite_edges=tuple(prerequisite_edges or ()),
            metadata=tuple(metadata or ()),
        )

    @property
    def section_count(self) -> int:
        """Number of normalised sections."""
        return len(self.sections)

    @property
    def topic_count(self) -> int:
        """Number of normalised topics."""
        return len(self.topics)

    @property
    def objective_count(self) -> int:
        """Number of normalised objectives."""
        return len(self.objectives)

    def topic_by_id(self, topic_id: str) -> NormalizedTopic | None:
        """Return a topic by identity, or None."""
        token = (topic_id or "").strip()
        for topic in self.topics:
            if topic.topic_id == token:
                return topic
        return None

    def section_by_id(self, section_id: str) -> NormalizedSection | None:
        """Return a section by identity, or None."""
        token = (section_id or "").strip()
        for section in self.sections:
            if section.section_id == token:
                return section
        return None


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
