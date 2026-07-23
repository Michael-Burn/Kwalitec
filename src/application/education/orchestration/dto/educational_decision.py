"""EducationalDecision — application projection of one recommendation.

Carries educational intent packaging produced by the Recommendation Engine.
Does not select, score, or invent recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EducationalDecision:
    """Immutable application view of a single educational recommendation.

    Attributes are primitives projected from domain recommendation value
    objects. This DTO never re-ranks or rewrites educational meaning.
    """

    decision_id: str
    category: str
    subject_id: str | None
    competency_id: str | None
    priority_band: str
    impact_band: str
    confidence_magnitude: float
    reason_summary: str
    rank: int

    def __post_init__(self) -> None:
        decision_id = (self.decision_id or "").strip()
        if not decision_id:
            raise ValueError("decision_id is required")
        object.__setattr__(self, "decision_id", decision_id)

        category = (self.category or "").strip()
        if not category:
            raise ValueError("category is required")
        object.__setattr__(self, "category", category)

        subject_id = (self.subject_id or "").strip() or None
        object.__setattr__(self, "subject_id", subject_id)

        competency_id = (self.competency_id or "").strip() or None
        object.__setattr__(self, "competency_id", competency_id)

        priority_band = (self.priority_band or "").strip()
        if not priority_band:
            raise ValueError("priority_band is required")
        object.__setattr__(self, "priority_band", priority_band)

        impact_band = (self.impact_band or "").strip()
        if not impact_band:
            raise ValueError("impact_band is required")
        object.__setattr__(self, "impact_band", impact_band)

        if isinstance(self.confidence_magnitude, bool) or not isinstance(
            self.confidence_magnitude, int | float
        ):
            raise ValueError("confidence_magnitude must be a real number")
        object.__setattr__(
            self, "confidence_magnitude", float(self.confidence_magnitude)
        )

        object.__setattr__(
            self, "reason_summary", (self.reason_summary or "").strip()
        )

        if isinstance(self.rank, bool) or not isinstance(self.rank, int):
            raise ValueError("rank must be an int")
        if self.rank < 1:
            raise ValueError("rank must be >= 1")
