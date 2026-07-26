"""Integration tests — Experience → Mission Read Adapter → MissionService → SQL."""

from __future__ import annotations

from datetime import date

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_PLANNING_SERVICE,
    MISSION_BRIDGE_SUCCESS,
    NO_ACTIVE_PLAN,
    MissionReadAdapter,
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
from app.services.mission_service import MissionService
from tests.conftest import _make_mission, _make_study_plan, _make_subject, _make_user


@pytest.fixture
def learner(ctx, db):
    user = _make_user()
    subject = _make_subject(user.id)
    plan = _make_study_plan(user.id)
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    return user, subject, plan, mission


def test_adapter_reads_sql_mission(learner):
    user, _subject, _plan, mission = learner
    events = EventRegistry()
    adapter = MissionReadAdapter(events=events)
    result = adapter.get_todays_session(str(user.id))
    assert result.ok is True
    assert result.value is not None
    assert result.value["mission_id"] == str(mission.id)
    assert result.value["topic_title"] == mission.title
    assert result.value["authority"] == AUTHORITY_PLANNING_SERVICE
    assert result.value["status"] == "ready"
    assert len(result.value["tasks"]) == 2
    assert any(e.event_type == MISSION_BRIDGE_SUCCESS for e in events.published())


def test_adapter_matches_mission_service(learner):
    user, _subject, _plan, mission = learner
    sql = MissionService.get_today_mission(user.id)
    assert sql is not None
    assert sql.id == mission.id
    bridged = MissionReadAdapter().get_todays_session(str(user.id))
    assert bridged.value["mission_id"] == str(sql.id)
    assert bridged.value["topic_title"] == sql.title


def test_experience_adapter_uses_bridge(learner):
    user, _subject, _plan, mission = learner
    bridge = MissionReadAdapter()
    experience = ExperienceMissionAdapter(mission_read=bridge)
    session = experience.get_todays_session(str(user.id))
    assert session is not None
    assert session["mission_id"] == str(mission.id)
    assert session["authority"] == AUTHORITY_PLANNING_SERVICE
    assert session["topic_title"] != "Core methods"


def test_experience_bridge_no_demo_fallback_when_no_mission(ctx, db):
    user = _make_user()
    bridge = MissionReadAdapter()
    experience = ExperienceMissionAdapter(mission_read=bridge, auto_provision=True)
    session = experience.get_todays_session(str(user.id))
    assert session is None
    result = bridge.get_todays_session(str(user.id))
    assert result.ok is True
    assert result.error_code == NO_ACTIVE_PLAN


def test_composition_flag_off_preserves_seed_path(ctx, db):
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_MISSION_READ_BRIDGE is False
    composition = StudentExperienceComposition(seed_demo_learners=True)
    assert composition._mission_read is None
    composition.seed_learner("42", demo=True)
    session = composition.mission.get_todays_session("42")
    assert session is not None
    assert session["topic_title"] == "Core methods"
    assert session["mission_id"] == "m1"


def test_composition_flag_on_wires_bridge_without_seeded_mission(learner):
    user, _subject, _plan, mission = learner
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_MISSION_READ_BRIDGE": "1"}
    )
    assert flags.ENABLE_MISSION_READ_BRIDGE is True
    assert flags.SEED_DEMO_LEARNERS is False
    composition, _service = build_production_experience(flags=flags)
    assert composition._mission_read is not None
    session = composition.mission.get_todays_session(str(user.id))
    assert session is not None
    assert session["mission_id"] == str(mission.id)
    assert session["authority"] == AUTHORITY_PLANNING_SERVICE
    demo = seeded_demo_mission(str(user.id))
    assert session["mission_id"] != demo["todays_session"]["mission_id"]


def test_flag_on_seed_learner_skips_demo_mission(ctx, db):
    user = _make_user()
    bridge = MissionReadAdapter()
    composition = StudentExperienceComposition(
        seed_demo_learners=True,
        mission_read=bridge,
    )
    composition.seed_learner(str(user.id), demo=True)
    # Twin/adaptive may be seeded; mission must come from Runtime A (none).
    assert composition.mission.get_todays_session(str(user.id)) is None
    stored = composition.store.get(composition.store.mission, str(user.id))
    assert stored is None or stored.get("authority") != "mission_engine"


def test_planning_service_topic_parity_when_mission_exists(learner):
    """Bridge changes data source only — topic equals SQL Mission title."""
    user, _subject, _plan, mission = learner
    from app.services.planning_service import PlanningService

    # Idempotent read of existing mission (no new educational decision).
    existing = PlanningService.generate_today_mission(user.id, today=date.today())
    # May return None if plan has no week window; fall back to MissionService.
    sql = existing or MissionService.get_today_mission(user.id)
    assert sql is not None
    bridged = MissionReadAdapter().get_todays_session(str(user.id)).value
    assert bridged["topic_title"] == sql.title
    assert bridged["mission_id"] == str(sql.id)
