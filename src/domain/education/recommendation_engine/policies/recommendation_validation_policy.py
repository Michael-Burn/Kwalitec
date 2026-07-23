"""Policy validating RecommendationSet aggregate shapes.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Validation Policy

This policy performs shape validation only — unique identities, resolvable
references, and well-typed fields. Educational reasoning lives in
``RecommendationPolicy``, ``PriorityPolicy``, ``ImpactPolicy``,
``ConstraintPolicy``, and ``OrderingPolicy``.
"""

from __future__ import annotations

from datetime import datetime

from domain.education.foundation.base import require_identity_value
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.ids import RecommendationSetId
from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)
from domain.education.recommendation_engine.value_objects.recommendation_constraint import (  # noqa: E501
    RecommendationConstraint,
)


class RecommendationValidationPolicy:
    """Validates RecommendationSet shapes — no educational reasoning."""

    @staticmethod
    def assert_identity(set_id: RecommendationSetId) -> RecommendationSetId:
        if not isinstance(set_id, RecommendationSetId):
            raise EducationalInvariantViolation(
                "recommendation set must possess a RecommendationSetId identity",
                invariant="RecommendationSet.identity.required",
            )
        return set_id

    @staticmethod
    def assert_student_id(student_id: str) -> str:
        return require_identity_value(student_id, "student_id")

    @staticmethod
    def assert_recommended_at(recommended_at: datetime) -> datetime:
        if not isinstance(recommended_at, datetime):
            raise EducationalInvariantViolation(
                "recommended_at must be a datetime",
                invariant="RecommendationSet.recommended_at.type",
            )
        return recommended_at

    @staticmethod
    def assert_recommendations(
        recommendations: list[Recommendation] | tuple[Recommendation, ...],
    ) -> tuple[Recommendation, ...]:
        items = tuple(recommendations)
        seen: set[str] = set()
        ranks: set[int] = set()
        for recommendation in items:
            if not isinstance(recommendation, Recommendation):
                raise EducationalInvariantViolation(
                    "recommendations must contain Recommendation value objects",
                    invariant="RecommendationSet.recommendations.type",
                )
            key = recommendation.recommendation_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate recommendation_id in recommendation set",
                    invariant="RecommendationSet.recommendations.unique",
                )
            seen.add(key)
            rank = recommendation.ordering.rank
            if rank in ranks:
                raise EducationalInvariantViolation(
                    "duplicate ordering.rank in recommendation set",
                    invariant="RecommendationSet.recommendations.rank.unique",
                )
            ranks.add(rank)
        if items:
            expected_ranks = set(range(1, len(items) + 1))
            if ranks != expected_ranks:
                raise EducationalInvariantViolation(
                    "recommendation ranks must be a dense 1..N sequence",
                    invariant="RecommendationSet.recommendations.rank.dense",
                )
            # Ordering must already be priority-descending.
            for index in range(1, len(items)):
                previous = items[index - 1]
                current = items[index]
                if previous.priority.magnitude < current.priority.magnitude:
                    raise EducationalInvariantViolation(
                        "recommendations must be ordered by descending priority",
                        invariant="RecommendationSet.recommendations.ordered",
                    )
        return items

    @staticmethod
    def assert_constraints(
        constraints: list[RecommendationConstraint]
        | tuple[RecommendationConstraint, ...],
    ) -> tuple[RecommendationConstraint, ...]:
        items = tuple(constraints)
        for constraint in items:
            if not isinstance(constraint, RecommendationConstraint):
                raise EducationalInvariantViolation(
                    "constraints must contain RecommendationConstraint "
                    "value objects",
                    invariant="RecommendationSet.constraints.type",
                )
        return items
