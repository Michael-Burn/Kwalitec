"""Dispatcher and coordinator tests."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.exceptions import DeliveryError, WorkloadExceeded
from app.application.mission_engine.mission_builder import MissionBuilder
from app.application.mission_engine.mission_coordinator import MissionCoordinator
from app.application.mission_engine.mission_dispatcher import MissionDispatcher
from app.application.mission_engine.mission_state import (
    DeliveryAction,
    MissionSlot,
    MissionState,
)
from tests.application.mission_engine.helpers import (
    TODAY,
    active_journey,
    make_builder,
    make_journey_engine,
)

NOW = datetime(2026, 7, 18, tzinfo=UTC)


def _m(**kwargs) -> DailyMission:
    base = dict(
        mission_id="m1",
        learner_id="learner-1",
        journey_id="journey-1",
        session_id="s1",
        topic_id="topic-a",
        curriculum_id="c1",
        scheduled_date=TODAY,
        slot=MissionSlot.TODAY,
        state=MissionState.ACTIVE,
        objective_id="obj-1",
        effort="medium",
        title="T",
        sequence_index=0,
        is_resume=False,
        is_revision=False,
        created_at=NOW,
    )
    base.update(kwargs)
    return DailyMission(**base)


@pytest.fixture
def dispatcher() -> MissionDispatcher:
    return MissionDispatcher()


def test_dispatch_today(dispatcher):
    d = dispatcher.dispatch(_m())
    assert d.action == DeliveryAction.TODAY
    assert d.payload["action"] == "today_mission"
    assert d.session_id == "s1"


def test_dispatch_resume(dispatcher):
    d = dispatcher.dispatch_resume(_m(is_resume=True))
    assert d.action == DeliveryAction.RESUME


def test_dispatch_continue(dispatcher):
    d = dispatcher.dispatch_continue(_m(state=MissionState.IN_PROGRESS))
    assert d.action == DeliveryAction.CONTINUE


def test_dispatch_review(dispatcher):
    d = dispatcher.dispatch_review(_m(state=MissionState.COMPLETED))
    assert d.action == DeliveryAction.REVIEW


def test_dispatch_revision(dispatcher):
    d = dispatcher.dispatch_revision(
        _m(is_revision=True, slot=MissionSlot.REVISION, state=MissionState.SCHEDULED)
    )
    assert d.action == DeliveryAction.REVISION


def test_dispatch_none_raises(dispatcher):
    with pytest.raises(DeliveryError):
        dispatcher.dispatch(_m(state=MissionState.ARCHIVED))


def test_dispatch_extra_payload(dispatcher):
    d = dispatcher.dispatch(_m(), extra={"source": "test"})
    assert d.payload["source"] == "test"


def test_dispatch_summary(dispatcher):
    builder = make_builder()
    journey = active_journey()
    mission = builder.build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    summary = builder.build_summary(mission)
    d = dispatcher.dispatch_summary(summary)
    assert d.mission_id == mission.mission_id


def test_dispatch_summary_none_raises(dispatcher):
    builder = make_builder()
    journey = active_journey()
    mission = builder.build_daily_mission(
        journey, scheduled_date=TODAY, as_of_date=TODAY
    )
    from dataclasses import replace

    summary = replace(
        builder.build_summary(mission),
        delivery_action=DeliveryAction.NONE,
    )
    with pytest.raises(DeliveryError):
        dispatcher.dispatch_summary(summary)


def test_dispatch_today_convenience(dispatcher):
    d = dispatcher.dispatch_today(_m())
    assert d.action in {
        DeliveryAction.TODAY,
        DeliveryAction.RESUME,
        DeliveryAction.CONTINUE,
    }


def test_dispatch_today_archived_fails(dispatcher):
    with pytest.raises(DeliveryError):
        dispatcher.dispatch_today(_m(state=MissionState.ARCHIVED))


# --- Coordinator ---


@pytest.fixture
def coordinator() -> MissionCoordinator:
    engine = make_journey_engine()
    return MissionCoordinator(
        builder=MissionBuilder(
            journey_engine=engine,
            clock=lambda: NOW,
            id_factory=lambda: "c",
        ),
        journey_engine=engine,
    )


def test_coordinator_generate_today(coordinator):
    journey = active_journey()
    mission = coordinator.generate_today_mission(journey, as_of_date=TODAY)
    assert mission.state == MissionState.ACTIVE
    assert mission.slot == MissionSlot.TODAY


def test_coordinator_generate_tomorrow(coordinator):
    journey = active_journey()
    mission = coordinator.generate_tomorrow_mission(journey, as_of_date=TODAY)
    assert mission.slot == MissionSlot.TOMORROW
    assert mission.scheduled_date == date(2026, 7, 19)


def test_coordinator_second_today_fails(coordinator):
    journey = active_journey()
    first = coordinator.generate_today_mission(journey, as_of_date=TODAY)
    # Distinct id factory so the second candidate is not confused with first.
    coordinator._builder._id_factory = lambda: "other"
    with pytest.raises(WorkloadExceeded):
        coordinator.generate_today_mission(
            journey, as_of_date=TODAY, existing=[first]
        )


def test_coordinator_revision_alongside_active(coordinator):
    journey = active_journey()
    today = coordinator.generate_today_mission(journey, as_of_date=TODAY)
    rev = coordinator.generate_today_mission(
        journey,
        as_of_date=TODAY,
        existing=[today],
        is_revision=True,
    )
    assert rev.is_revision is True
    assert rev.state == MissionState.SCHEDULED
    assert rev.slot == MissionSlot.REVISION


def test_coordinator_orchestrate_ensures_today(coordinator):
    journey = active_journey()
    ledger, schedule, summary = coordinator.orchestrate(
        journey, [], as_of_date=TODAY
    )
    assert len(ledger) == 1
    assert schedule.today is not None
    assert summary is not None
    assert summary.is_active is True


def test_coordinator_orchestrate_no_ensure(coordinator):
    journey = active_journey()
    ledger, schedule, summary = coordinator.orchestrate(
        journey, [], as_of_date=TODAY, ensure_today=False
    )
    assert ledger == ()
    assert schedule.today is None
    assert summary is None


def test_coordinator_dashboard_and_deliver(coordinator):
    journey = active_journey()
    mission = coordinator.generate_today_mission(journey, as_of_date=TODAY)
    summary = coordinator.dashboard_summary(mission)
    delivery = coordinator.deliver(mission)
    assert summary.mission_id == mission.mission_id
    assert delivery.mission_id == mission.mission_id


def test_coordinator_refresh_missed_in_orchestrate(coordinator):
    journey = active_journey()
    old = _m(
        mission_id="old",
        scheduled_date=date(2026, 7, 10),
        state=MissionState.ACTIVE,
    )
    ledger, schedule, _ = coordinator.orchestrate(
        journey, [old], as_of_date=TODAY, ensure_today=True
    )
    by_id = {m.mission_id: m for m in ledger}
    assert by_id["old"].state == MissionState.MISSED
    assert schedule.today is not None
