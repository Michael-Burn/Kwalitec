"""Integration tests — Experience → Mission Start Adapter → Runtime A → SQL."""

from __future__ import annotations

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.student_experience.exceptions import StudentExperienceError
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_STUDY_SESSION_SERVICE,
    MISSION_START_BRIDGE_SUCCESS,
    NO_ACTIVE_PLAN,
    MissionReadAdapter,
    MissionStartAdapter,
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
from app.services.planning_service import PlanningService
from app.services.study_session_service import StudySessionService
from tests.conftest import _make_mission, _make_study_plan, _make_subject, _make_user


@pytest.fixture
def learner(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    return user, subject, plan, mission


def test_adapter_starts_sql_mission(learner):
    user, _subject, _plan, mission = learner
    events = EventRegistry()
    adapter = MissionStartAdapter(events=events)
    result = adapter.start_session(str(user.id), mission_id=str(mission.id))
    assert result.ok is True
    assert result.value is not None
    assert result.value["mission_id"] == str(mission.id)
    assert result.value["topic_title"] == mission.title
    assert result.value["status"] == "in_progress"
    assert result.value["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    refreshed = Mission.query.get(mission.id)
    assert refreshed is not None
    assert refreshed.status == "In Progress"
    assert any(e.event_type == MISSION_START_BRIDGE_SUCCESS for e in events.published())


def test_adapter_ensure_today_then_start(learner):
    user, _subject, _plan, mission = learner
    result = MissionStartAdapter().start_session(str(user.id))
    assert result.ok is True
    assert result.value["mission_id"] == str(mission.id)
    assert Mission.query.get(mission.id).status == "In Progress"


def test_adapter_idempotent_double_start(learner):
    user, _subject, _plan, mission = learner
    adapter = MissionStartAdapter()
    first = adapter.start_session(str(user.id), mission_id=str(mission.id))
    second = adapter.start_session(str(user.id), mission_id=str(mission.id))
    assert first.ok is True
    assert second.ok is True
    assert first.value["mission_id"] == second.value["mission_id"]
    assert Mission.query.get(mission.id).status == "In Progress"


def test_experience_adapter_uses_start_bridge(learner):
    user, _subject, _plan, mission = learner
    experience = ExperienceMissionAdapter(mission_start=MissionStartAdapter())
    started = experience.start_session(str(user.id), mission_id=str(mission.id))
    assert started["mission_id"] == str(mission.id)
    assert started["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert started["topic_title"] != "Core methods"
    assert Mission.query.get(mission.id).status == "In Progress"


def test_experience_bridge_no_demo_fallback_when_no_plan(ctx, db):
    user = _make_user()
    experience = ExperienceMissionAdapter(
        mission_start=MissionStartAdapter(), auto_provision=True
    )
    with pytest.raises(StudentExperienceError) as exc:
        experience.start_session(str(user.id))
    assert NO_ACTIVE_PLAN in str(exc.value)
    demo = seeded_demo_mission(str(user.id))
    assert demo["todays_session"]["mission_id"] == "m1"


def test_composition_flag_off_preserves_opaque_start(ctx, db):
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_MISSION_START_BRIDGE is False
    composition = StudentExperienceComposition(seed_demo_learners=True)
    assert composition._mission_start is None
    composition.seed_learner("42", demo=True)
    started = composition.mission.start_session("42")
    assert started["status"] == "in_progress"
    assert started["mission_id"]
    # Opaque path does not touch SQL Mission rows for learner "42".
    assert Mission.query.filter_by(user_id=42).count() == 0


def test_composition_flag_on_wires_start_bridge(learner):
    user, _subject, _plan, mission = learner
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_MISSION_START_BRIDGE": "1"}
    )
    assert flags.ENABLE_MISSION_START_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False
    composition, _service = build_production_experience(flags=flags)
    assert composition._mission_start is not None
    started = composition.mission.start_session(
        str(user.id), mission_id=str(mission.id)
    )
    assert started["mission_id"] == str(mission.id)
    assert started["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    demo = seeded_demo_mission(str(user.id))
    assert started["mission_id"] != demo["todays_session"]["mission_id"]


def test_read_plus_start_bridges_together(learner):
    user, _subject, _plan, mission = learner
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_MISSION_READ_BRIDGE": "1",
            "KWALITEC_MISSION_START_BRIDGE": "1",
        }
    )
    composition, _service = build_production_experience(flags=flags)
    session = composition.mission.get_todays_session(str(user.id))
    assert session is not None
    assert session["mission_id"] == str(mission.id)
    started = composition.mission.start_session(str(user.id))
    assert started["mission_id"] == str(mission.id)
    assert Mission.query.get(mission.id).status == "In Progress"


def test_umbrella_flag_enables_start_bridge(learner):
    user, _subject, _plan, mission = learner
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE": "1"}
    )
    assert flags.ENABLE_MISSION_READ_BRIDGE is True
    assert flags.ENABLE_MISSION_START_BRIDGE is True
    assert flags.ENABLE_MISSION_RESUME_BRIDGE is True
    composition, _ = build_production_experience(flags=flags)
    assert composition._mission_read is not None
    assert composition._mission_start is not None
    assert composition._mission_resume is not None
    started = composition.mission.start_session(
        str(user.id), mission_id=str(mission.id)
    )
    assert started["mission_id"] == str(mission.id)


def test_behavioural_parity_with_legacy_start(learner):
    """Mission Read + Start outcomes match Planning + StudySession legacy path."""
    user, _subject, _plan, mission = learner

    sql_before = MissionService.get_today_mission(user.id)
    assert sql_before is not None
    assert sql_before.id == mission.id
    read = MissionReadAdapter().get_todays_session(str(user.id))
    assert read.ok is True
    assert read.value is not None
    assert read.value["mission_id"] == str(sql_before.id)
    assert read.value["topic_title"] == sql_before.title

    legacy_mission = PlanningService.generate_today_mission(user.id)
    assert legacy_mission is not None
    assert legacy_mission.id == mission.id
    legacy_started = StudySessionService.start_session(mission.id, user.id)
    assert legacy_started.status == "In Progress"
    assert legacy_started.title == mission.title

    # Reset so the bridged start path exercises the same Pending → In Progress
    # transition against identical educational inputs.
    MissionService.update_mission_status(
        mission_id=mission.id, user_id=user.id, status="Pending"
    )
    assert Mission.query.get(mission.id).status == "Pending"

    start = MissionStartAdapter().start_session(str(user.id))
    assert start.ok is True
    assert start.value is not None
    assert start.value["mission_id"] == str(legacy_started.id)
    assert start.value["topic_title"] == legacy_started.title
    bridged = Mission.query.get(mission.id)
    assert bridged is not None
    assert bridged.status == legacy_started.status
    assert bridged.title == legacy_started.title
