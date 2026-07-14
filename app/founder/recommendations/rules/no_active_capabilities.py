"""Rule 5 — No active capabilities (FOS-006)."""

from __future__ import annotations

from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.config import (
    CATEGORY_ROADMAP,
    PRIORITY_MEDIUM,
    TEMPLATE_SELECT_ROADMAP_CAPABILITY,
)
from app.founder.recommendations.dto import RuleOutcome
from app.founder.recommendations.models import RecommendationEvidence


class NoActiveCapabilitiesRule:
    """Recommend selecting a roadmap capability when none are active."""

    @property
    def rule_id(self) -> str:
        return "no_active_capabilities"

    def evaluate(self, state: FounderOperationalState) -> RuleOutcome | None:
        active_count = state.capability.active_count
        if active_count > 0:
            return None
        recent = state.capability.recent_capability_ids
        return RuleOutcome(
            rule_id=self.rule_id,
            template_id=TEMPLATE_SELECT_ROADMAP_CAPABILITY,
            category=CATEGORY_ROADMAP,
            priority=PRIORITY_MEDIUM,
            evidence=(
                RecommendationEvidence(
                    source="capability",
                    metric="active_count",
                    value=active_count,
                ),
                RecommendationEvidence(
                    source="capability",
                    metric="completed_count",
                    value=state.capability.completed_count,
                ),
                RecommendationEvidence(
                    source="capability",
                    metric="recent_capability_ids",
                    value=",".join(recent) if recent else "(none)",
                ),
                RecommendationEvidence(
                    source="release",
                    metric="current_release",
                    value=state.release.current_release,
                ),
            ),
        )
