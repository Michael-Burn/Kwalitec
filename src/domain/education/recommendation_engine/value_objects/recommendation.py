"""Recommendation — a single immutable educational recommendation.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.enums import RecommendationCategory
from domain.education.recommendation_engine.ids import RecommendationId
from domain.education.recommendation_engine.value_objects.recommendation_confidence import (  # noqa: E501
    RecommendationConfidence,
)
from domain.education.recommendation_engine.value_objects.recommendation_constraint import (  # noqa: E501
    RecommendationConstraint,
)
from domain.education.recommendation_engine.value_objects.recommendation_explanation import (  # noqa: E501
    RecommendationExplanation,
)
from domain.education.recommendation_engine.value_objects.recommendation_impact import (
    RecommendationImpact,
)
from domain.education.recommendation_engine.value_objects.recommendation_ordering import (  # noqa: E501
    RecommendationOrdering,
)
from domain.education.recommendation_engine.value_objects.recommendation_priority import (  # noqa: E501
    RecommendationPriority,
)
from domain.education.recommendation_engine.value_objects.recommendation_target import (
    RecommendationTarget,
)


@dataclass(frozen=True, slots=True)
class Recommendation(EducationalValueObject):
    """Immutable educational recommendation expressing educational intent.

    A Recommendation is the atomic product of the Recommendation Engine —
    category, target, priority, impact, confidence, constraints, and
    structured explanation. It never mutates, never persists, and never
    encodes UI actions or mission tasks.
    """

    recommendation_id: RecommendationId
    category: RecommendationCategory
    target: RecommendationTarget
    priority: RecommendationPriority
    impact: RecommendationImpact
    confidence: RecommendationConfidence
    explanation: RecommendationExplanation
    ordering: RecommendationOrdering
    constraints: tuple[RecommendationConstraint, ...] = ()

    def _validate(self) -> None:
        if not isinstance(self.recommendation_id, RecommendationId):
            raise EducationalInvariantViolation(
                "recommendation_id must be a RecommendationId",
                invariant="Recommendation.recommendation_id.type",
            )
        if not isinstance(self.category, RecommendationCategory):
            raise EducationalInvariantViolation(
                "category must be a RecommendationCategory",
                invariant="Recommendation.category.type",
            )
        if not isinstance(self.target, RecommendationTarget):
            raise EducationalInvariantViolation(
                "target must be a RecommendationTarget",
                invariant="Recommendation.target.type",
            )
        if not isinstance(self.priority, RecommendationPriority):
            raise EducationalInvariantViolation(
                "priority must be a RecommendationPriority",
                invariant="Recommendation.priority.type",
            )
        if not isinstance(self.impact, RecommendationImpact):
            raise EducationalInvariantViolation(
                "impact must be a RecommendationImpact",
                invariant="Recommendation.impact.type",
            )
        if not isinstance(self.confidence, RecommendationConfidence):
            raise EducationalInvariantViolation(
                "confidence must be a RecommendationConfidence",
                invariant="Recommendation.confidence.type",
            )
        if not isinstance(self.explanation, RecommendationExplanation):
            raise EducationalInvariantViolation(
                "explanation must be a RecommendationExplanation",
                invariant="Recommendation.explanation.type",
            )
        if not isinstance(self.ordering, RecommendationOrdering):
            raise EducationalInvariantViolation(
                "ordering must be a RecommendationOrdering",
                invariant="Recommendation.ordering.type",
            )
        if self.ordering.priority != self.priority:
            raise EducationalInvariantViolation(
                "ordering.priority must match recommendation priority",
                invariant="Recommendation.ordering.priority.consistent",
            )
        object.__setattr__(self, "constraints", tuple(self.constraints))
        for constraint in self.constraints:
            if not isinstance(constraint, RecommendationConstraint):
                raise EducationalInvariantViolation(
                    "constraints must contain RecommendationConstraint "
                    "value objects",
                    invariant="Recommendation.constraints.type",
                )

    def with_ordering(self, ordering: RecommendationOrdering) -> Recommendation:
        """Return a new Recommendation carrying an updated ordering."""
        return Recommendation(
            recommendation_id=self.recommendation_id,
            category=self.category,
            target=self.target,
            priority=self.priority,
            impact=self.impact,
            confidence=self.confidence,
            explanation=self.explanation,
            ordering=ordering,
            constraints=self.constraints,
        )

    def is_high_impact(self) -> bool:
        return self.impact.band.value == "high"

    def __str__(self) -> str:
        return (
            f"{self.category.value}@{self.target.correlation_key()}"
            f":{self.priority.band.value}"
        )
