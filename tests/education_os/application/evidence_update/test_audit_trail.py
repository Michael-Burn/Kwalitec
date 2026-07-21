"""Audit trail coverage for Educational Evidence Update (V3-007)."""

from __future__ import annotations

from application.events.evidence import EvidenceRecordedApplicationEvent
from application.evidence_update import (
    EvidenceUpdateOutcome,
    EvidenceUpdateService,
)
from tests.education_os.application.evidence_update import (
    make_captured,
    make_request,
    make_uow_with_twin,
)
from tests.education_os.application.helpers import make_clock, make_events


def test_applied_update_produces_audit_trail() -> None:
    uow = make_uow_with_twin()
    events = make_events()
    service = EvidenceUpdateService(uow, events, make_clock())

    result = service.update(
        make_request(make_captured(evidence_id="evidence-audit-001"))
    )

    assert result.outcome is EvidenceUpdateOutcome.APPLIED
    kinds = [entry.kind for entry in result.audit_trail]
    assert "EvidenceRecorded" in kinds
    assert "evidence_stored" in kinds
    assert "twin_evidence_recorded" in kinds
    assert "EvidenceRecordedApplicationEvent" in kinds
    assert all(
        entry.evidence_id == "evidence-audit-001" for entry in result.audit_trail
    )
    assert len(events.of_type(EvidenceRecordedApplicationEvent)) == 1


def test_duplicate_update_records_duplicate_audit_entry() -> None:
    uow = make_uow_with_twin()
    service = EvidenceUpdateService(uow, make_events(), make_clock())
    request = make_request(make_captured(evidence_id="evidence-audit-002"))

    service.update(request)
    duplicate = service.update(request)

    kinds = [entry.kind for entry in duplicate.audit_trail]
    assert kinds == ["duplicate_skipped"]
    assert duplicate.audit_trail[0].detail.startswith("evidence_id already present")


def test_update_without_twin_skips_twin_with_audit() -> None:
    from tests.education_os.application.helpers import make_uow

    uow = make_uow()
    service = EvidenceUpdateService(uow, make_events(), make_clock())

    result = service.update(
        make_request(make_captured(evidence_id="evidence-audit-003"))
    )

    assert result.applied is True
    assert result.twin_updated is False
    kinds = [entry.kind for entry in result.audit_trail]
    assert "twin_skipped" in kinds
    assert "twin_evidence_recorded" not in kinds
