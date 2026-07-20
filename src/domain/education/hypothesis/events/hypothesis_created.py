"""Domain event: educational hypothesis was created (proposed).

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    HypothesisCreated
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import HypothesisId
from domain.education.hypothesis.enums import (
    ExplanatoryStrengthLevel,
    HypothesisKind,
    PlausibilityLevel,
)


@dataclass(frozen=True, slots=True)
class HypothesisCreated(EducationalValueObject):
    """Immutable record that an EducationalHypothesis was proposed."""

    hypothesis_id: HypothesisId
    student_id: str
    hypothesis_kind: HypothesisKind
    plausibility_level: PlausibilityLevel
    explanatory_strength_level: ExplanatoryStrengthLevel
    diagnosis_count: int
    reason_count: int

    def _validate(self) -> None:
        if not isinstance(self.hypothesis_id, HypothesisId):
            raise EducationalInvariantViolation(
                "hypothesis_id must be a HypothesisId",
                invariant="HypothesisCreated.hypothesis_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.hypothesis_kind, HypothesisKind):
            raise EducationalInvariantViolation(
                "hypothesis_kind must be a HypothesisKind",
                invariant="HypothesisCreated.hypothesis_kind.type",
            )
        if not isinstance(self.plausibility_level, PlausibilityLevel):
            raise EducationalInvariantViolation(
                "plausibility_level must be a PlausibilityLevel",
                invariant="HypothesisCreated.plausibility_level.type",
            )
        if not isinstance(
            self.explanatory_strength_level, ExplanatoryStrengthLevel
        ):
            raise EducationalInvariantViolation(
                "explanatory_strength_level must be an ExplanatoryStrengthLevel",
                invariant="HypothesisCreated.explanatory_strength_level.type",
            )
        if not isinstance(self.diagnosis_count, int) or self.diagnosis_count < 1:
            raise EducationalInvariantViolation(
                "diagnosis_count must be a positive integer",
                invariant="HypothesisCreated.diagnosis_count.positive",
            )
        if not isinstance(self.reason_count, int) or self.reason_count < 1:
            raise EducationalInvariantViolation(
                "reason_count must be a positive integer",
                invariant="HypothesisCreated.reason_count.positive",
            )
