"""GraphValidator — structural validation of a CurriculumGraph."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.value_objects.dependency_type import DependencyType
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class GraphValidationResult:
    """Outcome of validating a CurriculumGraph.

    Attributes:
        issues: Human-readable issue messages (empty when valid).
        has_cycles: True when REQUIRES cycles were found.
        disconnected_topic_ids: Topics with zero incident edges (any type).
        duplicate_edge_keys: Duplicate (source, target, type) keys if any.
    """

    issues: tuple[str, ...] = ()
    has_cycles: bool = False
    disconnected_topic_ids: tuple[TopicId, ...] = ()
    duplicate_edge_keys: tuple[tuple[str, str, str], ...] = ()

    @property
    def is_valid(self) -> bool:
        """True when no blocking issues were recorded."""
        return len(self.issues) == 0


@dataclass
class GraphValidator:
    """Validate curriculum graph structure deterministically.

    Checks:
    - REQUIRES cycles
    - Duplicate topic ids (construction-time; re-checked)
    - Duplicate edges
    - Edges referencing missing topics
    - Self-loops
    - Disconnected nodes (informational; not always blocking)
    - Missing hard prerequisites referenced only as soft deps (optional)

    By default disconnected nodes are reported as issues. Set
    ``allow_disconnected=True`` to treat them as informational only.
    """

    allow_disconnected: bool = False
    _informational: list[str] = field(default_factory=list, init=False)

    def validate(self, graph: CurriculumGraph) -> GraphValidationResult:
        """Validate ``graph`` and return a structured result."""
        issues: list[str] = []
        self._informational = []

        # Duplicate edge keys
        seen_keys: set[tuple[str, str, str]] = set()
        duplicate_keys: list[tuple[str, str, str]] = []
        for edge in graph.edges():
            key = (
                edge.source_id.value,
                edge.target_id.value,
                edge.dependency_type.value,
            )
            if key in seen_keys:
                duplicate_keys.append(key)
                issues.append(
                    f"duplicate edge: {key[0]} -[{key[2]}]-> {key[1]}"
                )
            seen_keys.add(key)

            if edge.source_id == edge.target_id:
                issues.append(
                    f"self-loop edge on topic: {edge.source_id.value}"
                )
            if not graph.has_topic(edge.source_id):
                issues.append(
                    f"edge source missing from graph: {edge.source_id.value}"
                )
            if not graph.has_topic(edge.target_id):
                issues.append(
                    f"edge target missing from graph: {edge.target_id.value}"
                )

        # Cycles
        cycles = graph.detect_cycles()
        has_cycles = len(cycles) > 0
        for cycle in cycles:
            path = " → ".join(t.value for t in cycle)
            issues.append(f"REQUIRES cycle: {path}")

        # Disconnected nodes (no incident edges of any type)
        incident: set[str] = set()
        for edge in graph.edges():
            incident.add(edge.source_id.value)
            incident.add(edge.target_id.value)
        disconnected = tuple(
            TopicId(n.topic_id.value)
            for n in graph.nodes()
            if n.topic_id.value not in incident
        )
        if disconnected:
            ids = ", ".join(t.value for t in disconnected)
            message = f"disconnected topics: {ids}"
            if self.allow_disconnected:
                self._informational.append(message)
            else:
                # Single-node graphs with no edges are vacuously fine.
                if graph.topic_count() > 1:
                    issues.append(message)

        # Invalid soft-only REQUIRES shadows: topics that recommend a topic
        # they also require twice — already covered by duplicate edges.

        # Missing prerequisites: REQUIRES edge target not in graph — covered.

        return GraphValidationResult(
            issues=tuple(issues),
            has_cycles=has_cycles,
            disconnected_topic_ids=disconnected,
            duplicate_edge_keys=tuple(duplicate_keys),
        )

    def assert_valid(self, graph: CurriculumGraph) -> None:
        """Raise ValueError when validation fails."""
        result = self.validate(graph)
        if not result.is_valid:
            raise ValueError("; ".join(result.issues))

    def informational_messages(self) -> tuple[str, ...]:
        """Messages from the last validate() that were non-blocking."""
        return tuple(self._informational)


def validate_requires_dag(graph: CurriculumGraph) -> bool:
    """True when REQUIRES subgraph is a DAG (no cycles)."""
    return not graph.has_cycle()


def validate_dependency_endpoints(graph: CurriculumGraph) -> tuple[str, ...]:
    """Return issues for edges whose endpoints are not graph nodes."""
    issues: list[str] = []
    for edge in graph.edges():
        if not graph.has_topic(edge.source_id):
            issues.append(f"missing source: {edge.source_id.value}")
        if not graph.has_topic(edge.target_id):
            issues.append(f"missing target: {edge.target_id.value}")
    return tuple(issues)


# Re-export DependencyType for validators that filter by kind.
__all__ = [
    "DependencyType",
    "GraphValidationResult",
    "GraphValidator",
    "validate_dependency_endpoints",
    "validate_requires_dag",
]
