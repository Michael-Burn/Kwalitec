"""Unit tests for the Time Engine Service.

Covers:
    - TimeSummary dataclass (immutability, defaults)
    - calculate_time_summary edge cases
    - Deterministic calculations for total, completed, remaining,
      available, and surplus/deficit hours.
"""

from __future__ import annotations

from dataclasses import asdict
from datetime import date, datetime, timedelta

import pytest


# ═══════════════════════════════════════════════════════════════════════════════
# TimeSummary dataclass
# ═══════════════════════════════════════════════════════════════════════════════


class TestTimeSummary:
    """Tests for the TimeSummary immutable dataclass."""

    def test_create_all_fields(self):
        from app.services.time_engine_service import TimeSummary

        ts = TimeSummary(
            total_curriculum_hours=100.0,
            completed_hours=30.0,
            remaining_hours=70.0,
            available_study_hours=80.0,
            hours_surplus_or_deficit=10.0,
        )
        assert ts.total_curriculum_hours == 100.0
        assert ts.completed_hours == 30.0
        assert ts.remaining_hours == 70.0
        assert ts.available_study_hours == 80.0
        assert ts.hours_surplus_or_deficit == 10.0

    def test_is_frozen(self):
        from app.services.time_engine_service import TimeSummary

        ts = TimeSummary(
            total_curriculum_hours=100.0,
            completed_hours=0.0,
            remaining_hours=100.0,
            available_study_hours=50.0,
            hours_surplus_or_deficit=-50.0,
        )
        with pytest.raises(Exception):
            ts.total_curriculum_hours = 200.0  # type: ignore[misc]

    def test_equality(self):
        from app.services.time_engine_service import TimeSummary

        a = TimeSummary(100, 10, 90, 80, -10)
        b = TimeSummary(100, 10, 90, 80, -10)
        c = TimeSummary(200, 10, 190, 80, -110)
        assert a == b
        assert a != c

    def test_negative_values_allowed(self):
        """Surplus/deficit can be negative — that's a deficit."""
        from app.services.time_engine_service import TimeSummary

        ts = TimeSummary(
            total_curriculum_hours=50.0,
            completed_hours=0.0,
            remaining_hours=50.0,
            available_study_hours=30.0,
            hours_surplus_or_deficit=-20.0,
        )
        assert ts.hours_surplus_or_deficit == -20.0

    def test_asdict(self):
        from app.services.time_engine_service import TimeSummary

        ts = TimeSummary(100, 20, 80, 90, 10)
        d = asdict(ts)
        assert d["total_curriculum_hours"] == 100


# ═══════════════════════════════════════════════════════════════════════════════
# calculate_time_summary
# ═══════════════════════════════════════════════════════════════════════════════


class TestCalculateTimeSummary:
    """Tests for TimeEngineService.calculate_time_summary()."""

    # ── helpers ──────────────────────────────────────────────────────────

    @staticmethod
    def _make_study_plan(
        app,
        *,
        exam_name="IFoA CS1",
        exam_date=None,
        curriculum_id=None,
        curriculum_version=None,
        weekday_study_minutes=120,
        weekend_study_minutes=180,
        user_id=1,
    ):
        """Create a StudyPlan in the test DB and return it."""
        from app.extensions import db
        from app.models.study_plan import StudyPlan

        if exam_date is None:
            exam_date = date.today() + timedelta(days=100)

        sp = StudyPlan(
            user_id=user_id,
            curriculum_id=curriculum_id,
            exam_name=exam_name,
            exam_sitting="April 2027",
            exam_date=exam_date,
            weekday_study_minutes=weekday_study_minutes,
            weekend_study_minutes=weekend_study_minutes,
            current_stage="Chapter 1",
            study_preference="Mixed",
            target_grade="A",
            preferred_session_minutes=60,
            curriculum_version=curriculum_version,
            active=True,
        )
        db.session.add(sp)
        db.session.commit()
        return sp

    @staticmethod
    def _make_curriculum_with_db_topics(app, version="2026"):
        """Create a DB Curriculum with Topics that match canonical CS1 V2 titles.

        Returns (db_curriculum, list_of_db_topics).
        """
        from app.extensions import db
        from app.models.curriculum import Curriculum, Topic

        c = Curriculum(exam_name="IFoA CS1", version=version, active=True)
        db.session.add(c)
        db.session.flush()

        # Topic names MUST match the canonical CS1 2026 JSON titles
        topic_specs = [
            ("Describe the purpose and function of data analysis", 686),
            ("Complete exploratory data analysis", 514),
            (
                "Understand the characteristics of basic univariate "
                "distributions and how to generate samples from them",
                655,
            ),
            (
                "Determine the characteristics of jointly distributed "
                "random variables",
                436,
            ),
            ("Evaluate expectations and conditional expectations", 218),
            ("Evaluate and apply generating functions", 218),
            ("State and apply the central limit theorem", 218),
            (
                "Describe random sampling and the sampling distributions of "
                "statistics commonly used in statistical inference",
                655,
            ),
            ("Construct estimators and discuss their properties", 947),
            ("Calculate confidence intervals and prediction intervals", 1263),
            ("Apply the concepts of hypothesis testing and goodness of fit", 789),
            ("Understand and use linear regression models", 1200),
            ("Understand and use generalised linear models", 2400),
            (
                "Explain fundamental concepts of Bayesian statistics and use "
                "these concepts to calculate Bayesian estimators",
                1800,
            ),
        ]
        topics = [
            Topic(
                name=name,
                curriculum_id=c.id,
                order=i,
                recommended_minutes=minutes,
                active=True,
                syllabus_weight=0.0,
            )
            for i, (name, minutes) in enumerate(topic_specs, start=1)
        ]
        db.session.add_all(topics)
        db.session.commit()
        return c, topics

    @staticmethod
    def _set_topic_completed(app, user_id, topic_id):
        from app.extensions import db
        from app.models.topic_progress import TopicProgress

        tp = TopicProgress(
            user_id=user_id,
            topic_id=topic_id,
            mastery_score=80.0,
            current_stage=TopicProgress.STAGE_MASTERED,
            revision_count=5,
            completed=True,
        )
        db.session.add(tp)
        db.session.commit()
        return tp

    # ── tests ────────────────────────────────────────────────────────────

    def test_returns_none_when_no_curriculum_id(self, app, db, ctx):
        sp = self._make_study_plan(app)
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is None

    def test_returns_none_when_no_curriculum_version(self, app, db, ctx):
        c, _ = self._make_curriculum_with_db_topics(app)  # noqa: F841
        sp = self._make_study_plan(
            app,
            curriculum_id=c.id,
            curriculum_version=None,
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is None

    def test_returns_none_when_curriculum_not_loadable(self, app, db, ctx):
        """Bogus version that has no JSON file on disk."""
        c, _ = self._make_curriculum_with_db_topics(app, version="2099")
        sp = self._make_study_plan(
            app,
            curriculum_id=c.id,
            curriculum_version="2099",
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is None

    def test_returns_none_when_exam_name_unparseable(self, app, db, ctx):
        c, _ = self._make_curriculum_with_db_topics(app)
        sp = self._make_study_plan(
            app,
            exam_name="NonExistentCategory",
            curriculum_id=c.id,
            curriculum_version="2026",
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is None

    def test_no_completed_topics_all_hours_remaining(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841
        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=100),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None

        # Canonical CS1 V2 ≈ 200h from topic estimated_minutes
        assert result.total_curriculum_hours == 199.98
        assert result.completed_hours == 0.0
        assert result.remaining_hours == 199.98

    def test_some_completed_topics(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)
        # Mark first topic (11.43h) as completed
        self._set_topic_completed(app, 1, topics[0].id)
        # Mark third topic (10.92h) as completed
        self._set_topic_completed(app, 1, topics[2].id)

        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=100),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            user_id=1,
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None

        # completed: 11.43 + 10.92 = 22.35
        assert result.total_curriculum_hours == 199.98
        assert result.completed_hours == 22.35
        assert result.remaining_hours == 177.63

    def test_all_topics_completed(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)
        for t in topics:
            self._set_topic_completed(app, 1, t.id)

        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=100),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            user_id=1,
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None
        assert result.completed_hours == 199.98
        assert result.remaining_hours == 0.0

    def test_available_study_hours_calculation(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841

        # 7 days remaining, 60 min weekdays, 60 min weekends → pure 60 min/day
        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=7),
            weekday_study_minutes=60,
            weekend_study_minutes=60,
            user_id=1,
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None

        # 7 days × 60 min / 60 = 7 hours
        assert result.available_study_hours == 7.0

    def test_available_study_hours_weighted_average(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841

        # weekday=120, weekend=180 → (5*120 + 2*180)/7 = 960/7 ≈ 137.14 min/day
        # 14 days → 14 * 137.14... / 60 = ~32.0 hours
        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=14),
            weekday_study_minutes=120,
            weekend_study_minutes=180,
            user_id=1,
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None

        expected_minutes = (120 * 5 + 180 * 2) / 7.0
        expected_hours = round((14 * expected_minutes) / 60.0, 2)
        assert result.available_study_hours == expected_hours

    def test_exam_in_past_available_hours_zero(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841

        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() - timedelta(days=10),
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None
        assert result.available_study_hours == 0.0

    def test_exam_today_available_hours_zero(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841

        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today(),
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None
        assert result.available_study_hours == 0.0

    def test_surplus_when_available_exceeds_remaining(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841

        # 200 days at 120 min/day → 400 hours available, only ~199.98 needed
        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=200),
            weekday_study_minutes=120,
            weekend_study_minutes=120,
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None
        # 200 * 120 / 60 = 400 available, 199.98 remaining → surplus
        assert result.hours_surplus_or_deficit > 0

    def test_deficit_when_remaining_exceeds_available(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841

        # 10 days at 60 min → 10 hours available, 199.98 needed → deficit
        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=10),
            weekday_study_minutes=60,
            weekend_study_minutes=60,
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None
        assert result.available_study_hours == 10.0
        assert result.remaining_hours == 199.98
        assert result.hours_surplus_or_deficit == -189.98

    def test_deterministic_same_input_same_output(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841
        self._set_topic_completed(app, 1, topics[0].id)

        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=50),
            weekday_study_minutes=90,
            weekend_study_minutes=120,
            user_id=1,
        )
        from app.services.time_engine_service import TimeEngineService

        r1 = TimeEngineService.calculate_time_summary(sp)
        r2 = TimeEngineService.calculate_time_summary(sp)
        assert r1 == r2

    def test_handles_datetime_exam_date(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841

        # Simulate a datetime exam_date (some ORMs return datetime even for Date columns)
        exam_dt = datetime.now() + timedelta(days=30)
        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=exam_dt,
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None
        # Should still compute available hours
        assert result.available_study_hours > 0

    def test_different_user_sees_only_their_progress(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)

        # User 1 completes topic 0 (11.43h)
        self._set_topic_completed(app, 1, topics[0].id)

        # User 2 has no completions
        sp1 = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=100),
            user_id=1,
        )
        sp2 = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=100),
            user_id=2,
        )
        from app.services.time_engine_service import TimeEngineService

        r1 = TimeEngineService.calculate_time_summary(sp1)
        r2 = TimeEngineService.calculate_time_summary(sp2)

        assert r1 is not None
        assert r2 is not None
        assert r1.completed_hours == 11.43
        assert r2.completed_hours == 0.0

    def test_values_are_rounded_to_two_decimals(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841

        # 1 day remaining, 123 min → 123/60 = 2.05 hours
        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=1),
            weekday_study_minutes=123,
            weekend_study_minutes=123,
        )
        from app.services.time_engine_service import TimeEngineService

        result = TimeEngineService.calculate_time_summary(sp)
        assert result is not None
        assert result.available_study_hours == 2.05

    def test_result_is_time_summary_type(self, app, db, ctx):
        c, topics = self._make_curriculum_with_db_topics(app)  # noqa: F841

        sp = self._make_study_plan(
            app,
            exam_name="IFoA CS1",
            curriculum_id=c.id,
            curriculum_version="2026",
            exam_date=date.today() + timedelta(days=50),
        )
        from app.services.time_engine_service import TimeEngineService, TimeSummary

        result = TimeEngineService.calculate_time_summary(sp)
        assert isinstance(result, TimeSummary)