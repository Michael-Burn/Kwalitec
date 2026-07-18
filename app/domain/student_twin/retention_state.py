"""Retention state — durability estimates grounded in evidence recency."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.domain.student_twin.confidence_band import (
    ConfidenceBand,
    confidence_band_from_score,
)


@dataclass(frozen=True)
class TopicRetentionRecord:
    """Per-topic retention estimate."""

    topic_id: str
    retention_score: float
    confidence: ConfidenceBand
    last_evidence_at: datetime | None = None
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        topic_id: str,
        retention_score: float,
        *,
        confidence: ConfidenceBand | str | None = None,
        confidence_score: float | None = None,
        last_evidence_at: datetime | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
    ) -> TopicRetentionRecord:
        """Construct a TopicRetentionRecord."""
        tid = _require_non_empty(topic_id, "topic_id")
        score = _unit_interval(retention_score, "retention_score")
        if confidence is not None:
            band = (
                confidence
                if isinstance(confidence, ConfidenceBand)
                else ConfidenceBand(str(confidence).strip().lower())
            )
        elif confidence_score is not None:
            band = confidence_band_from_score(confidence_score)
        else:
            band = ConfidenceBand.VERY_LOW
        return cls(
            topic_id=tid,
            retention_score=score,
            confidence=band,
            last_evidence_at=last_evidence_at,
            evidence_ids=tuple(evidence_ids or ()),
        )


@dataclass(frozen=True)
class RetentionState:
    """Aggregate retention estimates across topics."""

    topic_records: tuple[TopicRetentionRecord, ...] = field(default_factory=tuple)
    overall_score: float = 0.0
    overall_confidence: ConfidenceBand = ConfidenceBand.VERY_LOW
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> RetentionState:
        """Return an empty retention state."""
        return cls()

    @classmethod
    def create(
        cls,
        topic_records: list[TopicRetentionRecord]
        | tuple[TopicRetentionRecord, ...]
        | None = None,
        *,
        overall_score: float | None = None,
        overall_confidence: ConfidenceBand | str | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
    ) -> RetentionState:
        """Construct RetentionState; overall defaults from topic records."""
        records = tuple(topic_records or ())
        seen: set[str] = set()
        for record in records:
            if record.topic_id in seen:
                raise ValueError(f"duplicate topic_id: {record.topic_id!r}")
            seen.add(record.topic_id)
        if overall_score is None:
            overall = (
                sum(r.retention_score for r in records) / len(records)
                if records
                else 0.0
            )
        else:
            overall = _unit_interval(overall_score, "overall_score")
        if overall_confidence is None:
            band = ConfidenceBand.VERY_LOW if not records else ConfidenceBand.LOW
        else:
            band = (
                overall_confidence
                if isinstance(overall_confidence, ConfidenceBand)
                else ConfidenceBand(str(overall_confidence).strip().lower())
            )
        return cls(
            topic_records=records,
            overall_score=overall,
            overall_confidence=band,
            evidence_ids=tuple(evidence_ids or ()),
        )

    def record_for(self, topic_id: str) -> TopicRetentionRecord | None:
        """Return the retention record for ``topic_id``, or None."""
        token = (topic_id or "").strip()
        for record in self.topic_records:
            if record.topic_id == token:
                return record
        return None

    @property
    def topic_count(self) -> int:
        """Number of topic retention records."""
        return len(self.topic_records)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _unit_interval(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number in [0, 1]")
    numeric = float(value)
    if numeric < 0.0 or numeric > 1.0:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric
