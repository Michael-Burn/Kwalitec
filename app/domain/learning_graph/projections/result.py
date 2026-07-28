"""ProjectionResult — immutable output of Twin→Graph projection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.domain.learning_graph.projections.batch import ProjectionBatch
from app.domain.learning_graph.projections.context import ProjectionContext
from app.domain.learning_graph.projections.events import (
    GraphProjectionCreated,
    GraphProjectionSkipped,
    GraphProjectionUpdated,
)
from app.domain.learning_graph.projections.projection import GraphProjection


@dataclass(frozen=True, slots=True)
class ProjectionResult:
    """Complete projection outcome ready for Graph persistence / replay."""

    context: ProjectionContext
    batch: ProjectionBatch
    graph_projection: GraphProjection
    projected_at: datetime
    events: tuple[
        GraphProjectionCreated | GraphProjectionUpdated | GraphProjectionSkipped, ...
    ] = ()

    def __post_init__(self) -> None:
        if self.context.reasoning_request_id != self.batch.context.reasoning_request_id:
            raise ValueError("reasoning_request_id mismatch")
        if self.context.evidence_bundle_id != self.batch.context.evidence_bundle_id:
            raise ValueError("evidence_bundle_id mismatch")
        if self.context.projection_version != self.batch.projection_version:
            raise ValueError("projection_version mismatch")
        if self.graph_projection.projection_id and (
            self.graph_projection.twin_id != self.context.twin_id
        ):
            raise ValueError("graph_projection twin_id mismatch")
        object.__setattr__(self, "events", tuple(self.events or ()))

    @property
    def projection_ids(self) -> tuple[str, ...]:
        return self.batch.projection_ids

    @property
    def relationship_count(self) -> int:
        return len(self.batch)

    @property
    def created_count(self) -> int:
        return sum(1 for e in self.events if isinstance(e, GraphProjectionCreated))

    @property
    def updated_count(self) -> int:
        return sum(1 for e in self.events if isinstance(e, GraphProjectionUpdated))

    @property
    def skipped_count(self) -> int:
        return sum(1 for e in self.events if isinstance(e, GraphProjectionSkipped))
