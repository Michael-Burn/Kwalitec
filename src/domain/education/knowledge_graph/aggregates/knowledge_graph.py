"""KnowledgeGraph aggregate root — educational structure of knowledge.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
    CONCEPT_NETWORK_MODEL.md
Concept
    Knowledge Dependency Graph
"""

from __future__ import annotations

from datetime import datetime

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.enums import RelationshipType
from domain.education.knowledge_graph.ids import (
    KnowledgeGraphId,
    KnowledgeNodeId,
    KnowledgeRelationshipId,
)
from domain.education.knowledge_graph.policies.cycle_detection_policy import (
    CycleDetectionPolicy,
)
from domain.education.knowledge_graph.policies.graph_validation_policy import (
    GraphValidationPolicy,
)
from domain.education.knowledge_graph.policies.learning_path_policy import (
    LearningPathPolicy,
)
from domain.education.knowledge_graph.policies.relationship_policy import (
    RelationshipPolicy,
)
from domain.education.knowledge_graph.value_objects.concept_cluster import (
    ConceptCluster,
)
from domain.education.knowledge_graph.value_objects.dependency_strength import (
    DependencyStrength,
)
from domain.education.knowledge_graph.value_objects.knowledge_edge import (
    KnowledgeEdge,
)
from domain.education.knowledge_graph.value_objects.knowledge_node import (
    KnowledgeNode,
)
from domain.education.knowledge_graph.value_objects.knowledge_path import (
    KnowledgePath,
)
from domain.education.knowledge_graph.value_objects.knowledge_relationship import (
    KnowledgeRelationship,
)
from domain.education.knowledge_graph.value_objects.knowledge_snapshot import (
    KnowledgeSnapshot,
)
from domain.education.knowledge_graph.value_objects.relationship_metadata import (
    RelationshipMetadata,
)


class KnowledgeGraph:
    """Aggregate root modelling the educational structure of knowledge.

    KnowledgeGraph describes how knowledge nodes depend upon, support, and
    relate to one another. It represents educational truth, independent of
    courses, subjects, UI navigation, study plans, or missions.

    The aggregate is the canonical source of prerequisite reasoning: it
    protects uniqueness of nodes and edges, forbids self-relationships,
    forbids duplicate edges, and forbids cycles among structural (strict
    dependency) relationships. Behaviour is exposed only through methods —
    no public mutable collections.
    """

    def __init__(
        self,
        graph_id: KnowledgeGraphId,
        *,
        nodes: list[KnowledgeNode] | tuple[KnowledgeNode, ...] | None = None,
        edges: list[KnowledgeEdge] | tuple[KnowledgeEdge, ...] | None = None,
    ) -> None:
        self._graph_id = GraphValidationPolicy.assert_identity(graph_id)
        node_list = GraphValidationPolicy.assert_nodes(nodes or ())
        self._nodes: dict[str, KnowledgeNode] = {
            node.node_id.value: node for node in node_list
        }
        self._edges: list[KnowledgeEdge] = GraphValidationPolicy.assert_edges(
            edges or (), self._nodes
        )

    @classmethod
    def create(cls, graph_id: KnowledgeGraphId) -> KnowledgeGraph:
        """Factory: create a new, empty KnowledgeGraph."""
        return cls(graph_id=graph_id)

    # --- identity / read models (no setters) ---

    @property
    def graph_id(self) -> KnowledgeGraphId:
        return self._graph_id

    @property
    def nodes(self) -> tuple[KnowledgeNode, ...]:
        return tuple(self._nodes.values())

    @property
    def edges(self) -> tuple[KnowledgeEdge, ...]:
        return tuple(self._edges)

    def node_count(self) -> int:
        return len(self._nodes)

    def edge_count(self) -> int:
        return len(self._edges)

    def has_node(self, node_id: KnowledgeNodeId) -> bool:
        return node_id.value in self._nodes

    def node_for(self, node_id: KnowledgeNodeId) -> KnowledgeNode | None:
        return self._nodes.get(node_id.value)

    def has_edge(
        self,
        source_node_id: KnowledgeNodeId,
        target_node_id: KnowledgeNodeId,
        relationship_type: RelationshipType,
    ) -> bool:
        return any(
            edge.source_node_id == source_node_id
            and edge.target_node_id == target_node_id
            and edge.relationship_type == relationship_type
            for edge in self._edges
        )

    def edges_from(self, node_id: KnowledgeNodeId) -> tuple[KnowledgeEdge, ...]:
        """Outgoing edges owned by ``node_id``."""
        self._require_registered(node_id)
        return tuple(edge for edge in self._edges if edge.source_node_id == node_id)

    def edges_to(self, node_id: KnowledgeNodeId) -> tuple[KnowledgeEdge, ...]:
        """Incoming edges pointing at ``node_id``."""
        self._require_registered(node_id)
        return tuple(edge for edge in self._edges if edge.target_node_id == node_id)

    # --- mutation ---

    def add_node(self, node: KnowledgeNode) -> None:
        """Register a new knowledge node. Node identities must be unique."""
        if not isinstance(node, KnowledgeNode):
            raise EducationalInvariantViolation(
                "node must be a KnowledgeNode",
                invariant="KnowledgeGraph.add_node.type",
            )
        if node.node_id.value in self._nodes:
            raise EducationalInvariantViolation(
                "node is already registered in the knowledge graph",
                invariant="KnowledgeGraph.add_node.duplicate",
            )
        self._nodes[node.node_id.value] = node

    def remove_node(self, node_id: KnowledgeNodeId) -> None:
        """Remove a node and every edge touching it (cascading removal)."""
        self._require_registered(node_id)
        del self._nodes[node_id.value]
        self._edges = [
            edge
            for edge in self._edges
            if edge.source_node_id != node_id and edge.target_node_id != node_id
        ]

    def connect(
        self,
        source_node_id: KnowledgeNodeId,
        target_node_id: KnowledgeNodeId,
        relationship_type: RelationshipType,
        *,
        strength: DependencyStrength | None = None,
        metadata: RelationshipMetadata | None = None,
    ) -> KnowledgeEdge:
        """Create a typed relationship edge from ``source`` to ``target``.

        Both endpoints must already be registered. Structural relationship
        types are additionally checked against the acyclic invariant before
        the edge is committed.

        Returns:
            The created KnowledgeEdge.

        Raises:
            EducationalInvariantViolation: On unknown endpoints, a
                self-relationship, a duplicate edge, or a structural cycle.
        """
        self._require_registered(source_node_id)
        self._require_registered(target_node_id)
        relationship = KnowledgeRelationship.of(
            target_node_id,
            relationship_type,
            strength=strength,
            metadata=metadata,
        )
        existing_from_source = self.edges_from(source_node_id)
        RelationshipPolicy.assert_can_connect(
            existing_from_source, source_node_id, relationship
        )
        if RelationshipPolicy.is_structural(relationship_type):
            candidate_pairs = [
                (edge.source_node_id, edge.target_node_id)
                for edge in self._structural_edges()
            ]
            candidate_pairs.append((source_node_id, target_node_id))
            CycleDetectionPolicy.assert_acyclic(candidate_pairs)
        edge = KnowledgeEdge(
            relationship_id=KnowledgeRelationshipId.for_edge(
                source_node_id, target_node_id, relationship_type
            ),
            source_node_id=source_node_id,
            relationship=relationship,
        )
        self._edges.append(edge)
        return edge

    def disconnect(
        self,
        source_node_id: KnowledgeNodeId,
        target_node_id: KnowledgeNodeId,
        relationship_type: RelationshipType,
    ) -> None:
        """Remove the matching relationship edge, if present."""
        for index, edge in enumerate(self._edges):
            if (
                edge.source_node_id == source_node_id
                and edge.target_node_id == target_node_id
                and edge.relationship_type == relationship_type
            ):
                del self._edges[index]
                return
        raise EducationalInvariantViolation(
            "no matching knowledge edge exists to disconnect",
            invariant="KnowledgeGraph.disconnect.not_found",
        )

    # --- graph reasoning ---

    def find_prerequisites(
        self,
        node_id: KnowledgeNodeId,
        *,
        transitive: bool = False,
    ) -> tuple[KnowledgeNodeId, ...]:
        """Structural prerequisites of ``node_id``.

        Direct prerequisites are the targets of ``node_id``'s outgoing
        structural edges. Transitive prerequisites additionally include
        every prerequisite reachable by following further structural edges.
        """
        self._require_registered(node_id)
        if not transitive:
            return tuple(
                edge.target_node_id
                for edge in self._structural_edges()
                if edge.source_node_id == node_id
            )
        return self._traverse_structural(node_id, forward=True)

    def find_dependents(
        self,
        node_id: KnowledgeNodeId,
        *,
        transitive: bool = False,
    ) -> tuple[KnowledgeNodeId, ...]:
        """Nodes that structurally depend on ``node_id``.

        Direct dependents are the sources of structural edges pointing at
        ``node_id``. Transitive dependents additionally include every node
        reachable by following further incoming structural edges.
        """
        self._require_registered(node_id)
        if not transitive:
            return tuple(
                edge.source_node_id
                for edge in self._structural_edges()
                if edge.target_node_id == node_id
            )
        return self._traverse_structural(node_id, forward=False)

    def find_foundations(self, node_id: KnowledgeNodeId) -> tuple[KnowledgeNodeId, ...]:
        """The foundational nodes underpinning ``node_id``.

        A foundation is a node with no further structural prerequisites of
        its own. When ``node_id`` itself has none, it is its own foundation.
        """
        self._require_registered(node_id)
        reachable = self._traverse_structural(node_id, forward=True)
        candidates = (node_id, *reachable) if not reachable else reachable
        foundations = [
            candidate
            for candidate in candidates
            if not self._has_structural_outgoing(candidate)
        ]
        if not foundations:
            return (node_id,)
        return tuple(foundations)

    def find_learning_path(
        self,
        start_node_id: KnowledgeNodeId,
        target_node_id: KnowledgeNodeId,
    ) -> KnowledgePath:
        """The shortest structural learning path from ``start`` to ``target``.

        A learning path exists when ``target`` structurally depends on
        ``start`` (directly or transitively). The returned path is ordered
        from ``start`` to ``target``.

        Raises:
            EducationalInvariantViolation: When no such path exists.
        """
        self._require_registered(start_node_id)
        self._require_registered(target_node_id)
        if start_node_id == target_node_id:
            return KnowledgePath((start_node_id,))
        path = self._shortest_structural_path(target_node_id, start_node_id)
        validated = LearningPathPolicy.assert_reachable(
            path, start=start_node_id, target=target_node_id
        )
        return KnowledgePath(tuple(reversed(validated.nodes)))

    def find_concept_clusters(self) -> tuple[ConceptCluster, ...]:
        """Connected groups of nodes joined by advisory relationships.

        Clusters are computed over an undirected graph built solely from
        advisory relationship types. Nodes with no advisory relationships
        do not appear in any cluster.
        """
        adjacency: dict[str, set[str]] = {}
        for edge in self._edges:
            if not RelationshipPolicy.is_advisory(edge.relationship_type):
                continue
            source_key = edge.source_node_id.value
            target_key = edge.target_node_id.value
            adjacency.setdefault(source_key, set()).add(target_key)
            adjacency.setdefault(target_key, set()).add(source_key)

        visited: set[str] = set()
        clusters: list[ConceptCluster] = []
        cluster_index = 0
        for node_key in self._nodes:
            if node_key in visited or node_key not in adjacency:
                continue
            component: list[str] = []
            queue = [node_key]
            visited.add(node_key)
            while queue:
                current = queue.pop(0)
                component.append(current)
                for neighbour in adjacency.get(current, ()):
                    if neighbour not in visited:
                        visited.add(neighbour)
                        queue.append(neighbour)
            if len(component) >= 2:
                cluster_index += 1
                clusters.append(
                    ConceptCluster(
                        cluster_id=f"cluster-{cluster_index}",
                        node_ids=tuple(self._nodes[key].node_id for key in component),
                    )
                )
        return tuple(clusters)

    def detect_cycles(self) -> tuple[tuple[KnowledgeNodeId, ...], ...]:
        """Detect cycles among structural relationships, if any exist.

        The graph enforces acyclicity of structural relationships at every
        mutation, so this normally returns an empty tuple. It remains
        available as an explicit consistency check.
        """
        pairs = [
            (edge.source_node_id, edge.target_node_id)
            for edge in self._structural_edges()
        ]
        cycle = CycleDetectionPolicy.find_cycle(pairs)
        if cycle is None:
            return ()
        return (cycle,)

    def produce_snapshot(
        self, *, produced_at: datetime | None = None
    ) -> KnowledgeSnapshot:
        """Produce an immutable, accurate snapshot of current graph state."""
        return KnowledgeSnapshot(
            graph_id=self._graph_id,
            nodes=tuple(self._nodes.values()),
            edges=tuple(self._edges),
            produced_at=produced_at,
        )

    # --- internals ---

    def _require_registered(self, node_id: KnowledgeNodeId) -> None:
        if node_id.value not in self._nodes:
            raise EducationalInvariantViolation(
                "node is not registered in the knowledge graph",
                invariant="KnowledgeGraph.node.not_registered",
            )

    def _structural_edges(self) -> tuple[KnowledgeEdge, ...]:
        return tuple(
            edge
            for edge in self._edges
            if RelationshipPolicy.is_structural(edge.relationship_type)
        )

    def _has_structural_outgoing(self, node_id: KnowledgeNodeId) -> bool:
        return any(edge.source_node_id == node_id for edge in self._structural_edges())

    def _traverse_structural(
        self, node_id: KnowledgeNodeId, *, forward: bool
    ) -> tuple[KnowledgeNodeId, ...]:
        """Breadth-first traversal of structural edges, excluding ``node_id``.

        ``forward=True`` walks outgoing edges (prerequisites); ``forward=
        False`` walks incoming edges (dependents).
        """
        structural = self._structural_edges()
        visited: set[str] = {node_id.value}
        order: list[KnowledgeNodeId] = []
        queue: list[KnowledgeNodeId] = [node_id]
        while queue:
            current = queue.pop(0)
            neighbours = (
                (
                    edge.target_node_id
                    for edge in structural
                    if edge.source_node_id == current
                )
                if forward
                else (
                    edge.source_node_id
                    for edge in structural
                    if edge.target_node_id == current
                )
            )
            for neighbour in neighbours:
                if neighbour.value in visited:
                    continue
                visited.add(neighbour.value)
                order.append(neighbour)
                queue.append(neighbour)
        return tuple(order)

    def _shortest_structural_path(
        self, from_node_id: KnowledgeNodeId, to_node_id: KnowledgeNodeId
    ) -> KnowledgePath | None:
        """Shortest structural path (BFS) from ``from_node_id`` to ``to_node_id``.

        Follows outgoing structural edges only. Returns ``None`` when
        ``to_node_id`` is unreachable from ``from_node_id``.
        """
        if from_node_id == to_node_id:
            return KnowledgePath((from_node_id,))
        structural = self._structural_edges()
        predecessors: dict[str, KnowledgeNodeId] = {}
        visited: set[str] = {from_node_id.value}
        queue: list[KnowledgeNodeId] = [from_node_id]
        while queue:
            current = queue.pop(0)
            for edge in structural:
                if edge.source_node_id != current:
                    continue
                neighbour = edge.target_node_id
                if neighbour.value in visited:
                    continue
                visited.add(neighbour.value)
                predecessors[neighbour.value] = current
                if neighbour == to_node_id:
                    return KnowledgePath(
                        tuple(
                            self._reconstruct_path(
                                predecessors, from_node_id, to_node_id
                            )
                        )
                    )
                queue.append(neighbour)
        return None

    @staticmethod
    def _reconstruct_path(
        predecessors: dict[str, KnowledgeNodeId],
        from_node_id: KnowledgeNodeId,
        to_node_id: KnowledgeNodeId,
    ) -> tuple[KnowledgeNodeId, ...]:
        path: list[KnowledgeNodeId] = [to_node_id]
        current = to_node_id
        while current.value != from_node_id.value:
            current = predecessors[current.value]
            path.append(current)
        path.reverse()
        return tuple(path)

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, KnowledgeGraph):
            return NotImplemented
        return self._graph_id == other._graph_id

    def __hash__(self) -> int:
        return hash((type(self), self._graph_id))

    def __repr__(self) -> str:
        return (
            f"KnowledgeGraph(graph_id={self._graph_id!r}, "
            f"nodes={len(self._nodes)}, edges={len(self._edges)})"
        )
