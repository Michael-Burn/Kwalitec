"""Rule 2 — Archive validation failed (FOS-006)."""

from __future__ import annotations

from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.config import (
    CATEGORY_ARCHIVE,
    PRIORITY_CRITICAL,
    TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES,
)
from app.founder.recommendations.dto import RuleOutcome
from app.founder.recommendations.models import RecommendationEvidence


class ArchiveValidationFailedRule:
    """Recommend resolving archive inconsistencies when any are present."""

    @property
    def rule_id(self) -> str:
        return "archive_validation_failed"

    def evaluate(self, state: FounderOperationalState) -> RuleOutcome | None:
        inconsistencies = state.capability.archive_inconsistencies
        if inconsistencies <= 0:
            return None
        return RuleOutcome(
            rule_id=self.rule_id,
            template_id=TEMPLATE_RESOLVE_ARCHIVE_INCONSISTENCIES,
            category=CATEGORY_ARCHIVE,
            priority=PRIORITY_CRITICAL,
            evidence=(
                RecommendationEvidence(
                    source="capability",
                    metric="archive_inconsistencies",
                    value=inconsistencies,
                ),
                RecommendationEvidence(
                    source="capability",
                    metric="total_count",
                    value=state.capability.total_count,
                ),
            ),
        )
