"""Knowledge state — curriculum-topic understanding beliefs from evidence."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.confidence_band import (
    ConfidenceBand,
    confidence_band_from_score,
)


@dataclass(frozen=True)
class TopicKnowledgeRecord:
    """Per-topic knowledge belief with explicit confidence."""

    topic_id: str
    knowledge_score: float
    confidence: ConfidenceBand
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        topic_id: str,
        knowledge_score: float,
        *,
        confidence: ConfidenceBand | str | None = None,
        confidence_score: float | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
    ) -> TopicKnowledgeRecord:
        """Construct a TopicKnowledgeRecord."""
        tid = _require_non_empty(topic_id, "topic_id")
        score = _unit_interval(knowledge_score, "knowledge_score")
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
            knowledge_score=score,
            confidence=band,
            evidence_ids=tuple(evidence_ids or ()),
        )


@dataclass(frozen=True)
class KnowledgeState:
    """Aggregate knowledge beliefs across topics."""

    topic_records: tuple[TopicKnowledgeRecord, ...] = field(default_factory=tuple)
    overall_score: float = 0.0
    overall_confidence: ConfidenceBand = ConfidenceBand.VERY_LOW
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> KnowledgeState:
        """Return an empty knowledge state."""
        return cls()

    @classmethod
    def create(
        cls,
        topic_records: list[TopicKnowledgeRecord]
        | tuple[TopicKnowledgeRecord, ...]
        | None = None,
        *,
        overall_score: float | None = None,
        overall_confidence: ConfidenceBand | str | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
    ) -> KnowledgeState:
        """Construct KnowledgeState; overall defaults from topic records."""
        records = tuple(topic_records or ())
        seen: set[str] = set()
        for record in records:
            if record.topic_id in seen:
                raise ValueError(f"duplicate topic_id: {record.topic_id!r}")
            seen.add(record.topic_id)
        if overall_score is None:
            if records:
                overall = sum(r.knowledge_score for r in records) / len(records)
            else:
                overall = 0.0
        else:
            overall = _unit_interval(overall_score, "overall_score")
        if overall_confidence is None:
            if not records:
                band = ConfidenceBand.VERY_LOW
            else:
                mid = sum(
                    _band_rank(r.confidence) for r in records
                ) / len(records)
                band = confidence_band_from_score(mid / 4.0)
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

    def record_for(self, topic_id: str) -> TopicKnowledgeRecord | None:
        """Return the knowledge record for ``topic_id``, or None."""
        token = (topic_id or "").strip()
        for record in self.topic_records:
            if record.topic_id == token:
                return record
        return None

    @property
    def topic_count(self) -> int:
        """Number of topic knowledge records."""
        return len(self.topic_records)


def _band_rank(band: ConfidenceBand) -> int:
    order = (
        ConfidenceBand.VERY_LOW,
        ConfidenceBand.LOW,
        ConfidenceBand.MEDIUM,
        ConfidenceBand.HIGH,
        ConfidenceBand.VERY_HIGH,
    )
    return order.index(band)


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
