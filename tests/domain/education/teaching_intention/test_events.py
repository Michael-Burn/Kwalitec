"""Domain event tests for Teaching Intention."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import TeachingIntentionType
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import TeachingIntentionId
from domain.education.teaching_intention import (
    IntentionRevisionKind,
    IntentionStrengthLevel,
    TeachingIntentionCreated,
    TeachingIntentionRevised,
)
from tests.domain.education.teaching_intention.conftest import make_intention


def test_created_event_immutable_and_valid() -> None:
    event = TeachingIntentionCreated(
        intention_id=TeachingIntentionId("ti-evt"),
        student_id="student-ada",
        intention_type=TeachingIntentionType.REPAIR_MISCONCEPTION,
        strength_level=IntentionStrengthLevel.MODERATE,
        priority_count=1,
        diagnosis_count=1,
        hypothesis_count=0,
    )
    assert event.priority_count == 1
    assert event.hypothesis_count == 0
    with pytest.raises(AttributeError):
        event.priority_count = 2  # type: ignore[misc]


def test_created_rejects_non_positive_counts() -> None:
    with pytest.raises(EducationalInvariantViolation):
        TeachingIntentionCreated(
            intention_id=TeachingIntentionId("ti-evt"),
            student_id="student-ada",
            intention_type=TeachingIntentionType.BUILD_INTUITION,
            strength_level=IntentionStrengthLevel.TENTATIVE,
            priority_count=0,
            diagnosis_count=1,
            hypothesis_count=0,
        )
    with pytest.raises(EducationalInvariantViolation):
        TeachingIntentionCreated(
            intention_id=TeachingIntentionId("ti-evt"),
            student_id="student-ada",
            intention_type=TeachingIntentionType.BUILD_INTUITION,
            strength_level=IntentionStrengthLevel.TENTATIVE,
            priority_count=1,
            diagnosis_count=0,
            hypothesis_count=0,
        )


def test_revised_event_requires_revision_kind() -> None:
    event = TeachingIntentionRevised(
        intention_id=TeachingIntentionId("ti-evt"),
        student_id="student-ada",
        intention_type=TeachingIntentionType.IMPROVE_TRANSFER,
        strength_level=IntentionStrengthLevel.FIRM,
        revision_kind=IntentionRevisionKind.STRENGTHENED,
    )
    assert event.revision_kind is IntentionRevisionKind.STRENGTHENED
    with pytest.raises(EducationalInvariantViolation):
        TeachingIntentionRevised(
            intention_id=TeachingIntentionId("ti-evt"),
            student_id="student-ada",
            intention_type=TeachingIntentionType.IMPROVE_TRANSFER,
            strength_level=IntentionStrengthLevel.FIRM,
            revision_kind="strengthened",  # type: ignore[arg-type]
        )


def test_pull_events_clears_pending() -> None:
    intention = make_intention()
    first = intention.pull_events()
    assert len(first) == 1
    assert isinstance(first[0], TeachingIntentionCreated)
    assert intention.pull_events() == []
    intention.activate()
    second = intention.pull_events()
    assert len(second) == 1
    assert isinstance(second[0], TeachingIntentionRevised)
    intention.retire()
    third = intention.pull_events()
    assert third[0].revision_kind is IntentionRevisionKind.RETIRED


def test_created_rejects_blank_student() -> None:
    with pytest.raises(EducationalInvariantViolation):
        TeachingIntentionCreated(
            intention_id=TeachingIntentionId("ti-evt"),
            student_id="  ",
            intention_type=TeachingIntentionType.IMPROVE_RETENTION,
            strength_level=IntentionStrengthLevel.MODERATE,
            priority_count=1,
            diagnosis_count=1,
            hypothesis_count=1,
        )
