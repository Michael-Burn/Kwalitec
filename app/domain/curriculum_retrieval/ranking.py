"""Ranking factor breakdown for explainable, deterministic scores."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RankingBreakdown:
    """Per-factor contributions that sum (weighted) to the rank score."""

    semantic_similarity: float
    graph_proximity: float
    confidence: float
    founder_verification: float
    document_version: float
    entity_freshness: float
    relationship_strength: float
    evidence_count: float
    rank_score: float

    def as_dict(self) -> dict[str, float]:
        """Serialise factor contributions for diagnostics / Founder UI."""
        return {
            "semantic_similarity": round(self.semantic_similarity, 6),
            "graph_proximity": round(self.graph_proximity, 6),
            "confidence": round(self.confidence, 6),
            "founder_verification": round(self.founder_verification, 6),
            "document_version": round(self.document_version, 6),
            "entity_freshness": round(self.entity_freshness, 6),
            "relationship_strength": round(self.relationship_strength, 6),
            "evidence_count": round(self.evidence_count, 6),
            "rank_score": round(self.rank_score, 6),
        }
