"""Tests for service-layer business logic."""

from __future__ import annotations

from datetime import date, timedelta

import pytest


class TestAdaptiveLearningService:
    """Tests for AdaptiveLearningService calculations."""

    def test_calculate_mastery_score_perfect(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        score = AdaptiveLearningService.calculate_mastery_score(
            accuracy=100.0,
            confidence_numeric=100.0,
            revision_count=5,
            unresolved_mistakes=0,
        )
        assert score == 100.0

    def test_calculate_mastery_score_low(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        score = AdaptiveLearningService.calculate_mastery_score(
            accuracy=20.0,
            confidence_numeric=10.0,
            revision_count=1,
            unresolved_mistakes=3,
        )
        assert 0 <= score <= 100

    def test_calculate_mastery_score_penalty(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        score_no_penalty = AdaptiveLearningService.calculate_mastery_score(
            accuracy=80.0,
            confidence_numeric=80.0,
            revision_count=3,
            unresolved_mistakes=0,
        )
        score_with_penalty = AdaptiveLearningService.calculate_mastery_score(
            accuracy=80.0,
            confidence_numeric=80.0,
            revision_count=3,
            unresolved_mistakes=4,
        )
        assert score_with_penalty < score_no_penalty

    def test_calculate_mastery_score_clamps_to_100(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        score = AdaptiveLearningService.calculate_mastery_score(
            accuracy=100.0,
            confidence_numeric=100.0,
            revision_count=10,
            unresolved_mistakes=0,
        )
        assert score <= 100.0

    def test_calculate_mastery_score_clamps_to_0(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        score = AdaptiveLearningService.calculate_mastery_score(
            accuracy=0.0,
            confidence_numeric=0.0,
            revision_count=0,
            unresolved_mistakes=10,
        )
        assert score >= 0.0

    def test_calculate_mastery_score_none_inputs(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        score = AdaptiveLearningService.calculate_mastery_score(
            accuracy=None,
            confidence_numeric=None,
            revision_count=2,
            unresolved_mistakes=0,
        )
        assert 0 <= score <= 100

    def test_determine_stage_mastered(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        assert AdaptiveLearningService.determine_stage(95.0) == "Mastered"

    def test_determine_stage_practising(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        assert AdaptiveLearningService.determine_stage(80.0) == "Practising"

    def test_determine_stage_learning(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        assert AdaptiveLearningService.determine_stage(50.0) == "Learning"

    def test_determine_stage_not_started(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        assert AdaptiveLearningService.determine_stage(10.0) == "Not Started"

    def test_confidence_numeric_mapping(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        assert AdaptiveLearningService.get_confidence_numeric("Not Started") == 0
        assert AdaptiveLearningService.get_confidence_numeric("Low") == 25
        assert AdaptiveLearningService.get_confidence_numeric("Medium") == 50
        assert AdaptiveLearningService.get_confidence_numeric("High") == 75
        assert AdaptiveLearningService.get_confidence_numeric("Mastered") == 100
        assert AdaptiveLearningService.get_confidence_numeric(None) is None
        assert AdaptiveLearningService.get_confidence_numeric("Unknown") is None

    def test_schedule_next_review_mastered(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        next_date = AdaptiveLearningService.schedule_next_review(95.0)
        assert next_date == date.today() + timedelta(days=14)

    def test_schedule_next_review_weak(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        next_date = AdaptiveLearningService.schedule_next_review(20.0)
        assert next_date == date.today() + timedelta(days=1)

    def test_schedule_next_review_practising(self):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        next_date = AdaptiveLearningService.schedule_next_review(80.0)
        assert next_date == date.today() + timedelta(days=7)

    def test_get_weak_topics(self, db, user, topic_progress):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        weak = AdaptiveLearningService.get_weak_topics(user.id, threshold=80.0)
        assert len(weak) >= 1
        assert weak[0].mastery_score < 80.0

    def test_get_mastered_topics(self, db, user, topic_progress):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        # Make this topic mastered
        topic_progress.mastery_score = 95.0
        topic_progress.current_stage = "Mastered"
        db.session.commit()

        mastered = AdaptiveLearningService.get_mastered_topics(user.id)
        assert len(mastered) >= 1

    def test_get_topics_due_for_review(self, db, user, topic_progress):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        # Set next review to yesterday
        topic_progress.next_review_date = date.today() - timedelta(days=1)
        db.session.commit()

        due = AdaptiveLearningService.get_topics_due_for_review(user.id)
        assert len(due) >= 1

    def test_get_learning_snapshot_empty(self, db, user):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        snapshot = AdaptiveLearningService.get_learning_snapshot(user.id)
        assert snapshot["overall_mastery"] == 0.0
        assert snapshot["topics_mastered"] == 0
        assert snapshot["current_streak"] == 0

    def test_get_learning_snapshot_with_data(self, db, user, topic_progress):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        snapshot = AdaptiveLearningService.get_learning_snapshot(user.id)
        assert snapshot["overall_mastery"] > 0
        assert snapshot["total_topics_started"] >= 1

    def test_calculate_streak_empty(self, db, user):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        streak = AdaptiveLearningService._calculate_streak(user.id)
        assert streak == 0

    def test_generate_daily_briefing_no_activity(self, db, user):
        from app.services.adaptive_learning_service import AdaptiveLearningService

        briefing = AdaptiveLearningService.generate_daily_briefing(user.id)
        assert "did not record any study activity yesterday" in briefing


class TestMissionService:
    """Tests for MissionService."""

    def test_create_mission(self, db, user, subject):
        from app.services.mission_service import MissionService

        m = MissionService.create_mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="Integration Test Mission",
            tasks=[
                {"title": "Task A", "description": "Desc A", "order": 0},
                {"title": "Task B", "description": "Desc B", "order": 1},
            ],
        )
        assert m.id is not None
        assert len(m.tasks) == 2

    def test_create_mission_invalid_subject(self, db, user):
        from app.services.mission_service import MissionService

        with pytest.raises(ValueError, match="Subject"):
            MissionService.create_mission(
                user_id=user.id,
                subject_id=99999,
                mission_date=date.today(),
                title="Bad Mission",
            )

    def test_get_today_mission(self, db, user, subject):
        from app.services.mission_service import MissionService

        MissionService.create_mission(
            user_id=user.id,
            subject_id=subject.id,
            mission_date=date.today(),
            title="Today's Mission",
        )
        m = MissionService.get_today_mission(user.id)
        assert m is not None
        assert m.title == "Today's Mission"

    def test_get_today_mission_none(self, db, user):
        from app.services.mission_service import MissionService

        m = MissionService.get_today_mission(user.id)
        assert m is None

    def test_mark_task_complete(self, db, mission, user):
        from app.services.mission_service import MissionService

        task = mission.tasks[0]
        updated = MissionService.mark_task_complete(task.id, user.id, completed=True)
        assert updated.completed is True
        assert mission.status == "In Progress"

    def test_mark_task_complete_invalid_task(self, db, user):
        from app.services.mission_service import MissionService

        with pytest.raises(ValueError, match="not found"):
            MissionService.mark_task_complete(99999, user.id)

    def test_get_mission_completion_percentage(self, db, mission):
        from app.services.mission_service import MissionService

        pct = MissionService.get_mission_completion_percentage(mission.id)
        assert pct == 0.0

    def test_get_mission_completion_percentage_invalid(self, app, db):
        from app.services.mission_service import MissionService

        with app.app_context():
            with pytest.raises(ValueError, match="not found"):
                MissionService.get_mission_completion_percentage(99999)

    def test_update_mission_status(self, db, mission, user):
        from app.services.mission_service import MissionService

        updated = MissionService.update_mission_status(mission.id, user.id, "Completed")
        assert updated.status == "Completed"

    def test_update_mission_status_invalid_status(self, db, mission, user):
        from app.services.mission_service import MissionService

        with pytest.raises(ValueError, match="Invalid status"):
            MissionService.update_mission_status(mission.id, user.id, "Unknown")


class TestStudyPlanService:
    """Tests for StudyPlanService."""

    def test_create_study_plan(self, db, user):
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CM1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            current_stage="Chapter 1",
            study_preference="Mixed",
            target_grade="A",
        )
        assert sp.id is not None
        assert sp.active is True
        assert sp.exam_name == "IFoA CM1"
        assert len(sp.week_plans) > 0

    def test_create_study_plan_past_date(self, db, user):
        from app.services.study_plan_service import StudyPlanService

        with pytest.raises(ValueError, match="future"):
            StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="Test",
                exam_sitting="Jan 2020",
                exam_date=date.today() - timedelta(days=365),
                weekday_study_minutes=120,
                weekend_study_minutes=180,
                current_stage="Chapter 1",
                study_preference="Mixed",
                target_grade="A",
            )

    def test_create_study_plan_invalid_minutes(self, db, user):
        from app.services.study_plan_service import StudyPlanService

        with pytest.raises(ValueError, match="Weekday"):
            StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="Test",
                exam_sitting="June 2027",
                exam_date=date.today() + timedelta(days=365),
                weekday_study_minutes=5,
                weekend_study_minutes=120,
                current_stage="Chapter 1",
                study_preference="Mixed",
                target_grade="A",
            )

        with pytest.raises(ValueError, match="Weekend"):
            StudyPlanService.create_study_plan(
                user_id=user.id,
                exam_name="Test",
                exam_sitting="June 2027",
                exam_date=date.today() + timedelta(days=365),
                weekday_study_minutes=120,
                weekend_study_minutes=1000,
                current_stage="Chapter 1",
                study_preference="Mixed",
                target_grade="A",
            )

    def test_get_user_active_plan(self, db, study_plan, user):
        from app.services.study_plan_service import StudyPlanService

        active = StudyPlanService.get_user_active_plan(user.id)
        assert active is not None
        assert active.active is True

    def test_get_user_active_plan_none(self, db, user):
        from app.services.study_plan_service import StudyPlanService

        active = StudyPlanService.get_user_active_plan(user.id)
        assert active is None

    def test_deactivate_user_plans(self, db, study_plan, user):
        from app.services.study_plan_service import StudyPlanService

        StudyPlanService.deactivate_user_plans(user.id)
        active = StudyPlanService.get_user_active_plan(user.id)
        assert active is None

    def test_set_active_plan(self, db, study_plan, user):
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.set_active_plan(study_plan.id, user.id)
        assert sp.active is True

    def test_set_active_plan_invalid(self, db, user):
        from app.services.study_plan_service import StudyPlanService

        with pytest.raises(ValueError, match="not found"):
            StudyPlanService.set_active_plan(99999, user.id)

    def test_get_user_plans(self, db, study_plan, user):
        from app.services.study_plan_service import StudyPlanService

        plans = StudyPlanService.get_user_plans(user.id)
        assert len(plans) >= 1

    def test_get_current_week_plan(self, db, study_plan):
        from app.services.study_plan_service import StudyPlanService
        from app.models.study_plan import WeekPlan

        # Create a week plan that covers today
        wp = WeekPlan(
            study_plan_id=study_plan.id,
            week_number=1,
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
        )
        db.session.add(wp)
        db.session.commit()

        current = StudyPlanService.get_current_week_plan(study_plan)
        assert current is not None
        assert current.week_number == 1


class TestPlanningService:
    """Tests for PlanningService mission generation."""

    def test_get_day_type_weekday(self):
        from app.services.planning_service import DayType, PlanningService

        # A Monday
        monday = date(2026, 8, 3)
        assert PlanningService._get_day_type(monday) == DayType.WEEKDAY

    def test_get_day_type_weekend(self):
        from app.services.planning_service import DayType, PlanningService

        # A Saturday
        saturday = date(2026, 8, 1)
        assert PlanningService._get_day_type(saturday) == DayType.WEEKEND

    def test_generate_weekday_tasks(self):
        from app.services.planning_service import PlanningService

        tasks = PlanningService._generate_weekday_tasks(
            study_minutes=120,
            current_stage="Chapter 3",
            study_preference="Mixed",
        )
        assert len(tasks) == 3
        assert tasks[0]["order"] == 0
        assert tasks[1]["order"] == 1
        assert tasks[2]["order"] == 2

    def test_generate_weekday_tasks_reading_first(self):
        from app.services.planning_service import PlanningService

        tasks = PlanningService._generate_weekday_tasks(
            study_minutes=120,
            current_stage="Chapter 1",
            study_preference="Reading First",
        )
        assert "Read" in tasks[0]["title"]

    def test_generate_weekday_tasks_questions_first(self):
        from app.services.planning_service import PlanningService

        tasks = PlanningService._generate_weekday_tasks(
            study_minutes=120,
            current_stage="Chapter 1",
            study_preference="Questions First",
        )
        assert "Practice Questions" in tasks[0]["title"]

    def test_generate_weekend_tasks(self):
        from app.services.planning_service import PlanningService

        tasks = PlanningService._generate_weekend_tasks(
            study_minutes=180,
            current_stage="Chapter 5",
        )
        assert len(tasks) == 3
        assert "Timed Practice" in tasks[0]["title"]

    def test_generate_mission_title_weekday(self):
        from app.services.planning_service import DayType, PlanningService

        d = date(2026, 8, 3)  # Monday
        title = PlanningService._generate_mission_title(DayType.WEEKDAY, d)
        assert "Monday" in title
        assert "Aug 03" in title

    def test_generate_mission_title_weekend(self):
        from app.services.planning_service import DayType, PlanningService

        d = date(2026, 8, 1)  # Saturday
        title = PlanningService._generate_mission_title(DayType.WEEKEND, d)
        assert "Saturday" in title

    def test_generate_mission_title_with_topic(self, db, curriculum):
        from app.services.planning_service import DayType, PlanningService

        c, topics = curriculum
        topic = topics[0]
        d = date(2026, 8, 3)
        title = PlanningService._generate_mission_title(DayType.WEEKDAY, d, topic=topic)
        assert topic.name in title

    def test_generate_today_mission_no_plan(self, db, user):
        from app.services.planning_service import PlanningService

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is None

    def test_generate_today_mission_with_plan(self, db, user, study_plan, subject):
        from app.services.planning_service import PlanningService
        from app.models.study_plan import WeekPlan
        from app.models.curriculum import Curriculum, Topic

        c = Curriculum(exam_name="IFoA CM1", version="2025", active=True)
        db.session.add(c)
        db.session.flush()
        t = Topic(name="Test Topic", curriculum_id=c.id, order=1,
                   recommended_minutes=60, active=True)
        db.session.add(t)
        db.session.flush()

        study_plan.curriculum_id = c.id
        db.session.flush()

        wp = WeekPlan(
            study_plan_id=study_plan.id,
            week_number=1,
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
        )
        db.session.add(wp)
        db.session.commit()

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert mission.user_id == user.id

    def test_generate_today_mission_idempotent(self, db, user, study_plan, subject):
        from app.services.planning_service import PlanningService
        from app.models.study_plan import WeekPlan
        from app.models.curriculum import Curriculum, Topic

        c = Curriculum(exam_name="IFoA CM1", version="2025", active=True)
        db.session.add(c)
        db.session.flush()
        t = Topic(name="Idempotent Topic", curriculum_id=c.id, order=1,
                   recommended_minutes=60, active=True)
        db.session.add(t)
        db.session.flush()
        study_plan.curriculum_id = c.id
        db.session.flush()

        wp = WeekPlan(
            study_plan_id=study_plan.id,
            week_number=1,
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
        )
        db.session.add(wp)
        db.session.commit()

        m1 = PlanningService.generate_today_mission(user.id)
        m2 = PlanningService.generate_today_mission(user.id)
        assert m1 is not None
        assert m2 is not None
        assert m1.id == m2.id  # Same mission returned


class TestReadinessService:
    """Tests for ReadinessService."""

    def test_get_overall_readiness_empty(self, db, user):
        from app.services.readiness_service import ReadinessService

        r = ReadinessService.get_overall_readiness(user.id)
        assert r["score"] == 0.0
        assert r["total_topics"] == 0

    def test_get_overall_readiness_with_data(self, db, user, topic_progress, curriculum):
        from app.services.readiness_service import ReadinessService

        r = ReadinessService.get_overall_readiness(user.id)
        assert "score" in r
        assert "coverage_pct" in r

    def test_get_review_backlog(self, db, user):
        from app.services.readiness_service import ReadinessService

        backlog = ReadinessService.get_review_backlog(user.id)
        assert "total_backlog" in backlog
        assert backlog["total_backlog"] == 0

    def test_get_weakest_topics(self, db, user, topic_progress):
        from app.services.readiness_service import ReadinessService

        worst = ReadinessService.get_weakest_topics(user.id, limit=3)
        assert len(worst) >= 1 if topic_progress.mastery_score < 100 else True

    def test_get_strongest_topics(self, db, user, topic_progress):
        from app.services.readiness_service import ReadinessService

        strongest = ReadinessService.get_strongest_topics(user.id, limit=3)
        assert isinstance(strongest, list)

    def test_get_review_completion_rate_empty(self, db, user):
        from app.services.readiness_service import ReadinessService

        rate = ReadinessService.get_review_completion_rate(user.id)
        assert rate["total_missions"] == 0
        assert rate["completion_rate"] == 0.0

    def test_get_curriculum_coverage_empty(self, db, user):
        from app.services.readiness_service import ReadinessService

        coverage = ReadinessService.get_curriculum_coverage(user.id)
        assert coverage["total_leaf_topics"] == 0

    def test_get_curriculum_coverage_with_data(self, db, user, curriculum, topic_progress):
        from app.services.readiness_service import ReadinessService

        coverage = ReadinessService.get_curriculum_coverage(user.id)
        assert "coverage_percentage" in coverage
        assert coverage["total_leaf_topics"] > 0

    def test_get_current_streak_empty(self, db, user):
        from app.services.readiness_service import ReadinessService

        streak = ReadinessService.get_current_streak(user.id)
        assert streak >= 0

    def test_get_longest_streak_empty(self, db, user):
        from app.services.readiness_service import ReadinessService

        streak = ReadinessService.get_longest_streak(user.id)
        assert streak >= 0


class TestRecommendationService:
    """Tests for RecommendationService."""

    def test_generate_recommendations_empty(self, db, user):
        from app.services.recommendation_service import RecommendationService

        recs = RecommendationService.generate_recommendations(user.id, limit=5)
        assert isinstance(recs, list)

    def test_generate_today_recommendation_empty(self, db, user):
        from app.services.recommendation_service import RecommendationService

        rec = RecommendationService.generate_today_recommendation(user.id)
        assert rec is None or isinstance(rec, dict)

    def test_generate_recommendations_with_data(self, db, user, topic_progress, curriculum):
        from app.services.recommendation_service import RecommendationService

        # Mark topic progress as weak to trigger recommendations
        topic_progress.mastery_score = 25.0
        topic_progress.current_stage = "Learning"
        db.session.commit()

        recs = RecommendationService.generate_recommendations(user.id, limit=5)
        assert isinstance(recs, list)
        # Should have at least one recommendation about weak topic
        if recs:
            assert all("title" in r for r in recs)
            assert all("category" in r for r in recs)
            assert all("priority" in r for r in recs)

    def test_decision_journal(self, db, user):
        from app.services.recommendation_service import RecommendationService

        rec = {
            "title": "Test Recommendation",
            "category": "Review",
            "priority": "High",
            "reason": "Test reason",
            "expected_benefit": "Test benefit",
            "generated_at": "2026-01-01T00:00:00",
        }
        decision = RecommendationService.record_decision(
            user_id=user.id,
            recommendation=rec,
            accepted=True,
            completed=False,
        )
        assert decision.id is not None
        assert decision.accepted is True

        journal = RecommendationService.get_decision_journal(user.id, limit=5)
        assert len(journal) >= 1

        summary = RecommendationService.get_decision_summary(user.id)
        assert summary["total_decisions"] >= 1
        assert summary["acceptance_rate"] > 0