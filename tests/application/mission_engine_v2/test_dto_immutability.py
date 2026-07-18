"""DTO immutability and package export tests."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from types import MappingProxyType

import pytest

from app.application.mission_engine_v2.dto.mission_card import MissionCard
from app.application.mission_engine_v2.dto.mission_dashboard import MissionDashboard
from app.application.mission_engine_v2.dto.mission_execution import MissionExecution
from app.application.mission_engine_v2.dto.mission_timeline import MissionTimeline
from app.application.mission_engine_v2.lifecycle import (
    DispatchAction,
    MissionSlot,
    MissionState,
)
from app.application.mission_engine_v2.workload_balancer import WorkloadAssessment
from tests.application.mission_engine_v2.helpers import TODAY, make_mission


def test_daily_mission_frozen():
    mission = make_mission()
    with pytest.raises(FrozenInstanceError):
        mission.title = "changed"  # type: ignore[misc]


def test_mission_card_frozen():
    card = MissionCard(
        mission_id="m1",
        learner_id="l1",
        journey_id="j1",
        session_id="s1",
        topic_id="t1",
        scheduled_date=TODAY,
        slot=MissionSlot.TODAY,
        state=MissionState.READY,
        title="T",
        effort="medium",
        dispatch_action=DispatchAction.TODAY,
        is_active=False,
        is_completed=False,
        is_resume=False,
        is_revision=False,
        objective_id="o1",
        sequence_index=0,
    )
    with pytest.raises(FrozenInstanceError):
        card.title = "x"  # type: ignore[misc]


def test_mission_execution_payload_proxy():
    payload = MissionExecution.freeze_payload({"a": "1"})
    assert isinstance(payload, MappingProxyType)
    with pytest.raises(TypeError):
        payload["a"] = "2"  # type: ignore[index]


def test_mission_execution_frozen():
    execution = MissionExecution(
        mission_id="m1",
        action=DispatchAction.TODAY,
        learner_id="l1",
        journey_id="j1",
        session_id="s1",
        topic_id="t1",
        title="T",
        scheduled_date=TODAY,
        payload=MissionExecution.freeze_payload({}),
    )
    with pytest.raises(FrozenInstanceError):
        execution.title = "x"  # type: ignore[misc]


def test_mission_timeline_frozen():
    mission = make_mission()
    timeline = MissionTimeline(
        learner_id="l1",
        as_of_date=TODAY,
        today=mission,
        deferred=(),
        revision=(),
        missed=(),
        future=(),
        ordered=(mission,),
    )
    with pytest.raises(FrozenInstanceError):
        timeline.learner_id = "x"  # type: ignore[misc]


def test_mission_dashboard_frozen():
    mission = make_mission()
    timeline = MissionTimeline(
        learner_id="l1",
        as_of_date=TODAY,
        today=mission,
        deferred=(),
        revision=(),
        missed=(),
        future=(),
        ordered=(mission,),
    )
    dashboard = MissionDashboard(
        learner_id="l1",
        as_of_date=TODAY,
        today=None,
        deferred=(),
        revision=(),
        missed=(),
        future=(),
        timeline=timeline,
        active_mission_id=None,
        open_mission_count=1,
        workload_ok=True,
    )
    with pytest.raises(FrozenInstanceError):
        dashboard.workload_ok = False  # type: ignore[misc]


def test_workload_assessment_frozen():
    assessment = WorkloadAssessment(
        open_count=0,
        active_count=0,
        deferred_count=0,
        missed_count=0,
        revision_count=0,
        future_count=0,
        effort_load=0,
        outstanding_reflections=0,
        revision_debt=0,
        journey_continuity=False,
        within_limits=True,
        blocking_reasons=(),
    )
    with pytest.raises(FrozenInstanceError):
        assessment.open_count = 1  # type: ignore[misc]


def test_dto_package_exports():
    from app.application.mission_engine_v2 import dto

    for name in ("DailyMission", "MissionCard", "MissionDashboard", "MissionExecution", "MissionTimeline"):  # noqa: E501
        assert name in dto.__all__
        assert hasattr(dto, name)


def test_main_package_exports():
    import app.application.mission_engine_v2 as me

    expected = [
        "MissionEngineV2",
        "DailyMission",
        "MissionState",
        "MissionSlot",
        "DispatchAction",
        "LifecyclePolicy",
        "SchedulingPolicy",
        "WorkloadPolicy",
        "DispatchPolicy",
    ]
    for name in expected:
        assert name in me.__all__
        assert hasattr(me, name)


def test_lazy_export_resolves_same_object():
    import app.application.mission_engine_v2 as me
    from app.application.mission_engine_v2.engine import MissionEngineV2

    assert me.MissionEngineV2 is MissionEngineV2


def test_component_lazy_exports():
    import app.application.mission_engine_v2 as me

    for name in (
        "MissionCoordinator",
        "MissionFactory",
        "MissionScheduler",
        "MissionValidator",
        "MissionDispatcher",
        "WorkloadBalancer",
    ):
        assert hasattr(me, name)


def test_daily_mission_optional_timestamps_default_none():
    mission = make_mission()
    assert mission.completed_at is None
    assert mission.archived_at is None


def test_mission_card_default_explanation_keys():
    card = MissionCard(
        mission_id="m1",
        learner_id="l1",
        journey_id="j1",
        session_id="s1",
        topic_id="t1",
        scheduled_date=TODAY,
        slot=MissionSlot.TODAY,
        state=MissionState.READY,
        title="T",
        effort="medium",
        dispatch_action=DispatchAction.TODAY,
        is_active=False,
        is_completed=False,
        is_resume=False,
        is_revision=False,
        objective_id=None,
        sequence_index=0,
    )
    assert card.explanation_keys == ()


def test_freeze_payload_copies_input():
    data = {"k": "v"}
    frozen = MissionExecution.freeze_payload(data)
    data["k"] = "changed"
    assert frozen["k"] == "v"
