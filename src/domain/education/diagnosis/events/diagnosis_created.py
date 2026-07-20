"""Domain event: educational diagnosis was created.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    DiagnosisCreated
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.diagnosis.enums import DiagnosisSeverityLevel
from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
)
from domain.education.foundation.enums import ConfidenceLevel, DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId


@dataclass(frozen=True, slots=True)
class DiagnosisCreated(EducationalValueObject):
    """Immutable record that an EducationalDiagnosis was created."""

    diagnosis_id: DiagnosisId
    student_id: str
    diagnosis_type: DiagnosisType
    confidence_level: ConfidenceLevel
    severity_level: DiagnosisSeverityLevel
    indicator_count: int
    reason_count: int

    def _validate(self) -> None:
        if not isinstance(self.diagnosis_id, DiagnosisId):
            raise EducationalInvariantViolation(
                "diagnosis_id must be a DiagnosisId",
                invariant="DiagnosisCreated.diagnosis_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.diagnosis_type, DiagnosisType):
            raise EducationalInvariantViolation(
                "diagnosis_type must be a DiagnosisType",
                invariant="DiagnosisCreated.diagnosis_type.type",
            )
        if not isinstance(self.confidence_level, ConfidenceLevel):
            raise EducationalInvariantViolation(
                "confidence_level must be a ConfidenceLevel",
                invariant="DiagnosisCreated.confidence_level.type",
            )
        if self.confidence_level is ConfidenceLevel.UNKNOWN:
            raise EducationalInvariantViolation(
                "confidence_level must not be UNKNOWN",
                invariant="DiagnosisCreated.confidence_level.known",
            )
        if not isinstance(self.severity_level, DiagnosisSeverityLevel):
            raise EducationalInvariantViolation(
                "severity_level must be a DiagnosisSeverityLevel",
                invariant="DiagnosisCreated.severity_level.type",
            )
        if not isinstance(self.indicator_count, int) or self.indicator_count < 1:
            raise EducationalInvariantViolation(
                "indicator_count must be a positive integer",
                invariant="DiagnosisCreated.indicator_count.positive",
            )
        if not isinstance(self.reason_count, int) or self.reason_count < 1:
            raise EducationalInvariantViolation(
                "reason_count must be a positive integer",
                invariant="DiagnosisCreated.reason_count.positive",
            )
