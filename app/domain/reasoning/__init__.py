"""Reasoning domain — observations, interpretation, and decisions (AP-002D).

Interpretation prepares immutable educational observations. Decisions derive
Twin belief update requests from those observations. Twin state is never
copied from observations.
"""

from __future__ import annotations

from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.decisions.context import DecisionContext
from app.domain.reasoning.decisions.decision import EducationalDecision
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.reasoning.decisions.reason import DecisionReason
from app.domain.reasoning.decisions.reference import DecisionReference
from app.domain.reasoning.decisions.result import DecisionResult
from app.domain.reasoning.decisions.version import DECISION_VERSION, DecisionVersion
from app.domain.reasoning.interpretation.context import InterpretationContext
from app.domain.reasoning.interpretation.errors import (
    BrokenEvidenceReference,
    DuplicateInterpretedObservation,
    InterpretationError,
    InvalidConceptMapping,
    MissingLearningObjective,
    UnknownObservationCategory,
    UnsupportedEvidenceSchema,
)
from app.domain.reasoning.interpretation.result import InterpretationResult
from app.domain.reasoning.interpretation.version import InterpretationVersion
from app.domain.reasoning.observations.category import ObservationCategory
from app.domain.reasoning.observations.observation import EducationalObservation
from app.domain.reasoning.observations.observation_set import EducationalObservationSet

__all__ = [
    "DECISION_VERSION",
    "BrokenEvidenceReference",
    "DecisionCategory",
    "DecisionContext",
    "DecisionReason",
    "DecisionReference",
    "DecisionResult",
    "DecisionVersion",
    "DuplicateInterpretedObservation",
    "EducationalDecision",
    "EducationalDecisionSet",
    "EducationalObservation",
    "EducationalObservationSet",
    "InterpretationContext",
    "InterpretationError",
    "InterpretationResult",
    "InterpretationVersion",
    "InvalidConceptMapping",
    "MissingLearningObjective",
    "ObservationCategory",
    "UnknownObservationCategory",
    "UnsupportedEvidenceSchema",
]
