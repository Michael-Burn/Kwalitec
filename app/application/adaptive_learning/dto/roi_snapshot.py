"""ROI snapshot DTOs."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.adaptive_learning.educational_roi import EducationalROI


@dataclass(frozen=True)
class ROISnapshot:
    """Immutable DTO for educational ROI estimates."""

    expected_readiness_improvement: float
    estimated_study_minutes: float
    educational_benefit: float
    cost_benefit_ratio: float
    return_on_study_time: float
    is_worthwhile: bool = False

    @classmethod
    def from_roi(cls, roi: EducationalROI) -> ROISnapshot:
        """Project an EducationalROI."""
        return cls(
            expected_readiness_improvement=roi.expected_readiness_improvement,
            estimated_study_minutes=roi.estimated_study_minutes,
            educational_benefit=roi.educational_benefit,
            cost_benefit_ratio=roi.cost_benefit_ratio,
            return_on_study_time=roi.return_on_study_time,
            is_worthwhile=roi.is_worthwhile,
        )

    @classmethod
    def zero(cls) -> ROISnapshot:
        """Return a zero ROI snapshot."""
        return cls.from_roi(EducationalROI.zero())
