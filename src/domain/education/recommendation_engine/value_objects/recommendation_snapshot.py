"""Recommendation snapshot — immutable mirror of a RecommendationSet.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Recommendation Snapshot
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.recommendation_engine.enums import RecommendationImpactBand
from domain.education.recommendation_engine.ids import RecommendationSetId
from domain.education.recommendation_engine.value_objects.recommendation import (
    Recommendation,
)
from domain.education.recommendation_engine.value_objects.recommendation_constraint import (  # noqa: E501
    RecommendationConstraint,
)


@dataclass(frozen=True, slots=True)
class RecommendationSnapshot(EducationalValueObject):
    """Immutable, accurate capture of a RecommendationSet aggregate.

    A snapshot is a read model. It does not re-recommend or recompute — it
    faithfully mirrors the set at the moment it was produced.
    """

    set_id: RecommendationSetId
    student_id: str
    recommendations: tuple[Recommendation, ...]
    constraints: tuple[RecommendationConstraint, ...]
    recommended_at: datetime

    def _validate(self) -> None:
        if not isinstance(self.set_id, RecommendationSetId):
            raise EducationalInvariantViolation(
                "set_id must be a RecommendationSetId",
                invariant="RecommendationSnapshot.set_id.type",
            )
        if not isinstance(self.student_id, str) or not self.student_id.strip():
            raise EducationalInvariantViolation(
                "student_id must be a non-empty string",
                invariant="RecommendationSnapshot.student_id.required",
            )
        object.__setattr__(self, "recommendations", tuple(self.recommendations))
        for recommendation in self.recommendations:
            if not isinstance(recommendation, Recommendation):
                raise EducationalInvariantViolation(
                    "recommendations must contain Recommendation value objects",
                    invariant="RecommendationSnapshot.recommendations.type",
                )
        object.__setattr__(self, "constraints", tuple(self.constraints))
        for constraint in self.constraints:
            if not isinstance(constraint, RecommendationConstraint):
                raise EducationalInvariantViolation(
                    "constraints must contain RecommendationConstraint "
                    "value objects",
                    invariant="RecommendationSnapshot.constraints.type",
                )
        if not isinstance(self.recommended_at, datetime):
            raise EducationalInvariantViolation(
                "recommended_at must be a datetime",
                invariant="RecommendationSnapshot.recommended_at.type",
            )

    def recommendation_count(self) -> int:
        return len(self.recommendations)

    def high_impact_count(self) -> int:
        return sum(
            1
            for recommendation in self.recommendations
            if recommendation.impact.band is RecommendationImpactBand.HIGH
        )

    def highest_priority(self) -> Recommendation | None:
        if not self.recommendations:
            return None
        return self.recommendations[0]
