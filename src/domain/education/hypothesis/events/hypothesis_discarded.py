"""Domain event: educational hypothesis was discarded.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    HypothesisDiscarded
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import HypothesisId
from domain.education.hypothesis.enums import HypothesisKind


@dataclass(frozen=True, slots=True)
class HypothesisDiscarded(EducationalValueObject):
    """Immutable record that an EducationalHypothesis was discarded."""

    hypothesis_id: HypothesisId
    student_id: str
    hypothesis_kind: HypothesisKind
    reason: str

    def _validate(self) -> None:
        if not isinstance(self.hypothesis_id, HypothesisId):
            raise EducationalInvariantViolation(
                "hypothesis_id must be a HypothesisId",
                invariant="HypothesisDiscarded.hypothesis_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.hypothesis_kind, HypothesisKind):
            raise EducationalInvariantViolation(
                "hypothesis_kind must be a HypothesisKind",
                invariant="HypothesisDiscarded.hypothesis_kind.type",
            )
        object.__setattr__(
            self,
            "reason",
            require_non_empty_text(self.reason, "reason"),
        )
