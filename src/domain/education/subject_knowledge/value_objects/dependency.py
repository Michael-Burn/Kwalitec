"""Educational dependency between concepts.

Architecture Source
    SUBJECT_KNOWLEDGE_MODEL.md / KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Dependency
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.enums import DependencyKind
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId


@dataclass(frozen=True, slots=True)
class Dependency(EducationalValueObject):
    """Typed educational dependency from an owning concept to a target concept.

    The owning concept is the *dependent* (target leans on the source in
    Knowledge Dependency Model terms when the owner is the teachable aim).
    ``target_concept_id`` identifies the concept this dependency points to
    (prerequisite, parallel neighbour, extension target, etc.).

    Self-dependency is forbidden: a concept may not depend on itself.
    """

    target_concept_id: ConceptId
    kind: DependencyKind
    description: str

    def _validate(self) -> None:
        if not isinstance(self.target_concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "target_concept_id must be a ConceptId",
                invariant="Dependency.target_concept_id.type",
            )
        if not isinstance(self.kind, DependencyKind):
            raise EducationalInvariantViolation(
                "kind must be a valid DependencyKind",
                invariant="Dependency.kind.valid",
            )
        object.__setattr__(
            self,
            "description",
            require_non_empty_text(self.description, "description"),
        )

    def assert_not_self(self, owner_concept_id: ConceptId) -> None:
        """Reject a dependency whose target is the owning concept.

        Args:
            owner_concept_id: Identity of the concept that would own this edge.

        Raises:
            EducationalInvariantViolation: When target equals owner.
        """
        if not isinstance(owner_concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "owner_concept_id must be a ConceptId",
                invariant="Dependency.owner_concept_id.type",
            )
        if self.target_concept_id == owner_concept_id:
            raise EducationalInvariantViolation(
                "a concept cannot depend on itself",
                invariant="Dependency.no_self_dependency",
            )

    def same_edge(self, other: Dependency) -> bool:
        """Return True when target and kind match (duplicate dependency key)."""
        return (
            self.target_concept_id == other.target_concept_id
            and self.kind == other.kind
        )
