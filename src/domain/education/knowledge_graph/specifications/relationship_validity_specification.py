"""Specification: every relationship edge in a graph is well-formed.

Architecture Source
    CONCEPT_NETWORK_MODEL.md
Concept
    RelationshipValiditySpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.enums import RelationshipType
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.knowledge_graph.value_objects.relationship_metadata import (
    RelationshipMetadata,
)

if TYPE_CHECKING:
    from domain.education.knowledge_graph.aggregates.knowledge_graph import (
        KnowledgeGraph,
    )


class RelationshipValiditySpecification:
    """True when every edge carries a well-typed, non-reflexive relationship.

    Guards against edges whose relationship, strength, or metadata have
    drifted from the value-object contract — for example after direct
    construction that bypasses the aggregate's own methods.
    """

    def is_satisfied_by(self, graph: KnowledgeGraph) -> bool:
        for edge in graph.edges:
            if not isinstance(edge.relationship_type, RelationshipType):
                return False
            if not isinstance(edge.strength, DependencyStrength):
                return False
            if not isinstance(edge.metadata, RelationshipMetadata):
                return False
            if edge.source_node_id == edge.target_node_id:
                return False
        return True

    def assert_satisfied_by(self, graph: KnowledgeGraph) -> None:
        if not self.is_satisfied_by(graph):
            raise EducationalInvariantViolation(
                "knowledge graph contains an invalid relationship edge",
                invariant="RelationshipValiditySpecification.unsatisfied",
            )
