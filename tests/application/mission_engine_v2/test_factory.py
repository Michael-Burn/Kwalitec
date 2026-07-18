"""MissionFactory composition tests."""

from __future__ import annotations

from datetime import timedelta

import pytest

from app.application.mission_engine_v2.exceptions import (
    MissionFactoryError,
    TopicUnavailable,
)
from app.application.mission_engine_v2.lifecycle import MissionSlot, MissionState
from app.application.mission_engine_v2.mission_factory import MissionFactory
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from tests.application.mission_engine_v2.helpers import (
    NOW,
    TODAY,
    FakeJourneyEngine,
    FakeNavigation,
    FakeSessionRuntime,
    make_objective,
    make_recommendation,
    make_session_plan,
    make_snapshot,
)


def _factory(**kwargs) -> MissionFactory:
    defaults = {
        "journey_engine": FakeJourneyEngine(),
        "session_runtime": FakeSessionRuntime(),
        "navigation": FakeNavigation(),
        "clock": lambda: NOW,
        "id_factory": lambda: "fixedid001",
    }
    defaults.update(kwargs)
    return MissionFactory(**defaults)


def test_create_from_snapshot_basic():
    snap = make_snapshot()
    plan = make_session_plan()
    mission = _factory().create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        as_of_date=TODAY,
        session_plan=plan,
    )
    assert mission.learner_id == "learner-1"
    assert mission.journey_id == "journey-1"
    assert mission.session_id == "sess-1"
    assert mission.topic_id == "topic-a"
    assert mission.mission_id == "mission-fixedid001"


def test_create_from_snapshot_ready_for_today():
    snap = make_snapshot()
    plan = make_session_plan()
    mission = _factory().create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        as_of_date=TODAY,
        session_plan=plan,
    )
    assert mission.state == MissionState.READY
    assert mission.slot == MissionSlot.TODAY


def test_create_from_snapshot_future_slot():
    snap = make_snapshot()
    plan = make_session_plan()
    future = TODAY + timedelta(days=3)
    mission = _factory().create_from_snapshot(
        snap,
        scheduled_date=future,
        as_of_date=TODAY,
        session_plan=plan,
    )
    assert mission.slot == MissionSlot.FUTURE
    assert mission.state == MissionState.PLANNED


def test_create_from_snapshot_revision():
    snap = make_snapshot()
    plan = make_session_plan()
    mission = _factory().create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        as_of_date=TODAY,
        session_plan=plan,
        is_revision=True,
    )
    assert mission.is_revision is True
    assert mission.slot == MissionSlot.REVISION


def test_create_from_snapshot_deferred():
    snap = make_snapshot()
    plan = make_session_plan()
    mission = _factory().create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        as_of_date=TODAY,
        session_plan=plan,
        is_deferred=True,
    )
    assert mission.slot == MissionSlot.DEFERRED


def test_create_from_snapshot_explanation_keys():
    snap = make_snapshot()
    plan = make_session_plan()
    rec = make_recommendation(rationale_tags=("continuity", "session"))
    mission = _factory().create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        session_plan=plan,
        recommendation=rec,
    )
    assert mission.explanation_keys == ("continuity", "session")


def test_create_from_snapshot_no_plan_raises():
    snap = make_snapshot()
    with pytest.raises(MissionFactoryError, match="No session plan"):
        _factory(journey_engine=None).create_from_snapshot(
            snap,
            scheduled_date=TODAY,
        )


@pytest.mark.parametrize(
    "state",
    [JourneyState.COMPLETED, JourneyState.ABANDONED, JourneyState.ARCHIVED],
)
def test_create_from_snapshot_terminal_journey_raises(state):
    snap = make_snapshot(state=state)
    plan = make_session_plan()
    with pytest.raises(MissionFactoryError, match="Cannot build mission"):
        _factory().create_from_snapshot(
            snap,
            scheduled_date=TODAY,
            session_plan=plan,
        )


def test_create_from_snapshot_topic_unavailable():
    snap = make_snapshot(topic_id="missing-topic")
    plan = make_session_plan()
    nav = FakeNavigation(topics=("topic-a",))
    with pytest.raises(TopicUnavailable):
        _factory(navigation=nav).create_from_snapshot(
            snap,
            scheduled_date=TODAY,
            session_plan=plan,
        )


def test_create_from_journey_id():
    journey = FakeJourneyEngine()
    mission = _factory(journey_engine=journey).create_from_journey_id(
        "journey-1",
        scheduled_date=TODAY,
    )
    assert mission.journey_id == "journey-1"
    assert "snapshot:journey-1" in journey.calls


def test_create_from_journey_id_requires_port():
    with pytest.raises(MissionFactoryError, match="Journey engine port"):
        _factory(journey_engine=None).create_from_journey_id(
            "journey-1",
            scheduled_date=TODAY,
        )


def test_detect_resume_from_runtime():
    runtime = FakeSessionRuntime(phases={"sess-1": "paused"})
    snap = make_snapshot()
    plan = make_session_plan()
    mission = _factory(session_runtime=runtime).create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        session_plan=plan,
    )
    assert mission.is_resume is True


def test_build_card_from_mission():
    snap = make_snapshot()
    plan = make_session_plan()
    factory = _factory()
    mission = factory.create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        session_plan=plan,
    )
    card = factory.build_card(mission)
    assert card.mission_id == mission.mission_id
    assert card.title == mission.title
    assert card.is_active is False


def test_build_card_active_mission():
    snap = make_snapshot()
    plan = make_session_plan()
    factory = _factory()
    mission = factory.create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        session_plan=plan,
        initial_state=MissionState.ACTIVE,
    )
    card = factory.build_card(mission, runtime_phase="active")
    assert card.is_active is True


def test_build_card_completed():
    snap = make_snapshot()
    plan = make_session_plan()
    factory = _factory()
    mission = factory.create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        session_plan=plan,
        initial_state=MissionState.COMPLETED,
    )
    card = factory.build_card(mission)
    assert card.is_completed is True


def test_with_state_updates_lifecycle():
    snap = make_snapshot()
    plan = make_session_plan()
    factory = _factory()
    mission = factory.create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        session_plan=plan,
    )
    updated = factory.with_state(mission, MissionState.ACTIVE)
    assert updated.state == MissionState.ACTIVE
    assert mission.state == MissionState.READY


def test_with_state_completed_at():
    snap = make_snapshot()
    plan = make_session_plan()
    factory = _factory()
    mission = factory.create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        session_plan=plan,
    )
    updated = factory.with_state(mission, MissionState.COMPLETED, completed_at=NOW)
    assert updated.completed_at == NOW


def test_structural_title_from_objective():
    from app.domain.learning_journey.entities.learning_objective import ObjectiveKind

    obj = make_objective("obj-custom")
    obj = type(obj)(
        objective_id=obj.objective_id,
        curriculum_objective_ref=obj.curriculum_objective_ref,
        topic_id=obj.topic_id,
        kind=ObjectiveKind.UNDERSTAND,
        title="Custom Title",
        sequence_index=obj.sequence_index,
    )
    plan = make_session_plan(objective=obj)
    snap = make_snapshot()
    mission = _factory().create_from_snapshot(
        snap,
        scheduled_date=TODAY,
        session_plan=plan,
    )
    assert mission.title == "Custom Title"
