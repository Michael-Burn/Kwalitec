"""MissionScheduler tests."""

from __future__ import annotations

from datetime import timedelta

import pytest

from app.application.mission_engine_v2.exceptions import (
    SchedulingError,
    WorkloadExceeded,
)
from app.application.mission_engine_v2.lifecycle import MissionSlot, MissionState
from app.application.mission_engine_v2.policies.workload_policy import WorkloadPolicy
from app.application.mission_engine_v2.scheduler import MissionScheduler
from tests.application.mission_engine_v2.helpers import TODAY, make_mission

YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)
scheduler = MissionScheduler()


def _m(**kwargs):
    return make_mission(**kwargs)


def test_schedule_today_sets_ready():
    mission = _m(state=MissionState.PLANNED, slot=MissionSlot.FUTURE, scheduled_date=TOMORROW)  # noqa: E501
    result = scheduler.schedule_today(mission, as_of_date=TODAY)
    assert result.slot == MissionSlot.TODAY
    assert result.state == MissionState.READY
    assert result.scheduled_date == TODAY


def test_schedule_today_open_capacity_exceeded():
    existing = [
        _m(mission_id=f"m{i}", state=MissionState.READY)
        for i in range(WorkloadPolicy.MAX_OPEN_MISSIONS_PER_LEARNER)
    ]
    mission = _m(mission_id="new")
    with pytest.raises(WorkloadExceeded, match="open mission capacity"):
        scheduler.schedule_today(mission, as_of_date=TODAY, existing=existing)


def test_schedule_deferred():
    mission = _m(state=MissionState.ACTIVE)
    result = scheduler.schedule_deferred(mission)
    assert result.slot == MissionSlot.DEFERRED
    assert result.state == MissionState.PAUSED


def test_schedule_deferred_from_ready():
    mission = _m(state=MissionState.READY)
    result = scheduler.schedule_deferred(mission)
    assert result.state == MissionState.READY


def test_schedule_deferred_completed_raises():
    mission = _m(state=MissionState.COMPLETED)
    with pytest.raises(SchedulingError, match="Cannot defer"):
        scheduler.schedule_deferred(mission)


def test_schedule_deferred_capacity_exceeded():
    existing = [
        _m(mission_id=f"d{i}", slot=MissionSlot.DEFERRED)
        for i in range(WorkloadPolicy.MAX_DEFERRED_MISSIONS)
    ]
    with pytest.raises(WorkloadExceeded, match="Deferred"):
        scheduler.schedule_deferred(_m(mission_id="new"), existing=existing)


def test_schedule_revision():
    mission = _m()
    result = scheduler.schedule_revision(mission, as_of_date=TODAY)
    assert result.slot == MissionSlot.REVISION
    assert result.is_revision is True
    assert result.revision_debt >= 1


def test_schedule_revision_capacity_exceeded():
    existing = [
        _m(mission_id=f"r{i}", is_revision=True)
        for i in range(WorkloadPolicy.MAX_REVISION_MISSIONS)
    ]
    with pytest.raises(WorkloadExceeded, match="Revision"):
        scheduler.schedule_revision(_m(mission_id="new"), as_of_date=TODAY, existing=existing)  # noqa: E501


def test_schedule_future():
    mission = _m()
    result = scheduler.schedule_future(mission, as_of_date=TODAY, days_ahead=2)
    assert result.slot == MissionSlot.FUTURE
    assert result.scheduled_date == TODAY + timedelta(days=2)
    assert result.state == MissionState.PLANNED


def test_schedule_future_capacity_exceeded():
    existing = [
        _m(mission_id=f"f{i}", slot=MissionSlot.FUTURE, scheduled_date=TOMORROW)
        for i in range(WorkloadPolicy.MAX_FUTURE_MISSIONS)
    ]
    with pytest.raises(WorkloadExceeded, match="Future"):
        scheduler.schedule_future(_m(mission_id="new"), as_of_date=TODAY, existing=existing)  # noqa: E501


def test_mark_missed_eligible():
    mission = _m(
        scheduled_date=YESTERDAY,
        slot=MissionSlot.TODAY,
        state=MissionState.READY,
    )
    result = scheduler.mark_missed(mission, as_of_date=TODAY)
    assert result.slot == MissionSlot.MISSED


def test_mark_missed_ineligible_raises():
    mission = _m(scheduled_date=TODAY, state=MissionState.ACTIVE)
    with pytest.raises(SchedulingError, match="not eligible"):
        scheduler.mark_missed(mission, as_of_date=TODAY)


def test_mark_missed_capacity_exceeded():
    existing = [
        _m(mission_id=f"m{i}", slot=MissionSlot.MISSED, scheduled_date=YESTERDAY)
        for i in range(WorkloadPolicy.MAX_MISSED_MISSIONS)
    ]
    mission = _m(
        mission_id="new",
        scheduled_date=YESTERDAY,
        slot=MissionSlot.TODAY,
        state=MissionState.READY,
    )
    with pytest.raises(WorkloadExceeded, match="Missed"):
        scheduler.mark_missed(mission, as_of_date=TODAY, existing=existing)


def test_reschedule_to_today():
    mission = _m(scheduled_date=YESTERDAY, slot=MissionSlot.MISSED)
    result = scheduler.reschedule(
        mission,
        new_date=TODAY,
        as_of_date=TODAY,
    )
    assert result.scheduled_date == TODAY
    assert result.slot == MissionSlot.TODAY
    assert result.state == MissionState.READY


def test_reschedule_completed_raises():
    mission = _m(state=MissionState.COMPLETED)
    with pytest.raises(SchedulingError, match="Cannot reschedule"):
        scheduler.reschedule(mission, new_date=TOMORROW, as_of_date=TODAY)


def test_reschedule_deferred_flag():
    mission = _m()
    result = scheduler.reschedule(
        mission,
        new_date=TODAY,
        as_of_date=TODAY,
        is_deferred=True,
    )
    assert result.slot == MissionSlot.DEFERRED


def test_build_timeline():
    missions = [
        _m(mission_id="today", slot=MissionSlot.TODAY, state=MissionState.READY),
        _m(mission_id="def", slot=MissionSlot.DEFERRED),
        _m(mission_id="other-learner", learner_id="other"),
    ]
    timeline = scheduler.build_timeline("learner-1", missions, as_of_date=TODAY)
    assert timeline.learner_id == "learner-1"
    assert timeline.today is not None
    assert timeline.today.mission_id == "today"
    assert len(timeline.deferred) == 1
    assert len(timeline.ordered) == 2


def test_refresh_missed_updates_past_missions():
    past = _m(
        mission_id="past",
        scheduled_date=YESTERDAY,
        slot=MissionSlot.TODAY,
        state=MissionState.READY,
    )
    current = _m(mission_id="current", scheduled_date=TODAY)
    refreshed = scheduler.refresh_missed([past, current], as_of_date=TODAY)
    missed = [m for m in refreshed if m.mission_id == "past"][0]
    assert missed.slot == MissionSlot.MISSED


def test_refresh_missed_skips_ineligible():
    today_active = _m(scheduled_date=TODAY, state=MissionState.ACTIVE)
    refreshed = scheduler.refresh_missed([today_active], as_of_date=TODAY)
    assert refreshed[0].slot == MissionSlot.TODAY
