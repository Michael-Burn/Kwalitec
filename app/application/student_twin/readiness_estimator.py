"""Readiness estimator — preparedness from mastery, retention, confidence."""

from __future__ import annotations

from app.domain.student_twin.confidence_band import confidence_band_from_score
from app.domain.student_twin.confidence_state import ConfidenceState
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.mastery_state import MasteryState
from app.domain.student_twin.readiness_state import ReadinessState
from app.domain.student_twin.retention_state import RetentionState

_SUPPORT_THRESHOLD = 0.65
_LIMIT_THRESHOLD = 0.40


class ReadinessEstimator:
    """Estimate readiness as a weighted blend of Twin states."""

    MASTERY_WEIGHT = 0.40
    RETENTION_WEIGHT = 0.30
    CONFIDENCE_WEIGHT = 0.30

    @staticmethod
    def calculate(
        mastery: MasteryState,
        retention: RetentionState,
        confidence: ConfidenceState,
    ) -> ReadinessState:
        """Compute readiness from component states."""
        score = (
            ReadinessEstimator.MASTERY_WEIGHT * mastery.overall_score
            + ReadinessEstimator.RETENTION_WEIGHT * retention.overall_score
            + ReadinessEstimator.CONFIDENCE_WEIGHT * confidence.overall_score
        )
        if score > 1.0:
            score = 1.0
        supporting = tuple(
            r.topic_id
            for r in mastery.topic_records
            if r.mastery_score >= _SUPPORT_THRESHOLD
        )
        limiting = tuple(
            r.topic_id
            for r in mastery.topic_records
            if r.mastery_score < _LIMIT_THRESHOLD
        )
        evidence_ids = tuple(
            dict.fromkeys(
                (
                    *mastery.evidence_ids,
                    *retention.evidence_ids,
                    *confidence.evidence_ids,
                )
            )
        )
        rationale = (
            "insufficient_evidence"
            if not mastery.topic_records
            else "weighted_mastery_retention_confidence"
        )
        return ReadinessState.create(
            score,
            confidence=confidence_band_from_score(confidence.overall_score),
            supporting_topic_ids=supporting,
            limiting_topic_ids=limiting,
            evidence_ids=evidence_ids,
            rationale=rationale,
        )

    @staticmethod
    def from_twin(twin: DigitalTwin) -> ReadinessState:
        """Estimate readiness from Twin component states."""
        return ReadinessEstimator.calculate(
            twin.mastery,
            twin.retention,
            twin.confidence,
        )
