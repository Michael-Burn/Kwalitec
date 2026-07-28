"""Interpretation domain artefacts (context, result, version, errors)."""

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
from app.domain.reasoning.interpretation.version import (
    INTERPRETATION_VERSION,
    InterpretationVersion,
)

__all__ = [
    "INTERPRETATION_VERSION",
    "BrokenEvidenceReference",
    "DuplicateInterpretedObservation",
    "InterpretationContext",
    "InterpretationError",
    "InterpretationResult",
    "InterpretationVersion",
    "InvalidConceptMapping",
    "MissingLearningObjective",
    "UnknownObservationCategory",
    "UnsupportedEvidenceSchema",
]
