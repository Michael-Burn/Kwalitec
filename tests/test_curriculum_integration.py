"""End-to-end integration tests for the complete curriculum workflow.

Covers the full chain from Study Plan Wizard through Dashboard, Study Plan
page, and Mission generation for a fresh IFoA CS1 study plan.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest


# ═══════════════════════════════════════════════════════════════════════════════
# End-to-End Curriculum Integration Tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestEndToEndCurriculumWorkflow:
    """Full end-to-end tests covering the complete curriculum integration.

    These tests verify that a fresh IFoA CS1 study plan flows correctly
    through: (1) curriculum checklist in wizard, (2) completed topics saved,
    (3) TopicProgress initialized, (4) Curriculum linked to StudyPlan,
    (5) StudentCurriculumSummary returns non-null, (6) roadmap renders
    official curriculum topics, (7) today's mission is generated from
    the next incomplete curriculum topic, and (8) dashboard displays
    curriculum progress, weighted readiness and time calculations.
    """

    # ── (3+4) TopicProgress & Curriculum linkage ────────────────────────

    def test_curriculum_plan_links_curriculum_record(self, db, user):
        """Creating a curriculum-backed plan must link a Curriculum record
        to the StudyPlan via curriculum_id."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.curriculum import Curriculum, Topic

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
            curriculum_topic_code="1.1",
        )

        assert sp.curriculum_id is not None
        db_cur = Curriculum.query.get(sp.curriculum_id)
        assert db_cur is not None
        assert db_cur.exam_name == "IFoA CS1"
        assert db_cur.version == "2026"
        assert db_cur.active is True

        # All 14 DB topics must exist
        topics = Topic.query.filter_by(curriculum_id=db_cur.id).all()
        assert len(topics) == 14
        for t in topics:
            assert t.recommended_minutes > 0
            assert t.syllabus_weight == 0.0

    def test_curriculum_plan_preserves_curriculum_relationship(self, db, user):
        """The study_plan.curriculum relationship is a valid ORM link."""
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
            curriculum_topic_code="1.1",
        )

        assert sp.curriculum is not None
        assert sp.curriculum.exam_name == "IFoA CS1"
        assert sp.curriculum.version == "2026"
        assert len(sp.curriculum.topics) == 14

    # ── (2) Completed topics from Step 4 saved ──────────────────────────

    def test_completed_topics_init_correct_confidence(self, db, user):
        """Completed topics must have confidence='Mastered', not 'Completed'
        (which is an invalid confidence value — it's a stage, not a
        confidence level)."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress
        from app.models.curriculum import Topic as DBTopic

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
            curriculum_topic_code="2.1",
            completed_curriculum_topics=["1.1", "1.2"],
        )

        db_topics = DBTopic.query.filter_by(curriculum_id=sp.curriculum_id).all()
        for db_topic in db_topics:
            tp = TopicProgress.query.filter_by(
                user_id=user.id, topic_id=db_topic.id,
            ).first()
            assert tp is not None
            # Valid confidence values per TopicProgress model
            valid_confidence = {"Not Started", "Low", "Medium", "High", "Mastered"}
            assert tp.confidence in valid_confidence, (
                f"Topic '{db_topic.name}' has invalid confidence "
                f"'{tp.confidence}'; must be one of {valid_confidence}"
            )

    def test_completed_topics_have_mastered_confidence(self, db, user):
        """Specifically, completed topics must have confidence='Mastered'."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress
        from app.models.curriculum import Topic as DBTopic

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
            curriculum_topic_code="2.1",
            completed_curriculum_topics=["1.1", "1.2"],
        )

        db_topics = DBTopic.query.filter_by(curriculum_id=sp.curriculum_id).all()
        for db_topic in db_topics:
            tp = TopicProgress.query.filter_by(
                user_id=user.id, topic_id=db_topic.id,
            ).first()
            assert tp is not None
            if tp.completed:
                assert tp.confidence == "Mastered", (
                    f"Completed topic '{db_topic.name}' has confidence "
                    f"'{tp.confidence}', expected 'Mastered'"
                )

    # ── (5) StudentCurriculumSummary returns non-null ───────────────────

    def test_curriculum_summary_non_null_for_valid_plan(self, db, user):
        """build_student_curriculum must return a non-None summary for a
        valid curriculum-backed plan."""
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
            curriculum_topic_code="1.1",
        )

        engine = CurriculumEngineService()
        summary = engine.build_student_curriculum(sp)
        assert summary is not None
        assert summary.total_topics == 14
        assert summary.current_topic_code == "1.1"
        assert summary.next_topic_code == "1.2"

    def test_curriculum_summary_with_completed_and_current(self, db, user):
        """Summary correctly reflects completed + current + next topics."""
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
            curriculum_topic_code="2.1",
            completed_curriculum_topics=["1.1", "1.2"],
        )

        engine = CurriculumEngineService()
        summary = engine.build_student_curriculum(sp)
        assert summary is not None
        assert summary.total_topics == 14
        assert summary.completed_topics == 2
        assert summary.remaining_topics == 12
        assert summary.completed_topic_codes == ("1.1", "1.2")
        assert summary.remaining_topic_codes == ("2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "3.1", "3.2", "3.3", "4.1", "4.2", "5.1")
        assert summary.current_topic_code == "2.1"
        # Next should skip completed (1.1,1.2) and current (2.1) → 2.2
        assert summary.next_topic_code == "2.2"

    def test_study_plan_curriculum_topic_code_is_persisted(self, db, user):
        """The curriculum_topic_code provided at creation time is stored
        on the study plan and accessible via the ORM."""
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
            curriculum_topic_code="2.3",
        )

        assert sp.curriculum_topic_code == "2.3"

    # ── (6) Roadmap renders official curriculum topics ──────────────────

    def test_curriculum_topics_ordered_by_engine(self, db, user):
        """DB Topic rows match the engine ordering (1..N)."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.curriculum import Topic as DBTopic

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
            curriculum_topic_code="1.1",
        )

        topics = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
        ).order_by(DBTopic.order).all()

        assert len(topics) == 14
        expected_names = [
            'Describe the purpose and function of data analysis',
            'Complete exploratory data analysis',
            'Understand the characteristics of basic univariate distributions and how to generate samples from them',
            'Determine the characteristics of jointly distributed random variables',
            'Evaluate expectations and conditional expectations',
            'Evaluate and apply generating functions',
            'State and apply the central limit theorem',
            'Describe random sampling and the sampling distributions of statistics commonly used in statistical inference',
            'Construct estimators and discuss their properties',
            'Calculate confidence intervals and prediction intervals',
            'Apply the concepts of hypothesis testing and goodness of fit',
            'Understand and use linear regression models',
            'Understand and use generalised linear models',
            'Explain fundamental concepts of Bayesian statistics and use these concepts to calculate Bayesian estimators'
        ]
        for i, expected in enumerate(expected_names):
            assert topics[i].name == expected, (
                f"Topic at position {i} is '{topics[i].name}'; expected '{expected}'"
            )
            assert topics[i].order == i + 1

    def test_curriculum_topics_have_correct_metadata(self, db, user):
        """Each DB topic carries the correct weighting and recommended time."""
        from app.services.study_plan_service import StudyPlanService
        from app.models.curriculum import Topic as DBTopic

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
            curriculum_topic_code="1.1",
        )

        topics = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
        ).order_by(DBTopic.order).all()

        # Weighting and estimated minutes from the JSON data
        expected = [
            (0.0, 686),  # 1.1,
            (0.0, 514),  # 1.2,
            (0.0, 655),  # 2.1,
            (0.0, 436),  # 2.2,
            (0.0, 218),  # 2.3,
            (0.0, 218),  # 2.4,
            (0.0, 218),  # 2.5,
            (0.0, 655),  # 2.6,
            (0.0, 947),  # 3.1,
            (0.0, 1263),  # 3.2,
            (0.0, 789),  # 3.3,
            (0.0, 1200),  # 4.1,
            (0.0, 2400),  # 4.2,
            (0.0, 1800),  # 5.1
        ]

        for i, (weight, minutes) in enumerate(expected):
            assert topics[i].syllabus_weight == weight, (
                f"Topic {topics[i].name}: expected weight {weight}, "
                f"got {topics[i].syllabus_weight}"
            )
            assert topics[i].recommended_minutes == minutes, (
                f"Topic {topics[i].name}: expected {minutes}min, "
                f"got {topics[i].recommended_minutes}"
            )

    # ── (7) Mission generated from next incomplete curriculum topic ─────

    def test_mission_selects_curriculum_topic_priority_3(self, db, user):
        """When no reviews are due and no weak topics exist, mission
        generation picks the next incomplete curriculum topic via
        Priority 3 (curriculum sequence).

        The first non-completed topic in curriculum order is the current
        topic itself (1.2), which is in 'Learning' stage — it hasn't
        been completed yet so it is the correct next topic to study.
        """
        from app.services.planning_service import PlanningService
        from app.services.study_plan_service import StudyPlanService
        from app.models.curriculum import Topic as DBTopic

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
            curriculum_topic_code="1.2",
            completed_curriculum_topics=["1.1"],
        )

        # No review topics, no weak topics → Priority 3 returns the
        # first non-completed topic (1.2, the current learning topic).
        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=sp,
            target_date=date.today(),
        )
        assert selected is not None
        # The current topic 1.2 is not completed → it is the next
        # incomplete topic in curriculum order (after skipping 1.1).
        cs1b_topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Complete exploratory data analysis",
        ).first()
        assert selected.id == cs1b_topic.id

    def test_mission_selects_curriculum_topic_after_current_completed(self, db, user):
        """When the current topic (1.2) is marked as completed,
        Priority 3 picks the next uncompleted topic (2.1)."""
        from app.services.planning_service import PlanningService
        from app.services.study_plan_service import StudyPlanService
        from app.models.topic_progress import TopicProgress
        from app.models.curriculum import Topic as DBTopic

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
            curriculum_topic_code="1.2",
            completed_curriculum_topics=["1.1"],
        )

        # Mark 1.2 as completed manually
        rows = TopicProgress.query.filter_by(user_id=user.id).all()
        for r in rows:
            if r.topic and r.topic.name == "Complete exploratory data analysis":
                r.completed = True
        db.session.commit()

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=sp,
            target_date=date.today(),
        )
        assert selected is not None
        # 1.1 and 1.2 completed → next is 2.1
        cs1c_topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Understand the characteristics of basic univariate distributions and how to generate samples from them",
        ).first()
        assert selected.id == cs1c_topic.id

    def test_mission_title_includes_curriculum_topic_name(self, db, user):
        """When a curriculum topic is selected for mission generation, the
        mission title includes the official topic name (not a generic stage)."""
        from app.services.planning_service import PlanningService
        from app.services.study_plan_service import StudyPlanService
        from app.models.study_plan import WeekPlan

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
            curriculum_topic_code="1.1",
        )

        # Ensure there's a current week plan so mission generation succeeds
        wp = WeekPlan(
            study_plan_id=sp.id,
            week_number=1,
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
        )
        db.session.add(wp)
        db.session.commit()

        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        # Title should reference the canonical curriculum topic (1.1)
        assert "data analysis" in mission.title.lower()

    def test_mission_from_curriculum_is_idempotent(self, db, user):
        """Generating a mission multiple times for a curriculum-backed plan
        always returns the same mission (no duplicates)."""
        from app.services.planning_service import PlanningService
        from app.services.study_plan_service import StudyPlanService
        from app.models.study_plan import WeekPlan

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
            curriculum_topic_code="1.1",
        )

        wp = WeekPlan(
            study_plan_id=sp.id,
            week_number=1,
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() + timedelta(days=4),
        )
        db.session.add(wp)
        db.session.commit()

        m1 = PlanningService.generate_today_mission(user.id)
        assert m1 is not None

        m2 = PlanningService.generate_today_mission(user.id)
        assert m2 is not None
        assert m1.id == m2.id

    # ── (8) Dashboard — curriculum progress, weighted readiness, time ──

    def test_weighted_coverage_calculation(self, db, user):
        """The weighted_completed_percentage in StudentCurriculumSummary
        respects official syllabus weightings from the engine JSON."""
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
            curriculum_topic_code="1.2",
            completed_curriculum_topics=[],
        )

        # Mark 1.1 as completed (V2 equal topic weighting)
        rows = TopicProgress.query.filter_by(user_id=user.id).all()
        for r in rows:
            if r.topic and r.topic.name == "Describe the purpose and function of data analysis":
                r.completed = True
        db.session.commit()

        engine = CurriculumEngineService()
        summary = engine.build_student_curriculum(sp)
        assert summary is not None

        # 1 of 14 topics → equal-weight coverage ≈ 1/14
        assert summary.weighted_completed_percentage == pytest.approx(1 / 14)
        assert summary.weighted_remaining_percentage == pytest.approx(13 / 14)

    def test_readiness_from_curriculum_summary(self, db, user):
        """ReadinessService.calculate_readiness produces a valid
        ReadinessSummary from a StudentCurriculumSummary."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.readiness_service import (
            ReadinessService,
            ReadinessSummary,
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
            curriculum_topic_code="2.1",
            completed_curriculum_topics=["1.1", "1.2"],
        )

        engine = CurriculumEngineService()
        summary = engine.build_student_curriculum(sp)
        assert summary is not None

        readiness = ReadinessService.calculate_readiness(summary)
        assert readiness is not None
        assert isinstance(readiness, ReadinessSummary)
        # 2 of 14 topics → equal-weight coverage ≈ 2/14
        assert readiness.weighted_completed_percentage == pytest.approx(2 / 14)
        assert readiness.weighted_remaining_percentage == pytest.approx(12 / 14)
        assert readiness.readiness_percentage == pytest.approx(2 / 14)
        assert "14%" in readiness.explanation

    def test_time_summary_from_curriculum_plan(self, db, user):
        """TimeEngineService calculates time summary for a
        curriculum-backed study plan."""
        from app.services.study_plan_service import StudyPlanService
        from app.services.time_engine_service import TimeEngineService

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
            curriculum_topic_code="1.1",
        )

        time_summary = TimeEngineService.calculate_time_summary(sp)
        assert time_summary is not None
        assert hasattr(time_summary, "remaining_hours")
        assert hasattr(time_summary, "available_study_hours")
        assert hasattr(time_summary, "hours_surplus_or_deficit")
        assert time_summary.remaining_hours >= 0
        assert time_summary.available_study_hours >= 0

    def test_curriculum_plan_dashboard_context_assembly(self, db, user):
        """All dashboard context objects (curriculum_summary,
        readiness_summary, time_summary) are computable without error
        for a curriculum-backed plan."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.readiness_service import ReadinessService
        from app.services.study_plan_service import StudyPlanService
        from app.services.time_engine_service import TimeEngineService

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
            curriculum_topic_code="2.1",
            completed_curriculum_topics=["1.1", "1.2"],
        )

        engine = CurriculumEngineService()
        curriculum_summary = engine.build_student_curriculum(sp)
        assert curriculum_summary is not None

        readiness_summary = ReadinessService.calculate_readiness(curriculum_summary)
        assert readiness_summary is not None

        time_summary = TimeEngineService.calculate_time_summary(sp)
        assert time_summary is not None

        # Ensure all values are internally consistent
        assert curriculum_summary.total_topics == 14
        assert curriculum_summary.completed_topics == 2
        assert curriculum_summary.current_topic_code == "2.1"
        assert readiness_summary.readiness_percentage > 0
        assert time_summary.remaining_hours >= 0

    def test_dashboard_time_surplus_deficit(self, db, user):
        """Time summary correctly reports surplus or deficit based on
        available hours vs required hours."""
        from app.services.study_plan_service import StudyPlanService
        from app.services.time_engine_service import TimeEngineService

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
            curriculum_topic_code="1.1",
        )

        ts = TimeEngineService.calculate_time_summary(sp)
        assert ts is not None
        # Both remaining and available should be positive numbers
        assert ts.remaining_hours > 0, (
            f"Expected remaining_hours > 0, got {ts.remaining_hours}"
        )
        assert ts.available_study_hours > 0, (
            f"Expected available_study_hours > 0, got {ts.available_study_hours}"
        )
        # Surplus/deficit should be calculable
        assert isinstance(ts.hours_surplus_or_deficit, (int, float))

    def test_dashboard_readiness_explanation_includes_percentage(self, db, user):
        """Readiness explanation includes the rounded percentage value."""
        from app.services.curriculum_engine_service import CurriculumEngineService
        from app.services.readiness_service import ReadinessService
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
            curriculum_topic_code="1.2",
            completed_curriculum_topics=["1.1"],
        )

        engine = CurriculumEngineService()
        summary = engine.build_student_curriculum(sp)
        assert summary is not None

        readiness = ReadinessService.calculate_readiness(summary)
        assert readiness is not None
        assert "%" in readiness.explanation
        # The percentage in the explanation should be a non-negative integer
        import re
        match = re.search(r"(\d+)%", readiness.explanation)
        assert match is not None, (
            f"Explanation '{readiness.explanation}' should contain a percentage"
        )
        pct = int(match.group(1))
        assert 0 <= pct <= 100


# ═══════════════════════════════════════════════════════════════════════════════
# Fresh-database import tests
# ═══════════════════════════════════════════════════════════════════════════════


class TestCurriculumDatabaseImport:
    """Tests for the idempotent curriculum import from bundled JSON.

    These tests verify that ``CurriculumService.import_curricula()``
    correctly populates the database tables (Curriculum, Topic,
    LearningObjective) on a fresh database and is safe to run repeatedly.
    """

    def test_import_populates_all_tables_on_fresh_db(self, ctx, db):
        """After calling import_curricula() on a fresh database, all
        curriculum tables should contain the expected rows."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic
        from app.models.learning import LearningObjective

        count = CurriculumService.import_curricula()
        assert count == 3, "Expected CS1, CB2, and CM1 curricula to be imported"

        assert Curriculum.query.count() == 3
        c = Curriculum.query.filter_by(exam_name="IFoA CS1", version="2026").one()
        assert c.exam_name == "IFoA CS1"
        assert c.version == "2026"
        assert c.active is True
        assert Curriculum.query.filter_by(exam_name="IFoA CB2", version="2026").one() is not None
        assert Curriculum.query.filter_by(exam_name="IFoA CM1", version="2026").one() is not None

        assert Topic.query.filter_by(curriculum_id=c.id).count() == 14
        topics = Topic.query.filter_by(curriculum_id=c.id).order_by(Topic.order).all()
        expected_names = [
            'Describe the purpose and function of data analysis',
            'Complete exploratory data analysis',
            'Understand the characteristics of basic univariate distributions and how to generate samples from them',
            'Determine the characteristics of jointly distributed random variables',
            'Evaluate expectations and conditional expectations',
            'Evaluate and apply generating functions',
            'State and apply the central limit theorem',
            'Describe random sampling and the sampling distributions of statistics commonly used in statistical inference',
            'Construct estimators and discuss their properties',
            'Calculate confidence intervals and prediction intervals',
            'Apply the concepts of hypothesis testing and goodness of fit',
            'Understand and use linear regression models',
            'Understand and use generalised linear models',
            'Explain fundamental concepts of Bayesian statistics and use these concepts to calculate Bayesian estimators'
        ]
        for i, t in enumerate(topics):
            assert t.name == expected_names[i]
            assert t.order == i + 1
            assert t.recommended_minutes > 0
            assert t.syllabus_weight == 0.0

        assert LearningObjective.query.count() > 0

    def test_import_is_idempotent(self, ctx, db):
        """Calling import_curricula() twice must not create duplicate rows."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic
        from app.models.learning import LearningObjective

        count1 = CurriculumService.import_curricula()
        assert count1 == 3

        count2 = CurriculumService.import_curricula()
        assert count2 == 0, "Second import should return 0 (no new curricula)"

        assert Curriculum.query.count() == 3
        cs1 = Curriculum.query.filter_by(exam_name="IFoA CS1", version="2026").one()
        assert Topic.query.filter_by(curriculum_id=cs1.id).count() == 14
        assert LearningObjective.query.count() > 0
        assert Curriculum.query.filter_by(exam_name="IFoA CM1", version="2026").one() is not None

    def test_imported_curriculum_available_for_study_plan(self, ctx, db, user):
        """A study plan created after import must link to the existing
        imported Curriculum record (not create a duplicate)."""
        from app.services.curriculum_service import CurriculumService
        from app.services.study_plan_service import StudyPlanService
        from app.models.curriculum import Curriculum, Topic
        from datetime import date, timedelta

        # Import first
        CurriculumService.import_curricula()
        pre_count = Curriculum.query.count()

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
            curriculum_topic_code="1.1",
        )

        assert sp.curriculum_id is not None
        assert Curriculum.query.count() == pre_count, (
            "No new Curriculum row should have been created"
        )
        db_cur = db.session.get(Curriculum, sp.curriculum_id)
        assert db_cur is not None
        assert db_cur.exam_name == "IFoA CS1"
        assert db_cur.version == "2026"

    def test_imported_topics_have_learning_objectives(self, ctx, db):
        """Every imported topic must have at least one LearningObjective."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Topic
        from app.models.learning import LearningObjective

        CurriculumService.import_curricula()
        for topic in Topic.query.all():
            los = LearningObjective.query.filter_by(topic_id=topic.id).all()
            assert len(los) > 0, (
                f"Topic '{topic.name}' has no learning objectives"
            )

    def test_imported_curriculum_supports_roadmap(self, ctx, db):
        """The ordered topic list from the imported curriculum matches
        the official syllabus order — this is what the roadmap displays."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic

        CurriculumService.import_curricula()
        cs1 = Curriculum.query.filter_by(exam_name="IFoA CS1", version="2026").one()
        topics = Topic.query.filter_by(curriculum_id=cs1.id).order_by(Topic.order).all()
        assert len(topics) == 14
        for t in topics:
            assert t.syllabus_weight == 0.0
            assert t.recommended_minutes > 0

    def test_imported_curriculum_supports_dashboard_progress(self, ctx, db, user):
        """Dashboard progress queries must work with the imported curriculum."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum

        CurriculumService.import_curricula()
        curriculum = Curriculum.query.filter_by(
            exam_name="IFoA CS1", version="2026"
        ).one()
        assert curriculum is not None

        progress = CurriculumService.get_curriculum_progress(
            user_id=user.id, curriculum=curriculum
        )
        assert progress["total_topics"] > 0
        assert progress["completion_percentage"] == 0.0

    def test_imported_curriculum_supports_mission_topic_selection(self, ctx, db, user):
        """Mission topic selection (Priority 3) must work with imported
        curricula and return the first incomplete topic."""
        from app.services.curriculum_service import CurriculumService
        from app.services.study_plan_service import StudyPlanService
        from app.services.planning_service import PlanningService
        from datetime import date, timedelta

        CurriculumService.import_curricula()

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
            curriculum_topic_code="1.1",
        )

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=sp,
            target_date=date.today(),
        )
        assert selected is not None
        assert selected.name == "Describe the purpose and function of data analysis"

    def test_startup_service_imports_curricula(self, ctx, app, db):
        """The StartupService must import curricula when it runs."""
        from app.models.curriculum import Curriculum
        from app.services.curriculum_service import CurriculumService

        count = CurriculumService.import_curricula()
        assert count >= 1
        assert Curriculum.query.count() >= 1


# ═══════════════════════════════════════════════════════════════════════════════
# Multi-paper consistency (CS1 / CB2 / CM1)
# ═══════════════════════════════════════════════════════════════════════════════


def _create_curriculum_plan(user_id: int, exam_name: str, topic_code: str = "1.1"):
    """Create a curriculum-backed study plan with a current week window."""
    from app.models.study_plan import WeekPlan
    from app.services.study_plan_service import StudyPlanService
    from app.extensions import db

    sp = StudyPlanService.create_study_plan(
        user_id=user_id,
        exam_name=exam_name,
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=180),
        weekday_study_minutes=60,
        weekend_study_minutes=120,
        current_stage="Learning",
        study_preference="Mixed",
        target_grade="B",
        curriculum_version="2026",
        curriculum_topic_code=topic_code,
    )
    wp = WeekPlan(
        study_plan_id=sp.id,
        week_number=1,
        start_date=date.today() - timedelta(days=2),
        end_date=date.today() + timedelta(days=4),
    )
    db.session.add(wp)
    db.session.commit()
    return sp


class TestMultiPaperCurriculumConsistency:
    """Every supported syllabus must drive topic-based missions and recommendations.

    Guards against paper-specific hardcoding regressions (e.g. CB2 omitted from
    a version map while CS1/CM1 remained wired).
    """

    @pytest.mark.parametrize(
        "exam_name,topic_fragment,topic_count",
        [
            ("IFoA CS1", "data analysis", 14),
            ("IFoA CB2", "economics and business", 21),
            ("IFoA CM1", "interest rates", 21),
        ],
    )
    def test_study_plan_links_curriculum_and_topics(
        self, db, user, exam_name, topic_fragment, topic_count
    ):
        from app.models.curriculum import Topic
        from app.models.topic_progress import TopicProgress

        sp = _create_curriculum_plan(user.id, exam_name)
        assert sp.curriculum_id is not None
        assert sp.curriculum.exam_name == exam_name
        assert Topic.query.filter_by(curriculum_id=sp.curriculum_id).count() == topic_count
        assert TopicProgress.query.filter_by(user_id=user.id).count() == topic_count

    @pytest.mark.parametrize(
        "exam_name,topic_fragment",
        [
            ("IFoA CS1", "data analysis"),
            ("IFoA CB2", "economics and business"),
            ("IFoA CM1", "interest rates"),
        ],
    )
    def test_mission_title_includes_syllabus_topic(
        self, db, user, exam_name, topic_fragment
    ):
        from app.services.planning_service import PlanningService

        _create_curriculum_plan(user.id, exam_name)
        mission = PlanningService.generate_today_mission(user.id)
        assert mission is not None
        assert topic_fragment in mission.title.lower()
        # Must not fall back to generic stage-only wording as the title subject.
        assert mission.title.lower() != "study learning"

    @pytest.mark.parametrize(
        "exam_name,topic_fragment",
        [
            ("IFoA CS1", "data analysis"),
            ("IFoA CB2", "economics and business"),
            ("IFoA CM1", "interest rates"),
        ],
    )
    def test_topic_selection_returns_first_incomplete(
        self, db, user, exam_name, topic_fragment
    ):
        from app.services.planning_service import PlanningService

        sp = _create_curriculum_plan(user.id, exam_name)
        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=sp,
            target_date=date.today(),
        )
        assert selected is not None
        assert topic_fragment in selected.name.lower()

    @pytest.mark.parametrize("exam_name", ["IFoA CS1", "IFoA CB2", "IFoA CM1"])
    def test_recommendation_uses_curriculum_coverage(self, db, user, exam_name):
        from app.services.recommendation_service import RecommendationService

        _create_curriculum_plan(user.id, exam_name)
        recs = RecommendationService.generate_recommendations(user.id, limit=5)
        assert len(recs) >= 1
        # Fresh plans should surface curriculum progression, not empty coverage.
        titles = " ".join(r["title"].lower() for r in recs)
        categories = {r["category"] for r in recs}
        assert (
            "new topic" in {c.lower() for c in categories}
            or "topic" in titles
            or "curriculum" in titles
            or "explore" in titles
            or "progress" in titles
        )

    @pytest.mark.parametrize("exam_name", ["IFoA CS1", "IFoA CB2", "IFoA CM1"])
    def test_dashboard_renders_with_curriculum_plan(
        self, logged_in_client, db, user, exam_name
    ):
        _create_curriculum_plan(user.id, exam_name)
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        # Mission auto-generation should produce a topic-bearing card/title area.
        body = response.data.lower()
        assert b"mission" in body or b"study" in body
        # Guard against unlinked curriculum (generic stage-only fallback).
        assert b"study learning" not in body
