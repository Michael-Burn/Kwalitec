"""Knowledge snapshot — an immutable, accurate mirror of a graph's state.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
    CONCEPT_NETWORK_MODEL.md
Concept
    Knowledge Snapshot
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.ids import KnowledgeGraphId
from domain.education.knowledge_graph.value_objects.knowledge_edge import (
    KnowledgeEdge,
)
from domain.education.knowledge_graph.value_objects.knowledge_node import (
    KnowledgeNode,
)


@dataclass(frozen=True, slots=True)
class KnowledgeSnapshot(EducationalValueObject):
    """Immutable, point-in-time read model of a KnowledgeGraph aggregate.

    A snapshot never invents or omits information — it must always be an
    accurate mirror of the aggregate that produced it.
    """

    graph_id: KnowledgeGraphId
    nodes: tuple[KnowledgeNode, ...]
    edges: tuple[KnowledgeEdge, ...]
    produced_at: datetime | None = None

    def _validate(self) -> None:
        if not isinstance(self.graph_id, KnowledgeGraphId):
            raise EducationalInvariantViolation(
                "graph_id must be a KnowledgeGraphId",
                invariant="KnowledgeSnapshot.graph_id.type",
            )
        if isinstance(self.nodes, list):
            object.__setattr__(self, "nodes", tuple(self.nodes))
        if not isinstance(self.nodes, tuple):
            raise EducationalInvariantViolation(
                "nodes must be a tuple of KnowledgeNode",
                invariant="KnowledgeSnapshot.nodes.type",
            )
        for node in self.nodes:
            if not isinstance(node, KnowledgeNode):
                raise EducationalInvariantViolation(
                    "every element of nodes must be a KnowledgeNode",
                    invariant="KnowledgeSnapshot.nodes.element_type",
                )
        node_ids = [node.node_id.value for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise EducationalInvariantViolation(
                "snapshot nodes must have unique identities",
                invariant="KnowledgeSnapshot.nodes.unique",
            )
        if isinstance(self.edges, list):
            object.__setattr__(self, "edges", tuple(self.edges))
        if not isinstance(self.edges, tuple):
            raise EducationalInvariantViolation(
                "edges must be a tuple of KnowledgeEdge",
                invariant="KnowledgeSnapshot.edges.type",
            )
        for edge in self.edges:
            if not isinstance(edge, KnowledgeEdge):
                raise EducationalInvariantViolation(
                    "every element of edges must be a KnowledgeEdge",
                    invariant="KnowledgeSnapshot.edges.element_type",
                )
        edge_keys = [
            (
                edge.source_node_id.value,
                edge.target_node_id.value,
                edge.relationship_type.value,
            )
            for edge in self.edges
        ]
        if len(edge_keys) != len(set(edge_keys)):
            raise EducationalInvariantViolation(
                "snapshot edges must be unique",
                invariant="KnowledgeSnapshot.edges.unique",
            )
        if self.produced_at is not None and not isinstance(self.produced_at, datetime):
            raise EducationalInvariantViolation(
                "produced_at must be a datetime when provided",
                invariant="KnowledgeSnapshot.produced_at.type",
            )

    def node_count(self) -> int:
        return len(self.nodes)

    def edge_count(self) -> int:
        return len(self.edges)
