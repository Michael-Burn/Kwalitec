"""First-session timing study for private beta (PB-001).

Measures hesitation as evidence: time from enrolment (or account creation)
to first mission, study session, Tutor use, and completion — plus drop-off.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import func

from app.extensions import db
from app.models.alpha_infrastructure import PresentationEvent
from app.models.learning import StudyAttempt
from app.models.mission import Mission
from app.models.private_beta import PrivateBetaParticipant
from app.models.user import User
from app.services.presentation_telemetry_service import (
    EVENT_KNOWLEDGE_MAP_OPENED,
    EVENT_MISSION_COMPLETED,
    EVENT_MISSION_STARTED,
    EVENT_TUTOR_OPENED,
    EVENT_TUTOR_QUESTION,
)

# Re-exported for metrics / dashboard consumers.
__all__ = [
    "EVENT_KNOWLEDGE_MAP_OPENED",
    "EVENT_TUTOR_OPENED",
    "EVENT_TUTOR_QUESTION",
    "FirstSessionTiming",
    "FirstSessionStudyService",
]


@dataclass(frozen=True)
class FirstSessionTiming:
    user_id: int
    email: str
    enrolled_at: datetime | None
    minutes_to_first_mission: float | None
    minutes_to_first_session: float | None
    minutes_to_first_tutor: float | None
    minutes_to_first_completion: float | None
    drop_off_location: str | None
    reached_mission: bool
    reached_session: bool
    reached_tutor: bool
    reached_completion: bool


def _minutes_between(start: datetime | None, end: datetime | None) -> float | None:
    if start is None or end is None:
        return None
    delta = end - start
    return round(delta.total_seconds() / 60.0, 1)


def _first_event_at(user_id: int, event_type: str) -> datetime | None:
    return (
        db.session.query(func.min(PresentationEvent.created_at))
        .filter(
            PresentationEvent.user_id == user_id,
            PresentationEvent.event_type == event_type,
        )
        .scalar()
    )


def _first_mission_started(user_id: int) -> datetime | None:
    at = _first_event_at(user_id, EVENT_MISSION_STARTED)
    if at is not None:
        return at
    return (
        db.session.query(func.min(Mission.created_at))
        .filter(
            Mission.user_id == user_id,
            Mission.status.in_(("In Progress", "Completed")),
        )
        .scalar()
    )


def _first_session_at(user_id: int) -> datetime | None:
    # StudyAttempt.study_date is a date; use created_at when present, else mission.
    row = (
        db.session.query(func.min(StudyAttempt.id))
        .filter(StudyAttempt.user_id == user_id)
        .scalar()
    )
    if row is None:
        return None
    attempt = db.session.get(StudyAttempt, row)
    if attempt is None:
        return None
    if attempt.mission_id:
        mission = db.session.get(Mission, attempt.mission_id)
    else:
        mission = None
    if mission is not None and mission.created_at is not None:
        return mission.created_at
    return _first_event_at(user_id, EVENT_MISSION_STARTED)


def _first_completion_at(user_id: int) -> datetime | None:
    at = _first_event_at(user_id, EVENT_MISSION_COMPLETED)
    if at is not None:
        return at
    return (
        db.session.query(func.min(Mission.created_at))
        .filter(Mission.user_id == user_id, Mission.status == "Completed")
        .scalar()
    )


def _drop_off(timing: FirstSessionTiming) -> str | None:
    if timing.reached_completion:
        return None
    if timing.reached_tutor and not timing.reached_completion:
        return "after_tutor"
    if timing.reached_session and not timing.reached_completion:
        return "after_session_start"
    if timing.reached_mission and not timing.reached_session:
        return "after_mission_start"
    if not timing.reached_mission:
        return "before_first_mission"
    return "unknown"


class FirstSessionStudyService:
    """Compute first-session timing evidence for enrolled beta users."""

    def for_user(self, user_id: int) -> FirstSessionTiming | None:
        participant = PrivateBetaParticipant.query.filter_by(user_id=user_id).first()
        user = db.session.get(User, user_id)
        if user is None:
            return None

        enrolled = participant.enrolled_at if participant else None
        if enrolled is None:
            # Fallback: earliest presentation event for non-enrolled diagnostics.
            enrolled = (
                db.session.query(func.min(PresentationEvent.created_at))
                .filter(PresentationEvent.user_id == user_id)
                .scalar()
            )
        mission_at = _first_mission_started(user_id)
        session_at = _first_session_at(user_id)
        tutor_at = _first_event_at(user_id, EVENT_TUTOR_OPENED) or _first_event_at(
            user_id, EVENT_TUTOR_QUESTION
        )
        completion_at = _first_completion_at(user_id)

        timing = FirstSessionTiming(
            user_id=user_id,
            email=str(user.email or ""),
            enrolled_at=enrolled,
            minutes_to_first_mission=_minutes_between(enrolled, mission_at),
            minutes_to_first_session=_minutes_between(enrolled, session_at),
            minutes_to_first_tutor=_minutes_between(enrolled, tutor_at),
            minutes_to_first_completion=_minutes_between(enrolled, completion_at),
            drop_off_location=None,
            reached_mission=mission_at is not None,
            reached_session=session_at is not None,
            reached_tutor=tutor_at is not None,
            reached_completion=completion_at is not None,
        )
        return FirstSessionTiming(
            user_id=timing.user_id,
            email=timing.email,
            enrolled_at=timing.enrolled_at,
            minutes_to_first_mission=timing.minutes_to_first_mission,
            minutes_to_first_session=timing.minutes_to_first_session,
            minutes_to_first_tutor=timing.minutes_to_first_tutor,
            minutes_to_first_completion=timing.minutes_to_first_completion,
            drop_off_location=_drop_off(timing),
            reached_mission=timing.reached_mission,
            reached_session=timing.reached_session,
            reached_tutor=timing.reached_tutor,
            reached_completion=timing.reached_completion,
        )

    def for_cohort(self) -> tuple[FirstSessionTiming, ...]:
        participants = (
            PrivateBetaParticipant.query.filter_by(is_active=True)
            .order_by(PrivateBetaParticipant.enrolled_at.asc())
            .all()
        )
        results: list[FirstSessionTiming] = []
        for p in participants:
            timing = self.for_user(p.user_id)
            if timing is not None:
                results.append(timing)
        return tuple(results)
