"""Domain event tests for Evidence Interpretation."""

from __future__ import annotations

import pytest

from domain.education.evidence_interpretation import (
    InterpretationCreated,
    InterpretationId,
)
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from tests.domain.education.evidence_interpretation.conftest import make_interpretation


def test_created_event_from_interpret() -> None:
    interp = make_interpretation()
    events = interp.pull_events()
    event = events[0]
    assert isinstance(event, InterpretationCreated)
    assert event.interpretation_id == InterpretationId("interp-001")
    assert event.student_id == "student-ada"
    assert event.pattern_count == 1
    assert event.cluster_count == 1
    assert event.confidence_level is ConfidenceLevel.HIGH


def test_created_event_validation() -> None:
    event = InterpretationCreated(
        interpretation_id=InterpretationId("i1"),
        student_id="student-x",
        pattern_count=2,
        cluster_count=3,
        confidence_level=ConfidenceLevel.MEDIUM,
    )
    assert event.pattern_count == 2


@pytest.mark.parametrize("count", [0, -1])
def test_created_rejects_non_positive_counts(count: int) -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationCreated(
            interpretation_id=InterpretationId("i1"),
            student_id="student-x",
            pattern_count=count,
            cluster_count=1,
            confidence_level=ConfidenceLevel.MEDIUM,
        )
    with pytest.raises(EducationalInvariantViolation):
        InterpretationCreated(
            interpretation_id=InterpretationId("i1"),
            student_id="student-x",
            pattern_count=1,
            cluster_count=count,
            confidence_level=ConfidenceLevel.MEDIUM,
        )


def test_created_rejects_blank_student() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationCreated(
            interpretation_id=InterpretationId("i1"),
            student_id="",
            pattern_count=1,
            cluster_count=1,
            confidence_level=ConfidenceLevel.MEDIUM,
        )


def test_created_rejects_unknown_confidence() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationCreated(
            interpretation_id=InterpretationId("i1"),
            student_id="student-x",
            pattern_count=1,
            cluster_count=1,
            confidence_level=ConfidenceLevel.UNKNOWN,
        )


def test_created_rejects_bad_id() -> None:
    with pytest.raises(EducationalInvariantViolation):
        InterpretationCreated(
            interpretation_id="i1",  # type: ignore[arg-type]
            student_id="student-x",
            pattern_count=1,
            cluster_count=1,
            confidence_level=ConfidenceLevel.MEDIUM,
        )


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
def test_created_accepts_known_levels(level: ConfidenceLevel) -> None:
    event = InterpretationCreated(
        interpretation_id=InterpretationId(f"i-{level.value}"),
        student_id="student-x",
        pattern_count=1,
        cluster_count=1,
        confidence_level=level,
    )
    assert event.confidence_level is level


def test_event_equality() -> None:
    a = InterpretationCreated(
        interpretation_id=InterpretationId("i1"),
        student_id="student-x",
        pattern_count=1,
        cluster_count=1,
        confidence_level=ConfidenceLevel.HIGH,
    )
    b = InterpretationCreated(
        interpretation_id=InterpretationId("i1"),
        student_id="student-x",
        pattern_count=1,
        cluster_count=1,
        confidence_level=ConfidenceLevel.HIGH,
    )
    assert a == b
