"""Contract tests — Journey Read Bridge interface stability."""

from __future__ import annotations

from datetime import date

from app.application.student_experience.ports.learning_journey_port import (
    LearningJourneyPort,
)
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_JOURNEY_BRIDGE,
    BRIDGE_ERROR_CODES,
    JOURNEY_BRIDGE_EVENT_TYPES,
    BridgeResult,
    JourneyAdapter,
    JourneyBridge,
    empty_authentic_journey,
    map_journey_to_projection,
)
from app.infrastructure.adapters.journey import ExperienceJourneyAdapter
from app.infrastructure.events.types import EVENT_TYPES

REQUIRED_JOURNEY_KEYS = frozenset(
    {
        "student_id",
        "has_journey",
        "progress",
        "topics",
        "active_missions",
        "completed_sessions_summary",
        "timeline",
        "recommendation_focus",
        "recommendation_history",
        "authority",
        "next_action_authority",
    }
)

REQUIRED_PROGRESS_KEYS = frozenset(
    {
        "overall_progress_ratio",
        "estimated_completion_label",
        "examination_label",
        "current_topic_id",
        "current_topic_title",
        "lifecycle_stage",
    }
)

REQUIRED_TRACE_KEYS = frozenset({"what", "why", "evidence_refs", "recommendation"})


def test_journey_adapter_satisfies_bridge_protocol():
    adapter = JourneyAdapter()
    assert isinstance(adapter, JourneyBridge)


def test_experience_adapter_with_bridge_still_journey_port():
    adapter = ExperienceJourneyAdapter(journey_read=JourneyAdapter())
    assert isinstance(adapter, LearningJourneyPort)


def test_bridge_result_shape():
    empty = BridgeResult(ok=True, value=None, error_code="NO_ACTIVE_PLAN")
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
    for event_type in JOURNEY_BRIDGE_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_projection_contract_keys():
    projection = map_journey_to_projection(
        student_id="1",
        has_journey=True,
        overall_progress_ratio=0.25,
        examination_label="IFoA CM1",
        topics=[],
        timeline=[],
        recommendation_history=None,
    )
    assert REQUIRED_JOURNEY_KEYS.issubset(projection.keys())
    assert REQUIRED_PROGRESS_KEYS.issubset(projection["progress"].keys())
    assert projection["authority"] == AUTHORITY_JOURNEY_BRIDGE
    assert projection["next_action_authority"] is False
    assert projection["recommendation_history"] is None


def test_empty_authentic_contract_keys():
    doc = empty_authentic_journey(student_id="3", error_code="NO_ACTIVE_PLAN")
    assert REQUIRED_JOURNEY_KEYS.issubset(doc.keys())
    assert doc["has_journey"] is False
    assert doc["authority"] == AUTHORITY_JOURNEY_BRIDGE


def test_timeline_item_requires_trace():
    from app.infrastructure.adapters.educational_runtime_bridge import (
        map_timeline_item,
    )

    item = map_timeline_item(
        event_id="session-completed-1",
        event_type="SessionCompleted",
        student_id="1",
        occurred_at="2026-07-25",
        summary="Completed session",
        authority="study_session_service",
        mission_id="1",
    )
    assert REQUIRED_TRACE_KEYS.issubset(item["trace"].keys())
    assert item["trace"]["recommendation"]["unavailable_reason"] == "unavailable"


def test_project_journey_signature_accepts_as_of_date():
    adapter = JourneyAdapter()
    result = adapter.project_journey("x", as_of_date=date(2026, 1, 1))
    assert isinstance(result, BridgeResult)


def test_bridged_authority_never_demo_seed():
    projection = map_journey_to_projection(
        student_id="1",
        has_journey=True,
        overall_progress_ratio=0.0,
        current_topic_title="Probability",
    )
    assert projection["authority"] == AUTHORITY_JOURNEY_BRIDGE
    assert projection["authority"] != "learning_journey"
    assert projection["progress"]["current_topic_title"] != "Core methods"
