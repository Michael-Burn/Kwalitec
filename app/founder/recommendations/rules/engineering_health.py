"""Rule 3 — Engineering health below threshold (FOS-006)."""

from __future__ import annotations

from app.founder.operational_state.models import FounderOperationalState
from app.founder.recommendations.config import (
    CATEGORY_ENGINEERING,
    ENGINEERING_VALIDATION_ERROR_THRESHOLD,
    PRIORITY_CRITICAL,
    TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH,
)
from app.founder.recommendations.dto import RuleOutcome
from app.founder.recommendations.models import RecommendationEvidence


class EngineeringHealthBelowThresholdRule:
    """Recommend pausing new capabilities when engineering health is weak."""

    def __init__(
        self,
        *,
        validation_error_threshold: int = ENGINEERING_VALIDATION_ERROR_THRESHOLD,
    ) -> None:
        self._validation_error_threshold = validation_error_threshold

    @property
    def rule_id(self) -> str:
        return "engineering_health_below_threshold"

    def evaluate(self, state: FounderOperationalState) -> RuleOutcome | None:
        tests_pass = state.engineering.tests_pass
        validation_errors = state.engineering.validation_errors
        unhealthy = (not tests_pass) or (
            validation_errors > self._validation_error_threshold
        )
        if not unhealthy:
            return None
        return RuleOutcome(
            rule_id=self.rule_id,
            template_id=TEMPLATE_PAUSE_FOR_ENGINEERING_HEALTH,
            category=CATEGORY_ENGINEERING,
            priority=PRIORITY_CRITICAL,
            evidence=(
                RecommendationEvidence(
                    source="engineering",
                    metric="tests_pass",
                    value=tests_pass,
                ),
                RecommendationEvidence(
                    source="engineering",
                    metric="validation_errors",
                    value=validation_errors,
                ),
                RecommendationEvidence(
                    source="engineering",
                    metric="standards_count",
                    value=state.engineering.standards_count,
                ),
            ),
        )
