"""Educational ROI — cost-benefit of an intervention in study time."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EducationalROI:
    """Deterministic educational return-on-investment estimate.

    Estimates expected readiness improvement relative to study duration.
    Does not invent mastery or generate content.
    """

    expected_readiness_improvement: float
    estimated_study_minutes: float
    educational_benefit: float
    cost_benefit_ratio: float
    return_on_study_time: float

    @classmethod
    def create(
        cls,
        *,
        expected_readiness_improvement: float,
        estimated_study_minutes: float,
        educational_benefit: float | None = None,
        cost_benefit_ratio: float | None = None,
        return_on_study_time: float | None = None,
    ) -> EducationalROI:
        """Construct EducationalROI with validated non-negative fields."""
        improvement = _unit_interval(
            expected_readiness_improvement, "expected_readiness_improvement"
        )
        minutes = _non_negative(estimated_study_minutes, "estimated_study_minutes")
        benefit = (
            _unit_interval(educational_benefit, "educational_benefit")
            if educational_benefit is not None
            else improvement
        )
        if cost_benefit_ratio is not None:
            ratio = _non_negative(cost_benefit_ratio, "cost_benefit_ratio")
        else:
            ratio = benefit / max(minutes / 60.0, 1e-6)
        if return_on_study_time is not None:
            rost = _non_negative(return_on_study_time, "return_on_study_time")
        else:
            rost = ratio
        return cls(
            expected_readiness_improvement=improvement,
            estimated_study_minutes=minutes,
            educational_benefit=benefit,
            cost_benefit_ratio=ratio,
            return_on_study_time=rost,
        )

    @classmethod
    def zero(cls) -> EducationalROI:
        """Return a zero-ROI placeholder."""
        return cls(
            expected_readiness_improvement=0.0,
            estimated_study_minutes=0.0,
            educational_benefit=0.0,
            cost_benefit_ratio=0.0,
            return_on_study_time=0.0,
        )

    @property
    def is_worthwhile(self) -> bool:
        """Heuristic: positive benefit with non-zero study time."""
        return self.educational_benefit > 0.0 and self.estimated_study_minutes > 0.0


def _unit_interval(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a number in [0, 1]")
    numeric = float(value)
    if numeric < 0.0 or numeric > 1.0:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric


def _non_negative(value: float, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(f"{field_name} must be a non-negative number")
    numeric = float(value)
    if numeric < 0.0:
        raise ValueError(f"{field_name} must be a non-negative number")
    return numeric
