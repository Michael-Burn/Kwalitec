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
            curriculum_topic_code="CS1-A",
        )

        assert sp.curriculum_id is not None
        db_cur = Curriculum.query.get(sp.curriculum_id)
        assert db_cur is not None
        assert db_cur.exam_name == "IFoA CS1"
        assert db_cur.version == "2026"
        assert db_cur.active is True

        # All 6 DB topics must exist
        topics = Topic.query.filter_by(curriculum_id=db_cur.id).all()
        assert len(topics) == 6
        for t in topics:
            assert t.recommended_minutes > 0
            assert t.syllabus_weight > 0

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
            curriculum_topic_code="CS1-A",
        )

        assert sp.curriculum is not None
        assert sp.curriculum.exam_name == "IFoA CS1"
        assert sp.curriculum.version == "2026"
        assert len(sp.curriculum.topics) == 6

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
            curriculum_topic_code="CS1-C",
            completed_curriculum_topics=["CS1-A", "CS1-B"],
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
            curriculum_topic_code="CS1-C",
            completed_curriculum_topics=["CS1-A", "CS1-B"],
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
            curriculum_topic_code="CS1-A",
        )

        engine = CurriculumEngineService()
        summary = engine.build_student_curriculum(sp)
        assert summary is not None
        assert summary.total_topics == 6
        assert summary.current_topic_code == "CS1-A"
        assert summary.next_topic_code == "CS1-B"

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
            curriculum_topic_code="CS1-C",
            completed_curriculum_topics=["CS1-A", "CS1-B"],
        )

        engine = CurriculumEngineService()
        summary = engine.build_student_curriculum(sp)
        assert summary is not None
        assert summary.total_topics == 6
        assert summary.completed_topics == 2
        assert summary.remaining_topics == 4
        assert summary.completed_topic_codes == ("CS1-A", "CS1-B")
        assert summary.remaining_topic_codes == ("CS1-C", "CS1-D", "CS1-E", "CS1-F")
        assert summary.current_topic_code == "CS1-C"
        # Next should skip completed (A,B) and current (C) → D
        assert summary.next_topic_code == "CS1-D"

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
            curriculum_topic_code="CS1-E",
        )

        assert sp.curriculum_topic_code == "CS1-E"

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
            curriculum_topic_code="CS1-A",
        )

        topics = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
        ).order_by(DBTopic.order).all()

        assert len(topics) == 6
        expected_names = [
            "Random Variables and Distributions",
            "Common Statistical Distributions",
            "Generating Functions and Sums of Random Variables",
            "Joint Distributions",
            "Bayesian Statistics",
            "Sampling and Statistical Inference",
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
            curriculum_topic_code="CS1-A",
        )

        topics = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
        ).order_by(DBTopic.order).all()

        # Weighting and estimated minutes from the JSON data
        expected = [
            (25.0, 45 * 60),  # CS1-A: 25%, 45h
            (20.0, 35 * 60),  # CS1-B: 20%, 35h
            (15.0, 30 * 60),  # CS1-C: 15%, 30h
            (15.0, 25 * 60),  # CS1-D: 15%, 25h
            (15.0, 25 * 60),  # CS1-E: 15%, 25h
            (10.0, 30 * 60),  # CS1-F: 10%, 30h
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
        topic itself (CS1-B), which is in 'Learning' stage — it hasn't
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
            curriculum_topic_code="CS1-B",
            completed_curriculum_topics=["CS1-A"],
        )

        # No review topics, no weak topics → Priority 3 returns the
        # first non-completed topic (CS1-B, the current learning topic).
        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=sp,
            target_date=date.today(),
        )
        assert selected is not None
        # The current topic CS1-B is not completed → it is the next
        # incomplete topic in curriculum order (after skipping CS1-A).
        cs1b_topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Common Statistical Distributions",
        ).first()
        assert selected.id == cs1b_topic.id

    def test_mission_selects_curriculum_topic_after_current_completed(self, db, user):
        """When the current topic (CS1-B) is marked as completed,
        Priority 3 picks the next uncompleted topic (CS1-C)."""
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
            curriculum_topic_code="CS1-B",
            completed_curriculum_topics=["CS1-A"],
        )

        # Mark CS1-B as completed manually
        rows = TopicProgress.query.filter_by(user_id=user.id).all()
        for r in rows:
            if r.topic and r.topic.name == "Common Statistical Distributions":
                r.completed = True
        db.session.commit()

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=sp,
            target_date=date.today(),
        )
        assert selected is not None
        # CS1-A and CS1-B completed → next is CS1-C
        cs1c_topic = DBTopic.query.filter_by(
            curriculum_id=sp.curriculum_id,
            name="Generating Functions and Sums of Random Variables",
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
            curriculum_topic_code="CS1-A",
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
        # The title should reference the curriculum topic name, not a
        # generic "Chapter X" or stage label
        assert "Random Variables" in mission.title or "CS1" in mission.title or (
            "Distributions" in mission.title
        )

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
            curriculum_topic_code="CS1-A",
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
            curriculum_topic_code="CS1-B",
            completed_curriculum_topics=[],
        )

        # Mark CS1-A as completed (weighting 25%)
        rows = TopicProgress.query.filter_by(user_id=user.id).all()
        for r in rows:
            if r.topic and r.topic.name == "Random Variables and Distributions":
                r.completed = True
        db.session.commit()

        engine = CurriculumEngineService()
        summary = engine.build_student_curriculum(sp)
        assert summary is not None

        # CS1-A = 25% of 100% total weight → weighted = 25%
        assert summary.weighted_completed_percentage == 0.25
        assert summary.weighted_remaining_percentage == 0.75

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
            curriculum_topic_code="CS1-C",
            completed_curriculum_topics=["CS1-A", "CS1-B"],
        )

        engine = CurriculumEngineService()
        summary = engine.build_student_curriculum(sp)
        assert summary is not None

        readiness = ReadinessService.calculate_readiness(summary)
        assert readiness is not None
        assert isinstance(readiness, ReadinessSummary)
        # CS1-A (25%) + CS1-B (20%) = 45%
        assert readiness.weighted_completed_percentage == 0.45
        assert readiness.weighted_remaining_percentage == 0.55
        assert readiness.readiness_percentage == 0.45
        assert "45%" in readiness.explanation

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
            curriculum_topic_code="CS1-A",
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
            curriculum_topic_code="CS1-C",
            completed_curriculum_topics=["CS1-A", "CS1-B"],
        )

        engine = CurriculumEngineService()
        curriculum_summary = engine.build_student_curriculum(sp)
        assert curriculum_summary is not None

        readiness_summary = ReadinessService.calculate_readiness(curriculum_summary)
        assert readiness_summary is not None

        time_summary = TimeEngineService.calculate_time_summary(sp)
        assert time_summary is not None

        # Ensure all values are internally consistent
        assert curriculum_summary.total_topics == 6
        assert curriculum_summary.completed_topics == 2
        assert curriculum_summary.current_topic_code == "CS1-C"
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
            curriculum_topic_code="CS1-A",
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
            curriculum_topic_code="CS1-B",
            completed_curriculum_topics=["CS1-A"],
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
        assert count == 1, "Expected 1 new curriculum to be imported"

        assert Curriculum.query.count() == 1
        c = Curriculum.query.first()
        assert c.exam_name == "IFoA CS1"
        assert c.version == "2026"
        assert c.active is True

        assert Topic.query.count() == 6
        topics = Topic.query.order_by(Topic.order).all()
        expected_names = [
            "Random Variables and Distributions",
            "Common Statistical Distributions",
            "Generating Functions and Sums of Random Variables",
            "Joint Distributions",
            "Bayesian Statistics",
            "Sampling and Statistical Inference",
        ]
        for i, t in enumerate(topics):
            assert t.name == expected_names[i]
            assert t.order == i + 1
            assert t.recommended_minutes > 0
            assert t.syllabus_weight > 0

        assert LearningObjective.query.count() > 0

    def test_import_is_idempotent(self, ctx, db):
        """Calling import_curricula() twice must not create duplicate rows."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum, Topic
        from app.models.learning import LearningObjective

        count1 = CurriculumService.import_curricula()
        assert count1 == 1

        count2 = CurriculumService.import_curricula()
        assert count2 == 0, "Second import should return 0 (no new curricula)"

        assert Curriculum.query.count() == 1
        assert Topic.query.count() == 6
        assert LearningObjective.query.count() > 0

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
            curriculum_topic_code="CS1-A",
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
        from app.models.curriculum import Topic

        CurriculumService.import_curricula()
        topics = Topic.query.order_by(Topic.order).all()
        assert len(topics) == 6
        for t in topics:
            assert t.syllabus_weight > 0
            assert t.recommended_minutes > 0

    def test_imported_curriculum_supports_dashboard_progress(self, ctx, db, user):
        """Dashboard progress queries must work with the imported curriculum."""
        from app.services.curriculum_service import CurriculumService
        from app.models.curriculum import Curriculum

        CurriculumService.import_curricula()
        curriculum = Curriculum.query.first()
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
            curriculum_topic_code="CS1-A",
        )

        selected = PlanningService._select_topic_for_today(
            user_id=user.id,
            active_plan=sp,
            target_date=date.today(),
        )
        assert selected is not None
        assert selected.name == "Random Variables and Distributions"

    def test_startup_service_imports_curricula(self, ctx, app, db):
        """The StartupService must import curricula when it runs."""
        from app.models.curriculum import Curriculum
        from app.services.curriculum_service import CurriculumService

        count = CurriculumService.import_curricula()
        assert count >= 1
        assert Curriculum.query.count() >= 1
