"""Lightweight Internal Alpha feedback — ALPHA-001.

Stores short in-flow feedback (mission helpful, explanation clear,
report a problem, suggest an improvement). Never mutates Twin,
readiness, recommendations, or Education OS state.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.extensions import db
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.models.alpha_infrastructure import AlphaFeedbackSubmission
from app.models.mission import Mission
from app.version import APP_VERSION

logger = logging.getLogger(__name__)

KIND_MISSION_HELPFUL = "mission_helpful"
KIND_EXPLANATION_CLEAR = "explanation_clear"
KIND_REPORT_PROBLEM = "report_problem"
KIND_SUGGEST_IMPROVEMENT = "suggest_improvement"

ALLOWED_KINDS = frozenset(
    {
        KIND_MISSION_HELPFUL,
        KIND_EXPLANATION_CLEAR,
        KIND_REPORT_PROBLEM,
        KIND_SUGGEST_IMPROVEMENT,
    }
)

BINARY_KINDS = frozenset({KIND_MISSION_HELPFUL, KIND_EXPLANATION_CLEAR})
TEXT_KINDS = frozenset({KIND_REPORT_PROBLEM, KIND_SUGGEST_IMPROVEMENT})

RATING_YES = "yes"
RATING_NO = "no"
ALLOWED_RATINGS = frozenset({RATING_YES, RATING_NO})


@dataclass(frozen=True)
class AlphaFeedbackResult:
    """Outcome of a feedback submission attempt."""

    ok: bool
    submission_id: int | None
    error: str | None = None


class AlphaFeedbackService:
    """Persist structured lightweight alpha feedback."""

    @staticmethod
    def submit(
        *,
        user_id: int,
        kind: str,
        rating: str | None = None,
        message: str | None = None,
        mission_id: int | None = None,
        surface: str | None = None,
        correlation_id: str | None = None,
    ) -> AlphaFeedbackResult:
        """Validate and store one feedback submission."""
        normalised_kind = (kind or "").strip().lower()
        if normalised_kind not in ALLOWED_KINDS:
            return AlphaFeedbackResult(
                ok=False,
                submission_id=None,
                error="Invalid feedback kind.",
            )

        normalised_rating = (rating or "").strip().lower() or None
        cleaned_message = (message or "").strip() or None
        if cleaned_message and len(cleaned_message) > 500:
            cleaned_message = cleaned_message[:500]

        if normalised_kind in BINARY_KINDS:
            if normalised_rating not in ALLOWED_RATINGS:
                return AlphaFeedbackResult(
                    ok=False,
                    submission_id=None,
                    error="Please choose yes or no.",
                )
        elif normalised_kind in TEXT_KINDS:
            if not cleaned_message:
                return AlphaFeedbackResult(
                    ok=False,
                    submission_id=None,
                    error="Please include a short message.",
                )

        owned_mission_id = None
        if mission_id is not None:
            mission = (
                Mission.query.filter_by(id=mission_id, user_id=user_id).first()
            )
            if mission is None:
                return AlphaFeedbackResult(
                    ok=False,
                    submission_id=None,
                    error="Mission not found.",
                )
            owned_mission_id = mission.id

        corr = (correlation_id or "").strip() or CorrelationContext.get_correlation_id()
        submission = AlphaFeedbackSubmission(
            user_id=user_id,
            kind=normalised_kind,
            rating=normalised_rating,
            message=cleaned_message,
            mission_id=owned_mission_id,
            surface=(surface or None),
            product_version=APP_VERSION,
            correlation_id=corr or None,
            status="new",
        )
        db.session.add(submission)
        try:
            db.session.commit()
        except Exception:  # noqa: BLE001
            db.session.rollback()
            logger.exception("Failed to store alpha feedback kind=%s", normalised_kind)
            return AlphaFeedbackResult(
                ok=False,
                submission_id=None,
                error="Could not save feedback. Please try again.",
            )

        logger.info(
            "alpha_feedback kind=%s user=%s id=%s correlation_id=%s",
            normalised_kind,
            user_id,
            submission.id,
            corr or "-",
        )
        return AlphaFeedbackResult(ok=True, submission_id=submission.id)

    @staticmethod
    def recent(
        *,
        limit: int = 50,
        kind: str | None = None,
    ) -> list[AlphaFeedbackSubmission]:
        """Recent submissions for founder support tooling."""
        query = AlphaFeedbackSubmission.query.order_by(
            AlphaFeedbackSubmission.created_at.desc()
        )
        if kind:
            query = query.filter_by(kind=kind.strip().lower())
        return list(query.limit(max(1, min(limit, 200))).all())
