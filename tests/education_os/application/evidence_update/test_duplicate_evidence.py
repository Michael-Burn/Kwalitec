"""Duplicate evidence coverage for Educational Evidence Update (V3-007)."""

from __future__ import annotations

from application.events.evidence import EvidenceRecordedApplicationEvent
from application.evidence_update import (
    EvidenceUpdateOutcome,
    EvidenceUpdateService,
)
from tests.education_os.application.evidence_update import (
    load_evidence,
    make_captured,
    make_request,
    make_uow_with_twin,
)
from tests.education_os.application.helpers import make_clock, make_events


def test_duplicate_evidence_id_returns_duplicate_outcome() -> None:
    uow = make_uow_with_twin()
    events = make_events()
    service = EvidenceUpdateService(uow, events, make_clock())
    request = make_request(make_captured(evidence_id="evidence-dup-001"))

    first = service.update(request)
    second = service.update(request)

    assert first.outcome is EvidenceUpdateOutcome.APPLIED
    assert second.outcome is EvidenceUpdateOutcome.DUPLICATE
    assert second.duplicate is True
    assert second.applied is False
    assert second.twin_updated is False
    assert len(events.of_type(EvidenceRecordedApplicationEvent)) == 1

    stored = load_evidence(uow, "evidence-dup-001")
    assert stored is not None
    assert len(uow.evidence.list_by_student("student-ada")) == 1


def test_duplicate_does_not_reappend_twin_history() -> None:
    uow = make_uow_with_twin()
    service = EvidenceUpdateService(uow, make_events(), make_clock())
    request = make_request(make_captured(evidence_id="evidence-dup-002"))

    first = service.update(request)
    twin = uow.digital_twins.get_by_student("student-ada")
    assert twin is not None
    history_len = len(twin.evidence_history)

    second = service.update(request)

    assert first.twin_updated is True
    assert second.outcome is EvidenceUpdateOutcome.DUPLICATE
    twin_after = uow.digital_twins.get_by_student("student-ada")
    assert twin_after is not None
    assert len(twin_after.evidence_history) == history_len
