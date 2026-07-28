"""Application Learning Graph projection pipeline (AP-002D4)."""

from __future__ import annotations

from app.application.learning_graph.projections.versions import (
    PROJECTION_VERSION,
    SUPPORTED_PROJECTION_VERSIONS,
)

__all__ = [
    "PROJECTION_VERSION",
    "SUPPORTED_PROJECTION_VERSIONS",
    "ProjectionPersistenceService",
    "ProjectionValidator",
    "RelationshipBuilder",
    "TwinProjectionService",
]


def __getattr__(name: str):
    if name == "TwinProjectionService":
        from app.application.learning_graph.projections.twin_projection_service import (
            TwinProjectionService,
        )

        return TwinProjectionService
    if name == "ProjectionValidator":
        from app.application.learning_graph.projections.validator import (
            ProjectionValidator,
        )

        return ProjectionValidator
    if name == "RelationshipBuilder":
        from app.application.learning_graph.projections.relationship_builder import (
            RelationshipBuilder,
        )

        return RelationshipBuilder
    if name == "ProjectionPersistenceService":
        from app.application.learning_graph.projections.persistence import (
            ProjectionPersistenceService,
        )

        return ProjectionPersistenceService
    raise AttributeError(name)
