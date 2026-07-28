"""RelationshipProjection — one immutable educational relationship for the Graph.

Represents a graph update only. Never stores independent mastery authority.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.domain.learning_graph.projections.reference import ProjectionReference
from app.domain.learning_graph.projections.relationship_type import (
    ProjectionRelationshipType,
    parse_projection_relationship_type,
)


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True)
class RelationshipProjection:
    """One immutable educational relationship projected from a Twin decision.

    Endpoints are opaque educational identifiers (student / LO / concept /
    misconception). Mastery scores are never authoritative here — only Twin
    decision references.
    """

    projection_id: str
    relationship_type: ProjectionRelationshipType
    from_ref: str
    to_ref: str
    twin_id: str
    graph_id: str
    reference: ProjectionReference
    projection_version: str
    created_at: datetime
    decision_id: str
    twin_decision_ref: str = ""
    provenance: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if not (self.projection_id or "").strip():
            raise ValueError("projection_id is required")
        if not (self.from_ref or "").strip():
            raise ValueError("from_ref is required")
        if not (self.to_ref or "").strip():
            raise ValueError("to_ref is required")
        if not (self.twin_id or "").strip():
            raise ValueError("twin_id is required")
        if not (self.graph_id or "").strip():
            raise ValueError("graph_id is required")
        if not (self.decision_id or "").strip():
            raise ValueError("decision_id is required")
        if not (self.projection_version or "").strip():
            raise ValueError("projection_version is required")
        if not isinstance(self.reference, ProjectionReference):
            raise TypeError("reference must be ProjectionReference")

        rel = parse_projection_relationship_type(self.relationship_type)
        object.__setattr__(self, "relationship_type", rel)

        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )

        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))
        object.__setattr__(self, "payload", _freeze_mapping(self.payload))
        if not (self.twin_decision_ref or "").strip():
            object.__setattr__(self, "twin_decision_ref", self.decision_id)
