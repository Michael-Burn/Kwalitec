"""Domain event tests for Educational Priority."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import PriorityId
from domain.education.priority import (
    InstructionalImpactLevel,
    PriorityAssigned,
    PriorityRevised,
    PriorityRevisionKind,
    PriorityScoreBand,
    UrgencyLevel,
)


def test_priority_assigned_immutable() -> None:
    event = PriorityAssigned(
        priority_id=PriorityId("prio-1"),
        student_id="student-ada",
        score_band=PriorityScoreBand.HIGH,
        urgency_level=UrgencyLevel.ELEVATED,
        impact_level=InstructionalImpactLevel.SUBSTANTIAL,
        factor_count=2,
        diagnosis_count=1,
        hypothesis_count=1,
    )
    with pytest.raises(AttributeError):
        event.student_id = "mutated"  # type: ignore[misc]


def test_priority_assigned_rejects_non_positive_counts() -> None:
    with pytest.raises(EducationalInvariantViolation):
        PriorityAssigned(
            priority_id=PriorityId("prio-1"),
            student_id="student-ada",
            score_band=PriorityScoreBand.HIGH,
            urgency_level=UrgencyLevel.ELEVATED,
            impact_level=InstructionalImpactLevel.SUBSTANTIAL,
            factor_count=0,
            diagnosis_count=1,
            hypothesis_count=1,
        )


@pytest.mark.parametrize("kind", list(PriorityRevisionKind))
def test_priority_revised_accepts_all_kinds(kind: PriorityRevisionKind) -> None:
    event = PriorityRevised(
        priority_id=PriorityId("prio-1"),
        student_id="student-ada",
        score_band=PriorityScoreBand.MEDIUM,
        urgency_level=UrgencyLevel.ROUTINE,
        impact_level=InstructionalImpactLevel.MATERIAL,
        revision_kind=kind,
    )
    assert event.revision_kind is kind


def test_priority_revised_immutable() -> None:
    event = PriorityRevised(
        priority_id=PriorityId("prio-1"),
        student_id="student-ada",
        score_band=PriorityScoreBand.MEDIUM,
        urgency_level=UrgencyLevel.ROUTINE,
        impact_level=InstructionalImpactLevel.MATERIAL,
        revision_kind=PriorityRevisionKind.PROMOTED,
    )
    with pytest.raises(AttributeError):
        event.revision_kind = PriorityRevisionKind.DEMOTED  # type: ignore[misc]


def test_priority_assigned_strips_student_id() -> None:
    event = PriorityAssigned(
        priority_id=PriorityId("prio-1"),
        student_id="  student-ada  ",
        score_band=PriorityScoreBand.HIGH,
        urgency_level=UrgencyLevel.ELEVATED,
        impact_level=InstructionalImpactLevel.SUBSTANTIAL,
        factor_count=1,
        diagnosis_count=1,
        hypothesis_count=1,
    )
    assert event.student_id == "student-ada"
