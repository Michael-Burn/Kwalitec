"""Integration tests for Educational Runtime Engine service operations."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.educational_runtime_engine import (
    EducationalRuntimeEngineService,
    RuntimeAuthority,
    RuntimeCoexistencePolicy,
)
from app.application.educational_runtime_engine.exceptions import (
    EnrolmentAlreadyExists,
    MissionAlreadyCompleted,
    PublishedCurriculumUnavailable,
    SyllabusAlreadyComplete,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.models.educational_runtime_engine import RuntimeEducationalEvent
from app.services.study_plan_service import StudyPlanService
from tests.application.educational_runtime_engine.helpers import (
    make_user,
    publish_subject,
)


def test_coexistence_prefers_published_when_available(ctx):
    policy = RuntimeCoexistencePolicy()
    assert policy.resolve_for_enrolment("MISSING") == RuntimeAuthority.JSON_BUNDLED
    assert policy.json_runtime_remains_default() is True

    publish_subject("COEX1")
    assert (
        policy.resolve_for_enrolment("COEX1")
        == RuntimeAuthority.PUBLISHED_CURRICULUM
    )


def test_enrolment_requires_published_curriculum(ctx):
    user = make_user("no-pub@example.com")
    runtime = EducationalRuntimeEngineService()
    with pytest.raises(PublishedCurriculumUnavailable):
        runtime.enrol_student(user_id=user.id, subject_code="NOSUBJECT")


def test_enrol_instantiates_study_plan_from_template(ctx):
    user = make_user("enrol@example.com")
    subject = publish_subject("ENR1")
    runtime = EducationalRuntimeEngineService()

    journey = runtime.enrol_student(user_id=user.id, subject_code=subject)

    assert journey.enrolment.subject_code == "ENR1"
    assert journey.enrolment.curriculum_identity == "ENR1:2027.1"
    assert journey.study_plan.status == "active"
    assert journey.study_plan.current_topic_id is not None
    assert len(journey.study_plan.topic_template_ids) == 2
    assert journey.progress.coverage_ratio == 0.0
    assert journey.runtime_authority == "published_curriculum"

    with pytest.raises(EnrolmentAlreadyExists):
        runtime.enrol_student(user_id=user.id, subject_code=subject)


def test_daily_mission_from_derived_template_and_completion_advances(ctx):
    user = make_user("mission@example.com")
    subject = publish_subject("MSN1")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    day = date(2026, 7, 27)
    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=day,
    )
    assert mission.status == "generated"
    assert mission.template_id.endswith(":learn")
    assert "Study" in mission.title
    assert mission.task_descriptions

    # Idempotent for the same day
    again = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=day,
    )
    assert again.mission_instance_id == mission.mission_instance_id

    journey = runtime.complete_mission(
        user_id=user.id,
        mission_instance_id=mission.mission_instance_id,
    )
    assert mission.topic_id in journey.progress.completed_topic_ids
    assert journey.progress.current_topic_id is not None
    assert journey.progress.current_topic_id != mission.topic_id
    assert journey.progress.coverage_ratio == pytest.approx(0.5)
    assert journey.progress.journey_stage == "learning"

    with pytest.raises(MissionAlreadyCompleted):
        runtime.complete_mission(
            user_id=user.id,
            mission_instance_id=mission.mission_instance_id,
        )


def test_readiness_and_ek_inputs_without_duplicating_state(ctx):
    user = make_user("ready@example.com")
    subject = publish_subject("RDY1")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)
    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=date(2026, 7, 28),
    )
    runtime.complete_mission(
        user_id=user.id,
        mission_instance_id=mission.mission_instance_id,
    )

    readiness = runtime.get_readiness_inputs(user_id=user.id, subject_code=subject)
    assert readiness.denominator_source == "published_progress_model"
    assert len(readiness.topic_ids) == 2
    assert len(readiness.completed_topic_ids) == 1
    assert readiness.coverage_ratio == pytest.approx(0.5)

    ek = runtime.get_estimated_knowledge_inputs(
        user_id=user.id, subject_code=subject
    )
    assert all(topic["has_estimated_knowledge"] is False for topic in ek.topics)
    assert all(topic.get("estimated_knowledge") is None for topic in ek.topics)
    assert all(topic["mastery_score"] is None for topic in ek.topics)
    assert "study_progress_only" in ek.evidence_policy


def test_json_runtime_unaffected_by_published_runtime_enrolment(ctx):
    """Coexistence: Runtime A study-plan path still works for bundled exams."""
    user = make_user("json-runtime@example.com")
    publish_subject("ISO1")
    EducationalRuntimeEngineService().enrol_student(
        user_id=user.id, subject_code="ISO1"
    )

    # Existing JSON-backed CS1 wizard path remains available independently.
    plan = StudyPlanService.create_study_plan(
        user_id=user.id,
        exam_name="IFoA CS1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=120),
        weekday_study_minutes=90,
        weekend_study_minutes=120,
        current_stage="Learning",
        study_preference="Mixed",
        target_grade="Pass",
        preferred_session_minutes=60,
        curriculum_version="2026",
    )
    assert plan is not None
    assert plan.curriculum_id is not None
    assert StudyPlanService.get_user_active_plan(user.id) is not None


def test_end_to_end_enrolment_to_syllabus_complete(ctx):
    """Acceptance: published subject drives full journey without subject code."""
    user = make_user("e2e@example.com")
    subject = publish_subject("E2E1")
    runtime = EducationalRuntimeEngineService()

    journey = runtime.enrol_student(user_id=user.id, subject_code=subject)
    assert journey.study_plan.plan_instance_id

    day = date(2026, 8, 1)
    first = runtime.generate_daily_mission(
        user_id=user.id, subject_code=subject, mission_date=day
    )
    journey = runtime.complete_mission(
        user_id=user.id, mission_instance_id=first.mission_instance_id
    )
    assert journey.progress.syllabus_complete is False

    second = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=day + timedelta(days=1),
    )
    assert second.topic_id != first.topic_id
    journey = runtime.complete_mission(
        user_id=user.id, mission_instance_id=second.mission_instance_id
    )

    assert journey.progress.syllabus_complete is True
    assert journey.progress.coverage_ratio == 1.0
    assert journey.progress.current_topic_id is None
    assert journey.enrolment.status == "completed"
    assert journey.study_plan.status == "completed"

    with pytest.raises(SyllabusAlreadyComplete):
        runtime.generate_daily_mission(
            user_id=user.id,
            subject_code=subject,
            mission_date=day + timedelta(days=2),
        )

    events = runtime.list_events(user_id=user.id, subject_code=subject)
    types = [event.event_type for event in events]
    assert EducationalEventType.STUDENT_ENROLLED.value in types
    assert EducationalEventType.STUDY_PLAN_INSTANTIATED.value in types
    assert types.count(EducationalEventType.MISSION_GENERATED.value) == 2
    assert types.count(EducationalEventType.MISSION_COMPLETED.value) == 2
    assert types.count(EducationalEventType.TOPIC_COMPLETED.value) == 2
    assert EducationalEventType.SYLLABUS_COMPLETED.value in types

    # Events are append-only rows
    assert RuntimeEducationalEvent.query.filter_by(user_id=user.id).count() >= 8
