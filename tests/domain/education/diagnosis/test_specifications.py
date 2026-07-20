"""Specification tests for supported and actionable diagnoses."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisIsActionableSpecification,
    DiagnosisIsSupportedSpecification,
    DiagnosisSeverityLevel,
)
from domain.education.foundation.enums import ConfidenceLevel, DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.diagnosis.conftest import (
    make_confidence,
    make_diagnosis,
    make_severity,
)


def test_supported_for_active_diagnosis() -> None:
    diagnosis = make_diagnosis()
    assert DiagnosisIsSupportedSpecification().is_satisfied_by(diagnosis)


def test_supported_false_when_invalidated() -> None:
    diagnosis = make_diagnosis()
    diagnosis.invalidate("superseded")
    assert not DiagnosisIsSupportedSpecification().is_satisfied_by(diagnosis)


def test_actionable_for_active_diagnosis() -> None:
    diagnosis = make_diagnosis()
    assert DiagnosisIsActionableSpecification().is_satisfied_by(diagnosis)


def test_actionable_false_for_very_low_confidence() -> None:
    diagnosis = make_diagnosis(
        confidence=make_confidence(ConfidenceLevel.VERY_LOW),
        severity=make_severity(DiagnosisSeverityLevel.MILD),
    )
    assert DiagnosisIsSupportedSpecification().is_satisfied_by(diagnosis)
    assert not DiagnosisIsActionableSpecification().is_satisfied_by(diagnosis)


def test_actionable_true_after_revise() -> None:
    diagnosis = make_diagnosis()
    diagnosis.revise(confidence=make_confidence(ConfidenceLevel.MEDIUM))
    assert DiagnosisIsActionableSpecification().is_satisfied_by(diagnosis)


def test_actionable_false_when_invalidated() -> None:
    diagnosis = make_diagnosis()
    diagnosis.invalidate("void")
    assert not DiagnosisIsActionableSpecification().is_satisfied_by(diagnosis)


def test_assert_supported_raises() -> None:
    diagnosis = make_diagnosis()
    diagnosis.invalidate("void")
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisIsSupportedSpecification().assert_satisfied_by(diagnosis)


def test_assert_actionable_raises() -> None:
    diagnosis = make_diagnosis(
        confidence=make_confidence(ConfidenceLevel.VERY_LOW),
    )
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisIsActionableSpecification().assert_satisfied_by(diagnosis)


@pytest.mark.parametrize("diagnosis_type", list(DiagnosisType))
def test_actionable_across_catalogue(diagnosis_type: DiagnosisType) -> None:
    diagnosis = make_diagnosis(
        diagnosis_id=f"diag-act-{diagnosis_type.value}",
        diagnosis_type=diagnosis_type,
    )
    assert DiagnosisIsActionableSpecification().is_satisfied_by(diagnosis)
    assert DiagnosisIsSupportedSpecification().is_satisfied_by(diagnosis)
