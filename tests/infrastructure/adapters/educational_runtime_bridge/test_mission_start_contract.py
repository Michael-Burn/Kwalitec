"""Contract tests — Mission Start Bridge interface stability."""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace

import pytest

from app.application.student_experience.ports.mission_port import MissionPort
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_STUDY_SESSION_SERVICE,
    BRIDGE_ERROR_CODES,
    MISSION_START_BRIDGE_EVENT_TYPES,
    BridgeResult,
    MissionStartAdapter,
    MissionStartBridge,
    map_mission_to_start_result,
)
from app.infrastructure.adapters.mission.experience_adapter import (
    ExperienceMissionAdapter,
)
from app.infrastructure.events.types import EVENT_TYPES

REQUIRED_START_KEYS = frozenset(
    {
        "student_id",
        "mission_id",
        "session_id",
        "experience_session_id",
        "topic_title",
        "estimated_minutes",
        "started_at",
        "status",
        "authority",
        "next_action_authority",
    }
)


def test_mission_start_adapter_satisfies_bridge_protocol():
    adapter = MissionStartAdapter()
    assert isinstance(adapter, MissionStartBridge)


def test_experience_adapter_with_start_bridge_still_mission_port():
    adapter = ExperienceMissionAdapter(mission_start=MissionStartAdapter())
    assert isinstance(adapter, MissionPort)


def test_error_codes_catalogue_includes_invalid_state():
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


def test_start_telemetry_event_types_registered():
    for event_type in MISSION_START_BRIDGE_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_start_result_contract_keys():
    mission = SimpleNamespace(id=1, title="T", user_id=1)
    started = map_mission_to_start_result(mission, student_id="1")
    assert REQUIRED_START_KEYS.issubset(started.keys())
    assert started["authority"] == AUTHORITY_STUDY_SESSION_SERVICE
    assert started["status"] == "in_progress"
    assert started["next_action_authority"] is False


def test_start_session_signature_accepts_as_of_date():
    adapter = MissionStartAdapter()
    result = adapter.start_session("x", as_of_date=date(2026, 1, 1))
    assert isinstance(result, BridgeResult)


def test_bridged_start_authority_never_demo_seed():
    mission = SimpleNamespace(id=3, title="Syllabus topic", user_id=1)
    started = map_mission_to_start_result(mission, student_id="1")
    assert started["authority"] != "mission_engine"
    assert "seeded" not in started["authority"]
    assert started["authority"] == AUTHORITY_STUDY_SESSION_SERVICE


@pytest.mark.parametrize("method", ["start_session"])
def test_bridge_exposes_start_surface_only(method):
    adapter = MissionStartAdapter()
    assert hasattr(adapter, method)
    # Resume / complete are intentionally absent on Mission Start.
    assert not hasattr(adapter, "get_session_status")
    assert not hasattr(adapter, "complete_session")
    assert not hasattr(adapter, "resume_session")
