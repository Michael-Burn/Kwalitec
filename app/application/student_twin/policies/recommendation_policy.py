"""Stateless recommendation policy — smallest helpful intervention."""

from __future__ import annotations

from app.domain.student_twin.confidence_band import ConfidenceBand
from app.domain.student_twin.recommendation_state import RecommendationKind


class RecommendationPolicy:
    """Educational rules for Twin recommendations.

    Prefer the smallest intervention that improves long-term mastery.
    Never optimise engagement or screen time.
    """

    LOW_MASTERY_THRESHOLD = 0.40
    LOW_RETENTION_THRESHOLD = 0.45
    HIGH_MASTERY_THRESHOLD = 0.80
    HIGH_VELOCITY_EVENTS_PER_DAY = 8.0
    MAX_RECOMMENDATIONS = 5

    @staticmethod
    def should_take_break(events_per_day: float) -> bool:
        """True when recent study intensity suggests rest."""
        return events_per_day >= RecommendationPolicy.HIGH_VELOCITY_EVENTS_PER_DAY

    @staticmethod
    def should_stop_studying(
        *,
        overall_mastery: float,
        overall_retention: float,
        readiness: float,
    ) -> bool:
        """True when further study is unlikely to help today."""
        return (
            overall_mastery >= RecommendationPolicy.HIGH_MASTERY_THRESHOLD
            and overall_retention >= RecommendationPolicy.HIGH_MASTERY_THRESHOLD
            and readiness >= 0.75
        )

    @staticmethod
    def kind_for_weakness(
        *,
        mastery: float,
        retention: float,
        confidence: ConfidenceBand,
    ) -> RecommendationKind:
        """Select recommendation kind from weakness signals."""
        if mastery < RecommendationPolicy.LOW_MASTERY_THRESHOLD:
            return RecommendationKind.PRACTICE_TOPIC
        if retention < RecommendationPolicy.LOW_RETENTION_THRESHOLD:
            return RecommendationKind.REVISE_TOPIC
        if confidence in (ConfidenceBand.VERY_LOW, ConfidenceBand.LOW):
            return RecommendationKind.BUILD_CONFIDENCE
        return RecommendationKind.CONTINUE_CURRENT

    @staticmethod
    def expected_benefit_for(kind: RecommendationKind) -> str:
        """Deterministic expected-benefit phrase for a recommendation kind."""
        mapping = {
            RecommendationKind.REVISE_TOPIC: "improve_long_term_retention",
            RecommendationKind.PRACTICE_TOPIC: "raise_demonstrated_mastery",
            RecommendationKind.REPEAT_YESTERDAY: "consolidate_recent_learning",
            RecommendationKind.SKIP_TOPIC: "avoid_unnecessary_study",
            RecommendationKind.TAKE_BREAK: "protect_learning_quality",
            RecommendationKind.STOP_STUDYING: "prevent_diminishing_returns",
            RecommendationKind.CONTINUE_CURRENT: "maintain_learning_momentum",
            RecommendationKind.BUILD_CONFIDENCE: "reduce_uncertainty_with_evidence",
        }
        return mapping[kind]
