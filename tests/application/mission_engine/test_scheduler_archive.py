"""Mission scheduler and archive tests."""

from __future__ import annotations

from datetime import UTC, date, datetime

import pytest

from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.exceptions import (
    InvalidMissionState,
    MissionAlreadyArchived,
    SchedulingError,
    WorkloadExceeded,
)
from app.application.mission_engine.mission_archive import MissionArchive
from app.application.mission_engine.mission_scheduler import MissionScheduler
from app.application.mission_engine.mission_state import MissionSlot, MissionState

TODAY = date(2026, 7, 18)
NOW = datetime(2026, 7, 18, tzinfo=UTC)


def _m(
    *,
    mid: str = "m1",
    scheduled: date = TODAY,
    slot: MissionSlot = MissionSlot.TODAY,
    state: MissionState = MissionState.ACTIVE,
    learner: str = "l1",
) -> DailyMission:
    return DailyMission(
        mission_id=mid,
        learner_id=learner,
        journey_id="j1",
        session_id=f"s-{mid}",
        topic_id="t1",
        curriculum_id="c1",
        scheduled_date=scheduled,
        slot=slot,
        state=state,
        objective_id="o1",
        effort="medium",
        title="T",
        sequence_index=0,
        is_resume=False,
        is_revision=False,
        created_at=NOW,
    )


@pytest.fixture
def scheduler() -> MissionScheduler:
    return MissionScheduler()


@pytest.fixture
def archive() -> MissionArchive:
    return MissionArchive(clock=lambda: NOW)


def test_build_schedule_empty(scheduler):
    sched = scheduler.build_schedule("l1", [], as_of_date=TODAY)
    assert sched.today is None
    assert sched.tomorrow is None
    assert sched.ordered == ()


def test_build_schedule_partitions(scheduler):
    missions = [
        _m(mid="today"),
        _m(
            mid="tm",
            scheduled=date(2026, 7, 19),
            slot=MissionSlot.TOMORROW,
            state=MissionState.SCHEDULED,
        ),
        _m(mid="def", slot=MissionSlot.DEFERRED, state=MissionState.DEFERRED),
        _m(mid="miss", slot=MissionSlot.MISSED, state=MissionState.MISSED),
        _m(mid="rev", slot=MissionSlot.REVISION, state=MissionState.SCHEDULED),
    ]
    # mark revision flag
    from dataclasses import replace

    missions[-1] = replace(missions[-1], is_revision=True)
    sched = scheduler.build_schedule("l1", missions, as_of_date=TODAY)
    assert sched.today is not None
    assert sched.today.mission_id == "today"
    assert sched.tomorrow is not None
    assert len(sched.deferred) >= 1
    assert len(sched.missed) >= 1
    assert len(sched.revision) >= 1


def test_schedule_ignores_other_learners(scheduler):
    sched = scheduler.build_schedule(
        "l1",
        [_m(learner="other")],
        as_of_date=TODAY,
    )
    assert sched.today is None


def test_schedule_today(scheduler):
    m = _m(state=MissionState.SCHEDULED)
    out = scheduler.schedule_today(m, as_of_date=TODAY)
    assert out.state == MissionState.ACTIVE
    assert out.slot == MissionSlot.TODAY
    assert out.scheduled_date == TODAY


def test_schedule_today_workload(scheduler):
    with pytest.raises(WorkloadExceeded):
        scheduler.schedule_today(_m(mid="new"), as_of_date=TODAY, existing=[_m()])


def test_schedule_tomorrow(scheduler):
    out = scheduler.schedule_tomorrow(_m(), as_of_date=TODAY)
    assert out.scheduled_date == date(2026, 7, 19)
    assert out.slot == MissionSlot.TOMORROW
    assert out.state == MissionState.SCHEDULED


def test_defer(scheduler):
    out = scheduler.defer(_m())
    assert out.state == MissionState.DEFERRED
    assert out.slot == MissionSlot.DEFERRED


def test_defer_capacity(scheduler):
    existing = [
        _m(mid=f"d{i}", state=MissionState.DEFERRED) for i in range(10)
    ]
    with pytest.raises(WorkloadExceeded):
        scheduler.defer(_m(), existing=existing)


def test_defer_unlawful(scheduler):
    with pytest.raises(SchedulingError):
        scheduler.defer(_m(state=MissionState.COMPLETED))


def test_mark_missed(scheduler):
    m = _m(scheduled=date(2026, 7, 10), state=MissionState.ACTIVE)
    out = scheduler.mark_missed(m, as_of_date=TODAY)
    assert out.state == MissionState.MISSED
    assert out.slot == MissionSlot.MISSED


def test_mark_missed_not_eligible(scheduler):
    with pytest.raises(SchedulingError):
        scheduler.mark_missed(_m(), as_of_date=TODAY)


def test_reschedule_to_today(scheduler):
    m = _m(state=MissionState.DEFERRED, slot=MissionSlot.DEFERRED)
    out = scheduler.reschedule(m, new_date=TODAY, as_of_date=TODAY)
    assert out.state == MissionState.ACTIVE
    assert out.slot == MissionSlot.TODAY


def test_reschedule_to_tomorrow(scheduler):
    m = _m(state=MissionState.MISSED, slot=MissionSlot.MISSED)
    out = scheduler.reschedule(
        m, new_date=date(2026, 7, 19), as_of_date=TODAY
    )
    assert out.slot == MissionSlot.TOMORROW
    assert out.state == MissionState.SCHEDULED


def test_reschedule_completed_fails(scheduler):
    with pytest.raises(SchedulingError):
        scheduler.reschedule(
            _m(state=MissionState.COMPLETED),
            new_date=TODAY,
            as_of_date=TODAY,
        )


def test_reschedule_today_workload(scheduler):
    m = _m(mid="def", state=MissionState.DEFERRED, slot=MissionSlot.DEFERRED)
    with pytest.raises(WorkloadExceeded):
        scheduler.reschedule(
            m,
            new_date=TODAY,
            as_of_date=TODAY,
            existing=[_m()],
        )


def test_skip(scheduler):
    assert scheduler.skip(_m()).state == MissionState.SKIPPED


def test_skip_completed_fails(scheduler):
    with pytest.raises(SchedulingError):
        scheduler.skip(_m(state=MissionState.COMPLETED))


def test_start(scheduler):
    assert scheduler.start(_m()).state == MissionState.IN_PROGRESS


def test_start_from_scheduled_fails(scheduler):
    with pytest.raises(SchedulingError):
        scheduler.start(_m(state=MissionState.SCHEDULED))


def test_refresh_missed(scheduler):
    missions = [
        _m(mid="old", scheduled=date(2026, 7, 10), state=MissionState.ACTIVE),
        _m(mid="ok"),
    ]
    out = scheduler.refresh_missed(missions, as_of_date=TODAY)
    by_id = {m.mission_id: m for m in out}
    assert by_id["old"].state == MissionState.MISSED
    assert by_id["ok"].state == MissionState.ACTIVE


# --- Archive ---


def test_archive_complete(archive):
    m = _m(state=MissionState.IN_PROGRESS)
    done = archive.complete(m)
    assert done.state == MissionState.COMPLETED
    assert done.completed_at == NOW


def test_archive_complete_idempotent(archive):
    m = _m(state=MissionState.COMPLETED)
    done = archive.complete(m)
    assert done is m or done.state == MissionState.COMPLETED


def test_archive_requires_completed(archive):
    with pytest.raises(InvalidMissionState):
        archive.archive(_m(state=MissionState.ACTIVE))


def test_archive_stores_history(archive):
    m = archive.complete_and_archive(_m(state=MissionState.ACTIVE))
    assert m.state == MissionState.ARCHIVED
    assert archive.find(m.mission_id) is m
    assert archive.for_learner("l1") == (m,)
    assert archive.for_journey("j1") == (m,)


def test_archive_already_archived(archive):
    m = archive.complete_and_archive(_m())
    with pytest.raises(MissionAlreadyArchived):
        archive.archive(m)


def test_complete_already_archived(archive):
    m = archive.complete_and_archive(_m())
    with pytest.raises(MissionAlreadyArchived):
        archive.complete(m)


def test_archive_clear(archive):
    archive.complete_and_archive(_m())
    archive.clear()
    assert archive.history == ()


def test_archive_find_missing(archive):
    assert archive.find("nope") is None
