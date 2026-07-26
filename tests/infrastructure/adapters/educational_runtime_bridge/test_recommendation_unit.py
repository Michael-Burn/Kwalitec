"""Unit tests — Recommendation Read Adapter mapping, errors, DTOs."""

from __future__ import annotations

from types import SimpleNamespace

from app.infrastructure.adapters.educational_runtime_bridge import (
    AUTHORITY_RECOMMENDATION_BRIDGE,
    FORBIDDEN,
    NOT_FOUND,
    RECOMMENDATION_BRIDGE_FAILURE,
    RECOMMENDATION_BRIDGE_LATENCY,
    RECOMMENDATION_BRIDGE_REQUESTED,
    RECOMMENDATION_BRIDGE_SUCCESS,
    UNAVAILABLE,
    BridgeResult,
    RecommendationAdapter,
    map_recommendation_to_projection,
)
from app.infrastructure.events.registry import EventRegistry


def test_map_recommendation_mission_aligned():
    mission = SimpleNamespace(id=42, title="Study Probability", user_id=1)
    primary = {
        "title": "Clear your review backlog (2 overdue)",
        "category": "Review",
        "priority": "Critical",
        "reason": "You have 2 topic(s) overdue for review.",
        "expected_benefit": "Restore retention.",
        "generated_at": "2026-07-25T10:00:00",
    }
    projection = map_recommendation_to_projection(
        student_id="1",
        mission=mission,
        primary=primary,
        alternatives=[
            {
                "title": "Improve Estimated Knowledge: Algebra",
                "category": "Weak Topic",
                "priority": "High",
                "reason": "Practice Algebra.",
                "expected_benefit": "Strengthen Algebra.",
            }
        ],
        topic_code="1.1",
        estimated_minutes=45,
    )
    assert projection is not None
    assert projection["mission_aligned"] is True
    assert projection["topic_title"] == "Study Probability"
    assert projection["recommendation_label"] == "Study Probability"
    assert projection["title"] == "Study Probability"
    assert projection["mission_id"] == "42"
    assert projection["authority"] == AUTHORITY_RECOMMENDATION_BRIDGE
    assert projection["next_action_authority"] is True
    assert projection["estimated_minutes"] == 45
    assert projection["topic_code"] == "1.1"
    assert "overdue" in projection["summary"]
    assert projection["alternatives"][0]["title"].startswith("Improve")
    assert projection["decision_id"] == "rec-mission-42"


def test_map_recommendation_narrative_only_without_mission():
    primary = {
        "title": "Take a mock exam this week",
        "category": "Mock Exam",
        "priority": "Medium",
        "reason": "Estimated readiness supports a mock exam.",
        "expected_benefit": "Reveal gaps.",
        "generated_at": "2026-07-25T10:00:00",
    }
    projection = map_recommendation_to_projection(
        student_id="9",
        mission=None,
        primary=primary,
        alternatives=[],
    )
    assert projection is not None
    assert projection["mission_aligned"] is False
    assert projection["mission_id"] is None
    assert projection["title"] == "Take a mock exam this week"
    assert projection["authority"] == AUTHORITY_RECOMMENDATION_BRIDGE


def test_map_recommendation_empty_returns_none():
    assert (
        map_recommendation_to_projection(
            student_id="1", mission=None, primary=None, alternatives=[]
        )
        is None
    )


def test_adapter_forbidden_for_non_numeric_student_id():
    events = EventRegistry()
    adapter = RecommendationAdapter(events=events)
    result = adapter.get_todays_recommendation("not-a-user")
    assert isinstance(result, BridgeResult)
    assert result.ok is False
    assert result.error_code == FORBIDDEN
    assert result.value is None
    types = [e.event_type for e in events.published()]
    assert RECOMMENDATION_BRIDGE_REQUESTED in types
    assert RECOMMENDATION_BRIDGE_FAILURE in types
    assert RECOMMENDATION_BRIDGE_LATENCY in types


def test_adapter_empty_when_no_mission_and_no_recs():
    events = EventRegistry()

    class _RecSvc:
        @staticmethod
        def generate_recommendations(user_id, limit=5):
            return []

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return None

    adapter = RecommendationAdapter(
        events=events,
        recommendation_service=_RecSvc,
        mission_service=_MissionSvc,
    )
    result = adapter.get_todays_recommendation("9")
    assert result.ok is True
    assert result.value is None
    assert result.error_code == NOT_FOUND
    types = [e.event_type for e in events.published()]
    assert RECOMMENDATION_BRIDGE_SUCCESS in types
    assert RECOMMENDATION_BRIDGE_FAILURE not in types


def test_adapter_mission_aligned_projection():
    events = EventRegistry()
    mission = SimpleNamespace(id=7, title="Practice Distributions", user_id=5)

    class _RecSvc:
        @staticmethod
        def generate_recommendations(user_id, limit=5):
            return [
                {
                    "title": "Clear your review backlog (1 overdue)",
                    "category": "Review",
                    "priority": "Critical",
                    "reason": "One topic overdue.",
                    "expected_benefit": "Restore retention.",
                    "generated_at": "2026-07-25T10:00:00",
                }
            ]

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return mission

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return SimpleNamespace(preferred_session_minutes=40)

    adapter = RecommendationAdapter(
        events=events,
        recommendation_service=_RecSvc,
        mission_service=_MissionSvc,
        study_plan_service=_PlanSvc,
    )
    result = adapter.get_todays_recommendation("5")
    assert result.ok is True
    assert result.value is not None
    assert result.value["mission_aligned"] is True
    assert result.value["topic_title"] == "Practice Distributions"
    assert result.value["mission_id"] == "7"
    assert result.value["estimated_minutes"] == 40
    assert result.fallback_used is False
    types = [e.event_type for e in events.published()]
    assert RECOMMENDATION_BRIDGE_SUCCESS in types


def test_adapter_estimated_minutes_agrees_with_mission_on_weekend():
    """B3 (PX-003): Home's duration must not diverge from Mission's on
    weekend days when no ``preferred_session_minutes`` is set — both must
    resolve through the same call path with the same calendar day."""
    from datetime import date

    from app.application.student_experience.session_duration import (
        resolve_planned_session_minutes,
    )

    events = EventRegistry()
    saturday = date(2026, 8, 1)
    assert saturday.weekday() == 5  # Saturday
    mission = SimpleNamespace(id=11, title="Weekend Revision", user_id=6)

    class _RecSvc:
        @staticmethod
        def generate_recommendations(user_id, limit=5):
            return []

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return mission

    plan = SimpleNamespace(
        preferred_session_minutes=None,
        weekday_study_minutes=45,
        weekend_study_minutes=90,
    )

    class _PlanSvc:
        @staticmethod
        def get_user_active_plan(user_id):
            return plan

    adapter = RecommendationAdapter(
        events=events,
        recommendation_service=_RecSvc,
        mission_service=_MissionSvc,
        study_plan_service=_PlanSvc,
    )
    result = adapter.get_todays_recommendation("6", as_of_date=saturday)
    assert result.ok is True
    assert result.value is not None
    # Mission's own duration call path for the same day/plan:
    mission_side_minutes = resolve_planned_session_minutes(
        plan, mission_date=saturday
    )
    assert mission_side_minutes == 90
    assert result.value["estimated_minutes"] == mission_side_minutes == 90


def test_adapter_fallback_to_mission_when_rec_service_fails():
    events = EventRegistry()
    mission = SimpleNamespace(id=3, title="Study Algebra", user_id=2)

    class _RecSvc:
        @staticmethod
        def generate_recommendations(user_id, limit=5):
            raise RuntimeError("recommendation boom")

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return mission

    result = RecommendationAdapter(
        events=events,
        recommendation_service=_RecSvc,
        mission_service=_MissionSvc,
    ).get_todays_recommendation("2")
    assert result.ok is True
    assert result.fallback_used is True
    assert result.value is not None
    assert result.value["topic_title"] == "Study Algebra"
    assert result.value["mission_aligned"] is True


def test_adapter_unavailable_when_rec_fails_without_mission():
    events = EventRegistry()

    class _RecSvc:
        @staticmethod
        def generate_recommendations(user_id, limit=5):
            raise RuntimeError("down")

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return None

    result = RecommendationAdapter(
        events=events,
        recommendation_service=_RecSvc,
        mission_service=_MissionSvc,
    ).get_todays_recommendation("2")
    assert result.ok is False
    assert result.error_code == UNAVAILABLE
    types = [e.event_type for e in events.published()]
    assert RECOMMENDATION_BRIDGE_FAILURE in types


def test_adapter_uses_injected_mission_projection():
    class _RecSvc:
        @staticmethod
        def generate_recommendations(user_id, limit=5):
            return []

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            raise AssertionError("must use injected mission projection")

    adapter = RecommendationAdapter(
        recommendation_service=_RecSvc,
        mission_service=_MissionSvc,
    )
    result = adapter.get_todays_recommendation(
        "1",
        mission_projection={
            "mission_id": "99",
            "topic_title": "Injected Topic",
            "topic_code": "2.1",
        },
    )
    assert result.ok is True
    assert result.value["topic_title"] == "Injected Topic"
    assert result.value["mission_id"] == "99"
    assert result.value["topic_code"] == "2.1"
    assert result.value["mission_aligned"] is True


def test_adapter_never_calls_record_decision():
    class _RecSvc:
        @staticmethod
        def generate_recommendations(user_id, limit=5):
            return [
                {
                    "title": "Study next topic",
                    "category": "New Topic",
                    "priority": "High",
                    "reason": "Coverage low.",
                    "expected_benefit": "Increase coverage.",
                    "generated_at": "2026-07-25T10:00:00",
                }
            ]

        @staticmethod
        def record_decision(*args, **kwargs):
            raise AssertionError("read path must not record decisions")

    class _MissionSvc:
        @staticmethod
        def get_today_mission(user_id, mission_date=None):
            return None

    result = RecommendationAdapter(
        recommendation_service=_RecSvc,
        mission_service=_MissionSvc,
    ).get_todays_recommendation("4")
    assert result.ok is True
    assert result.value["title"] == "Study next topic"
