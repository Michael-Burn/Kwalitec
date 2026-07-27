"""CS-04 to CS-08: Runtime lifecycle certification.

Covers enrolment, study plan, mission generation, completion, and progress.
"""

from __future__ import annotations

from datetime import date

import pytest

from app.application.educational_runtime_engine import (
    EducationalRuntimeEngineService,
)
from app.application.educational_runtime_engine.exceptions import (
    EnrolmentAlreadyExists,
    MissionAlreadyCompleted,
    PublishedCurriculumUnavailable,
)
from tests.certification.pi001d_helpers import (
    make_certified_user,
    publish_certified_subject,
)


class TestStudentEnrolment:
    """CS-04: Student enrolment certification."""

    def test_cs04_1_enrol_against_published(self, ctx):
        user = make_certified_user("cs04-1@cert.test")
        subject = publish_certified_subject("CS04A")
        runtime = EducationalRuntimeEngineService()

        journey = runtime.enrol_student(user_id=user.id, subject_code=subject)
        assert journey.enrolment.subject_code == "CS04A"
        assert journey.enrolment.curriculum_identity == "CS04A:2027.1"
        assert journey.enrolment.status == "active"

    def test_cs04_2_auto_instantiate_plan(self, ctx):
        user = make_certified_user("cs04-2@cert.test")
        subject = publish_certified_subject("CS04B")
        runtime = EducationalRuntimeEngineService()

        journey = runtime.enrol_student(user_id=user.id, subject_code=subject)
        assert journey.study_plan.status == "active"
        assert journey.study_plan.current_topic_id is not None
        assert len(journey.study_plan.topic_template_ids) == 3

    def test_cs04_3_duplicate_enrolment_rejected(self, ctx):
        user = make_certified_user("cs04-3@cert.test")
        subject = publish_certified_subject("CS04C")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        with pytest.raises(EnrolmentAlreadyExists):
            runtime.enrol_student(user_id=user.id, subject_code=subject)

    def test_cs04_4_no_published_curriculum_rejected(self, ctx):
        user = make_certified_user("cs04-4@cert.test")
        runtime = EducationalRuntimeEngineService()

        with pytest.raises(PublishedCurriculumUnavailable):
            runtime.enrol_student(user_id=user.id, subject_code="NONEXISTENT")


class TestStudyPlanInstantiation:
    """CS-05: Study plan instantiation certification."""

    def test_cs05_1_plan_from_template(self, ctx):
        user = make_certified_user("cs05-1@cert.test")
        subject = publish_certified_subject("CS05A")
        runtime = EducationalRuntimeEngineService()

        journey = runtime.enrol_student(user_id=user.id, subject_code=subject)
        assert len(journey.study_plan.topic_template_ids) == 3

    def test_cs05_2_current_topic_initialised(self, ctx):
        user = make_certified_user("cs05-2@cert.test")
        subject = publish_certified_subject("CS05B")
        runtime = EducationalRuntimeEngineService()

        journey = runtime.enrol_student(user_id=user.id, subject_code=subject)
        first_template_id = journey.study_plan.topic_template_ids[0]
        assert journey.study_plan.current_topic_id == first_template_id

    def test_cs05_3_progress_starts_at_zero(self, ctx):
        user = make_certified_user("cs05-3@cert.test")
        subject = publish_certified_subject("CS05C")
        runtime = EducationalRuntimeEngineService()

        journey = runtime.enrol_student(user_id=user.id, subject_code=subject)
        assert journey.progress.coverage_ratio == 0.0
        assert len(journey.progress.completed_topic_ids) == 0


class TestMissionGeneration:
    """CS-06: Mission generation certification."""

    def test_cs06_1_generate_daily_mission(self, ctx):
        user = make_certified_user("cs06-1@cert.test")
        subject = publish_certified_subject("CS06A")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        mission = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=date(2026, 8, 1)
        )
        assert mission.status == "generated"
        assert mission.template_id is not None
        assert mission.topic_id is not None
        assert mission.task_descriptions

    def test_cs06_2_idempotent_same_day(self, ctx):
        user = make_certified_user("cs06-2@cert.test")
        subject = publish_certified_subject("CS06B")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        day = date(2026, 8, 1)
        m1 = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=day
        )
        m2 = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=day
        )
        assert m1.mission_instance_id == m2.mission_instance_id

    def test_cs06_3_mission_targets_current_topic(self, ctx):
        user = make_certified_user("cs06-3@cert.test")
        subject = publish_certified_subject("CS06C")
        runtime = EducationalRuntimeEngineService()
        journey = runtime.enrol_student(user_id=user.id, subject_code=subject)

        mission = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=date(2026, 8, 1)
        )
        assert mission.topic_id == journey.study_plan.current_topic_id


class TestMissionCompletion:
    """CS-07: Mission completion certification."""

    def test_cs07_1_complete_mission(self, ctx):
        user = make_certified_user("cs07-1@cert.test")
        subject = publish_certified_subject("CS07A")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        mission = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=date(2026, 8, 1)
        )
        journey = runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )
        assert mission.topic_id in journey.progress.completed_topic_ids

    def test_cs07_2_journey_advances(self, ctx):
        user = make_certified_user("cs07-2@cert.test")
        subject = publish_certified_subject("CS07B")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        mission = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=date(2026, 8, 1)
        )
        first_topic = mission.topic_id
        journey = runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )
        assert journey.progress.current_topic_id != first_topic
        assert journey.progress.current_topic_id is not None

    def test_cs07_3_duplicate_completion_rejected(self, ctx):
        user = make_certified_user("cs07-3@cert.test")
        subject = publish_certified_subject("CS07C")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        mission = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=date(2026, 8, 1)
        )
        runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )
        with pytest.raises(MissionAlreadyCompleted):
            runtime.complete_mission(
                user_id=user.id, mission_instance_id=mission.mission_instance_id
            )


class TestProgressDerivation:
    """CS-08: Progress derivation certification."""

    def test_cs08_1_coverage_updates(self, ctx):
        user = make_certified_user("cs08-1@cert.test")
        subject = publish_certified_subject("CS08A")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        mission = runtime.generate_daily_mission(
            user_id=user.id, subject_code=subject, mission_date=date(2026, 8, 1)
        )
        journey = runtime.complete_mission(
            user_id=user.id, mission_instance_id=mission.mission_instance_id
        )
        assert journey.progress.coverage_ratio == pytest.approx(1.0 / 3.0)

    def test_cs08_2_journey_stage_progresses(self, ctx):
        user = make_certified_user("cs08-2@cert.test")
        subject = publish_certified_subject("CS08B")
        runtime = EducationalRuntimeEngineService()
        runtime.enrol_student(user_id=user.id, subject_code=subject)

        progress = runtime.get_progress(user_id=user.id, subject_code=subject)
        assert progress.journey_stage in ("not_started", "learning")
