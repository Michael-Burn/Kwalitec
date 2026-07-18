"""Explanation service — educational explanations for adaptive decisions."""

from __future__ import annotations

from app.application.adaptive_learning.dto.decision_snapshot import (
    DecisionExplanationDTO,
)
from app.application.adaptive_learning.exceptions import ExplanationError
from app.domain.adaptive_learning.adaptive_decision import AdaptiveDecision
from app.domain.adaptive_learning.decision_explanation import DecisionExplanation
from app.domain.adaptive_learning.intervention import Intervention


class ExplanationService:
    """Produce educational explanations for adaptive decisions."""

    @staticmethod
    def explain_decision(decision: AdaptiveDecision) -> DecisionExplanationDTO:
        """Explain a complete adaptive decision."""
        return DecisionExplanationDTO.from_explanation(
            decision.explanation,
            decision_id=decision.decision_id,
            topic_id=decision.primary_topic_id,
            intervention_type=decision.intervention_type.value,
            estimated_study_minutes=decision.estimated_study_minutes,
            educational_benefit=decision.roi.educational_benefit,
            confidence=decision.confidence.value,
        )

    @staticmethod
    def explain_intervention(intervention: Intervention) -> DecisionExplanationDTO:
        """Explain a single intervention."""
        return DecisionExplanationDTO.from_explanation(
            intervention.explanation,
            decision_id=intervention.intervention_id,
            topic_id=intervention.topic_id,
            intervention_type=intervention.intervention_type.value,
            estimated_study_minutes=intervention.estimated_study_minutes,
            educational_benefit=intervention.roi.educational_benefit,
            confidence=intervention.confidence.value,
        )

    @staticmethod
    def require_complete(explanation: DecisionExplanation) -> DecisionExplanation:
        """Validate that an explanation carries required educational fields."""
        if not explanation.rationale:
            raise ExplanationError("explanation missing rationale")
        if not explanation.expected_educational_benefit:
            raise ExplanationError("explanation missing expected educational benefit")
        if explanation.priority_score < 0.0:
            raise ExplanationError("explanation has invalid priority")
        return explanation
