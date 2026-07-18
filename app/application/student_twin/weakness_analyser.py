"""Weakness analyser — surface educational weaknesses from Twin state."""

from __future__ import annotations

from app.application.student_twin.policies.recommendation_policy import (
    RecommendationPolicy,
)
from app.domain.student_twin.confidence_band import ConfidenceBand
from app.domain.student_twin.confidence_state import ConfidenceState
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.mastery_state import MasteryState
from app.domain.student_twin.retention_state import RetentionState
from app.domain.student_twin.weakness_profile import (
    WeaknessItem,
    WeaknessKind,
    WeaknessProfile,
)


class WeaknessAnalyser:
    """Derive an ordered WeaknessProfile from Twin component states."""

    @staticmethod
    def analyse(
        mastery: MasteryState,
        retention: RetentionState,
        confidence: ConfidenceState,
    ) -> WeaknessProfile:
        """Analyse weaknesses; highest severity first."""
        items: list[WeaknessItem] = []
        evidence_ids: list[str] = []

        mastery_by_topic = {r.topic_id: r for r in mastery.topic_records}
        retention_by_topic = {r.topic_id: r for r in retention.topic_records}
        confidence_by_topic = {r.topic_id: r for r in confidence.topic_records}
        topic_ids = sorted(
            set(mastery_by_topic)
            | set(retention_by_topic)
            | set(confidence_by_topic)
        )

        for topic_id in topic_ids:
            m = mastery_by_topic.get(topic_id)
            r = retention_by_topic.get(topic_id)
            c = confidence_by_topic.get(topic_id)
            if (
                m is not None
                and m.mastery_score < RecommendationPolicy.LOW_MASTERY_THRESHOLD
            ):
                sev = 1.0 - m.mastery_score
                items.append(
                    WeaknessItem.create(
                        topic_id,
                        WeaknessKind.LOW_MASTERY,
                        sev,
                        confidence=m.confidence,
                        evidence_ids=m.evidence_ids,
                        rationale="mastery_below_threshold",
                    )
                )
                evidence_ids.extend(m.evidence_ids)
            if (
                r is not None
                and r.retention_score < RecommendationPolicy.LOW_RETENTION_THRESHOLD
            ):
                sev = 1.0 - r.retention_score
                items.append(
                    WeaknessItem.create(
                        topic_id,
                        WeaknessKind.LOW_RETENTION,
                        sev,
                        confidence=r.confidence,
                        evidence_ids=r.evidence_ids,
                        rationale="retention_below_threshold",
                    )
                )
                evidence_ids.extend(r.evidence_ids)
            if c is not None and c.confidence_band in (
                ConfidenceBand.VERY_LOW,
                ConfidenceBand.LOW,
            ):
                sev = 1.0 - c.confidence_score
                items.append(
                    WeaknessItem.create(
                        topic_id,
                        WeaknessKind.LOW_CONFIDENCE,
                        sev,
                        confidence=c.confidence_band,
                        evidence_ids=c.evidence_ids,
                        rationale="confidence_band_low",
                    )
                )
                evidence_ids.extend(c.evidence_ids)

        items.sort(key=lambda item: (-item.severity, item.topic_id, item.kind.value))
        return WeaknessProfile.create(
            items,
            evidence_ids=tuple(dict.fromkeys(evidence_ids)),
        )

    @staticmethod
    def from_twin(twin: DigitalTwin) -> WeaknessProfile:
        """Analyse weaknesses from Twin component states."""
        return WeaknessAnalyser.analyse(
            twin.mastery,
            twin.retention,
            twin.confidence,
        )
