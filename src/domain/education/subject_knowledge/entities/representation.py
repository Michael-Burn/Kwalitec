"""Representation — mode of presenting subject structure.

Architecture Source
    SUBJECT_KNOWLEDGE_MODEL.md / REPRESENTATION_MODEL.md
Concept
    Representation
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalEntity,
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import RepresentationKind
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId


@dataclass(frozen=True, slots=True)
class RepresentationId(EducationalValueObject):
    """Identity of a concept representation."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "RepresentationId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True, eq=False)
class Representation(EducationalEntity):
    """Educational mode of presenting a concept's structure.

    Multiple representations strengthen connection; kinds are unique within a
    concept (Subject Invariant K13 / representation policy).
    """

    representation_id: RepresentationId
    concept_id: ConceptId
    kind: RepresentationKind
    description: str
    educational_purpose: str

    @property
    def entity_id(self) -> RepresentationId:
        return self.representation_id

    def _validate(self) -> None:
        if not isinstance(self.representation_id, RepresentationId):
            raise EducationalInvariantViolation(
                "representation_id must be a RepresentationId",
                invariant="Representation.representation_id.type",
            )
        if not isinstance(self.concept_id, ConceptId):
            raise EducationalInvariantViolation(
                "concept_id must be a ConceptId",
                invariant="Representation.concept_id.type",
            )
        if not isinstance(self.kind, RepresentationKind):
            raise EducationalInvariantViolation(
                "kind must be a RepresentationKind",
                invariant="Representation.kind.type",
            )
        object.__setattr__(
            self,
            "description",
            require_non_empty_text(self.description, "description"),
        )
        object.__setattr__(
            self,
            "educational_purpose",
            require_non_empty_text(self.educational_purpose, "educational_purpose"),
        )

    def belongs_to(self, concept_id: ConceptId) -> bool:
        """Return True when this representation belongs to ``concept_id``."""
        return self.concept_id == concept_id
