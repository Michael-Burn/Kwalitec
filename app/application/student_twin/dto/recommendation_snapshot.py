"""Immutable recommendation snapshot and explanation DTOs."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.recommendation_state import RecommendationState


@dataclass(frozen=True)
class RecommendationItemDTO:
    """Single recommendation projection."""

    recommendation_id: str
    kind: str
    topic_id: str | None
    priority: float
    confidence: str
    rationale: str
    expected_benefit: str
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RecommendationSnapshot:
    """Ordered recommendation list projection."""

    items: tuple[RecommendationItemDTO, ...] = field(default_factory=tuple)
    overall_confidence: str = "very_low"
    primary_kind: str | None = None

    @classmethod
    def from_domain(cls, state: RecommendationState) -> RecommendationSnapshot:
        """Project RecommendationState to a DTO."""
        items = tuple(
            RecommendationItemDTO(
                recommendation_id=rec.recommendation_id,
                kind=rec.kind.value,
                topic_id=rec.topic_id,
                priority=rec.priority,
                confidence=rec.confidence.value,
                rationale=rec.rationale,
                expected_benefit=rec.expected_benefit,
                evidence_ids=rec.evidence_ids,
            )
            for rec in state.recommendations
        )
        primary = items[0].kind if items else None
        return cls(
            items=items,
            overall_confidence=state.overall_confidence.value,
            primary_kind=primary,
        )


@dataclass(frozen=True)
class RecommendationExplanation:
    """Explainable recommendation payload for consumers."""

    recommendation_id: str
    kind: str
    topic_id: str | None
    evidence_ids: tuple[str, ...]
    rationale: str
    expected_benefit: str
    confidence: str
    priority: float
