"""Immutable evidence event — sole lawful input to Twin state changes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.domain.student_twin.evidence_type import (
    EvidenceType,
    resolve_evidence_type,
)


@dataclass(frozen=True)
class EvidenceEvent:
    """A single observable learning evidence event.

    Never rewritten. Twin evolves by accumulating events, never replacing them.
    Does not carry curriculum content, PDFs, or AI-generated text as truth.
    """

    event_id: str
    evidence_type: EvidenceType
    occurred_at: datetime
    topic_id: str | None = None
    outcome: str | None = None
    score: float | None = None
    confidence_rating: float | None = None
    duration_seconds: int | None = None
    source_ref: str | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        event_id: str,
        evidence_type: EvidenceType | str,
        occurred_at: datetime,
        *,
        topic_id: str | None = None,
        outcome: str | None = None,
        score: float | None = None,
        confidence_rating: float | None = None,
        duration_seconds: int | None = None,
        source_ref: str | None = None,
        metadata: list[tuple[str, str]]
        | tuple[tuple[str, str], ...]
        | None = None,
    ) -> EvidenceEvent:
        """Construct an EvidenceEvent after validating invariants."""
        eid = _require_non_empty(event_id, "event_id")
        etype = resolve_evidence_type(evidence_type)
        if not isinstance(occurred_at, datetime):
            raise ValueError("occurred_at must be a datetime")
        when = occurred_at if occurred_at.tzinfo else occurred_at.replace(tzinfo=UTC)
        topic = None
        if topic_id is not None:
            topic = _require_non_empty(topic_id, "topic_id")
        out = None
        if outcome is not None:
            out = outcome.strip().lower() or None
        sc = _optional_unit_interval(score, "score")
        rating = _optional_unit_interval(confidence_rating, "confidence_rating")
        duration = None
        if duration_seconds is not None:
            if not isinstance(duration_seconds, int) or isinstance(
                duration_seconds, bool
            ):
                raise ValueError("duration_seconds must be a non-negative integer")
            if duration_seconds < 0:
                raise ValueError("duration_seconds must be a non-negative integer")
            duration = duration_seconds
        ref = None
        if source_ref is not None:
            ref = source_ref.strip() or None
        return cls(
            event_id=eid,
            evidence_type=etype,
            occurred_at=when,
            topic_id=topic,
            outcome=out,
            score=sc,
            confidence_rating=rating,
            duration_seconds=duration,
            source_ref=ref,
            metadata=tuple(metadata or ()),
        )

    @property
    def is_topic_scoped(self) -> bool:
        """True when this event references a curriculum topic id."""
        return self.topic_id is not None


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _optional_unit_interval(value: float | None, field_name: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number in [0, 1]")
    numeric = float(value)
    if numeric < 0.0 or numeric > 1.0:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric
