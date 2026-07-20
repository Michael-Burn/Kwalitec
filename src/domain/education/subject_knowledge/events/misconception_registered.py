"""Domain event: a misconception was registered on a concept.

Architecture Source
    SUBJECT_KNOWLEDGE_MODEL.md / MISCONCEPTION_AUTHORING_MODEL.md
Concept
    MisconceptionRegistered
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, MisconceptionId


@dataclass(frozen=True, slots=True)
class MisconceptionRegistered(EducationalValueObject):
    """Immutable record that a misconception was attached to a concept."""

    concept_id: ConceptId
    misconception_id: MisconceptionId

    def _validate(self) -> None:
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="MisconceptionRegistered.concept_id.type",
            )
        if not isinstance(self.misconception_id, MisconceptionId):
            raise EducationalInvariantViolation(
                "misconception_id must be a MisconceptionId",
                invariant="MisconceptionRegistered.misconception_id.type",
            )
