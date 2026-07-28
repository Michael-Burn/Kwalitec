"""Application reasoning package — educational evidence interpretation (AP-002D2).

Transforms Assessment EvidenceBundle facts into an immutable
EducationalObservationSet. Does not update Twin, Mission, Graph, or Tutor.
"""

from __future__ import annotations

from app.application.reasoning.dto.interpretation_dto import (
    InterpretationRequestDTO,
    InterpretationResultDTO,
    InterpretedObservationDTO,
)
from app.application.reasoning.interpretation.evidence_interpreter import (
    EvidenceInterpreter,
)
from app.application.reasoning.interpretation.versions import (
    INTERPRETATION_VERSION,
    SUPPORTED_PACKAGING_VERSIONS,
)
from app.domain.reasoning.interpretation.result import InterpretationResult

__all__ = [
    "INTERPRETATION_VERSION",
    "SUPPORTED_PACKAGING_VERSIONS",
    "EvidenceInterpreter",
    "InterpretationRequestDTO",
    "InterpretationResult",
    "InterpretationResultDTO",
    "InterpretedObservationDTO",
]
