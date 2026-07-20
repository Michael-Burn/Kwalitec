"""Specification: EducationalDiagnosis is educationally actionable.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    DiagnosisIsActionableSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.diagnosis.enums import DiagnosisStatus
from domain.education.diagnosis.policies.diagnosis_consistency_policy import (
    DiagnosisConsistencyPolicy,
)
from domain.education.diagnosis.specifications.diagnosis_is_supported import (
    DiagnosisIsSupportedSpecification,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.diagnosis.aggregates.educational_diagnosis import (
        EducationalDiagnosis,
    )


class DiagnosisIsActionableSpecification:
    """True when a diagnosis is structurally ready as diagnostic output.

    Actionability means the diagnosis is ACTIVE or REVISED, is supported,
    identifies educational scope, and possesses at least LOW confidence. It
    does **not** mean a teaching strategy, priority, or hypothesis has been
    selected — those remain downstream acts.
    """

    def __init__(self) -> None:
        self._supported = DiagnosisIsSupportedSpecification()

    def is_satisfied_by(self, diagnosis: EducationalDiagnosis) -> bool:
        if diagnosis.status not in {
            DiagnosisStatus.ACTIVE,
            DiagnosisStatus.REVISED,
        }:
            return False
        if not self._supported.is_satisfied_by(diagnosis):
            return False
        if not diagnosis.confidence.is_at_least(ConfidenceLevel.LOW):
            return False
        if not diagnosis.scope.statement:
            return False
        if not diagnosis.student_id:
            return False
        try:
            DiagnosisConsistencyPolicy.assert_consistent(
                diagnosis.diagnosis_type,
                diagnosis.indicators,
                diagnosis.reasons,
                diagnosis.confidence,
                diagnosis.severity,
            )
        except EducationalInvariantViolation:
            return False
        return True

    def assert_satisfied_by(self, diagnosis: EducationalDiagnosis) -> None:
        if not self.is_satisfied_by(diagnosis):
            raise EducationalInvariantViolation(
                "diagnosis is not educationally actionable",
                invariant="DiagnosisIsActionableSpecification.unsatisfied",
            )
