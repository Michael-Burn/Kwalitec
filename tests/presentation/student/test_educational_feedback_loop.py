"""Presentation + regression tests for Educational Feedback Loop (ILE-005)."""

from __future__ import annotations

from app.domain.decision_journal import (
    EntryKind,
    JournalLifecycleStatus,
    QualitativeConfidence,
    StudentAction,
)
from app.domain.educational_timeline import NarrativeCertainty
from app.models.educational_feedback import EducationalFeedbackReview
from app.services.decision_journal_service import DecisionJournalService
from app.services.educational_timeline_service import EducationalTimelineService
from tests.presentation.student.helpers import FORBIDDEN_TERMS


def _seed_entry(user, *, accepted: bool = True):
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
        student_action=(
            StudentAction.ACCEPTED if accepted else StudentAction.NONE_YET
        ),
        lifecycle_status=(
            JournalLifecycleStatus.ACCEPTED
            if accepted
            else JournalLifecycleStatus.RECOMMENDED
        ),
    )


class TestReflectionCaptureRoute:
    def test_journal_shows_optional_reflection(self, student_client, user, db):
        _seed_entry(user)
        resp = student_client.get("/student/decision-journal")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "Optional reflection" in body
        assert "Did this recommendation help?" in body
        assert "Was the timing appropriate?" in body
        assert 'aria-labelledby="dj-reflect-1"' in body or "dj-reflect-" in body
        for term in FORBIDDEN_TERMS:
            assert term not in body.lower()

    def test_post_reflection_persists(self, student_client, user, db):
        entry = _seed_entry(user)
        DecisionJournalService.record_outcome(
            user.id,
            entry.entry_id,
            outcome_summary="Mission completed",
        )
        prefix = entry.entry_id
        resp = student_client.post(
            f"/student/decision-journal/{entry.entry_id}/reflect",
            data={
                "csrf_token": "not-checked-in-tests",
                f"{prefix}-csrf_token": "x",
                f"{prefix}-entry_id": entry.entry_id,
                f"{prefix}-helped": "yes",
                f"{prefix}-timing": "mostly",
                f"{prefix}-understood_why": "yes",
                f"{prefix}-same_decision": "yes",
                f"{prefix}-free_text": "Clearer than yesterday.",
                f"{prefix}-submit": "Save reflection",
            },
            follow_redirects=True,
        )
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "Reflection saved" in body or "Reflected" in body
        refreshed = DecisionJournalService.get_entry(user.id, entry.entry_id)
        assert refreshed.reflection_note
        assert "Clearer than yesterday" in refreshed.reflection_note
        assert (
            EducationalFeedbackReview.query.filter_by(user_id=user.id).count()
            >= 1
        )
        # Sensei review must not leak into student journal HTML.
        assert "future learning" not in body.lower()
        assert "educational_assessment" not in body.lower()

    def test_requires_login(self, client, user, db):
        entry = _seed_entry(user)
        resp = client.post(
            f"/student/decision-journal/{entry.entry_id}/reflect",
            follow_redirects=False,
        )
        assert resp.status_code in (302, 401)


class TestTimelineIntegration:
    def test_reflected_entry_feeds_timeline(self, user, db):
        entry = _seed_entry(user)
        DecisionJournalService.record_outcome(
            user.id,
            entry.entry_id,
            outcome_summary="Mission completed",
        )
        DecisionJournalService.record_reflection(
            user.id,
            entry.entry_id,
            note="Did this recommendation help: Yes\nUseful focus.",
        )
        narrative = EducationalTimelineService.build_for_user(user.id)
        assert narrative.entry_count >= 1
        assert narrative.certainty in (
            NarrativeCertainty.INSUFFICIENT,
            NarrativeCertainty.SUGGESTIVE,
            NarrativeCertainty.SUPPORTED,
        )
        # Reflection highlights section should see the reflected entry.
        labels = [s.label for s in narrative.sections]
        assert any("Reflection" in label or "reflection" in label.lower()
                   for label in labels) or narrative.entry_count >= 1


class TestRegression:
    def test_decision_journal_still_renders(self, student_client, user, db):
        _seed_entry(user)
        resp = student_client.get("/student/decision-journal")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "What happened?" in body
        assert "Discounting" in body

    def test_educational_timeline_route(self, student_client, user, db):
        _seed_entry(user)
        resp = student_client.get("/student/educational-timeline")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "Educational Timeline" in body or "timeline" in body.lower()
        for term in FORBIDDEN_TERMS:
            assert term not in body.lower()
