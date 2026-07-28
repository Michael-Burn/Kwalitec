"""Presentation + accessibility tests for Decision Journal (ILE-002)."""

from __future__ import annotations

from app.domain.decision_journal import (
    EntryKind,
    QualitativeConfidence,
)
from app.services.decision_journal_service import DecisionJournalService
from tests.presentation.student.helpers import FORBIDDEN_TERMS


def _seed_entry(user):
    return DecisionJournalService.record_entry(
        user.id,
        kind=EntryKind.MISSION_RECOMMENDATION,
        educational_context="Today's Mission focus",
        observation="Recent practice on Discounting looks fragile.",
        meaning="That topic supports later syllabus steps.",
        recommendation="Spend today's Mission reinforcing Discounting.",
        supporting_evidence_summary="Two short sessions this week.",
        qualitative_confidence=QualitativeConfidence.EMERGING,
        expected_benefit="A steadier base for later topics.",
        uncertainty="Limited evidence from careful checks remains.",
        catalogue_decision_id="D-L01",
    )


class TestDecisionJournalRoute:
    def test_timeline_empty_state(self, student_client):
        resp = student_client.get("/student/decision-journal")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "Decision Journal" in body
        assert "Your journal starts" in body
        assert 'role="status"' in body
        for term in FORBIDDEN_TERMS:
            assert term not in body.lower()

    def test_timeline_renders_entry_questions(self, student_client, user, db):
        _seed_entry(user)
        resp = student_client.get("/student/decision-journal")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "What happened?" in body
        assert "Why?" in body
        assert "What did I choose?" in body
        assert "Discounting" in body
        assert 'aria-label="Decision Journal timeline"' in body
        assert "decision-journal-arc" in body
        for term in FORBIDDEN_TERMS:
            assert term not in body.lower()

    def test_history_links_to_journal(self, student_client):
        resp = student_client.get("/student/history")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "/student/decision-journal" in body

    def test_requires_login(self, client):
        resp = client.get("/student/decision-journal", follow_redirects=False)
        assert resp.status_code in (302, 401)


class TestDecisionJournalAccessibility:
    def test_landmarks_and_keyboard_details(self, student_client, user, db):
        _seed_entry(user)
        resp = student_client.get("/student/decision-journal")
        body = resp.get_data(as_text=True)
        assert 'lang="en"' in body
        assert "<h1" in body
        assert "<h2" in body
        assert "<details" in body
        assert "<summary" in body
        # Meaning not colour-only: lifecycle / confidence are text-labelled.
        assert "Recommended" in body or "Emerging confidence" in body


class TestDecisionJournalRegression:
    def test_commitment_mirror_writes_journal(self, db, user):
        """EP-008.3 adapter mirrors preference decisions into ILE-002 journal."""
        from app.infrastructure.adapters.student_experience import (
            commitment_persistence as commit_persist,
        )
        from app.models.decision_journal import DecisionJournalEntry

        adapter = commit_persist.RecommendationServiceDecisionJournalAdapter()
        tip = {
            "title": "Reinforce Discounting",
            "category": "Study",
            "priority": "Medium",
            "reason": "Recent practice looks fragile.",
            "expected_benefit": "Steadier foundation.",
            "generated_at": "2026-07-28T10:00:00",
            "summary": "Two short sessions.",
            "suggested_next_action": "Focus today's Mission on Discounting.",
        }
        decision_id = adapter.record_decision(
            user.id, tip, accepted=True, completed=False
        )
        assert decision_id is not None
        rows = DecisionJournalEntry.query.filter_by(user_id=user.id).all()
        assert len(rows) >= 1
        assert rows[0].legacy_decision_id == decision_id
        assert "Discounting" in rows[0].recommendation
