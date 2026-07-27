"""Deterministic Learning Graph traversal primitives.

Pure functions / value objects — no I/O, no LLM, no randomness.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from app.domain.learning_graph.dependency import DependencyChain, DependencyHop
from app.domain.learning_graph.graph_edge import GraphEdge
from app.domain.learning_graph.graph_node import GraphNode
from app.domain.learning_graph.relationship import (
    DEPENDENCY_RELATIONSHIPS,
    RelationshipType,
)

# Mastery below this is treated as weak for recovery-path generation.
DEFAULT_WEAK_MASTERY_THRESHOLD = 0.55


@dataclass(frozen=True)
class TraversalResult:
    """Deterministic result of a graph traversal."""

    seed_concept_id: str
    visited_concept_ids: tuple[str, ...]
    chains: tuple[DependencyChain, ...]
    depth_by_concept: tuple[tuple[str, int], ...]
    kind: str = "prerequisites"

    def depths(self) -> dict[str, int]:
        return dict(self.depth_by_concept)


@dataclass(frozen=True)
class RecoveryPath:
    """Ordered recovery sequence for a weak concept.

    Concepts are ordered from deepest foundation toward the seed so the learner
    repairs dependencies before tackling the weak concept itself.
    The seed is included last when ``include_seed`` is True.
    """

    seed_concept_id: str
    concept_ids: tuple[str, ...]
    hops: tuple[DependencyHop, ...]
    reason: str = ""

    @property
    def length(self) -> int:
        return len(self.concept_ids)


@dataclass(frozen=True)
class ImpactAnalysis:
    """Concepts whose mastery is likely affected by a change to the seed."""

    seed_concept_id: str
    impacted_concept_ids: tuple[str, ...]
    hops: tuple[DependencyHop, ...]
    reason: str = ""


def traverse_prerequisites(
    *,
    seed_concept_id: str,
    edges: tuple[GraphEdge, ...],
    nodes_by_concept: dict[str, GraphNode],
    max_depth: int = 8,
) -> TraversalResult:
    """BFS upstream along dependency edges (concept → prerequisite)."""
    return _bfs(
        seed_concept_id=seed_concept_id,
        edges=edges,
        nodes_by_concept=nodes_by_concept,
        max_depth=max_depth,
        direction="upstream",
        kind="prerequisites",
    )


def traverse_dependencies(
    *,
    seed_concept_id: str,
    edges: tuple[GraphEdge, ...],
    nodes_by_concept: dict[str, GraphNode],
    max_depth: int = 8,
) -> TraversalResult:
    """BFS downstream: concepts that depend on the seed."""
    return _bfs(
        seed_concept_id=seed_concept_id,
        edges=edges,
        nodes_by_concept=nodes_by_concept,
        max_depth=max_depth,
        direction="downstream",
        kind="dependencies",
    )


def connected_concepts(
    *,
    seed_concept_id: str,
    edges: tuple[GraphEdge, ...],
    nodes_by_concept: dict[str, GraphNode],
    max_depth: int = 2,
) -> TraversalResult:
    """BFS over all relationship types (undirected neighbourhood)."""
    return _bfs(
        seed_concept_id=seed_concept_id,
        edges=edges,
        nodes_by_concept=nodes_by_concept,
        max_depth=max_depth,
        direction="undirected",
        kind="connected",
        dependency_only=False,
    )


def generate_recovery_path(
    *,
    seed_concept_id: str,
    edges: tuple[GraphEdge, ...],
    nodes_by_concept: dict[str, GraphNode],
    weak_threshold: float = DEFAULT_WEAK_MASTERY_THRESHOLD,
    max_depth: int = 8,
    include_seed: bool = True,
) -> RecoveryPath:
    """Build a deterministic recovery path for a weak concept.

    Collects weak prerequisites (and optionally the seed), ordered deepest
    foundation first so recovery proceeds bottom-up.
    """
    traversal = traverse_prerequisites(
        seed_concept_id=seed_concept_id,
        edges=edges,
        nodes_by_concept=nodes_by_concept,
        max_depth=max_depth,
    )
    # Sort by depth descending (deepest foundations first), then concept_id.
    candidates: list[DependencyHop] = []
    for concept_id, depth in traversal.depth_by_concept:
        if concept_id == seed_concept_id:
            continue
        node = nodes_by_concept.get(concept_id)
        score = node.mastery_score if node is not None else 0.0
        if score < weak_threshold:
            candidates.append(
                DependencyHop(
                    concept_id=concept_id,
                    concept_title=node.concept_title if node else "",
                    mastery_score=score,
                    depth=depth,
                )
            )
    candidates.sort(key=lambda h: (-h.depth, h.concept_id))

    hops = list(candidates)
    if include_seed:
        seed_node = nodes_by_concept.get(seed_concept_id)
        hops.append(
            DependencyHop(
                concept_id=seed_concept_id,
                concept_title=seed_node.concept_title if seed_node else "",
                mastery_score=seed_node.mastery_score if seed_node else 0.0,
                depth=0,
            )
        )

    reason = (
        f"Graph-driven recovery for {seed_concept_id}: "
        f"{len(candidates)} weak prerequisite(s) below {weak_threshold}"
    )
    return RecoveryPath(
        seed_concept_id=seed_concept_id,
        concept_ids=tuple(h.concept_id for h in hops),
        hops=tuple(hops),
        reason=reason,
    )


def impact_analysis(
    *,
    seed_concept_id: str,
    edges: tuple[GraphEdge, ...],
    nodes_by_concept: dict[str, GraphNode],
    max_depth: int = 8,
) -> ImpactAnalysis:
    """Concepts that depend on the seed (downstream educational impact)."""
    traversal = traverse_dependencies(
        seed_concept_id=seed_concept_id,
        edges=edges,
        nodes_by_concept=nodes_by_concept,
        max_depth=max_depth,
    )
    impacted = tuple(
        cid for cid in traversal.visited_concept_ids if cid != seed_concept_id
    )
    hops = tuple(
        DependencyHop(
            concept_id=cid,
            concept_title=(
                nodes_by_concept[cid].concept_title
                if cid in nodes_by_concept
                else ""
            ),
            mastery_score=(
                nodes_by_concept[cid].mastery_score
                if cid in nodes_by_concept
                else 0.0
            ),
            depth=traversal.depths().get(cid, 0),
        )
        for cid in impacted
    )
    return ImpactAnalysis(
        seed_concept_id=seed_concept_id,
        impacted_concept_ids=impacted,
        hops=hops,
        reason=(
            f"Downstream impact of {seed_concept_id}: "
            f"{len(impacted)} dependent concept(s)"
        ),
    )


def learning_path(
    *,
    seed_concept_id: str,
    edges: tuple[GraphEdge, ...],
    nodes_by_concept: dict[str, GraphNode],
    max_depth: int = 8,
) -> DependencyChain:
    """Ordered learning path: foundations → seed (topological-ish BFS order).

    Returns prerequisites sorted deepest-first, then the seed.
    """
    recovery = generate_recovery_path(
        seed_concept_id=seed_concept_id,
        edges=edges,
        nodes_by_concept=nodes_by_concept,
        weak_threshold=1.01,  # include all prerequisites regardless of mastery
        max_depth=max_depth,
        include_seed=True,
    )
    return DependencyChain(
        seed_concept_id=seed_concept_id,
        hops=recovery.hops,
        direction="learning_path",
    )


def _bfs(
    *,
    seed_concept_id: str,
    edges: tuple[GraphEdge, ...],
    nodes_by_concept: dict[str, GraphNode],
    max_depth: int,
    direction: str,
    kind: str,
    dependency_only: bool = True,
) -> TraversalResult:
    adjacency = _adjacency(
        edges, direction=direction, dependency_only=dependency_only
    )
    if not (seed_concept_id or "").strip():
        return TraversalResult(
            seed_concept_id=seed_concept_id or "",
            visited_concept_ids=(),
            chains=(),
            depth_by_concept=(),
            kind=kind,
        )

    visited: dict[str, int] = {seed_concept_id: 0}
    parent: dict[str, tuple[str, str, RelationshipType | None]] = {}
    queue: deque[str] = deque([seed_concept_id])

    while queue:
        current = queue.popleft()
        depth = visited[current]
        if depth >= max_depth:
            continue
        for neighbour, edge_id, rel in sorted(
            adjacency.get(current, ()), key=lambda t: t[0]
        ):
            if neighbour in visited:
                continue
            visited[neighbour] = depth + 1
            parent[neighbour] = (current, edge_id, rel)
            queue.append(neighbour)

    # Deterministic visit order: by depth, then concept_id.
    ordered = tuple(sorted(visited.keys(), key=lambda c: (visited[c], c)))
    depth_pairs = tuple((c, visited[c]) for c in ordered)

    chains: list[DependencyChain] = []
    # Primary chain: path from seed through each leaf (or all visited as one chain).
    hops = [
        DependencyHop(
            concept_id=seed_concept_id,
            concept_title=_title(seed_concept_id, nodes_by_concept),
            mastery_score=_score(seed_concept_id, nodes_by_concept),
            depth=0,
        )
    ]
    for concept_id in ordered:
        if concept_id == seed_concept_id:
            continue
        via = parent.get(concept_id)
        hops.append(
            DependencyHop(
                concept_id=concept_id,
                concept_title=_title(concept_id, nodes_by_concept),
                mastery_score=_score(concept_id, nodes_by_concept),
                depth=visited[concept_id],
                via_edge_id=via[1] if via else "",
                relationship_type=via[2] if via else None,
            )
        )
    chains.append(
        DependencyChain(
            seed_concept_id=seed_concept_id,
            hops=tuple(hops),
            direction=direction,
        )
    )

    return TraversalResult(
        seed_concept_id=seed_concept_id,
        visited_concept_ids=ordered,
        chains=tuple(chains),
        depth_by_concept=depth_pairs,
        kind=kind,
    )


def _adjacency(
    edges: tuple[GraphEdge, ...],
    *,
    direction: str,
    dependency_only: bool,
) -> dict[str, list[tuple[str, str, RelationshipType]]]:
    adj: dict[str, list[tuple[str, str, RelationshipType]]] = {}
    for edge in edges:
        if dependency_only and edge.relationship_type not in DEPENDENCY_RELATIONSHIPS:
            continue
        if direction == "upstream":
            # concept → prerequisite (follow edge as stored)
            adj.setdefault(edge.from_concept_id, []).append(
                (edge.to_concept_id, edge.edge_id, edge.relationship_type)
            )
        elif direction == "downstream":
            # prerequisite ← concept (reverse)
            adj.setdefault(edge.to_concept_id, []).append(
                (edge.from_concept_id, edge.edge_id, edge.relationship_type)
            )
        else:  # undirected
            adj.setdefault(edge.from_concept_id, []).append(
                (edge.to_concept_id, edge.edge_id, edge.relationship_type)
            )
            adj.setdefault(edge.to_concept_id, []).append(
                (edge.from_concept_id, edge.edge_id, edge.relationship_type)
            )
    return adj


def _title(concept_id: str, nodes: dict[str, GraphNode]) -> str:
    node = nodes.get(concept_id)
    return node.concept_title if node else ""


def _score(concept_id: str, nodes: dict[str, GraphNode]) -> float:
    node = nodes.get(concept_id)
    return node.mastery_score if node else 0.0
