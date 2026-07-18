"""MissionEngine facade tests."""

from __future__ import annotations

from datetime import date

import pytest

from app.application.mission_engine.exceptions import (
    MissionAlreadyArchived,
    MissionAlreadyCompleted,
    MissionNotFound,
    WorkloadExceeded,
)
from app.application.mission_engine.mission_state import MissionSlot, MissionState
from tests.application.mission_engine.helpers import (
    TODAY,
    TOMORROW,
    active_journey,
    make_mission_engine,
)


def test_generate_today_and_get():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    assert engine.get_mission(mission.mission_id) == mission
    assert engine.get_today_mission("learner-1", as_of_date=TODAY) == mission


def test_generate_tomorrow():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_tomorrow_mission(journey, as_of_date=TODAY)
    assert mission.scheduled_date == TOMORROW
    assert mission.slot == MissionSlot.TOMORROW


def test_schedule_revision():
    counter = {"n": 0}

    def ids():
        counter["n"] += 1
        return f"id{counter['n']}"

    engine = make_mission_engine()
    engine._id_factory = ids  # type: ignore[attr-defined]
    engine._builder._id_factory = ids
    journey = active_journey()
    today = engine.generate_today_mission(journey, as_of_date=TODAY)
    rev = engine.schedule_revision_mission(journey, as_of_date=TODAY)
    assert today.state == MissionState.ACTIVE
    assert rev.is_revision is True


def test_start_defer_skip_reschedule():
    counter = {"n": 0}

    def ids():
        counter["n"] += 1
        return f"x{counter['n']}"

    engine = make_mission_engine()
    engine._id_factory = ids
    engine._builder._id_factory = ids
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    started = engine.start_mission(mission.mission_id)
    assert started.state == MissionState.IN_PROGRESS
    deferred = engine.defer_mission(started.mission_id)
    assert deferred.state == MissionState.DEFERRED
    rescheduled = engine.reschedule_mission(
        deferred.mission_id, new_date=TODAY, as_of_date=TODAY
    )
    assert rescheduled.state == MissionState.ACTIVE
    skipped = engine.skip_mission(rescheduled.mission_id)
    assert skipped.state == MissionState.SKIPPED


def test_complete_and_archive():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    completed = engine.complete_mission(mission.mission_id)
    assert completed.state == MissionState.COMPLETED
    archived = engine.archive_mission(completed.mission_id)
    assert archived.state == MissionState.ARCHIVED
    assert engine.archived_missions(learner_id="learner-1") == (archived,)
    assert engine.get_mission(archived.mission_id) == archived


def test_archive_active_completes_first():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    archived = engine.archive_mission(mission.mission_id)
    assert archived.state == MissionState.ARCHIVED


def test_complete_twice_fails():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.complete_mission(mission.mission_id)
    with pytest.raises(MissionAlreadyCompleted):
        engine.complete_mission(mission.mission_id)


def test_archive_twice_fails():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.archive_mission(mission.mission_id)
    with pytest.raises(MissionAlreadyArchived):
        engine.archive_mission(mission.mission_id)


def test_get_missing():
    engine = make_mission_engine()
    with pytest.raises(MissionNotFound):
        engine.get_mission("missing")


def test_second_today_fails():
    counter = {"n": 0}

    def ids():
        counter["n"] += 1
        return f"y{counter['n']}"

    engine = make_mission_engine()
    engine._id_factory = ids
    engine._builder._id_factory = ids
    journey = active_journey()
    engine.generate_today_mission(journey, as_of_date=TODAY)
    with pytest.raises(WorkloadExceeded):
        engine.generate_today_mission(journey, as_of_date=TODAY)


def test_get_schedule():
    counter = {"n": 0}

    def ids():
        counter["n"] += 1
        return f"sch{counter['n']}"

    engine = make_mission_engine()
    engine._id_factory = ids
    engine._builder._id_factory = ids
    journey = active_journey()
    engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.generate_tomorrow_mission(journey, as_of_date=TODAY)
    sched = engine.get_schedule("learner-1", as_of_date=TODAY)
    assert sched.today is not None
    assert sched.tomorrow is not None


def test_summarize_and_deliver():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    summary = engine.summarize(mission.mission_id)
    delivery = engine.deliver(mission.mission_id)
    assert summary.mission_id == mission.mission_id
    assert delivery.action.value == "today_mission"


def test_orchestrate():
    engine = make_mission_engine()
    journey = active_journey()
    schedule, summary = engine.orchestrate(journey, as_of_date=TODAY)
    assert schedule.today is not None
    assert summary is not None


def test_orchestrate_without_ensure():
    engine = make_mission_engine()
    journey = active_journey()
    schedule, summary = engine.orchestrate(
        journey, as_of_date=TODAY, ensure_today=False
    )
    assert schedule.today is None
    assert summary is None


def test_missions_for_learner_and_all():
    engine = make_mission_engine()
    journey = active_journey()
    engine.generate_today_mission(journey, as_of_date=TODAY)
    assert len(engine.missions_for_learner("learner-1")) == 1
    assert len(engine.all_missions()) == 1


def test_archived_by_journey():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.archive_mission(mission.mission_id)
    assert len(engine.archived_missions(journey_id="journey-1")) == 1
    assert len(engine.archived_missions()) == 1


def test_refresh_missed_via_schedule():
    from dataclasses import replace

    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    # backdate
    engine._missions[mission.mission_id] = replace(
        mission,
        scheduled_date=date(2026, 7, 10),
    )
    sched = engine.get_schedule("learner-1", as_of_date=TODAY)
    assert engine.get_mission(mission.mission_id).state == MissionState.MISSED
    # today empty after miss — schedule.today may be None
    assert sched.today is None or sched.today.state != MissionState.MISSED


def test_defer_with_target_date():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    deferred = engine.defer_mission(
        mission.mission_id, target_date=date(2026, 7, 25)
    )
    assert deferred.scheduled_date == date(2026, 7, 25)
    assert deferred.state == MissionState.DEFERRED
