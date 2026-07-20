"""Domain event: an educational dependency was added to a concept.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    DependencyAdded
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import DependencyKind
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId


@dataclass(frozen=True, slots=True)
class DependencyAdded(EducationalValueObject):
    """Immutable record that a typed dependency edge was added."""

    concept_id: ConceptId
    target_concept_id: ConceptId
    kind: DependencyKind

    def _validate(self) -> None:
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="DependencyAdded.concept_id.type",
            )
        if not isinstance(self.target_concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "target_concept_id must be a ConceptId",
                invariant="DependencyAdded.target_concept_id.type",
            )
        if not isinstance(self.kind, DependencyKind):
            raise EducationalInvariantViolation(
                "kind must be a DependencyKind",
                invariant="DependencyAdded.kind.type",
            )
        if self.concept_id == self.target_concept_id:
            raise EducationalInvariantViolation(
                "dependency event cannot record a self-dependency",
                invariant="DependencyAdded.no_self_dependency",
            )
