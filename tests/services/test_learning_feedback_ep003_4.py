"""EP-003.4 Runtime A ownership + emission regression tests."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from app.infrastructure.adapters.learning_feedback import (
    FEEDBACK_EVENT_PLAN_COMPLETED,
    FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
    FEEDBACK_EVENT_STUDY_CONSISTENCY,
    RECORD_STATUS_RECORDED,
    LearningFeedbackRecorder,
    emit_plan_completed_feedback,
    emit_recommendation_decision_feedback,
    emit_study_consistency_feedback,
)
from app.services.planning_service import PlanningService
from app.services.readiness_service import ReadinessService
from app.services.recommendation_service import RecommendationService


def test_recommendation_emit_helper_records_accept():
    recorder = LearningFeedbackRecorder(enabled=True)
    result = emit_recommendation_decision_feedback(
        user_id=11,
        accepted=True,
        recommendation_title="Weak topic drill",
        recommendation_category="Weak Topic",
        recorder=recorder,
    )
    assert result.status == RECORD_STATUS_RECORDED
    assert result.event.event_type == FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED
    assert result.event.source_authority == "recommendation_service"


def test_planning_emit_helper_records_completion():
    recorder = LearningFeedbackRecorder(enabled=True)
    result = emit_plan_completed_feedback(
        user_id=12,
        mission_id=99,
        study_plan_id=3,
        mission_title="Today's Mission",
        recorder=recorder,
    )
    assert result.status == RECORD_STATUS_RECORDED
    assert result.event.event_type == FEEDBACK_EVENT_PLAN_COMPLETED
    assert result.event.source_authority == "planning_service"


def test_readiness_emit_helper_records_consistency():
    recorder = LearningFeedbackRecorder(enabled=True)
    result = emit_study_consistency_feedback(
        user_id=13,
        current_streak=4,
        longest_streak=10,
        recorder=recorder,
    )
    assert result.status == RECORD_STATUS_RECORDED
    assert result.event.event_type == FEEDBACK_EVENT_STUDY_CONSISTENCY
    assert result.event.source_authority == "readiness_service"


def test_recommendation_decision_feedback_hook_fail_open():
    """_emit_decision_feedback must not raise even if emitter blows up."""
    with patch(
        "app.infrastructure.adapters.learning_feedback.emit_recommendation_decision_feedback",
        side_effect=RuntimeError("boom"),
    ):
        RecommendationService._emit_decision_feedback(
            1,
            accepted=True,
            recommendation={"title": "x", "category": "y"},
        )


def test_planning_record_completion_fail_open():
    with patch(
        "app.infrastructure.adapters.learning_feedback.emit_plan_completed_feedback",
        side_effect=RuntimeError("boom"),
    ):
        PlanningService.record_plan_completion_feedback(
            1, mission_id=1, study_plan_id=2, mission_title="t"
        )


def test_planning_daily_plan_feedback_emits_recovery():
    plan = {
        "explainability": {"recovery_mode": True, "mission_missed_count": 2},
        "mission_slots": [{"slot": "review"}, {"slot": "recovery"}],
        "study_plan_id": 9,
    }
    with patch(
        "app.infrastructure.adapters.learning_feedback.emit_planning_recovery_feedback"
    ) as recovery:
        recovery.return_value = []
        PlanningService._emit_daily_plan_feedback(42, plan)
        recovery.assert_called_once_with(
            user_id=42,
            mission_missed_count=2,
            recovery_mode=True,
            correlation_id="9",
        )


def test_planning_completion_can_emit_revision_adherence():
    with patch(
        "app.infrastructure.adapters.learning_feedback.emit_plan_completed_feedback"
    ) as completed, patch(
        "app.infrastructure.adapters.learning_feedback.emit_revision_feedback"
    ) as revision:
        completed.return_value = MagicMock()
        revision.return_value = MagicMock()
        PlanningService.record_plan_completion_feedback(
            7,
            mission_id=3,
            study_plan_id=1,
            mission_title="Review",
            revision_adhered=True,
            revision_slot_count=1,
        )
        completed.assert_called_once()
        revision.assert_called_once()


def test_planning_daily_plan_feedback_fail_open():
    with patch(
        "app.infrastructure.adapters.learning_feedback.emit_planning_recovery_feedback",
        side_effect=RuntimeError("boom"),
    ):
        PlanningService._emit_daily_plan_feedback(
            1,
            {"explainability": {"recovery_mode": True, "mission_missed_count": 1}},
        )


def test_readiness_consistency_feedback_fail_open():
    with patch.object(
        ReadinessService,
        "get_current_streak",
        side_effect=RuntimeError("boom"),
    ):
        ReadinessService._emit_consistency_feedback(1)


def test_overall_readiness_does_not_emit_feedback():
    """Collector-safe path must not call consistency emitter."""
    with patch.object(
        ReadinessService, "_emit_consistency_feedback"
    ) as emit, patch.object(
        ReadinessService,
        "get_curriculum_coverage",
        return_value={
            "coverage_pct": 0,
            "total_topics": 0,
            "topics_started": 0,
            "topics_mastered": 0,
        },
    ), patch.object(
        ReadinessService,
        "get_review_completion_rate",
        return_value={"completion_rate": 0},
    ):
        # get_overall_readiness uses more helpers — if it somehow called emit
        # we would see it. Call through patched internals carefully.
        try:
            ReadinessService.get_overall_readiness(1)
        except Exception:
            pass
        emit.assert_not_called()
