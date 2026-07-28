"""Application-layer tests for Decision Journal timeline (ILE-002)."""

from __future__ import annotations

from app.application.decision_journal import DecisionJournalApplicationService
from app.domain.decision_journal import EntryKind, QualitativeConfidence
from app.services.decision_journal_service import DecisionJournalService


def test_timeline_snapshot(db, user):
    DecisionJournalService.record_entry(
        user.id,
        kind=EntryKind.QUICK_CHECK_RECOMMENDATION,
        educational_context="Quick Check invitation",
        observation="We have limited recent evidence on this topic.",
        meaning="A short check would strengthen what we know.",
        recommendation="Take a Quick Check on today's focus.",
        supporting_evidence_summary="One brief Mission session.",
        qualitative_confidence=QualitativeConfidence.EMERGING,
        expected_benefit="Clearer next-step guidance.",
        uncertainty="One check will not prove exam readiness.",
    )
    snap = DecisionJournalApplicationService.timeline(user.id)
    assert snap.empty is False
    assert snap.entry_count == 1
    entry = snap.entries[0]
    assert entry.kind_label == "Quick Check recommendation"
    assert "What" not in entry.decision_id  # public id is opaque
    assert entry.what_happened
    assert entry.confidence_label
