"""Deterministic regression scenarios for Mission Engine 2.0."""

from __future__ import annotations

import pytest

from app.application.mission_engine_v2.exceptions import (
    DuplicateMission,
    InvalidJourneyReference,
)
from app.application.mission_engine_v2.lifecycle import MissionSlot, MissionState
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from tests.application.mission_engine_v2.helpers import (
    TODAY,
    FakeJourneyEngine,
    make_engine,
    make_snapshot,
)


def _deterministic_engine():
    counter = {"n": 0}

    def ids():
        counter["n"] += 1
        return f"reg{counter['n']:03d}"

    journey = FakeJourneyEngine()
    return make_engine(journey=journey), journey


def test_same_inputs_same_mission_id():
    engine1, _ = _deterministic_engine()
    engine2, _ = _deterministic_engine()
    m1 = engine1.generate_today_mission("journey-1", as_of_date=TODAY)
    m2 = engine2.generate_today_mission("journey-1", as_of_date=TODAY)
    assert m1.mission_id == m2.mission_id
    assert m1.title == m2.title
    assert m1.slot == m2.slot


def test_orchestrate_deterministic():
    engine, _ = _deterministic_engine()
    t1, c1 = engine.orchestrate("journey-1", as_of_date=TODAY)
    engine2, _ = _deterministic_engine()
    t2, c2 = engine2.orchestrate("journey-1", as_of_date=TODAY)
    assert t1.today is not None and t2.today is not None
    assert t1.today.mission_id == t2.today.mission_id
    assert c1 is not None and c2 is not None
    assert c1.dispatch_action == c2.dispatch_action


def test_complete_mission_does_not_touch_journey():
    journey = FakeJourneyEngine()
    snap = make_snapshot()
    engine = make_engine(journey=journey)
    mission = engine.generate_today_mission(
        "journey-1",
        as_of_date=TODAY,
        snapshot=snap,
    )
    calls_before = list(journey.calls)
    engine.activate_mission(mission.mission_id)
    engine.complete_mission(mission.mission_id)
    assert journey.calls == calls_before


def test_mission_binds_single_session():
    engine, _ = _deterministic_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    assert mission.session_id == "sess-1"
    assert mission.topic_id == "topic-a"


def test_cannot_generate_for_terminal_journey():
    engine = make_engine()
    for state in (JourneyState.COMPLETED, JourneyState.ABANDONED, JourneyState.ARCHIVED):  # noqa: E501
        snap = make_snapshot(state=state)
        with pytest.raises(InvalidJourneyReference):
            engine.generate_today_mission("journey-1", as_of_date=TODAY, snapshot=snap)


def test_lifecycle_sequence_deterministic():
    engine, _ = _deterministic_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    mid = mission.mission_id
    engine.activate_mission(mid)
    engine.pause_mission_by_id(mid)
    engine.resume_mission_by_id(mid)
    completed = engine.complete_mission(mid)
    assert completed.state == MissionState.COMPLETED
    archived = engine.archive_mission_by_id(mid)
    assert archived.state == MissionState.ARCHIVED


def test_dashboard_stable_for_same_ledger():
    engine, _ = _deterministic_engine()
    engine.generate_today_mission("journey-1", as_of_date=TODAY)
    d1 = engine.get_dashboard("learner-1", as_of_date=TODAY)
    d2 = engine.get_dashboard("learner-1", as_of_date=TODAY)
    assert d1.open_mission_count == d2.open_mission_count
    assert d1.today.mission_id == d2.today.mission_id  # type: ignore[union-attr]


def test_defer_preserves_journey_reference():
    engine, _ = _deterministic_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    deferred = engine.defer_mission(mission.mission_id)
    assert deferred.journey_id == mission.journey_id
    assert deferred.session_id == mission.session_id


def test_timeline_order_stable():
    engine, _ = _deterministic_engine()
    engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.generate_deferred_mission("journey-1", as_of_date=TODAY)
    t1 = engine.get_timeline("learner-1", as_of_date=TODAY)
    t2 = engine.get_timeline("learner-1", as_of_date=TODAY)
    assert [m.mission_id for m in t1.ordered] == [m.mission_id for m in t2.ordered]


def test_revision_mission_flagged():
    engine, _ = _deterministic_engine()
    mission = engine.schedule_revision_mission("journey-1", as_of_date=TODAY)
    assert mission.is_revision is True
    assert mission.slot == MissionSlot.REVISION


def test_duplicate_generation_blocked_by_validator():
    counter = {"n": 0}

    def ids():
        counter["n"] += 1
        return f"dup{counter['n']:03d}"

    engine = make_engine()
    engine._id_factory = ids
    engine._factory._id_factory = ids
    engine.generate_today_mission("journey-1", as_of_date=TODAY)
    with pytest.raises(DuplicateMission):
        engine.generate_today_mission("journey-1", as_of_date=TODAY)


def test_archived_mission_removed_from_active_ledger():
    engine, _ = _deterministic_engine()
    mission = engine.generate_today_mission("journey-1", as_of_date=TODAY)
    engine.activate_mission(mission.mission_id)
    engine.archive_mission_by_id(mission.mission_id)
    assert mission.mission_id not in {m.mission_id for m in engine.all_missions()}
    assert len(engine.archived_missions()) == 1
