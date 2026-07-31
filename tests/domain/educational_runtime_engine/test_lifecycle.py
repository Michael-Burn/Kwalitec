"""Unit tests for educational runtime domain progress + state rules."""

from __future__ import annotations

import pytest

from app.domain.educational_runtime_engine.events import (
    EducationalEventRecord,
    EducationalEventType,
)
from app.domain.educational_runtime_engine.progress import (
    ProgressModelSpec,
    ProgressTopicSpec,
    derive_progress,
)
from app.domain.educational_runtime_engine.state import (
    EnrolmentStatus,
    IllegalRuntimeTransition,
    JourneyStage,
    MissionStatus,
    PlanInstanceStatus,
    assert_enrolment_transition,
    assert_mission_transition,
    assert_plan_transition,
    next_journey_stage,
)


def _model() -> ProgressModelSpec:
    return ProgressModelSpec(
        curriculum_identity="LAW1:2027.1",
        topic_ids=("t1", "t2", "t3"),
        topics=(
            ProgressTopicSpec(topic_id="t1", topic_code="1.1"),
            ProgressTopicSpec(
                topic_id="t2",
                topic_code="1.2",
                prerequisite_ids=("t1",),
            ),
            ProgressTopicSpec(
                topic_id="t3",
                topic_code="2.1",
                prerequisite_ids=("t2",),
            ),
        ),
    )


def test_derive_progress_starts_at_first_topic():
    progress = derive_progress(_model(), ())
    assert progress.current_topic_id == "t1"
    assert progress.completed_topic_ids == ()
    assert progress.coverage_ratio == 0.0
    assert progress.journey_stage == JourneyStage.NOT_STARTED
    assert progress.syllabus_complete is False


def test_derive_progress_advances_after_topic_completed_events():
    events = (
        EducationalEventRecord(
            event_id="e1",
            event_type=EducationalEventType.TOPIC_COMPLETED,
            user_id=1,
            curriculum_identity="LAW1:2027.1",
            topic_id="t1",
        ),
    )
    progress = derive_progress(_model(), events)
    assert progress.completed_topic_ids == ("t1",)
    assert progress.current_topic_id == "t2"
    assert progress.coverage_ratio == pytest.approx(1 / 3)
    assert progress.journey_stage == JourneyStage.LEARNING


def test_derive_progress_marks_syllabus_complete():
    events = tuple(
        EducationalEventRecord(
            event_id=f"e{i}",
            event_type=EducationalEventType.TOPIC_COMPLETED,
            user_id=1,
            curriculum_identity="LAW1:2027.1",
            topic_id=topic_id,
        )
        for i, topic_id in enumerate(("t1", "t2", "t3"), start=1)
    )
    progress = derive_progress(_model(), events)
    assert progress.syllabus_complete is True
    assert progress.current_topic_id is None
    assert progress.journey_stage == JourneyStage.SYLLABUS_COMPLETE
    assert progress.coverage_ratio == 1.0


def test_mission_completion_events_do_not_count_as_topic_progress():
    events = (
        EducationalEventRecord(
            event_id="e1",
            event_type=EducationalEventType.MISSION_COMPLETED,
            user_id=1,
            curriculum_identity="LAW1:2027.1",
            topic_id="t1",
        ),
        EducationalEventRecord(
            event_id="e2",
            event_type=EducationalEventType.MISSION_ACCEPTED,
            user_id=1,
            curriculum_identity="LAW1:2027.1",
            topic_id="t1",
            payload={"session_id": "lsr-1"},
        ),
        EducationalEventRecord(
            event_id="e3",
            event_type=EducationalEventType.MISSION_DEFERRED,
            user_id=1,
            curriculum_identity="LAW1:2027.1",
            topic_id="t1",
        ),
    )
    progress = derive_progress(_model(), events)
    assert progress.completed_topic_ids == ()
    assert progress.current_topic_id == "t1"


def test_mission_accept_and_defer_transitions():
    assert_mission_transition(MissionStatus.GENERATED, MissionStatus.ACCEPTED)
    assert_mission_transition(MissionStatus.GENERATED, MissionStatus.DEFERRED)
    assert_mission_transition(MissionStatus.ACCEPTED, MissionStatus.COMPLETED)
    assert_mission_transition(MissionStatus.DEFERRED, MissionStatus.ACCEPTED)
    with pytest.raises(IllegalRuntimeTransition):
        assert_mission_transition(MissionStatus.COMPLETED, MissionStatus.ACCEPTED)


def test_state_transitions_enforce_legality():
    assert_enrolment_transition(EnrolmentStatus.ACTIVE, EnrolmentStatus.COMPLETED)
    assert_plan_transition(PlanInstanceStatus.ACTIVE, PlanInstanceStatus.PAUSED)
    assert_mission_transition(MissionStatus.GENERATED, MissionStatus.COMPLETED)
    with pytest.raises(IllegalRuntimeTransition):
        assert_mission_transition(MissionStatus.COMPLETED, MissionStatus.GENERATED)
    with pytest.raises(IllegalRuntimeTransition):
        assert_enrolment_transition(
            EnrolmentStatus.WITHDRAWN, EnrolmentStatus.ACTIVE
        )


def test_next_journey_stage_helper():
    assert next_journey_stage(completed_topic_count=0, total_topic_count=3) == (
        JourneyStage.NOT_STARTED
    )
    assert next_journey_stage(completed_topic_count=1, total_topic_count=3) == (
        JourneyStage.LEARNING
    )
    assert next_journey_stage(completed_topic_count=3, total_topic_count=3) == (
        JourneyStage.SYLLABUS_COMPLETE
    )
