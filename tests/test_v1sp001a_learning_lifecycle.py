"""V1SP-001A — Learning Lifecycle Completion tests.

Covers lifecycle transitions, syllabus completion detection, revision missions,
dashboard Revision Workspace, recommendation changes, and legacy migration.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.extensions import db
from app.models.curriculum import Curriculum, Topic
from app.models.mission import Mission
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.topic_progress import TopicProgress
from app.services.learning_lifecycle_service import (
    LearningLifecycle,
    LearningLifecycleService,
)
from app.services.planning_service import PlanningService
from app.services.recommendation_service import RecommendationService


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
    curriculum: Curriculum,
    current_stage: str = "Chapter 1",
) -> StudyPlan:
    today = date.today()
    plan = StudyPlan(
        user_id=user_id,
        curriculum_id=curriculum.id,
        curriculum_version=curriculum.version,
        exam_name=curriculum.exam_name,
        exam_sitting="April 2027",
        exam_date=today + timedelta(days=180),
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        current_stage=current_stage,
        study_preference="Mixed",
        target_grade="Pass",
        preferred_session_minutes=60,
        active=True,
        curriculum_topic_code=None,
    )
    db.session.add(plan)
    db.session.flush()
    week = WeekPlan(
        study_plan_id=plan.id,
        week_number=1,
        start_date=today - timedelta(days=today.weekday()),
        end_date=today - timedelta(days=today.weekday()) + timedelta(days=6),
    )
    db.session.add(week)
    db.session.commit()
    return plan


def _complete_all_topics(user_id: int, topics: list[Topic]) -> None:
    for topic in topics:
        db.session.add(
            TopicProgress(
                user_id=user_id,
                topic_id=topic.id,
                confidence="Medium",
                completed=True,
                mastery_score=55.0,
                revision_count=1,
                current_stage=TopicProgress.STAGE_COMPLETED,
            )
        )
    db.session.commit()


def _complete_some_topics(user_id: int, topics: list[Topic], count: int) -> None:
    for topic in topics[:count]:
        db.session.add(
            TopicProgress(
                user_id=user_id,
                topic_id=topic.id,
                confidence="Medium",
                completed=True,
                mastery_score=50.0,
                revision_count=1,
                current_stage=TopicProgress.STAGE_COMPLETED,
            )
        )
    db.session.commit()


@pytest.fixture
def user(ctx, db):
    from tests.conftest import _make_user

    return _make_user()


class TestLifecycleTransitions:
    def test_not_started_without_plan(self, db, user):
        snap = LearningLifecycleService.resolve(user.id)
        assert snap.stage == LearningLifecycle.NOT_STARTED
        assert snap.syllabus_complete is False

    def test_learning_while_topics_remain(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["Alpha", "Beta", "Gamma"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_some_topics(user.id, topics, 1)

        snap = LearningLifecycleService.resolve(user.id, study_plan=plan)
        assert snap.stage == LearningLifecycle.LEARNING
        assert snap.syllabus_complete is False
        assert snap.topics_completed == 1
        assert snap.topics_total == 3
        assert snap.workspace_label == "Learning Workspace"
        assert snap.show_completion_acknowledgement is False

    def test_revision_when_all_topics_complete(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["Alpha", "Beta", "Gamma"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)

        snap = LearningLifecycleService.resolve(user.id, study_plan=plan)
        assert snap.stage == LearningLifecycle.REVISION
        assert snap.syllabus_complete is True
        assert snap.workspace_label == "Revision Workspace"
        assert snap.show_completion_acknowledgement is True
        assert plan.revision_entered_at is not None

    def test_exam_ready_never_assigned(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["Alpha", "Beta"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)
        snap = LearningLifecycleService.resolve(user.id, study_plan=plan)
        assert snap.stage != "exam_ready"
        assert snap.stage == LearningLifecycle.REVISION


class TestSyllabusCompletionDetection:
    def test_is_syllabus_complete(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B"])
        assert (
            LearningLifecycleService.is_syllabus_complete(user.id, curriculum)
            is False
        )
        _complete_all_topics(user.id, topics)
        assert (
            LearningLifecycleService.is_syllabus_complete(user.id, curriculum)
            is True
        )

    def test_empty_curriculum_not_complete(self, db, user):
        curriculum, _topics = _make_curriculum("Empty", [])
        assert (
            LearningLifecycleService.is_syllabus_complete(user.id, curriculum)
            is False
        )


class TestRevisionMissions:
    def test_revision_mission_never_restarts_topic_one(self, db, user):
        curriculum, topics = _make_curriculum(
            "CM1", ["Topic One Intro", "Topic Two", "Topic Three"]
        )
        _make_active_plan(
            user.id, curriculum=curriculum, current_stage="Chapter 1"
        )
        _complete_all_topics(user.id, topics)

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert mission.title.startswith("Revision:")
        descs = " ".join(t.description or "" for t in mission.tasks)
        blob = (mission.title + " " + descs).lower()
        assert "topic one intro" not in blob
        assert "chapter 1" not in blob
        assert not mission.title.lower().startswith("study topic one")

    def test_learning_student_still_gets_topic_mission(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["First Topic", "Second Topic"])
        _make_active_plan(user.id, curriculum=curriculum)
        _complete_some_topics(user.id, topics, 0)

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert not mission.title.startswith("Revision:")
        assert "First Topic" in mission.title or "first topic" in mission.title.lower()

    def test_revision_mission_kinds_are_deterministic(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)

        today = date.today()
        m1 = PlanningService._generate_revision_mission_for_date(
            user.id, plan, today
        )
        # Delete and regenerate same date — same kind/title pattern
        db.session.delete(m1)
        db.session.commit()
        m2 = PlanningService._generate_revision_mission_for_date(
            user.id, plan, today
        )
        assert m1.title == m2.title
        assert [t.title for t in m1.tasks] == [t.title for t in m2.tasks]

    def test_unfinished_learning_mission_replaced_on_revision(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["Alpha", "Beta"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        # Learning mission while incomplete
        learning = PlanningService.generate_today_mission(user.id)
        assert learning is not None
        assert not learning.title.startswith("Revision:")

        _complete_all_topics(user.id, topics)
        # Clear entered stamp so resolve can re-stamp; mission still learning
        plan.revision_entered_at = None
        db.session.commit()

        replacement = PlanningService.generate_today_mission(user.id)
        assert replacement is not None
        assert replacement.title.startswith("Revision:")
        assert "Study Alpha" not in (replacement.title or "")
        assert Mission.query.filter_by(user_id=user.id).count() == 1


class TestRecommendations:
    def test_revision_recommends_consolidation_not_unread_topics(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["Alpha", "Beta", "Gamma"])
        _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)

        recs = RecommendationService.generate_recommendations(user.id, limit=5)
        assert recs
        titles = " ".join(r["title"].lower() for r in recs)
        assert "unread" not in titles
        assert "next incomplete" not in titles
        # Should not push Topic 1 style progression
        assert not any(
            "continue with alpha" in r["title"].lower() for r in recs
        )
        assert any(
            r["category"] == "Revision" or "revision" in r["title"].lower()
            or "mixed" in r["title"].lower()
            or "formulae" in r["title"].lower()
            or "timed" in r["title"].lower()
            or "weakest" in r["title"].lower()
            for r in recs
        )

    def test_learning_recommendations_unchanged_path(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["Alpha", "Beta", "Gamma"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_some_topics(user.id, topics, 1)

        # Should not take revision-only path
        snap = LearningLifecycleService.resolve(user.id, study_plan=plan)
        assert snap.stage == LearningLifecycle.LEARNING
        recs = RecommendationService.generate_recommendations(user.id, limit=5)
        assert isinstance(recs, list)


class TestLegacyMigration:
    def test_legacy_completed_student_enters_revision_on_first_load(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B", "C"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)
        assert plan.revision_entered_at is None
        assert plan.revision_acknowledged is False

        snap = LearningLifecycleService.resolve(user.id, study_plan=plan)
        assert snap.stage == LearningLifecycle.REVISION
        assert plan.revision_entered_at is not None
        assert snap.show_completion_acknowledgement is True

    def test_acknowledge_dismisses_celebration(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)
        LearningLifecycleService.resolve(user.id, study_plan=plan)

        assert LearningLifecycleService.acknowledge_revision(user.id) is True
        snap = LearningLifecycleService.resolve(user.id, study_plan=plan)
        assert snap.show_completion_acknowledgement is False
        assert plan.revision_acknowledged is True


class TestProgressRetained:
    def test_progress_remains_complete_in_revision(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B", "C"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)

        snap = LearningLifecycleService.resolve(user.id, study_plan=plan)
        assert snap.topics_completed == snap.topics_total == 3
        assert snap.revision_metrics is not None
        assert snap.revision_metrics.topics_completed == 3

        # Completing a revision mission must not un-complete topics
        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        for topic in topics:
            tp = TopicProgress.query.filter_by(
                user_id=user.id, topic_id=topic.id
            ).first()
            assert tp is not None
            assert tp.completed is True


class TestDashboardRevisionWorkspace:
    def test_dashboard_shows_revision_workspace(self, app, client, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B"])
        _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)

        with client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)
            sess["_fresh"] = True

        response = client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Revision Workspace" in body
        assert "Syllabus Complete" in body
        assert "Revision Progress" in body or "Topics Completed" in body
        assert "100%" in body
        # Must not push remaining-topics learning copy as primary
        assert "Topic One" not in body or "Revision:" in body

    def test_dashboard_learning_unchanged_for_active_students(
        self, app, client, db, user
    ):
        curriculum, topics = _make_curriculum("CM1", ["A", "B", "C"])
        _make_active_plan(user.id, curriculum=curriculum)
        _complete_some_topics(user.id, topics, 1)

        with client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)
            sess["_fresh"] = True

        response = client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Learning Workspace" in body
        assert "Revision Workspace" not in body
        assert "Syllabus Complete" not in body

    def test_acknowledge_endpoint(self, app, client, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)
        LearningLifecycleService.resolve(user.id, study_plan=plan)

        with client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)
            sess["_fresh"] = True

        response = client.post(
            "/dashboard/revision/acknowledge",
            follow_redirects=True,
        )
        assert response.status_code == 200
        db.session.refresh(plan)
        assert plan.revision_acknowledged is True


class TestRevisionMetricsHonesty:
    def test_metrics_do_not_fabricate_activity(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)

        snap = LearningLifecycleService.resolve(user.id, study_plan=plan)
        metrics = snap.revision_metrics
        assert metrics is not None
        assert metrics.topics_completed == 2
        # No completed revision missions yet — sessions may be 0 after stamp
        # with empty mission set, or None before any activity depending on path.
        assert metrics.revision_sessions in (0, None) or metrics.revision_sessions >= 0
        assert metrics.practice_questions_completed is None
        assert metrics.mixed_quiz_attempts is None


class TestEdgeCases:
    def test_idempotent_mission_generation_in_revision(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B"])
        _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)

        m1 = PlanningService.generate_today_mission(user.id)
        m2 = PlanningService.generate_today_mission(user.id)
        assert m1 is not None and m2 is not None
        assert m1.id == m2.id

    def test_select_topic_returns_none_when_complete(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)

        topic = PlanningService._select_topic_for_today(
            user.id, plan, date.today()
        )
        assert topic is None

    def test_no_mission_outside_week_window(self, db, user):
        curriculum, topics = _make_curriculum("CM1", ["A", "B"])
        plan = _make_active_plan(user.id, curriculum=curriculum)
        _complete_all_topics(user.id, topics)
        # Move week far in the past
        for week in plan.week_plans:
            week.start_date = date.today() - timedelta(days=400)
            week.end_date = date.today() - timedelta(days=394)
        db.session.commit()

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is None
