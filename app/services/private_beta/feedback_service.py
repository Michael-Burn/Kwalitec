"""Private beta student feedback capture (PB-001)."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.extensions import db
from app.models.mission import Mission
from app.models.private_beta import (
    FEEDBACK_CATEGORIES,
    PrivateBetaFeedback,
)
from app.services.private_beta.classification import (
    classify_feedback_severity,
    parse_user_agent,
)
from app.version import APP_VERSION

logger = logging.getLogger(__name__)

CATEGORY_LABELS: dict[str, str] = {
    "bug": "Bug",
    "suggestion": "Suggestion",
    "confusing_screen": "Confusing screen",
    "missing_feature": "Missing feature",
    "incorrect_recommendation": "Incorrect recommendation",
    "general": "General feedback",
}


@dataclass(frozen=True)
class FeedbackSubmitResult:
    ok: bool
    feedback_id: int | None
    severity: str | None = None
    error: str | None = None


class PrivateBetaFeedbackService:
    """Persist categorised private-beta feedback with auto severity."""

    @staticmethod
    def submit(
        *,
        user_id: int,
        category: str,
        message: str,
        current_screen: str | None = None,
        subject_code: str | None = None,
        browser: str | None = None,
        device: str | None = None,
        user_agent: str | None = None,
        path: str | None = None,
        mission_id: int | None = None,
        product_version: str | None = None,
    ) -> FeedbackSubmitResult:
        """Validate and store one feedback report."""
        cat = (category or "").strip().lower()
        if cat not in FEEDBACK_CATEGORIES:
            return FeedbackSubmitResult(
                ok=False,
                feedback_id=None,
                error="Please choose a feedback category.",
            )

        cleaned = (message or "").strip()
        if not cleaned:
            return FeedbackSubmitResult(
                ok=False,
                feedback_id=None,
                error="Please include a short message.",
            )
        if len(cleaned) > 1000:
            cleaned = cleaned[:1000]

        owned_mission_id = None
        if mission_id is not None:
            mission = Mission.query.filter_by(id=mission_id, user_id=user_id).first()
            if mission is None:
                return FeedbackSubmitResult(
                    ok=False,
                    feedback_id=None,
                    error="Mission not found.",
                )
            owned_mission_id = mission.id

        ua = (user_agent or "").strip() or None
        parsed_browser, parsed_device = parse_user_agent(ua)
        severity = classify_feedback_severity(category=cat, message=cleaned)

        row = PrivateBetaFeedback(
            user_id=user_id,
            category=cat,
            severity=severity,
            message=cleaned,
            current_screen=(current_screen or None),
            subject_code=(subject_code or None),
        browser=(browser or parsed_browser)[:64]
        if (browser or parsed_browser)
        else None,
        device=(device or parsed_device)[:64]
        if (device or parsed_device)
        else None,
            product_version=(product_version or APP_VERSION)[:32],
            user_agent=ua[:512] if ua else None,
            path=(path or None),
            mission_id=owned_mission_id,
            status="new",
        )
        db.session.add(row)
        try:
            db.session.commit()
        except Exception:  # noqa: BLE001
            db.session.rollback()
            logger.exception("Failed to store private beta feedback user=%s", user_id)
            return FeedbackSubmitResult(
                ok=False,
                feedback_id=None,
                error="Could not save feedback. Please try again.",
            )

        logger.info(
            "private_beta_feedback id=%s category=%s severity=%s user=%s",
            row.id,
            cat,
            severity,
            user_id,
        )
        return FeedbackSubmitResult(
            ok=True, feedback_id=row.id, severity=severity
        )

    @staticmethod
    def recent(*, limit: int = 25) -> list[PrivateBetaFeedback]:
        return list(
            PrivateBetaFeedback.query.order_by(PrivateBetaFeedback.created_at.desc())
            .limit(max(1, min(limit, 200)))
            .all()
        )

    @staticmethod
    def count_by_severity() -> dict[str, int]:
        rows = (
            db.session.query(
                PrivateBetaFeedback.severity,
                db.func.count(PrivateBetaFeedback.id),
            )
            .group_by(PrivateBetaFeedback.severity)
            .all()
        )
        return {str(sev): int(count) for sev, count in rows}

    @staticmethod
    def critical_open_count() -> int:
        return (
            db.session.query(db.func.count(PrivateBetaFeedback.id))
            .filter(
                PrivateBetaFeedback.severity == "critical",
                PrivateBetaFeedback.status.in_(("new", "triaged", "open")),
            )
            .scalar()
            or 0
        )

    @staticmethod
    def category_choices() -> list[tuple[str, str]]:
        return [(key, CATEGORY_LABELS[key]) for key in FEEDBACK_CATEGORIES]
