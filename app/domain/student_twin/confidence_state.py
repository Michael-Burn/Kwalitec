"""Confidence state — explicit uncertainty over Twin conclusions."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.confidence_band import (
    ConfidenceBand,
    confidence_band_from_score,
    confidence_score_from_band,
)


@dataclass(frozen=True)
class TopicConfidenceRecord:
    """Per-topic confidence in Twin conclusions for that topic."""

    topic_id: str
    confidence_score: float
    confidence_band: ConfidenceBand
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        topic_id: str,
        confidence_score: float,
        *,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
    ) -> TopicConfidenceRecord:
        """Construct a TopicConfidenceRecord."""
        tid = _require_non_empty(topic_id, "topic_id")
        score = _unit_interval(confidence_score, "confidence_score")
        return cls(
            topic_id=tid,
            confidence_score=score,
            confidence_band=confidence_band_from_score(score),
            evidence_ids=tuple(evidence_ids or ()),
        )


@dataclass(frozen=True)
class ConfidenceState:
    """Aggregate confidence across knowledge, mastery, retention, recommendations."""

    topic_records: tuple[TopicConfidenceRecord, ...] = field(default_factory=tuple)
    knowledge_confidence: ConfidenceBand = ConfidenceBand.VERY_LOW
    mastery_confidence: ConfidenceBand = ConfidenceBand.VERY_LOW
    retention_confidence: ConfidenceBand = ConfidenceBand.VERY_LOW
    recommendation_confidence: ConfidenceBand = ConfidenceBand.VERY_LOW
    overall_score: float = 0.0
    overall_band: ConfidenceBand = ConfidenceBand.VERY_LOW
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> ConfidenceState:
        """Return an empty confidence state."""
        return cls()

    @classmethod
    def create(
        cls,
        *,
        topic_records: list[TopicConfidenceRecord]
        | tuple[TopicConfidenceRecord, ...]
        | None = None,
        knowledge_confidence: ConfidenceBand | str = ConfidenceBand.VERY_LOW,
        mastery_confidence: ConfidenceBand | str = ConfidenceBand.VERY_LOW,
        retention_confidence: ConfidenceBand | str = ConfidenceBand.VERY_LOW,
        recommendation_confidence: ConfidenceBand | str = ConfidenceBand.VERY_LOW,
        overall_score: float | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
    ) -> ConfidenceState:
        """Construct ConfidenceState with explicit bands."""
        records = tuple(topic_records or ())
        seen: set[str] = set()
        for record in records:
            if record.topic_id in seen:
                raise ValueError(f"duplicate topic_id: {record.topic_id!r}")
            seen.add(record.topic_id)
        k = _as_band(knowledge_confidence)
        m = _as_band(mastery_confidence)
        r = _as_band(retention_confidence)
        rec = _as_band(recommendation_confidence)
        if overall_score is None:
            overall = (
                confidence_score_from_band(k)
                + confidence_score_from_band(m)
                + confidence_score_from_band(r)
                + confidence_score_from_band(rec)
            ) / 4.0
        else:
            overall = _unit_interval(overall_score, "overall_score")
        return cls(
            topic_records=records,
            knowledge_confidence=k,
            mastery_confidence=m,
            retention_confidence=r,
            recommendation_confidence=rec,
            overall_score=overall,
            overall_band=confidence_band_from_score(overall),
            evidence_ids=tuple(evidence_ids or ()),
        )

    def record_for(self, topic_id: str) -> TopicConfidenceRecord | None:
        """Return the confidence record for ``topic_id``, or None."""
        token = (topic_id or "").strip()
        for record in self.topic_records:
            if record.topic_id == token:
                return record
        return None


def _as_band(value: ConfidenceBand | str) -> ConfidenceBand:
    if isinstance(value, ConfidenceBand):
        return value
    return ConfidenceBand(str(value).strip().lower())


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
