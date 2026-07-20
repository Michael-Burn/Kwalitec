"""Domain event: Twin mastery memory changed for a concept.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    MasteryChanged
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.digital_twin.enums import MasteryBand
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, DigitalTwinId


@dataclass(frozen=True, slots=True)
class MasteryChanged(EducationalValueObject):
    """Immutable record that concept mastery memory was updated."""

    twin_id: DigitalTwinId
    student_id: str
    concept_id: ConceptId
    previous_band: MasteryBand
    new_band: MasteryBand

    def _validate(self) -> None:
        if not isinstance(self.twin_id, DigitalTwinId):
            raise EducationalInvariantViolation(
                "twin_id must be a DigitalTwinId",
                invariant="MasteryChanged.twin_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="MasteryChanged.concept_id.type",
            )
        if not isinstance(self.previous_band, MasteryBand):
            raise EducationalInvariantViolation(
                "previous_band must be a MasteryBand",
                invariant="MasteryChanged.previous_band.type",
            )
        if not isinstance(self.new_band, MasteryBand):
            raise EducationalInvariantViolation(
                "new_band must be a MasteryBand",
                invariant="MasteryChanged.new_band.type",
            )
