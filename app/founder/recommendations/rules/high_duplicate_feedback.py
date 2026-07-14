"""Rule 4 — High duplicate feedback (FOS-006)."""

from __future__ import annotations

from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.config import (
    CATEGORY_FEEDBACK,
    DUPLICATE_FEEDBACK_ABSOLUTE_THRESHOLD,
    DUPLICATE_FEEDBACK_RATIO_THRESHOLD,
    PRIORITY_HIGH,
    TEMPLATE_PRIORITISE_RECURRING_ISSUES,
)
from app.founder.recommendations.dto import RuleOutcome
from app.founder.recommendations.models import RecommendationEvidence


class HighDuplicateFeedbackRule:
    """Recommend prioritising recurring issues when duplicates are high."""

    def __init__(
        self,
        *,
        absolute_threshold: int = DUPLICATE_FEEDBACK_ABSOLUTE_THRESHOLD,
        ratio_threshold: float = DUPLICATE_FEEDBACK_RATIO_THRESHOLD,
    ) -> None:
        self._absolute_threshold = absolute_threshold
        self._ratio_threshold = ratio_threshold

    @property
    def rule_id(self) -> str:
        return "high_duplicate_feedback"

    def evaluate(self, state: FounderOperationalState) -> RuleOutcome | None:
        feedback_count = state.internal_alpha.feedback_count
        duplicate_count = state.internal_alpha.duplicate_count
        if feedback_count <= 0:
            return None
        ratio = duplicate_count / feedback_count
        high_duplicates = (
            duplicate_count >= self._absolute_threshold
            or ratio >= self._ratio_threshold
        )
        if not high_duplicates:
            return None
        return RuleOutcome(
            rule_id=self.rule_id,
            template_id=TEMPLATE_PRIORITISE_RECURRING_ISSUES,
            category=CATEGORY_FEEDBACK,
            priority=PRIORITY_HIGH,
            evidence=(
                RecommendationEvidence(
                    source="internal_alpha",
                    metric="duplicate_count",
                    value=duplicate_count,
                ),
                RecommendationEvidence(
                    source="internal_alpha",
                    metric="feedback_count",
                    value=feedback_count,
                ),
                RecommendationEvidence(
                    source="internal_alpha",
                    metric="duplicate_ratio",
                    value=round(ratio, 4),
                ),
            ),
        )
