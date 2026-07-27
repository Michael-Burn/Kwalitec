"""Prerequisite relationship helpers over Learning Graph edges."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_graph.graph_edge import GraphEdge
from app.domain.learning_graph.relationship import (
    DEPENDENCY_RELATIONSHIPS,
    RelationshipType,
)


@dataclass(frozen=True)
class PrerequisiteRelationship:
    """A concept depends on another concept as a prerequisite."""

    concept_id: str
    prerequisite_id: str
    edge_id: str
    strength: float
    confidence: float
    relationship_type: RelationshipType = RelationshipType.PREREQUISITE

    @classmethod
    def from_edge(cls, edge: GraphEdge) -> PrerequisiteRelationship | None:
        """Interpret a dependency-typed edge as a prerequisite relationship.

        Edge direction: concept ──prerequisite──▶ foundation.
        """
        if edge.relationship_type not in DEPENDENCY_RELATIONSHIPS:
            return None
        return cls(
            concept_id=edge.from_concept_id,
            prerequisite_id=edge.to_concept_id,
            edge_id=edge.edge_id,
            strength=edge.strength,
            confidence=edge.confidence,
            relationship_type=edge.relationship_type,
        )


def is_prerequisite_edge(edge: GraphEdge) -> bool:
    return edge.relationship_type in DEPENDENCY_RELATIONSHIPS
