"""Contract tests — Mission Read Bridge interface stability."""

from __future__ import annotations

from datetime import date

import pytest

from app.application.student_experience.ports.mission_port import MissionPort
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_PLANNING_SERVICE,
    BRIDGE_ERROR_CODES,
    MISSION_BRIDGE_EVENT_TYPES,
    BridgeResult,
    MissionReadAdapter,
    MissionReadBridge,
    map_mission_to_todays_session,
)
from app.infrastructure.adapters.mission.experience_adapter import (
    ExperienceMissionAdapter,
)
from app.infrastructure.events.types import EVENT_TYPES

REQUIRED_SESSION_KEYS = frozenset(
    {
        "student_id",
        "mission_id",
        "session_id",
        "topic_code",
        "topic_title",
        "estimated_minutes",
        "status",
        "tasks",
        "lifecycle_stage",
        "authority",
        "next_action_authority",
    }
)


def test_mission_read_adapter_satisfies_bridge_protocol():
    adapter = MissionReadAdapter()
    assert isinstance(adapter, MissionReadBridge)


def test_experience_adapter_with_bridge_still_mission_port():
    adapter = ExperienceMissionAdapter(mission_read=MissionReadAdapter())
    assert isinstance(adapter, MissionPort)


def test_bridge_result_shape():
    empty = BridgeResult(ok=True, value=None, error_code="NOT_FOUND")
    assert empty.ok is True
    assert empty.fallback_used is False
    failed = BridgeResult(ok=False, error_code="UNAVAILABLE", message="x")
    assert failed.value is None


def test_error_codes_catalogue_stable():
    expected = {
        "UNAVAILABLE",
        "NO_ACTIVE_PLAN",
        "OUTSIDE_PLAN_WINDOW",
        "NOT_FOUND",
        "FORBIDDEN",
        "INVALID_STATE",
        "EVIDENCE_REJECTED",
    }
    assert set(BRIDGE_ERROR_CODES) == expected


def test_telemetry_event_types_registered():
    for event_type in MISSION_BRIDGE_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_projection_contract_keys():
    from types import SimpleNamespace

    mission = SimpleNamespace(
        id=1, title="T", status="Pending", tasks=[], user_id=1
    )
    session = map_mission_to_todays_session(mission, student_id="1")
    assert REQUIRED_SESSION_KEYS.issubset(session.keys())
    assert session["authority"] == AUTHORITY_PLANNING_SERVICE
    assert session["next_action_authority"] is False


def test_get_todays_session_signature_accepts_as_of_date():
    adapter = MissionReadAdapter()
    # Non-numeric id → BridgeResult failure without touching SQL.
    result = adapter.get_todays_session("x", as_of_date=date(2026, 1, 1))
    assert isinstance(result, BridgeResult)


def test_bridged_authority_never_demo_seed():
    from types import SimpleNamespace

    mission = SimpleNamespace(
        id=3, title="Syllabus topic", status="Pending", tasks=[], user_id=1
    )
    session = map_mission_to_todays_session(mission, student_id="1")
    assert session["authority"] != "mission_engine"
    assert "seeded" not in session["authority"]
    assert session["authority"] == AUTHORITY_PLANNING_SERVICE


@pytest.mark.parametrize("method", ["get_todays_session"])
def test_bridge_exposes_read_only_surface(method):
    adapter = MissionReadAdapter()
    assert hasattr(adapter, method)
    # Write/ensure APIs are intentionally absent on Mission Read.
    assert not hasattr(adapter, "ensure_today")
    assert not hasattr(adapter, "start_session")
    assert not hasattr(adapter, "complete_session")
