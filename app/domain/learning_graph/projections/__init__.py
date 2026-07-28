"""Learning Graph projections — Twin decisions → educational relationships (AP-002D4).

The Graph stores relationships only. Twin remains authoritative for learner belief.
Projection never reasons, never invents mastery, never notifies Mission/Tutor.
"""

from __future__ import annotations

from app.domain.learning_graph.projections.batch import ProjectionBatch
from app.domain.learning_graph.projections.context import ProjectionContext
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
from app.domain.learning_graph.projections.events import (
    GraphProjectionCreated,
    GraphProjectionSkipped,
    GraphProjectionUpdated,
    ProjectionEventKind,
)
from app.domain.learning_graph.projections.projection import GraphProjection
from app.domain.learning_graph.projections.reference import ProjectionReference
from app.domain.learning_graph.projections.relationship import RelationshipProjection
from app.domain.learning_graph.projections.relationship_type import (
    KNOWN_PROJECTION_RELATIONSHIP_TYPES,
    ProjectionRelationshipType,
    parse_projection_relationship_type,
)
from app.domain.learning_graph.projections.result import ProjectionResult
from app.domain.learning_graph.projections.version import (
    PROJECTION_VERSION,
    ProjectionVersion,
)

__all__ = [
    "KNOWN_PROJECTION_RELATIONSHIP_TYPES",
    "PROJECTION_VERSION",
    "BrokenConceptReference",
    "BrokenProjectionProvenance",
    "DuplicateProjection",
    "GraphProjection",
    "GraphProjectionCreated",
    "GraphProjectionSkipped",
    "GraphProjectionUpdated",
    "IncompleteProjectionProvenance",
    "InvalidDecisionVersion",
    "InvalidProjectionSchema",
    "MissingLearningObjective",
    "ProjectionBatch",
    "ProjectionContext",
    "ProjectionError",
    "ProjectionEventKind",
    "ProjectionRejected",
    "ProjectionReference",
    "ProjectionRelationshipType",
    "ProjectionResult",
    "ProjectionVersion",
    "RelationshipProjection",
    "UnknownProjectionRelationshipType",
    "UnsupportedProjectionVersion",
    "parse_projection_relationship_type",
]
