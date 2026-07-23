"""Knowledge relationship — a typed edge label pointing at a target node.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
    CONCEPT_NETWORK_MODEL.md
Concept
    Knowledge Relationship
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.enums import RelationshipType
from domain.education.knowledge_graph.ids import KnowledgeNodeId
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.knowledge_graph.value_objects.relationship_metadata import (
    RelationshipMetadata,
)


@dataclass(frozen=True, slots=True)
class KnowledgeRelationship(EducationalValueObject):
    """Typed educational relationship from an owning node to a target node.

    The owning node is implicit (carried by the enclosing ``KnowledgeEdge``).
    ``target_node_id`` identifies the node this relationship points to.

    Self-relationships are forbidden: a node may not relate to itself.
    """

    target_node_id: KnowledgeNodeId
    relationship_type: RelationshipType
    strength: DependencyStrength
    metadata: RelationshipMetadata

    def _validate(self) -> None:
        if not isinstance(self.target_node_id, KnowledgeNodeId):
            raise EducationalInvariantViolation(
                "target_node_id must be a KnowledgeNodeId",
                invariant="KnowledgeRelationship.target_node_id.type",
            )
        if not isinstance(self.relationship_type, RelationshipType):
            raise EducationalInvariantViolation(
                "relationship_type must be a valid RelationshipType",
                invariant="KnowledgeRelationship.relationship_type.valid",
            )
        if not isinstance(self.strength, DependencyStrength):
            raise EducationalInvariantViolation(
                "strength must be a DependencyStrength",
                invariant="KnowledgeRelationship.strength.type",
            )
        if not isinstance(self.metadata, RelationshipMetadata):
            raise EducationalInvariantViolation(
                "metadata must be a RelationshipMetadata",
                invariant="KnowledgeRelationship.metadata.type",
            )

    @classmethod
    def of(
        cls,
        target_node_id: KnowledgeNodeId,
        relationship_type: RelationshipType,
        *,
        strength: DependencyStrength | None = None,
        metadata: RelationshipMetadata | None = None,
    ) -> KnowledgeRelationship:
        """Factory with sensible defaults for strength and metadata."""
        return cls(
            target_node_id=target_node_id,
            relationship_type=relationship_type,
            strength=strength if strength is not None else DependencyStrength.helpful(),
            metadata=metadata if metadata is not None else RelationshipMetadata.empty(),
        )

    def assert_not_self(self, owner_node_id: KnowledgeNodeId) -> None:
        """Reject a relationship whose target is the owning node.

        Args:
            owner_node_id: Identity of the node that would own this edge.

        Raises:
            EducationalInvariantViolation: When target equals owner.
        """
        if not isinstance(owner_node_id, KnowledgeNodeId):
            raise EducationalInvariantViolation(
                "owner_node_id must be a KnowledgeNodeId",
                invariant="KnowledgeRelationship.owner_node_id.type",
            )
        if self.target_node_id == owner_node_id:
            raise EducationalInvariantViolation(
                "a knowledge node cannot relate to itself",
                invariant="KnowledgeRelationship.no_self_relationship",
            )

    def same_edge(self, other: KnowledgeRelationship) -> bool:
        """True when target and relationship type match (duplicate edge key)."""
        return (
            self.target_node_id == other.target_node_id
            and self.relationship_type == other.relationship_type
        )
