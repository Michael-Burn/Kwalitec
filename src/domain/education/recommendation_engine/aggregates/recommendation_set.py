"""RecommendationSet aggregate — the Recommendation Engine's product.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Set

RecommendationSet represents educational reasoning, not storage: a
deterministic, explainable collection of educational recommendations at
one point in time.
"""

from __future__ import annotations

from datetime import datetime

from domain.education.recommendation_engine.enums import RecommendationCategory
from domain.education.recommendation_engine.ids import (
    CompetencyId,
    RecommendationSetId,
    SubjectId,
)
from domain.education.recommendation_engine.policies.impact_policy import ImpactPolicy
from domain.education.recommendation_engine.policies.recommendation_validation_policy import (  # noqa: E501
    RecommendationValidationPolicy,
)
from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)
from domain.education.recommendation_engine.value_objects.recommendation_constraint import (  # noqa: E501
    RecommendationConstraint,
)
from domain.education.recommendation_engine.value_objects.recommendation_snapshot import (  # noqa: E501
    RecommendationSnapshot,
)


class RecommendationSet:
    """Aggregate root modelling one deterministic recommendation set.

    RecommendationSet is the Recommendation Engine's product: an immutable,
    explainable collection of educational recommendations built entirely
    from a ``StudentEducationalState``, a ``MasteryAssessment``,
    ``EducationalEvidence``, and a ``KnowledgeGraph`` at one
    caller-supplied point in time.

    It never mutates after construction — a revised set is always a new
    instance, never a silent edit — and it never persists itself,
    orchestrates, mutates ``StudentEducationalState``, updates the Digital
    Twin, or generates missions.
    """

    def __init__(
        self,
        set_id: RecommendationSetId,
        student_id: str,
        recommended_at: datetime,
        *,
        recommendations: list[Recommendation] | tuple[Recommendation, ...] = (),
        constraints: list[RecommendationConstraint]
        | tuple[RecommendationConstraint, ...] = (),
    ) -> None:
        self._set_id = RecommendationValidationPolicy.assert_identity(set_id)
        self._student_id = RecommendationValidationPolicy.assert_student_id(
            student_id
        )
        self._recommended_at = (
            RecommendationValidationPolicy.assert_recommended_at(recommended_at)
        )
        self._recommendations = (
            RecommendationValidationPolicy.assert_recommendations(recommendations)
        )
        self._constraints = RecommendationValidationPolicy.assert_constraints(
            constraints
        )

    # --- identity / read models (no setters; sets are immutable) ---

    @property
    def set_id(self) -> RecommendationSetId:
        return self._set_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def recommended_at(self) -> datetime:
        return self._recommended_at

    @property
    def recommendations(self) -> tuple[Recommendation, ...]:
        return tuple(self._recommendations)

    @property
    def constraints(self) -> tuple[RecommendationConstraint, ...]:
        return tuple(self._constraints)

    # --- queries ---

    def recommendation_count(self) -> int:
        return len(self._recommendations)

    def is_empty(self) -> bool:
        return not self._recommendations

    def highest_priority(self) -> Recommendation | None:
        if not self._recommendations:
            return None
        return self._recommendations[0]

    def recommendations_for_subject(
        self, subject_id: SubjectId
    ) -> tuple[Recommendation, ...]:
        return tuple(
            recommendation
            for recommendation in self._recommendations
            if recommendation.target.subject_id is not None
            and recommendation.target.subject_id == subject_id
        )

    def recommendations_for_competency(
        self, competency_id: CompetencyId
    ) -> tuple[Recommendation, ...]:
        return tuple(
            recommendation
            for recommendation in self._recommendations
            if recommendation.target.competency_id is not None
            and recommendation.target.competency_id == competency_id
        )

    def recommendations_of_category(
        self, category: RecommendationCategory
    ) -> tuple[Recommendation, ...]:
        return tuple(
            recommendation
            for recommendation in self._recommendations
            if recommendation.category is category
        )

    def highest_impact_actions(
        self, *, limit: int = 3
    ) -> tuple[Recommendation, ...]:
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            limit = 1
        high_impact = [
            recommendation
            for recommendation in self._recommendations
            if ImpactPolicy.is_highest_impact(recommendation.impact)
        ]
        return tuple(high_impact[:limit])

    def has_blocking_constraints(self) -> bool:
        return any(
            constraint.blocks_advancement() for constraint in self._constraints
        )

    def produce_snapshot(self) -> RecommendationSnapshot:
        return RecommendationSnapshot(
            set_id=self._set_id,
            student_id=self._student_id,
            recommendations=self.recommendations,
            constraints=self.constraints,
            recommended_at=self._recommended_at,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RecommendationSet):
            return NotImplemented
        return (
            self._set_id == other._set_id
            and self._student_id == other._student_id
            and self._recommended_at == other._recommended_at
            and self._recommendations == other._recommendations
            and self._constraints == other._constraints
        )

    def __hash__(self) -> int:
        return hash(self._set_id)
