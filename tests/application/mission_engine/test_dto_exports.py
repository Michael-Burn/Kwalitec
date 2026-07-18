"""DTO immutability and export tests for Mission Engine 2.0."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import UTC, date, datetime
from types import MappingProxyType

import pytest

from app.application import mission_engine as pkg
from app.application.mission_engine.dto.daily_mission import DailyMission
from app.application.mission_engine.dto.mission_delivery import MissionDelivery
from app.application.mission_engine.dto.mission_schedule import MissionSchedule
from app.application.mission_engine.dto.mission_summary import MissionSummary
from app.application.mission_engine.mission_state import (
    DeliveryAction,
    MissionSlot,
    MissionState,
)


def _mission(**overrides) -> DailyMission:
    base = dict(
        mission_id="m1",
        learner_id="l1",
        journey_id="j1",
        session_id="s1",
        topic_id="t1",
        curriculum_id="c1",
        scheduled_date=date(2026, 7, 18),
        slot=MissionSlot.TODAY,
        state=MissionState.ACTIVE,
        objective_id="o1",
        effort="medium",
        title="Title",
        sequence_index=0,
        is_resume=False,
        is_revision=False,
        created_at=datetime(2026, 7, 18, tzinfo=UTC),
    )
    base.update(overrides)
    return DailyMission(**base)


def test_daily_mission_frozen():
    m = _mission()
    with pytest.raises(FrozenInstanceError):
        m.title = "x"  # type: ignore[misc]


def test_mission_summary_frozen():
    s = MissionSummary(
        mission_id="m1",
        learner_id="l1",
        journey_id="j1",
        session_id="s1",
        topic_id="t1",
        scheduled_date=date(2026, 7, 18),
        slot=MissionSlot.TODAY,
        state=MissionState.ACTIVE,
        title="T",
        delivery_action=DeliveryAction.TODAY,
        is_active=True,
        is_completed=False,
        is_resume=False,
        is_revision=False,
        objective_id="o1",
        effort="medium",
    )
    with pytest.raises(FrozenInstanceError):
        s.title = "x"  # type: ignore[misc]


def test_mission_schedule_frozen():
    sched = MissionSchedule(
        learner_id="l1",
        as_of_date=date(2026, 7, 18),
        today=None,
        tomorrow=None,
        deferred=(),
        missed=(),
        revision=(),
        ordered=(),
    )
    with pytest.raises(FrozenInstanceError):
        sched.today = _mission()  # type: ignore[misc]


def test_mission_delivery_frozen_and_payload_immutable():
    d = MissionDelivery(
        mission_id="m1",
        action=DeliveryAction.TODAY,
        learner_id="l1",
        journey_id="j1",
        session_id="s1",
        topic_id="t1",
        title="T",
        scheduled_date=date(2026, 7, 18),
        payload=MissionDelivery.freeze_payload({"a": "1"}),
    )
    with pytest.raises(FrozenInstanceError):
        d.title = "x"  # type: ignore[misc]
    assert isinstance(d.payload, MappingProxyType)
    with pytest.raises(TypeError):
        d.payload["a"] = "2"  # type: ignore[index]


def test_freeze_payload_defaults_empty():
    p = MissionDelivery.freeze_payload()
    assert dict(p) == {}


def test_freeze_payload_copies_input():
    src = {"k": "v"}
    p = MissionDelivery.freeze_payload(src)
    src["k"] = "changed"
    assert p["k"] == "v"


@pytest.mark.parametrize(
    "name",
    [
        "DailyMission",
        "MissionSummary",
        "MissionSchedule",
        "MissionDelivery",
        "MissionEngine",
        "MissionBuilder",
        "MissionScheduler",
        "MissionCoordinator",
        "MissionDispatcher",
        "MissionArchive",
        "MissionValidator",
        "SchedulingPolicy",
        "WorkloadPolicy",
        "DeliveryPolicy",
        "MissionState",
        "MissionSlot",
        "DeliveryAction",
        "V1MissionAdapter",
        "V1MissionView",
        "DuplicateMission",
        "ActiveMissionExists",
        "MissionNotFound",
    ],
)
def test_package_exports(name):
    assert hasattr(pkg, name)
    assert getattr(pkg, name) is not None


def test_package_dir_includes_exports():
    names = dir(pkg)
    assert "MissionEngine" in names
    assert "DailyMission" in names


def test_unknown_export_raises():
    with pytest.raises(AttributeError):
        _ = pkg.DoesNotExist  # type: ignore[attr-defined]


def test_daily_mission_equality():
    a = _mission()
    b = _mission()
    assert a == b


def test_daily_mission_inequality_on_id():
    assert _mission(mission_id="a") != _mission(mission_id="b")


def test_schedule_tuple_fields_immutable_identity():
    m = _mission()
    sched = MissionSchedule(
        learner_id="l1",
        as_of_date=date(2026, 7, 18),
        today=m,
        tomorrow=None,
        deferred=(m,),
        missed=(),
        revision=(),
        ordered=(m,),
    )
    assert sched.deferred[0] is m
    assert sched.ordered == (m,)
