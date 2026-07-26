"""LearningFeedbackRecorder behaviour tests (EP-003.4)."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.learning_feedback import (
    CLAIM_PREFERENCE_JOURNAL,
    FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
    REASON_FLAG_OFF,
    RECORD_STATUS_RECORDED,
    RECORD_STATUS_SKIPPED,
    SOURCE_RECOMMENDATION,
    LearningFeedbackEvent,
    LearningFeedbackRecorder,
    bind_learning_feedback_recorder,
    build_learning_feedback_recorder,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status


def _event(*, student_id: str = "1") -> LearningFeedbackEvent:
    return LearningFeedbackEvent(
        feedback_id="lfeed-test-1",
        timestamp="2026-07-26T10:00:00Z",
        event_type=FEEDBACK_EVENT_RECOMMENDATION_ACCEPTED,
        source_authority=SOURCE_RECOMMENDATION,
        claim_boundary=CLAIM_PREFERENCE_JOURNAL,
        student_id=student_id,
        payload={"accepted": True},
    )


def test_learning_feedback_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_LEARNING_FEEDBACK is False
    dual = build_dual_run_status(flags=flags)
    assert dual.learning_feedback is False
    assert build_learning_feedback_recorder(enabled=False) is None


def test_learning_feedback_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_LEARNING_FEEDBACK": "1"})
    assert flags.ENABLE_LEARNING_FEEDBACK is True
    dual = build_dual_run_status(flags=flags)
    assert dual.learning_feedback is True


def test_recorder_appends_observed_events():
    recorder = LearningFeedbackRecorder(enabled=True)
    result = recorder.record(_event())
    assert result.ok is True
    assert result.status == RECORD_STATUS_RECORDED
    assert len(recorder.list_events()) == 1
    assert recorder.stats()["recorded_count"] == 1


def test_disabled_recorder_skips_without_raising():
    recorder = LearningFeedbackRecorder(enabled=False)
    result = recorder.record(_event())
    assert result.ok is False
    assert result.status == RECORD_STATUS_SKIPPED
    assert result.reason == REASON_FLAG_OFF
    assert recorder.list_events() == []


def test_buffer_cap_and_clear():
    recorder = LearningFeedbackRecorder(enabled=True, buffer_cap=2)
    recorder.record(_event(student_id="1"))
    recorder.record(_event(student_id="2"))
    recorder.record(_event(student_id="3"))
    events = recorder.list_events()
    assert len(events) == 2
    assert events[0].student_id == "2"
    recorder.clear()
    assert recorder.list_events() == []


def test_bind_recorder_for_tests():
    recorder = LearningFeedbackRecorder(enabled=True)
    bind_learning_feedback_recorder(recorder)
    try:
        from app.infrastructure.adapters.learning_feedback import (
            get_learning_feedback_recorder,
        )

        assert get_learning_feedback_recorder() is recorder
    finally:
        bind_learning_feedback_recorder(None)
