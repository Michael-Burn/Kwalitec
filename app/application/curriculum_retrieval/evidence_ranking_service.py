"""Deterministic evidence ranking for CIP-003 retrieval."""

from __future__ import annotations

from dataclasses import dataclass

from app.application.curriculum_retrieval.retrieval_policy_service import (
    RetrievalPolicyService,
)
from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import RankingWeights
from app.domain.curriculum_retrieval.ranking import RankingBreakdown


@dataclass(frozen=True)
class RankingInputs:
    """Normalised 0–1 factor inputs for a candidate entity."""

    semantic_similarity: float
    graph_distance: int | None
    confidence: float
    founder_verified: bool
    document_version_score: float
    entity_freshness: float
    relationship_strength: float
    evidence_count_norm: float
    entity_kind: str = ""


class EvidenceRankingService:
    """Combine retrieval signals into a deterministic rank score.

    Ranking considers:
    - Semantic similarity
    - Knowledge graph distance
    - Confidence
    - Founder verification
    - Document version freshness
    - Entity freshness
    - Relationship strength
    - Evidence count
    """

    def __init__(self, policies: RetrievalPolicyService | None = None) -> None:
        self._policies = policies or RetrievalPolicyService()

    def rank(
        self,
        *,
        inputs: RankingInputs,
        weights: RankingWeights,
        intent: QueryIntent = QueryIntent.GENERAL,
    ) -> RankingBreakdown:
        """Return explainable ranking breakdown. Same inputs → same score."""
        w = weights.normalised()
        semantic = _clamp(inputs.semantic_similarity)
        graph = _graph_proximity(inputs.graph_distance)
        confidence = _clamp(inputs.confidence)
        verified = 1.0 if inputs.founder_verified else 0.0
        version = _clamp(inputs.document_version_score)
        freshness = _clamp(inputs.entity_freshness)
        relation = _clamp(inputs.relationship_strength)
        evidence = _clamp(inputs.evidence_count_norm)

        # Intent kind boost folds into relationship_strength channel (bounded).
        kind_boost = self._policies.kind_boost(
            kind=inputs.entity_kind, intent=intent
        )
        relation = _clamp(relation + kind_boost)

        score = (
            w.semantic_similarity * semantic
            + w.graph_distance * graph
            + w.confidence * confidence
            + w.founder_verification * verified
            + w.document_version * version
            + w.entity_freshness * freshness
            + w.relationship_strength * relation
            + w.evidence_count * evidence
        )
        score = round(_clamp(score), 6)

        return RankingBreakdown(
            semantic_similarity=round(w.semantic_similarity * semantic, 6),
            graph_proximity=round(w.graph_distance * graph, 6),
            confidence=round(w.confidence * confidence, 6),
            founder_verification=round(w.founder_verification * verified, 6),
            document_version=round(w.document_version * version, 6),
            entity_freshness=round(w.entity_freshness * freshness, 6),
            relationship_strength=round(w.relationship_strength * relation, 6),
            evidence_count=round(w.evidence_count * evidence, 6),
            rank_score=score,
        )


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _graph_proximity(distance: int | None) -> float:
    """Map graph distance to proximity in (0, 1]. None (unknown) → mild prior."""
    if distance is None:
        return 0.35
    if distance <= 0:
        return 1.0
    return 1.0 / (1.0 + float(distance))
