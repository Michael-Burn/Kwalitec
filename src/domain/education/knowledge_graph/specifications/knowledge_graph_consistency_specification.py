"""Specification: a KnowledgeGraph is internally consistent.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    KnowledgeGraphConsistencySpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.policies.cycle_detection_policy import (
    CycleDetectionPolicy,
)
from domain.education.knowledge_graph.policies.relationship_policy import (
    RelationshipPolicy,
)

if TYPE_CHECKING:
    from domain.education.knowledge_graph.aggregates.knowledge_graph import (
        KnowledgeGraph,
    )


class KnowledgeGraphConsistencySpecification:
    """True when a graph's nodes and edges remain structurally coherent.

    Consistency is structural integrity — unique node identities, unique
    edges, resolvable endpoints, no self-relationships, and an acyclic
    structural dependency subgraph. It is not a judgement of whether the
    graph's educational claims are correct.
    """

    def is_satisfied_by(self, graph: KnowledgeGraph) -> bool:
        node_ids = [node.node_id.value for node in graph.nodes]
        if len(node_ids) != len(set(node_ids)):
            return False
        node_id_set = set(node_ids)

        edge_keys = [
            (
                edge.source_node_id.value,
                edge.target_node_id.value,
                edge.relationship_type.value,
            )
            for edge in graph.edges
        ]
        if len(edge_keys) != len(set(edge_keys)):
            return False

        for edge in graph.edges:
            if edge.source_node_id.value not in node_id_set:
                return False
            if edge.target_node_id.value not in node_id_set:
                return False
            if edge.source_node_id == edge.target_node_id:
                return False

        structural_pairs = [
            (edge.source_node_id, edge.target_node_id)
            for edge in graph.edges
            if RelationshipPolicy.is_structural(edge.relationship_type)
        ]
        if CycleDetectionPolicy.find_cycle(structural_pairs) is not None:
            return False

        return True

    def assert_satisfied_by(self, graph: KnowledgeGraph) -> None:
        if not self.is_satisfied_by(graph):
            raise EducationalInvariantViolation(
                "knowledge graph is not internally consistent",
                invariant="KnowledgeGraphConsistencySpecification.unsatisfied",
            )
