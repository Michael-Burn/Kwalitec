"""Domain event: educational hypothesis was revised.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    HypothesisRevised
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
    RevisionForm,
)


@dataclass(frozen=True, slots=True)
class HypothesisRevised(EducationalValueObject):
    """Immutable record that an EducationalHypothesis was revised."""

    hypothesis_id: HypothesisId
    student_id: str
    hypothesis_kind: HypothesisKind
    plausibility_level: PlausibilityLevel
    explanatory_strength_level: ExplanatoryStrengthLevel
    revision_form: RevisionForm | None = None

    def _validate(self) -> None:
        if not isinstance(self.hypothesis_id, HypothesisId):
            raise EducationalInvariantViolation(
                "hypothesis_id must be a HypothesisId",
                invariant="HypothesisRevised.hypothesis_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.hypothesis_kind, HypothesisKind):
            raise EducationalInvariantViolation(
                "hypothesis_kind must be a HypothesisKind",
                invariant="HypothesisRevised.hypothesis_kind.type",
            )
        if not isinstance(self.plausibility_level, PlausibilityLevel):
            raise EducationalInvariantViolation(
                "plausibility_level must be a PlausibilityLevel",
                invariant="HypothesisRevised.plausibility_level.type",
            )
        if not isinstance(
            self.explanatory_strength_level, ExplanatoryStrengthLevel
        ):
            raise EducationalInvariantViolation(
                "explanatory_strength_level must be an ExplanatoryStrengthLevel",
                invariant="HypothesisRevised.explanatory_strength_level.type",
            )
        if self.revision_form is not None and not isinstance(
            self.revision_form, RevisionForm
        ):
            raise EducationalInvariantViolation(
                "revision_form must be a RevisionForm when provided",
                invariant="HypothesisRevised.revision_form.type",
            )
