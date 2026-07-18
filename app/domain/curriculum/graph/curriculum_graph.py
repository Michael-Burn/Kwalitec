"""CurriculumGraph — core educational knowledge graph.

Deterministic algorithms only: DFS, BFS, topological sort, cycle detection,
shortest prerequisite path. No AI, no heuristics.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from app.domain.curriculum.graph.graph_edge import GraphEdge
from app.domain.curriculum.graph.graph_node import GraphNode
from app.domain.curriculum.value_objects.dependency_type import DependencyType
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass
class CurriculumGraph:
    """Mutable educational dependency graph over topics.

    Nodes are topics. Directed edges encode DependencyType relationships.
    REQUIRES edges define the hard prerequisite DAG used for ordering and
    eligibility.
    """

    _nodes: dict[str, GraphNode] = field(default_factory=dict)
    _edges: list[GraphEdge] = field(default_factory=list)
    _edge_keys: set[tuple[str, str, str]] = field(default_factory=set)

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add_topic(self, node: GraphNode) -> None:
        """Add a topic node.

        Raises:
            ValueError: When the topic id already exists.
        """
        key = node.topic_id.value
        if key in self._nodes:
            raise ValueError(f"duplicate topic_id in graph: {key}")
        self._nodes[key] = node

    def remove_topic(self, topic_id: str | TopicId) -> bool:
        """Remove a topic and all incident edges. Returns True if removed."""
        key = TopicId.of(topic_id).value
        if key not in self._nodes:
            return False
        del self._nodes[key]
        remaining: list[GraphEdge] = []
        keys: set[tuple[str, str, str]] = set()
        for edge in self._edges:
            if edge.source_id.value == key or edge.target_id.value == key:
                continue
            remaining.append(edge)
            keys.add(_edge_key(edge))
        self._edges = remaining
        self._edge_keys = keys
        return True

    def connect_topics(
        self,
        source_id: str | TopicId,
        target_id: str | TopicId,
        dependency_type: DependencyType | str,
        *,
        edge_id: str | None = None,
        rationale: str | None = None,
    ) -> GraphEdge:
        """Add a directed dependency edge.

        Raises:
            ValueError: When endpoints missing, self-loop, or duplicate edge.
        """
        source = TopicId.of(source_id)
        target = TopicId.of(target_id)
        if source.value not in self._nodes:
            raise ValueError(f"source topic not in graph: {source.value}")
        if target.value not in self._nodes:
            raise ValueError(f"target topic not in graph: {target.value}")
        edge = GraphEdge.create(
            source,
            target,
            dependency_type,
            edge_id=edge_id,
            rationale=rationale,
        )
        key = _edge_key(edge)
        if key in self._edge_keys:
            raise ValueError("duplicate graph edge")
        self._edges.append(edge)
        self._edge_keys.add(key)
        return edge

    def add_edge(self, edge: GraphEdge) -> None:
        """Add a pre-built edge (endpoints must exist)."""
        if edge.source_id.value not in self._nodes:
            raise ValueError(f"source topic not in graph: {edge.source_id.value}")
        if edge.target_id.value not in self._nodes:
            raise ValueError(f"target topic not in graph: {edge.target_id.value}")
        key = _edge_key(edge)
        if key in self._edge_keys:
            raise ValueError("duplicate graph edge")
        self._edges.append(edge)
        self._edge_keys.add(key)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def has_topic(self, topic_id: str | TopicId) -> bool:
        """True when the topic is a node in the graph."""
        return TopicId.of(topic_id).value in self._nodes

    def get_node(self, topic_id: str | TopicId) -> GraphNode | None:
        """Return the node, or None."""
        return self._nodes.get(TopicId.of(topic_id).value)

    def nodes(self) -> tuple[GraphNode, ...]:
        """All nodes in stable topic_id order."""
        return tuple(
            self._nodes[k] for k in sorted(self._nodes.keys())
        )

    def edges(self) -> tuple[GraphEdge, ...]:
        """All edges in insertion order."""
        return tuple(self._edges)

    def topic_count(self) -> int:
        """Number of topic nodes."""
        return len(self._nodes)

    def edge_count(self) -> int:
        """Number of dependency edges."""
        return len(self._edges)

    def neighbours(
        self,
        topic_id: str | TopicId,
        *,
        dependency_type: DependencyType | None = None,
        direction: str = "both",
    ) -> tuple[TopicId, ...]:
        """Adjacent topic ids.

        Args:
            topic_id: Anchor topic.
            dependency_type: Optional filter by edge kind.
            direction: ``out`` (source→), ``in`` (→target), or ``both``.
        """
        tid = TopicId.of(topic_id)
        if tid.value not in self._nodes:
            raise ValueError(f"topic not in graph: {tid.value}")
        if direction not in {"out", "in", "both"}:
            raise ValueError("direction must be 'out', 'in', or 'both'")
        found: set[str] = set()
        for edge in self._edges:
            if (
                dependency_type is not None
                and edge.dependency_type is not dependency_type
            ):
                continue
            if direction in {"out", "both"} and edge.source_id == tid:
                found.add(edge.target_id.value)
            if direction in {"in", "both"} and edge.target_id == tid:
                found.add(edge.source_id.value)
        return tuple(TopicId(v) for v in sorted(found))

    def find_prerequisites(self, topic_id: str | TopicId) -> tuple[TopicId, ...]:
        """Direct REQUIRES targets (topics this topic hard-depends on)."""
        return self.neighbours(
            topic_id,
            dependency_type=DependencyType.REQUIRES,
            direction="out",
        )

    def find_successors(self, topic_id: str | TopicId) -> tuple[TopicId, ...]:
        """Topics that directly REQUIRES this topic (dependents)."""
        return self.neighbours(
            topic_id,
            dependency_type=DependencyType.REQUIRES,
            direction="in",
        )

    def find_revision_links(self, topic_id: str | TopicId) -> tuple[TopicId, ...]:
        """Topics connected via REVISION edges (either direction)."""
        return self.neighbours(
            topic_id,
            dependency_type=DependencyType.REVISION,
            direction="both",
        )

    def all_prerequisites(
        self, topic_id: str | TopicId, *, transitive: bool = True
    ) -> tuple[TopicId, ...]:
        """Direct or transitive REQUIRES prerequisites (excluding self)."""
        tid = TopicId.of(topic_id)
        if not transitive:
            return self.find_prerequisites(tid)
        return self._reachable_requires(tid, direction="out")

    def all_successors(
        self, topic_id: str | TopicId, *, transitive: bool = True
    ) -> tuple[TopicId, ...]:
        """Direct or transitive dependents via REQUIRES edges."""
        tid = TopicId.of(topic_id)
        if not transitive:
            return self.find_successors(tid)
        return self._reachable_requires(tid, direction="in")

    # ------------------------------------------------------------------
    # Traversal algorithms
    # ------------------------------------------------------------------

    def dfs(
        self,
        start: str | TopicId,
        *,
        dependency_type: DependencyType | None = DependencyType.REQUIRES,
        direction: str = "out",
    ) -> tuple[TopicId, ...]:
        """Depth-first traversal from ``start`` (deterministic neighbour order)."""
        start_id = TopicId.of(start)
        if start_id.value not in self._nodes:
            raise ValueError(f"topic not in graph: {start_id.value}")
        visited: set[str] = set()
        order: list[TopicId] = []

        def visit(current: TopicId) -> None:
            if current.value in visited:
                return
            visited.add(current.value)
            order.append(current)
            for neighbour in self.neighbours(
                current,
                dependency_type=dependency_type,
                direction=direction,
            ):
                visit(neighbour)

        visit(start_id)
        return tuple(order)

    def bfs(
        self,
        start: str | TopicId,
        *,
        dependency_type: DependencyType | None = DependencyType.REQUIRES,
        direction: str = "out",
    ) -> tuple[TopicId, ...]:
        """Breadth-first traversal from ``start`` (deterministic)."""
        start_id = TopicId.of(start)
        if start_id.value not in self._nodes:
            raise ValueError(f"topic not in graph: {start_id.value}")
        visited: set[str] = {start_id.value}
        order: list[TopicId] = [start_id]
        queue: deque[TopicId] = deque([start_id])
        while queue:
            current = queue.popleft()
            for neighbour in self.neighbours(
                current,
                dependency_type=dependency_type,
                direction=direction,
            ):
                if neighbour.value in visited:
                    continue
                visited.add(neighbour.value)
                order.append(neighbour)
                queue.append(neighbour)
        return tuple(order)

    def topological_ordering(self) -> tuple[TopicId, ...]:
        """Kahn topological sort over REQUIRES edges.

        Edge meaning: source REQUIRES target ⇒ target must precede source.
        Returns nodes with no REQUIRES constraints as well.

        Raises:
            ValueError: When a REQUIRES cycle exists.
        """
        # Build adjacency: prerequisite → dependents, and indegree of dependents.
        preds: dict[str, set[str]] = {k: set() for k in self._nodes}
        dependents: dict[str, set[str]] = {k: set() for k in self._nodes}
        for edge in self._edges:
            if edge.dependency_type is not DependencyType.REQUIRES:
                continue
            # source requires target ⇒ target precedes source
            src = edge.source_id.value
            tgt = edge.target_id.value
            preds[src].add(tgt)
            dependents[tgt].add(src)

        indegree = {k: len(preds[k]) for k in self._nodes}
        ready = sorted(k for k, deg in indegree.items() if deg == 0)
        order: list[TopicId] = []
        while ready:
            current = ready.pop(0)
            order.append(TopicId(current))
            for dep in sorted(dependents[current]):
                indegree[dep] -= 1
                if indegree[dep] == 0:
                    ready.append(dep)
                    ready.sort()
        if len(order) != len(self._nodes):
            raise ValueError("REQUIRES cycle detected; topological sort impossible")
        return tuple(order)

    def has_cycle(self) -> bool:
        """True when REQUIRES edges contain a directed cycle."""
        return len(self.detect_cycles()) > 0

    def detect_cycles(self) -> tuple[tuple[TopicId, ...], ...]:
        """Detect REQUIRES cycles via DFS colouring.

        Returns a tuple of cycles (each cycle as ordered topic ids).
        Deterministic: nodes visited in sorted id order.
        """
        white, gray, black = 0, 1, 2
        colour: dict[str, int] = {k: white for k in self._nodes}
        parent: dict[str, str | None] = {k: None for k in self._nodes}
        cycles: list[tuple[TopicId, ...]] = []
        adj: dict[str, list[str]] = {k: [] for k in self._nodes}
        for edge in self._edges:
            if edge.dependency_type is not DependencyType.REQUIRES:
                continue
            # Follow dependency direction source → target for cycle walk
            adj[edge.source_id.value].append(edge.target_id.value)
        for key in adj:
            adj[key].sort()

        def dfs(u: str, path: list[str]) -> None:
            colour[u] = gray
            path.append(u)
            for v in adj[u]:
                if colour[v] == white:
                    parent[v] = u
                    dfs(v, path)
                elif colour[v] == gray:
                    # Cycle: from v along path back to u then to v
                    if v in path:
                        idx = path.index(v)
                        cycle = tuple(TopicId(x) for x in path[idx:])
                        cycles.append(cycle)
            path.pop()
            colour[u] = black

        for node in sorted(self._nodes.keys()):
            if colour[node] == white:
                dfs(node, [])
        return tuple(cycles)

    def shortest_prerequisite_path(
        self,
        from_topic: str | TopicId,
        to_topic: str | TopicId,
    ) -> tuple[TopicId, ...] | None:
        """Shortest path along REQUIRES edges from ``from_topic`` to ``to_topic``.

        Walks source→target (dependency direction). Returns None if unreachable.
        """
        start = TopicId.of(from_topic)
        goal = TopicId.of(to_topic)
        if start.value not in self._nodes or goal.value not in self._nodes:
            raise ValueError("topic not in graph")
        if start == goal:
            return (start,)
        parent: dict[str, str | None] = {start.value: None}
        queue: deque[str] = deque([start.value])
        while queue:
            current = queue.popleft()
            for neighbour in self.neighbours(
                current,
                dependency_type=DependencyType.REQUIRES,
                direction="out",
            ):
                if neighbour.value in parent:
                    continue
                parent[neighbour.value] = current
                if neighbour == goal:
                    return _reconstruct_path(parent, goal.value)
                queue.append(neighbour.value)
        return None

    def validate(self) -> tuple[str, ...]:
        """Run built-in structural checks; return issue messages (empty = ok)."""
        from app.domain.curriculum.graph.graph_validator import GraphValidator

        return GraphValidator().validate(self).issues

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _reachable_requires(
        self, start: TopicId, *, direction: str
    ) -> tuple[TopicId, ...]:
        if start.value not in self._nodes:
            raise ValueError(f"topic not in graph: {start.value}")
        visited: set[str] = set()
        order: list[TopicId] = []
        queue: deque[TopicId] = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in self.neighbours(
                current,
                dependency_type=DependencyType.REQUIRES,
                direction=direction,
            ):
                if neighbour.value in visited or neighbour == start:
                    continue
                visited.add(neighbour.value)
                order.append(neighbour)
                queue.append(neighbour)
        return tuple(sorted(order, key=lambda t: t.value))


def _edge_key(edge: GraphEdge) -> tuple[str, str, str]:
    return (
        edge.source_id.value,
        edge.target_id.value,
        edge.dependency_type.value,
    )


def _reconstruct_path(
    parent: dict[str, str | None], goal: str
) -> tuple[TopicId, ...]:
    path: list[str] = [goal]
    current = goal
    while parent[current] is not None:
        current = parent[current]  # type: ignore[assignment]
        path.append(current)
    path.reverse()
    return tuple(TopicId(x) for x in path)
