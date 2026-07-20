"""RecommendationSpecification — deterministic educational recommendation set.

Architecture Source
    EDUCATIONAL_LOGIC_REGISTRY.md (EL-008)
Concept
    Recommendation Specification
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    DiagnosisId,
    DigitalTwinId,
    PriorityId,
    TeachingStrategyId,
)
from domain.mission_generation.ids import MissionSpecificationId
from domain.progress_evaluation.ids import ProgressReportId
from domain.recommendation.enums import RecommendationCategory
from domain.recommendation.ids import RecommendationSpecificationId
from domain.recommendation.recommendation import Recommendation
from domain.study_planning.ids import StudyPlanId


@dataclass(frozen=True, slots=True)
class RecommendationSpecification(EducationalValueObject):
    """Fully explainable recommendation projection from Educational OS state.

    A RecommendationSpecification is a pure educational decision set: ordered
    recommendations with reasons, priorities, expected outcomes, supporting
    evidence, and confidence. It does not persist, invoke AI, or present UI.
    """

    specification_id: RecommendationSpecificationId
    student_id: str
    recommendations: tuple[Recommendation, ...]
    educational_rationale: str
    twin_id: DigitalTwinId
    mission_id: MissionSpecificationId
    plan_id: StudyPlanId
    progress_report_id: ProgressReportId
    diagnosis_id: DiagnosisId
    priority_id: PriorityId
    strategy_id: TeachingStrategyId

    def _validate(self) -> None:
        if not isinstance(self.specification_id, RecommendationSpecificationId):
            raise EducationalInvariantViolation(
                "specification_id must be a RecommendationSpecificationId",
                invariant="RecommendationSpecification.specification_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_non_empty_text(self.student_id, "student_id"),
        )
        if not isinstance(self.recommendations, tuple) or not self.recommendations:
            raise EducationalInvariantViolation(
                "recommendations must be a non-empty tuple",
                invariant="RecommendationSpecification.recommendations.min_one",
            )
        seen: set[str] = set()
        for recommendation in self.recommendations:
            if not isinstance(recommendation, Recommendation):
                raise EducationalInvariantViolation(
                    "recommendations must contain Recommendation values",
                    invariant="RecommendationSpecification.recommendations.item_type",
                )
            if recommendation.recommendation_id.value in seen:
                raise EducationalInvariantViolation(
                    "recommendation identities must be unique",
                    invariant="RecommendationSpecification.recommendations.unique",
                )
            seen.add(recommendation.recommendation_id.value)
        object.__setattr__(
            self,
            "educational_rationale",
            require_non_empty_text(
                self.educational_rationale, "educational_rationale"
            ),
        )
        if len(self.educational_rationale) < 24:
            raise EducationalInvariantViolation(
                "educational rationale must be educationally substantive",
                invariant="RecommendationSpecification.educational_rationale.substantive",
            )
        for name, value, expected in (
            ("twin_id", self.twin_id, DigitalTwinId),
            ("mission_id", self.mission_id, MissionSpecificationId),
            ("plan_id", self.plan_id, StudyPlanId),
            ("progress_report_id", self.progress_report_id, ProgressReportId),
            ("diagnosis_id", self.diagnosis_id, DiagnosisId),
            ("priority_id", self.priority_id, PriorityId),
            ("strategy_id", self.strategy_id, TeachingStrategyId),
        ):
            if not isinstance(value, expected):
                raise EducationalInvariantViolation(
                    f"{name} must be a {expected.__name__}",
                    invariant=f"RecommendationSpecification.{name}.type",
                )

    @property
    def primary(self) -> Recommendation:
        """Highest-priority recommendation (first in ordered tuple)."""
        return self.recommendations[0]

    def recommendation_count(self) -> int:
        return len(self.recommendations)

    def categories(self) -> tuple[RecommendationCategory, ...]:
        return tuple(item.category for item in self.recommendations)

    def has_category(self, category: RecommendationCategory) -> bool:
        return any(item.category is category for item in self.recommendations)
