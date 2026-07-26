"""Contract tests — Recommendation Read Bridge interface stability."""

from __future__ import annotations

from datetime import date

from app.application.student_experience.ports.adaptive_decision_port import (
    AdaptiveDecisionPort,
)
from app.infrastructure.adapters.adaptive import ExperienceAdaptiveAdapter
from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_RECOMMENDATION_BRIDGE,
    BRIDGE_ERROR_CODES,
    RECOMMENDATION_BRIDGE_EVENT_TYPES,
    BridgeResult,
    RecommendationAdapter,
    RecommendationBridge,
    map_recommendation_to_projection,
)
from app.infrastructure.events.types import EVENT_TYPES

REQUIRED_RECOMMENDATION_KEYS = frozenset(
    {
        "student_id",
        "decision_id",
        "recommendation_label",
        "title",
        "topic_code",
        "topic_title",
        "summary",
        "explanation",
        "alternatives",
        "authority",
        "next_action_authority",
        "mission_aligned",
        "mission_id",
    }
)


def test_recommendation_adapter_satisfies_bridge_protocol():
    adapter = RecommendationAdapter()
    assert isinstance(adapter, RecommendationBridge)


def test_experience_adapter_with_bridge_still_adaptive_port():
    adapter = ExperienceAdaptiveAdapter(
        recommendation_read=RecommendationAdapter()
    )
    assert isinstance(adapter, AdaptiveDecisionPort)


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
    for event_type in RECOMMENDATION_BRIDGE_EVENT_TYPES:
        assert event_type in EVENT_TYPES


def test_projection_contract_keys():
    from types import SimpleNamespace

    mission = SimpleNamespace(id=1, title="T", user_id=1)
    projection = map_recommendation_to_projection(
        student_id="1",
        mission=mission,
        primary={
            "title": "Narrative",
            "category": "Review",
            "priority": "High",
            "reason": "Because",
            "expected_benefit": "Benefit",
        },
    )
    assert projection is not None
    assert REQUIRED_RECOMMENDATION_KEYS.issubset(projection.keys())
    assert projection["authority"] == AUTHORITY_RECOMMENDATION_BRIDGE
    assert projection["next_action_authority"] is True
    assert projection["explanation"]["authority"] == AUTHORITY_RECOMMENDATION_BRIDGE


def test_get_todays_recommendation_signature_accepts_as_of_date():
    adapter = RecommendationAdapter()
    result = adapter.get_todays_recommendation("x", as_of_date=date(2026, 1, 1))
    assert isinstance(result, BridgeResult)


def test_bridged_authority_never_demo_seed():
    from types import SimpleNamespace

    mission = SimpleNamespace(id=3, title="Syllabus topic", user_id=1)
    projection = map_recommendation_to_projection(
        student_id="1",
        mission=mission,
        primary=None,
    )
    assert projection is not None
    assert projection["authority"] == AUTHORITY_RECOMMENDATION_BRIDGE
    assert projection["authority"] != "adaptive_decision_engine"
    assert projection["topic_title"] == "Syllabus topic"
    assert projection["topic_title"] != "Core methods"
