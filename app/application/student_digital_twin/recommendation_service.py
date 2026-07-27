"""Recommendation generation — delegates to RecommendationRule (SDT-002)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.domain.educational_reasoning.reasoning_context import (
    CurriculumEvidenceBundle,
    ReasoningContext,
)
from app.domain.educational_reasoning.recommendation_rule import RecommendationRule
from app.domain.student_digital_twin.knowledge_gap import KnowledgeGap
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.recommendation import Recommendation


class RecommendationService:
    """Produce explainable educational recommendations via RecommendationRule."""

    def generate(
        self,
        *,
        twin_id: str,
        gaps: tuple[KnowledgeGap, ...],
    ) -> tuple[Recommendation, ...]:
        now = datetime.now(UTC).replace(tzinfo=None)
        context = ReasoningContext(
            twin_id=twin_id,
            student_id=twin_id,
            workspace_id="",
            subject_code="",
            observations=(),
            observation_ids=(),
            prior_mastery=MasteryMap.empty(),
            curriculum_evidence=CurriculumEvidenceBundle.empty(),
            triggered_by="recommendation_service",
            computed_at=now,
            gaps=gaps,
        )
        execution = RecommendationRule().apply(context)
        return execution.recommendations or ()
