"""Retrieval profiles / policies that influence ranking weights."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RetrievalProfile(StrEnum):
    """Named retrieval policies for downstream consumers."""

    TUTOR = "tutor"
    MISSION_ENGINE = "mission_engine"
    REVISION_PLANNER = "revision_planner"
    KNOWLEDGE_SEARCH = "knowledge_search"
    ANALYTICS = "analytics"
    FOUNDER_EXPLORER = "founder_explorer"
    STUDENT_DIGITAL_TWIN = "student_digital_twin"


@dataclass(frozen=True)
class RankingWeights:
    """Deterministic ranking factor weights (must sum approximately to 1.0)."""

    semantic_similarity: float
    graph_distance: float
    confidence: float
    founder_verification: float
    document_version: float
    entity_freshness: float
    relationship_strength: float
    evidence_count: float

    def normalised(self) -> RankingWeights:
        """Return weights renormalised to sum to 1.0 (or self if zero)."""
        total = (
            self.semantic_similarity
            + self.graph_distance
            + self.confidence
            + self.founder_verification
            + self.document_version
            + self.entity_freshness
            + self.relationship_strength
            + self.evidence_count
        )
        if total <= 0:
            return self
        return RankingWeights(
            semantic_similarity=self.semantic_similarity / total,
            graph_distance=self.graph_distance / total,
            confidence=self.confidence / total,
            founder_verification=self.founder_verification / total,
            document_version=self.document_version / total,
            entity_freshness=self.entity_freshness / total,
            relationship_strength=self.relationship_strength / total,
            evidence_count=self.evidence_count / total,
        )


# Profile → ranking weight policy. Profiles change weights, not pipeline shape.
PROFILE_WEIGHTS: dict[RetrievalProfile, RankingWeights] = {
    RetrievalProfile.TUTOR: RankingWeights(
        semantic_similarity=0.28,
        graph_distance=0.18,
        confidence=0.18,
        founder_verification=0.16,
        document_version=0.05,
        entity_freshness=0.03,
        relationship_strength=0.07,
        evidence_count=0.05,
    ),
    RetrievalProfile.MISSION_ENGINE: RankingWeights(
        semantic_similarity=0.18,
        graph_distance=0.22,
        confidence=0.20,
        founder_verification=0.18,
        document_version=0.06,
        entity_freshness=0.04,
        relationship_strength=0.08,
        evidence_count=0.04,
    ),
    RetrievalProfile.REVISION_PLANNER: RankingWeights(
        semantic_similarity=0.22,
        graph_distance=0.20,
        confidence=0.16,
        founder_verification=0.12,
        document_version=0.08,
        entity_freshness=0.06,
        relationship_strength=0.10,
        evidence_count=0.06,
    ),
    RetrievalProfile.KNOWLEDGE_SEARCH: RankingWeights(
        semantic_similarity=0.40,
        graph_distance=0.12,
        confidence=0.14,
        founder_verification=0.10,
        document_version=0.06,
        entity_freshness=0.04,
        relationship_strength=0.08,
        evidence_count=0.06,
    ),
    RetrievalProfile.ANALYTICS: RankingWeights(
        semantic_similarity=0.10,
        graph_distance=0.15,
        confidence=0.25,
        founder_verification=0.20,
        document_version=0.10,
        entity_freshness=0.05,
        relationship_strength=0.05,
        evidence_count=0.10,
    ),
    RetrievalProfile.FOUNDER_EXPLORER: RankingWeights(
        semantic_similarity=0.30,
        graph_distance=0.15,
        confidence=0.15,
        founder_verification=0.10,
        document_version=0.08,
        entity_freshness=0.05,
        relationship_strength=0.10,
        evidence_count=0.07,
    ),
    RetrievalProfile.STUDENT_DIGITAL_TWIN: RankingWeights(
        semantic_similarity=0.16,
        graph_distance=0.24,
        confidence=0.20,
        founder_verification=0.16,
        document_version=0.06,
        entity_freshness=0.04,
        relationship_strength=0.10,
        evidence_count=0.04,
    ),
}


def resolve_profile(value: RetrievalProfile | str) -> RetrievalProfile:
    """Resolve a profile enum from enum or string token."""
    if isinstance(value, RetrievalProfile):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    try:
        return RetrievalProfile(token)
    except ValueError as exc:
        raise ValueError(f"Unknown retrieval profile: {value!r}") from exc


def weights_for_profile(profile: RetrievalProfile | str) -> RankingWeights:
    """Return normalised ranking weights for a retrieval profile."""
    resolved = resolve_profile(profile)
    return PROFILE_WEIGHTS[resolved].normalised()
