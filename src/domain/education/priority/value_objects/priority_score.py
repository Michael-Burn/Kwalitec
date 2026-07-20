"""Priority score — instructional ordering measure.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Priority Score
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.priority.enums import PriorityScoreBand

_SCORE_ORDER: tuple[PriorityScoreBand, ...] = (
    PriorityScoreBand.NEGLIGIBLE,
    PriorityScoreBand.LOW,
    PriorityScoreBand.MEDIUM,
    PriorityScoreBand.HIGH,
    PriorityScoreBand.CRITICAL,
)


@dataclass(frozen=True, slots=True)
class PriorityScore(EducationalValueObject):
    """Immutable instructional-ordering score.

    Priority score answers how strongly this diagnosed problem should govern
    the next episode relative to competing needs. It is **not** diagnosis
    severity, mastery, or a teaching-strategy recommendation.
    """

    band: PriorityScoreBand
    ratio: float | None = None
    rationale: str | None = None

    def _validate(self) -> None:
        if not isinstance(self.band, PriorityScoreBand):
            raise EducationalInvariantViolation(
                "band must be a PriorityScoreBand",
                invariant="PriorityScore.band.type",
            )
        if self.ratio is not None:
            if isinstance(self.ratio, bool) or not isinstance(self.ratio, int | float):
                raise EducationalInvariantViolation(
                    "ratio must be a real number when provided",
                    invariant="PriorityScore.ratio.type",
                )
            if self.ratio < 0.0 or self.ratio > 1.0:
                raise EducationalInvariantViolation(
                    "ratio must be between 0.0 and 1.0 inclusive",
                    invariant="PriorityScore.ratio.range",
                )
            object.__setattr__(self, "ratio", float(self.ratio))
        if self.rationale is not None:
            cleaned = self.rationale.strip()
            if not cleaned:
                raise EducationalInvariantViolation(
                    "score rationale must be non-empty when provided",
                    invariant="PriorityScore.rationale.non_empty",
                )
            object.__setattr__(self, "rationale", cleaned)

    @classmethod
    def of(
        cls,
        band: PriorityScoreBand,
        *,
        ratio: float | None = None,
        rationale: str | None = None,
    ) -> PriorityScore:
        return cls(band=band, ratio=ratio, rationale=rationale)

    def is_at_least(self, other: PriorityScoreBand) -> bool:
        if other not in _SCORE_ORDER:
            raise EducationalInvariantViolation(
                "comparison requires a known PriorityScoreBand",
                invariant="PriorityScore.is_at_least.band",
            )
        return _SCORE_ORDER.index(self.band) >= _SCORE_ORDER.index(other)

    def promoted(self) -> PriorityScore:
        """Return the next higher instructional-ordering band."""
        index = _SCORE_ORDER.index(self.band)
        if index >= len(_SCORE_ORDER) - 1:
            raise EducationalInvariantViolation(
                "priority score is already at maximum band",
                invariant="PriorityScore.promote.max",
            )
        return PriorityScore(
            band=_SCORE_ORDER[index + 1],
            ratio=self.ratio,
            rationale=self.rationale,
        )

    def demoted(self) -> PriorityScore:
        """Return the next lower instructional-ordering band."""
        index = _SCORE_ORDER.index(self.band)
        if index <= 0:
            raise EducationalInvariantViolation(
                "priority score is already at minimum band",
                invariant="PriorityScore.demote.min",
            )
        return PriorityScore(
            band=_SCORE_ORDER[index - 1],
            ratio=self.ratio,
            rationale=self.rationale,
        )

    def __str__(self) -> str:
        if self.ratio is None:
            return self.band.value
        return f"{self.band.value}({self.ratio:.2f})"
