"""Application-layer projection errors (re-export domain errors)."""

from __future__ import annotations

from app.domain.learning_graph.projections.errors import (
    BrokenConceptReference,
    BrokenProjectionProvenance,
    DuplicateProjection,
    IncompleteProjectionProvenance,
    InvalidDecisionVersion,
    InvalidProjectionSchema,
    MissingLearningObjective,
    ProjectionError,
    ProjectionRejected,
    UnknownProjectionRelationshipType,
    UnsupportedProjectionVersion,
)

__all__ = [
    "BrokenConceptReference",
    "BrokenProjectionProvenance",
    "DuplicateProjection",
    "IncompleteProjectionProvenance",
    "InvalidDecisionVersion",
    "InvalidProjectionSchema",
    "MissingLearningObjective",
    "ProjectionError",
    "ProjectionRejected",
    "UnknownProjectionRelationshipType",
    "UnsupportedProjectionVersion",
]
