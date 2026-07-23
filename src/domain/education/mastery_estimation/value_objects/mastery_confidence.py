"""Mastery confidence — richer, explainable confidence in a mastery estimate.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Mastery Confidence
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.mastery_estimation.value_objects.confidence_score import (
    ConfidenceScore,
)


@dataclass(frozen=True, slots=True)
class MasteryConfidence(EducationalValueObject):
    """Immutable, explainable confidence posture for a mastery estimate.

    Composes a bare ``ConfidenceScore`` with the deterministic factors the
    estimator considered — evidence volume (via ``evidence_count``),
    contradiction, recency, and whether a prerequisite penalty was applied
    — so downstream consumers can trace *why* confidence is what it is
    without recomputing the estimate themselves.
    """

    score: ConfidenceScore
    evidence_count: int = 0
    contradiction_ratio: float = 0.0
    recency_factor: float = 0.0
    prerequisite_penalty_applied: bool = False

    def _validate(self) -> None:
        if not isinstance(self.score, ConfidenceScore):
            raise EducationalInvariantViolation(
                "score must be a ConfidenceScore",
                invariant="MasteryConfidence.score.type",
            )
        if isinstance(self.evidence_count, bool) or not isinstance(
            self.evidence_count, int
        ):
            raise EducationalInvariantViolation(
                "evidence_count must be an integer",
                invariant="MasteryConfidence.evidence_count.type",
            )
        if self.evidence_count < 0:
            raise EducationalInvariantViolation(
                "evidence_count must be non-negative",
                invariant="MasteryConfidence.evidence_count.non_negative",
            )
        for field_name in ("contradiction_ratio", "recency_factor"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise EducationalInvariantViolation(
                    f"{field_name} must be a real number",
                    invariant=f"MasteryConfidence.{field_name}.type",
                )
            if value < 0.0 or value > 1.0:
                raise EducationalInvariantViolation(
                    f"{field_name} must be between 0.0 and 1.0 inclusive",
                    invariant=f"MasteryConfidence.{field_name}.range",
                )
            object.__setattr__(self, field_name, round(float(value), 4))
        if not isinstance(self.prerequisite_penalty_applied, bool):
            raise EducationalInvariantViolation(
                "prerequisite_penalty_applied must be a boolean",
                invariant=(
                    "MasteryConfidence.prerequisite_penalty_applied.type"
                ),
            )

    @classmethod
    def zero(cls) -> MasteryConfidence:
        return cls(score=ConfidenceScore.zero())

    def is_contradicted(self) -> bool:
        return self.contradiction_ratio > 0.0

    def __str__(self) -> str:
        return str(self.score)
