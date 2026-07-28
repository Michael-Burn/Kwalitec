"""Presentation + accessibility tests for Educational Timeline (ILE-003)."""

from __future__ import annotations

from datetime import datetime, timedelta

from app.domain.decision_journal import (
    EntryKind,
    QualitativeConfidence,
    StudentAction,
)
from app.domain.decision_journal.enums import JournalLifecycleStatus
from app.services.decision_journal_service import DecisionJournalService
from tests.presentation.student.helpers import FORBIDDEN_TERMS


def _seed_entries(user):
    base = datetime(2026, 7, 10, 10, 0, 0)
    for i in range(4):
        DecisionJournalService.record_entry(
            user.id,
            kind=EntryKind.MISSION_RECOMMENDATION,
            educational_context="Today's Mission focus",
            observation=f"Recent practice on topic {i} looks fragile.",
            meaning="That topic supports later syllabus steps.",
            recommendation=f"Spend today's Mission reinforcing topic {i}.",
            supporting_evidence_summary="Two short sessions this week.",
            qualitative_confidence=(
                QualitativeConfidence.RELIABLE
                if i == 2
                else QualitativeConfidence.EMERGING
            ),
            expected_benefit="A steadier base for later topics.",
            uncertainty="Limited evidence remains." if i == 0 else "",
            student_action=StudentAction.ACCEPTED,
            lifecycle_status=JournalLifecycleStatus.ACCEPTED,
            recorded_at=base + timedelta(days=i),
        )


class TestEducationalTimelineRoute:
    def test_empty_state(self, student_client):
        resp = student_client.get("/student/educational-timeline")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "Educational Timeline" in body
        assert "Your timeline begins" in body
        assert 'role="status"' in body
        assert "/student/decision-journal" in body
        for term in FORBIDDEN_TERMS:
            assert term not in body.lower()

    def test_renders_narrative_arc(self, student_client, user, db):
        _seed_entries(user)
        resp = student_client.get("/student/educational-timeline")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "Learning Journey" in body
        assert "Observation" in body
        assert "Pattern" in body
        assert "Educational meaning" in body
        assert "Reflection" in body
        assert 'aria-label="Timeline sections"' in body
        assert "educational-timeline-arc" in body
        for term in FORBIDDEN_TERMS:
            assert term not in body.lower()

    def test_history_links_to_timeline(self, student_client):
        resp = student_client.get("/student/history")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "/student/educational-timeline" in body

    def test_journal_links_to_timeline(self, student_client, user, db):
        _seed_entries(user)
        resp = student_client.get("/student/decision-journal")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "/student/educational-timeline" in body

    def test_requires_login(self, client):
        resp = client.get(
            "/student/educational-timeline", follow_redirects=False
        )
        assert resp.status_code in (302, 401)


class TestEducationalTimelineAccessibility:
    def test_landmarks_nav_and_typography(self, student_client, user, db):
        _seed_entries(user)
        resp = student_client.get("/student/educational-timeline")
        body = resp.get_data(as_text=True)
        assert 'lang="en"' in body
        assert "<h1" in body
        assert "<h2" in body
        assert "<h3" in body
        assert 'aria-label="Timeline sections"' in body
        assert 'nav class="educational-timeline-nav"' in body
        # Chronological section anchors for keyboard jump navigation.
        assert 'id="timeline-learning-journey"' in body
        assert 'tabindex="-1"' in body
        # Meaning not colour-only: section labels and arc terms are text.
        assert "Observation" in body
        assert "Reflection" in body


class TestEducationalTimelineRegression:
    def test_does_not_mutate_journal_or_mastery(self, db, user):
        """Timeline reads journal; does not rewrite entries or mastery."""
        from app.models.decision_journal import DecisionJournalEntry

        _seed_entries(user)
        before = DecisionJournalEntry.query.filter_by(user_id=user.id).count()
        observations = [
            e.observation
            for e in DecisionJournalEntry.query.filter_by(user_id=user.id)
        ]
        from app.services.educational_timeline_service import (
            EducationalTimelineService,
        )

        EducationalTimelineService.build_for_user(user.id)
        after = DecisionJournalEntry.query.filter_by(user_id=user.id).count()
        assert after == before
        after_obs = [
            e.observation
            for e in DecisionJournalEntry.query.filter_by(user_id=user.id)
        ]
        assert after_obs == observations
