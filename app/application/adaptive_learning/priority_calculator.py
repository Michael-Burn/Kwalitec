"""Priority calculator — deterministic intervention priority from Twin signals."""

from __future__ import annotations

from app.application.adaptive_learning.policies.priority_policy import PriorityPolicy
from app.domain.adaptive_learning.intervention_priority import InterventionPriority
from app.domain.student_twin.confidence_band import (
    ConfidenceBand,
    confidence_score_from_band,
)


class PriorityCalculator:
    """Compute InterventionPriority from educational factor inputs.

    Considers retention risk, mastery, prerequisite criticality, curriculum
    importance, historical struggle, confidence, learning velocity, and exam
    proximity. No randomness.
    """

    @staticmethod
    def calculate(
        *,
        retention_score: float,
        mastery_score: float,
        confidence: ConfidenceBand | str | float,
        curriculum_importance: float = 0.5,
        prerequisite_criticality: float = 0.0,
        historical_struggle: float = 0.0,
        events_per_day: float = 0.0,
        mastery_delta: float = 0.0,
        exam_proximity: float = 0.0,
    ) -> InterventionPriority:
        """Return a deterministic InterventionPriority."""
        retention_risk = _clamp01(1.0 - float(retention_score))
        mastery_gap = _clamp01(1.0 - float(mastery_score))
        confidence_gap = _clamp01(1.0 - _confidence_numeric(confidence))
        velocity = PriorityPolicy.velocity_factor(events_per_day, mastery_delta)
        importance = _clamp01(curriculum_importance)
        prereq = _clamp01(prerequisite_criticality)
        struggle = _clamp01(historical_struggle)
        exam = _clamp01(exam_proximity)

        score = (
            PriorityPolicy.WEIGHT_RETENTION_RISK * retention_risk
            + PriorityPolicy.WEIGHT_MASTERY_GAP * mastery_gap
            + PriorityPolicy.WEIGHT_PREREQUISITE * prereq
            + PriorityPolicy.WEIGHT_CURRICULUM * importance
            + PriorityPolicy.WEIGHT_STRUGGLE * struggle
            + PriorityPolicy.WEIGHT_CONFIDENCE_GAP * confidence_gap
            + PriorityPolicy.WEIGHT_VELOCITY * velocity
            + PriorityPolicy.WEIGHT_EXAM * exam
        )
        return InterventionPriority.create(
            round(_clamp01(score), 6),
            retention_risk=retention_risk,
            mastery_gap=mastery_gap,
            prerequisite_criticality=prereq,
            curriculum_importance=importance,
            historical_struggle=struggle,
            confidence_gap=confidence_gap,
            velocity_factor=velocity,
            exam_proximity=exam,
        )


def _confidence_numeric(confidence: ConfidenceBand | str | float) -> float:
    if isinstance(confidence, int | float) and not isinstance(confidence, bool):
        return _clamp01(float(confidence))
    if isinstance(confidence, ConfidenceBand):
        return confidence_score_from_band(confidence)
    return confidence_score_from_band(str(confidence))


def _clamp01(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)
