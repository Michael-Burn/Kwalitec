"""Recommendation service — explainable Twin recommendations."""

from __future__ import annotations

from app.application.student_twin.policies.recommendation_policy import (
    RecommendationPolicy,
)
from app.domain.student_twin.confidence_band import ConfidenceBand
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.learning_velocity import LearningVelocity
from app.domain.student_twin.mastery_state import MasteryState
from app.domain.student_twin.readiness_state import ReadinessState
from app.domain.student_twin.recommendation_state import (
    Recommendation,
    RecommendationKind,
    RecommendationState,
)
from app.domain.student_twin.retention_state import RetentionState
from app.domain.student_twin.weakness_profile import WeaknessProfile


class RecommendationService:
    """Produce explainable recommendations from Twin educational state."""

    @staticmethod
    def recommend(
        mastery: MasteryState,
        retention: RetentionState,
        readiness: ReadinessState,
        weaknesses: WeaknessProfile,
        velocity: LearningVelocity,
    ) -> RecommendationState:
        """Build ordered recommendations with evidence and rationale."""
        recommendations: list[Recommendation] = []
        evidence_pool = list(
            dict.fromkeys(
                (
                    *mastery.evidence_ids,
                    *retention.evidence_ids,
                    *readiness.evidence_ids,
                    *weaknesses.evidence_ids,
                    *velocity.evidence_ids,
                )
            )
        )

        if RecommendationPolicy.should_take_break(velocity.events_per_day):
            recommendations.append(
                Recommendation.create(
                    "rec-take-break",
                    RecommendationKind.TAKE_BREAK,
                    priority=0.95,
                    confidence=velocity.confidence,
                    evidence_ids=velocity.evidence_ids,
                    rationale="high_recent_study_intensity",
                    expected_benefit=RecommendationPolicy.expected_benefit_for(
                        RecommendationKind.TAKE_BREAK
                    ),
                )
            )

        if RecommendationPolicy.should_stop_studying(
            overall_mastery=mastery.overall_score,
            overall_retention=retention.overall_score,
            readiness=readiness.readiness_score,
        ):
            recommendations.append(
                Recommendation.create(
                    "rec-stop",
                    RecommendationKind.STOP_STUDYING,
                    priority=0.90,
                    confidence=readiness.confidence,
                    evidence_ids=evidence_pool[:8],
                    rationale="high_mastery_retention_readiness",
                    expected_benefit=RecommendationPolicy.expected_benefit_for(
                        RecommendationKind.STOP_STUDYING
                    ),
                )
            )

        mastery_by = {r.topic_id: r for r in mastery.topic_records}
        retention_by = {r.topic_id: r for r in retention.topic_records}

        for index, weakness in enumerate(weaknesses.items):
            if len(recommendations) >= RecommendationPolicy.MAX_RECOMMENDATIONS:
                break
            m = mastery_by.get(weakness.topic_id)
            r = retention_by.get(weakness.topic_id)
            kind = RecommendationPolicy.kind_for_weakness(
                mastery=m.mastery_score if m else 0.0,
                retention=r.retention_score if r else 0.0,
                confidence=weakness.confidence,
            )
            priority = max(0.1, min(0.89, weakness.severity * 0.85))
            recommendations.append(
                Recommendation.create(
                    f"rec-weak-{index}-{weakness.topic_id}",
                    kind,
                    topic_id=weakness.topic_id,
                    priority=priority,
                    confidence=weakness.confidence,
                    evidence_ids=weakness.evidence_ids,
                    rationale=weakness.rationale or weakness.kind.value,
                    expected_benefit=RecommendationPolicy.expected_benefit_for(kind),
                )
            )

        if not recommendations:
            recommendations.append(
                Recommendation.create(
                    "rec-continue",
                    RecommendationKind.CONTINUE_CURRENT,
                    priority=0.40,
                    confidence=(
                        readiness.confidence
                        if mastery.topic_records
                        else ConfidenceBand.VERY_LOW
                    ),
                    evidence_ids=evidence_pool[:4],
                    rationale=(
                        "insufficient_evidence"
                        if not mastery.topic_records
                        else "no_urgent_weakness"
                    ),
                    expected_benefit=RecommendationPolicy.expected_benefit_for(
                        RecommendationKind.CONTINUE_CURRENT
                    ),
                )
            )

        recommendations.sort(key=lambda rec: (-rec.priority, rec.recommendation_id))
        capped = recommendations[: RecommendationPolicy.MAX_RECOMMENDATIONS]
        overall = capped[0].confidence if capped else ConfidenceBand.VERY_LOW
        return RecommendationState.create(
            capped,
            overall_confidence=overall,
            evidence_ids=evidence_pool,
        )

    @staticmethod
    def from_twin(twin: DigitalTwin) -> RecommendationState:
        """Recommend from Twin component states."""
        return RecommendationService.recommend(
            twin.mastery,
            twin.retention,
            twin.readiness,
            twin.weaknesses,
            twin.velocity,
        )
