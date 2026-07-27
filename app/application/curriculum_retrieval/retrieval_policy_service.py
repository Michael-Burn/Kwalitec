"""Retrieval policy resolution — profiles influence ranking, not pipeline shape."""

from __future__ import annotations

from app.domain.curriculum_retrieval.intent import QueryIntent
from app.domain.curriculum_retrieval.profile import (
    RankingWeights,
    RetrievalProfile,
    resolve_profile,
    weights_for_profile,
)


class RetrievalPolicyService:
    """Resolve profile weights and intent-biased entity kind preferences."""

    # Intent → preferred entity kinds (metadata filter bias, not hard exclusion).
    INTENT_KIND_PREFERENCE: dict[QueryIntent, tuple[str, ...]] = {
        QueryIntent.DEFINITION: ("concept", "topic", "subtopic"),
        QueryIntent.FORMULA: ("formula", "concept"),
        QueryIntent.EXAMPLE: ("example", "concept"),
        QueryIntent.PRACTICE: ("practice_question", "example"),
        QueryIntent.LEARNING_OBJECTIVE: ("learning_objective", "topic"),
        QueryIntent.PREREQUISITE: ("concept", "topic", "learning_objective"),
        QueryIntent.RELATED: ("concept", "topic", "subtopic"),
        QueryIntent.GENERAL: (),
    }

    def resolve(self, profile: RetrievalProfile | str) -> RetrievalProfile:
        """Resolve a profile token."""
        return resolve_profile(profile)

    def weights(self, profile: RetrievalProfile | str) -> RankingWeights:
        """Return normalised ranking weights for a profile."""
        return weights_for_profile(profile)

    def preferred_kinds(self, intent: QueryIntent) -> tuple[str, ...]:
        """Return preferred entity kinds for an intent (may be empty)."""
        return self.INTENT_KIND_PREFERENCE.get(intent, ())

    def kind_boost(self, *, kind: str, intent: QueryIntent) -> float:
        """Return a small deterministic boost when kind matches intent preference.

        Boost is applied inside ranking as part of relationship_strength /
        semantic path — kept as a 0.0–0.08 additive factor by the ranker.
        """
        preferred = self.preferred_kinds(intent)
        if not preferred:
            return 0.0
        if kind in preferred:
            # Earlier preference → slightly higher boost.
            index = preferred.index(kind)
            return max(0.0, 0.08 - (0.02 * index))
        return 0.0
