"""Fail-open Learning Feedback emitter tests (EP-003.4)."""

from __future__ import annotations

from app.infrastructure.adapters.learning_feedback import (
    FEEDBACK_EVENT_PLAN_COMPLETED,
    FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
    FEEDBACK_EVENT_RECOMMENDATION_DISMISSED,
    FEEDBACK_EVENT_RECOVERY_APPLIED,
    FEEDBACK_EVENT_SESSION_MISSED,
    FEEDBACK_EVENT_STUDY_CONSISTENCY,
    REASON_FLAG_OFF,
    REASON_FORBIDDEN_INFERENCE,
    RECORD_STATUS_FAILED,
    RECORD_STATUS_RECORDED,
    RECORD_STATUS_SKIPPED,
    LearningFeedbackRecorder,
    bind_learning_feedback_recorder,
    emit_learning_feedback,
    emit_plan_completed_feedback,
    emit_planning_recovery_feedback,
    emit_recommendation_decision_feedback,
    emit_study_consistency_feedback,
)
from app.infrastructure.adapters.learning_feedback.contracts import (
    CLAIM_PREFERENCE_JOURNAL,
    SOURCE_RECOMMENDATION,
)


def setup_function() -> None:
    bind_learning_feedback_recorder(None)


def teardown_function() -> None:
    bind_learning_feedback_recorder(None)


def test_emit_skips_when_flag_off_and_no_recorder():
    result = emit_recommendation_decision_feedback(
        user_id=9,
        accepted=True,
        recommendation_title="Review weak topic",
    )
    assert result.ok is False
    assert result.status == RECORD_STATUS_SKIPPED
    assert result.reason == REASON_FLAG_OFF


def test_emit_records_accept_and_dismiss():
    recorder = LearningFeedbackRecorder(enabled=True)
    bind_learning_feedback_recorder(recorder)
    accepted = emit_recommendation_decision_feedback(
        user_id=3,
        accepted=True,
        recommendation_title="Practice",
        recommendation_category="weak_topic",
        recorder=recorder,
    )
    dismissed = emit_recommendation_decision_feedback(
        user_id=3,
        accepted=False,
        recommendation_title="Practice",
        recommendation_category="weak_topic",
        recorder=recorder,
    )
    assert accepted.ok and accepted.status == RECORD_STATUS_RECORDED
    assert dismissed.ok and dismissed.status == RECORD_STATUS_RECORDED
    types = {e.event_type for e in recorder.list_events()}
    assert FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED in types
    assert FEEDBACK_EVENT_RECOMMENDATION_DISMISSED in types


def test_emit_rejects_forbidden_inference_fail_open():
    recorder = LearningFeedbackRecorder(enabled=True)
    result = emit_learning_feedback(
        student_id=1,
        event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
        source_authority=SOURCE_RECOMMENDATION,
        claim_boundary=CLAIM_PREFERENCE_JOURNAL,
        payload={"accepted": True, "mastery": 88},
        recorder=recorder,
    )
    assert result.ok is False
    assert result.status == RECORD_STATUS_FAILED
    assert result.reason == REASON_FORBIDDEN_INFERENCE
    assert recorder.list_events() == []


def test_emit_planning_recovery_and_plan_completion():
    recorder = LearningFeedbackRecorder(enabled=True)
    results = emit_planning_recovery_feedback(
        user_id=4,
        mission_missed_count=2,
        recovery_mode=True,
        recorder=recorder,
    )
    assert len(results) == 2
    assert all(r.ok for r in results)
    types = {e.event_type for e in recorder.list_events()}
    assert FEEDBACK_EVENT_SESSION_MISSED in types
    assert FEEDBACK_EVENT_RECOVERY_APPLIED in types

    done = emit_plan_completed_feedback(
        user_id=4,
        mission_id=99,
        study_plan_id=7,
        mission_title="Today's Mission",
        recorder=recorder,
    )
    assert done.ok
    assert any(
        e.event_type == FEEDBACK_EVENT_PLAN_COMPLETED
        for e in recorder.list_events()
    )


def test_emit_study_consistency_from_readiness_source():
    recorder = LearningFeedbackRecorder(enabled=True)
    result = emit_study_consistency_feedback(
        user_id=5,
        current_streak=3,
        longest_streak=10,
        recorder=recorder,
    )
    assert result.ok
    event = recorder.list_events()[-1]
    assert event.event_type == FEEDBACK_EVENT_STUDY_CONSISTENCY
    assert event.source_authority == "readiness_service"
    assert event.payload["current_streak"] == 3
    assert "readiness_score" not in event.payload


def test_broken_recorder_does_not_raise():
    class Broken:
        enabled = True

        def record(self, event):  # noqa: ANN001
            raise RuntimeError("boom")

    result = emit_recommendation_decision_feedback(
        user_id=1,
        accepted=True,
        recorder=Broken(),
    )
    assert result.ok is False
    assert result.status == RECORD_STATUS_FAILED
