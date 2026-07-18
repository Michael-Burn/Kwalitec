"""SchedulingPolicy, WorkloadPolicy, and DispatchPolicy tests."""

from __future__ import annotations

from datetime import timedelta

import pytest

from app.application.mission_engine_v2.lifecycle import (
    DispatchAction,
    MissionSlot,
    MissionState,
)
from app.application.mission_engine_v2.policies.dispatch_policy import DispatchPolicy
from app.application.mission_engine_v2.policies.scheduling_policy import (
    SchedulingPolicy,
)
from app.application.mission_engine_v2.policies.workload_policy import WorkloadPolicy
from tests.application.mission_engine_v2.helpers import TODAY, make_mission

YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)
FUTURE = TODAY + timedelta(days=5)


def _m(**kwargs):
    return make_mission(**kwargs)


# --- SchedulingPolicy.slot_for_date ---


@pytest.mark.parametrize(
    ("scheduled", "as_of", "revision", "deferred", "missed", "expected"),
    [
        (TODAY, TODAY, False, False, False, MissionSlot.TODAY),
        (TOMORROW, TODAY, False, False, False, MissionSlot.FUTURE),
        (YESTERDAY, TODAY, False, False, False, MissionSlot.MISSED),
        (TODAY, TODAY, True, False, False, MissionSlot.REVISION),
        (TODAY, TODAY, False, True, False, MissionSlot.DEFERRED),
    ],
)
def test_slot_for_date(scheduled, as_of, revision, deferred, missed, expected):
    assert (
        SchedulingPolicy.slot_for_date(
            scheduled,
            as_of_date=as_of,
            is_revision=revision,
            is_deferred=deferred,
            is_missed=missed,
        )
        == expected
    )


def test_future_date():
    assert SchedulingPolicy.future_date(TODAY, days_ahead=7) == TODAY + timedelta(days=7)  # noqa: E501


def test_future_date_minimum_one_day():
    assert SchedulingPolicy.future_date(TODAY, days_ahead=0) == TOMORROW


@pytest.mark.parametrize(
    ("state", "slot", "scheduled", "expected"),
    [
        (MissionState.READY, MissionSlot.TODAY, YESTERDAY, True),
        (MissionState.ACTIVE, MissionSlot.TODAY, TODAY, False),
        (MissionState.COMPLETED, MissionSlot.TODAY, YESTERDAY, False),
    ],
)
def test_should_mark_missed(state, slot, scheduled, expected):
    mission = _m(state=state, slot=slot, scheduled_date=scheduled)
    assert SchedulingPolicy.should_mark_missed(mission, as_of_date=TODAY) is expected


def test_order_by_slot_priority():
    missions = [
        _m(mission_id="f", slot=MissionSlot.FUTURE, scheduled_date=TOMORROW),
        _m(mission_id="t", slot=MissionSlot.TODAY),
        _m(mission_id="m", slot=MissionSlot.MISSED, scheduled_date=YESTERDAY),
    ]
    ordered = SchedulingPolicy.order(missions)
    assert [m.mission_id for m in ordered] == ["t", "m", "f"]


def test_order_by_date_within_slot():
    missions = [
        _m(mission_id="b", slot=MissionSlot.MISSED, scheduled_date=YESTERDAY),
        _m(mission_id="a", slot=MissionSlot.MISSED, scheduled_date=YESTERDAY - timedelta(1)),  # noqa: E501
    ]
    ordered = SchedulingPolicy.order(missions)
    assert ordered[0].mission_id == "a"


def test_pick_today_prefers_active():
    missions = [
        _m(mission_id="ready", state=MissionState.READY),
        _m(mission_id="active", state=MissionState.ACTIVE),
    ]
    picked = SchedulingPolicy.pick_today(missions, as_of_date=TODAY)
    assert picked is not None
    assert picked.mission_id == "active"


def test_pick_today_none_when_empty():
    assert SchedulingPolicy.pick_today([], as_of_date=TODAY) is None


def test_pick_today_skips_revision():
    missions = [_m(is_revision=True, slot=MissionSlot.TODAY)]
    assert SchedulingPolicy.pick_today(missions, as_of_date=TODAY) is None


def test_filter_slot_deferred():
    target = _m(mission_id="target", slot=MissionSlot.DEFERRED)
    other = _m(mission_id="other", slot=MissionSlot.TODAY)
    result = SchedulingPolicy.filter_slot([other, target], MissionSlot.DEFERRED)
    assert len(result) == 1
    assert result[0].mission_id == "target"


def test_filter_slot_revision():
    target = _m(mission_id="target", slot=MissionSlot.REVISION, is_revision=True)
    result = SchedulingPolicy.filter_slot([target], MissionSlot.REVISION)
    assert len(result) == 1


def test_filter_slot_excludes_completed():
    completed = _m(mission_id="done", slot=MissionSlot.DEFERRED, state=MissionState.COMPLETED)  # noqa: E501
    result = SchedulingPolicy.filter_slot([completed], MissionSlot.DEFERRED)
    assert result == ()


def test_slot_priority_order():
    assert SchedulingPolicy.SLOT_PRIORITY[0] == MissionSlot.TODAY
    assert MissionSlot.FUTURE in SchedulingPolicy.SLOT_PRIORITY


# --- WorkloadPolicy ---


def test_open_missions_filters_terminal():
    missions = [
        _m(state=MissionState.ACTIVE),
        _m(mission_id="m2", state=MissionState.COMPLETED),
    ]
    assert len(WorkloadPolicy.open_missions(missions)) == 1


def test_active_missions():
    missions = [
        _m(state=MissionState.ACTIVE),
        _m(mission_id="m2", state=MissionState.PAUSED),
        _m(mission_id="m3", state=MissionState.READY),
    ]
    assert len(WorkloadPolicy.active_missions(missions)) == 2


def test_deferred_missions():
    missions = [
        _m(slot=MissionSlot.DEFERRED),
        _m(mission_id="m2", slot=MissionSlot.TODAY),
    ]
    assert len(WorkloadPolicy.deferred_missions(missions)) == 1


def test_missed_missions():
    missions = [_m(slot=MissionSlot.MISSED, scheduled_date=YESTERDAY)]
    assert len(WorkloadPolicy.missed_missions(missions)) == 1


def test_revision_missions():
    missions = [_m(is_revision=True)]
    assert len(WorkloadPolicy.revision_missions(missions)) == 1


def test_future_missions():
    missions = [_m(slot=MissionSlot.FUTURE, scheduled_date=TOMORROW)]
    assert len(WorkloadPolicy.future_missions(missions)) == 1


def test_can_activate_when_none_active():
    assert WorkloadPolicy.can_activate([]) is True


def test_can_activate_false_when_one_active():
    missions = [_m(state=MissionState.ACTIVE)]
    assert WorkloadPolicy.can_activate(missions) is False


def test_can_activate_excluding_self():
    missions = [_m(mission_id="m1", state=MissionState.ACTIVE)]
    assert WorkloadPolicy.can_activate(missions, excluding_mission_id="m1") is True


def test_can_add_open_under_capacity():
    missions = [_m(mission_id="m0", state=MissionState.READY)]
    assert WorkloadPolicy.can_add_open(missions) is True


def test_can_add_open_at_capacity():
    missions = [
        _m(mission_id=f"m{i}", state=MissionState.READY)
        for i in range(WorkloadPolicy.MAX_OPEN_MISSIONS_PER_LEARNER)
    ]
    assert WorkloadPolicy.can_add_open(missions) is False


@pytest.mark.parametrize(
    ("effort", "weight"),
    [
        ("minimal", 1),
        ("medium", 2),
        ("heavy", 3),
        ("unknown", 2),
    ],
)
def test_effort_weight(effort, weight):
    assert WorkloadPolicy.effort_weight(effort) == weight


def test_total_outstanding_reflections():
    missions = [
        _m(outstanding_reflections=2),
        _m(mission_id="m2", outstanding_reflections=3, state=MissionState.COMPLETED),
    ]
    assert WorkloadPolicy.total_outstanding_reflections(missions) == 2


def test_total_revision_debt():
    missions = [_m(revision_debt=2), _m(mission_id="m2", revision_debt=1)]
    assert WorkloadPolicy.total_revision_debt(missions) == 3


def test_has_journey_continuity():
    missions = [_m(journey_id="journey-1")]
    assert WorkloadPolicy.has_journey_continuity(missions, "journey-1") is True
    assert WorkloadPolicy.has_journey_continuity(missions, "journey-2") is False


def test_is_paused():
    assert WorkloadPolicy.is_paused(_m(state=MissionState.PAUSED)) is True
    assert WorkloadPolicy.is_paused(_m(state=MissionState.ACTIVE)) is False


def test_capacity_methods_empty_ledger():
    assert WorkloadPolicy.can_defer([]) is True
    assert WorkloadPolicy.can_add_future([]) is True


# --- DispatchPolicy ---


@pytest.mark.parametrize(
    ("state", "slot", "is_revision", "is_resume", "phase", "expected"),
    [
        (MissionState.ARCHIVED, MissionSlot.TODAY, False, False, None, DispatchAction.NONE),  # noqa: E501
        (MissionState.COMPLETED, MissionSlot.TODAY, False, False, None, DispatchAction.REVIEW),  # noqa: E501
        (MissionState.PLANNED, MissionSlot.REVISION, True, False, None, DispatchAction.REVISION),  # noqa: E501
        (MissionState.READY, MissionSlot.DEFERRED, False, False, None, DispatchAction.DEFERRED),  # noqa: E501
        (MissionState.PAUSED, MissionSlot.TODAY, False, False, None, DispatchAction.RESUME),  # noqa: E501
        (MissionState.ACTIVE, MissionSlot.TODAY, False, False, None, DispatchAction.CONTINUE),  # noqa: E501
        (MissionState.PLANNED, MissionSlot.FUTURE, False, False, None, DispatchAction.NONE),  # noqa: E501
        (MissionState.READY, MissionSlot.TODAY, False, False, "paused", DispatchAction.RESUME),  # noqa: E501
    ],
)
def test_dispatch_decide(state, slot, is_revision, is_resume, phase, expected):
    mission = _m(
        state=state,
        slot=slot,
        is_revision=is_revision,
        is_resume=is_resume,
    )
    assert DispatchPolicy.decide(mission, runtime_phase=phase) == expected


def test_is_deliverable():
    assert DispatchPolicy.is_deliverable(DispatchAction.TODAY) is True
    assert DispatchPolicy.is_deliverable(DispatchAction.NONE) is False
