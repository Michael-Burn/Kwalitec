"""RevisionPathService — revision clusters and review sequences."""

from __future__ import annotations

from collections import deque

from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.value_objects.dependency_type import DependencyType
from app.domain.curriculum.value_objects.topic_id import TopicId


class RevisionPathService:
    """Determine related concepts, revision clusters, and review sequences.

    Operates on REVISION edges (and optionally RELATED). Deterministic
    connected-component clustering; no AI.
    """

    def __init__(self, graph: CurriculumGraph) -> None:
        self._graph = graph

    def related_concepts(
        self,
        topic_id: str | TopicId,
        *,
        include_related: bool = True,
    ) -> tuple[TopicId, ...]:
        """Direct revision (and optionally RELATED) neighbours."""
        tid = TopicId.of(topic_id)
        found: set[str] = set()
        for neighbour in self._graph.find_revision_links(tid):
            found.add(neighbour.value)
        if include_related:
            for neighbour in self._graph.neighbours(
                tid,
                dependency_type=DependencyType.RELATED,
                direction="both",
            ):
                found.add(neighbour.value)
        found.discard(tid.value)
        return tuple(TopicId(v) for v in sorted(found))

    def revision_clusters(self) -> tuple[tuple[TopicId, ...], ...]:
        """Connected components over undirected REVISION edges.

        Isolated topics (no revision edges) form singleton clusters.
        Clusters are ordered by their minimum topic_id; members sorted.
        """
        # Build undirected adjacency from REVISION edges
        adj: dict[str, set[str]] = {
            n.topic_id.value: set() for n in self._graph.nodes()
        }
        for edge in self._graph.edges():
            if edge.dependency_type is not DependencyType.REVISION:
                continue
            a, b = edge.source_id.value, edge.target_id.value
            adj[a].add(b)
            adj[b].add(a)

        visited: set[str] = set()
        clusters: list[tuple[TopicId, ...]] = []
        for start in sorted(adj.keys()):
            if start in visited:
                continue
            component: list[str] = []
            queue: deque[str] = deque([start])
            visited.add(start)
            while queue:
                current = queue.popleft()
                component.append(current)
                for neighbour in sorted(adj[current]):
                    if neighbour in visited:
                        continue
                    visited.add(neighbour)
                    queue.append(neighbour)
            clusters.append(tuple(TopicId(x) for x in sorted(component)))

        clusters.sort(key=lambda c: c[0].value if c else "")
        return tuple(clusters)

    def cluster_for(self, topic_id: str | TopicId) -> tuple[TopicId, ...]:
        """Revision cluster containing ``topic_id``."""
        tid = TopicId.of(topic_id)
        for cluster in self.revision_clusters():
            if tid in cluster:
                return cluster
        raise ValueError(f"topic not in graph: {tid.value}")

    def recommended_review_sequence(
        self,
        topic_id: str | TopicId,
        *,
        completed: set[str]
        | set[TopicId]
        | frozenset[str]
        | frozenset[TopicId]
        | None = None,
    ) -> tuple[TopicId, ...]:
        """Deterministic review order for the topic's revision cluster.

        Order:
        1. Prefer incomplete topics first (if ``completed`` provided)
        2. Within that, topological REQUIRES order restricted to the cluster
        3. Fallback: sorted topic ids

        The seed topic is included.
        """
        cluster = self.cluster_for(topic_id)
        cluster_set = {t.value for t in cluster}
        completed_ids = {TopicId.of(t).value for t in (completed or set())}

        # Topological order for whole graph, then filter to cluster.
        try:
            topo = self._graph.topological_ordering()
            ordered = [t for t in topo if t.value in cluster_set]
        except ValueError:
            ordered = sorted(cluster, key=lambda t: t.value)

        # Ensure every cluster member appears (isolated from REQUIRES).
        seen = {t.value for t in ordered}
        for tid in cluster:
            if tid.value not in seen:
                ordered.append(tid)

        if completed is None:
            return tuple(ordered)

        incomplete = [t for t in ordered if t.value not in completed_ids]
        complete = [t for t in ordered if t.value in completed_ids]
        return tuple(incomplete + complete)
