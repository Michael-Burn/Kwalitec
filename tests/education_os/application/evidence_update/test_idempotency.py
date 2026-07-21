"""Idempotency coverage for Educational Evidence Update (V3-007)."""

from __future__ import annotations

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


def test_repeated_updates_are_idempotent() -> None:
    uow = make_uow_with_twin()
    service = EvidenceUpdateService(uow, make_events(), make_clock())
    request = make_request(make_captured(evidence_id="evidence-idem-001"))

    results = [service.update(request) for _ in range(3)]

    assert results[0].outcome is EvidenceUpdateOutcome.APPLIED
    assert all(r.outcome is EvidenceUpdateOutcome.DUPLICATE for r in results[1:])
    assert all(r.evidence_id == "evidence-idem-001" for r in results)
    assert len(uow.evidence.list_by_student("student-ada")) == 1

    stored = load_evidence(uow, "evidence-idem-001")
    assert stored is not None
    first_items = [item.observation for item in stored.items]
    # Re-run does not mutate stored observational content.
    service.update(request)
    stored_again = load_evidence(uow, "evidence-idem-001")
    assert stored_again is not None
    assert [item.observation for item in stored_again.items] == first_items


def test_accepts_bare_captured_evidence() -> None:
    uow = make_uow_with_twin()
    service = EvidenceUpdateService(uow, make_events(), make_clock())
    captured = make_captured(evidence_id="evidence-idem-002")

    result = service.update(captured)

    assert result.applied is True
    assert result.evidence_id == "evidence-idem-002"
