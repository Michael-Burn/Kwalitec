"""EvaluationSummary — compact application summary of an evaluation turn."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class EvaluationSummary:
    """Immutable summary of mastery + recommendation outcomes.

    Aggregates projected scalars only. Does not recompute mastery or
    re-decide recommendations.
    """

    student_id: str
    assessment_id: str
    recommendation_set_id: str
    mastery_magnitude: float
    mastery_band: str
    confidence_magnitude: float
    stability_band: str
    knowledge_gap_count: int
    recommendation_count: int
    evidence_count: int
    evaluated_at: datetime
    top_decision_category: str | None = None

    def __post_init__(self) -> None:
        student_id = (self.student_id or "").strip()
        if not student_id:
            raise ValueError("student_id is required")
        object.__setattr__(self, "student_id", student_id)

        assessment_id = (self.assessment_id or "").strip()
        if not assessment_id:
            raise ValueError("assessment_id is required")
        object.__setattr__(self, "assessment_id", assessment_id)

        recommendation_set_id = (self.recommendation_set_id or "").strip()
        if not recommendation_set_id:
            raise ValueError("recommendation_set_id is required")
        object.__setattr__(self, "recommendation_set_id", recommendation_set_id)

        for name in ("mastery_magnitude", "confidence_magnitude"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise ValueError(f"{name} must be a real number")
            object.__setattr__(self, name, float(value))

        mastery_band = (self.mastery_band or "").strip()
        if not mastery_band:
            raise ValueError("mastery_band is required")
        object.__setattr__(self, "mastery_band", mastery_band)

        stability_band = (self.stability_band or "").strip()
        if not stability_band:
            raise ValueError("stability_band is required")
        object.__setattr__(self, "stability_band", stability_band)

        for name in (
            "knowledge_gap_count",
            "recommendation_count",
            "evidence_count",
        ):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be an int")
            if value < 0:
                raise ValueError(f"{name} must be >= 0")

        if not isinstance(self.evaluated_at, datetime):
            raise ValueError("evaluated_at must be a datetime")

        top = (self.top_decision_category or "").strip() or None
        object.__setattr__(self, "top_decision_category", top)
