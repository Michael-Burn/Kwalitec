"""Value-object tests for Educational Decision."""

from __future__ import annotations

import pytest

from domain.education.decision import DecisionConfidence, ReadinessBand, ReadinessLevel
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
def test_decision_confidence_levels(level: ConfidenceLevel) -> None:
    confidence = DecisionConfidence.of(level, ratio=0.5)
    assert confidence.level is level
    assert confidence.is_at_least(ConfidenceLevel.VERY_LOW)


def test_decision_confidence_rejects_unknown() -> None:
    with pytest.raises(EducationalInvariantViolation):
        DecisionConfidence.of(ConfidenceLevel.UNKNOWN)


@pytest.mark.parametrize("ratio", [-0.1, 1.1, True])
def test_decision_confidence_rejects_bad_ratio(ratio: object) -> None:
    with pytest.raises(EducationalInvariantViolation):
        DecisionConfidence.of(ConfidenceLevel.HIGH, ratio=ratio)  # type: ignore[arg-type]


@pytest.mark.parametrize("band", list(ReadinessBand))
def test_readiness_level_bands(band: ReadinessBand) -> None:
    readiness = ReadinessLevel.of(band, ratio=0.4, rationale="posture")
    assert readiness.band is band
    assert readiness.is_ready() is (band is ReadinessBand.READY)
    assert readiness.is_blocked() is (band is ReadinessBand.BLOCKED)
    assert readiness.permits_approval() is (band is ReadinessBand.READY)


def test_readiness_is_at_least() -> None:
    ready = ReadinessLevel.of(ReadinessBand.READY)
    assert ready.is_at_least(ReadinessBand.PARTIALLY_READY)
    assert not ReadinessLevel.of(ReadinessBand.NOT_READY).is_at_least(
        ReadinessBand.READY
    )


def test_readiness_rejects_blank_rationale() -> None:
    with pytest.raises(EducationalInvariantViolation):
        ReadinessLevel.of(ReadinessBand.READY, rationale="   ")


def test_confidence_str_and_readiness_str() -> None:
    assert "high" in str(DecisionConfidence.of(ConfidenceLevel.HIGH, ratio=0.75))
    assert "ready" in str(ReadinessLevel.of(ReadinessBand.READY, ratio=0.9))
