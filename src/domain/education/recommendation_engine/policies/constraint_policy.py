"""Constraint policy — derives educational constraints from signals.

Architecture Source
    PROJECT_CONTEXT.md
Concept
    Constraint Policy
"""

from __future__ import annotations

from collections.abc import Sequence

from domain.education.mastery_estimation.enums import KnowledgeGapKind
from domain.education.mastery_estimation.value_objects.competency_assessment import (
    CompetencyAssessment,
)
from domain.education.mastery_estimation.value_objects.knowledge_gap import (
    KnowledgeGap,
)
from domain.education.recommendation_engine.enums import RecommendationConstraintKind
from domain.education.recommendation_engine.ids import CompetencyId, SubjectId
from domain.education.recommendation_engine.value_objects.recommendation_constraint import (  # noqa: E501
    RecommendationConstraint,
)


class ConstraintPolicy:
    """Deterministically derives educational constraints."""

    @staticmethod
    def constraints_for_gap(
        gap: KnowledgeGap,
        *,
        subject_id: SubjectId,
    ) -> tuple[RecommendationConstraint, ...]:
        if gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE:
            return (
                RecommendationConstraint(
                    kind=RecommendationConstraintKind.REQUIRE_PREREQUISITE,
                    subject_id=subject_id,
                    competency_id=CompetencyId(gap.competency_id.value),
                    detail=gap.mastery_score.magnitude,
                ),
                RecommendationConstraint(
                    kind=RecommendationConstraintKind.BLOCK_ADVANCEMENT,
                    subject_id=subject_id,
                    competency_id=(
                        CompetencyId(gap.related_competency_id.value)
                        if gap.related_competency_id is not None
                        else CompetencyId(gap.competency_id.value)
                    ),
                    detail=gap.mastery_score.magnitude,
                ),
            )
        return (
            RecommendationConstraint(
                kind=RecommendationConstraintKind.LIMIT_SCOPE,
                subject_id=subject_id,
                competency_id=CompetencyId(gap.competency_id.value),
                detail=gap.mastery_score.magnitude,
            ),
        )

    @staticmethod
    def constraints_for_competency(
        assessment: CompetencyAssessment,
        *,
        subject_id: SubjectId,
    ) -> tuple[RecommendationConstraint, ...]:
        constraints: list[RecommendationConstraint] = []
        for gap in assessment.gaps:
            constraints.extend(
                ConstraintPolicy.constraints_for_gap(gap, subject_id=subject_id)
            )
        if ConstraintPolicy.should_defer_checkpoint(assessment):
            constraints.append(
                RecommendationConstraint(
                    kind=RecommendationConstraintKind.DEFER_CHECKPOINT,
                    subject_id=subject_id,
                    competency_id=CompetencyId(assessment.competency_id.value),
                    detail=assessment.mastery.magnitude,
                )
            )
        return tuple(constraints)

    @staticmethod
    def should_defer_checkpoint(assessment: CompetencyAssessment) -> bool:
        """Defer checkpoint attempts when mastery is weak or contradicted."""
        if assessment.confidence.is_contradicted():
            return True
        return any(
            gap.kind is KnowledgeGapKind.WEAK_PREREQUISITE
            for gap in assessment.gaps
        )

    @staticmethod
    def preserve_mission_constraint(
        *,
        subject_id: SubjectId | None = None,
    ) -> RecommendationConstraint:
        return RecommendationConstraint(
            kind=RecommendationConstraintKind.PRESERVE_MISSION,
            subject_id=subject_id,
        )

    @staticmethod
    def aggregate_set_constraints(
        constraints: Sequence[RecommendationConstraint],
    ) -> tuple[RecommendationConstraint, ...]:
        """Deduplicate set-level constraints by (kind, competency, subject)."""
        seen: set[tuple[str, str, str]] = set()
        unique: list[RecommendationConstraint] = []
        for constraint in constraints:
            key = (
                constraint.kind.value,
                constraint.competency_id.value
                if constraint.competency_id is not None
                else "",
                constraint.subject_id.value
                if constraint.subject_id is not None
                else "",
            )
            if key in seen:
                continue
            seen.add(key)
            unique.append(constraint)
        return tuple(unique)
