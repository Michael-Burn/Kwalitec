"""Approved Learning Graph projection relationship types (AP-002D4).

These describe educational *relationships* projected from Twin decisions.
They never author mastery belief — Twin remains authoritative for belief.
"""

from __future__ import annotations

from enum import StrEnum


class ProjectionRelationshipType(StrEnum):
    """Canonical relationship kinds that may be projected onto the Graph."""

    LEARNING_OBJECTIVE_CONCEPT = "learning_objective_concept"
    CONCEPT_CONCEPT = "concept_concept"
    STUDENT_LEARNING_OBJECTIVE = "student_learning_objective"
    STUDENT_CONCEPT = "student_concept"
    STUDENT_MISCONCEPTION = "student_misconception"
    PREREQUISITE = "prerequisite"
    DEPENDENCY = "dependency"


KNOWN_PROJECTION_RELATIONSHIP_TYPES: frozenset[str] = frozenset(
    item.value for item in ProjectionRelationshipType
)


def parse_projection_relationship_type(
    value: str | ProjectionRelationshipType,
) -> ProjectionRelationshipType:
    """Parse a relationship type or raise for unknown values (never invent)."""
    if isinstance(value, ProjectionRelationshipType):
        return value
    normalised = (value or "").strip()
    if normalised not in KNOWN_PROJECTION_RELATIONSHIP_TYPES:
        from app.domain.learning_graph.projections.errors import (
            UnknownProjectionRelationshipType,
        )

        raise UnknownProjectionRelationshipType(
            f"unknown projection relationship type: {value!r}"
        )
    return ProjectionRelationshipType(normalised)
