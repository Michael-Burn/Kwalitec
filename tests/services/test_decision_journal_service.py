"""Unit + integration tests for DecisionJournalService (ILE-002)."""

from __future__ import annotations

import pytest

from app.domain.decision_journal import (
    EntryKind,
    JournalLifecycleStatus,
    QualitativeConfidence,
    StudentAction,
)
from app.services.decision_journal_service import (
    DecisionJournalNotFoundError,
    DecisionJournalService,
    DecisionJournalTransitionError,
)


def _record(user, **overrides):
    payload = {
        "kind": EntryKind.MISSION_RECOMMENDATION,
        "educational_context": "Today's Mission focus",
        "observation": "Recent practice on Discounting looks fragile.",
        "meaning": "That topic supports later syllabus steps.",
        "recommendation": "Spend today's Mission reinforcing Discounting.",
        "supporting_evidence_summary": "Two short sessions this week.",
        "qualitative_confidence": QualitativeConfidence.EMERGING,
        "expected_benefit": "A steadier base for later topics.",
        "uncertainty": "We still have limited evidence from careful checks.",
        "catalogue_decision_id": "D-L01",
    }
    payload.update(overrides)
    return DecisionJournalService.record_entry(user.id, **payload)


class TestRecordAndTimeline:
    def test_record_entry_and_timeline(self, db, user):
        entry = _record(user)
        assert entry.entry_id.startswith("dj_")
        assert entry.lifecycle_status == JournalLifecycleStatus.RECOMMENDED.value

        timeline = DecisionJournalService.get_timeline(user.id)
        assert len(timeline) == 1
        assert timeline[0].entry_id == entry.entry_id

        student = DecisionJournalService.to_student_dict(entry)
        assert student["decision_id"] == entry.entry_id
        assert "what_happened" in student
        assert "digital twin" not in str(student).lower()

    def test_rejects_unsafe_observation(self, db, user):
        with pytest.raises(ValueError, match="digital twin"):
            _record(user, observation="The digital twin says practise more.")

    def test_ownership_isolation(self, db, user):
        from app.models.user import User

        other = User(email="other-dj@kwalitec.example", is_active_user=True)
        other.set_password("password123")
        other.alpha_onboarding_completed = True
        db.session.add(other)
        db.session.commit()

        entry = _record(user)
        with pytest.raises(DecisionJournalNotFoundError):
            DecisionJournalService.get_entry(other.id, entry.entry_id)


class TestLifecycle:
    def test_accept_defer_evidence_reflect_outcome_archive(self, db, user):
        entry = _record(user)
        entry = DecisionJournalService.accept_entry(user.id, entry.entry_id)
        assert entry.student_action == StudentAction.ACCEPTED.value
        assert entry.lifecycle_status == JournalLifecycleStatus.ACCEPTED.value

        DecisionJournalService.append_evidence(
            user.id,
            entry.entry_id,
            summary="A careful check after practice added clarity.",
        )
        entry = DecisionJournalService.get_entry(user.id, entry.entry_id)
        assert (
            entry.lifecycle_status
            == JournalLifecycleStatus.EVIDENCE_EVOLVING.value
        )
        assert len(list(entry.evidence_events)) == 1

        # Original recommendation must remain unchanged.
        assert "reinforcing Discounting" in entry.recommendation

        entry = DecisionJournalService.record_reflection(
            user.id,
            entry.entry_id,
            note="Short focused practice helped more than rushing ahead.",
        )
        assert entry.lifecycle_status == JournalLifecycleStatus.REFLECTED.value

        entry = DecisionJournalService.record_outcome(
            user.id,
            entry.entry_id,
            outcome_summary="You completed the Mission on Discounting.",
        )
        assert (
            entry.lifecycle_status
            == JournalLifecycleStatus.OUTCOME_RECORDED.value
        )

        entry = DecisionJournalService.archive_entry(user.id, entry.entry_id)
        assert entry.lifecycle_status == JournalLifecycleStatus.ARCHIVED.value
        assert entry.archived_at is not None

        # Archived entries remain readable.
        timeline = DecisionJournalService.get_timeline(user.id)
        assert any(e.entry_id == entry.entry_id for e in timeline)

    def test_cannot_append_evidence_when_archived(self, db, user):
        entry = _record(user)
        DecisionJournalService.accept_entry(user.id, entry.entry_id)
        DecisionJournalService.record_reflection(user.id, entry.entry_id)
        DecisionJournalService.record_outcome(
            user.id, entry.entry_id, outcome_summary="Completed."
        )
        DecisionJournalService.archive_entry(user.id, entry.entry_id)
        with pytest.raises(DecisionJournalTransitionError):
            DecisionJournalService.append_evidence(
                user.id, entry.entry_id, summary="Too late."
            )

    def test_history_never_rewritten_on_evidence(self, db, user):
        entry = _record(
            user,
            recommendation="Original recommendation text.",
            observation="Original observation.",
        )
        original_rec = entry.recommendation
        original_obs = entry.observation
        DecisionJournalService.append_evidence(
            user.id,
            entry.entry_id,
            summary="New evidence arrived.",
            move_status=True,
        )
        entry = DecisionJournalService.get_entry(user.id, entry.entry_id)
        assert entry.recommendation == original_rec
        assert entry.observation == original_obs


class TestRecommendationMirror:
    def test_record_from_recommendation(self, db, user):
        tip = {
            "title": "Reinforce Discounting",
            "category": "Study",
            "reason": "Recent practice looks fragile.",
            "expected_benefit": "Steadier foundation.",
            "summary": "Two short sessions this week.",
            "suggested_next_action": "Focus today's Mission on Discounting.",
        }
        entry = DecisionJournalService.record_from_recommendation(
            user.id,
            tip,
            accepted=True,
            completed=False,
            kind=EntryKind.MISSION_RECOMMENDATION,
        )
        assert entry.student_action == StudentAction.ACCEPTED.value
        assert "Discounting" in entry.recommendation
