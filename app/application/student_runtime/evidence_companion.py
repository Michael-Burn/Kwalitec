"""SQL evidence-companion Mission for Runtime C sittings (Phase 1).

Creates a Stage A ORM Mission row solely so StudyAttempt can hold a
``mission_id`` FK. Never selects topics, never drives Home Primary, and
must not be returned by ``MissionService.get_today_mission`` /
PlanningService orphan adoption.

Does not call ``PlanningService.generate_today_mission``.

Student-selected Study sittings have no daily RuntimeMissionInstance, so
this module also materialises a substrate RuntimeMissionInstance marked
with ``SQL_EVIDENCE_COMPANION_TEMPLATE_ID``. That row exists only to bind
``sql_mission_id`` and must be excluded from daily-mission / open-mission
lookups (see EducationalRuntimeEngineService filters).
"""

from __future__ import annotations

import logging
import uuid
from datetime import date

from app.application.educational_runtime_engine.dto import MissionInstanceSnapshot
from app.domain.educational_runtime_engine.state import (
    MissionStatus,
    PlanInstanceStatus,
)
from app.extensions import db
from app.models.educational_runtime_engine import (
    RuntimeEnrolment,
    RuntimeMissionInstance,
    RuntimeStudyPlanInstance,
)
from app.models.mission import Mission
from app.services.mission_service import MissionService

logger = logging.getLogger(__name__)

# Substrate RuntimeMissionInstance rows for student-selected sittings.
# Never selected as today's recommended mission; filter on this id.
SQL_EVIDENCE_COMPANION_TEMPLATE_ID = "sql_evidence_companion"
# Distinct from any real daily mission_date so the DB unique constraint
# (plan_instance_id, mission_date) is never shared with today's sitting.
SQL_EVIDENCE_COMPANION_MISSION_DATE = date(1, 1, 1)


def is_sql_evidence_companion_template(template_id: str | None) -> bool:
    """True when *template_id* marks an evidence-only substrate mission."""
    return (template_id or "").strip() == SQL_EVIDENCE_COMPANION_TEMPLATE_ID


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
    # Substrate rows use a sentinel mission_date for the unique (plan, date)
    # constraint; the SQL Mission itself is always dated for the sitting day.
    companion_date = (
        date.today()
        if is_sql_evidence_companion_template(runtime_mission.template_id)
        else runtime_mission.mission_date
    )
    subject_id = MissionService.get_or_create_default_subject(user_id)
    companion = MissionService.create_mission(
        user_id=user_id,
        subject_id=subject_id,
        mission_date=companion_date,
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


def ensure_student_selected_sql_evidence_substrate(
    *,
    user_id: int,
    curriculum_identity: str,
    topic_id: str,
    topic_code: str = "",
    title: str = "",
    mission_date: date | None = None,
) -> MissionInstanceSnapshot | None:
    """Create a substrate RuntimeMissionInstance for a student-selected sitting.

    The row is marked with ``SQL_EVIDENCE_COMPANION_TEMPLATE_ID`` so daily
    mission and journey open-mission queries never treat it as today's
    recommended sitting. Emits no educational events.

    ``mission_date`` is accepted for call-site clarity but the substrate row
    always uses ``SQL_EVIDENCE_COMPANION_MISSION_DATE`` so it never collides
    with the unique ``(plan_instance_id, mission_date)`` daily sitting row.

    Returns:
        Snapshot of the substrate mission, or ``None`` when enrolment/plan
        cannot be resolved (fail-open).
    """
    _ = mission_date  # call-site documentation only; see docstring.
    identity = (curriculum_identity or "").strip()
    tid = (topic_id or "").strip()
    if not identity or not tid:
        return None

    enrolment = RuntimeEnrolment.query.filter_by(
        user_id=user_id,
        curriculum_identity=identity,
    ).first()
    if enrolment is None:
        logger.warning(
            "evidence_companion_substrate_enrolment_missing user=%s identity=%s",
            user_id,
            identity,
        )
        return None

    plan = (
        RuntimeStudyPlanInstance.query.filter_by(
            enrolment_id=enrolment.enrolment_id,
            status=PlanInstanceStatus.ACTIVE.value,
        ).first()
        or RuntimeStudyPlanInstance.query.filter_by(
            enrolment_id=enrolment.enrolment_id,
        )
        .order_by(RuntimeStudyPlanInstance.id.desc())
        .first()
    )
    if plan is None:
        logger.warning(
            "evidence_companion_substrate_plan_missing user=%s enrolment=%s",
            user_id,
            enrolment.enrolment_id,
        )
        return None

    day = SQL_EVIDENCE_COMPANION_MISSION_DATE
    mid = f"msn_{uuid.uuid4().hex}"
    mission_title = (title or "").strip() or "Study session"
    row = RuntimeMissionInstance(
        mission_instance_id=mid,
        plan_instance_id=plan.plan_instance_id,
        user_id=user_id,
        curriculum_identity=identity,
        template_id=SQL_EVIDENCE_COMPANION_TEMPLATE_ID,
        topic_id=tid,
        topic_code=(topic_code or "").strip(),
        title=mission_title,
        task_descriptions_json="[]",
        mission_date=day,
        status=MissionStatus.ACCEPTED.value,
    )
    db.session.add(row)
    db.session.commit()
    logger.info(
        "evidence_companion_substrate_created mid=%s user=%s topic=%s",
        mid,
        user_id,
        tid,
    )
    return MissionInstanceSnapshot(
        mission_instance_id=row.mission_instance_id,
        plan_instance_id=row.plan_instance_id,
        user_id=row.user_id,
        curriculum_identity=row.curriculum_identity,
        template_id=row.template_id,
        topic_id=row.topic_id,
        topic_code=row.topic_code or "",
        title=row.title or "",
        task_descriptions=(),
        mission_date=row.mission_date,
        status=row.status,
        created_at=row.created_at,
        completed_at=row.completed_at,
    )
