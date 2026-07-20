"""Domain event tests for Educational Diagnosis."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisCreated,
    DiagnosisInvalidated,
    DiagnosisSeverityLevel,
)
from domain.education.foundation.enums import ConfidenceLevel, DiagnosisType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import DiagnosisId
from tests.domain.education.diagnosis.conftest import make_diagnosis


def test_create_emits_diagnosis_created() -> None:
    diagnosis = make_diagnosis()
    events = diagnosis.pull_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, DiagnosisCreated)
    assert event.diagnosis_id == diagnosis.diagnosis_id
    assert event.student_id == diagnosis.student_id
    assert event.diagnosis_type is diagnosis.diagnosis_type
    assert event.indicator_count == 1
    assert event.reason_count == 1
    assert diagnosis.pull_events() == []


def test_invalidate_emits_diagnosis_invalidated() -> None:
    diagnosis = make_diagnosis()
    diagnosis.pull_events()
    diagnosis.invalidate("new evidence relocates deficit")
    events = diagnosis.pull_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, DiagnosisInvalidated)
    assert event.reason == "new evidence relocates deficit"
    assert event.diagnosis_type is diagnosis.diagnosis_type


def test_diagnosis_created_immutable() -> None:
    event = DiagnosisCreated(
        diagnosis_id=DiagnosisId("diag-evt"),
        student_id="student-ada",
        diagnosis_type=DiagnosisType.MISCONCEPTION,
        confidence_level=ConfidenceLevel.HIGH,
        severity_level=DiagnosisSeverityLevel.SEVERE,
        indicator_count=2,
        reason_count=1,
    )
    with pytest.raises(AttributeError):
        event.student_id = "other"  # type: ignore[misc]


def test_diagnosis_invalidated_immutable() -> None:
    event = DiagnosisInvalidated(
        diagnosis_id=DiagnosisId("diag-evt"),
        student_id="student-ada",
        diagnosis_type=DiagnosisType.WEAK_RETENTION,
        reason="delayed probe contradicts prior label",
    )
    with pytest.raises(AttributeError):
        event.reason = "changed"  # type: ignore[misc]


def test_created_rejects_unknown_confidence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisCreated(
            diagnosis_id=DiagnosisId("diag-evt"),
            student_id="student-ada",
            diagnosis_type=DiagnosisType.TRANSFER_WEAKNESS,
            confidence_level=ConfidenceLevel.UNKNOWN,
            severity_level=DiagnosisSeverityLevel.MODERATE,
            indicator_count=1,
            reason_count=1,
        )


@pytest.mark.parametrize("count", [0, -1])
def test_created_rejects_non_positive_counts(count: int) -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisCreated(
            diagnosis_id=DiagnosisId("diag-evt"),
            student_id="student-ada",
            diagnosis_type=DiagnosisType.PROCEDURAL_WEAKNESS,
            confidence_level=ConfidenceLevel.MEDIUM,
            severity_level=DiagnosisSeverityLevel.MILD,
            indicator_count=count,
            reason_count=1,
        )
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisCreated(
            diagnosis_id=DiagnosisId("diag-evt"),
            student_id="student-ada",
            diagnosis_type=DiagnosisType.PROCEDURAL_WEAKNESS,
            confidence_level=ConfidenceLevel.MEDIUM,
            severity_level=DiagnosisSeverityLevel.MILD,
            indicator_count=1,
            reason_count=count,
        )


def test_invalidated_rejects_blank_reason() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisInvalidated(
            diagnosis_id=DiagnosisId("diag-evt"),
            student_id="student-ada",
            diagnosis_type=DiagnosisType.APPLICATION_WEAKNESS,
            reason="  ",
        )


@pytest.mark.parametrize("diagnosis_type", list(DiagnosisType))
def test_created_accepts_all_diagnosis_types(diagnosis_type: DiagnosisType) -> None:
    event = DiagnosisCreated(
        diagnosis_id=DiagnosisId(f"diag-{diagnosis_type.value}"),
        student_id="student-ada",
        diagnosis_type=diagnosis_type,
        confidence_level=ConfidenceLevel.MEDIUM,
        severity_level=DiagnosisSeverityLevel.MODERATE,
        indicator_count=1,
        reason_count=1,
    )
    assert event.diagnosis_type is diagnosis_type
