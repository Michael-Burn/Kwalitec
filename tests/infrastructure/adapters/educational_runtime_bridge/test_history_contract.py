"""Contract tests — History Read Bridge interface stability."""

from __future__ import annotations

from datetime import date

from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_HISTORY_BRIDGE,
    BRIDGE_ERROR_CODES,
    HARD_MAX_PAGE_LIMIT,
    HISTORY_BRIDGE_EVENT_TYPES,
    BridgeResult,
    HistoryAdapter,
    HistoryBridge,
    empty_authentic_history,
    map_history_to_projection,
    map_page_meta,
)
from app.infrastructure.events.types import EVENT_TYPES

REQUIRED_HISTORY_KEYS = frozenset(
    {
        "student_id",
        "completed_sessions",
        "total_study_minutes",
        "readiness_progression",
        "mastered_topics",
        "revision_history",
        "recent_achievements",
        "session_count",
        "mastered_count",
        "recommendation_history",
        "page",
        "authority",
    }
)

REQUIRED_PAGE_KEYS = frozenset({"limit", "offset", "has_more"})

REQUIRED_SESSION_KEYS = frozenset(
    {
        "session_id",
        "mission_id",
        "topic_title",
        "completed_at",
        "study_minutes",
    }
)

REQUIRED_TRACE_KEYS = frozenset({"what", "why", "evidence_refs", "recommendation"})


def test_history_adapter_satisfies_bridge_protocol():
    adapter = HistoryAdapter()
    assert isinstance(adapter, HistoryBridge)


def test_bridge_result_shape():
    empty = BridgeResult(ok=True, value=None, error_code="NOT_FOUND")
    assert empty.ok is True
    assert empty.fallback_used is False


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
    for event_type in HISTORY_BRIDGE_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_projection_contract_keys():
    projection = map_history_to_projection(
        student_id="1",
        completed_sessions=[],
        recommendation_history=None,
        readiness_progression=None,
        page=map_page_meta(limit=20, offset=0, has_more=False),
    )
    assert REQUIRED_HISTORY_KEYS.issubset(projection.keys())
    assert REQUIRED_PAGE_KEYS.issubset(projection["page"].keys())
    assert projection["authority"] == AUTHORITY_HISTORY_BRIDGE
    assert projection["recommendation_history"] is None
    assert projection["readiness_progression"] is None
    assert projection["recommendation_history_meta"]["unavailable_reason"] == (
        "unavailable"
    )


def test_empty_authentic_contract_keys():
    doc = empty_authentic_history(student_id="3")
    assert REQUIRED_HISTORY_KEYS.issubset(doc.keys())
    assert doc["authority"] == AUTHORITY_HISTORY_BRIDGE
    assert doc["session_count"] == 0


def test_completed_session_trace_contract():
    from app.infrastructure.adapters.educational_runtime_bridge import (
        map_completed_session,
        session_trace_for_mission,
    )

    card = map_completed_session(
        session_id="1",
        mission_id="1",
        topic_title="Probability",
        completed_at="2026-07-25",
        study_minutes=20,
        trace=session_trace_for_mission(
            topic_title="Probability",
            mission_id="1",
            attempt_ids=["9"],
        ),
    )
    assert REQUIRED_SESSION_KEYS.issubset(card.keys())
    assert REQUIRED_TRACE_KEYS.issubset(card["trace"].keys())
    assert card["trace"]["recommendation"]["unavailable_reason"] == "unavailable"


def test_project_history_signature_accepts_pagination_and_filters():
    adapter = HistoryAdapter()
    result = adapter.project_history(
        "x",
        limit=5,
        offset=0,
        cursor=None,
        from_date=date(2026, 1, 1),
        to_date=date(2026, 12, 31),
        event_types=["SessionCompleted"],
        lifecycle_stage="learning",
        topic_code=None,
    )
    assert isinstance(result, BridgeResult)


def test_hard_max_page_limit_is_100():
    assert HARD_MAX_PAGE_LIMIT == 100


def test_bridged_authority_never_demo_seed():
    projection = map_history_to_projection(student_id="1")
    assert projection["authority"] == AUTHORITY_HISTORY_BRIDGE
    assert projection["authority"] != "student_digital_twin"
