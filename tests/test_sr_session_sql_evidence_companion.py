"""SQL evidence companion — Phase 1 Accept binding + Phase 2 write-through.

Phase 1: flag-gated Accept-time companion Mission creation.
Phase 2: Session completion aggregates scored practice → StudyAttempt on
the companion via ``record_practice_outcome`` (no Phase 3 topic resolver).
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_experience import EducationalExperienceService
from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.student_runtime import StudentRuntimeCoordinator
from app.application.student_runtime.evidence_companion import (
    is_sql_evidence_companion_mission,
)
from app.application.student_runtime.evidence_write_through import (
    ScoredPracticeCounts,
    aggregate_scored_practice_responses,
    load_sitting_response_items,
    optional_sql_topic_id,
)
from app.extensions import db
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    LearningSessionRuntimeEngine,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.models.educational_runtime_engine import RuntimeMissionInstance
from app.models.learning import StudyAttempt
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
        "SR_EVIDENCE_GATE": "0",
        "SR_TWIN_DAILY_LOOP": "0",
        "SR_SESSION_COMPLETION_PRODUCT": "0",
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


def _coordinator(*, companion: bool, store: SessionDocumentStore | None = None):
    persistence = LearningSessionPersistenceAdapter(
        store=store or SessionDocumentStore()
    )
    return StudentRuntimeCoordinator(
        persistence=persistence,
        flags=_flags(companion=companion),
    ), persistence


def _seed_scored_practice(
    store: SessionDocumentStore,
    *,
    student_id: str,
    session_id: str,
    outcomes: list[bool | None],
) -> None:
    """Persist activity.responses items with scored practice outcomes."""
    items = []
    for index, scored in enumerate(outcomes):
        items.append(
            {
                "activity_id": f"act-practice-{index}",
                "stage": "practice",
                "response": f"answer-{index}",
                "scored_correct": scored,
            }
        )
    # Non-practice / unscored noise that aggregation must ignore.
    items.append(
        {
            "activity_id": "act-read-1",
            "stage": "read",
            "response": "noted",
            "scored_correct": None,
        }
    )
    key = PackageActivityEngine._key(student_id, session_id)
    store.save(
        PackageActivityEngine.NS_RESPONSES,
        key,
        {
            "student_id": student_id,
            "session_id": session_id,
            "items": items,
        },
    )


def _complete_sitting(
    persistence: LearningSessionPersistenceAdapter,
    *,
    student_id: str,
    session_id: str,
    finish_verdict: str = "partially",
):
    engine = LearningSessionRuntimeEngine(
        runtime=LearningSessionRuntime(),
        persistence=persistence,
    )
    return engine.complete_session_opaque(
        student_id,
        session_id=session_id,
        finish_verdict=finish_verdict,
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


class TestPracticeAggregationHelper:
    def test_counts_only_scored_practice(self):
        counts = aggregate_scored_practice_responses(
            [
                {"stage": "read", "scored_correct": True},
                {"stage": "practice", "scored_correct": True},
                {"stage": "practice", "scored_correct": False},
                {"stage": "practice", "scored_correct": None},
                {"stage": "worked_example", "scored_correct": False},
            ]
        )
        assert counts == ScoredPracticeCounts(
            questions_attempted=2, questions_correct=1
        )

    def test_optional_sql_topic_id_does_not_resolve_codes(self):
        assert optional_sql_topic_id(42) == 42
        assert optional_sql_topic_id("7") == 7
        assert optional_sql_topic_id("topic-cash") is None
        assert optional_sql_topic_id(None) is None


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
        coordinator, _ = _coordinator(companion=True)
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

        coordinator, _ = _coordinator(companion=True)
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
        coordinator, _ = _coordinator(companion=False)
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

        coordinator, _ = _coordinator(companion=True)
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

        coordinator, _ = _coordinator(companion=True)
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


@pytest.mark.usefixtures("ctx")
class TestEvidenceCompanionWriteThrough:
    def test_flag_on_writes_study_attempt_with_aggregated_counts(self, monkeypatch):
        monkeypatch.setenv("SR_SESSION_SQL_EVIDENCE_COMPANION", "1")
        monkeypatch.setenv("KWALITEC_COMMERCIAL_LOOP", "0")
        monkeypatch.setenv("SR_EVIDENCE_GATE", "0")
        monkeypatch.setenv("SR_TWIN_DAILY_LOOP", "0")
        monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "0")

        subject = publish_subject("ECMP6", title="Write Through On")
        user = make_user("ecmp-write@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None

        store = SessionDocumentStore()
        coordinator, persistence = _coordinator(companion=True, store=store)
        binding = coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
        )
        row = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=snap.mission.mission_instance_id
        ).one()
        companion_id = row.sql_mission_id
        assert companion_id is not None

        _seed_scored_practice(
            store,
            student_id=str(user.id),
            session_id=binding.session_id,
            outcomes=[True, False, True],
        )
        loaded = load_sitting_response_items(
            store, student_id=str(user.id), session_id=binding.session_id
        )
        assert aggregate_scored_practice_responses(loaded).questions_attempted == 3

        before = StudyAttempt.query.filter_by(mission_id=companion_id).count()
        result = _complete_sitting(
            persistence,
            student_id=str(user.id),
            session_id=binding.session_id,
            finish_verdict="no",
        )
        assert result is not None
        assert result["status"] == "completed"
        # Additive only — gate/Twin off ⇒ Runtime C mission/twin flags unchanged.
        assert result["mission_completed"] is False
        assert result["twin_updated"] is False
        assert result["sql_evidence_attempt_id"] is not None

        attempts = StudyAttempt.query.filter_by(
            user_id=user.id, mission_id=companion_id
        ).all()
        assert len(attempts) == before + 1
        attempt = attempts[-1]
        assert attempt.questions_attempted == 3
        assert attempt.questions_correct == 2
        assert attempt.topic_id is None  # curriculum code not SQL Topic.id yet
        companion = Mission.query.get(companion_id)
        assert companion is not None
        assert companion.status == "Completed"

    def test_flag_off_does_not_write_study_attempt(self, monkeypatch):
        monkeypatch.setenv("SR_SESSION_SQL_EVIDENCE_COMPANION", "0")
        monkeypatch.setenv("KWALITEC_COMMERCIAL_LOOP", "0")
        monkeypatch.setenv("SR_EVIDENCE_GATE", "0")
        monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "0")

        subject = publish_subject("ECMP7", title="Write Through Off")
        user = make_user("ecmp-write-off@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None

        store = SessionDocumentStore()
        # Accept with companion ON so a Mission exists, then complete with flag OFF.
        coordinator_on, persistence = _coordinator(companion=True, store=store)
        binding = coordinator_on.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
        )
        row = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=snap.mission.mission_instance_id
        ).one()
        companion_id = row.sql_mission_id
        assert companion_id is not None

        _seed_scored_practice(
            store,
            student_id=str(user.id),
            session_id=binding.session_id,
            outcomes=[True, True],
        )
        monkeypatch.setenv("SR_SESSION_SQL_EVIDENCE_COMPANION", "0")
        result = _complete_sitting(
            persistence,
            student_id=str(user.id),
            session_id=binding.session_id,
        )
        assert result is not None
        assert result.get("sql_evidence_attempt_id") is None
        assert (
            StudyAttempt.query.filter_by(mission_id=companion_id).count() == 0
        )

    def test_no_scored_practice_does_not_write(self, monkeypatch):
        monkeypatch.setenv("SR_SESSION_SQL_EVIDENCE_COMPANION", "1")
        monkeypatch.setenv("KWALITEC_COMMERCIAL_LOOP", "0")
        monkeypatch.setenv("SR_EVIDENCE_GATE", "0")
        monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "0")

        subject = publish_subject("ECMP8", title="No Scored Practice")
        user = make_user("ecmp-noscore@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None

        store = SessionDocumentStore()
        coordinator, persistence = _coordinator(companion=True, store=store)
        binding = coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
        )
        row = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=snap.mission.mission_instance_id
        ).one()
        companion_id = row.sql_mission_id

        _seed_scored_practice(
            store,
            student_id=str(user.id),
            session_id=binding.session_id,
            outcomes=[None, None],
        )
        result = _complete_sitting(
            persistence,
            student_id=str(user.id),
            session_id=binding.session_id,
            finish_verdict="yes",
        )
        assert result is not None
        assert result.get("sql_evidence_attempt_id") is None
        assert (
            StudyAttempt.query.filter_by(mission_id=companion_id).count() == 0
        )
        companion = Mission.query.get(companion_id)
        assert companion is not None
        assert companion.status == "In Progress"

    def test_write_through_is_idempotent_on_recomplete(self, monkeypatch):
        monkeypatch.setenv("SR_SESSION_SQL_EVIDENCE_COMPANION", "1")
        monkeypatch.setenv("KWALITEC_COMMERCIAL_LOOP", "0")
        monkeypatch.setenv("SR_EVIDENCE_GATE", "0")
        monkeypatch.setenv("SR_SESSION_COMPLETION_PRODUCT", "0")

        subject = publish_subject("ECMP9", title="Write Idempotent")
        user = make_user("ecmp-idem-write@example.com")
        _enrol_runtime_c(user, subject)
        snap = EducationalExperienceService().load_for_user(user.id)
        assert snap is not None and snap.mission is not None

        store = SessionDocumentStore()
        coordinator, persistence = _coordinator(companion=True, store=store)
        binding = coordinator.accept_and_start_session(
            user_id=user.id,
            mission_instance_id=snap.mission.mission_instance_id,
        )
        row = RuntimeMissionInstance.query.filter_by(
            mission_instance_id=snap.mission.mission_instance_id
        ).one()
        companion_id = row.sql_mission_id

        _seed_scored_practice(
            store,
            student_id=str(user.id),
            session_id=binding.session_id,
            outcomes=[True, False],
        )
        first = _complete_sitting(
            persistence,
            student_id=str(user.id),
            session_id=binding.session_id,
            finish_verdict="partially",
        )
        assert first is not None
        first_id = first.get("sql_evidence_attempt_id")
        assert first_id is not None
        assert (
            StudyAttempt.query.filter_by(mission_id=companion_id).count() == 1
        )

        second = _complete_sitting(
            persistence,
            student_id=str(user.id),
            session_id=binding.session_id,
            finish_verdict="yes",
        )
        assert second is not None
        assert second.get("sql_evidence_attempt_id") == first_id
        assert (
            StudyAttempt.query.filter_by(mission_id=companion_id).count() == 1
        )
        attempt = StudyAttempt.query.get(first_id)
        assert attempt is not None
        assert attempt.questions_attempted == 2
        assert attempt.questions_correct == 1
