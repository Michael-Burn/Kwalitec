"""Phase 1 — SQL evidence-companion Mission at Accept (runtime identity).

Flag-gated Accept-time companion creation; no practice aggregation (Phase 2)
and no topic resolver (Phase 3).
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_experience import EducationalExperienceService
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.student_runtime import StudentRuntimeCoordinator
from app.application.student_runtime.evidence_companion import (
    is_sql_evidence_companion_mission,
)
from app.extensions import db
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.models.educational_runtime_engine import RuntimeMissionInstance
from app.models.mission import Mission
from app.models.user import User
from app.services.mission_service import MissionService
from app.services.planning_service import PlanningService
from app.services.study_plan_service import StudyPlanService
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)


def _flags(*, companion: bool, primary: bool = True):
    env = {
        "SR_SESSION_PRIMARY": "1" if primary else "0",
        "SR_SESSION_SQL_EVIDENCE_COMPANION": "1" if companion else "0",
        # Keep commercial-loop inheritance from affecting other SR_* flags.
        "KWALITEC_COMMERCIAL_LOOP": "0",
        "KWALITEC_V2_SOLE_RUNTIME": "0",
    }
    return resolve_v2_feature_flags(environ=env)


def _enrol_runtime_c(user: User, subject: str) -> None:
    bridge = FounderStudentEnrolmentBridge(flags=bridge_flags())
    result = bridge.enrol(
        user_id=user.id,
        category_code=PUBLISHED_CATEGORY_CODE,
        subject_code=subject,
        exam_date=date.today() + timedelta(days=120),
    )
    assert result.runtime_authority == "published_curriculum"


def _coordinator(*, companion: bool):
    persistence = LearningSessionPersistenceAdapter(store=SessionDocumentStore())
    return StudentRuntimeCoordinator(
        persistence=persistence,
        flags=_flags(companion=companion),
    )


class TestEvidenceCompanionFlag:
    def test_defaults_off_and_not_inherited_from_commercial_loop(self):
        bare = resolve_v2_feature_flags(environ={})
        assert bare.SR_SESSION_SQL_EVIDENCE_COMPANION is False

        loop_on = resolve_v2_feature_flags(
            environ={"KWALITEC_COMMERCIAL_LOOP": "1"}
        )
        assert loop_on.SR_SESSION_SQL_EVIDENCE_COMPANION is False
        assert loop_on.SR_SESSION_PRIMARY is True

        explicit = resolve_v2_feature_flags(
            environ={"SR_SESSION_SQL_EVIDENCE_COMPANION": "1"}
        )
        assert explicit.SR_SESSION_SQL_EVIDENCE_COMPANION is True


@pytest.mark.usefixtures("ctx")
class TestEvidenceCompanionAccept:
    def test_flag_on_creates_companion_and_stores_sql_mission_id(self):
        subject = publish_subject("ECMP1", title="Evidence Companion On")
        user = make_user("ecmp-on@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None
        mid = snap.mission.mission_instance_id

        before = Mission.query.filter_by(user_id=user.id).count()
        coordinator = _coordinator(companion=True)
        coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=mid,
            topic_title=snap.mission.topic_title,
        )

        row = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=mid, user_id=user.id
        ).one()
        assert row.sql_mission_id is not None
        companion = Mission.query.get(row.sql_mission_id)
        assert companion is not None
        assert companion.user_id == user.id
        assert companion.study_plan_id is None
        assert companion.status == "In Progress"
        assert (companion.title or "").strip()
        assert Mission.query.filter_by(user_id=user.id).count() == before + 1
        assert is_sql_evidence_companion_mission(companion.id)

    def test_flag_on_accept_is_idempotent(self):
        subject = publish_subject("ECMP2", title="Evidence Companion Idem")
        user = make_user("ecmp-idem@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None
        mid = snap.mission.mission_instance_id

        coordinator = _coordinator(companion=True)
        coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=mid,
        )
        row = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=mid
        ).one()
        first_id = row.sql_mission_id
        count_after_first = Mission.query.filter_by(user_id=user.id).count()

        # Resume path (open session exists) must not create another companion.
        coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=mid,
        )
        db.session.refresh(row)
        assert row.sql_mission_id == first_id
        assert Mission.query.filter_by(user_id=user.id).count() == count_after_first

    def test_flag_off_creates_no_companion(self):
        subject = publish_subject("ECMP3", title="Evidence Companion Off")
        user = make_user("ecmp-off@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None
        mid = snap.mission.mission_instance_id

        before = Mission.query.filter_by(user_id=user.id).count()
        coordinator = _coordinator(companion=False)
        coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=mid,
        )

        row = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=mid, user_id=user.id
        ).one()
        assert row.sql_mission_id is None
        assert Mission.query.filter_by(user_id=user.id).count() == before


@pytest.mark.usefixtures("ctx")
class TestEvidenceCompanionNotSurfacedAsTodaysMission:
    def test_get_today_mission_skips_companion_without_plan(self):
        subject = publish_subject("ECMP4", title="No Surfacing")
        user = make_user("ecmp-surface@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None

        coordinator = _coordinator(companion=True)
        coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
        )
        row = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=snap.mission.mission_instance_id
        ).one()
        assert row.sql_mission_id is not None

        # Runtime C students typically have no StudyPlan — unbound lookup must
        # not return the evidence companion as "today's mission".
        assert StudyPlanService.get_user_active_plan(user.id) is None
        todays = MissionService.get_today_mission(user.id)
        assert todays is None or todays.id != row.sql_mission_id
        assert not is_sql_evidence_companion_mission(
            todays.id if todays is not None else None
        )

    def test_orphan_adoption_skips_companion(self):
        subject = publish_subject("ECMP5", title="Orphan Skip")
        user = make_user("ecmp-orphan@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None

        coordinator = _coordinator(companion=True)
        coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
        )
        row = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=snap.mission.mission_instance_id
        ).one()
        companion_id = row.sql_mission_id
        assert companion_id is not None

        plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=90,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="Pass",
        )
        adopted = PlanningService._resolve_legacy_orphan_mission(
            user_id=user.id,
            today=date.today(),
            active_plan=plan,
        )
        assert adopted is None
        companion = Mission.query.get(companion_id)
        assert companion is not None
        assert companion.study_plan_id is None
