"""Opaque references to priority, diagnosis, and hypothesis aggregates.

Architecture Source
    TEACHING_INTENTION_MODEL.md
Concept
    Priority Reference / Diagnosis Reference / Hypothesis Reference
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import EducationalValueObject
from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId, HypothesisId, PriorityId


@dataclass(frozen=True, slots=True)
class PriorityReference(EducationalValueObject):
    """Opaque citation of an upstream EducationalPriority.

    Teaching Intention must reference a Priority. It does not import or load
    the Priority package aggregate, recalculate ordering, or invent need.
    """

    priority_id: PriorityId

    def _validate(self) -> None:
        if not isinstance(self.priority_id, PriorityId):
            raise EducationalInvariantViolation(
                "priority_id must be a PriorityId",
                invariant="PriorityReference.priority_id.type",
            )

    def __str__(self) -> str:
        return self.priority_id.value


@dataclass(frozen=True, slots=True)
class DiagnosisReference(EducationalValueObject):
    """Opaque citation of an upstream EducationalDiagnosis.

    Intention references diagnoses by identity and type only. Alignment
    policies use diagnosis_type without loading Diagnosis aggregates.
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

    Intention may be informed by hypothesis. It does not revise explanatory
    belief or select teaching strategy.
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
