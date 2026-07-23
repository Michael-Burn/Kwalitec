"""Knowledge edge — a directed relationship owned by a source node.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
    CONCEPT_NETWORK_MODEL.md
Concept
    Knowledge Edge
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.enums import RelationshipType
from domain.education.knowledge_graph.ids import (
    KnowledgeNodeId,
    KnowledgeRelationshipId,
)
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.knowledge_graph.value_objects.knowledge_relationship import (
    KnowledgeRelationship,
)
from domain.education.knowledge_graph.value_objects.relationship_metadata import (
    RelationshipMetadata,
)


@dataclass(frozen=True, slots=True)
class KnowledgeEdge:
    """Directed educational relationship edge within a knowledge graph.

    ``source_node_id`` owns the relationship; ``relationship`` carries the
    target, type, strength, and metadata. ``relationship_id`` is a stable,
    deterministic identity derived from the edge's shape.
    """

    relationship_id: KnowledgeRelationshipId
    source_node_id: KnowledgeNodeId
    relationship: KnowledgeRelationship

    def __post_init__(self) -> None:
        if not isinstance(self.relationship_id, KnowledgeRelationshipId):
            raise EducationalInvariantViolation(
                "relationship_id must be a KnowledgeRelationshipId",
                invariant="KnowledgeEdge.relationship_id.type",
            )
        if not isinstance(self.source_node_id, KnowledgeNodeId):
            raise EducationalInvariantViolation(
                "source_node_id must be a KnowledgeNodeId",
                invariant="KnowledgeEdge.source_node_id.type",
            )
        if not isinstance(self.relationship, KnowledgeRelationship):
            raise EducationalInvariantViolation(
                "relationship must be a KnowledgeRelationship",
                invariant="KnowledgeEdge.relationship.type",
            )

    @property
    def target_node_id(self) -> KnowledgeNodeId:
        return self.relationship.target_node_id

    @property
    def relationship_type(self) -> RelationshipType:
        return self.relationship.relationship_type

    @property
    def strength(self) -> DependencyStrength:
        return self.relationship.strength

    @property
    def metadata(self) -> RelationshipMetadata:
        return self.relationship.metadata

    def same_edge(self, other: KnowledgeEdge) -> bool:
        """True when source, target, and relationship type all match."""
        return (
            self.source_node_id == other.source_node_id
            and self.relationship.same_edge(other.relationship)
        )

    def __str__(self) -> str:
        return (
            f"{self.source_node_id.value} "
            f"--{self.relationship_type.value}--> "
            f"{self.target_node_id.value}"
        )
