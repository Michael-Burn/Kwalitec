"""V1SP-003 — Performance optimisation regression and budget tests."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from app.extensions import db
from app.founder.dashboard.services.operational_health_service import (
    OperationalHealthService,
)
from app.models.mission import Mission
from app.models.study_plan import StudyPlan
from app.models.subject import Subject
from app.models.user import User
from app.services.analytics_service import AnalyticsService
from app.services.readiness_service import ReadinessService
from app.services.research_feedback_service import (
    SOURCE_SETTINGS,
    ResearchFeedbackService,
)
from tests.perf_v1sp003_harness import count_queries, measure_static_assets


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


def _login(client, email: str, password: str = "password123") -> None:
    client.post(
        "/auth/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )


class TestQueryBudgets:
    """Evidence-based soft budgets after V1SP-003 optimisations."""

    def test_readiness_over_time_is_constant_query_count(self, ctx, db) -> None:
        user = _make_user("trend@kwalitec.example")
        with count_queries() as stmts:
            AnalyticsService.get_readiness_over_time(user.id, weeks=12)
        # leaf topics + progress + missions (3), independent of week count
        assert len(stmts) <= 5

    def test_revision_idle_is_single_query(self, ctx, db) -> None:
        user = _make_user("rev@kwalitec.example")
        subject = Subject(
            user_id=user.id, name="CS1", colour="#336699", active=True
        )
        db.session.add(subject)
        db.session.flush()
        plan = StudyPlan(
            user_id=user.id,
            exam_name="IFoA CS1",
            exam_sitting="April 2027",
            exam_date=date.today() + timedelta(days=120),
            weekday_study_minutes=90,
            weekend_study_minutes=120,
            current_stage="Revision",
            study_preference="Mixed",
            target_grade="Pass",
            preferred_session_minutes=60,
            active=True,
            archived=False,
            revision_entered_at=datetime.utcnow() - timedelta(days=3),
        )
        db.session.add(plan)
        db.session.commit()

        with count_queries() as stmts:
            count = OperationalHealthService._revision_without_sessions_count()
        assert count == 1
        assert len(stmts) == 1

    def test_overall_readiness_batches_leaf_progress(self, ctx, db) -> None:
        user = _make_user("ready@kwalitec.example")
        with count_queries() as stmts:
            ReadinessService.get_overall_readiness(user.id)
        # leaf topics + progress (+ optional mission aggregate) — not 4× leaf scans
        assert len(stmts) <= 4


class TestDashboardDoesNotFetchDeadWidgets:
    def test_dashboard_omits_unused_payloads(self, client, ctx, app) -> None:
        user = _make_user("dash@kwalitec.example")
        _login(client, user.email)
        response = client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        # Core workspace still present
        assert "Student Dashboard" in body or "Learning Workspace" in body
        # Dead widgets must not reappear as template requirements
        assert "decision_journal" not in body
        assert "daily_briefing" not in body


class TestStaticAssetsOptimised:
    def test_first_party_css_js_under_budget(self, app) -> None:
        static_root = Path(app.root_path) / "static"
        assets = measure_static_assets(static_root)
        css_bytes = sum(
            v["bytes"] for k, v in assets.items() if k.startswith("css/")
        )
        js_bytes = sum(
            v["bytes"] for k, v in assets.items() if k.startswith("js/")
        )
        # Post-minify budgets (baseline was ~85KB CSS / ~22KB JS)
        assert css_bytes < 70_000
        assert js_bytes < 22_000

    def test_performance_indexes_declared(self) -> None:
        mission_indexes = {
            idx.name for idx in Mission.__table__.indexes
        }
        assert "ix_missions_status_mission_date" in mission_indexes
        assert "ix_missions_user_date_study_plan" in mission_indexes


class TestEducationalParity:
    def test_review_completion_rate_matches_status_counts(self, ctx, db) -> None:
        user = _make_user("missions@kwalitec.example")
        subject = Subject(
            user_id=user.id, name="CS1", colour="#336699", active=True
        )
        db.session.add(subject)
        db.session.flush()
        for status in ("Completed", "Completed", "Pending", "In Progress"):
            db.session.add(
                Mission(
                    user_id=user.id,
                    subject_id=subject.id,
                    mission_date=date.today(),
                    title=status,
                    status=status,
                )
            )
        db.session.commit()

        rate = ReadinessService.get_review_completion_rate(user.id)
        assert rate["total_missions"] == 4
        assert rate["completed_missions"] == 2
        assert rate["pending"] == 1
        assert rate["in_progress"] == 1
        assert rate["completion_rate"] == 50.0

    def test_negative_sentiment_window_matches_rule(self, ctx, db, app) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        student = _make_user("neg2@kwalitec.example")
        ResearchFeedbackService.submit_checkin(
            student.id,
            experience_rating="Frustrating",
            feature_helped_most="Dashboard",
            friction_area="Nothing",
            confidence_rating="Low",
            return_intent="Probably",
            submission_source=SOURCE_SETTINGS,
        )
        ResearchFeedbackService.submit_checkin(
            student.id,
            experience_rating="Poor",
            feature_helped_most="Dashboard",
            friction_area="Nothing",
            confidence_rating="Low",
            return_intent="Probably",
            submission_source=SOURCE_SETTINGS,
        )
        assert OperationalHealthService._consecutive_negative_sentiment_users() == 1
