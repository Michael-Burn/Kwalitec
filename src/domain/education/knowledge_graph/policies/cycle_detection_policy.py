"""Policy detecting cycles among directed structural relationship edges.

Architecture Source
    KNOWLEDGE_DEPENDENCY_MODEL.md
Concept
    Cycle Detection Policy

Prerequisite-like relationships must form a directed acyclic structure:
learnability cannot honestly depend on itself, directly or transitively.
"""

from __future__ import annotations

from collections.abc import Sequence

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.knowledge_graph.ids import KnowledgeNodeId

_WHITE, _GRAY, _BLACK = 0, 1, 2


class CycleDetectionPolicy:
    """Deterministic depth-first cycle detection over directed edges.

    Operates purely on the supplied edge pairs — no randomness, no wall
    clock, and no dependency on dict/set iteration order beyond the stable
    insertion order the caller provides.
    """

    @staticmethod
    def find_cycle(
        edges: Sequence[tuple[KnowledgeNodeId, KnowledgeNodeId]],
    ) -> tuple[KnowledgeNodeId, ...] | None:
        """Return the first cycle discovered, or ``None`` when acyclic.

        Args:
            edges: Directed (source, target) pairs to search for a cycle.

        Returns:
            A tuple of node identities describing the cycle, starting and
            ending at the same node, or ``None`` when no cycle exists.
        """
        registry: dict[str, KnowledgeNodeId] = {}
        adjacency: dict[str, list[str]] = {}
        for source, target in edges:
            registry.setdefault(source.value, source)
            registry.setdefault(target.value, target)
            adjacency.setdefault(source.value, []).append(target.value)

        color: dict[str, int] = dict.fromkeys(registry, _WHITE)
        stack: list[str] = []
        cycle: list[str] | None = None

        def visit(node_key: str) -> None:
            nonlocal cycle
            color[node_key] = _GRAY
            stack.append(node_key)
            for neighbour in adjacency.get(node_key, []):
                neighbour_color = color.get(neighbour, _WHITE)
                if neighbour_color == _WHITE:
                    visit(neighbour)
                elif neighbour_color == _GRAY:
                    start = stack.index(neighbour)
                    cycle = [*stack[start:], neighbour]
                if cycle is not None:
                    return
            stack.pop()
            color[node_key] = _BLACK

        for node_key in registry:
            if cycle is not None:
                break
            if color[node_key] == _WHITE:
                visit(node_key)

        if cycle is None:
            return None
        return tuple(registry[key] for key in cycle)

    @staticmethod
    def assert_acyclic(
        edges: Sequence[tuple[KnowledgeNodeId, KnowledgeNodeId]],
    ) -> None:
        """Raise when the supplied directed edges contain a cycle."""
        cycle = CycleDetectionPolicy.find_cycle(edges)
        if cycle is not None:
            path = " -> ".join(node_id.value for node_id in cycle)
            raise EducationalInvariantViolation(
                f"cycle detected among prerequisite relationships: {path}",
                invariant="CycleDetectionPolicy.cycle_detected",
            )
