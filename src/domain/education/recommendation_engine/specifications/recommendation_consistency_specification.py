"""Specification: a RecommendationSet's parts agree with its ordering.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Consistency Specification
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)
from domain.education.recommendation_engine.policies.ordering_policy import (
    OrderingPolicy,
)


class RecommendationConsistencySpecification:
    """A RecommendationSet's ordering must match OrderingPolicy.rank.

    Verifies the aggregate's own invariant: recommendation ranks are always
    the same dense 1..N ordering that ``OrderingPolicy`` would recompute —
    never independently supplied ranks that could silently drift.
    """

    @staticmethod
    def is_satisfied_by(recommendation_set: RecommendationSet) -> bool:
        recomputed = OrderingPolicy.rank(recommendation_set.recommendations)
        if len(recomputed) != len(recommendation_set.recommendations):
            return False
        for expected, actual in zip(
            recomputed, recommendation_set.recommendations, strict=True
        ):
            if expected.recommendation_id != actual.recommendation_id:
                return False
            if expected.ordering.rank != actual.ordering.rank:
                return False
        return True

    @staticmethod
    def assert_satisfied_by(recommendation_set: RecommendationSet) -> None:
        if not RecommendationConsistencySpecification.is_satisfied_by(
            recommendation_set
        ):
            raise EducationalInvariantViolation(
                "recommendation ordering must match OrderingPolicy.rank",
                invariant="RecommendationConsistencySpecification.ordering",
            )
