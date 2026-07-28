"""GraphProjection — immutable projection artefact for one graph update cycle."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any

from app.domain.learning_graph.projections.context import ProjectionContext
from app.domain.learning_graph.projections.relationship import RelationshipProjection


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    return MappingProxyType(dict(value or {}))


@dataclass(frozen=True)
class GraphProjection:
    """Immutable Learning Graph projection derived from Twin decisions.

    Graph updates only — not learner state. Twin remains authoritative when
    Graph and Twin disagree.
    """

    projection_id: str
    graph_id: str
    twin_id: str
    context: ProjectionContext
    relationships: tuple[RelationshipProjection, ...]
    projection_version: str
    twin_version: int
    created_at: datetime
    prior_projection_ids: tuple[str, ...] = ()
    provenance: Mapping[str, Any] = field(
        default_factory=lambda: MappingProxyType({})
    )

    def __post_init__(self) -> None:
        if not (self.projection_id or "").strip():
            raise ValueError("projection_id is required")
        if not isinstance(self.context, ProjectionContext):
            raise TypeError("context must be ProjectionContext")
        if self.context.twin_id != self.twin_id:
            raise ValueError("twin_id mismatch with context")
        if self.context.graph_id != self.graph_id:
            raise ValueError("graph_id mismatch with context")
        if self.context.projection_version != self.projection_version:
            raise ValueError("projection_version mismatch with context")
        if self.twin_version < 1:
            raise ValueError("twin_version must be >= 1")

        when = self.created_at
        if when.tzinfo is not None:
            object.__setattr__(
                self, "created_at", when.astimezone(UTC).replace(tzinfo=None)
            )

        if not isinstance(self.relationships, tuple):
            object.__setattr__(self, "relationships", tuple(self.relationships))
        object.__setattr__(
            self, "prior_projection_ids", tuple(self.prior_projection_ids or ())
        )
        object.__setattr__(self, "provenance", _freeze_mapping(self.provenance))

        seen: set[str] = set()
        for rel in self.relationships:
            if not isinstance(rel, RelationshipProjection):
                raise TypeError("relationships must be RelationshipProjection")
            if rel.projection_id in seen:
                from app.domain.learning_graph.projections.errors import (
                    DuplicateProjection,
                )

                raise DuplicateProjection(
                    f"duplicate relationship projection: {rel.projection_id!r}"
                )
            seen.add(rel.projection_id)
            if rel.twin_id != self.twin_id:
                raise ValueError("relationship twin_id mismatch")
            if rel.graph_id != self.graph_id:
                raise ValueError("relationship graph_id mismatch")

    @property
    def relationship_ids(self) -> tuple[str, ...]:
        return tuple(r.projection_id for r in self.relationships)

    @property
    def decision_ids(self) -> tuple[str, ...]:
        ids: list[str] = []
        seen: set[str] = set()
        for rel in self.relationships:
            if rel.decision_id not in seen:
                seen.add(rel.decision_id)
                ids.append(rel.decision_id)
        return tuple(ids)

    def __len__(self) -> int:
        return len(self.relationships)
