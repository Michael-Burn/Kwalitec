"""Extracted topic — raw syllabus unit from a curriculum document."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExtractedTopic:
    """Topic candidate produced by extraction (pre-normalisation)."""

    topic_id: str
    title: str
    section_ref: str | None = None
    number: str | None = None
    source_entry_id: str | None = None
    prerequisite_refs: tuple[str, ...] = field(default_factory=tuple)
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        topic_id: str,
        title: str,
        *,
        section_ref: str | None = None,
        number: str | None = None,
        source_entry_id: str | None = None,
        prerequisite_refs: list[str] | tuple[str, ...] | None = None,
        metadata: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
    ) -> ExtractedTopic:
        """Construct an ExtractedTopic after validating invariants."""
        tid = _require_non_empty(topic_id, "topic_id")
        name = _require_non_empty(title, "title")
        section = (
            None
            if section_ref is None
            else _require_non_empty(section_ref, "section_ref")
        )
        num = None if number is None else _require_non_empty(number, "number")
        source = (
            None
            if source_entry_id is None
            else _require_non_empty(source_entry_id, "source_entry_id")
        )
        prereqs = tuple(
            _require_non_empty(p, "prerequisite_ref")
            for p in (prerequisite_refs or ())
        )
        return cls(
            topic_id=tid,
            title=name,
            section_ref=section,
            number=num,
            source_entry_id=source,
            prerequisite_refs=prereqs,
            metadata=tuple(metadata or ()),
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
