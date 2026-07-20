"""Value object tests for Evidence Interpretation domain."""

from __future__ import annotations

import pytest

from domain.education.evidence_interpretation import (
    InterpretationConfidence,
    InterpretationSummary,
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
    measure = InterpretationConfidence.of(level)
    assert measure.level is level
    assert measure.ratio is None


def test_confidence_rejects_unknown() -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        InterpretationConfidence.of(ConfidenceLevel.UNKNOWN)
    assert exc.value.invariant == "InterpretationConfidence.level.known"


@pytest.mark.parametrize("ratio", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_confidence_ratio_range(ratio: float) -> None:
    measure = InterpretationConfidence.of(ConfidenceLevel.MEDIUM, ratio=ratio)
    assert measure.ratio == ratio


@pytest.mark.parametrize("ratio", [-0.01, 1.01, 2.0])
def test_confidence_rejects_out_of_range_ratio(ratio: float) -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationConfidence.of(ConfidenceLevel.MEDIUM, ratio=ratio)


def test_confidence_rejects_bool_ratio() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationConfidence.of(ConfidenceLevel.MEDIUM, ratio=True)  # type: ignore[arg-type]


def test_confidence_is_at_least() -> None:
    high = InterpretationConfidence.of(ConfidenceLevel.HIGH)
    assert high.is_at_least(ConfidenceLevel.MEDIUM)
    assert not high.is_at_least(ConfidenceLevel.VERY_HIGH)


def test_confidence_is_at_least_rejects_unknown() -> None:
    high = InterpretationConfidence.of(ConfidenceLevel.HIGH)
    with pytest.raises(EducationalInvariantViolation):
        high.is_at_least(ConfidenceLevel.UNKNOWN)


def test_confidence_str_with_and_without_ratio() -> None:
    bare = InterpretationConfidence.of(ConfidenceLevel.LOW)
    with_ratio = InterpretationConfidence.of(ConfidenceLevel.LOW, ratio=0.4)
    assert str(bare) == "low"
    assert "0.40" in str(with_ratio)


def test_confidence_equality() -> None:
    left = InterpretationConfidence.of(ConfidenceLevel.HIGH, ratio=0.9)
    right = InterpretationConfidence.of(ConfidenceLevel.HIGH, ratio=0.9)
    assert left == right


def test_summary_requires_non_empty_text() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationSummary.of("  ", pattern_count=1, cluster_count=1)


@pytest.mark.parametrize(
    "token",
    [
        "diagnose",
        "diagnosis",
        "recommend",
        "recommendation",
        "prioritise",
        "prioritize",
        "priority",
        "mastery",
        "mastered",
        "prescribe",
        "prescription",
    ],
)
def test_summary_rejects_conclusion_language(token: str) -> None:
    with pytest.raises(EducationalInvariantViolation) as exc:
        InterpretationSummary.of(
            f"Student shows {token} of weakness",
            pattern_count=1,
            cluster_count=1,
        )
    assert exc.value.invariant == "InterpretationSummary.text.no_conclusion"


def test_summary_accepts_observational_text() -> None:
    summary = InterpretationSummary.of(
        "Observed repeated transfer failures across two probes",
        pattern_count=2,
        cluster_count=1,
    )
    assert summary.pattern_count == 2
    assert summary.cluster_count == 1
    assert str(summary).startswith("Observed")


@pytest.mark.parametrize("count", [0, -1])
def test_summary_rejects_non_positive_counts(count: int) -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationSummary.of("ok", pattern_count=count, cluster_count=1)
    with pytest.raises(EducationalInvariantViolation):
        InterpretationSummary.of("ok", pattern_count=1, cluster_count=count)


def test_summary_rejects_bool_counts() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationSummary.of("ok", pattern_count=True, cluster_count=1)  # type: ignore[arg-type]
