"""Extracted learning objective — raw objective from a curriculum document."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExtractedObjective:
    """Learning objective candidate produced by extraction (pre-normalisation)."""

    objective_id: str
    text: str
    topic_ref: str | None = None
    number: str | None = None
    source_entry_id: str | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        objective_id: str,
        text: str,
        *,
        topic_ref: str | None = None,
        number: str | None = None,
        source_entry_id: str | None = None,
        metadata: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
    ) -> ExtractedObjective:
        """Construct an ExtractedObjective after validating invariants."""
        oid = _require_non_empty(objective_id, "objective_id")
        body = _require_non_empty(text, "text")
        topic = (
            None if topic_ref is None else _require_non_empty(topic_ref, "topic_ref")
        )
        num = None if number is None else _require_non_empty(number, "number")
        source = (
            None
            if source_entry_id is None
            else _require_non_empty(source_entry_id, "source_entry_id")
        )
        return cls(
            objective_id=oid,
            text=body,
            topic_ref=topic,
            number=num,
            source_entry_id=source,
            metadata=tuple(metadata or ()),
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized
