"""Value object tests for Educational Diagnosis confidence and severity."""

from __future__ import annotations

import pytest

from domain.education.diagnosis import (
    DiagnosisConfidence,
    DiagnosisSeverity,
    DiagnosisSeverityLevel,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation


@pytest.mark.parametrize(
    "level",
    [
        ConfidenceLevel.VERY_LOW,
        ConfidenceLevel.LOW,
        ConfidenceLevel.MEDIUM,
        ConfidenceLevel.HIGH,
        ConfidenceLevel.VERY_HIGH,
    ],
)
def test_confidence_accepts_known_levels(level: ConfidenceLevel) -> None:
    measure = DiagnosisConfidence.of(level, ratio=0.5)
    assert measure.level is level
    assert measure.ratio == 0.5


def test_confidence_rejects_unknown() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisConfidence.of(ConfidenceLevel.UNKNOWN)


@pytest.mark.parametrize("ratio", [-0.01, 1.01, True, "high"])
def test_confidence_rejects_invalid_ratio(ratio: object) -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisConfidence.of(ConfidenceLevel.MEDIUM, ratio=ratio)  # type: ignore[arg-type]


@pytest.mark.parametrize("ratio", [0.0, 0.5, 1.0, None])
def test_confidence_accepts_valid_ratio(ratio: float | None) -> None:
    measure = DiagnosisConfidence.of(ConfidenceLevel.LOW, ratio=ratio)
    assert measure.ratio == ratio


def test_confidence_is_at_least() -> None:
    high = DiagnosisConfidence.of(ConfidenceLevel.HIGH)
    assert high.is_at_least(ConfidenceLevel.MEDIUM)
    assert high.is_at_least(ConfidenceLevel.HIGH)
    assert not high.is_at_least(ConfidenceLevel.VERY_HIGH)


def test_confidence_is_at_least_rejects_unknown() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisConfidence.of(ConfidenceLevel.MEDIUM).is_at_least(
            ConfidenceLevel.UNKNOWN
        )


def test_confidence_str() -> None:
    assert str(DiagnosisConfidence.of(ConfidenceLevel.HIGH)) == "high"
    assert "0.75" in str(DiagnosisConfidence.of(ConfidenceLevel.HIGH, ratio=0.75))


def test_confidence_equality() -> None:
    a = DiagnosisConfidence.of(ConfidenceLevel.MEDIUM, ratio=0.4)
    b = DiagnosisConfidence.of(ConfidenceLevel.MEDIUM, ratio=0.4)
    assert a == b


@pytest.mark.parametrize("level", list(DiagnosisSeverityLevel))
def test_severity_accepts_all_levels(level: DiagnosisSeverityLevel) -> None:
    severity = DiagnosisSeverity.of(level, rationale="within scope")
    assert severity.level is level


def test_severity_rejects_blank_rationale() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisSeverity.of(DiagnosisSeverityLevel.MILD, rationale="   ")


def test_severity_is_at_least() -> None:
    severe = DiagnosisSeverity.of(DiagnosisSeverityLevel.SEVERE)
    assert severe.is_at_least(DiagnosisSeverityLevel.MODERATE)
    assert not DiagnosisSeverity.of(DiagnosisSeverityLevel.MILD).is_at_least(
        DiagnosisSeverityLevel.SEVERE
    )


def test_severity_str() -> None:
    assert str(DiagnosisSeverity.of(DiagnosisSeverityLevel.MILD)) == "mild"
    text = str(
        DiagnosisSeverity.of(
            DiagnosisSeverityLevel.SUBSTANTIAL, rationale="blocks progress"
        )
    )
    assert "substantial" in text
    assert "blocks progress" in text


def test_severity_equality() -> None:
    a = DiagnosisSeverity.of(DiagnosisSeverityLevel.MODERATE)
    b = DiagnosisSeverity.of(DiagnosisSeverityLevel.MODERATE)
    assert a == b


def test_confidence_rejects_non_confidence_level() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisConfidence(level="high")  # type: ignore[arg-type]


def test_severity_rejects_non_severity_level() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DiagnosisSeverity(level="severe")  # type: ignore[arg-type]
