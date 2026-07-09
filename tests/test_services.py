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

    def test_create_study_plan_with_curriculum_version(self, db, user):
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="June 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Chapter 1",
            study_preference="Reading First",
            target_grade="B",
            curriculum_version="2026",
        )
        assert sp.curriculum_version == "2026"

    def test_create_study_plan_curriculum_version_defaults_to_none(self, db, user):
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CM2",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            current_stage="Chapter 1",
            study_preference="Mixed",
            target_grade="A",
        )
        assert sp.curriculum_version is None

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

    # ── Curriculum-backed TopicProgress initialisation ────────────────────

    def test_create_curriculum_plan_initialises_topic_progress(self, db, user):
        """Creating a curriculum-backed study plan creates TopicProgress
        records for every curriculum topic."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-A",
        )

        # A curriculum should have been created
        assert sp.curriculum_id is not None

        # All 6 CS1-2026 curriculum topics should now have TopicProgress rows
        progress_rows = TopicProgress.query.filter_by(user_id=user.id).all()
        assert len(progress_rows) == 6

        # Every row must be initialised with defaults
        for tp in progress_rows:
            assert tp.completed is False
            assert tp.mastery_score == 0.0
            assert tp.last_reviewed is None
            assert tp.revision_count == 0
            assert tp.confidence == "Not Started"

        # The selected topic (CS1-A) must be marked as current (Learning stage)
        # CS1-A = "Random Variables and Distributions" in the engine data
        db_topics = DBTopic.query.filter_by(curriculum_id=sp.curriculum_id).all()
        cs1a_topic = next(
            (t for t in db_topics if t.name == "Random Variables and Distributions"),
            None,
        )
        assert cs1a_topic is not None
        cs1a_progress = TopicProgress.query.filter_by(
            user_id=user.id,
            topic_id=cs1a_topic.id,
        ).first()
        assert cs1a_progress is not None
        assert cs1a_progress.current_stage == TopicProgress.STAGE_LEARNING
        assert cs1a_progress.completed is False  # Must NOT be marked completed

    def test_create_curriculum_plan_other_topics_not_started(self, db, user):
        """Non-selected topics must remain in 'Not Started' stage."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress

        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="June 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            curriculum_version="2026",
            curriculum_topic_code="CS1-A",
        )

        db_topics = DBTopic.query.filter_by(curriculum_id=sp.curriculum_id).all()
        for db_topic in db_topics:
            tp = TopicProgress.query.filter_by(
                user_id=user.id,
                topic_id=db_topic.id,
            ).first()
            assert tp is not None
            if db_topic.name == "Random Variables and Distributions":
                assert tp.current_stage == TopicProgress.STAGE_LEARNING
            else:
                assert tp.current_stage == TopicProgress.STAGE_NOT_STARTED

    def test_create_plan_without_curriculum_skips_progress_init(self, db, user):
        """Plans without curriculum_version or curriculum_topic_code must
        not create any TopicProgress rows."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        # Neither curriculum param set
        StudyPlanService.create_study_plan(
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

        tp_count = TopicProgress.query.filter_by(user_id=user.id).count()
        assert tp_count == 0

    def test_create_plan_with_curriculum_version_only_still_creates_progress(self, db, user):
        """curriculum_version without curriculum_topic_code should still create TopicProgress."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="June 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            curriculum_version="2026",
            # No curriculum_topic_code
        )

        tp_count = TopicProgress.query.filter_by(user_id=user.id).count()
        # TopicProgress should be initialised from the curriculum even
        # when no specific curriculum_topic_code is provided.
        assert tp_count > 0

    def test_create_plan_with_topic_code_only_does_nothing(self, db, user):
        """curriculum_topic_code without curriculum_version should skip init."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="June 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            curriculum_topic_code="CS1-A",
            # No curriculum_version
        )

        tp_count = TopicProgress.query.filter_by(user_id=user.id).count()
        assert tp_count == 0

    def test_curriculum_topic_progress_is_idempotent(self, db, user):
        """Creating a second plan for the same curriculum must not duplicate
        TopicProgress rows."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        # First plan
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
            curriculum_topic_code="CS1-A",
        )

        first_count = TopicProgress.query.filter_by(user_id=user.id).count()
        assert first_count == 6

        # Second plan — must not create more TopicProgress rows
        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="October 2027",
            exam_date=date.today() + timedelta(days=365),
            weekday_study_minutes=45,
            weekend_study_minutes=90,
            current_stage="Revision",
            study_preference="Questions First",
            target_grade="A",
            curriculum_version="2026",
            curriculum_topic_code="CS1-B",
        )

        second_count = TopicProgress.query.filter_by(user_id=user.id).count()
        assert second_count == 6  # Same count — no dupes

    def test_existing_topic_progress_not_overwritten(self, db, user):
        """Pre-existing TopicProgress values must survive plan re-creation."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress

        # Plan 1 with CS1-A as current
        sp1 = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-A",
        )

        # Manually set some progress to emulate real work
        rv_topic = DBTopic.query.filter_by(
            curriculum_id=sp1.curriculum_id,
            name="Random Variables and Distributions",
        ).first()
        rv_progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=rv_topic.id,
        ).first()
        rv_progress.mastery_score = 85.0
        rv_progress.completed = True
        rv_progress.confidence = "High"
        rv_progress.revision_count = 5
        db.session.commit()

        # Plan 2 — same curriculum, different current topic
        StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="October 2027",
            exam_date=date.today() + timedelta(days=365),
            weekday_study_minutes=45,
            weekend_study_minutes=90,
            current_stage="Revision",
            study_preference="Questions First",
            target_grade="A",
            curriculum_version="2026",
            curriculum_topic_code="CS1-B",
        )

        # The previously worked-on topic must keep its progress
        rv_progress_check = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=rv_topic.id,
        ).first()
        assert rv_progress_check.mastery_score == 85.0
        assert rv_progress_check.completed is True
        assert rv_progress_check.confidence == "High"
        assert rv_progress_check.revision_count == 5

    def test_unsupported_curriculum_version_does_not_crash(self, db, user):
        """A curriculum_version that does not exist on disk should not
        raise an exception — it should just skip initialisation."""
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="June 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            curriculum_version="2099",
            curriculum_topic_code="CS1-A",
        )

        # Plan is still created successfully
        assert sp.id is not None
        # But no TopicProgress rows are created
        from app.models.topic_progress import TopicProgress
        assert TopicProgress.query.filter_by(user_id=user.id).count() == 0

    def test_curriculum_plan_uses_curriculum_week_plans(self, db, user):
        """A curriculum-backed study plan generates week plans following the
        official curriculum order rather than a simple date grid."""
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-A",
        )

        # Should have week plans covering at least the 6 CS1 topics
        assert len(sp.week_plans) > 0
        # Week numbers should be sequential starting at 1
        week_numbers = [wp.week_number for wp in sp.week_plans]
        assert week_numbers == list(range(1, len(week_numbers) + 1))
        # Start date should be the Monday of the current week
        today = date.today()
        expected_start = today - timedelta(days=today.weekday())
        assert sp.week_plans[0].start_date == expected_start

    def test_curriculum_plan_with_large_weekly_minutes_has_fewer_weeks(self, db, user):
        """With more study minutes per week, topics should be covered in
        fewer weeks because each topic spans fewer weeks."""
        from app.services.study_plan_service import StudyPlanService

        # Both plans have the same exam date
        exam_date = date.today() + timedelta(days=180)

        sp_low = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=exam_date,
            weekday_study_minutes=30,
            weekend_study_minutes=30,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="CS1-A",
        )

        import time
        time.sleep(0.1)  # ensure creation timestamps differ

        sp_high = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=exam_date,
            weekday_study_minutes=300,
            weekend_study_minutes=300,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version="2026",
            curriculum_topic_code="CS1-A",
        )

        # Low-minutes plan should need more weeks per topic
        assert len(sp_low.week_plans) > 0
        assert len(sp_high.week_plans) > 0
        # High-minutes plan covers topics faster → at least as many weeks
        # for low-minutes as for high-minutes (but capped at exam date)
        assert len(sp_low.week_plans) >= len(sp_high.week_plans)

    def test_curriculum_plan_respects_topic_code_start(self, db, user):
        """Starting from a later topic code (e.g. CS1-D) should skip earlier
        topics and begin from that point in the sequence."""
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-D",
        )

        assert sp.id is not None
        # Plan created successfully — the sequence starts from CS1-D
        assert len(sp.week_plans) > 0

    def test_non_curriculum_plan_uses_simple_week_grid(self, db, user):
        """A plan without curriculum_version and curriculum_topic_code must
        use the simple date-based week grid (unchanged behaviour)."""
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
            # No curriculum_version or curriculum_topic_code
        )

        # Simple date grid: one week per block from today to exam
        total_days = (sp.exam_date - date.today()).days
        expected_weeks = (total_days + sp.exam_date.weekday()) // 7 + 1
        # Week count should be close to date span / 7
        assert len(sp.week_plans) > 0
        # Each week should be 7 days (except possibly the last)
        for i, wp in enumerate(sp.week_plans):
            span = (wp.end_date - wp.start_date).days
            if i < len(sp.week_plans) - 1:
                assert span == 6  # Mon-Sun = 6 days between start and end
            else:
                assert 0 <= span <= 6  # Last week may be truncated

    def test_unsupported_exam_still_uses_generic_weeks(self, db, user):
        """When curriculum_version+curriculum_topic_code are provided but
        the curriculum doesn't exist on disk, the simple date grid is used."""
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA ZZ9",
            exam_sitting="June 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            curriculum_version="2099",
            curriculum_topic_code="ZZ9-A",
        )

        assert sp.id is not None
        # Falls back to simple date grid — ensure week plans exist
        assert len(sp.week_plans) > 0
        # Week numbers sequential
        week_numbers = [wp.week_number for wp in sp.week_plans]
        assert week_numbers == list(range(1, len(week_numbers) + 1))

    # ── completed_curriculum_topics initialisation ───────────────────────

    def test_completed_curriculum_topics_initialise_as_completed(self, db, user):
        """Topics listed in completed_curriculum_topics must be initialised
        with completed=True, mastery_score=100.0, current_stage='Completed'."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        completed_codes = ["CS1-A", "CS1-B"]
        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-C",
            completed_curriculum_topics=completed_codes,
        )

        assert sp.curriculum_id is not None

        # All 6 topics must have TopicProgress
        progress_rows = TopicProgress.query.filter_by(user_id=user.id).all()
        assert len(progress_rows) == 6

        # Build a map: topic name → TopicProgress
        from app.models.curriculum import Topic as DBTopic
        db_topics = DBTopic.query.filter_by(curriculum_id=sp.curriculum_id).all()
        name_to_progress = {}
        for db_topic in db_topics:
            tp = TopicProgress.query.filter_by(
                user_id=user.id, topic_id=db_topic.id,
            ).first()
            name_to_progress[db_topic.name] = tp

        # CS1-A (Random Variables) and CS1-B (Common Distributions) → Completed
        cs1a = name_to_progress["Random Variables and Distributions"]
        assert cs1a.completed is True
        assert cs1a.mastery_score == 100.0
        assert cs1a.current_stage == TopicProgress.STAGE_COMPLETED

        cs1b = name_to_progress["Common Statistical Distributions"]
        assert cs1b.completed is True
        assert cs1b.mastery_score == 100.0
        assert cs1b.current_stage == TopicProgress.STAGE_COMPLETED

        # CS1-C (Generating Functions) → current topic, must be Learning
        cs1c = name_to_progress["Generating Functions and Sums of Random Variables"]
        assert cs1c.completed is False
        assert cs1c.mastery_score == 0.0
        assert cs1c.current_stage == TopicProgress.STAGE_LEARNING

        # CS1-D through CS1-F → Not Started
        for name in ("Joint Distributions", "Bayesian Statistics",
                     "Sampling and Statistical Inference"):
            tp = name_to_progress[name]
            assert tp.completed is False
            assert tp.mastery_score == 0.0
            assert tp.current_stage == TopicProgress.STAGE_NOT_STARTED

    def test_completed_curriculum_topics_empty_list(self, db, user):
        """An empty completed_curriculum_topics list should leave all topics
        as Not Started (except the current learning topic)."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="June 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            curriculum_version="2026",
            curriculum_topic_code="CS1-A",
            completed_curriculum_topics=[],
        )

        progress_rows = TopicProgress.query.filter_by(user_id=user.id).all()
        assert len(progress_rows) == 6

        from app.models.curriculum import Topic as DBTopic
        db_topics = DBTopic.query.filter_by(curriculum_id=sp.curriculum_id).all()
        for db_topic in db_topics:
            tp = TopicProgress.query.filter_by(
                user_id=user.id, topic_id=db_topic.id,
            ).first()
            assert tp is not None
            assert tp.completed is False
            assert tp.mastery_score == 0.0
            if db_topic.name == "Random Variables and Distributions":
                assert tp.current_stage == TopicProgress.STAGE_LEARNING
            else:
                assert tp.current_stage == TopicProgress.STAGE_NOT_STARTED

    def test_curriculum_topic_code_never_completed(self, db, user):
        """The current learning topic (curriculum_topic_code) must NEVER
        be marked completed, even if it appears in completed_curriculum_topics."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        # CS1-D is both the current topic AND in the completed list.
        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-D",
            completed_curriculum_topics=["CS1-A", "CS1-B", "CS1-D"],
        )

        from app.models.curriculum import Topic as DBTopic

        cs1d_topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Joint Distributions",
        ).first()
        assert cs1d_topic is not None

        cs1d_progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=cs1d_topic.id,
        ).first()
        assert cs1d_progress is not None
        assert cs1d_progress.current_stage == TopicProgress.STAGE_LEARNING
        assert cs1d_progress.completed is False
        assert cs1d_progress.mastery_score == 0.0

        # CS1-A and CS1-B should still be marked completed
        cs1a_topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Random Variables and Distributions",
        ).first()
        cs1a_progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=cs1a_topic.id,
        ).first()
        assert cs1a_progress.completed is True
        assert cs1a_progress.mastery_score == 100.0
        assert cs1a_progress.current_stage == TopicProgress.STAGE_COMPLETED

        cs1b_topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Common Statistical Distributions",
        ).first()
        cs1b_progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=cs1b_topic.id,
        ).first()
        assert cs1b_progress.completed is True

    def test_completed_topics_preserve_idempotency(self, db, user):
        """Existing TopicProgress records must not be overwritten when a new
        plan is created with a different completed_curriculum_topics list."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.curriculum import Topic as DBTopic
        from app.models.topic_progress import TopicProgress

        # ── Plan 1: CS1-A as current, no completed topics ──────────────
        sp1 = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-A",
            completed_curriculum_topics=[],
        )

        assert TopicProgress.query.filter_by(user_id=user.id).count() == 6

        # ── Manually advance CS1-B progress to simulate real work ──────
        cs1b_topic = DBTopic.query.filter_by(
            curriculum_id=sp1.curriculum_id,
            name="Common Statistical Distributions",
        ).first()
        cs1b_progress = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=cs1b_topic.id,
        ).first()
        cs1b_progress.mastery_score = 72.0
        cs1b_progress.revision_count = 4
        cs1b_progress.confidence = "Medium"
        cs1b_progress.current_stage = TopicProgress.STAGE_PRACTISING
        cs1b_progress.completed = False
        db.session.commit()

        # ── Plan 2: CS1-C as current, CS1-B listed as completed ────────
        # Because CS1-B already has a TopicProgress row from Plan 1, its
        # existing values must NOT be overwritten — even though Plan 2
        # lists it in completed_curriculum_topics.
        sp2 = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="October 2027",
            exam_date=date.today() + timedelta(days=365),
            weekday_study_minutes=45,
            weekend_study_minutes=90,
            current_stage="Revision",
            study_preference="Questions First",
            target_grade="A",
            curriculum_version="2026",
            curriculum_topic_code="CS1-C",
            completed_curriculum_topics=["CS1-B"],
        )

        # CS1-B must retain its manual progress (idempotent — NOT overwritten)
        cs1b_check = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=cs1b_topic.id,
        ).first()
        assert cs1b_check.mastery_score == 72.0
        assert cs1b_check.revision_count == 4
        assert cs1b_check.confidence == "Medium"
        assert cs1b_check.current_stage == TopicProgress.STAGE_PRACTISING
        assert cs1b_check.completed is False

        # CS1-C is the current learning topic — must be Learning
        cs1c_topic = DBTopic.query.filter_by(
            curriculum_id=sp2.curriculum_id,
            name="Generating Functions and Sums of Random Variables",
        ).first()
        cs1c_check = TopicProgress.query.filter_by(
            user_id=user.id, topic_id=cs1c_topic.id,
        ).first()
        assert cs1c_check is not None
        assert cs1c_check.current_stage == TopicProgress.STAGE_LEARNING
        assert cs1c_check.completed is False
        assert cs1c_check.mastery_score == 0.0

        # Row count unchanged
        assert TopicProgress.query.filter_by(user_id=user.id).count() == 6

    def test_unsupported_exam_with_completed_topics_does_nothing(self, db, user):
        """completed_curriculum_topics passed for an unsupported examination
        must not cause any TopicProgress rows to be created."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        sp = StudyPlanService.create_study_plan(
            user_id=user.id,
            exam_name="IFoA CM1",  # not in curriculum map
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            current_stage="Chapter 1",
            study_preference="Mixed",
            target_grade="A",
            completed_curriculum_topics=["CS1-A", "CS1-B"],
        )

        assert sp.id is not None
        tp_count = TopicProgress.query.filter_by(user_id=user.id).count()
        assert tp_count == 0

    def test_completed_topics_with_none_default_is_graceful(self, db, user):
        """Calling create_study_plan without completed_curriculum_topics
        (or with None) must work identically to before (no crash)."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-A",
        )

        assert sp.id is not None
        progress_rows = TopicProgress.query.filter_by(user_id=user.id).all()
        assert len(progress_rows) == 6
        for tp in progress_rows:
            assert tp.completed is False
            assert tp.mastery_score == 0.0


class TestExaminationCatalogue:
    """Tests for IFoA dynamic sitting generation."""

    def test_ifoa_sittings_january_2026(self):
        """January 2026: the first sitting is April 2026 (same year)."""
        from datetime import date as dt_date
        from app.services.examination_catalogue import (
            _generate_ifoa_sittings,
            get_sitting_choices,
        )

        jan_2026 = dt_date(2026, 1, 15)
        sittings = _generate_ifoa_sittings(today=jan_2026)
        assert len(sittings) == 4
        assert sittings[0] == "April 2026"
        assert "April 2026" in sittings
        assert "September 2026" in sittings

        # The public API forwards to the generator for IFoA
        choices = get_sitting_choices("IFoA")
        assert len(choices) >= 1
        # First choice should not be in the past (relative to real today)
        assert choices[0][0] == choices[0][1]

    def test_ifoa_sittings_may_2026(self):
        """May 2026: April is already past, so September 2026 is next."""
        from datetime import date as dt_date
        from app.services.examination_catalogue import _generate_ifoa_sittings

        may_2026 = dt_date(2026, 5, 1)
        sittings = _generate_ifoa_sittings(today=may_2026)
        assert len(sittings) == 4
        assert sittings[0] == "September 2026"
        # April 2026 must NOT appear (it has passed)
        assert "April 2026" not in sittings

    def test_ifoa_sittings_july_2026(self):
        """July 2026: both April and September are still future,
        but September is the next available sitting."""
        from datetime import date as dt_date
        from app.services.examination_catalogue import _generate_ifoa_sittings

        jul_2026 = dt_date(2026, 7, 10)
        sittings = _generate_ifoa_sittings(today=jul_2026)
        assert len(sittings) == 4
        assert sittings[0] == "September 2026"
        assert "April 2026" not in sittings
        assert "April 2027" in sittings

    def test_ifoa_sittings_october_2026(self):
        """October 2026: both 2026 sittings have passed, so April 2027 is first."""
        from datetime import date as dt_date
        from app.services.examination_catalogue import _generate_ifoa_sittings

        oct_2026 = dt_date(2026, 10, 5)
        sittings = _generate_ifoa_sittings(today=oct_2026)
        assert len(sittings) == 4
        assert sittings[0] == "April 2027"
        assert "April 2026" not in sittings
        assert "September 2026" not in sittings

    def test_ifoa_sittings_during_april(self):
        """During April, the April sitting should still appear (same month)."""
        from datetime import date as dt_date
        from app.services.examination_catalogue import _generate_ifoa_sittings

        april_2026 = dt_date(2026, 4, 15)
        sittings = _generate_ifoa_sittings(today=april_2026)
        assert len(sittings) == 4
        assert sittings[0] == "April 2026"

    def test_ifoa_sittings_during_september(self):
        """During September, the September sitting should still appear."""
        from datetime import date as dt_date
        from app.services.examination_catalogue import _generate_ifoa_sittings

        sept_2026 = dt_date(2026, 9, 25)
        sittings = _generate_ifoa_sittings(today=sept_2026)
        assert len(sittings) == 4
        assert sittings[0] == "September 2026"

    def test_ifoa_sittings_cross_year_boundary(self):
        """December 2026: all 2026 sittings passed, next is April 2027."""
        from datetime import date as dt_date
        from app.services.examination_catalogue import _generate_ifoa_sittings

        dec_2026 = dt_date(2026, 12, 1)
        sittings = _generate_ifoa_sittings(today=dec_2026)
        assert len(sittings) == 4
        assert sittings[0] == "April 2027"
        assert "April 2026" not in sittings
        assert "September 2026" not in sittings

    def test_get_sitting_choices_non_ifoa_unchanged(self):
        """Non-IFoA categories return their hard-coded sittings."""
        from app.services.examination_catalogue import get_sitting_choices

        cfa = get_sitting_choices("CFA")
        assert len(cfa) == 4
        assert ("February 2027", "February 2027") in cfa

    def test_get_sitting_choices_unknown_category(self):
        """Unknown category returns Custom."""
        from app.services.examination_catalogue import get_sitting_choices

        choices = get_sitting_choices("DoesNotExist")
        assert choices == [("Custom", "Custom")]

    def test_generate_ifoa_sittings_custom_count(self):
        """The count parameter controls how many sittings are returned."""
        from datetime import date as dt_date
        from app.services.examination_catalogue import _generate_ifoa_sittings

        jan_2026 = dt_date(2026, 1, 1)
        sittings = _generate_ifoa_sittings(today=jan_2026, count=6)
        assert len(sittings) == 6
        assert sittings == [
            "April 2026",
            "September 2026",
            "April 2027",
            "September 2027",
            "April 2028",
            "September 2028",
        ]


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

    # ── Learning outcomes in curriculum sequence ─────────────────────────

    def test_curriculum_sequence_includes_learning_outcomes(self, db, user):
        """Each topic in the resolved curriculum sequence must include its
        ordered learning outcomes from the Curriculum Engine."""
        from app.services.planning_service import PlanningService
        from app.models.study_plan import StudyPlan

        sp = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            preferred_session_minutes=60,
            curriculum_version="2026",
            curriculum_topic_code="CS1-A",
            active=True,
        )
        db.session.add(sp)
        db.session.commit()

        sequence = PlanningService._resolve_curriculum_sequence(sp)
        assert sequence is not None
        assert len(sequence) == 6  # CS1 has 6 topics

        for topic_dict in sequence:
            assert "learning_outcomes" in topic_dict
            outcomes = topic_dict["learning_outcomes"]
            assert isinstance(outcomes, list)
            # The curriculum data file must have at least one outcome per topic
            assert len(outcomes) >= 1

    def test_curriculum_learning_outcomes_preserve_ordered_fields(self, db, user):
        """Learning outcome dicts must contain code, description, and
        suggested_revision_days in order-preserving list form."""
        from app.services.planning_service import PlanningService
        from app.models.study_plan import StudyPlan

        sp = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            preferred_session_minutes=60,
            curriculum_version="2026",
            curriculum_topic_code="CS1-A",
            active=True,
        )
        db.session.add(sp)
        db.session.commit()

        sequence = PlanningService._resolve_curriculum_sequence(sp)
        assert sequence is not None

        # Check the first topic's outcomes explicitly
        first_topic = sequence[0]
        outcomes = first_topic["learning_outcomes"]

        for lo in outcomes:
            assert "code" in lo
            assert isinstance(lo["code"], str)
            assert lo["code"] != ""

            assert "description" in lo
            assert isinstance(lo["description"], str)
            assert lo["description"] != ""

            assert "suggested_revision_days" in lo
            assert isinstance(lo["suggested_revision_days"], int)

        # Verify outcomes are in the order defined by the curriculum JSON
        # (the list itself should already be ordered by construction)
        assert outcomes[0]["code"] == "CS1-A-1"
        assert outcomes[1]["code"] == "CS1-A-2"
        assert outcomes[2]["code"] == "CS1-A-3"

    def test_non_curriculum_plan_sequence_returns_none(self):
        """A study plan without curriculum_version or curriculum_topic_code
        returns None from _resolve_curriculum_sequence."""
        from app.services.planning_service import PlanningService
        from app.models.study_plan import StudyPlan

        sp = StudyPlan(
            user_id=1,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            active=True,
        )

        result = PlanningService._resolve_curriculum_sequence(sp)
        assert result is None

    def test_unsupported_exam_sequence_returns_none(self, db, user):
        """An unsupported examination (no curriculum on disk) returns None."""
        from app.services.planning_service import PlanningService
        from app.models.study_plan import StudyPlan

        sp = StudyPlan(
            user_id=user.id,
            exam_name="IFoA ZZ9",
            exam_sitting="June 2027",
            exam_date=date.today() + timedelta(days=90),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="A",
            curriculum_version="2099",
            curriculum_topic_code="ZZ9-A",
            active=True,
        )
        db.session.add(sp)
        db.session.commit()

        result = PlanningService._resolve_curriculum_sequence(sp)
        assert result is None


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

    # ── calculate_readiness ──────────────────────────────────────────

    def test_calculate_readiness_returns_none_for_none_input(self):
        """None input returns None."""
        from app.services.readiness_service import ReadinessService

        result = ReadinessService.calculate_readiness(None)
        assert result is None

    def test_calculate_readiness_zero_completion(self):
        """0% weighted completion produces correct summary."""
        from app.services.readiness_service import (
            ReadinessService,
            ReadinessSummary,
        )
        from app.services.curriculum_engine_service import StudentCurriculumSummary

        summary = StudentCurriculumSummary(
            total_topics=6,
            completed_topics=0,
            remaining_topics=6,
            current_topic_code="CS1-A",
            next_topic_code="CS1-B",
            next_topic_title="Common Statistical Distributions",
            curriculum_coverage_percentage=0.0,
            weighted_completed_percentage=0.0,
            weighted_remaining_percentage=1.0,
            completed_topic_codes=(),
            remaining_topic_codes=("CS1-A", "CS1-B", "CS1-C", "CS1-D", "CS1-E", "CS1-F"),
        )

        result = ReadinessService.calculate_readiness(summary)
        assert result is not None
        assert isinstance(result, ReadinessSummary)
        assert result.readiness_percentage == 0.0
        assert result.weighted_completed_percentage == 0.0
        assert result.weighted_remaining_percentage == 1.0
        assert result.explanation == (
            "You have completed topics representing "
            "0% of the official syllabus weighting."
        )

    def test_calculate_readiness_full_completion(self):
        """100% weighted completion produces correct summary."""
        from app.services.readiness_service import (
            ReadinessService,
            ReadinessSummary,
        )
        from app.services.curriculum_engine_service import StudentCurriculumSummary

        summary = StudentCurriculumSummary(
            total_topics=6,
            completed_topics=6,
            remaining_topics=0,
            current_topic_code="CS1-A",
            next_topic_code=None,
            next_topic_title=None,
            curriculum_coverage_percentage=1.0,
            weighted_completed_percentage=1.0,
            weighted_remaining_percentage=0.0,
            completed_topic_codes=("CS1-A", "CS1-B", "CS1-C", "CS1-D", "CS1-E", "CS1-F"),
            remaining_topic_codes=(),
        )

        result = ReadinessService.calculate_readiness(summary)
        assert result is not None
        assert result.readiness_percentage == 1.0
        assert result.weighted_completed_percentage == 1.0
        assert result.weighted_remaining_percentage == 0.0
        assert result.explanation == (
            "You have completed topics representing "
            "100% of the official syllabus weighting."
        )

    def test_calculate_readiness_partial_completion(self):
        """45% weighted completion matches the example in requirements."""
        from app.services.readiness_service import (
            ReadinessService,
            ReadinessSummary,
        )
        from app.services.curriculum_engine_service import StudentCurriculumSummary

        summary = StudentCurriculumSummary(
            total_topics=6,
            completed_topics=3,
            remaining_topics=3,
            current_topic_code="CS1-D",
            next_topic_code="CS1-E",
            next_topic_title="Bayesian Statistics",
            curriculum_coverage_percentage=0.5,
            weighted_completed_percentage=0.45,
            weighted_remaining_percentage=0.55,
            completed_topic_codes=("CS1-A", "CS1-B", "CS1-C"),
            remaining_topic_codes=("CS1-D", "CS1-E", "CS1-F"),
        )

        result = ReadinessService.calculate_readiness(summary)
        assert result is not None
        assert result.readiness_percentage == 0.45
        assert result.weighted_completed_percentage == 0.45
        assert result.weighted_remaining_percentage == 0.55
        assert result.explanation == (
            "You have completed topics representing "
            "45% of the official syllabus weighting."
        )

    def test_readiness_summary_is_immutable(self):
        """ReadinessSummary is frozen and cannot be mutated."""
        from app.services.readiness_service import ReadinessSummary

        rs = ReadinessSummary(
            readiness_percentage=0.45,
            weighted_completed_percentage=0.45,
            weighted_remaining_percentage=0.55,
            explanation="You have completed topics representing 45% of the official syllabus weighting.",
        )

        import pytest as _pytest
        with _pytest.raises(Exception):
            rs.readiness_percentage = 0.99  # type: ignore[misc]

    def test_explanation_is_deterministic(self):
        """Same input always produces identical explanation."""
        from app.services.readiness_service import ReadinessService
        from app.services.curriculum_engine_service import StudentCurriculumSummary

        summary = StudentCurriculumSummary(
            total_topics=10,
            completed_topics=7,
            remaining_topics=3,
            current_topic_code="CM1-A",
            next_topic_code="CM1-B",
            next_topic_title="Cashflows",
            curriculum_coverage_percentage=0.7,
            weighted_completed_percentage=0.72,
            weighted_remaining_percentage=0.28,
            completed_topic_codes=tuple(f"CM1-{c}" for c in "ABCDEFG"),
            remaining_topic_codes=("CM1-H", "CM1-I", "CM1-J"),
        )

        result1 = ReadinessService.calculate_readiness(summary)
        result2 = ReadinessService.calculate_readiness(summary)

        assert result1 is not None
        assert result2 is not None
        assert result1.explanation == result2.explanation
        assert result1.readiness_percentage == result2.readiness_percentage

    def test_calculate_readiness_edge_case_rounding(self):
        """Explanation rounds the percentage to the nearest integer."""
        from app.services.readiness_service import ReadinessService
        from app.services.curriculum_engine_service import StudentCurriculumSummary

        # 0.456 → 46% when rounded
        summary = StudentCurriculumSummary(
            total_topics=6,
            completed_topics=2,
            remaining_topics=4,
            current_topic_code="CS1-C",
            next_topic_code="CS1-D",
            next_topic_title="Joint Distributions",
            curriculum_coverage_percentage=2.0 / 6.0,
            weighted_completed_percentage=0.456,
            weighted_remaining_percentage=0.544,
            completed_topic_codes=("CS1-A", "CS1-B"),
            remaining_topic_codes=("CS1-C", "CS1-D", "CS1-E", "CS1-F"),
        )

        result = ReadinessService.calculate_readiness(summary)
        assert result is not None
        assert result.explanation == (
            "You have completed topics representing "
            "46% of the official syllabus weighting."
        )


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


# ═══════════════════════════════════════════════════════════════════════════════
# CurriculumEngineService — build_student_curriculum
# ═══════════════════════════════════════════════════════════════════════════════


class TestBuildStudentCurriculum:
    """Integration tests for CurriculumEngineService.build_student_curriculum()."""

    def test_no_curriculum_id_returns_none(self, db, user):
        """When a study plan has no curriculum_id, return None."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.models.study_plan import StudyPlan

        sp = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_version=None,
            curriculum_topic_code=None,
            active=True,
        )
        db.session.add(sp)
        db.session.commit()

        svc = CurriculumEngineService()
        result = svc.build_student_curriculum(sp)
        assert result is None

    def test_no_curriculum_version_returns_none(self, db, user):
        """When a study plan has curriculum_id but no curriculum_version, return None."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.models.curriculum import Curriculum as DBCurriculum
        from app.models.study_plan import StudyPlan

        db_cur = DBCurriculum(exam_name="IFoA CS1", version="2026", active=True)
        db.session.add(db_cur)
        db.session.flush()

        sp = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_id=db_cur.id,
            curriculum_version=None,
            curriculum_topic_code=None,
            active=True,
        )
        db.session.add(sp)
        db.session.commit()

        svc = CurriculumEngineService()
        result = svc.build_student_curriculum(sp)
        assert result is None

    def test_curriculum_plan_returns_summary(self, db, user):
        """A curriculum-backed study plan produces a complete StudentCurriculumSummary."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-C",
        )

        svc = CurriculumEngineService()
        summary = svc.build_student_curriculum(sp)
        assert summary is not None
        assert summary.total_topics == 6
        assert summary.completed_topics == 0
        assert summary.remaining_topics == 6
        assert summary.current_topic_code == "CS1-C"
        assert summary.curriculum_coverage_percentage == 0.0
        assert summary.completed_topic_codes == ()
        assert len(summary.remaining_topic_codes) == 6
        expected_codes = ("CS1-A", "CS1-B", "CS1-C", "CS1-D", "CS1-E", "CS1-F")
        assert summary.remaining_topic_codes == expected_codes
        # next_topic skips current (CS1-C) → CS1-D
        assert summary.next_topic_code == "CS1-D"
        assert summary.next_topic_title is not None

    def test_completed_topics_reflected_in_summary(self, db, user):
        """Topics marked as completed in TopicProgress appear as completed."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-C",
        )

        # Mark the first two topics as completed
        rows = TopicProgress.query.filter_by(user_id=user.id).all()
        rows[0].completed = True  # CS1-A
        rows[1].completed = True  # CS1-B
        db.session.commit()

        svc = CurriculumEngineService()
        summary = svc.build_student_curriculum(sp)
        assert summary is not None
        assert summary.total_topics == 6
        assert summary.completed_topics == 2
        assert summary.remaining_topics == 4
        assert summary.curriculum_coverage_percentage == 2.0 / 6.0
        assert summary.completed_topic_codes == ("CS1-A", "CS1-B")
        assert summary.remaining_topic_codes == ("CS1-C", "CS1-D", "CS1-E", "CS1-F")
        # next_topic skips completed (CS1-A, CS1-B) and current (CS1-C) → CS1-D
        assert summary.next_topic_code == "CS1-D"
        assert summary.next_topic_title is not None

    def test_all_topics_completed(self, db, user):
        """When all topics are completed, coverage is 100%."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-C",
        )

        # Mark all topics as completed
        rows = TopicProgress.query.filter_by(user_id=user.id).all()
        for r in rows:
            r.completed = True
        db.session.commit()

        svc = CurriculumEngineService()
        summary = svc.build_student_curriculum(sp)
        assert summary is not None
        assert summary.total_topics == 6
        assert summary.completed_topics == 6
        assert summary.remaining_topics == 0
        assert summary.curriculum_coverage_percentage == 1.0
        assert summary.remaining_topic_codes == ()
        # All completed → no next topic
        assert summary.next_topic_code is None
        assert summary.next_topic_title is None

    def test_unsupported_exam_name_returns_none(self, db, user):
        """An exam name that cannot be parsed returns None."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.models.curriculum import Curriculum as DBCurriculum
        from app.models.study_plan import StudyPlan

        db_cur = DBCurriculum(exam_name="Weird Exam", version="2099", active=True)
        db.session.add(db_cur)
        db.session.flush()

        sp = StudyPlan(
            user_id=user.id,
            exam_name="Weird Exam",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_id=db_cur.id,
            curriculum_version="2099",
            curriculum_topic_code="X-A",
            active=True,
        )
        db.session.add(sp)
        db.session.commit()

        svc = CurriculumEngineService()
        summary = svc.build_student_curriculum(sp)
        assert summary is None

    def test_non_existent_curriculum_version_returns_none(self, db, user):
        """A curriculum_version that doesn't exist on-disk returns None."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.models.curriculum import Curriculum as DBCurriculum
        from app.models.study_plan import StudyPlan

        db_cur = DBCurriculum(exam_name="IFoA CS1", version="2099", active=True)
        db.session.add(db_cur)
        db.session.flush()

        sp = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=180),
            weekday_study_minutes=60,
            weekend_study_minutes=120,
            current_stage="Learning",
            study_preference="Mixed",
            target_grade="B",
            curriculum_id=db_cur.id,
            curriculum_version="2099",
            curriculum_topic_code="CS1-A",
            active=True,
        )
        db.session.add(sp)
        db.session.commit()

        svc = CurriculumEngineService()
        summary = svc.build_student_curriculum(sp)
        assert summary is None

    def test_summary_is_read_only(self, db, user):
        """The StudentCurriculumSummary is frozen and cannot be mutated."""
        from app.services.curriculum_engine_service import (
            CurriculumEngineService,
            StudentCurriculumSummary,
        )
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-C",
        )

        svc = CurriculumEngineService()
        summary = svc.build_student_curriculum(sp)
        assert summary is not None

        import pytest as _pytest
        with _pytest.raises(Exception):
            summary.total_topics = 99  # type: ignore[misc]

    def test_summary_omits_mastery_and_weightings(self, db, user):
        """The summary does not contain mastery scores or topic weightings."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-C",
        )

        svc = CurriculumEngineService()
        summary = svc.build_student_curriculum(sp)
        assert summary is not None

        from dataclasses import fields as dc_fields
        field_names = {f.name for f in dc_fields(summary)}
        assert "mastery_score" not in field_names
        assert "weighting" not in field_names
        assert "overall_mastery" not in field_names
        # But next_topic fields must be present
        assert "next_topic_code" in field_names
        assert "next_topic_title" in field_names

    def test_next_topic_when_current_is_first(self, db, user):
        """When current_topic_code is the first topic (CS1-A),
        next_topic should be CS1-B."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-A",
        )

        svc = CurriculumEngineService()
        summary = svc.build_student_curriculum(sp)
        assert summary is not None
        assert summary.next_topic_code == "CS1-B"
        assert summary.next_topic_title is not None
        assert summary.next_topic_title != ""

    def test_next_topic_skips_completed_topics(self, db, user):
        """Completed topics are ignored when determining next_topic."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress

        sp = StudyPlanService.create_study_plan(
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
            curriculum_topic_code="CS1-C",
        )

        # Mark CS1-A, CS1-B, CS1-D as completed (CS1-C is current)
        rows = TopicProgress.query.filter_by(user_id=user.id).all()
        # rows are in DB topic order; map by name
        for r in rows:
            name = r.topic.name if r.topic else ""
            if name in ("Random Variables and Distributions",
                         "Common Statistical Distributions",
                         "Joint Distributions"):
                r.completed = True
        db.session.commit()

        svc = CurriculumEngineService()
        summary = svc.build_student_curriculum(sp)
        assert summary is not None
        # Next should be CS1-E (skips completed A,B,D and current C)
        assert summary.next_topic_code == "CS1-E"
        assert summary.next_topic_title is not None

    def test_existing_behaviour_preserved(self, db):
        """Delegation methods continue to work as before."""
        from app.services.curriculum_engine_service import CurriculumEngineService

        svc = CurriculumEngineService()
        # list_supported_exams still works
        exams = svc.list_supported_exams()
        assert len(exams) >= 1

        # curriculum_exists still works
        assert svc.curriculum_exists("ifoa", "cs1", "2026") is True
        assert svc.curriculum_exists("no", "no", "9999") is False

        # get_topics still works
        svc.load_curriculum("ifoa", "cs1", "2026")
        topics = svc.get_topics("ifoa", "cs1", "2026")
        assert len(topics) == 6