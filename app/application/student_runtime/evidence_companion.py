"""SQL evidence-companion Mission for Runtime C sittings (Phase 1).

Creates a Stage A ORM Mission row solely so StudyAttempt can hold a
``mission_id`` FK. Never selects topics, never drives Home Primary, and
must not be returned by ``MissionService.get_today_mission`` /
PlanningService orphan adoption.

Does not call ``PlanningService.generate_today_mission``.
"""

from __future__ import annotations

import logging

from app.application.educational_runtime_engine.dto import MissionInstanceSnapshot
from app.extensions import db
from app.models.educational_runtime_engine import RuntimeMissionInstance
from app.models.mission import Mission
from app.services.mission_service import MissionService

logger = logging.getLogger(__name__)


def is_sql_evidence_companion_mission(mission_id: int | None) -> bool:
    """True when *mission_id* is bound as a Runtime C evidence companion."""
    if mission_id is None:
        return False
    return (
        RuntimeMissionInstance.query.filter_by(sql_mission_id=int(mission_id))
        .first()
        is not None
    )


def ensure_sql_evidence_companion(
    *,
    user_id: int,
    runtime_mission: MissionInstanceSnapshot,
) -> Mission | None:
    """Get-or-create the SQL companion Mission for a Runtime C sitting.

    Idempotent: if ``RuntimeMissionInstance.sql_mission_id`` is already set
    and the Mission row exists, returns that Mission without creating another.

    Returns:
        The companion Mission, or ``None`` when the RuntimeMissionInstance
        row cannot be found (fail-open for coordinator resilience).
    """
    mid = (runtime_mission.mission_instance_id or "").strip()
    if not mid:
        return None

    row = RuntimeMissionInstance.query.filter_by(
        mission_instance_id=mid,
        user_id=user_id,
    ).first()
    if row is None:
        logger.warning(
            "evidence_companion_runtime_mission_missing mid=%s user=%s",
            mid,
            user_id,
        )
        return None

    if row.sql_mission_id is not None:
        existing = Mission.query.get(int(row.sql_mission_id))
        if existing is not None and int(existing.user_id) == int(user_id):
            return existing
        logger.warning(
            "evidence_companion_stale_sql_mission_id mid=%s sql_mission_id=%s",
            mid,
            row.sql_mission_id,
        )
        row.sql_mission_id = None
        db.session.flush()

    title = (runtime_mission.title or "").strip() or "Today's Study Session"
    subject_id = MissionService.get_or_create_default_subject(user_id)
    companion = MissionService.create_mission(
        user_id=user_id,
        subject_id=subject_id,
        mission_date=runtime_mission.mission_date,
        title=title,
        tasks=None,
        study_plan_id=None,
    )
    companion = MissionService.update_mission_status(
        companion.id, user_id, "In Progress"
    )
    row.sql_mission_id = int(companion.id)
    db.session.commit()
    logger.info(
        "evidence_companion_bound mid=%s sql_mission_id=%s user=%s",
        mid,
        companion.id,
        user_id,
    )
    return companion
