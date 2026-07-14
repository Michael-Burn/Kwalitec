"""Rule 1 — No Internal Alpha feedback (FOS-006)."""

from __future__ import annotations

from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.config import (
    CATEGORY_RELEASE,
    PRIORITY_HIGH,
    TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
)
from app.founder.recommendations.dto import RuleOutcome
from app.founder.recommendations.models import RecommendationEvidence


class NoInternalAlphaFeedbackRule:
    """Recommend waiting for Internal Alpha when no feedback exists."""

    @property
    def rule_id(self) -> str:
        return "no_internal_alpha_feedback"

    def evaluate(self, state: FounderOperationalState) -> RuleOutcome | None:
        feedback_count = state.internal_alpha.feedback_count
        if feedback_count > 0:
            return None
        return RuleOutcome(
            rule_id=self.rule_id,
            template_id=TEMPLATE_WAIT_FOR_INTERNAL_ALPHA,
            category=CATEGORY_RELEASE,
            priority=PRIORITY_HIGH,
            evidence=(
                RecommendationEvidence(
                    source="internal_alpha",
                    metric="feedback_count",
                    value=feedback_count,
                ),
                RecommendationEvidence(
                    source="internal_alpha",
                    metric="current_week",
                    value=state.internal_alpha.current_week or "(none)",
                ),
            ),
        )
