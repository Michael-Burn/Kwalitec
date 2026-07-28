"""Educational Feedback Loop service (ILE-005).

Reviews recommendation outcomes via Decision Journal evidence, captures
optional student reflection, and records internal Sensei educational
reviews. Never re-ranks recommendations; never mutates Twin or mastery.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from app.domain.decision_journal.enums import ReflectionStatus
from app.domain.educational_feedback_loop import (
    FeedbackEvidenceInput,
    RecommendationReview,
    SenseiEducationalReview,
    StudentReflectionInvite,
    assess_recommendation_review,
    compose_reflection_invite,
    compose_sensei_review,
    format_reflection_note,
    parse_reflection_answers_from_note,
    summarise_later_evidence,
)
from app.extensions import db
from app.models.educational_feedback import EducationalFeedbackReview
from app.services.decision_journal_service import (
    DecisionJournalError,
    DecisionJournalService,
)

logger = logging.getLogger(__name__)


class EducationalFeedbackLoopError(Exception):
    """Base error for Educational Feedback Loop operations."""


class EducationalFeedbackLoopService:
    """Educational calibration over Decision Journal recommendation records."""

    @staticmethod
    def assess_entry(
        user_id: int,
        entry_id: str,
        *,
        helped_answer: str = "",
        timing_answer: str = "",
        understood_why_answer: str = "",
        same_decision_answer: str = "",
    ) -> RecommendationReview:
        """Assess educational usefulness of one owned journal entry.

        Pure projection from journal state (+ optional answer overrides).
        Does not write.
        """
        entry = DecisionJournalService.get_entry(user_id, entry_id)
        payload = DecisionJournalService.to_student_dict(entry)
        answers = parse_reflection_answers_from_note(
            payload.get("reflection_note") or ""
        )
        evidence = FeedbackEvidenceInput(
            decision_id=payload["decision_id"],
            recommendation=payload.get("recommendation") or "",
            observation=payload.get("observation") or "",
            meaning=payload.get("meaning") or "",
            expected_benefit=payload.get("expected_benefit") or "",
            student_action=payload.get("student_action") or "",
            outcome_summary=payload.get("outcome_summary") or "",
            reflection_status=payload.get("reflection_status") or "",
            reflection_note=payload.get("reflection_note") or "",
            qualitative_confidence=payload.get("qualitative_confidence")
            or "",
            supporting_evidence_summary=payload.get(
                "supporting_evidence_summary"
            )
            or "",
            evidence_update_count=len(payload.get("evidence_updates") or []),
            evidence_update_summaries=tuple(
                item.get("summary") or ""
                for item in (payload.get("evidence_updates") or [])
            ),
            helped_answer=helped_answer or answers.get("helped_answer", ""),
            timing_answer=timing_answer or answers.get("timing_answer", ""),
            understood_why_answer=understood_why_answer
            or answers.get("understood_why_answer", ""),
            same_decision_answer=same_decision_answer
            or answers.get("same_decision_answer", ""),
        )
        return assess_recommendation_review(evidence)

    @staticmethod
    def reflection_invite(
        user_id: int,
        entry_id: str,
    ) -> StudentReflectionInvite:
        """Build an optional student reflection invite for a journal entry."""
        entry = DecisionJournalService.get_entry(user_id, entry_id)
        already = entry.reflection_status == ReflectionStatus.REFLECTED.value
        return compose_reflection_invite(
            decision_id=entry.entry_id,
            recommendation_title=entry.recommendation or "",
            already_reflected=already,
        )

    @staticmethod
    def capture_student_reflection(
        user_id: int,
        entry_id: str,
        *,
        helped: str = "",
        timing: str = "",
        understood_why: str = "",
        same_decision: str = "",
        free_text: str = "",
        persist_sensei_review: bool = True,
    ) -> dict[str, Any]:
        """Persist optional student reflection and refresh Sensei review.

        Appends educational evidence only — never rewrites the original
        recommendation snapshot. Failures raise ``EducationalFeedbackLoopError``
        for journal transition problems; Sensei persistence is fail-open.

        Returns:
            Dict with ``entry``, ``review``, and optional ``sensei_review``.
        """
        note = format_reflection_note(
            helped=helped,
            timing=timing,
            understood_why=understood_why,
            same_decision=same_decision,
            free_text=free_text,
        )
        try:
            entry = DecisionJournalService.record_reflection(
                user_id,
                entry_id,
                note=note,
            )
        except DecisionJournalError as exc:
            raise EducationalFeedbackLoopError(str(exc)) from exc

        # Append a calm evidence line — never replaces history.
        try:
            DecisionJournalService.append_evidence(
                user_id,
                entry_id,
                summary=(
                    "Learner reflection recorded for educational "
                    "calibration of this guidance."
                ),
                move_status=False,
            )
        except DecisionJournalError:
            logger.exception(
                "feedback_loop_evidence_append_failed user_id=%s entry_id=%s",
                user_id,
                entry_id,
            )

        review = EducationalFeedbackLoopService.assess_entry(
            user_id,
            entry_id,
            helped_answer=helped,
            timing_answer=timing,
            understood_why_answer=understood_why,
            same_decision_answer=same_decision,
        )
        sensei: SenseiEducationalReview | None = None
        if persist_sensei_review:
            sensei = EducationalFeedbackLoopService.record_sensei_review(
                user_id,
                entry_id,
                review=review,
            )
        logger.info(
            "feedback_loop_reflection_captured user_id=%s entry_id=%s "
            "state=%s",
            user_id,
            entry_id,
            review.review_state.value,
        )
        return {
            "entry": entry,
            "review": review,
            "sensei_review": sensei,
        }

    @staticmethod
    def record_sensei_review(
        user_id: int,
        entry_id: str,
        *,
        review: RecommendationReview | None = None,
    ) -> SenseiEducationalReview | None:
        """Persist an internal Sensei educational review (not learner-visible).

        Idempotent per entry + review_state: reuses the latest matching row
        when state is unchanged; otherwise appends a new review row.
        Fail-open on persistence errors.
        """
        try:
            entry = DecisionJournalService.get_entry(user_id, entry_id)
            assessed = review or EducationalFeedbackLoopService.assess_entry(
                user_id, entry_id
            )
            payload = DecisionJournalService.to_student_dict(entry)
            later = summarise_later_evidence(
                outcome_summary=payload.get("outcome_summary") or "",
                reflection_note=payload.get("reflection_note") or "",
                evidence_updates=tuple(
                    item.get("summary") or ""
                    for item in (payload.get("evidence_updates") or [])
                ),
            )
            sensei = compose_sensei_review(
                review=assessed,
                observation=payload.get("observation") or "",
                original_recommendation=payload.get("recommendation") or "",
                later_evidence=later,
            )
            existing = (
                EducationalFeedbackReview.query.filter_by(
                    user_id=user_id,
                    journal_entry_id=entry_id,
                    review_state=sensei.review_state.value,
                )
                .order_by(EducationalFeedbackReview.recorded_at.desc())
                .first()
            )
            if existing is not None:
                return sensei

            row = EducationalFeedbackReview(
                review_id=_new_review_id(),
                user_id=user_id,
                journal_entry_id=entry_id,
                observation=sensei.observation,
                original_recommendation=sensei.original_recommendation,
                later_evidence=sensei.later_evidence,
                educational_assessment=sensei.educational_assessment,
                future_learning=sensei.future_learning,
                review_state=sensei.review_state.value,
                evidence_quality=sensei.evidence_quality.value,
                assessment_focus=sensei.assessment_focus.value,
                rationale_summary="; ".join(sensei.rationale_points),
                learner_visible=False,
            )
            db.session.add(row)
            db.session.commit()
            logger.info(
                "feedback_loop_sensei_review_recorded user_id=%s "
                "entry_id=%s review_id=%s state=%s",
                user_id,
                entry_id,
                row.review_id,
                row.review_state,
            )
            return sensei
        except Exception:
            logger.exception(
                "feedback_loop_sensei_review_failed user_id=%s entry_id=%s",
                user_id,
                entry_id,
            )
            try:
                db.session.rollback()
            except Exception:
                pass
            return None

    @staticmethod
    def review_after_outcome(
        user_id: int,
        entry_id: str,
    ) -> RecommendationReview | None:
        """Refresh internal Sensei review after an educational outcome.

        Fail-open: returns None on soft failure.
        """
        try:
            review = EducationalFeedbackLoopService.assess_entry(
                user_id, entry_id
            )
            EducationalFeedbackLoopService.record_sensei_review(
                user_id,
                entry_id,
                review=review,
            )
            return review
        except Exception:
            logger.exception(
                "feedback_loop_review_after_outcome_failed "
                "user_id=%s entry_id=%s",
                user_id,
                entry_id,
            )
            return None

    @staticmethod
    def list_sensei_reviews(
        user_id: int,
        *,
        limit: int = 50,
    ) -> list[EducationalFeedbackReview]:
        """Return internal Sensei reviews for governance (never student UI)."""
        return (
            EducationalFeedbackReview.query.filter_by(user_id=user_id)
            .filter_by(learner_visible=False)
            .order_by(EducationalFeedbackReview.recorded_at.desc())
            .limit(max(1, min(limit, 200)))
            .all()
        )


def _new_review_id() -> str:
    return f"efr_{uuid.uuid4().hex[:20]}"
