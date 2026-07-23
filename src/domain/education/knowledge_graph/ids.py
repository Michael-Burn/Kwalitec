"""Knowledge Dependency Graph identity value objects.

Opaque, immutable identifiers scoped to the Knowledge Dependency Graph
bounded context. Identities are not database keys and carry no persistence
semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.knowledge_graph.enums import RelationshipType


@dataclass(frozen=True, slots=True)
class KnowledgeGraphId(EducationalValueObject):
    """Identity of a KnowledgeGraph aggregate."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "KnowledgeGraphId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class KnowledgeNodeId(EducationalValueObject):
    """Identity of a knowledge node within a KnowledgeGraph."""

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "KnowledgeNodeId"),
        )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class KnowledgeRelationshipId(EducationalValueObject):
    """Identity of a single typed relationship edge within a KnowledgeGraph.

    Derived deterministically from the edge's source, target, and
    relationship type — never from randomness or the wall clock — so that
    graph reasoning remains reproducible from the same inputs.
    """

    value: str

    def _validate(self) -> None:
        object.__setattr__(
            self,
            "value",
            require_identity_value(self.value, "KnowledgeRelationshipId"),
        )

    def __str__(self) -> str:
        return self.value

    @classmethod
    def for_edge(
        cls,
        source_node_id: KnowledgeNodeId,
        target_node_id: KnowledgeNodeId,
        relationship_type: RelationshipType,
    ) -> KnowledgeRelationshipId:
        """Derive a stable identity for the edge described by the arguments."""
        return cls(
            f"{source_node_id.value}--{relationship_type.value}-->"
            f"{target_node_id.value}"
        )
