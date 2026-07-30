"""Private beta participant enrolment (PB-001)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime

from app.extensions import db
from app.models.private_beta import PrivateBetaParticipant
from app.models.user import User

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EnrolmentResult:
    ok: bool
    participant_id: int | None
    error: str | None = None


class PrivateBetaParticipantService:
    """Enrol and list private-beta cohort members."""

    @staticmethod
    def enrol(
        *,
        user_id: int,
        cohort_label: str = "pb001",
        device_preference: str | None = None,
        notes: str | None = None,
    ) -> EnrolmentResult:
        """Enrol a user into the private beta cohort (idempotent)."""
        user = db.session.get(User, user_id)
        if user is None:
            return EnrolmentResult(
                ok=False, participant_id=None, error="User not found."
            )

        existing = PrivateBetaParticipant.query.filter_by(user_id=user_id).first()
        if existing is not None:
            existing.is_active = True
            if device_preference:
                existing.device_preference = device_preference[:32]
            if notes:
                existing.notes = notes[:500]
            try:
                db.session.commit()
            except Exception:  # noqa: BLE001
                db.session.rollback()
                logger.exception("Failed to refresh beta participant user=%s", user_id)
                return EnrolmentResult(
                    ok=False, participant_id=None, error="Could not update enrolment."
                )
            return EnrolmentResult(ok=True, participant_id=existing.id)

        participant = PrivateBetaParticipant(
            user_id=user_id,
            enrolled_at=datetime.now(UTC).replace(tzinfo=None),
            cohort_label=(cohort_label or "pb001")[:64],
            device_preference=(device_preference or None),
            notes=(notes[:500] if notes else None),
            is_active=True,
        )
        db.session.add(participant)
        try:
            db.session.commit()
        except Exception:  # noqa: BLE001
            db.session.rollback()
            logger.exception("Failed to enrol beta participant user=%s", user_id)
            return EnrolmentResult(
                ok=False, participant_id=None, error="Could not enrol participant."
            )
        logger.info(
            "private_beta_enrolled user=%s participant=%s",
            user_id,
            participant.id,
        )
        return EnrolmentResult(ok=True, participant_id=participant.id)

    @staticmethod
    def active_participants() -> list[PrivateBetaParticipant]:
        return list(
            PrivateBetaParticipant.query.filter_by(is_active=True)
            .order_by(PrivateBetaParticipant.enrolled_at.asc())
            .all()
        )

    @staticmethod
    def active_user_ids() -> set[int]:
        rows = (
            db.session.query(PrivateBetaParticipant.user_id)
            .filter_by(is_active=True)
            .all()
        )
        return {int(r[0]) for r in rows}

    @staticmethod
    def count_active() -> int:
        return (
            db.session.query(db.func.count(PrivateBetaParticipant.id))
            .filter_by(is_active=True)
            .scalar()
            or 0
        )
