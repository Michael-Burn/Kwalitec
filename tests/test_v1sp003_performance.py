"""V1SP-003 — Performance optimisation regression and budget tests."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from app.extensions import db
from app.founder.dashboard.services.operational_health_service import (
    OperationalHealthService,
)
from app.models.curriculum import Curriculum, Topic
from app.models.mission import Mission
from app.models.study_plan import StudyPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
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
    user.alpha_onboarding_completed = True
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
        """Guard the V1SP-003 batched readiness path (not User/RBAC refresh).

        Seeds active leaf topics + progress with no curriculum-bound plan so
        ``_leaf_topics_for_user`` uses the global ``_get_leaf_topics`` batch
        (one topics scan). Captures ``uid`` before the counter so
        expire-on-commit User reload + RBAC ``selectin`` loads are excluded.
        Expected statements: study_plans + topics + topic_progress + mission
        status aggregate — not 4× leaf rescans.
        """
        user = _make_user("ready@kwalitec.example")
        curriculum = Curriculum(
            exam_name="IFoA CS1 Perf Budget", version="2026", active=True
        )
        db.session.add(curriculum)
        db.session.flush()
        topics: list[Topic] = []
        for index in range(1, 4):
            topic = Topic(
                curriculum_id=curriculum.id,
                name=f"Leaf {index}",
                order=index,
                recommended_minutes=45,
                active=True,
            )
            db.session.add(topic)
            topics.append(topic)
        db.session.flush()
        for topic in topics[:2]:
            db.session.add(
                TopicProgress(
                    user_id=user.id,
                    topic_id=topic.id,
                    confidence="Medium",
                    completed=True,
                    mastery_score=50.0,
                )
            )
        db.session.commit()

        # Capture PK before counting — accessing user.id after commit would
        # refresh User and selectin-load roles/capabilities inside the budget.
        uid = user.id
        with count_queries() as stmts:
            ReadinessService.get_overall_readiness(uid)
        # plan lookup + topics + progress + mission status aggregate
        assert len(stmts) == 4


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
        # First-party top-level budgets as of 2026-08-24 (inventory ~123032 CSS /
        # ~40016 JS under css/*.css and js/*.js). Nested static dirs (student/,
        # session/, wizard/, assessment/, …) are NOT included in this
        # measurement. Raised deliberately for DX-004→REL-001 design-system
        # growth — not silently loosened to force green. V1SP-003 post-minify
        # baseline was ~63514 CSS / ~20592 JS with ceilings 70000 / 22000.
        assert css_bytes < 135_000
        assert js_bytes < 45_000

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
