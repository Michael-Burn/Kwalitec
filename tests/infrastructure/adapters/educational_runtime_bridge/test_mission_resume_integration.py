"""Integration tests — Experience → Mission Resume Adapter → Runtime A → SQL."""

from __future__ import annotations

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.student_experience.exceptions import StudentExperienceError
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_STUDY_SESSION_SERVICE,
    INVALID_STATE,
    MISSION_RESUME_BRIDGE_SUCCESS,
    NO_ACTIVE_PLAN,
    MissionResumeAdapter,
)
from app.infrastructure.adapters.mission.experience_adapter import (
    ExperienceMissionAdapter,
)
from app.infrastructure.adapters.student_experience.composition import (
    StudentExperienceComposition,
    build_production_experience,
)
from app.infrastructure.adapters.student_experience.defaults import (
    seeded_demo_mission,
)
from app.infrastructure.events.registry import EventRegistry
from app.models.mission import Mission
from app.services.mission_service import MissionService
from app.services.study_session_service import StudySessionService
from tests.conftest import _make_mission, _make_study_plan, _make_subject, _make_user


@pytest.fixture
def learner(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    return user, subject, plan, mission


def test_adapter_resumes_sql_in_progress_mission(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    events = EventRegistry()
    adapter = MissionResumeAdapter(events=events)
    result = adapter.resume_session(str(user.id), session_id=str(mission.id))
    assert result.ok is True
    assert result.value is not None
    assert result.value["mission_id"] == str(mission.id)
    assert result.value["session_id"] == str(mission.id)
    assert result.value["topic_title"] == mission.title
    assert result.value["status"] == "in_progress"
    assert result.value["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert result.value["resumed"] is True
    refreshed = Mission.query.get(mission.id)
    assert refreshed is not None
    assert refreshed.status == "In Progress"
    assert refreshed.id == mission.id
    assert any(
        e.event_type == MISSION_RESUME_BRIDGE_SUCCESS for e in events.published()
    )


def test_adapter_locates_today_active_without_session_id(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    result = MissionResumeAdapter().resume_session(str(user.id))
    assert result.ok is True
    assert result.value["mission_id"] == str(mission.id)
    assert Mission.query.get(mission.id).status == "In Progress"


def test_adapter_does_not_create_session_for_pending(learner):
    user, _subject, _plan, mission = learner
    assert mission.status == "Pending"
    result = MissionResumeAdapter().resume_session(
        str(user.id), session_id=str(mission.id)
    )
    assert result.ok is False
    assert result.error_code == INVALID_STATE
    assert Mission.query.get(mission.id).status == "Pending"


def test_experience_adapter_uses_resume_bridge(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    experience = ExperienceMissionAdapter(mission_resume=MissionResumeAdapter())
    resumed = experience.resume_session(
        str(user.id), session_id=str(mission.id)
    )
    assert resumed["mission_id"] == str(mission.id)
    assert resumed["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert resumed["topic_title"] != "Core methods"
    assert Mission.query.get(mission.id).status == "In Progress"


def test_experience_get_session_status_via_resume_bridge(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    experience = ExperienceMissionAdapter(mission_resume=MissionResumeAdapter())
    status = experience.get_session_status(
        str(user.id), session_id=str(mission.id)
    )
    assert status is not None
    assert status["mission_id"] == str(mission.id)
    assert status["status"] == "in_progress"


def test_experience_bridge_no_demo_fallback_when_no_plan(ctx, db):
    user = _make_user()
    experience = ExperienceMissionAdapter(
        mission_resume=MissionResumeAdapter(), auto_provision=True
    )
    with pytest.raises(StudentExperienceError) as exc:
        experience.resume_session(str(user.id))
    assert NO_ACTIVE_PLAN in str(exc.value)
    demo = seeded_demo_mission(str(user.id))
    assert demo["todays_session"]["mission_id"] == "m1"


def test_composition_flag_off_preserves_opaque_resume(ctx, db):
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_MISSION_RESUME_BRIDGE is False
    composition = StudentExperienceComposition(seed_demo_learners=True)
    assert composition._mission_resume is None
    composition.seed_learner("42", demo=True)
    # Opaque path resumes from seeded projection when status is in_progress.
    composition.mission.put_projection(
        "42",
        {
            "student_id": "42",
            "todays_session": {
                "mission_id": "m1",
                "session_id": "sess-1",
                "status": "in_progress",
                "topic_title": "Core methods",
            },
            "sessions": {
                "sess-1": {
                    "mission_id": "m1",
                    "session_id": "sess-1",
                    "status": "in_progress",
                }
            },
        },
    )
    resumed = composition.mission.resume_session("42", session_id="sess-1")
    assert resumed["status"] == "in_progress"
    assert Mission.query.filter_by(user_id=42).count() == 0


def test_composition_flag_on_wires_resume_bridge(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_MISSION_RESUME_BRIDGE": "1"}
    )
    assert flags.ENABLE_MISSION_RESUME_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False
    composition, _service = build_production_experience(flags=flags)
    assert composition._mission_resume is not None
    resumed = composition.mission.resume_session(
        str(user.id), session_id=str(mission.id)
    )
    assert resumed["mission_id"] == str(mission.id)
    assert resumed["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    demo = seeded_demo_mission(str(user.id))
    assert resumed["mission_id"] != demo["todays_session"]["mission_id"]


def test_start_then_resume_preserves_identities(learner):
    user, _subject, _plan, mission = learner
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_MISSION_START_BRIDGE": "1",
            "KWALITEC_MISSION_RESUME_BRIDGE": "1",
        }
    )
    composition, _service = build_production_experience(flags=flags)
    started = composition.mission.start_session(
        str(user.id), mission_id=str(mission.id)
    )
    resumed = composition.mission.resume_session(
        str(user.id), session_id=str(mission.id)
    )
    assert started["mission_id"] == resumed["mission_id"] == str(mission.id)
    assert started["session_id"] == resumed["session_id"] == str(mission.id)
    assert Mission.query.get(mission.id).status == "In Progress"


def test_umbrella_flag_enables_resume_bridge(learner):
    user, _subject, _plan, mission = learner
    StudySessionService.start_session(mission.id, user.id)
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE": "1"}
    )
    assert flags.ENABLE_MISSION_READ_BRIDGE is True
    assert flags.ENABLE_MISSION_START_BRIDGE is True
    assert flags.ENABLE_MISSION_RESUME_BRIDGE is True
    composition, _ = build_production_experience(flags=flags)
    assert composition._mission_resume is not None
    resumed = composition.mission.resume_session(
        str(user.id), session_id=str(mission.id)
    )
    assert resumed["mission_id"] == str(mission.id)


def test_behavioural_parity_with_legacy_resume(learner):
    """Resume preserves the same identities as StudySessionService ownership."""
    user, _subject, _plan, mission = learner
    legacy = StudySessionService.start_session(mission.id, user.id)
    assert legacy.status == "In Progress"
    owned = StudySessionService.get_owned_mission(mission.id, user.id)
    assert owned.id == legacy.id
    assert owned.title == legacy.title

    resume = MissionResumeAdapter().resume_session(
        str(user.id), session_id=str(mission.id)
    )
    assert resume.ok is True
    assert resume.value is not None
    assert resume.value["mission_id"] == str(owned.id)
    assert resume.value["session_id"] == str(owned.id)
    assert resume.value["topic_title"] == owned.title
    bridged = Mission.query.get(mission.id)
    assert bridged is not None
    assert bridged.id == owned.id
    assert bridged.status == owned.status
    assert bridged.title == owned.title
    assert bridged.user_id == user.id

    # Resume must not invent a second mission or flip Pending→In Progress again.
    assert Mission.query.filter_by(user_id=user.id).count() == 1
    today = MissionService.get_today_mission(user.id)
    assert today is not None
    assert today.id == mission.id
