"""Policy validating KnowledgeGraph aggregate shapes.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md / CONCEPT_NETWORK_MODEL.md
Concept
    Graph Validation Policy
"""

from __future__ import annotations

from collections.abc import Mapping

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.ids import KnowledgeGraphId
from domain.education.knowledge_graph.policies.cycle_detection_policy import (
    CycleDetectionPolicy,
)
from domain.education.knowledge_graph.policies.relationship_policy import (
    RelationshipPolicy,
)
from domain.education.knowledge_graph.value_objects.knowledge_edge import (
    KnowledgeEdge,
)
from domain.education.knowledge_graph.value_objects.knowledge_node import (
    KnowledgeNode,
)


class GraphValidationPolicy:
    """Validates KnowledgeGraph shapes — no educational reasoning.

    Structural correctness only: unique identities, resolvable endpoints,
    no duplicate edges, no self-relationships, and acyclic structural
    relationships. Educational judgement about *which* dependency is true
    lives outside this policy.
    """

    @staticmethod
    def assert_identity(graph_id: KnowledgeGraphId) -> KnowledgeGraphId:
        if not isinstance(graph_id, KnowledgeGraphId):
            raise EducationalInvariantViolation(
                "graph must possess a KnowledgeGraphId identity",
                invariant="KnowledgeGraph.identity.required",
            )
        return graph_id

    @staticmethod
    def assert_nodes(
        nodes: list[KnowledgeNode] | tuple[KnowledgeNode, ...],
    ) -> list[KnowledgeNode]:
        items = list(nodes)
        seen: set[str] = set()
        for node in items:
            if not isinstance(node, KnowledgeNode):
                raise EducationalInvariantViolation(
                    "nodes must contain KnowledgeNode value objects",
                    invariant="KnowledgeGraph.nodes.type",
                )
            key = node.node_id.value
            if key in seen:
                raise EducationalInvariantViolation(
                    "duplicate node identity in knowledge graph",
                    invariant="KnowledgeGraph.nodes.unique",
                )
            seen.add(key)
        return items

    @staticmethod
    def assert_edges(
        edges: list[KnowledgeEdge] | tuple[KnowledgeEdge, ...],
        nodes_by_id: Mapping[str, KnowledgeNode],
    ) -> list[KnowledgeEdge]:
        items = list(edges)
        seen_keys: set[tuple[str, str, str]] = set()
        structural_pairs = []
        for edge in items:
            if not isinstance(edge, KnowledgeEdge):
                raise EducationalInvariantViolation(
                    "edges must contain KnowledgeEdge value objects",
                    invariant="KnowledgeGraph.edges.type",
                )
            if edge.source_node_id.value not in nodes_by_id:
                raise EducationalInvariantViolation(
                    "edge source node must be registered in the graph",
                    invariant="KnowledgeGraph.edges.source_not_registered",
                )
            if edge.target_node_id.value not in nodes_by_id:
                raise EducationalInvariantViolation(
                    "edge target node must be registered in the graph",
                    invariant="KnowledgeGraph.edges.target_not_registered",
                )
            edge.relationship.assert_not_self(edge.source_node_id)
            key = (
                edge.source_node_id.value,
                edge.target_node_id.value,
                edge.relationship_type.value,
            )
            if key in seen_keys:
                raise EducationalInvariantViolation(
                    "duplicate knowledge edge in knowledge graph",
                    invariant="KnowledgeGraph.edges.unique",
                )
            seen_keys.add(key)
            if RelationshipPolicy.is_structural(edge.relationship_type):
                structural_pairs.append((edge.source_node_id, edge.target_node_id))
        CycleDetectionPolicy.assert_acyclic(structural_pairs)
        return items
