"""Tests for Internal Alpha educational-state reset (Epic 4)."""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from app.application.calibration import (
    CONTRACT_VERSION_1_0,
    BeginnerOrHistoryPosture,
    CoreReadingDeclaration,
    CurriculumExamScope,
    IntendedSitting,
    PreviousAttemptsDeclaration,
    PreviouslyStudied,
    StudentCalibrationBuilder,
    StudentCalibrationContract,
    StudyObjective,
)
from app.application.twin_repository import (
    PersistAcknowledgement,
    TwinRepository,
    TwinScope,
    reset_shared_twin_repository,
)
from app.domain.twin import DigitalTwin
from app.extensions import db
from app.models.curriculum import Curriculum, Section, Topic
from app.models.decision import Decision
from app.models.learning import LearningObjective, Mistake, StudyAttempt
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.models.twin_snapshot import TwinSnapshot
from app.models.user import User
from app.services.curriculum_service import CurriculumService
from app.services.internal_alpha_reset_service import (
    RESET_MODELS,
    InternalAlphaResetService,
)
from app.services.planning_service import PlanningService
from app.services.recommendation_service import RecommendationService
from app.services.study_plan_service import StudyPlanService


def _seed_generated_state(user: User) -> Curriculum:
    """Create a full educational history for *user* (everything the reset clears)."""
    curriculum = Curriculum(exam_name="IFoA CS1", version="2026", active=True)
    db.session.add(curriculum)
    db.session.flush()

    section = Section(
        curriculum_id=curriculum.id,
        official_id="CS1-A",
        code="A",
        title="Probability",
        display_order=1,
    )
    db.session.add(section)
    db.session.flush()

    topic = Topic(
        name="Probability basics",
        curriculum_id=curriculum.id,
        section_id=section.id,
        order=1,
        recommended_minutes=60,
        active=True,
    )
    db.session.add(topic)
    db.session.flush()

    lo = LearningObjective(
        topic_id=topic.id,
        description="Define a probability space",
        order=1,
        active=True,
    )
    db.session.add(lo)

    plan = StudyPlan(
        user_id=user.id,
        curriculum_id=curriculum.id,
        exam_name="IFoA CS1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        current_stage="Learning",
        study_preference="Mixed",
        target_grade="Pass",
        preferred_session_minutes=60,
        curriculum_version="2026",
        curriculum_topic_code="1.1",
        active=True,
    )
    db.session.add(plan)
    db.session.flush()

    week = WeekPlan(
        study_plan_id=plan.id,
        week_number=1,
        start_date=date.today() - timedelta(days=2),
        end_date=date.today() + timedelta(days=4),
    )
    db.session.add(week)

    subject = Subject(
        user_id=user.id,
        name="Study Plan",
        colour="#007bff",
        active=True,
    )
    db.session.add(subject)
    db.session.flush()

    mission = Mission(
        user_id=user.id,
        subject_id=subject.id,
        mission_date=date.today(),
        title="Study 1.1",
        status="Pending",
    )
    db.session.add(mission)
    db.session.flush()

    task = MissionTask(
        mission_id=mission.id,
        title="Core reading",
        description="Read topic 1.1",
        order=0,
    )
    db.session.add(task)

    attempt = StudyAttempt(
        user_id=user.id,
        mission_id=mission.id,
        topic_id=topic.id,
        study_date=date.today(),
        questions_attempted=10,
        questions_correct=7,
        confidence_before="Low",
        confidence_after="Medium",
    )
    db.session.add(attempt)
    db.session.flush()

    mistake = Mistake(
        study_attempt_id=attempt.id,
        topic_id=topic.id,
        mistake_type="Concept",
        description="Misapplied conditional probability",
    )
    db.session.add(mistake)

    progress = TopicProgress(
        user_id=user.id,
        topic_id=topic.id,
        mastery_score=40.0,
        current_stage=TopicProgress.STAGE_LEARNING,
        revision_count=1,
    )
    db.session.add(progress)

    decision = Decision(
        user_id=user.id,
        recommendation_title="Study Probability",
        recommendation_category="Focus",
        recommendation_priority="High",
        recommendation_reason="Next syllabus topic",
        recommendation_expected_benefit="Coverage",
        accepted=True,
    )
    db.session.add(decision)

    twin_row = TwinSnapshot(
        snapshot_id="seed-birth-1",
        student_id=str(user.id),
        sitting_id="april-2027",
        curriculum_id=str(curriculum.id),
        sequence=1,
        format_version="1.0",
        authorship="birth",
        twin_payload="{}",
        provenance_payload=None,
        persisted_at=datetime.now(UTC).replace(tzinfo=None),
    )
    db.session.add(twin_row)
    db.session.commit()
    return curriculum


def _beginner_contract(
    *, student_id: str, curriculum_id: str
) -> StudentCalibrationContract:
    return StudentCalibrationContract.create(
        authorised_student_identity=student_id,
        curriculum_exam_scope=CurriculumExamScope.create(
            curriculum_id, current_exam="CS1"
        ),
        declaration_confirmation=True,
        previously_studied=PreviouslyStudied.FIRST_TIME,
        core_reading_completed=CoreReadingDeclaration.none(),
        previous_attempts=PreviousAttemptsDeclaration.create_none(),
        study_objective=StudyObjective.FIRST_SIT,
        intended_sitting=IntendedSitting.create(
            sitting_date=date.today() + timedelta(days=180),
            sitting_label="April 2027",
        ),
        beginner_or_history_posture=BeginnerOrHistoryPosture.EMPTY_HISTORY,
        contract_version=CONTRACT_VERSION_1_0,
        declared_completed_sections=(),
        declared_study_capacity=8.0,
        optional_notes=None,
        emitted_at=datetime.now(UTC),
    )


class TestInternalAlphaResetService:
    """Service-level reset behaviour."""

    def test_preview_lists_generated_and_preserved_counts(self, ctx, user):
        curriculum = _seed_generated_state(user)
        preview = InternalAlphaResetService.preview()

        by_table = {item.table: item.count for item in preview.to_delete}
        assert by_table["study_plans"] >= 1
        assert by_table["missions"] >= 1
        assert by_table["twin_snapshots"] >= 1
        assert preview.total_to_delete >= 1

        preserved = {item.table: item.count for item in preview.preserved}
        assert preserved["users"] == 1
        assert preserved["curricula"] == 1
        assert db.session.get(Curriculum, curriculum.id) is not None

    def test_execute_removes_generated_state_preserves_users_and_curriculum(
        self, ctx, user
    ):
        password_hash = user.password_hash
        curriculum = _seed_generated_state(user)
        topic_ids = [t.id for t in Topic.query.filter_by(curriculum_id=curriculum.id)]
        lo_count = LearningObjective.query.count()
        section_count = Section.query.count()

        result = InternalAlphaResetService.execute()

        assert result.total_deleted >= 1
        for model in RESET_MODELS:
            assert db.session.query(model).count() == 0

        assert User.query.count() == 1
        preserved_user = db.session.get(User, user.id)
        assert preserved_user is not None
        assert preserved_user.password_hash == password_hash
        assert preserved_user.check_password("password123") is True
        assert preserved_user.email == "test@kwalitec.example"

        assert (
            Curriculum.query.filter_by(id=curriculum.id).one().exam_name == "IFoA CS1"
        )
        assert Topic.query.filter(Topic.id.in_(topic_ids)).count() == len(topic_ids)
        assert Section.query.count() == section_count
        assert LearningObjective.query.count() == lo_count

        preserved = {item.table: item.count for item in result.preserved}
        assert preserved["users"] == 1
        assert preserved["curricula"] == 1


class TestInternalAlphaResetCli:
    """flask internal-alpha-reset command."""

    def test_cancelled_when_operator_declines(self, runner, ctx, user):
        _seed_generated_state(user)
        result = runner.invoke(args=["internal-alpha-reset"], input="n\n")

        assert result.exit_code == 0
        assert "THIS CANNOT BE UNDONE" in result.output
        assert "Reset cancelled" in result.output
        assert StudyPlan.query.count() == 1

    def test_executes_with_yes_flag_and_reports_counts(self, runner, ctx, user):
        _seed_generated_state(user)
        result = runner.invoke(args=["internal-alpha-reset", "--yes"])

        assert result.exit_code == 0
        assert "THIS CANNOT BE UNDONE" in result.output
        assert "Reset complete" in result.output
        assert "study_plans:" in result.output
        assert StudyPlan.query.count() == 0
        assert TwinSnapshot.query.count() == 0
        assert User.query.count() == 1
        assert user.check_password("password123") is True


class TestInternalAlphaResetPostResetFlows:
    """After reset, the educational pipeline must work from a clean baseline."""

    def test_new_study_plan_calibration_twin_recommendations_and_missions(
        self, ctx, user, logged_in_client
    ):
        _seed_generated_state(user)
        InternalAlphaResetService.execute()
        reset_shared_twin_repository()

        # Curriculum import remains available / still present.
        CurriculumService.import_curricula()
        curriculum = Curriculum.query.filter_by(
            exam_name="IFoA CS1", version="2026"
        ).first()
        assert curriculum is not None
        assert Topic.query.filter_by(curriculum_id=curriculum.id).count() >= 1

        # New Study Plan works.
        plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="Pass",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        assert plan.id is not None
        assert plan.curriculum_id is not None
        assert StudyPlan.query.filter_by(user_id=user.id).count() == 1

        # New Calibration works (builder → Birth Twin).
        contract = _beginner_contract(
            student_id=str(user.id),
            curriculum_id=str(plan.curriculum_id),
        )
        calibration = StudentCalibrationBuilder().build(contract)
        assert isinstance(calibration.twin, DigitalTwin)

        # New Twin persists and is retrievable.
        scope = TwinScope.create(
            student_id=str(user.id),
            sitting_id="april-2027",
            curriculum_id=str(plan.curriculum_id),
        )
        ack = TwinRepository().persist_birth_twin(
            calibration.twin,
            scope=scope,
            snapshot_id="post-reset-birth-1",
            provenance={"source": "internal_alpha_reset_test"},
        )
        assert isinstance(ack, PersistAcknowledgement)
        loaded = TwinRepository().retrieve_current_twin(scope)
        assert isinstance(loaded, DigitalTwin)
        assert TwinSnapshot.query.count() == 1

        # Recommendations generate.
        recommendations = RecommendationService.generate_recommendations(
            user.id, limit=5
        )
        assert len(recommendations) >= 1

        # Missions generate.
        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert Mission.query.filter_by(user_id=user.id).count() >= 1
        assert MissionTask.query.count() >= 1

        # Dashboard loads for the preserved account.
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
