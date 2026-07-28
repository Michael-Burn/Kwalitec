"""Application reasoning package — interpretation + Twin decision integration.

AP-002D2: EvidenceBundle → EducationalObservationSet (no Twin write).
AP-002D3: EducationalObservationSet → EducationalDecisionSet → Twin belief.
Mission, Learning Graph, and Tutor remain untouched by this package.
"""

from __future__ import annotations

from app.application.reasoning.decisions.versions import (
    DECISION_VERSION,
    SUPPORTED_DECISION_VERSIONS,
)
from app.application.reasoning.interpretation.versions import (
    INTERPRETATION_VERSION,
    SUPPORTED_PACKAGING_VERSIONS,
)

__all__ = [
    "DECISION_VERSION",
    "INTERPRETATION_VERSION",
    "SUPPORTED_DECISION_VERSIONS",
    "SUPPORTED_PACKAGING_VERSIONS",
    "DecisionGenerator",
    "DecisionResultDTO",
    "EvidenceInterpreter",
    "InterpretationRequestDTO",
    "InterpretationResult",
    "InterpretationResultDTO",
    "InterpretedObservationDTO",
    "TwinUpdater",
]


def __getattr__(name: str):
    if name == "DecisionGenerator":
        from app.application.reasoning.decisions.decision_generator import (
            DecisionGenerator,
        )

        return DecisionGenerator
    if name == "TwinUpdater":
        from app.application.reasoning.decisions.twin_updater import TwinUpdater

        return TwinUpdater
    if name == "DecisionResultDTO":
        from app.application.reasoning.dto.decision_dto import DecisionResultDTO

        return DecisionResultDTO
    if name == "EvidenceInterpreter":
        from app.application.reasoning.interpretation.evidence_interpreter import (
            EvidenceInterpreter,
        )

        return EvidenceInterpreter
    if name in {
        "InterpretationRequestDTO",
        "InterpretationResultDTO",
        "InterpretedObservationDTO",
    }:
        from app.application.reasoning.dto import interpretation_dto as dto

        return getattr(dto, name)
    if name == "InterpretationResult":
        from app.domain.reasoning.interpretation.result import InterpretationResult

        return InterpretationResult
    raise AttributeError(name)
