"""PB-001 — Private Beta Validation evidence infrastructure tests."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from app.extensions import db
from app.models.alpha_infrastructure import PresentationEvent
from app.models.private_beta import PrivateBetaFeedback, PrivateBetaParticipant
from app.models.user import User
from app.services.presentation_telemetry_service import (
    ALLOWED_EVENTS,
    EVENT_KNOWLEDGE_MAP_OPENED,
    EVENT_TUTOR_OPENED,
)
from app.services.private_beta.classification import (
    classify_feedback_severity,
    parse_user_agent,
)
from app.services.private_beta.feedback_service import PrivateBetaFeedbackService
from app.services.private_beta.first_session_service import FirstSessionStudyService
from app.services.private_beta.metrics_service import PrivateBetaMetricsService
from app.services.private_beta.observation_service import PrivateBetaObservationService
from app.services.private_beta.participant_service import PrivateBetaParticipantService
from app.services.private_beta.report_emitter import PrivateBetaReportEmitter


def _make_user(email: str = "beta@kwalitec.example") -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    user.alpha_onboarding_completed = True
    db.session.add(user)
    db.session.commit()
    return user


def _login(client, email: str = "beta@kwalitec.example") -> None:
    client.post(
        "/auth/login",
        data={"email": email, "password": "password123"},
        follow_redirects=False,
    )


def _login_founder(client, app) -> User:
    app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
    founder = _make_user("founder@kwalitec.example")
    client.post(
        "/auth/login",
        data={"email": founder.email, "password": "password123"},
        follow_redirects=True,
    )
    return founder


class TestClassification:
    def test_critical_from_data_loss_message(self):
        assert (
            classify_feedback_severity(
                category="bug", message="I had data loss after refresh"
            )
            == "critical"
        )

    def test_enhancement_for_suggestion(self):
        assert (
            classify_feedback_severity(
                category="suggestion", message="Add dark mode please"
            )
            == "enhancement"
        )

    def test_incorrect_recommendation_is_major(self):
        assert (
            classify_feedback_severity(
                category="incorrect_recommendation",
                message="This topic is already mastered",
            )
            == "major"
        )

    def test_parse_user_agent(self):
        browser, device = parse_user_agent(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/17.0 Mobile/15E148 Safari/604.1"
        )
        assert browser == "Safari"
        assert device == "mobile"


class TestFeedbackService:
    def test_submit_stores_category_and_severity(self, ctx):
        user = _make_user()
        result = PrivateBetaFeedbackService.submit(
            user_id=user.id,
            category="bug",
            message="The session crashed when I clicked Start",
            current_screen="Study Session",
            subject_code="CS1",
            browser="Chrome",
            device="desktop",
            path="/session/1",
        )
        assert result.ok
        assert result.severity == "critical"
        row = db.session.get(PrivateBetaFeedback, result.feedback_id)
        assert row is not None
        assert row.category == "bug"
        assert row.subject_code == "CS1"


class TestParticipantAndObservation:
    def test_enrol_and_observe(self, ctx):
        user = _make_user()
        enrol = PrivateBetaParticipantService.enrol(
            user_id=user.id, device_preference="laptop"
        )
        assert enrol.ok
        assert PrivateBetaParticipantService.count_active() == 1

        obs = PrivateBetaObservationService.record(
            user_id=user.id,
            understood_todays_mission=True,
            knew_where_to_click=True,
            became_stuck=True,
            stuck_where="Tutor",
        )
        assert obs.ok
        rows = PrivateBetaObservationService.for_user(user.id)
        assert len(rows) == 1
        assert rows[0].stuck_where == "Tutor"


class TestFirstSessionAndMetrics:
    def test_empty_cohort_recommends_extension(self, ctx):
        snap = PrivateBetaMetricsService().build()
        assert snap.total_beta_users == 0
        assert snap.go_recommendation == "PRIVATE BETA EXTENSION REQUIRED"
        assert snap.gates_passed is False

    def test_first_session_timing_after_enrol(self, ctx):
        user = _make_user()
        PrivateBetaParticipantService.enrol(user_id=user.id)
        participant = PrivateBetaParticipant.query.filter_by(user_id=user.id).first()
        assert participant is not None
        participant.enrolled_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(
            minutes=30
        )
        db.session.add(
            PresentationEvent(
                user_id=user.id,
                event_type=EVENT_TUTOR_OPENED,
                path="/student/tutor",
                created_at=(
                    datetime.now(UTC).replace(tzinfo=None) - timedelta(minutes=10)
                ),
            )
        )
        db.session.commit()

        timing = FirstSessionStudyService().for_user(user.id)
        assert timing is not None
        assert timing.reached_tutor is True
        assert timing.minutes_to_first_tutor is not None
        assert timing.drop_off_location == "after_tutor"


class TestTelemetryAllowlist:
    def test_tutor_and_knowledge_map_events_allowed(self):
        assert EVENT_TUTOR_OPENED in ALLOWED_EVENTS
        assert EVENT_KNOWLEDGE_MAP_OPENED in ALLOWED_EVENTS


class TestStudentFeedbackRoute:
    def test_beta_feedback_form_submits(self, client, ctx):
        _make_user()
        _login(client)
        response = client.post(
            "/alpha/feedback/beta",
            data={
                "category": "confusing_screen",
                "message": "I do not understand Today's Mission",
                "current_screen": "Home",
                "browser": "Firefox",
                "device": "desktop",
                "path": "/student/",
            },
            follow_redirects=False,
        )
        assert response.status_code in {302, 200}
        rows = PrivateBetaFeedback.query.all()
        assert len(rows) == 1
        assert rows[0].category == "confusing_screen"
        assert rows[0].severity == "question"


class TestFounderBetaDashboard:
    def test_beta_dashboard_renders(self, client, ctx, app):
        _login_founder(client, app)
        response = client.get("/console/beta")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Private Beta" in body
        assert "Quality gates" in body
        assert "PRIVATE BETA EXTENSION REQUIRED" in body

    def test_enrol_from_dashboard(self, client, ctx, app):
        _login_founder(client, app)
        student = _make_user("cohort@kwalitec.example")
        response = client.post(
            "/console/beta/enrol",
            data={"email": student.email, "device_preference": "mobile"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert PrivateBetaParticipant.query.filter_by(user_id=student.id).first()


class TestReportEmitter:
    def test_writes_markdown_report(self, ctx, tmp_path: Path):
        target = tmp_path / "PB001_PRIVATE_BETA_REPORT.md"
        path = PrivateBetaReportEmitter().write(target)
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "PB-001 — Private Beta Validation Report" in text
        assert "FINAL DECISION" in text
        assert "PRIVATE BETA EXTENSION REQUIRED" in text
        assert "Go / No-Go recommendation" in text
