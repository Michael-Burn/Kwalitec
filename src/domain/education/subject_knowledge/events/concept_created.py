"""Domain event: a teachable concept was created.

Architecture Source
    SUBJECT_KNOWLEDGE_MODEL.md
Concept
    ConceptCreated
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, LearningObjectiveId


@dataclass(frozen=True, slots=True)
class ConceptCreated(EducationalValueObject):
    """Immutable record that a Concept aggregate entered the domain model."""

    concept_id: ConceptId
    canonical_name: str
    initial_objective_id: LearningObjectiveId

    def _validate(self) -> None:
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="ConceptCreated.concept_id.type",
            )
        object.__setattr__(
            self,
            "canonical_name",
            require_non_empty_text(self.canonical_name, "canonical_name"),
        )
        if not isinstance(self.initial_objective_id, LearningObjectiveId):
            raise EducationalInvariantViolation(
                "initial_objective_id must be a LearningObjectiveId",
                invariant="ConceptCreated.initial_objective_id.type",
            )
