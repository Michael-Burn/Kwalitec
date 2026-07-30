"""Founder observation checklist for private beta (PB-001)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import UTC, datetime

from app.extensions import db
from app.models.private_beta import PrivateBetaObservation
from app.models.user import User

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ObservationResult:
    ok: bool
    observation_id: int | None
    error: str | None = None


def _tri_state(value: bool | None) -> bool | None:
    if value is None:
        return None
    return bool(value)


class PrivateBetaObservationService:
    """Persist founder observation checklist answers per beta user."""

    @staticmethod
    def record(
        *,
        user_id: int,
        observer_user_id: int | None = None,
        understood_onboarding: bool | None = None,
        knew_where_to_click: bool | None = None,
        understood_todays_mission: bool | None = None,
        understood_progress: bool | None = None,
        understood_tutor: bool | None = None,
        understood_knowledge_map: bool | None = None,
        became_stuck: bool | None = None,
        stuck_where: str | None = None,
        notes: str | None = None,
    ) -> ObservationResult:
        """Store one observation checklist row."""
        user = db.session.get(User, user_id)
        if user is None:
            return ObservationResult(
                ok=False, observation_id=None, error="User not found."
            )

        stuck = (stuck_where or "").strip() or None
        if stuck and len(stuck) > 255:
            stuck = stuck[:255]
        cleaned_notes = (notes or "").strip() or None
        if cleaned_notes and len(cleaned_notes) > 1000:
            cleaned_notes = cleaned_notes[:1000]

        row = PrivateBetaObservation(
            user_id=user_id,
            observer_user_id=observer_user_id,
            understood_onboarding=_tri_state(understood_onboarding),
            knew_where_to_click=_tri_state(knew_where_to_click),
            understood_todays_mission=_tri_state(understood_todays_mission),
            understood_progress=_tri_state(understood_progress),
            understood_tutor=_tri_state(understood_tutor),
            understood_knowledge_map=_tri_state(understood_knowledge_map),
            became_stuck=_tri_state(became_stuck),
            stuck_where=stuck,
            notes=cleaned_notes,
            observed_at=datetime.now(UTC).replace(tzinfo=None),
        )
        db.session.add(row)
        try:
            db.session.commit()
        except Exception:  # noqa: BLE001
            db.session.rollback()
            logger.exception("Failed to store beta observation user=%s", user_id)
            return ObservationResult(
                ok=False,
                observation_id=None,
                error="Could not save observation.",
            )
        return ObservationResult(ok=True, observation_id=row.id)

    @staticmethod
    def recent(*, limit: int = 50) -> list[PrivateBetaObservation]:
        return list(
            PrivateBetaObservation.query.order_by(
                PrivateBetaObservation.observed_at.desc()
            )
            .limit(max(1, min(limit, 200)))
            .all()
        )

    @staticmethod
    def for_user(user_id: int) -> list[PrivateBetaObservation]:
        return list(
            PrivateBetaObservation.query.filter_by(user_id=user_id)
            .order_by(PrivateBetaObservation.observed_at.desc())
            .all()
        )
