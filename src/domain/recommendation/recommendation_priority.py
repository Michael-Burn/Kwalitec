"""RecommendationPriority — instructional urgency of an educational recommendation.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Recommendation Priority
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.enums import UrgencyLevel
from domain.recommendation.enums import RecommendationPriorityBand

_BAND_ORDER: tuple[RecommendationPriorityBand, ...] = (
    RecommendationPriorityBand.NEGLIGIBLE,
    RecommendationPriorityBand.LOW,
    RecommendationPriorityBand.MEDIUM,
    RecommendationPriorityBand.HIGH,
    RecommendationPriorityBand.CRITICAL,
)


@dataclass(frozen=True, slots=True)
class RecommendationPriority(EducationalValueObject):
    """Immutable instructional-urgency projection for a recommendation.

    Priority answers how urgently this educational decision should govern
    the next move relative to competing recommendations. It is not diagnosis
    severity and not a UI sort key.
    """

    band: RecommendationPriorityBand
    urgency: UrgencyLevel
    ratio: float | None = None
    rationale: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.band, RecommendationPriorityBand):
            raise EducationalInvariantViolation(
                "band must be a RecommendationPriorityBand",
                invariant="RecommendationPriority.band.type",
            )
        if not isinstance(self.urgency, UrgencyLevel):
            raise EducationalInvariantViolation(
                "urgency must be an UrgencyLevel",
                invariant="RecommendationPriority.urgency.type",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="RecommendationPriority.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="RecommendationPriority.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))
        if self.rationale is not None:
            cleaned = self.rationale.strip()
            if not cleaned:
                raise EducationalInvariantViolation(
                    "priority rationale must be non-empty when provided",
                    invariant="RecommendationPriority.rationale.non_empty",
                )
            object.__setattr__(self, "rationale", cleaned)

    @classmethod
    def of(
        cls,
        band: RecommendationPriorityBand,
        urgency: UrgencyLevel,
        *,
        ratio: float | None = None,
        rationale: str | None = None,
    ) -> RecommendationPriority:
        return cls(band=band, urgency=urgency, ratio=ratio, rationale=rationale)

    def is_at_least(self, other: RecommendationPriorityBand) -> bool:
        if other not in _BAND_ORDER:
            raise EducationalInvariantViolation(
                "comparison requires a known RecommendationPriorityBand",
                invariant="RecommendationPriority.is_at_least.band",
            )
        return _BAND_ORDER.index(self.band) >= _BAND_ORDER.index(other)

    def __str__(self) -> str:
        if self.ratio is None:
            return f"{self.band.value}/{self.urgency.value}"
        return f"{self.band.value}({self.ratio:.2f})/{self.urgency.value}"
