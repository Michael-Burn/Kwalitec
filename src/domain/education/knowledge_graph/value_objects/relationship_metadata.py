"""Relationship metadata — descriptive context for a knowledge relationship.

Architecture Source
    CONCEPT_NETWORK_MODEL.md
Concept
    Relationship Metadata
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_non_empty_text,
)
from domain.education.foundation.errors import EducationalInvariantViolation


@dataclass(frozen=True, slots=True)
class RelationshipMetadata(EducationalValueObject):
    """Immutable, supplied descriptive context for a relationship edge.

    Carries an optional rationale and an optional set of free-form tags.
    Metadata is documentation for the edge, not a computation input.
    """

    description: str | None = None
    tags: tuple[str, ...] = ()

    def _validate(self) -> None:
        if self.description is not None:
            object.__setattr__(
                self,
                "description",
                require_non_empty_text(self.description, "description"),
            )
        if not isinstance(self.tags, tuple | list):
            raise EducationalInvariantViolation(
                "tags must be a tuple or list of strings",
                invariant="RelationshipMetadata.tags.type",
            )
        cleaned: list[str] = []
        seen: set[str] = set()
        for tag in self.tags:
            normalised = require_non_empty_text(tag, "tag")
            if normalised in seen:
                raise EducationalInvariantViolation(
                    "duplicate tag in relationship metadata",
                    invariant="RelationshipMetadata.tags.unique",
                )
            seen.add(normalised)
            cleaned.append(normalised)
        object.__setattr__(self, "tags", tuple(cleaned))

    @classmethod
    def empty(cls) -> RelationshipMetadata:
        return cls()

    def with_description(self, description: str | None) -> RelationshipMetadata:
        return RelationshipMetadata(description=description, tags=self.tags)

    def with_tag(self, tag: str) -> RelationshipMetadata:
        if tag in self.tags:
            return self
        return RelationshipMetadata(
            description=self.description, tags=(*self.tags, tag)
        )
