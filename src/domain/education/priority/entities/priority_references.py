"""Opaque references to upstream diagnosis and hypothesis aggregates.

Architecture Source
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Diagnosis Reference / Hypothesis Reference
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, HypothesisId


@dataclass(frozen=True, slots=True)
class DiagnosisReference(EducationalValueObject):
    """Opaque citation of an upstream EducationalDiagnosis.

    Priority references diagnoses by identity and type only. It does not
    import or load the Diagnosis package aggregates. Priority orders needs;
    it does not invent them.
    """

    diagnosis_id: DiagnosisId
    diagnosis_type: DiagnosisType

    def _validate(self) -> None:
        if not isinstance(self.diagnosis_id, DiagnosisId):
            raise EducationalInvariantViolation(
                "diagnosis_id must be a DiagnosisId",
                invariant="DiagnosisReference.diagnosis_id.type",
            )
        if not isinstance(self.diagnosis_type, DiagnosisType):
            raise EducationalInvariantViolation(
                "diagnosis_type must be a DiagnosisType",
                invariant="DiagnosisReference.diagnosis_type.type",
            )

    def __str__(self) -> str:
        return f"{self.diagnosis_id.value}:{self.diagnosis_type.value}"


@dataclass(frozen=True, slots=True)
class HypothesisReference(EducationalValueObject):
    """Opaque citation of an upstream EducationalHypothesis.

    Priority references hypotheses by identity only. It does not import or
    load the Hypothesis package aggregates, explain why a deficiency exists,
    or revise explanatory belief.
    """

    hypothesis_id: HypothesisId

    def _validate(self) -> None:
        if not isinstance(self.hypothesis_id, HypothesisId):
            raise EducationalInvariantViolation(
                "hypothesis_id must be a HypothesisId",
                invariant="HypothesisReference.hypothesis_id.type",
            )

    def __str__(self) -> str:
        return self.hypothesis_id.value
