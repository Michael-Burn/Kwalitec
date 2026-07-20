"""Specification: EducationalDiagnosis is educationally supported.

Architecture Source
    EDUCATIONAL_DIAGNOSIS_MODEL.md
Concept
    DiagnosisIsSupportedSpecification
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from domain.education.diagnosis.enums import DiagnosisStatus
from domain.education.foundation.errors import EducationalInvariantViolation

if TYPE_CHECKING:
    from domain.education.diagnosis.aggregates.educational_diagnosis import (
        EducationalDiagnosis,
    )


class DiagnosisIsSupportedSpecification:
    """True when a diagnosis has lawful interpretive and evidential warrant.

    Support means the diagnosis references at least one Interpretation, cites
    supporting Evidence, possesses indicators and reasons, and is not
    INVALIDATED. Support does **not** mean the diagnosis is a priority,
    hypothesis, or teaching recommendation.
    """

    def is_satisfied_by(self, diagnosis: EducationalDiagnosis) -> bool:
        if diagnosis.status is DiagnosisStatus.INVALIDATED:
            return False
        if not diagnosis.indicators:
            return False
        if not diagnosis.reasons:
            return False
        if not diagnosis.supporting_interpretation_ids():
            return False
        if not diagnosis.supporting_evidence_ids():
            return False
        if diagnosis.confidence is None:
            return False
        if diagnosis.severity is None:
            return False
        if diagnosis.scope is None:
            return False
        return True

    def assert_satisfied_by(self, diagnosis: EducationalDiagnosis) -> None:
        if not self.is_satisfied_by(diagnosis):
            raise EducationalInvariantViolation(
                "diagnosis is not educationally supported",
                invariant="DiagnosisIsSupportedSpecification.unsatisfied",
            )
