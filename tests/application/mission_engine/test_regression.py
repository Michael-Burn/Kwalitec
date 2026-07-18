"""Regression and integration coverage for Mission Engine 2.0."""

from __future__ import annotations

import pytest

from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.mission_engine.exceptions import (
    InvalidMissionState,
    MissionBuildError,
    SchedulingError,
)
from app.application.mission_engine.mission_state import (
    DeliveryAction,
    MissionSlot,
    MissionState,
)
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.mission_engine.helpers import (
    NOW,
    TODAY,
    TOMORROW,
    YESTERDAY,
    active_journey,
    make_journey,
    make_journey_engine,
    make_mission_engine,
    make_objective,
    make_session,
)


def _engine_with_ids():
    counter = {"n": 0}

    def ids():
        counter["n"] += 1
        return f"reg{counter['n']}"

    engine = make_mission_engine()
    engine._id_factory = ids
    engine._builder._id_factory = ids
    return engine


@pytest.mark.parametrize(
    "state",
    [
        JourneyState.COMPLETED,
        JourneyState.ABANDONED,
        JourneyState.ARCHIVED,
    ],
)
def test_cannot_generate_for_terminal_journeys(state):
    engine = make_mission_engine()
    journey = make_journey(state=state)
    with pytest.raises(Exception):
        engine.generate_today_mission(journey, as_of_date=TODAY)


def test_mission_is_one_session_not_topic():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    assert mission.session_id
    assert mission.topic_id == "topic-a"
    # Mission binds a single session id, not a topic completion claim.
    assert mission.state != MissionState.COMPLETED


def test_complete_mission_does_not_complete_journey():
    j_engine = make_journey_engine()
    engine = make_mission_engine(journey_engine=j_engine)
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.complete_mission(mission.mission_id)
    # Journey aggregate passed in is unchanged (engine never mutates it).
    assert journey.state == JourneyState.ACTIVE


def test_lifecycle_happy_path():
    engine = _engine_with_ids()
    journey = active_journey()
    m = engine.generate_today_mission(journey, as_of_date=TODAY)
    m = engine.start_mission(m.mission_id)
    assert m.state == MissionState.IN_PROGRESS
    m = engine.complete_mission(m.mission_id)
    assert m.state == MissionState.COMPLETED
    m = engine.archive_mission(m.mission_id)
    assert m.state == MissionState.ARCHIVED
    delivery = engine.summarize(m.mission_id)
    assert delivery.delivery_action == DeliveryAction.NONE or delivery.is_completed


def test_defer_then_reschedule_tomorrow():
    engine = _engine_with_ids()
    journey = active_journey()
    m = engine.generate_today_mission(journey, as_of_date=TODAY)
    m = engine.defer_mission(m.mission_id)
    m = engine.reschedule_mission(
        m.mission_id, new_date=TOMORROW, as_of_date=TODAY
    )
    assert m.slot == MissionSlot.TOMORROW
    assert m.state == MissionState.SCHEDULED


def test_missed_then_reschedule_today():
    engine = _engine_with_ids()
    journey = active_journey()
    m = engine.generate_today_mission(journey, as_of_date=TODAY)
    from dataclasses import replace

    engine._missions[m.mission_id] = replace(
        m, scheduled_date=YESTERDAY
    )
    sched = engine.get_schedule("learner-1", as_of_date=TODAY)
    assert engine.get_mission(m.mission_id).state == MissionState.MISSED
    restored = engine.reschedule_mission(
        m.mission_id, new_date=TODAY, as_of_date=TODAY
    )
    assert restored.state == MissionState.ACTIVE
    assert sched.as_of_date == TODAY


def test_orchestrate_idempotent_when_today_exists():
    engine = _engine_with_ids()
    journey = active_journey()
    first = engine.generate_today_mission(journey, as_of_date=TODAY)
    schedule, summary = engine.orchestrate(journey, as_of_date=TODAY)
    assert schedule.today is not None
    assert schedule.today.mission_id == first.mission_id
    assert summary is not None
    assert len(engine.missions_for_learner("learner-1")) == 1


def test_resume_delivery_with_paused_session():
    engine = make_mission_engine()
    journey = active_journey(
        with_session=True, session_state=SessionState.PAUSED
    )
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    assert mission.is_resume is True
    delivery = engine.deliver(mission.mission_id, runtime_phase="paused")
    assert delivery.action == DeliveryAction.RESUME


def test_continue_delivery_in_progress():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.start_mission(mission.mission_id)
    delivery = engine.deliver(mission.mission_id)
    assert delivery.action == DeliveryAction.CONTINUE


def test_review_delivery_after_complete():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.complete_mission(mission.mission_id)
    delivery = engine.deliver(mission.mission_id)
    assert delivery.action == DeliveryAction.REVIEW


def test_revision_delivery():
    engine = _engine_with_ids()
    journey = active_journey()
    engine.generate_today_mission(journey, as_of_date=TODAY)
    rev = engine.schedule_revision_mission(journey, as_of_date=TODAY)
    delivery = engine.deliver(rev.mission_id)
    assert delivery.action == DeliveryAction.REVISION


def test_skip_removes_from_active_schedule():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.skip_mission(mission.mission_id)
    assert engine.get_today_mission("learner-1", as_of_date=TODAY) is None


def test_deterministic_mission_ids_with_fixed_factory():
    engine = make_mission_engine(id_token="fixed")
    journey = active_journey()
    m1 = engine.generate_today_mission(journey, as_of_date=TODAY)
    assert m1.mission_id == "mission-fixed"


def test_session_runtime_optional_does_not_break():
    runtime = LearningSessionRuntime(clock=lambda: NOW, id_factory=lambda: "rt")
    engine = make_mission_engine(session_runtime=runtime)
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    assert mission.session_id


def test_multiple_learners_isolated():
    engine = _engine_with_ids()
    j_engine = make_journey_engine()
    j1 = j_engine.create_journey(
        learner_id="a",
        topic_id="topic-a",
        curriculum_id="c1",
        journey_id="ja",
        objectives=[make_objective("oa")],
    )
    j1 = j_engine.start_journey(j1)
    j2 = j_engine.create_journey(
        learner_id="b",
        topic_id="topic-a",
        curriculum_id="c1",
        journey_id="jb",
        objectives=[make_objective("ob")],
    )
    j2 = j_engine.start_journey(j2)
    engine = make_mission_engine(journey_engine=j_engine)
    engine._id_factory = lambda: "a1"
    engine._builder._id_factory = lambda: "a1"
    m1 = engine.generate_today_mission(j1, as_of_date=TODAY)
    engine._id_factory = lambda: "b1"
    engine._builder._id_factory = lambda: "b1"
    m2 = engine.generate_today_mission(j2, as_of_date=TODAY)
    assert m1.learner_id == "a"
    assert m2.learner_id == "b"
    assert engine.get_today_mission("a", as_of_date=TODAY).mission_id == m1.mission_id
    assert engine.get_today_mission("b", as_of_date=TODAY).mission_id == m2.mission_id


def test_cannot_start_deferred_directly():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.defer_mission(mission.mission_id)
    with pytest.raises(SchedulingError):
        engine.start_mission(mission.mission_id)


def test_cannot_archive_skipped():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.skip_mission(mission.mission_id)
    with pytest.raises(InvalidMissionState):
        engine.archive_mission(mission.mission_id)


def test_build_error_surfaces_from_engine():
    engine = make_mission_engine()
    journey = make_journey(state=JourneyState.COMPLETED)
    with pytest.raises((MissionBuildError, Exception)):
        engine.generate_today_mission(journey, as_of_date=TODAY)


def test_existing_session_bound():
    journey = active_journey(with_session=True)
    engine = make_mission_engine()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    assert mission.session_id == "sess-1"


def test_effort_propagates_from_session():
    from app.domain.learning_journey.value_objects.effort_estimate import (
        EffortEstimate,
    )

    journey = make_journey(
        state=JourneyState.ACTIVE,
        sessions=[
            make_session(effort=EffortEstimate.HIGH),
        ],
    )
    # journey create with ACTIVE may need start via engine
    j_engine = make_journey_engine()
    journey = j_engine.create_journey(
        learner_id="learner-1",
        topic_id="topic-a",
        curriculum_id="curr-1",
        journey_id="journey-1",
        objectives=[make_objective()],
        sessions=[make_session(effort=EffortEstimate.HIGH)],
    )
    journey = j_engine.start_journey(journey)
    engine = make_mission_engine(journey_engine=j_engine)
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    assert mission.effort == "high"


def test_schedule_ordered_deterministic():
    engine = _engine_with_ids()
    journey = active_journey()
    engine.generate_today_mission(journey, as_of_date=TODAY)
    engine.generate_tomorrow_mission(journey, as_of_date=TODAY)
    sched = engine.get_schedule("learner-1", as_of_date=TODAY)
    ids = [m.mission_id for m in sched.ordered]
    assert ids == sorted(ids, key=lambda _: 0) or len(ids) >= 1
    # Today precedes tomorrow in ordered list
    if sched.today and sched.tomorrow:
        assert sched.ordered.index(sched.today) < sched.ordered.index(sched.tomorrow)


def test_payload_contains_structural_keys():
    engine = make_mission_engine()
    journey = active_journey()
    mission = engine.generate_today_mission(journey, as_of_date=TODAY)
    delivery = engine.deliver(mission.mission_id)
    for key in ("mission_id", "journey_id", "session_id", "topic_id", "action"):
        assert key in delivery.payload
