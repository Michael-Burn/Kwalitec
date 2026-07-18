"""Policy unit tests for Mission Engine 2.0."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.mission_state import (
    DeliveryAction,
    MissionSlot,
    MissionState,
    MissionTransitionEvent,
    is_open_mission_state,
    is_terminal_mission_state,
    next_mission_state,
)
from app.application.mission_engine.policies.delivery_policy import DeliveryPolicy
from app.application.mission_engine.policies.scheduling_policy import SchedulingPolicy
from app.application.mission_engine.policies.workload_policy import WorkloadPolicy

TODAY = date(2026, 7, 18)


def _m(
    *,
    mid: str = "m1",
    scheduled: date = TODAY,
    slot: MissionSlot = MissionSlot.TODAY,
    state: MissionState = MissionState.ACTIVE,
    is_resume: bool = False,
    is_revision: bool = False,
    session_id: str | None = None,
) -> DailyMission:
    return DailyMission(
        mission_id=mid,
        learner_id="l1",
        journey_id="j1",
        session_id=session_id or f"s-{mid}",
        topic_id="t1",
        curriculum_id="c1",
        scheduled_date=scheduled,
        slot=slot,
        state=state,
        objective_id="o1",
        effort="medium",
        title="T",
        sequence_index=0,
        is_resume=is_resume,
        is_revision=is_revision,
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
    )


# --- SchedulingPolicy ---


@pytest.mark.parametrize(
    ("scheduled", "as_of", "revision", "expected"),
    [
        (TODAY, TODAY, False, MissionSlot.TODAY),
        (date(2026, 7, 19), TODAY, False, MissionSlot.TOMORROW),
        (date(2026, 7, 17), TODAY, False, MissionSlot.MISSED),
        (date(2026, 7, 25), TODAY, False, MissionSlot.DEFERRED),
        (TODAY, TODAY, True, MissionSlot.REVISION),
    ],
)
def test_slot_for_date(scheduled, as_of, revision, expected):
    assert (
        SchedulingPolicy.slot_for_date(
            scheduled, as_of_date=as_of, is_revision=revision
        )
        == expected
    )


def test_tomorrow_date():
    assert SchedulingPolicy.tomorrow_date(TODAY) == date(2026, 7, 19)


def test_should_mark_missed_true():
    m = _m(scheduled=date(2026, 7, 17), state=MissionState.ACTIVE)
    assert SchedulingPolicy.should_mark_missed(m, as_of_date=TODAY)


def test_should_mark_missed_false_for_today():
    m = _m(state=MissionState.ACTIVE)
    assert not SchedulingPolicy.should_mark_missed(m, as_of_date=TODAY)


def test_should_mark_missed_false_for_completed():
    m = _m(scheduled=date(2026, 7, 10), state=MissionState.COMPLETED)
    assert not SchedulingPolicy.should_mark_missed(m, as_of_date=TODAY)


def test_should_activate_today():
    m = _m(state=MissionState.SCHEDULED, slot=MissionSlot.TODAY)
    assert SchedulingPolicy.should_activate_today(m, as_of_date=TODAY)


def test_order_prefers_today_over_tomorrow():
    a = _m(
        mid="tomorrow",
        scheduled=date(2026, 7, 19),
        slot=MissionSlot.TOMORROW,
        state=MissionState.SCHEDULED,
    )
    b = _m(mid="today", slot=MissionSlot.TODAY, state=MissionState.ACTIVE)
    ordered = SchedulingPolicy.order([a, b])
    assert ordered[0].mission_id == "today"


def test_pick_today_prefers_in_progress():
    a = _m(mid="active", state=MissionState.ACTIVE)
    b = _m(mid="prog", state=MissionState.IN_PROGRESS, session_id="s-prog")
    # different session ids already
    pick = SchedulingPolicy.pick_today([a, b], as_of_date=TODAY)
    assert pick is not None
    assert pick.mission_id == "prog"


def test_pick_today_none():
    assert SchedulingPolicy.pick_today([], as_of_date=TODAY) is None


def test_pick_tomorrow():
    m = _m(
        mid="tm",
        scheduled=date(2026, 7, 19),
        slot=MissionSlot.TOMORROW,
        state=MissionState.SCHEDULED,
    )
    assert SchedulingPolicy.pick_tomorrow([m], as_of_date=TODAY) is m


def test_pick_tomorrow_none_when_wrong_slot():
    m = _m(
        scheduled=date(2026, 7, 19),
        slot=MissionSlot.DEFERRED,
        state=MissionState.SCHEDULED,
    )
    assert SchedulingPolicy.pick_tomorrow([m], as_of_date=TODAY) is None


# --- WorkloadPolicy ---


def test_workload_active_cap():
    assert WorkloadPolicy.MAX_ACTIVE_MISSIONS == 1
    assert not WorkloadPolicy.can_activate([_m()])
    assert WorkloadPolicy.can_activate([_m()], excluding_mission_id="m1")


def test_workload_open_cap():
    assert WorkloadPolicy.can_add_open([])
    many = [_m(mid=f"m{i}", state=MissionState.DEFERRED) for i in range(20)]
    assert not WorkloadPolicy.can_add_open(many)


def test_workload_deferred_cap():
    many = [_m(mid=f"d{i}", state=MissionState.DEFERRED) for i in range(10)]
    assert not WorkloadPolicy.can_defer(many)


def test_workload_missed_cap():
    many = [_m(mid=f"x{i}", state=MissionState.MISSED) for i in range(10)]
    assert not WorkloadPolicy.can_mark_missed(many)


def test_workload_revision_cap():
    many = [
        _m(mid=f"r{i}", is_revision=True, state=MissionState.SCHEDULED)
        for i in range(5)
    ]
    assert not WorkloadPolicy.can_add_revision(many)


def test_workload_filters():
    missions = [
        _m(mid="a", state=MissionState.ACTIVE),
        _m(mid="d", state=MissionState.DEFERRED),
        _m(mid="c", state=MissionState.COMPLETED),
        _m(mid="r", is_revision=True, state=MissionState.SCHEDULED),
    ]
    assert len(WorkloadPolicy.active_missions(missions)) == 1
    assert len(WorkloadPolicy.deferred_missions(missions)) == 1
    assert len(WorkloadPolicy.open_missions(missions)) == 3
    assert len(WorkloadPolicy.revision_missions(missions)) == 1


# --- DeliveryPolicy ---


@pytest.mark.parametrize(
    ("kwargs", "phase", "expected"),
    [
        ({"state": MissionState.ARCHIVED}, None, DeliveryAction.NONE),
        ({"state": MissionState.SKIPPED}, None, DeliveryAction.NONE),
        ({"state": MissionState.COMPLETED}, None, DeliveryAction.REVIEW),
        (
            {
                "is_revision": True,
                "slot": MissionSlot.REVISION,
                "state": MissionState.SCHEDULED,
            },
            None,
            DeliveryAction.REVISION,
        ),
        (
            {"is_resume": True, "state": MissionState.ACTIVE},
            None,
            DeliveryAction.RESUME,
        ),
        ({"state": MissionState.ACTIVE}, "paused", DeliveryAction.RESUME),
        ({"state": MissionState.IN_PROGRESS}, None, DeliveryAction.CONTINUE),
        ({"state": MissionState.ACTIVE}, "active", DeliveryAction.CONTINUE),
        ({"state": MissionState.ACTIVE}, "completed", DeliveryAction.REVIEW),
        ({"state": MissionState.ACTIVE}, None, DeliveryAction.TODAY),
        ({"state": MissionState.SCHEDULED}, None, DeliveryAction.TODAY),
    ],
)
def test_delivery_decide(kwargs, phase, expected):
    assert DeliveryPolicy.decide(_m(**kwargs), runtime_phase=phase) == expected


def test_is_deliverable():
    assert DeliveryPolicy.is_deliverable(_m())
    assert not DeliveryPolicy.is_deliverable(_m(state=MissionState.ARCHIVED))


# --- Mission state helpers ---


@pytest.mark.parametrize(
    ("state", "event", "expected"),
    [
        (MissionState.SCHEDULED, MissionTransitionEvent.ACTIVATE, MissionState.ACTIVE),
        (MissionState.ACTIVE, MissionTransitionEvent.START, MissionState.IN_PROGRESS),
        (
            MissionState.IN_PROGRESS,
            MissionTransitionEvent.COMPLETE,
            MissionState.COMPLETED,
        ),
        (MissionState.COMPLETED, MissionTransitionEvent.ARCHIVE, MissionState.ARCHIVED),
        (MissionState.ACTIVE, MissionTransitionEvent.DEFER, MissionState.DEFERRED),
        (MissionState.ACTIVE, MissionTransitionEvent.SKIP, MissionState.SKIPPED),
        (MissionState.ARCHIVED, MissionTransitionEvent.START, None),
    ],
)
def test_next_mission_state(state, event, expected):
    assert next_mission_state(state, event) == expected


def test_terminal_and_open_helpers():
    assert is_terminal_mission_state(MissionState.COMPLETED)
    assert is_terminal_mission_state(MissionState.ARCHIVED)
    assert is_terminal_mission_state(MissionState.SKIPPED)
    assert not is_terminal_mission_state(MissionState.ACTIVE)
    assert is_open_mission_state(MissionState.DEFERRED)
    assert not is_open_mission_state(MissionState.ARCHIVED)
