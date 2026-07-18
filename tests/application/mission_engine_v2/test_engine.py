"""MissionEngineV2 facade tests."""

from __future__ import annotations

from datetime import timedelta

import pytest

from app.application.mission_engine_v2.exceptions import (
    ActiveMissionExists,
    InvalidMissionState,
    MissionAlreadyArchived,
    MissionAlreadyCompleted,
    MissionNotFound,
)
from app.application.mission_engine_v2.lifecycle import MissionSlot, MissionState
from tests.application.mission_engine_v2.helpers import (
    NOW,
    TODAY,
    make_engine,
    make_mission,
    make_snapshot,
)


def test_engine_id_and_version():
    engine = make_engine()
    assert engine.engine_id == "v2"
    assert engine.engine_version == "2.0.0"


def test_is_available():
    engine = make_engine(available=True)
    assert engine.is_available() is True
    engine.set_available(False)
    assert engine.is_available() is False


def test_generate_today_mission():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    assert mission.mission_id.startswith("mission-")
    assert mission in engine.all_missions()


def test_generate_deferred_mission():
    engine = make_engine()
    mission = engine.generate_deferred_mission("journey-1", as_of_date=TODAY)
    assert mission.slot == MissionSlot.DEFERRED


def test_generate_future_mission():
    engine = make_engine()
    mission = engine.generate_future_mission("journey-1", as_of_date=TODAY, days_ahead=3)  # noqa: E501
    assert mission.slot == MissionSlot.FUTURE


def test_schedule_revision_mission():
    engine = make_engine()
    mission = engine.schedule_revision_mission("journey-1", as_of_date=TODAY)
    assert mission.is_revision is True


def test_prepare_mission():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    planned = engine._factory.with_state(mission, MissionState.PLANNED)
    engine._missions[planned.mission_id] = planned
    ready = engine.prepare_mission(planned.mission_id)
    assert ready.state == MissionState.READY


def test_activate_mission():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    active = engine.activate_mission(mission.mission_id)
    assert active.state == MissionState.ACTIVE


def test_activate_second_mission_raises():
    engine = make_engine()
    m1 = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(m1.mission_id)
    m2 = make_mission(
        mission_id="mission-2",
        session_id="sess-2",
        state=MissionState.READY,
    )
    engine._missions[m2.mission_id] = m2
    with pytest.raises(ActiveMissionExists):
        engine.activate_mission(m2.mission_id)


def test_pause_and_resume():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    paused = engine.pause_mission_by_id(mission.mission_id)
    assert paused.state == MissionState.PAUSED
    resumed = engine.resume_mission_by_id(mission.mission_id)
    assert resumed.state == MissionState.ACTIVE
    assert resumed.is_resume is True


def test_complete_mission():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    completed = engine.complete_mission(mission.mission_id)
    assert completed.state == MissionState.COMPLETED
    assert completed.completed_at == NOW


def test_complete_already_completed_raises():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    engine.complete_mission(mission.mission_id)
    with pytest.raises(MissionAlreadyCompleted):
        engine.complete_mission(mission.mission_id)


def test_archive_mission_from_completed():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    engine.complete_mission(mission.mission_id)
    archived = engine.archive_mission_by_id(mission.mission_id)
    assert archived.state == MissionState.ARCHIVED
    assert archived.archived_at == NOW
    assert mission.mission_id not in engine._missions


def test_archive_active_auto_completes():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    archived = engine.archive_mission_by_id(mission.mission_id)
    assert archived.state == MissionState.ARCHIVED


def test_archive_planned_raises():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    with pytest.raises(InvalidMissionState):
        engine.archive_mission_by_id(mission.mission_id)


def test_defer_mission():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    deferred = engine.defer_mission(mission.mission_id)
    assert deferred.slot == MissionSlot.DEFERRED


def test_reschedule_mission():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    new_date = TODAY + timedelta(days=2)
    rescheduled = engine.reschedule_mission(
        mission.mission_id,
        new_date=new_date,
        as_of_date=TODAY,
    )
    assert rescheduled.scheduled_date == new_date


def test_get_timeline_and_today():
    engine = make_engine()
    engine.generate_today_mission("journey-1", as_of_date=TODAY)
    timeline = engine.get_timeline("learner-1", as_of_date=TODAY)
    today = engine.get_today_mission("learner-1", as_of_date=TODAY)
    assert timeline.today is not None
    assert today is not None
    assert timeline.today.mission_id == today.mission_id


def test_get_dashboard():
    engine = make_engine()
    engine.generate_today_mission("journey-1", as_of_date=TODAY)
    dashboard = engine.get_dashboard("learner-1", as_of_date=TODAY)
    assert dashboard.today is not None
    assert dashboard.open_mission_count >= 1


def test_summarize():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    card = engine.summarize(mission.mission_id)
    assert card.mission_id == mission.mission_id


def test_deliver():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    execution = engine.deliver(mission.mission_id)
    assert execution.mission_id == mission.mission_id


def test_orchestrate():
    engine = make_engine()
    timeline, card = engine.orchestrate("journey-1", as_of_date=TODAY)
    assert timeline.today is not None
    assert card is not None


def test_get_mission_not_found():
    engine = make_engine()
    with pytest.raises(MissionNotFound):
        engine.get_mission("missing")


def test_missions_for_learner_scoped():
    engine = make_engine()
    engine.generate_today_mission("journey-1", as_of_date=TODAY)
    missions = engine.missions_for_learner("learner-1")
    assert len(missions) == 1
    assert engine.missions_for_learner("other") == ()


def test_archived_missions_retrieval():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    engine.archive_mission_by_id(mission.mission_id)
    archived = engine.archived_missions(learner_id="learner-1")
    assert len(archived) == 1


def test_get_mission_from_archive():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    engine.archive_mission_by_id(mission.mission_id)
    fetched = engine.get_mission(mission.mission_id)
    assert fetched.state == MissionState.ARCHIVED


def test_archive_already_archived_raises():
    engine = make_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    engine.archive_mission_by_id(mission.mission_id)
    with pytest.raises(MissionAlreadyArchived):
        engine.archive_mission_by_id(mission.mission_id)


def test_generate_with_explicit_snapshot():
    engine = make_engine()
    snap = make_snapshot()
    mission = engine.generate_today_mission(
        "journey-1",
        as_of_date=TODAY,
        snapshot=snap,
    )
    assert mission.journey_id == snap.journey_id


def test_timeline_refresh_missed():
    engine = make_engine()
    past = make_mission(
        mission_id="past",
        scheduled_date=TODAY - timedelta(days=1),
        slot=MissionSlot.TODAY,
        state=MissionState.READY,
    )
    engine._missions[past.mission_id] = past
    timeline = engine.get_timeline("learner-1", as_of_date=TODAY, refresh_missed=True)
    assert any(m.slot == MissionSlot.MISSED for m in timeline.ordered)
