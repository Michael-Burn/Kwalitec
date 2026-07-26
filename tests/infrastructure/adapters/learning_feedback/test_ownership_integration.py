"""Constitutional ownership + service integration tests (EP-003.4)."""

from __future__ import annotations

from datetime import date

from app.infrastructure.adapters.learning_feedback import (
    FEEDBACK_EVENT_PLAN_COMPLETED,
    FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
    FEEDBACK_EVENT_RECOMMENDATION_DISMISSED,
    FEEDBACK_EVENT_RECOVERY_APPLIED,
    FEEDBACK_EVENT_REVISION_ADHERED,
    FEEDBACK_EVENT_SESSION_MISSED,
    FEEDBACK_EVENT_STUDY_CONSISTENCY,
    LearningFeedbackRecorder,
    bind_learning_feedback_recorder,
)
from app.services.planning_service import PlanningService
from app.services.readiness_service import ReadinessService
from app.services.recommendation_service import RecommendationService


def setup_function() -> None:
    bind_learning_feedback_recorder(None)


def teardown_function() -> None:
    bind_learning_feedback_recorder(None)


def test_recommendation_record_decision_emits_preference_feedback(ctx):
    recorder = LearningFeedbackRecorder(enabled=True)
    bind_learning_feedback_recorder(recorder)
    from tests.conftest import _make_user

    user = _make_user()
    recommendation = {
        "title": "Review Fractions",
        "category": "review",
        "priority": "high",
        "reason": "Due review",
        "expected_benefit": "Retention",
        "generated_at": "2026-07-26T09:00:00",
    }
    RecommendationService.record_decision(user.id, recommendation, accepted=True)
    RecommendationService.record_decision(user.id, recommendation, accepted=False)
    types = {e.event_type for e in recorder.list_events(student_id=str(user.id))}
    assert FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED in types
    assert FEEDBACK_EVENT_RECOMMENDATION_DISMISSED in types
    for event in recorder.list_events(student_id=str(user.id)):
        assert event.source_authority == "recommendation_service"
        assert "mastery" not in event.payload


def test_planning_daily_plan_feedback_emits_recovery_only(ctx):
    recorder = LearningFeedbackRecorder(enabled=True)
    bind_learning_feedback_recorder(recorder)
    PlanningService._emit_daily_plan_feedback(
        11,
        {
            "study_plan_id": 5,
            "explainability": {
                "recovery_mode": True,
                "mission_missed_count": 2,
            },
            "mission_slots": [{"slot": "review"}],
        },
    )
    types = {e.event_type for e in recorder.list_events(student_id="11")}
    assert FEEDBACK_EVENT_SESSION_MISSED in types
    assert FEEDBACK_EVENT_RECOVERY_APPLIED in types
    # Offering a review slot must not claim revision adherence.
    assert FEEDBACK_EVENT_REVISION_ADHERED not in types
    for event in recorder.list_events(student_id="11"):
        assert event.source_authority == "planning_service"


def test_planning_completion_feedback_emits_plan_completed(ctx):
    recorder = LearningFeedbackRecorder(enabled=True)
    bind_learning_feedback_recorder(recorder)
    PlanningService.record_plan_completion_feedback(
        12,
        mission_id=44,
        study_plan_id=3,
        mission_title="Revision Focus",
        revision_adhered=True,
        revision_slot_count=1,
    )
    types = {e.event_type for e in recorder.list_events(student_id="12")}
    assert FEEDBACK_EVENT_PLAN_COMPLETED in types
    assert FEEDBACK_EVENT_REVISION_ADHERED in types


def test_readiness_consistency_emit_is_observation_only(ctx, monkeypatch):
    recorder = LearningFeedbackRecorder(enabled=True)
    bind_learning_feedback_recorder(recorder)
    monkeypatch.setattr(
        ReadinessService, "get_current_streak", staticmethod(lambda _uid: 4)
    )
    monkeypatch.setattr(
        ReadinessService, "get_longest_streak", staticmethod(lambda _uid: 9)
    )
    ReadinessService._emit_consistency_feedback(21)
    events = recorder.list_events(student_id="21")
    assert len(events) == 1
    event = events[0]
    assert event.event_type == FEEDBACK_EVENT_STUDY_CONSISTENCY
    assert event.source_authority == "readiness_service"
    assert event.payload == {"current_streak": 4, "longest_streak": 9}
    assert "readiness_score" not in event.payload


def test_feedback_failures_do_not_break_decision_recording(ctx, monkeypatch):
    class Boom:
        enabled = True

        def record(self, event):  # noqa: ANN001
            raise RuntimeError("storage down")

    bind_learning_feedback_recorder(Boom())
    from tests.conftest import _make_user

    user = _make_user()
    recommendation = {
        "title": "Keep going",
        "category": "motivation",
        "priority": "medium",
        "reason": "Consistency",
        "expected_benefit": "Habit",
        "generated_at": date.today().isoformat(),
    }
    decision = RecommendationService.record_decision(
        user.id, recommendation, accepted=True
    )
    assert decision is not None
    assert decision.accepted is True


def test_presentation_adapter_is_not_allowed_source():
    """RuntimeAPresentationAdapter must not be a feedback source authority."""
    from app.infrastructure.adapters.learning_feedback.contracts import (
        ALLOWED_SOURCE_AUTHORITIES,
    )

    assert "runtime_a_presentation_adapter" not in ALLOWED_SOURCE_AUTHORITIES
    assert "presentation" not in ALLOWED_SOURCE_AUTHORITIES
    assert ALLOWED_SOURCE_AUTHORITIES == frozenset(
        {
            "recommendation_service",
            "readiness_service",
            "planning_service",
        }
    )
