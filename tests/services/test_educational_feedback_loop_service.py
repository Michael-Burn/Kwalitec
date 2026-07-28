"""Service tests for Educational Feedback Loop (ILE-005)."""

from __future__ import annotations

from app.domain.decision_journal import (
    EntryKind,
    JournalLifecycleStatus,
    QualitativeConfidence,
    ReflectionStatus,
    StudentAction,
)
from app.domain.educational_feedback_loop import RecommendationReviewState
from app.models.educational_feedback import EducationalFeedbackReview
from app.services.decision_journal_service import DecisionJournalService
from app.services.educational_feedback_loop_service import (
    EducationalFeedbackLoopService,
)


def _seed_accepted(user):
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
        student_action=StudentAction.ACCEPTED,
        lifecycle_status=JournalLifecycleStatus.ACCEPTED,
    )


class TestEducationalFeedbackLoopService:
    def test_assess_requires_future_observation(self, user, db):
        entry = _seed_accepted(user)
        review = EducationalFeedbackLoopService.assess_entry(
            user.id, entry.entry_id
        )
        assert review.review_state == (
            RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION
        )

    def test_capture_reflection_and_sensei_review(self, user, db):
        entry = _seed_accepted(user)
        DecisionJournalService.record_outcome(
            user.id,
            entry.entry_id,
            outcome_summary="Mission completed",
        )
        result = EducationalFeedbackLoopService.capture_student_reflection(
            user.id,
            entry.entry_id,
            helped="yes",
            timing="yes",
            understood_why="yes",
            same_decision="mostly",
            free_text="The timing felt right for syllabus order.",
        )
        updated = result["entry"]
        assert updated.reflection_status == ReflectionStatus.REFLECTED.value
        assert "Did this recommendation help" in updated.reflection_note
        assert result["review"].review_state in (
            RecommendationReviewState.SUPPORTED,
            RecommendationReviewState.PARTIALLY_SUPPORTED,
        )
        assert result["sensei_review"] is not None
        assert result["sensei_review"].learner_visible is False

        rows = EducationalFeedbackReview.query.filter_by(
            user_id=user.id, journal_entry_id=entry.entry_id
        ).all()
        assert len(rows) == 1
        assert rows[0].learner_visible is False

    def test_journal_integration_appends_evidence(self, user, db):
        entry = _seed_accepted(user)
        EducationalFeedbackLoopService.capture_student_reflection(
            user.id,
            entry.entry_id,
            helped="mostly",
            timing="yes",
        )
        refreshed = DecisionJournalService.get_entry(user.id, entry.entry_id)
        payload = DecisionJournalService.to_student_dict(refreshed)
        assert payload["reflection_status"] == ReflectionStatus.REFLECTED.value
        assert any(
            "reflection" in (u["summary"] or "").lower()
            for u in payload["evidence_updates"]
        )

    def test_review_after_outcome(self, user, db):
        entry = _seed_accepted(user)
        DecisionJournalService.record_outcome(
            user.id,
            entry.entry_id,
            outcome_summary="Mission completed",
        )
        review = EducationalFeedbackLoopService.review_after_outcome(
            user.id, entry.entry_id
        )
        assert review is not None
        assert review.review_state in (
            RecommendationReviewState.INCONCLUSIVE,
            RecommendationReviewState.PARTIALLY_SUPPORTED,
            RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION,
        )
        assert (
            EducationalFeedbackReview.query.filter_by(user_id=user.id).count()
            == 1
        )

    def test_reflection_invite(self, user, db):
        entry = _seed_accepted(user)
        invite = EducationalFeedbackLoopService.reflection_invite(
            user.id, entry.entry_id
        )
        assert invite.available
        assert len(invite.prompts) == 4
