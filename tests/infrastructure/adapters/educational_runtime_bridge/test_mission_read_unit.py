"""Unit tests — Mission Read Adapter mapping, errors, DTOs."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_PLANNING_SERVICE,
    FORBIDDEN,
    MISSION_BRIDGE_FAILURE,
    MISSION_BRIDGE_LATENCY,
    MISSION_BRIDGE_REQUESTED,
    MISSION_BRIDGE_SUCCESS,
    NO_ACTIVE_PLAN,
    NOT_FOUND,
    OUTSIDE_PLAN_WINDOW,
    UNAVAILABLE,
    BridgeResult,
    MissionReadAdapter,
    map_mission_status,
    map_mission_to_todays_session,
)
from app.infrastructure.events.registry import EventRegistry


def test_map_mission_status_values():
    assert map_mission_status("Pending") == "ready"
    assert map_mission_status("In Progress") == "in_progress"
    assert map_mission_status("Completed") == "completed"
    assert map_mission_status(None) == "ready"


def test_map_mission_to_todays_session_dto():
    task = SimpleNamespace(
        id=7, title="Read", description="Ch 1", order=0, completed=False
    )
    mission = SimpleNamespace(
        id=42,
        title="Study Probability",
        status="Pending",
        tasks=[task],
        user_id=1,
    )
    session = map_mission_to_todays_session(
        mission,
        student_id="1",
        lifecycle_stage="learning",
        topic_code="1.1",
        estimated_minutes=45,
    )
    assert session["mission_id"] == "42"
    assert session["session_id"] == "42"
    assert session["topic_title"] == "Study Probability"
    assert session["topic_code"] == "1.1"
    assert session["status"] == "ready"
    assert session["estimated_minutes"] == 45
    assert session["lifecycle_stage"] == "learning"
    assert session["authority"] == AUTHORITY_PLANNING_SERVICE
    assert session["next_action_authority"] is False
    assert session["tasks"][0]["id"] == "7"
    assert session["tasks"][0]["title"] == "Read"


def test_adapter_forbidden_for_non_numeric_student_id():
    events = EventRegistry()
    adapter = MissionReadAdapter(events=events)
    result = adapter.get_todays_session("not-a-user")
    assert isinstance(result, BridgeResult)
    assert result.ok is False
    assert result.error_code == FORBIDDEN
    assert result.value is None
    types = [e.event_type for e in events.published()]
    assert MISSION_BRIDGE_REQUESTED in types
    assert MISSION_BRIDGE_FAILURE in types
    assert MISSION_BRIDGE_LATENCY in types


def test_adapter_no_active_plan_contract():
    events = EventRegistry()

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return None

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return None

        @staticmethod
        def get_current_week_plan(plan):
            return None

    adapter = MissionReadAdapter(
        events=events,
        mission_service=_MissionSvc,
        study_plan_service=_PlanSvc,
    )
    result = adapter.get_todays_session("9")
    assert result.ok is True
    assert result.value is None
    assert result.error_code == NO_ACTIVE_PLAN
    assert result.fallback_used is False
    types = [e.event_type for e in events.published()]
    assert MISSION_BRIDGE_SUCCESS in types
    assert MISSION_BRIDGE_FAILURE not in types


def test_adapter_outside_window_contract():
    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return None

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1)

        @staticmethod
        def get_current_week_plan(plan):
            return None

    adapter = MissionReadAdapter(
        mission_service=_MissionSvc,
        study_plan_service=_PlanSvc,
    )
    result = adapter.get_todays_session("3")
    assert result.ok is True
    assert result.value is None
    assert result.error_code == OUTSIDE_PLAN_WINDOW


def test_adapter_not_found_when_plan_exists():
    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return None

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1, preferred_session_minutes=60)

        @staticmethod
        def get_current_week_plan(plan):
            return SimpleNamespace(id=10)

    adapter = MissionReadAdapter(
        mission_service=_MissionSvc,
        study_plan_service=_PlanSvc,
    )
    result = adapter.get_todays_session("3")
    assert result.ok is True
    assert result.error_code == NOT_FOUND


def test_adapter_maps_mission_success():
    events = EventRegistry()
    mission = SimpleNamespace(
        id=99,
        user_id=5,
        title="Practice Distributions",
        status="In Progress",
        tasks=[],
    )

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            assert user_id == 5
            return mission

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(id=1, preferred_session_minutes=30)

        @staticmethod
        def get_current_week_plan(plan):
            return SimpleNamespace(id=1)

    class _Lifecycle:
        @staticmethod
        def resolve(user_id, today=None, study_plan=None):
            return SimpleNamespace(stage="learning")

    adapter = MissionReadAdapter(
        events=events,
        mission_service=_MissionSvc,
        study_plan_service=_PlanSvc,
        learning_lifecycle_service=_Lifecycle,
    )
    result = adapter.get_todays_session("5")
    assert result.ok is True
    assert result.value is not None
    assert result.value["mission_id"] == "99"
    assert result.value["status"] == "in_progress"
    assert result.value["authority"] == AUTHORITY_PLANNING_SERVICE
    assert result.value["estimated_minutes"] == 30
    assert result.value["lifecycle_stage"] == "learning"
    types = [e.event_type for e in events.published()]
    assert MISSION_BRIDGE_REQUESTED in types
    assert MISSION_BRIDGE_SUCCESS in types
    assert MISSION_BRIDGE_LATENCY in types


def test_adapter_unavailable_on_service_exception():
    events = EventRegistry()

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            raise RuntimeError("db down")

    adapter = MissionReadAdapter(events=events, mission_service=_MissionSvc)
    result = adapter.get_todays_session("1")
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
    assert result.fallback_used is False
    types = [e.event_type for e in events.published()]
    assert MISSION_BRIDGE_FAILURE in types


def test_adapter_ownership_mismatch_forbidden():
    mission = SimpleNamespace(
        id=1, user_id=999, title="x", status="Pending", tasks=[]
    )

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return mission

    adapter = MissionReadAdapter(mission_service=_MissionSvc)
    result = adapter.get_todays_session("1")
    assert result.ok is False
    assert result.error_code == FORBIDDEN


def test_opaque_entry_returns_none_on_failure():
    adapter = MissionReadAdapter()
    assert adapter.get_todays_session_opaque("bad") is None


@pytest.mark.parametrize(
    "code",
    [UNAVAILABLE, NO_ACTIVE_PLAN, OUTSIDE_PLAN_WINDOW, NOT_FOUND, FORBIDDEN],
)
def test_error_codes_stable(code):
    assert isinstance(code, str)
    assert code
