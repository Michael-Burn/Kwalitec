"""WorkloadBalancer and WorkloadAssessment tests."""

from __future__ import annotations

from datetime import timedelta

import pytest

from app.application.mission_engine_v2.exceptions import WorkloadExceeded
from app.application.mission_engine_v2.lifecycle import MissionSlot, MissionState
from app.application.mission_engine_v2.policies.workload_policy import WorkloadPolicy
from app.application.mission_engine_v2.workload_balancer import WorkloadBalancer
from tests.application.mission_engine_v2.helpers import TODAY, make_mission

YESTERDAY = TODAY - timedelta(days=1)
TOMORROW = TODAY + timedelta(days=1)


balancer = WorkloadBalancer()


def _m(**kwargs):
    return make_mission(**kwargs)


def test_assess_empty_ledger():
    assessment = balancer.assess([])
    assert assessment.open_count == 0
    assert assessment.within_limits is True
    assert assessment.blocking_reasons == ()


def test_assess_open_count():
    missions = [_m(), _m(mission_id="m2", state=MissionState.COMPLETED)]
    assessment = balancer.assess(missions)
    assert assessment.open_count == 1


def test_assess_effort_load():
    missions = [_m(effort="heavy"), _m(mission_id="m2", effort="minimal")]
    assessment = balancer.assess(missions)
    assert assessment.effort_load == 4


def test_assess_journey_continuity():
    missions = [_m(journey_id="journey-1")]
    assessment = balancer.assess(missions, journey_id="journey-1")
    assert assessment.journey_continuity is True


def test_assess_blocking_open_capacity():
    missions = [
        _m(mission_id=f"m{i}", state=MissionState.READY)
        for i in range(WorkloadPolicy.MAX_OPEN_MISSIONS_PER_LEARNER)
    ]
    assessment = balancer.assess(missions)
    assert assessment.within_limits is False
    assert "open_capacity" in assessment.blocking_reasons


def test_assess_blocking_active_capacity():
    missions = [_m(state=MissionState.ACTIVE)]
    assessment = balancer.assess(missions)
    assert "active_capacity" in assessment.blocking_reasons


def test_assess_blocking_reflections():
    missions = [_m(outstanding_reflections=6)]
    assessment = balancer.assess(missions)
    assert "outstanding_reflections" in assessment.blocking_reasons


def test_assess_blocking_revision_debt():
    missions = [_m(revision_debt=9)]
    assessment = balancer.assess(missions)
    assert "revision_debt" in assessment.blocking_reasons


def test_assert_can_add_ok():
    candidate = _m(mission_id="new")
    balancer.assert_can_add([], candidate)


def test_assert_can_add_open_exceeded():
    existing = [
        _m(mission_id=f"m{i}")
        for i in range(WorkloadPolicy.MAX_OPEN_MISSIONS_PER_LEARNER)
    ]
    candidate = _m(mission_id="new")
    with pytest.raises(WorkloadExceeded, match="Open mission"):
        balancer.assert_can_add(existing, candidate)


def test_assert_can_add_revision_exceeded():
    existing = [
        _m(mission_id=f"r{i}", is_revision=True)
        for i in range(WorkloadPolicy.MAX_REVISION_MISSIONS)
    ]
    candidate = _m(mission_id="new", is_revision=True)
    with pytest.raises(WorkloadExceeded, match="Revision"):
        balancer.assert_can_add(existing, candidate)


def test_assert_can_add_deferred_exceeded():
    existing = [
        _m(mission_id=f"d{i}", slot=MissionSlot.DEFERRED)
        for i in range(WorkloadPolicy.MAX_DEFERRED_MISSIONS)
    ]
    candidate = _m(mission_id="new", slot=MissionSlot.DEFERRED)
    with pytest.raises(WorkloadExceeded, match="Deferred"):
        balancer.assert_can_add(existing, candidate)


def test_assert_can_add_reflections_exceeded():
    candidate = _m(mission_id="new", outstanding_reflections=6)
    with pytest.raises(WorkloadExceeded, match="reflection"):
        balancer.assert_can_add([], candidate)


def test_prefer_continuity_matches_journey():
    existing = [_m(journey_id="journey-1")]
    candidates = [
        _m(mission_id="other", journey_id="journey-2"),
        _m(mission_id="match", journey_id="journey-1"),
    ]
    picked = balancer.prefer_continuity(existing, candidates)
    assert picked is not None
    assert picked.mission_id == "match"


def test_prefer_continuity_fallback_first():
    existing = [_m(journey_id="journey-1")]
    candidates = [_m(mission_id="only", journey_id="journey-99")]
    picked = balancer.prefer_continuity(existing, candidates)
    assert picked.mission_id == "only"


def test_prefer_continuity_empty():
    assert balancer.prefer_continuity([], []) is None


def test_should_defer_new_work_when_over_capacity():
    missions = [
        _m(mission_id=f"m{i}")
        for i in range(WorkloadPolicy.MAX_OPEN_MISSIONS_PER_LEARNER)
    ]
    assert balancer.should_defer_new_work(missions) is True


def test_should_defer_new_work_high_reflections():
    missions = [_m(outstanding_reflections=3)]
    assert balancer.should_defer_new_work(missions) is True


def test_should_defer_new_work_high_effort():
    missions = [_m(effort="intensive") for _ in range(5)]
    assert balancer.should_defer_new_work(missions) is True


def test_should_defer_new_work_false_when_light():
    missions = [_m(effort="minimal")]
    assert balancer.should_defer_new_work(missions) is False


def test_assess_slot_counts():
    missions = [
        _m(slot=MissionSlot.DEFERRED),
        _m(mission_id="m2", slot=MissionSlot.MISSED, scheduled_date=YESTERDAY),
        _m(mission_id="m3", is_revision=True),
        _m(mission_id="m4", slot=MissionSlot.FUTURE, scheduled_date=TOMORROW),
    ]
    assessment = balancer.assess(missions)
    assert assessment.deferred_count == 1
    assert assessment.missed_count == 1
    assert assessment.revision_count == 1
    assert assessment.future_count == 1
