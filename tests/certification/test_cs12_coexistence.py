"""CS-12: Runtime coexistence certification."""

from __future__ import annotations

from datetime import date, timedelta

from app.application.educational_runtime_engine import (
    EducationalRuntimeEngineService,
    RuntimeAuthority,
    RuntimeCoexistencePolicy,
)
from app.services.study_plan_service import StudyPlanService
from tests.certification.pi001d_helpers import (
    make_certified_user,
    publish_certified_subject,
)


class TestRuntimeCoexistence:
    """Certify Runtime A and Runtime C operate independently."""

    def test_cs12_1_unpublished_resolves_to_json(self, ctx):
        policy = RuntimeCoexistencePolicy()
        assert policy.resolve_for_enrolment("UNPUB99") == RuntimeAuthority.JSON_BUNDLED

    def test_cs12_2_published_resolves_to_curriculum(self, ctx):
        publish_certified_subject("COEX1")
        policy = RuntimeCoexistencePolicy()
        assert (
            policy.resolve_for_enrolment("COEX1")
            == RuntimeAuthority.PUBLISHED_CURRICULUM
        )

    def test_cs12_3_json_runtime_unaffected(self, ctx):
        """Runtime A study plan path works independently of Runtime C."""
        user = make_certified_user("cs12-3@cert.test")
        publish_certified_subject("COEX2")
        EducationalRuntimeEngineService().enrol_student(
            user_id=user.id, subject_code="COEX2"
        )

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

    def test_cs12_4_json_runtime_remains_default(self, ctx):
        policy = RuntimeCoexistencePolicy()
        assert policy.json_runtime_remains_default() is True
