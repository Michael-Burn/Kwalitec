"""Relationship types for Learning Graph edges."""

from __future__ import annotations

from enum import StrEnum


class RelationshipType(StrEnum):
    """Directed relationship between two curriculum concepts on a learner graph.

    Direction convention:
      from_concept ──type──▶ to_concept

    For PREREQUISITE / DEPENDS_ON / REVISION_DEPENDENCY, ``to_concept`` is the
    dependency (must be learned / recovered first). STRENGTHENS and
    RELATED_CONCEPT are associative supports.
    """

    PREREQUISITE = "prerequisite"
    DEPENDS_ON = "depends_on"
    STRENGTHENS = "strengthens"
    RELATED_CONCEPT = "related_concept"
    REVISION_DEPENDENCY = "revision_dependency"


# Edges that define educational dependency chains (traverse toward foundations).
DEPENDENCY_RELATIONSHIPS: frozenset[RelationshipType] = frozenset(
    {
        RelationshipType.PREREQUISITE,
        RelationshipType.DEPENDS_ON,
        RelationshipType.REVISION_DEPENDENCY,
    }
)
