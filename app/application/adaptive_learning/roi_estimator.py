"""ROI estimator — educational return on study time."""

from __future__ import annotations

from app.application.adaptive_learning.policies.roi_policy import ROIPolicy
from app.domain.adaptive_learning.educational_roi import EducationalROI
from app.domain.adaptive_learning.intervention_priority import InterventionPriority


class ROIEstimator:
    """Estimate educational ROI for a revision candidate.

    Outputs expected readiness improvement, study duration, benefit, and
    cost-benefit / return-on-study-time ratios.
    """

    @staticmethod
    def estimate(
        *,
        priority: InterventionPriority | float,
        retention_risk: float,
        mastery_gap: float,
        curriculum_importance: float = 0.5,
    ) -> EducationalROI:
        """Return a deterministic EducationalROI."""
        if isinstance(priority, InterventionPriority):
            priority_score = priority.score
        else:
            priority_score = float(priority)
        priority_score = _clamp01(priority_score)
        risk = _clamp01(retention_risk)
        gap = _clamp01(mastery_gap)
        importance = _clamp01(curriculum_importance)

        minutes = ROIPolicy.estimate_study_minutes(
            priority_score=priority_score,
            retention_risk=risk,
            mastery_gap=gap,
        )
        improvement = ROIPolicy.estimate_readiness_improvement(
            retention_risk=risk,
            mastery_gap=gap,
            curriculum_importance=importance,
        )
        benefit = ROIPolicy.educational_benefit(
            readiness_improvement=improvement,
            curriculum_importance=importance,
            priority_score=priority_score,
        )
        hours = max(minutes / 60.0, 1e-6)
        ratio = round(benefit / hours, 6)
        return EducationalROI.create(
            expected_readiness_improvement=improvement,
            estimated_study_minutes=minutes,
            educational_benefit=benefit,
            cost_benefit_ratio=ratio,
            return_on_study_time=ratio,
        )


def _clamp01(value: float) -> float:
    if value < 0.0:
        return 0.0
    if value > 1.0:
        return 1.0
    return float(value)
