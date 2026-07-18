"""Stateless ROI policy — educational benefit vs study-time cost."""

from __future__ import annotations


class ROIPolicy:
    """Deterministic educational ROI estimation rules.

    Estimates expected readiness improvement and study duration.
    Does not invent mastery or generate content.
    """

    BASE_STUDY_MINUTES = 15.0
    MAX_STUDY_MINUTES = 90.0
    MIN_STUDY_MINUTES = 10.0

    # Minutes scale with severity (priority / retention risk / mastery gap).
    MINUTES_PER_PRIORITY = 40.0
    MINUTES_PER_RETENTION_RISK = 25.0
    MINUTES_PER_MASTERY_GAP = 20.0

    # Readiness improvement caps.
    MAX_READINESS_IMPROVEMENT = 0.35
    IMPROVEMENT_FROM_RETENTION = 0.18
    IMPROVEMENT_FROM_MASTERY = 0.12
    IMPROVEMENT_FROM_IMPORTANCE = 0.08

    WORTHWHILE_ROI_THRESHOLD = 0.15

    @staticmethod
    def estimate_study_minutes(
        *,
        priority_score: float,
        retention_risk: float,
        mastery_gap: float,
    ) -> float:
        """Deterministic study-duration estimate in minutes."""
        raw = (
            ROIPolicy.BASE_STUDY_MINUTES
            + ROIPolicy.MINUTES_PER_PRIORITY * _clamp01(priority_score)
            + ROIPolicy.MINUTES_PER_RETENTION_RISK * _clamp01(retention_risk)
            + ROIPolicy.MINUTES_PER_MASTERY_GAP * _clamp01(mastery_gap)
        )
        return round(
            min(ROIPolicy.MAX_STUDY_MINUTES, max(ROIPolicy.MIN_STUDY_MINUTES, raw)),
            2,
        )

    @staticmethod
    def estimate_readiness_improvement(
        *,
        retention_risk: float,
        mastery_gap: float,
        curriculum_importance: float,
    ) -> float:
        """Expected readiness improvement in [0, MAX]."""
        raw = (
            ROIPolicy.IMPROVEMENT_FROM_RETENTION * _clamp01(retention_risk)
            + ROIPolicy.IMPROVEMENT_FROM_MASTERY * _clamp01(mastery_gap)
            + ROIPolicy.IMPROVEMENT_FROM_IMPORTANCE * _clamp01(curriculum_importance)
        )
        return round(min(ROIPolicy.MAX_READINESS_IMPROVEMENT, raw), 6)

    @staticmethod
    def educational_benefit(
        *,
        readiness_improvement: float,
        curriculum_importance: float,
        priority_score: float,
    ) -> float:
        """Blend improvement, importance, and priority into [0, 1] benefit."""
        return round(
            _clamp01(
                0.50
                * _clamp01(readiness_improvement)
                / ROIPolicy.MAX_READINESS_IMPROVEMENT
                + 0.30 * _clamp01(curriculum_importance)
                + 0.20 * _clamp01(priority_score)
            ),
            6,
        )

    @staticmethod
    def is_worthwhile(cost_benefit_ratio: float) -> bool:
        """True when ROI clears the educational worth threshold."""
        return cost_benefit_ratio >= ROIPolicy.WORTHWHILE_ROI_THRESHOLD


def _clamp01(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)
