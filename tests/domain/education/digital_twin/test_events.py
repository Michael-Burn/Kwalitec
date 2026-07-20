"""Domain event tests for Educational Digital Twin."""

from __future__ import annotations

import pytest

from domain.education.digital_twin import (
    MasteryBand,
    MasteryChanged,
    TwinCreated,
    TwinStatus,
    TwinUpdated,
    TwinUpdateKind,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import ConceptId, DigitalTwinId
from tests.domain.education.digital_twin.conftest import make_twin


def test_create_event_fields() -> None:
    twin = make_twin(pull_created=False)
    events = twin.pull_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, TwinCreated)
    assert event.status is TwinStatus.ACTIVE
    assert event.student_id == twin.student_id


def test_twin_created_rejects_archived_status() -> None:
    with pytest.raises(EducationalInvariantViolation):
        TwinCreated(
            twin_id=DigitalTwinId("t"),
            student_id="s",
            status=TwinStatus.ARCHIVED,
            learner_state_id="ls",
        )


@pytest.mark.parametrize("kind", list(TwinUpdateKind))
def test_twin_updated_accepts_all_kinds(kind: TwinUpdateKind) -> None:
    event = TwinUpdated(
        twin_id=DigitalTwinId("t"),
        student_id="student-x",
        status=TwinStatus.ACTIVE,
        update_kind=kind,
        evidence_count=0,
        intervention_count=0,
        trajectory_length=1,
    )
    assert event.update_kind is kind


def test_twin_updated_rejects_negative_counts() -> None:
    with pytest.raises(EducationalInvariantViolation):
        TwinUpdated(
            twin_id=DigitalTwinId("t"),
            student_id="s",
            status=TwinStatus.ACTIVE,
            update_kind=TwinUpdateKind.EVIDENCE_RECORDED,
            evidence_count=-1,
            intervention_count=0,
            trajectory_length=1,
        )


@pytest.mark.parametrize("previous", list(MasteryBand))
@pytest.mark.parametrize("new", list(MasteryBand))
def test_mastery_changed_matrix(previous: MasteryBand, new: MasteryBand) -> None:
    event = MasteryChanged(
        twin_id=DigitalTwinId("t"),
        student_id="s",
        concept_id=ConceptId("c"),
        previous_band=previous,
        new_band=new,
    )
    assert event.previous_band is previous
    assert event.new_band is new


def test_archive_emits_twin_updated() -> None:
    twin = make_twin()
    twin.archive()
    events = twin.pull_events()
    assert any(
        isinstance(e, TwinUpdated) and e.update_kind is TwinUpdateKind.ARCHIVED
        for e in events
    )
