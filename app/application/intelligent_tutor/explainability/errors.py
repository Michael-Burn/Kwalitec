"""Application-layer re-exports of Tutor explanation domain errors."""

from __future__ import annotations

from app.domain.intelligent_tutor.explainability.errors import (
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

__all__ = [
    "BrokenConceptReference",
    "BrokenLearningObjectiveReference",
    "DuplicateExplanationRequest",
    "ExplanationError",
    "ExplanationRejected",
    "IncompleteProvenance",
    "InvalidDecisionVersion",
    "InvalidExplanationSchema",
    "MissingExplanationInput",
    "MissingProvenance",
    "MissionVersionMismatch",
    "TwinVersionMismatch",
    "UnknownExplanationSchema",
    "UnknownTwinVersion",
    "UnsupportedExplanationContract",
]
