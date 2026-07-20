"""Domain event tests for Evidence domain."""

from __future__ import annotations

import pytest

from domain.education.evidence import (
    EvidenceRecorded,
    EvidenceRecordStatus,
    EvidenceStrengthLevel,
    EvidenceUpdated,
)
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import EvidenceId
from tests.domain.education.evidence.conftest import make_record, make_timestamp


class TestEvidenceRecorded:
    def test_emitted_on_record(self) -> None:
        record = make_record()
        events = record.pull_events()
        assert len(events) == 1
        event = events[0]
        assert isinstance(event, EvidenceRecorded)
        assert event.evidence_id == EvidenceId("evidence-001")
        assert event.student_id == "student-ada"
        assert event.item_count == 1
        assert event.strength_level is EvidenceStrengthLevel.STRONG

    def test_immutable(self) -> None:
        record = make_record()
        event = record.pull_events()[0]
        assert isinstance(event, EvidenceRecorded)
        with pytest.raises(Exception):
            event.item_count = 99  # type: ignore[misc]

    def test_pull_clears(self) -> None:
        record = make_record()
        assert record.pull_events()
        assert record.pull_events() == []

    def test_construction_validation(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceRecorded(
                evidence_id=EvidenceId("e1"),
                student_id="",
                item_count=1,
                strength_level=EvidenceStrengthLevel.WEAK,
                recorded_at=make_timestamp(),
            )

    def test_item_count_positive(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceRecorded(
                evidence_id=EvidenceId("e1"),
                student_id="s1",
                item_count=0,
                strength_level=EvidenceStrengthLevel.WEAK,
                recorded_at=make_timestamp(),
            )


class TestEvidenceUpdated:
    @pytest.mark.parametrize(
        "action",
        ["amend", "invalidate", "attach_context", "add_item"],
    )
    def test_emitted_on_mutations(self, action: str) -> None:
        record = make_record()
        record.pull_events()
        if action == "amend":
            record.amend(confidence=record.confidence)
        elif action == "invalidate":
            record.invalidate("attribution error")
        elif action == "attach_context":
            record.attach_context(record.context)
        elif action == "add_item":
            from tests.domain.education.evidence.conftest import make_item

            record.add_item(
                make_item(
                    item_id="item-extra",
                    observation="Additional retrieval outcome",
                )
            )
        events = record.pull_events()
        assert len(events) == 1
        assert isinstance(events[0], EvidenceUpdated)
        assert events[0].change_kind == action

    def test_merge_emits_on_both(self) -> None:
        primary = make_record(evidence_id="ev-a")
        other = make_record(
            evidence_id="ev-b",
            items=[
                __import__(
                    "tests.domain.education.evidence.conftest", fromlist=["make_item"]
                ).make_item(
                    item_id="item-b",
                    observation="Distinct observational outcome",
                )
            ],
        )
        primary.pull_events()
        other.pull_events()
        primary.merge(other)
        assert any(
            isinstance(e, EvidenceUpdated) and e.change_kind == "merge"
            for e in primary.pull_events()
        )
        assert any(
            isinstance(e, EvidenceUpdated) and e.change_kind == "merged_away"
            for e in other.pull_events()
        )
        assert other.status is EvidenceRecordStatus.MERGED

    def test_blank_change_kind_rejected(self) -> None:
        with pytest.raises(EducationalInvariantViolation):
            EvidenceUpdated(
                evidence_id=EvidenceId("e1"),
                student_id="s1",
                status=EvidenceRecordStatus.ACTIVE,
                change_kind="  ",
            )

    def test_immutable(self) -> None:
        event = EvidenceUpdated(
            evidence_id=EvidenceId("e1"),
            student_id="s1",
            status=EvidenceRecordStatus.AMENDED,
            change_kind="amend",
        )
        with pytest.raises(Exception):
            event.change_kind = "other"  # type: ignore[misc]
