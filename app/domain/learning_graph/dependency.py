"""Dependency chain — ordered educational dependency path."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_graph.relationship import RelationshipType


@dataclass(frozen=True)
class DependencyHop:
    """One hop in a dependency chain."""

    concept_id: str
    concept_title: str = ""
    mastery_score: float = 0.0
    depth: int = 0
    via_edge_id: str = ""
    relationship_type: RelationshipType | None = None


@dataclass(frozen=True)
class DependencyChain:
    """Ordered chain from a seed concept toward foundations (or dependents).

    ``hops[0]`` is the seed. Subsequent hops are prerequisites (upstream) or
    dependents (downstream) depending on traversal direction.
    """

    seed_concept_id: str
    hops: tuple[DependencyHop, ...]
    direction: str = "upstream"  # upstream = prerequisites; downstream = dependents

    @property
    def concept_ids(self) -> tuple[str, ...]:
        return tuple(h.concept_id for h in self.hops)

    @property
    def length(self) -> int:
        return max(0, len(self.hops) - 1)
