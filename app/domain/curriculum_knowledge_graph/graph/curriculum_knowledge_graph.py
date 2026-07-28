"""CurriculumKnowledgeGraph — aggregate over structural nodes and edges.

Deterministic containment traversal and hard-prerequisite walks.
No AI, scoring, extraction, Twin, or persistence.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any

from app.domain.curriculum_knowledge_graph.entities.definition import Definition
from app.domain.curriculum_knowledge_graph.entities.formula import Formula
from app.domain.curriculum_knowledge_graph.entities.learning_objective import (
    LearningObjective,
)
from app.domain.curriculum_knowledge_graph.entities.practice_exercise import (
    PracticeExercise,
)
from app.domain.curriculum_knowledge_graph.entities.reading_reference import (
    ReadingReference,
)
from app.domain.curriculum_knowledge_graph.entities.section import Section
from app.domain.curriculum_knowledge_graph.entities.subject import Subject
from app.domain.curriculum_knowledge_graph.entities.subsection import Subsection
from app.domain.curriculum_knowledge_graph.entities.syllabus_outcome import (
    SyllabusOutcome,
)
from app.domain.curriculum_knowledge_graph.entities.topic import Topic
from app.domain.curriculum_knowledge_graph.entities.worked_example import (
    WorkedExample,
)
from app.domain.curriculum_knowledge_graph.graph.edge import CkgEdge
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    HARD_PREREQUISITE_TYPES,
    CkgRelationshipType,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
)

NodePayload = (
    Subject
    | Topic
    | Section
    | Subsection
    | LearningObjective
    | Definition
    | Formula
    | WorkedExample
    | PracticeExercise
    | ReadingReference
    | SyllabusOutcome
)


@dataclass
class CurriculumKnowledgeGraph:
    """Mutable educational knowledge graph for one subject edition.

    Structural containment is modelled both via entity ownership fields and
    explicit ``contains`` edges. Hard prerequisites use ``requires`` edges and
    must remain acyclic.
    """

    subject: Subject
    _nodes: dict[str, NodePayload] = field(default_factory=dict)
    _edges: list[CkgEdge] = field(default_factory=list)
    _edge_keys: set[tuple[str, str, str]] = field(default_factory=set)

    def __post_init__(self) -> None:
        sid = self.subject.stable_id.value
        if sid not in self._nodes:
            self._nodes[sid] = self.subject

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_node(self, node: NodePayload) -> None:
        """Register a node. Raises on duplicate stable_id."""
        key = node.stable_id.value
        if key in self._nodes:
            raise ValueError(f"duplicate stable_id in graph: {key}")
        if node.stable_id.subject_code != self.subject.code:
            # Subject.code may differ only by casing; compare subject stable id.
            if not key.startswith(self.subject.stable_id.value):
                raise ValueError(
                    "node stable_id must belong to graph subject "
                    f"{self.subject.stable_id.value}"
                )
        self._nodes[key] = node

    def add_edge(self, edge: CkgEdge) -> None:
        """Add a typed edge. Endpoints must exist. Rejects duplicate keys."""
        if edge.from_stable_id.value not in self._nodes:
            raise ValueError(
                f"edge source not in graph: {edge.from_stable_id.value}"
            )
        if edge.to_stable_id.value not in self._nodes:
            raise ValueError(
                f"edge target not in graph: {edge.to_stable_id.value}"
            )
        key = _edge_key(edge)
        if key in self._edge_keys:
            raise ValueError("duplicate graph edge")
        if edge.relationship_type in HARD_PREREQUISITE_TYPES:
            if self._would_cycle_requires(
                edge.from_stable_id.value, edge.to_stable_id.value
            ):
                raise ValueError("requires edge would create a cycle")
        self._edges.append(edge)
        self._edge_keys.add(key)

    def connect(
        self,
        from_stable_id: str | StableCurriculumId,
        to_stable_id: str | StableCurriculumId,
        relationship_type: CkgRelationshipType | str,
        *,
        edge_id: str | None = None,
        sequence_index: int = 0,
        rationale: str | None = None,
    ) -> CkgEdge:
        """Create and add a directed edge."""
        edge = CkgEdge.create(
            from_stable_id,
            to_stable_id,
            relationship_type,
            edge_id=edge_id,
            sequence_index=sequence_index,
            rationale=rationale,
        )
        self.add_edge(edge)
        return edge

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def has_node(self, stable_id: str | StableCurriculumId) -> bool:
        """True when the stable id is registered."""
        return StableCurriculumId.of(stable_id).value in self._nodes

    def get_node(self, stable_id: str | StableCurriculumId) -> NodePayload | None:
        """Return the node payload, or None."""
        return self._nodes.get(StableCurriculumId.of(stable_id).value)

    def nodes(self) -> tuple[NodePayload, ...]:
        """All nodes in stable_id sort order."""
        return tuple(self._nodes[k] for k in sorted(self._nodes))

    def edges(
        self,
        *,
        relationship_type: CkgRelationshipType | str | None = None,
    ) -> tuple[CkgEdge, ...]:
        """All edges, optionally filtered by type, in insertion order."""
        if relationship_type is None:
            return tuple(self._edges)
        rel = (
            relationship_type
            if isinstance(relationship_type, CkgRelationshipType)
            else CkgRelationshipType(relationship_type)
        )
        return tuple(e for e in self._edges if e.relationship_type is rel)

    def children(
        self,
        stable_id: str | StableCurriculumId,
        *,
        relationship_type: CkgRelationshipType = CkgRelationshipType.CONTAINS,
    ) -> tuple[str, ...]:
        """Stable ids of outgoing neighbours of the given type, sorted."""
        key = StableCurriculumId.of(stable_id).value
        found = [
            e.to_stable_id.value
            for e in self._edges
            if e.from_stable_id.value == key
            and e.relationship_type is relationship_type
        ]
        return tuple(sorted(found, key=lambda s: (s,)))

    def prerequisites(
        self, learning_objective_id: str | StableCurriculumId
    ) -> tuple[str, ...]:
        """Direct ``requires`` targets (prerequisites) for an LO."""
        return self.children(
            learning_objective_id,
            relationship_type=CkgRelationshipType.REQUIRES,
        )

    def traverse_containment(
        self, root_id: str | StableCurriculumId | None = None
    ) -> tuple[str, ...]:
        """Depth-first containment walk with stable sorted children."""
        start = (
            self.subject.stable_id.value
            if root_id is None
            else StableCurriculumId.of(root_id).value
        )
        if start not in self._nodes:
            raise ValueError(f"root not in graph: {start}")
        ordered: list[str] = []
        stack = [start]
        seen: set[str] = set()
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            ordered.append(current)
            kids = list(self.children(current))
            # DFS: push reversed so lowest sort order is visited first.
            for child in reversed(kids):
                if child not in seen:
                    stack.append(child)
        return tuple(ordered)

    def topological_learning_objectives(self) -> tuple[str, ...]:
        """Kahn topological order over LO nodes under ``requires`` edges.

        Isolated LOs are included in stable_id sort order among free nodes.
        """
        lo_ids = sorted(
            k
            for k, node in self._nodes.items()
            if isinstance(node, LearningObjective)
        )
        if not lo_ids:
            return ()
        lo_set = set(lo_ids)
        indegree = {k: 0 for k in lo_ids}
        adjacency: dict[str, list[str]] = {k: [] for k in lo_ids}
        for edge in self._edges:
            if edge.relationship_type not in HARD_PREREQUISITE_TYPES:
                continue
            # Edge A requires B means A depends on B: B precedes A.
            src = edge.from_stable_id.value
            tgt = edge.to_stable_id.value
            if src not in lo_set or tgt not in lo_set:
                continue
            adjacency[tgt].append(src)
            indegree[src] += 1
        queue = deque(sorted(k for k, d in indegree.items() if d == 0))
        result: list[str] = []
        while queue:
            node = queue.popleft()
            result.append(node)
            for nxt in sorted(adjacency[node]):
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
        if len(result) != len(lo_ids):
            raise ValueError("requires graph contains a cycle")
        return tuple(result)

    def to_snapshot(self) -> dict[str, Any]:
        """Deterministic structural snapshot for tests / debugging."""
        return {
            "subject_id": self.subject.stable_id.value,
            "edition_label": self.subject.edition_label,
            "node_ids": sorted(self._nodes),
            "edges": [
                {
                    "edge_id": e.edge_id,
                    "from": e.from_stable_id.value,
                    "to": e.to_stable_id.value,
                    "type": e.relationship_type.value,
                }
                for e in self._edges
            ],
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _would_cycle_requires(self, from_id: str, to_id: str) -> bool:
        """True if adding from→requires→to creates a cycle.

        ``from requires to`` means ``from`` depends on ``to``. A cycle exists
        if ``to`` can already reach ``from`` via requires edges.
        """
        # Walk prerequisites of ``to``; if we reach ``from``, adding the edge cycles.
        stack = [to_id]
        seen: set[str] = set()
        while stack:
            current = stack.pop()
            if current == from_id:
                return True
            if current in seen:
                continue
            seen.add(current)
            for edge in self._edges:
                if (
                    edge.relationship_type in HARD_PREREQUISITE_TYPES
                    and edge.from_stable_id.value == current
                ):
                    stack.append(edge.to_stable_id.value)
        return False


def _edge_key(edge: CkgEdge) -> tuple[str, str, str]:
    return (
        edge.from_stable_id.value,
        edge.to_stable_id.value,
        edge.relationship_type.value,
    )
