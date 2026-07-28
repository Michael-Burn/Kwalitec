"""Educational decisions — reasoning outputs for Twin belief updates (AP-002D3).

Decisions are derived from EducationalObservationSet. They are not Twin state
and must never be treated as Assessment authority.
"""

from __future__ import annotations

from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.decisions.context import DecisionContext
from app.domain.reasoning.decisions.decision import EducationalDecision
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
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
from app.domain.reasoning.decisions.reason import DecisionReason
from app.domain.reasoning.decisions.reference import DecisionReference
from app.domain.reasoning.decisions.result import DecisionResult
from app.domain.reasoning.decisions.version import DECISION_VERSION, DecisionVersion

__all__ = [
    "DECISION_VERSION",
    "BrokenDecisionProvenance",
    "DecisionCategory",
    "DecisionContext",
    "DecisionError",
    "DecisionReason",
    "DecisionReference",
    "DecisionResult",
    "DecisionVersion",
    "DuplicateDecision",
    "EducationalDecision",
    "EducationalDecisionSet",
    "InvalidDecisionSchema",
    "InvalidLearningObjectiveReference",
    "MissingDecisionTraceability",
    "TwinUpdateRejected",
    "UnknownConceptReference",
    "UnknownDecisionCategory",
    "UnsupportedDecisionVersion",
]
