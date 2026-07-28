"""Application layer for Tutor explainability (AP-002D6)."""

from __future__ import annotations

from app.application.intelligent_tutor.explainability.errors import (
    BrokenConceptReference,
    BrokenLearningObjectiveReference,
    DuplicateExplanationRequest,
    ExplanationError,
    ExplanationRejected,
    IncompleteProvenance,
    InvalidDecisionVersion,
    InvalidExplanationSchema,
    MissingExplanationInput,
    MissingProvenance,
    MissionVersionMismatch,
    TwinVersionMismatch,
    UnknownExplanationSchema,
    UnknownTwinVersion,
    UnsupportedExplanationContract,
)
from app.application.intelligent_tutor.explainability.explanation_builder import (
    ExplanationBuilder,
)
from app.application.intelligent_tutor.explainability.persistence import (
    ExplanationPersistenceService,
)
from app.application.intelligent_tutor.explainability.tutor_explanation_service import (
    TutorExplanationService,
)
from app.application.intelligent_tutor.explainability.validator import (
    ExplanationValidator,
)
from app.application.intelligent_tutor.explainability.versions import (
    EXPLANATION_PROVENANCE_PREFIX,
    EXPLANATION_VERSION,
    SUPPORTED_DECISION_VERSIONS_FOR_EXPLANATION,
    SUPPORTED_EXPLANATION_VERSIONS,
    SUPPORTED_PLANNING_VERSIONS_FOR_EXPLANATION,
)

__all__ = [
    "EXPLANATION_PROVENANCE_PREFIX",
    "EXPLANATION_VERSION",
    "SUPPORTED_DECISION_VERSIONS_FOR_EXPLANATION",
    "SUPPORTED_EXPLANATION_VERSIONS",
    "SUPPORTED_PLANNING_VERSIONS_FOR_EXPLANATION",
    "BrokenConceptReference",
    "BrokenLearningObjectiveReference",
    "DuplicateExplanationRequest",
    "ExplanationBuilder",
    "ExplanationError",
    "ExplanationPersistenceService",
    "ExplanationRejected",
    "ExplanationValidator",
    "IncompleteProvenance",
    "InvalidDecisionVersion",
    "InvalidExplanationSchema",
    "MissingExplanationInput",
    "MissingProvenance",
    "MissionVersionMismatch",
    "TutorExplanationService",
    "TwinVersionMismatch",
    "UnknownExplanationSchema",
    "UnknownTwinVersion",
    "UnsupportedExplanationContract",
]
