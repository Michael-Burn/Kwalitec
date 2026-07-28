"""Domain tests for Educational Feedback Loop (ILE-005)."""

from __future__ import annotations

import pytest

from app.domain.decision_journal.enums import (
    QualitativeConfidence,
    ReflectionStatus,
    StudentAction,
)
from app.domain.educational_feedback_loop import (
    FeedbackEvidenceInput,
    RecommendationReviewState,
    assess_recommendation_review,
    compose_reflection_invite,
    compose_sensei_review,
    empty_recommendation_review,
    format_reflection_note,
    parse_reflection_answers_from_note,
)
from app.domain.educational_feedback_loop.invariants import (
    assert_calibration_speech_safe,
)


class TestAssessRecommendationReview:
    def test_requires_future_observation_without_response(self):
        review = assess_recommendation_review(
            FeedbackEvidenceInput(
                decision_id="dj_1",
                recommendation="Revise Discounting",
                student_action=StudentAction.NONE_YET.value,
            )
        )
        assert (
            review.review_state
            == RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION
        )

    def test_supported_with_outcome_and_affirming_reflection(self):
        note = format_reflection_note(
            helped="yes",
            timing="yes",
            understood_why="mostly",
            same_decision="yes",
        )
        answers = parse_reflection_answers_from_note(note)
        review = assess_recommendation_review(
            FeedbackEvidenceInput(
                decision_id="dj_2",
                recommendation="Practice duration matching",
                student_action=StudentAction.ACCEPTED.value,
                outcome_summary="Mission completed",
                reflection_status=ReflectionStatus.REFLECTED.value,
                reflection_note=note,
                qualitative_confidence=QualitativeConfidence.RELIABLE.value,
                supporting_evidence_summary="Two uneven sessions.",
                evidence_update_count=1,
                **answers,
            )
        )
        assert review.review_state == RecommendationReviewState.SUPPORTED
        assert "supports" in review.educational_assessment.lower()

    def test_evidence_insufficient(self):
        review = assess_recommendation_review(
            {
                "decision_id": "dj_3",
                "recommendation": "Quick Check",
                "student_action": StudentAction.ACCEPTED.value,
                "qualitative_confidence": (
                    QualitativeConfidence.INSUFFICIENT.value
                ),
            }
        )
        assert (
            review.review_state
            == RecommendationReviewState.EVIDENCE_INSUFFICIENT
        )

    def test_partially_supported_mixed_reflection(self):
        review = assess_recommendation_review(
            FeedbackEvidenceInput(
                decision_id="dj_4",
                recommendation="Recovery session",
                student_action=StudentAction.ACCEPTED.value,
                outcome_summary="Session finished",
                reflection_status=ReflectionStatus.REFLECTED.value,
                helped_answer="yes",
                timing_answer="no",
                understood_why_answer="no",
                same_decision_answer="mostly",
                supporting_evidence_summary="Missed yesterday.",
            )
        )
        assert (
            review.review_state
            == RecommendationReviewState.PARTIALLY_SUPPORTED
        )

    def test_empty_without_recommendation(self):
        review = assess_recommendation_review({})
        assert review.empty
        assert review.review_state == (
            RecommendationReviewState.REQUIRES_FUTURE_OBSERVATION
        )

    def test_forbids_engagement_theatre(self):
        with pytest.raises(ValueError, match="engagement"):
            assert_calibration_speech_safe(
                "Boost engagement with a longer streak"
            )

    def test_empty_helper(self):
        review = empty_recommendation_review(reason="Nothing yet.")
        assert review.empty
        assert "Nothing yet" in review.educational_assessment


class TestReflectionAndSensei:
    def test_compose_reflection_invite(self):
        invite = compose_reflection_invite(
            decision_id="dj_9",
            recommendation_title="Revise CT1",
        )
        assert invite.available
        assert len(invite.prompts) == 4
        assert "optional" in invite.intro_line.lower()

    def test_invite_unavailable_when_reflected(self):
        invite = compose_reflection_invite(
            decision_id="dj_9",
            already_reflected=True,
        )
        assert not invite.available

    def test_sensei_review_not_learner_visible(self):
        review = assess_recommendation_review(
            FeedbackEvidenceInput(
                decision_id="dj_10",
                recommendation="Focus on equity",
                student_action=StudentAction.ACCEPTED.value,
                outcome_summary="Completed",
                reflection_status=ReflectionStatus.REFLECTED.value,
                helped_answer="yes",
                timing_answer="yes",
                understood_why_answer="yes",
                same_decision_answer="yes",
                supporting_evidence_summary="Prior practice.",
                evidence_update_count=1,
                qualitative_confidence=QualitativeConfidence.RELIABLE.value,
            )
        )
        sensei = compose_sensei_review(
            review=review,
            observation="Practice looked fragile.",
            original_recommendation="Focus on equity",
            later_evidence="Outcome: Completed",
        )
        assert sensei.learner_visible is False
        assert sensei.decision_id == "dj_10"
