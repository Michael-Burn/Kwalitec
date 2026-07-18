"""Recommendation state — explainable Twin recommendations (no content)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.domain.student_twin.confidence_band import ConfidenceBand


class RecommendationKind(StrEnum):
    """Kinds of educational recommendation the Twin may produce."""

    REVISE_TOPIC = "revise_topic"
    PRACTICE_TOPIC = "practice_topic"
    REPEAT_YESTERDAY = "repeat_yesterday"
    SKIP_TOPIC = "skip_topic"
    TAKE_BREAK = "take_break"
    STOP_STUDYING = "stop_studying"
    CONTINUE_CURRENT = "continue_current"
    BUILD_CONFIDENCE = "build_confidence"


@dataclass(frozen=True)
class Recommendation:
    """A single explainable recommendation derived from Twin state."""

    recommendation_id: str
    kind: RecommendationKind
    topic_id: str | None
    priority: float
    confidence: ConfidenceBand
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    rationale: str = ""
    expected_benefit: str = ""

    @classmethod
    def create(
        cls,
        recommendation_id: str,
        kind: RecommendationKind | str,
        *,
        topic_id: str | None = None,
        priority: float = 0.5,
        confidence: ConfidenceBand | str = ConfidenceBand.LOW,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
        rationale: str = "",
        expected_benefit: str = "",
    ) -> Recommendation:
        """Construct a Recommendation with required explanation fields."""
        rid = _require_non_empty(recommendation_id, "recommendation_id")
        rk = (
            kind
            if isinstance(kind, RecommendationKind)
            else RecommendationKind(str(kind))
        )
        topic = None
        if topic_id is not None:
            topic = _require_non_empty(topic_id, "topic_id")
        pri = _unit_interval(priority, "priority")
        band = (
            confidence
            if isinstance(confidence, ConfidenceBand)
            else ConfidenceBand(str(confidence).strip().lower())
        )
        return cls(
            recommendation_id=rid,
            kind=rk,
            topic_id=topic,
            priority=pri,
            confidence=band,
            evidence_ids=tuple(evidence_ids or ()),
            rationale=(rationale or "").strip(),
            expected_benefit=(expected_benefit or "").strip(),
        )


@dataclass(frozen=True)
class RecommendationState:
    """Ordered recommendations (highest priority first when built by service)."""

    recommendations: tuple[Recommendation, ...] = field(default_factory=tuple)
    overall_confidence: ConfidenceBand = ConfidenceBand.VERY_LOW
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def empty(cls) -> RecommendationState:
        """Return an empty recommendation state."""
        return cls()

    @classmethod
    def create(
        cls,
        recommendations: list[Recommendation]
        | tuple[Recommendation, ...]
        | None = None,
        *,
        overall_confidence: ConfidenceBand | str = ConfidenceBand.VERY_LOW,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
    ) -> RecommendationState:
        """Construct a RecommendationState."""
        band = (
            overall_confidence
            if isinstance(overall_confidence, ConfidenceBand)
            else ConfidenceBand(str(overall_confidence).strip().lower())
        )
        return cls(
            recommendations=tuple(recommendations or ()),
            overall_confidence=band,
            evidence_ids=tuple(evidence_ids or ()),
        )

    @property
    def primary(self) -> Recommendation | None:
        """Highest-priority recommendation, or None."""
        return self.recommendations[0] if self.recommendations else None

    @property
    def is_empty(self) -> bool:
        """True when no recommendations are present."""
        return not self.recommendations


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
