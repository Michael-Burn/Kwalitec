"""LearningGraph aggregate — learner-specific knowledge interconnection model.

One graph exists per Student Digital Twin. The Twin remains the canonical
learner-state store; this aggregate owns relationship structure and traversal
metadata, referencing Twin mastery via MasteryLink rather than duplicating it.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime

from app.domain.learning_graph.dependency import DependencyChain
from app.domain.learning_graph.graph_edge import GraphEdge
from app.domain.learning_graph.graph_node import GraphNode, PrerequisiteStatus
from app.domain.learning_graph.graph_snapshot import GraphSnapshot
from app.domain.learning_graph.graph_traversal import (
    ImpactAnalysis,
    RecoveryPath,
    TraversalResult,
    connected_concepts,
    generate_recovery_path,
    impact_analysis,
    learning_path,
    traverse_dependencies,
    traverse_prerequisites,
)
from app.domain.learning_graph.graph_update import GraphUpdate
from app.domain.learning_graph.mastery_link import MasteryLink
from app.domain.learning_graph.prerequisite import PrerequisiteRelationship
from app.domain.learning_graph.relationship import DEPENDENCY_RELATIONSHIPS


@dataclass(frozen=True)
class LearningGraph:
    """Canonical learner knowledge graph aggregate.

    Owns: Nodes, Edges, Prerequisite Relationships, Mastery Links,
    Dependency Chains (derived), Traversal Metadata (derived).
    """

    graph_id: str
    twin_id: str
    student_id: str
    nodes: tuple[GraphNode, ...] = ()
    edges: tuple[GraphEdge, ...] = ()
    mastery_links: tuple[MasteryLink, ...] = ()
    update_history: tuple[GraphUpdate, ...] = ()
    snapshots: tuple[GraphSnapshot, ...] = ()
    created_at: datetime | None = None
    updated_at: datetime | None = None
    version: int = 1

    def __post_init__(self) -> None:
        if not (self.graph_id or "").strip():
            raise ValueError("graph_id is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        for when_attr in ("created_at", "updated_at"):
            when = getattr(self, when_attr)
            if when is not None and when.tzinfo is not None:
                object.__setattr__(
                    self, when_attr, when.astimezone(UTC).replace(tzinfo=None)
                )
        object.__setattr__(self, "nodes", tuple(self.nodes or ()))
        object.__setattr__(self, "edges", tuple(self.edges or ()))
        object.__setattr__(self, "mastery_links", tuple(self.mastery_links or ()))
        object.__setattr__(
            self, "update_history", tuple(self.update_history or ())
        )
        object.__setattr__(self, "snapshots", tuple(self.snapshots or ()))

    @classmethod
    def create(
        cls,
        *,
        graph_id: str,
        twin_id: str,
        student_id: str,
        created_at: datetime | None = None,
    ) -> LearningGraph:
        when = created_at or datetime.now(UTC).replace(tzinfo=None)
        return cls(
            graph_id=graph_id,
            twin_id=twin_id,
            student_id=student_id,
            created_at=when,
            updated_at=when,
            version=1,
        )

    # ── lookups ──────────────────────────────────────────────────────────

    def nodes_by_concept(self) -> dict[str, GraphNode]:
        return {n.concept_id: n for n in self.nodes}

    def get_node(self, concept_id: str) -> GraphNode | None:
        return self.nodes_by_concept().get(concept_id)

    def edges_from(self, concept_id: str) -> tuple[GraphEdge, ...]:
        return tuple(e for e in self.edges if e.from_concept_id == concept_id)

    def edges_to(self, concept_id: str) -> tuple[GraphEdge, ...]:
        return tuple(e for e in self.edges if e.to_concept_id == concept_id)

    def prerequisite_relationships(self) -> tuple[PrerequisiteRelationship, ...]:
        results: list[PrerequisiteRelationship] = []
        for edge in self.edges:
            rel = PrerequisiteRelationship.from_edge(edge)
            if rel is not None:
                results.append(rel)
        return tuple(results)

    def direct_prerequisites(self, concept_id: str) -> tuple[str, ...]:
        return tuple(
            sorted(
                e.to_concept_id
                for e in self.edges
                if e.from_concept_id == concept_id
                and e.relationship_type in DEPENDENCY_RELATIONSHIPS
            )
        )

    # ── mutations (immutable) ────────────────────────────────────────────

    def with_node(self, node: GraphNode) -> LearningGraph:
        if node.graph_id != self.graph_id:
            raise ValueError("node graph_id mismatch")
        others = tuple(n for n in self.nodes if n.concept_id != node.concept_id)
        return replace(
            self,
            nodes=(*others, node),
            updated_at=datetime.now(UTC).replace(tzinfo=None),
            version=self.version + 1,
        )

    def with_edge(self, edge: GraphEdge) -> LearningGraph:
        if edge.graph_id != self.graph_id:
            raise ValueError("edge graph_id mismatch")
        others = tuple(
            e
            for e in self.edges
            if not (
                e.from_concept_id == edge.from_concept_id
                and e.to_concept_id == edge.to_concept_id
                and e.relationship_type == edge.relationship_type
            )
        )
        return replace(
            self,
            edges=(*others, edge),
            updated_at=datetime.now(UTC).replace(tzinfo=None),
            version=self.version + 1,
        )

    def with_mastery_link(self, link: MasteryLink) -> LearningGraph:
        if link.graph_id != self.graph_id:
            raise ValueError("mastery link graph_id mismatch")
        others = tuple(
            m for m in self.mastery_links if m.concept_id != link.concept_id
        )
        return replace(
            self,
            mastery_links=(*others, link),
            updated_at=datetime.now(UTC).replace(tzinfo=None),
            version=self.version + 1,
        )

    def with_structure(
        self,
        *,
        nodes: tuple[GraphNode, ...] | None = None,
        edges: tuple[GraphEdge, ...] | None = None,
        mastery_links: tuple[MasteryLink, ...] | None = None,
        update: GraphUpdate | None = None,
        snapshot: GraphSnapshot | None = None,
        updated_at: datetime | None = None,
    ) -> LearningGraph:
        """Replace structural collections (used by sync services)."""
        when = updated_at or datetime.now(UTC).replace(tzinfo=None)
        history = self.update_history
        if update is not None:
            history = (*history, update)
        snaps = self.snapshots
        if snapshot is not None:
            snaps = (*snaps, snapshot)
        return replace(
            self,
            nodes=nodes if nodes is not None else self.nodes,
            edges=edges if edges is not None else self.edges,
            mastery_links=(
                mastery_links if mastery_links is not None else self.mastery_links
            ),
            update_history=history,
            snapshots=snaps,
            updated_at=when,
            version=self.version + 1,
        )

    def recompute_prerequisite_statuses(self) -> LearningGraph:
        """Refresh node.prerequisite_status from current edges + mastery projections."""
        by_concept = self.nodes_by_concept()
        updated_nodes: list[GraphNode] = []
        for node in self.nodes:
            prereqs = self.direct_prerequisites(node.concept_id)
            if not prereqs:
                status = PrerequisiteStatus.NONE
            else:
                scores = []
                for pid in prereqs:
                    pnode = by_concept.get(pid)
                    scores.append(pnode.mastery_score if pnode is not None else 0.0)
                if all(s >= 0.55 for s in scores):
                    status = PrerequisiteStatus.MET
                elif any(s >= 0.55 for s in scores):
                    status = PrerequisiteStatus.PARTIAL
                else:
                    status = PrerequisiteStatus.UNMET
            updated_nodes.append(
                replace(node, prerequisite_status=status)
                if node.prerequisite_status != status
                else node
            )
        return replace(
            self,
            nodes=tuple(updated_nodes),
            updated_at=datetime.now(UTC).replace(tzinfo=None),
            version=self.version + 1,
        )

    # ── traversal facade ─────────────────────────────────────────────────

    def traverse_prerequisites(
        self, concept_id: str, *, max_depth: int = 8
    ) -> TraversalResult:
        return traverse_prerequisites(
            seed_concept_id=concept_id,
            edges=self.edges,
            nodes_by_concept=self.nodes_by_concept(),
            max_depth=max_depth,
        )

    def traverse_dependencies(
        self, concept_id: str, *, max_depth: int = 8
    ) -> TraversalResult:
        return traverse_dependencies(
            seed_concept_id=concept_id,
            edges=self.edges,
            nodes_by_concept=self.nodes_by_concept(),
            max_depth=max_depth,
        )

    def recovery_path(
        self, concept_id: str, *, max_depth: int = 8
    ) -> RecoveryPath:
        return generate_recovery_path(
            seed_concept_id=concept_id,
            edges=self.edges,
            nodes_by_concept=self.nodes_by_concept(),
            max_depth=max_depth,
        )

    def impact(self, concept_id: str, *, max_depth: int = 8) -> ImpactAnalysis:
        return impact_analysis(
            seed_concept_id=concept_id,
            edges=self.edges,
            nodes_by_concept=self.nodes_by_concept(),
            max_depth=max_depth,
        )

    def connected(self, concept_id: str, *, max_depth: int = 2) -> TraversalResult:
        return connected_concepts(
            seed_concept_id=concept_id,
            edges=self.edges,
            nodes_by_concept=self.nodes_by_concept(),
            max_depth=max_depth,
        )

    def learning_path_for(
        self, concept_id: str, *, max_depth: int = 8
    ) -> DependencyChain:
        return learning_path(
            seed_concept_id=concept_id,
            edges=self.edges,
            nodes_by_concept=self.nodes_by_concept(),
            max_depth=max_depth,
        )

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        return len(self.edges)
