"""Application-layer decision errors (re-export domain errors)."""

from __future__ import annotations

from app.domain.reasoning.decisions.errors import (
    BrokenDecisionProvenance,
    DecisionError,
    DuplicateDecision,
    InvalidDecisionSchema,
    InvalidLearningObjectiveReference,
    MissingDecisionTraceability,
    TwinUpdateRejected,
    UnknownConceptReference,
    UnknownDecisionCategory,
    UnsupportedDecisionVersion,
)

__all__ = [
    "BrokenDecisionProvenance",
    "DecisionError",
    "DuplicateDecision",
    "InvalidDecisionSchema",
    "InvalidLearningObjectiveReference",
    "MissingDecisionTraceability",
    "TwinUpdateRejected",
    "UnknownConceptReference",
    "UnknownDecisionCategory",
    "UnsupportedDecisionVersion",
]
