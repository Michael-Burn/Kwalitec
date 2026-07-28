"""Service + application tests for Educational Timeline (ILE-003)."""

from __future__ import annotations

from datetime import datetime, timedelta

from app.application.educational_timeline import (
    EducationalTimelineApplicationService,
)
from app.domain.decision_journal import (
    EntryKind,
    QualitativeConfidence,
    StudentAction,
)
from app.domain.decision_journal.enums import (
    JournalLifecycleStatus,
)
from app.services.decision_journal_service import DecisionJournalService
from app.services.educational_timeline_service import EducationalTimelineService


def _seed_rich_journal(user_id: int) -> None:
    base = datetime(2026, 7, 1, 9, 0, 0)
    DecisionJournalService.record_entry(
        user_id,
        kind=EntryKind.MISSION_RECOMMENDATION,
        educational_context="Today's Mission focus",
        observation="Recent practice on Discounting looks fragile.",
        meaning="That topic supports later syllabus steps.",
        recommendation="Spend today's Mission reinforcing Discounting.",
        supporting_evidence_summary="Two short sessions this week.",
        qualitative_confidence=QualitativeConfidence.EMERGING,
        expected_benefit="A steadier base for later topics.",
        uncertainty="Limited evidence from careful checks remains.",
        student_action=StudentAction.ACCEPTED,
        recorded_at=base,
    )
    DecisionJournalService.record_entry(
        user_id,
        kind=EntryKind.RECOVERY_RECOMMENDATION,
        educational_context="Recovery focus",
        observation="Recall slipped after a busy week.",
        meaning="A short recovery block can rebuild confidence.",
        recommendation="Rebuild foundations before new material.",
        supporting_evidence_summary="One incomplete Mission.",
        qualitative_confidence=QualitativeConfidence.EMERGING,
        student_action=StudentAction.ACCEPTED,
        recorded_at=base + timedelta(days=1),
    )
    entry = DecisionJournalService.record_entry(
        user_id,
        kind=EntryKind.MISSION_RECOMMENDATION,
        educational_context="Mission completion",
        observation="Practice on Cash flows looked steadier.",
        meaning="Completing the Mission closed a useful loop.",
        recommendation="Finish today's Cash flows Mission.",
        qualitative_confidence=QualitativeConfidence.RELIABLE,
        student_action=StudentAction.ACCEPTED,
        lifecycle_status=JournalLifecycleStatus.ACCEPTED,
        recorded_at=base + timedelta(days=2),
    )
    DecisionJournalService.record_reflection(
        user_id,
        entry.entry_id,
        note="Short sessions helped more than long ones.",
    )
    DecisionJournalService.record_outcome(
        user_id,
        entry.entry_id,
        outcome_summary="Mission completed with clearer recall.",
    )
    DecisionJournalService.record_entry(
        user_id,
        kind=EntryKind.QUICK_CHECK_RECOMMENDATION,
        educational_context="Quick Check",
        observation="We still have limited recent evidence.",
        meaning="A short check would strengthen what we know.",
        recommendation="Take a Quick Check on today's focus.",
        qualitative_confidence=QualitativeConfidence.INSUFFICIENT,
        uncertainty="One check will not prove exam readiness.",
        student_action=StudentAction.ACCEPTED,
        recorded_at=base + timedelta(days=3),
    )


def test_service_builds_from_journal(db, user):
    _seed_rich_journal(user.id)
    narrative = EducationalTimelineService.build_for_user(user.id)
    assert narrative.empty is False
    assert narrative.entry_count >= 4
    assert narrative.sections
    labels = [s.label for s in narrative.sections]
    assert "Learning Journey" in labels


def test_application_snapshot(db, user):
    _seed_rich_journal(user.id)
    snap = EducationalTimelineApplicationService.timeline(user.id)
    assert snap.empty is False
    assert snap.entry_count >= 4
    assert snap.certainty_label
    assert snap.sections
    first = snap.sections[0]
    assert first.anchor_id.startswith("timeline-")
    moment = first.moments[0]
    assert moment.observation
    assert moment.pattern
    assert moment.educational_meaning
    assert moment.reflection_question
    # No engineering leakage in student projection.
    blob = " ".join(
        [
            moment.observation,
            moment.pattern,
            moment.educational_meaning,
            moment.reflection_question,
            snap.intro_line,
            snap.certainty_label,
        ]
    ).lower()
    for term in ("digital twin", "ranking algorithm", "mastery score"):
        assert term not in blob


def test_empty_timeline_when_no_journal(db, user):
    snap = EducationalTimelineApplicationService.timeline(user.id)
    assert snap.empty is True
    assert snap.entry_count == 0
    assert snap.sections == ()
