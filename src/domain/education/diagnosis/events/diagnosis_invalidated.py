"""Domain event: educational diagnosis was invalidated.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    DiagnosisInvalidated
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.education.foundation.base import (
    EducationalValueObject,
    require_identity_value,
    require_non_empty_text,
)
from domain.education.foundation.enums import DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId


@dataclass(frozen=True, slots=True)
class DiagnosisInvalidated(EducationalValueObject):
    """Immutable record that an EducationalDiagnosis was invalidated."""

    diagnosis_id: DiagnosisId
    student_id: str
    diagnosis_type: DiagnosisType
    reason: str

    def _validate(self) -> None:
        if not isinstance(self.diagnosis_id, DiagnosisId):
            raise EducationalInvariantViolation(
                "diagnosis_id must be a DiagnosisId",
                invariant="DiagnosisInvalidated.diagnosis_id.type",
            )
        object.__setattr__(
            self,
            "student_id",
            require_identity_value(self.student_id, "student_id"),
        )
        if not isinstance(self.diagnosis_type, DiagnosisType):
            raise EducationalInvariantViolation(
                "diagnosis_type must be a DiagnosisType",
                invariant="DiagnosisInvalidated.diagnosis_type.type",
            )
        object.__setattr__(
            self,
            "reason",
            require_non_empty_text(self.reason, "reason"),
        )
