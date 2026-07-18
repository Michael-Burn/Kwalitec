"""Extracted section — raw structural partition from a curriculum document."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExtractedSection:
    """Section / chapter candidate produced by extraction (pre-normalisation)."""

    section_id: str
    title: str
    number: str | None = None
    source_entry_id: str | None = None
    parent_section_id: str | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        section_id: str,
        title: str,
        *,
        number: str | None = None,
        source_entry_id: str | None = None,
        parent_section_id: str | None = None,
        metadata: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
    ) -> ExtractedSection:
        """Construct an ExtractedSection after validating invariants."""
        sid = _require_non_empty(section_id, "section_id")
        name = _require_non_empty(title, "title")
        num = None if number is None else _require_non_empty(number, "number")
        source = (
            None
            if source_entry_id is None
            else _require_non_empty(source_entry_id, "source_entry_id")
        )
        parent = (
            None
            if parent_section_id is None
            else _require_non_empty(parent_section_id, "parent_section_id")
        )
        return cls(
            section_id=sid,
            title=name,
            number=num,
            source_entry_id=source,
            parent_section_id=parent,
            metadata=tuple(metadata or ()),
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
