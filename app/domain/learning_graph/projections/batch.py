"""ProjectionBatch — ordered immutable set of relationship projections."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_graph.projections.context import ProjectionContext
from app.domain.learning_graph.projections.relationship import RelationshipProjection


@dataclass(frozen=True)
class ProjectionBatch:
    """Ordered, immutable batch of relationship projections for one cycle."""

    batch_id: str
    relationships: tuple[RelationshipProjection, ...]
    context: ProjectionContext
    projection_version: str
    skipped_decision_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not (self.batch_id or "").strip():
            raise ValueError("batch_id is required")
        if not (self.projection_version or "").strip():
            raise ValueError("projection_version is required")
        if not isinstance(self.context, ProjectionContext):
            raise TypeError("context must be ProjectionContext")
        if self.context.projection_version != self.projection_version:
            raise ValueError("projection_version mismatch between context and batch")
        if not isinstance(self.relationships, tuple):
            object.__setattr__(self, "relationships", tuple(self.relationships))
        object.__setattr__(
            self, "skipped_decision_ids", tuple(self.skipped_decision_ids or ())
        )

        seen: set[str] = set()
        for rel in self.relationships:
            if not isinstance(rel, RelationshipProjection):
                raise TypeError(
                    "ProjectionBatch accepts RelationshipProjection only"
                )
            if rel.projection_id in seen:
                from app.domain.learning_graph.projections.errors import (
                    DuplicateProjection,
                )

                raise DuplicateProjection(
                    f"duplicate projection: {rel.projection_id!r}"
                )
            seen.add(rel.projection_id)
            if rel.twin_id != self.context.twin_id:
                raise ValueError("relationship twin_id mismatch with context")
            if rel.graph_id != self.context.graph_id:
                raise ValueError("relationship graph_id mismatch with context")
            if rel.projection_version != self.projection_version:
                raise ValueError("projection_version mismatch within batch")

    @property
    def projection_ids(self) -> tuple[str, ...]:
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

    def by_type(self, relationship_type: str) -> tuple[RelationshipProjection, ...]:
        return tuple(
            r
            for r in self.relationships
            if r.relationship_type.value == relationship_type
        )
