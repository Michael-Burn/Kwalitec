"""Immutable result of journey recommendation generation."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_journey.entities.journey_recommendation import (
    JourneyRecommendation,
    RecommendationCertainty,
    RecommendationKind,
)


@dataclass(frozen=True)
class RecommendationResult:
    """Educational recommendation with explainability cargo.

    Attributes:
        recommendation: Domain recommendation artefact (or None if none lawful).
        kind: Proposed next move (mirrors recommendation when present).
        reason: Human-readable structural reason (not marketing copy).
        confidence_explanation: Why certainty is provisional / suggested /
            conditional — never claims mastery.
        rationale_tags: Machine-readable explainability tags.
    """

    recommendation: JourneyRecommendation | None
    kind: RecommendationKind | None
    reason: str
    confidence_explanation: str
    rationale_tags: tuple[str, ...] = ()
    certainty: RecommendationCertainty | None = None
