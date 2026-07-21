"""Repository failure coverage for Educational Evidence Update (V3-007)."""

from __future__ import annotations

import pytest

from application.events.evidence import EvidenceRecordedApplicationEvent
from application.evidence_update import EvidenceUpdateService
from tests.education_os.application.evidence_update import (
    FailingEvidenceRepository,
    make_captured,
    make_request,
    make_uow_with_failing_evidence,
)
from tests.education_os.application.helpers import make_clock, make_events, make_twin


def test_repository_failure_rolls_back_and_raises() -> None:
    uow = make_uow_with_failing_evidence()
    make_twin(uow)
    events = make_events()
    service = EvidenceUpdateService(uow, events, make_clock())
    request = make_request(make_captured(evidence_id="evidence-fail-001"))

    with pytest.raises(RuntimeError, match="repository save failed"):
        service.update(request)

    assert uow.commit_count == 0
    assert uow.rollback_count >= 1
    failing = uow.evidence
    assert isinstance(failing, FailingEvidenceRepository)
    assert failing.save_attempts == 1
    assert failing.list_by_student("student-ada") == []
    assert len(events.of_type(EvidenceRecordedApplicationEvent)) == 0

    twin = uow.digital_twins.get_by_student("student-ada")
    assert twin is not None
    assert twin.evidence_history == ()
