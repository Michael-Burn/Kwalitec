"""MissionCoordinator orchestration tests."""

from __future__ import annotations

from datetime import timedelta

import pytest

from app.application.mission_engine_v2.coordinator import MissionCoordinator
from app.application.mission_engine_v2.exceptions import WorkloadExceeded
from app.application.mission_engine_v2.lifecycle import MissionSlot, MissionState
from app.application.mission_engine_v2.policies.workload_policy import WorkloadPolicy
from tests.application.mission_engine_v2.helpers import (
    TODAY,
    FakeJourneyEngine,
    FakeNavigation,
    FakeSessionRuntime,
    make_mission,
    make_snapshot,
)


def _coordinator(**kwargs) -> MissionCoordinator:
    defaults = {
        "journey_engine": FakeJourneyEngine(),
        "session_runtime": FakeSessionRuntime(),
        "navigation": FakeNavigation(),
    }
    defaults.update(kwargs)
    return MissionCoordinator(**defaults)


def test_generate_today_mission():
    snap = make_snapshot()
    mission = _coordinator().generate_today_mission(snap, as_of_date=TODAY)
    assert mission.slot == MissionSlot.TODAY
    assert mission.state == MissionState.READY


def test_generate_today_revision():
    snap = make_snapshot()
    mission = _coordinator().generate_today_mission(
        snap,
        as_of_date=TODAY,
        is_revision=True,
    )
    assert mission.is_revision is True
    assert mission.slot == MissionSlot.REVISION


def test_generate_deferred_mission():
    snap = make_snapshot()
    mission = _coordinator().generate_deferred_mission(snap, as_of_date=TODAY)
    assert mission.slot == MissionSlot.DEFERRED


def test_generate_future_mission():
    snap = make_snapshot()
    mission = _coordinator().generate_future_mission(snap, as_of_date=TODAY, days_ahead=2)  # noqa: E501
    assert mission.slot == MissionSlot.FUTURE
    assert mission.scheduled_date == TODAY + timedelta(days=2)


def test_orchestrate_ensure_today():
    snap = make_snapshot()
    ledger, timeline, card = _coordinator().orchestrate(
        snap,
        [],
        as_of_date=TODAY,
        ensure_today=True,
    )
    assert len(ledger) >= 1
    assert timeline.today is not None
    assert card is not None


def test_orchestrate_without_ensure_today():
    snap = make_snapshot()
    ledger, timeline, card = _coordinator().orchestrate(
        snap,
        [],
        as_of_date=TODAY,
        ensure_today=False,
    )
    assert card is None
    assert timeline.today is None


def test_orchestrate_refresh_missed():
    snap = make_snapshot()
    past = make_mission(
        mission_id="past",
        scheduled_date=TODAY - timedelta(days=1),
        slot=MissionSlot.TODAY,
        state=MissionState.READY,
    )
    ledger, timeline, _ = _coordinator().orchestrate(
        snap,
        [past],
        as_of_date=TODAY,
        ensure_today=False,
    )
    missed_ids = [m.mission_id for m in ledger if m.slot == MissionSlot.MISSED]
    assert "past" in missed_ids
    assert len(timeline.missed) >= 1


def test_build_dashboard():
    snap = make_snapshot()
    coord = _coordinator()
    mission = coord.generate_today_mission(snap, as_of_date=TODAY)
    dashboard = coord.build_dashboard(
        "learner-1",
        [mission],
        as_of_date=TODAY,
    )
    assert dashboard.learner_id == "learner-1"
    assert dashboard.today is not None
    assert dashboard.workload_ok is True


def test_build_dashboard_with_deferred():
    snap = make_snapshot()
    coord = _coordinator()
    deferred = coord.generate_deferred_mission(snap, as_of_date=TODAY)
    dashboard = coord.build_dashboard("learner-1", [deferred], as_of_date=TODAY)
    assert len(dashboard.deferred) == 1


def test_deliver():
    snap = make_snapshot()
    coord = _coordinator()
    mission = coord.generate_today_mission(snap, as_of_date=TODAY)
    execution = coord.deliver(mission)
    assert execution.mission_id == mission.mission_id


def test_coordinator_exposes_components():
    coord = _coordinator()
    assert coord.factory is not None
    assert coord.scheduler is not None
    assert coord.validator is not None
    assert coord.dispatcher is not None
    assert coord.balancer is not None


def test_generate_today_workload_blocked():
    snap = make_snapshot()
    existing = [
        make_mission(mission_id=f"m{i}")
        for i in range(WorkloadPolicy.MAX_OPEN_MISSIONS_PER_LEARNER)
    ]
    with pytest.raises(WorkloadExceeded):
        _coordinator().generate_today_mission(snap, as_of_date=TODAY, existing=existing)


def test_orchestrate_skips_generation_when_overloaded():
    snap = make_snapshot()
    existing = [
        make_mission(mission_id=f"m{i}", outstanding_reflections=3)
        for i in range(3)
    ]
    ledger, timeline, card = _coordinator().orchestrate(
        snap,
        existing,
        as_of_date=TODAY,
        ensure_today=True,
    )
    assert len(ledger) == 3
    assert timeline.today is not None
    assert card is not None


def test_build_dashboard_active_mission_id():
    snap = make_snapshot()
    coord = _coordinator()
    mission = coord.generate_today_mission(snap, as_of_date=TODAY)
    active = coord.factory.with_state(mission, MissionState.ACTIVE)
    dashboard = coord.build_dashboard("learner-1", [active], as_of_date=TODAY)
    assert dashboard.active_mission_id == active.mission_id


def test_orchestrate_does_not_mutate_input_list_type():
    snap = make_snapshot()
    missions = [make_mission(scheduled_date=TODAY, state=MissionState.READY)]
    ledger, _, _ = _coordinator().orchestrate(
        snap,
        missions,
        as_of_date=TODAY,
        ensure_today=False,
    )
    assert isinstance(ledger, tuple)
