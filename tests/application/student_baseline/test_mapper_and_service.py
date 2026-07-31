"""SB-001A Student Baseline — mapper, service, finalize, history safety."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.calibration.contract import (
    PreviouslyStudied,
    StudyObjective,
)
from app.application.student_baseline.declarations import (
    BaselineDeclarations,
    BaselineSubjectScope,
)
from app.application.student_baseline.enums import (
    BaselineStatus,
    ConfidenceBand,
    ExamHistory,
    LearningObjective,
    PositionMode,
    PreviousExperience,
)
from app.application.student_baseline.mapper import (
    build_plan_fields,
    experience_to_previously_studied,
    objective_to_study_objective,
    to_alpha_declarations,
)
from app.application.student_baseline.service import StudentBaselineService
from app.extensions import db
from app.models.learning import StudyAttempt
from app.models.study_plan import StudyPlan


@pytest.fixture
def user(ctx):
    from tests.conftest import _make_user

    return _make_user()


def _decls(**overrides) -> BaselineDeclarations:
    base = dict(
        experience=PreviousExperience.STARTED,
        position_mode=PositionMode.CONTINUE_TOPIC,
        exam_history=ExamHistory.FIRST_SITTING,
        learning_objective=LearningObjective.CONTINUE,
        confidence=ConfidenceBand.MODERATE,
        curriculum_topic_code="CS1-A",
        highest_mark=None,
    )
    base.update(overrides)
    return BaselineDeclarations(**base)


class TestBaselineMapper:
    def test_brand_new_maps_first_time(self):
        assert (
            experience_to_previously_studied(PreviousExperience.BRAND_NEW)
            is PreviouslyStudied.FIRST_TIME
        )

    def test_revision_objective_maps_finish_remaining(self):
        assert (
            objective_to_study_objective(LearningObjective.CONTINUE)
            is StudyObjective.FINISH_REMAINING
        )

    def test_restart_clears_completed_topics(self):
        fields = build_plan_fields(
            _decls(
                learning_objective=LearningObjective.RESTART,
                position_mode=PositionMode.CONTINUE_TOPIC,
                curriculum_topic_code="CS1-B",
            ),
            ordered_topic_codes=["CS1-A", "CS1-B", "CS1-C"],
        )
        assert fields.current_position == "not_started"
        assert fields.completed_curriculum_topics == []
        assert fields.curriculum_topic_code is None

    def test_continue_topic_seeds_prior_codes(self):
        fields = build_plan_fields(
            _decls(curriculum_topic_code="CS1-B"),
            ordered_topic_codes=["CS1-A", "CS1-B", "CS1-C"],
        )
        assert fields.curriculum_topic_code == "CS1-B"
        assert fields.completed_curriculum_topics == ["CS1-A"]

    def test_alpha_declarations_first_time(self):
        alpha = to_alpha_declarations(
            _decls(experience=PreviousExperience.BRAND_NEW)
        )
        assert alpha.previously_studied is PreviouslyStudied.FIRST_TIME
        assert alpha.previous_attempts_count == 0


class TestBaselineService:
    def test_draft_autosave_and_complete(self, ctx, user):
        scope = BaselineSubjectScope(
            subject_key="IFoA:CS1",
            category_code="IFoA",
            subject_code="CS1",
            curriculum_version="2026",
        )
        draft = StudentBaselineService.ensure_draft(user.id, scope)
        assert draft.status == BaselineStatus.DRAFT.value

        StudentBaselineService.save_answer(
            draft.id,
            user.id,
            experience=PreviousExperience.BRAND_NEW.value,
            position_mode=PositionMode.START_BEGINNING.value,
            exam_history=ExamHistory.FIRST_SITTING.value,
            learning_objective=LearningObjective.RECOMMEND.value,
            confidence=ConfidenceBand.LOW.value,
        )
        draft = StudentBaselineService.get_by_id(draft.id)
        decls = StudentBaselineService.declarations_from_row(draft)
        assert decls is not None
        assert decls.experience is PreviousExperience.BRAND_NEW

        StudentBaselineService.mark_complete(
            draft,
            twin_snapshot_id="snap-1",
            study_plan_id=None,
            runtime_authority="json_bundled",
        )
        complete = StudentBaselineService.get_complete(user.id, "IFoA:CS1")
        assert complete is not None
        assert complete.twin_snapshot_id == "snap-1"

    def test_restart_preserves_study_attempts(self, ctx, user):
        from tests.conftest import _make_mission, _make_subject

        scope = BaselineSubjectScope(
            subject_key="IFoA:CS1",
            category_code="IFoA",
            subject_code="CS1",
        )
        draft = StudentBaselineService.ensure_draft(user.id, scope)
        for field, value in (
            ("experience", PreviousExperience.REVISION_PHASE.value),
            ("position_mode", PositionMode.START_BEGINNING.value),
            ("exam_history", ExamHistory.PREVIOUSLY_ATTEMPTED.value),
            ("learning_objective", LearningObjective.CONTINUE.value),
            ("confidence", ConfidenceBand.HIGH.value),
        ):
            StudentBaselineService.save_answer(draft.id, user.id, **{field: value})

        plan = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=200),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            current_stage="Currently revising",
            study_preference="Mixed",
            target_grade="Pass",
            preferred_session_minutes=60,
            active=True,
        )
        db.session.add(plan)
        db.session.flush()
        subject = _make_subject(user.id)
        mission = _make_mission(user.id, subject.id, plan.id)
        attempt = StudyAttempt(
            user_id=user.id,
            mission_id=mission.id,
            study_date=date.today(),
            duration_minutes=30,
            notes="kept forever",
        )
        db.session.add(attempt)
        db.session.commit()

        StudentBaselineService.mark_complete(
            draft, twin_snapshot_id="snap-r", study_plan_id=plan.id
        )
        StudentBaselineService.restart_for_student(user.id, "IFoA:CS1")

        assert StudentBaselineService.get_complete(user.id, "IFoA:CS1") is None
        draft2 = StudentBaselineService.get_draft(user.id, "IFoA:CS1")
        assert draft2 is not None
        assert StudyAttempt.query.filter_by(user_id=user.id).count() == 1
        assert db.session.get(StudyPlan, plan.id) is not None

    def test_founder_reset_does_not_delete_plan(self, ctx, user):
        scope = BaselineSubjectScope(
            subject_key="IFoA:CS1",
            category_code="IFoA",
            subject_code="CS1",
        )
        draft = StudentBaselineService.ensure_draft(user.id, scope)
        StudentBaselineService.save_answer(
            draft.id,
            user.id,
            experience=PreviousExperience.STARTED.value,
            position_mode=PositionMode.START_BEGINNING.value,
            exam_history=ExamHistory.FIRST_SITTING.value,
            learning_objective=LearningObjective.CONTINUE.value,
            confidence=ConfidenceBand.MODERATE.value,
        )
        plan = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=200),
            weekday_study_minutes=60,
            weekend_study_minutes=90,
            current_stage="Learning new material",
            study_preference="Mixed",
            target_grade="Pass",
            preferred_session_minutes=60,
            active=True,
        )
        db.session.add(plan)
        db.session.commit()
        StudentBaselineService.mark_complete(
            draft, twin_snapshot_id=None, study_plan_id=plan.id
        )
        StudentBaselineService.founder_reset(user.id, "IFoA:CS1")
        assert StudentBaselineService.get_complete(user.id, "IFoA:CS1") is None
        assert db.session.get(StudyPlan, plan.id) is not None
