"""IA-004 Truthful Learning Progress regression tests.

Ensures Study Progress is never conflated with Mastery, Learning Mode
follows the Current Learning Topic, and student-facing wording stays truthful.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from app.extensions import db
from app.mission.routes import _apply_mission_topic_progress
from app.models.curriculum import Curriculum, Topic
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.topic_progress import TopicProgress
from app.services.planning_service import PlanningService
from app.services.study_plan_service import StudyPlanService

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "app" / "templates"

# Student-facing fragments that falsely imply mastery from completion.
FALSE_MASTERY_CLAIMS = (
    "already mastered",
    "you've mastered",
    "you have mastered",
    "fully learned",
    "finished learning forever",
    "mark as mastered",
    "topics mastered",
)


def _make_curriculum(
    exam_name: str, topic_names: list[str]
) -> tuple[Curriculum, list[Topic]]:
    curriculum = Curriculum(exam_name=exam_name, version="2025", active=True)
    db.session.add(curriculum)
    db.session.flush()
    topics: list[Topic] = []
    for index, name in enumerate(topic_names, start=1):
        topic = Topic(
            name=name,
            curriculum_id=curriculum.id,
            order=index,
            recommended_minutes=60,
            active=True,
        )
        db.session.add(topic)
        topics.append(topic)
    db.session.flush()
    return curriculum, topics


def _make_active_plan(
    user_id: int,
    *,
    exam_name: str,
    curriculum: Curriculum,
) -> StudyPlan:
    plan = StudyPlan(
        user_id=user_id,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        exam_name=exam_name,
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="A",
        preferred_session_minutes=60,
        active=True,
        curriculum_topic_code=None,
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
    db.session.commit()
    return plan


@pytest.mark.usefixtures("ctx")
class TestCompletionRecordsStudyProgressOnly:
    """Completing a topic records Study Progress — never Mastery."""

    def test_mission_completion_sets_completed_not_mastery(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1", ["Learning Topic A", "Learning Topic B"]
        )
        _make_active_plan(user.id, exam_name="IFoA CS1", curriculum=curriculum)

        before = TopicProgress(
            user_id=user.id,
            topic_id=topics[0].id,
            completed=False,
            mastery_score=12.0,
            confidence="Low",
            current_stage=TopicProgress.STAGE_LEARNING,
            revision_count=0,
        )
        db.session.add(before)
        db.session.commit()
        prior_score = before.mastery_score

        _apply_mission_topic_progress(user.id, topics[0])

        progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=topics[0].id
        ).one()
        assert progress.completed is True
        assert progress.current_stage == TopicProgress.STAGE_COMPLETED
        assert progress.mastery_score == prior_score
        assert progress.confidence != "Mastered"
        assert progress.has_estimated_mastery is False

    def test_wizard_completed_topics_do_not_set_mastery(self, db, user):
        plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="2.1",
            completed_curriculum_topics=["1.1", "1.2"],
        )
        assert plan.curriculum_id is not None

        completed_rows = TopicProgress.query.filter_by(
            user_id=user.id, completed=True
        ).all()
        assert len(completed_rows) >= 2
        for row in completed_rows:
            assert row.mastery_score == 0.0
            # EIP-001: Study Progress must not co-write student-felt confidence.
            assert row.confidence == "Not Started"
            assert row.current_stage == TopicProgress.STAGE_COMPLETED
            assert row.has_estimated_mastery is False


@pytest.mark.usefixtures("ctx")
class TestLearningModeMissionSelection:
    """Today's Mission follows Current Learning Topic; review never hijacks."""

    def test_mission_follows_current_learning_topic(self, db, user):
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Completed Topic", "Current Learning Topic", "Future Topic"],
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )

        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[0].id,
                completed=True,
                mastery_score=0.0,
                current_stage=TopicProgress.STAGE_COMPLETED,
            )
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[1].id,
                completed=False,
                mastery_score=0.0,
                current_stage=TopicProgress.STAGE_LEARNING,
            )
        )
        db.session.commit()

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert selected is not None
        assert selected.id == topics[1].id

    def test_review_due_completed_topic_never_replaces_learning_mode(
        self, db, user
    ):
        """Completed overdue/weak topics must not override Current Learning Topic."""
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["Old Completed Weak", "Current Learning Topic"],
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )

        # Completed topic that would previously win Priority 1 / Priority 2.
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[0].id,
                completed=True,
                mastery_score=15.0,
                revision_count=5,
                average_accuracy=20.0,
                next_review_date=date.today() - timedelta(days=1),
                current_stage=TopicProgress.STAGE_COMPLETED,
            )
        )
        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[1].id,
                completed=False,
                mastery_score=0.0,
                current_stage=TopicProgress.STAGE_LEARNING,
            )
        )
        db.session.commit()

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert selected is not None
        assert selected.id == topics[1].id
        assert selected.name == "Current Learning Topic"

    def test_incomplete_weak_topic_does_not_preempt_syllabus_order(
        self, db, user
    ):
        curriculum, topics = _make_curriculum(
            "IFoA CS1",
            ["First Incomplete", "Later Weak Topic"],
        )
        plan = _make_active_plan(
            user.id, exam_name="IFoA CS1", curriculum=curriculum
        )

        db.session.add(
            TopicProgress(
                user_id=user.id,
                topic_id=topics[1].id,
                completed=False,
                mastery_score=10.0,
                revision_count=4,
                average_accuracy=15.0,
                next_review_date=date.today(),
                current_stage=TopicProgress.STAGE_NEEDS_REVIEW,
            )
        )
        db.session.commit()

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=plan,
            target_date=date.today(),
        )
        assert selected is not None
        assert selected.id == topics[0].id


@pytest.mark.usefixtures("ctx")
class TestStudentFacingTerminology:
    """Study Plan / Dashboard labels stay educationally truthful."""

    def test_study_plan_view_uses_completed_and_estimated_mastery(
        self, app, user, logged_in_client
    ):
        plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.2",
            completed_curriculum_topics=["1.1"],
        )

        response = logged_in_client.get(f"/study-plan/{plan.id}")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Completed" in body
        assert "Learning" in body or "Not Started" in body
        assert "already mastered" not in body.lower()

        # Completion without attempt evidence must not use a bare "Mastery" label.
        assert 'roadmap-metric-label">Mastery<' not in body
        assert "already mastered" not in body.lower()

    def test_dashboard_labels_study_progress_not_false_mastery(
        self, app, user, logged_in_client
    ):
        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        PlanningService.generate_today_mission(user.id)

        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Study Progress" in body or "Learning Progress" in body
        lower = body.lower()
        for claim in FALSE_MASTERY_CLAIMS:
            assert claim not in lower, f"Found false mastery claim: {claim}"

    def test_mission_page_explains_learning_mode(
        self, app, user, logged_in_client
    ):
        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        PlanningService.generate_today_mission(user.id)

        response = logged_in_client.get("/missions/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Learning Mode" in body
        assert "Current Learning Topic" in body
        assert "Study Progress" in body

    def test_student_facing_templates_avoid_false_mastery_claims(self):
        """Static scan of student templates for banned mastery wording."""
        student_dirs = (
            "dashboard",
            "study_plan",
            "mission",
            "analytics",
            "settings",
            "calibration",
        )
        offenders: list[str] = []
        for folder in student_dirs:
            root = TEMPLATE_ROOT / folder
            if not root.exists():
                continue
            for path in root.rglob("*.html"):
                text = path.read_text(encoding="utf-8").lower()
                for claim in FALSE_MASTERY_CLAIMS:
                    if claim in text:
                        offenders.append(f"{path.relative_to(REPO_ROOT)}: {claim}")

        assert not offenders, "False mastery claims:\n" + "\n".join(offenders)

    def test_edit_plan_uses_completed_not_mastered_copy(
        self, app, user, logged_in_client
    ):
        plan = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="1.1",
        )
        response = logged_in_client.get(f"/study-plan/{plan.id}/edit")
        assert response.status_code == 200
        body = response.get_data(as_text=True).lower()
        assert "already completed studying" in body
        assert "already mastered" not in body
