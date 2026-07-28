"""Educational Feedback Loop application service (ILE-005).

Orchestrates recommendation review, optional student reflection, and
internal Sensei educational reviews. No HTTP; no Twin; no re-ranking.
"""

from __future__ import annotations

from app.application.educational_feedback_loop.dto import (
    EducationalFeedbackLoopSnapshot,
    RecommendationReviewSnapshot,
    ReflectionPromptSnapshot,
    StudentReflectionInviteSnapshot,
)
from app.domain.educational_feedback_loop import (
    RecommendationReview,
    StudentReflectionInvite,
)
from app.services.educational_feedback_loop_service import (
    EducationalFeedbackLoopService,
)


class EducationalFeedbackLoopApplicationService:
    """Application façade for educational feedback calibration."""

    @staticmethod
    def review_entry(
        user_id: int,
        entry_id: str,
    ) -> RecommendationReviewSnapshot:
        """Assess one journal recommendation without writing."""
        review = EducationalFeedbackLoopService.assess_entry(
            user_id, entry_id
        )
        return EducationalFeedbackLoopApplicationService._review_snapshot(
            review
        )

    @staticmethod
    def reflection_invite(
        user_id: int,
        entry_id: str,
    ) -> StudentReflectionInviteSnapshot:
        """Build optional student reflection invite for one entry."""
        invite = EducationalFeedbackLoopService.reflection_invite(
            user_id, entry_id
        )
        return EducationalFeedbackLoopApplicationService._invite_snapshot(
            invite
        )

    @staticmethod
    def capture_reflection(
        user_id: int,
        entry_id: str,
        *,
        helped: str = "",
        timing: str = "",
        understood_why: str = "",
        same_decision: str = "",
        free_text: str = "",
    ) -> EducationalFeedbackLoopSnapshot:
        """Capture optional reflection and refresh Sensei review."""
        result = EducationalFeedbackLoopService.capture_student_reflection(
            user_id,
            entry_id,
            helped=helped,
            timing=timing,
            understood_why=understood_why,
            same_decision=same_decision,
            free_text=free_text,
        )
        review = result["review"]
        invite = EducationalFeedbackLoopService.reflection_invite(
            user_id, entry_id
        )
        return EducationalFeedbackLoopSnapshot(
            review=EducationalFeedbackLoopApplicationService._review_snapshot(
                review
            ),
            reflection_invite=(
                EducationalFeedbackLoopApplicationService._invite_snapshot(
                    invite
                )
            ),
            sensei_review_recorded=result.get("sensei_review") is not None,
        )

    @staticmethod
    def snapshot_for_entry(
        user_id: int,
        entry_id: str,
    ) -> EducationalFeedbackLoopSnapshot:
        """Compose review + invite snapshot for one journal entry."""
        review = EducationalFeedbackLoopService.assess_entry(
            user_id, entry_id
        )
        invite = EducationalFeedbackLoopService.reflection_invite(
            user_id, entry_id
        )
        return EducationalFeedbackLoopSnapshot(
            review=EducationalFeedbackLoopApplicationService._review_snapshot(
                review
            ),
            reflection_invite=(
                EducationalFeedbackLoopApplicationService._invite_snapshot(
                    invite
                )
            ),
            sensei_review_recorded=False,
        )

    @staticmethod
    def _review_snapshot(
        review: RecommendationReview,
    ) -> RecommendationReviewSnapshot:
        return RecommendationReviewSnapshot(
            decision_id=review.decision_id,
            review_state=review.review_state.value,
            review_state_label=review.review_state_label,
            evidence_quality=review.evidence_quality.value,
            evidence_quality_label=review.evidence_quality_label,
            educational_assessment=review.educational_assessment,
            future_learning=review.future_learning,
            rationale_points=review.rationale_points,
            empty=review.empty,
        )

    @staticmethod
    def _invite_snapshot(
        invite: StudentReflectionInvite,
    ) -> StudentReflectionInviteSnapshot:
        prompts = tuple(
            ReflectionPromptSnapshot(
                prompt_id=p.prompt_id,
                question=p.question,
                answer_choices=p.answer_choices,
            )
            for p in invite.prompts
        )
        return StudentReflectionInviteSnapshot(
            decision_id=invite.decision_id,
            recommendation_title=invite.recommendation_title,
            prompts=prompts,
            intro_line=invite.intro_line,
            optional_note_label=invite.optional_note_label,
            submit_label=invite.submit_label,
            skip_label=invite.skip_label,
            available=invite.available,
        )
