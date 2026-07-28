"""Reasoning domain — educational observations and interpretation (AP-002D2).

Interpretation prepares immutable educational observations for later Twin
consumption. It does not estimate mastery, update learner belief, or produce
recommendations.
"""

from __future__ import annotations

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
    "BrokenEvidenceReference",
    "DuplicateInterpretedObservation",
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
