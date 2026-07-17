"""V1SP-001C — Founder Operational Health Dashboard tests."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from app.extensions import db
from app.founder.dashboard.services.operational_health_service import (
    OperationalHealthService,
)
from app.models.mission import Mission
from app.models.study_plan import StudyPlan
from app.models.subject import Subject
from app.models.user import User
from app.services.research_feedback_service import (
    SOURCE_SETTINGS,
    ResearchFeedbackService,
)
from app.services.vision_journal_service import VisionJournalService


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


def _login_founder(client, app) -> User:
    app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
    founder = _make_user("founder@kwalitec.example")
    client.post(
        "/auth/login",
        data={"email": founder.email, "password": "password123"},
        follow_redirects=True,
    )
    return founder


def _make_subject(user_id: int) -> Subject:
    subject = Subject(
        user_id=user_id, name="CS1", colour="#336699", active=True
    )
    db.session.add(subject)
    db.session.commit()
    return subject


def _make_plan(
    user_id: int,
    *,
    active: bool = True,
    revision_entered_at: datetime | None = None,
) -> StudyPlan:
    plan = StudyPlan(
        user_id=user_id,
        exam_name="IFoA CS1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=120),
        weekday_study_minutes=90,
        weekend_study_minutes=120,
        current_stage="Chapter 1",
        study_preference="Mixed",
        target_grade="Pass",
        preferred_session_minutes=60,
        active=active,
        archived=False,
        revision_entered_at=revision_entered_at,
    )
    db.session.add(plan)
    db.session.commit()
    return plan


def _complete_mission(
    user_id: int,
    subject_id: int,
    plan_id: int,
    mission_date: date,
) -> Mission:
    mission = Mission(
        user_id=user_id,
        subject_id=subject_id,
        study_plan_id=plan_id,
        mission_date=mission_date,
        title="Study Session",
        status="Completed",
    )
    db.session.add(mission)
    db.session.commit()
    return mission


def _submit_checkin(
    user_id: int,
    *,
    experience: str = "Good",
    classification: str | None = None,
    free_text: str | None = None,
):
    return ResearchFeedbackService.submit_checkin(
        user_id,
        experience_rating=experience,
        feature_helped_most="Dashboard",
        friction_area="Nothing",
        confidence_rating="High",
        return_intent="Probably",
        submission_source=SOURCE_SETTINGS,
        free_text=free_text,
        classification=classification,
    )


class TestOperationalHealthPermissions:
    def test_founder_can_open_page(self, client, ctx, app) -> None:
        _login_founder(client, app)
        response = client.get("/founder/operational-health")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Operational Health" in body
        assert "Needs Attention" in body
        assert "Healthy Activity" in body
        assert "Trends" in body

    def test_student_forbidden(self, client, ctx, app) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        student = _make_user("student@kwalitec.example")
        client.post(
            "/auth/login",
            data={"email": student.email, "password": "password123"},
            follow_redirects=True,
        )
        assert client.get("/founder/operational-health").status_code == 403

    def test_nav_includes_operational_health(self, client, ctx, app) -> None:
        _login_founder(client, app)
        body = client.get("/founder/").get_data(as_text=True)
        assert "Operational Health" in body
        assert 'href="/founder/operational-health"' in body or \
            "/founder/operational-health" in body


class TestNeedsAttentionRules:
    def test_plan_never_started(self, client, ctx, app) -> None:
        _login_founder(client, app)
        student = _make_user("idle@kwalitec.example")
        _make_plan(student.id)

        with app.test_request_context():
            page = OperationalHealthService().build_page(on_date=date.today())

        rule_ids = {card.rule_id for card in page.needs_attention}
        assert "plan_never_started" in rule_ids
        card = next(
            c for c in page.needs_attention if c.rule_id == "plan_never_started"
        )
        assert card.count == 1
        assert "/founder/participants" in card.href

    def test_inactive_and_prolonged(self, client, ctx, app) -> None:
        _login_founder(client, app)
        today = date.today()
        student = _make_user("away@kwalitec.example")
        subject = _make_subject(student.id)
        plan = _make_plan(student.id)
        _complete_mission(
            student.id, subject.id, plan.id, today - timedelta(days=16)
        )

        with app.test_request_context():
            page = OperationalHealthService().build_page(on_date=today)

        by_id = {c.rule_id: c for c in page.needs_attention}
        assert by_id["no_study_activity_7d"].count == 1
        assert by_id["prolonged_inactivity"].count == 1

    def test_revision_without_sessions(self, client, ctx, app) -> None:
        _login_founder(client, app)
        student = _make_user("revision@kwalitec.example")
        _make_plan(
            student.id,
            revision_entered_at=datetime.utcnow() - timedelta(days=3),
        )

        with app.test_request_context():
            page = OperationalHealthService().build_page(on_date=date.today())

        by_id = {c.rule_id: c for c in page.needs_attention}
        assert "revision_no_sessions" in by_id
        assert by_id["revision_no_sessions"].count == 1

    def test_help_seeking_and_triage(self, client, ctx, app) -> None:
        _login_founder(client, app)
        a = _make_user("a@kwalitec.example")
        b = _make_user("b@kwalitec.example")
        _submit_checkin(
            a.id, classification="Bug", free_text="Broken filter"
        )
        _submit_checkin(
            b.id, classification="Question", free_text="How do I revise?"
        )

        with app.test_request_context():
            page = OperationalHealthService().build_page(on_date=date.today())

        by_id = {c.rule_id: c for c in page.needs_attention}
        assert by_id["help_seeking_checkins"].count == 2
        assert "Review Feedback" in by_id["help_seeking_checkins"].primary_action_label
        assert by_id["feedback_awaiting_triage"].count >= 2
        assert by_id["alpha_awaiting_review"].count >= 2

    def test_consecutive_negative_sentiment(self, client, ctx, app) -> None:
        _login_founder(client, app)
        student = _make_user("neg@kwalitec.example")
        _submit_checkin(student.id, experience="Frustrating")
        _submit_checkin(student.id, experience="Poor")

        with app.test_request_context():
            page = OperationalHealthService().build_page(on_date=date.today())

        by_id = {c.rule_id: c for c in page.needs_attention}
        assert by_id["consecutive_negative_sentiment"].count == 1

    def test_repeated_feedback(self, client, ctx, app) -> None:
        _login_founder(client, app)
        student = _make_user("repeat@kwalitec.example")
        for _ in range(3):
            _submit_checkin(student.id)

        with app.test_request_context():
            page = OperationalHealthService().build_page(on_date=date.today())

        by_id = {c.rule_id: c for c in page.needs_attention}
        assert by_id["repeated_feedback"].count == 1

    def test_promoted_vision_not_researched(self, client, ctx, app) -> None:
        founder = _login_founder(client, app)
        entry = VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Twin Ops View",
            description="Aggregate twin health.",
            reason="Founder needs observability.",
            potential_value="high",
            expected_impact="Faster decisions.",
            target_version="version_2",
            category="Founder Experience",
            tags=["Ops"],
        )
        VisionJournalService.promote_to_development(
            entry.id,
            promoted_by_user_id=founder.id,
            placeholder_ref="ARCH-FUTURE-001",
            notes="Placeholder only",
        )

        with app.test_request_context():
            page = OperationalHealthService().build_page(on_date=date.today())

        by_id = {c.rule_id: c for c in page.needs_attention}
        assert by_id["vision_promoted_not_researched"].count == 1
        assert "/founder/vision" in by_id["vision_promoted_not_researched"].href

    def test_promoted_after_research_not_flagged(self, client, ctx, app) -> None:
        founder = _login_founder(client, app)
        entry = VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Researched Idea",
            description="Already researched.",
            reason="Validated path.",
            potential_value="medium",
            expected_impact="Clearer ops.",
            target_version="version_1_x",
            category="Operations",
            tags=["Research"],
        )
        VisionJournalService.update_entry(
            entry.id,
            changed_by_user_id=founder.id,
            title=entry.title,
            description=entry.description,
            reason=entry.reason,
            potential_value=entry.potential_value,
            expected_impact=entry.expected_impact,
            target_version=entry.target_version,
            category=entry.category,
            tags=entry.tags,
            status="research",
        )
        VisionJournalService.promote_to_development(
            entry.id,
            promoted_by_user_id=founder.id,
            placeholder_ref="ARCH-OK-001",
        )

        with app.test_request_context():
            page = OperationalHealthService().build_page(on_date=date.today())

        by_id = {c.rule_id: c for c in page.needs_attention}
        assert "vision_promoted_not_researched" not in by_id


class TestHealthyActivityAndTrends:
    def test_healthy_activity_counts(self, client, ctx, app) -> None:
        _login_founder(client, app)
        today = date.today()
        student = _make_user("active@kwalitec.example")
        subject = _make_subject(student.id)
        plan = _make_plan(
            student.id,
            revision_entered_at=datetime.combine(today, datetime.min.time()),
        )
        _complete_mission(student.id, subject.id, plan.id, today)
        _submit_checkin(student.id)
        founder = User.query.filter_by(email="founder@kwalitec.example").one()
        VisionJournalService.create_entry(
            author_user_id=founder.id,
            title="Founder idea",
            description="Desc",
            reason="Why",
            potential_value="medium",
            expected_impact="Impact",
            target_version="version_1_x",
            category="Operations",
            tags=["health"],
        )

        with app.test_request_context():
            page = OperationalHealthService().build_page(on_date=today)

        by_id = {m.metric_id: m for m in page.healthy_activity}
        assert by_id["active_learners_today"].value == 1
        assert by_id["study_sessions_week"].value == 1
        assert by_id["revision_sessions_week"].value == 1
        assert by_id["alpha_feedback_week"].value >= 1
        assert by_id["vision_entries_week"].value >= 1
        assert by_id["plans_completed_week"].value == 1

    def test_trends_have_seven_days_and_summaries(self, client, ctx, app) -> None:
        _login_founder(client, app)
        today = date.today()
        student = _make_user("trend@kwalitec.example")
        subject = _make_subject(student.id)
        plan = _make_plan(student.id)
        _complete_mission(student.id, subject.id, plan.id, today)
        _complete_mission(
            student.id, subject.id, plan.id, today - timedelta(days=2)
        )
        _submit_checkin(student.id)

        with app.test_request_context():
            page = OperationalHealthService().build_page(on_date=today)

        assert len(page.trends) == 6
        study = next(
            t for t in page.trends if t.series_id == "daily_study_sessions"
        )
        assert len(study.values) == 7
        assert len(study.labels) == 7
        assert study.values[-1] == 1
        assert "7 days" in study.summary
        assert sum(study.values) == 2

    def test_page_renders_empty_attention_honestly(self, client, ctx, app) -> None:
        _login_founder(client, app)
        response = client.get("/founder/operational-health")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Nothing needs attention right now." in body
        assert 'data-oh-trend="daily_study_sessions"' in body
        assert "role=\"img\"" in body or "role='img'" in body


class TestRegression:
    def test_overview_still_loads_and_links_health(self, client, ctx, app) -> None:
        _login_founder(client, app)
        response = client.get("/founder/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Founder Command Centre" in body
        assert "Needs action" in body
        assert "/founder/operational-health" in body

    def test_operations_route_still_available(self, client, ctx, app) -> None:
        _login_founder(client, app)
        # FOS Operations remains reachable (secondary destination).
        # May be unavailable in TESTING for Operational State — still 200.
        response = client.get("/founder/operations")
        assert response.status_code == 200
