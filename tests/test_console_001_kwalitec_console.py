"""CONSOLE-001 — Kwalitec Console portal presentation tests."""

from __future__ import annotations

from app.brand_identity import (
    CONSOLE_HOME_LABEL,
    FOUNDER_COMMAND_CENTRE_LABEL,
    KWALITEC_CONSOLE_LABEL,
)
from app.extensions import db
from app.founder.dashboard.nav import COMMAND_CENTRE_NAV, active_section_id
from app.models.user import User
from app.services.research_feedback_service import (
    SOURCE_SETTINGS,
    ResearchFeedbackService,
)


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


def _login_student(client, app) -> User:
    app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
    student = _make_user("student@kwalitec.example")
    client.post(
        "/auth/login",
        data={"email": student.email, "password": "password123"},
        follow_redirects=True,
    )
    return student


class TestConsoleTerminology:
    def test_brand_labels(self) -> None:
        assert KWALITEC_CONSOLE_LABEL == "Kwalitec Console"
        assert CONSOLE_HOME_LABEL == "Console Home"
        assert FOUNDER_COMMAND_CENTRE_LABEL == KWALITEC_CONSOLE_LABEL


class TestConsoleNavigation:
    def test_primary_nav_structure(self) -> None:
        labels = [item.label for item in COMMAND_CENTRE_NAV]
        assert labels == [
            "Overview",
            "Operations",
            "Students",
            "Learning",
            "Assessments",
            "Content",
            "Analytics",
            "Platform",
            "Settings",
            "Support",
        ]

    def test_section_mapping(self) -> None:
        assert active_section_id("founder_dashboard.index") == "overview"
        assert active_section_id("founder_dashboard.feedback") == "support"
        assert active_section_id("founder_dashboard.alpha_observability") == (
            "platform"
        )
        assert active_section_id("curriculum_studio.index") == "content"
        assert active_section_id("founder_dashboard.attention") == "operations"


class TestConsoleRouting:
    def test_console_home_renders(self, client, ctx, app) -> None:
        _login_founder(client, app)
        response = client.get("/console/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Console Home" in body
        assert "Kwalitec Console" in body
        assert "Attention Required" in body
        assert "Platform Summary" in body
        assert "Quick Actions" in body
        assert "console-sidebar" in body
        assert "console-search" in body
        assert 'aria-label="Console primary"' in body

    def test_legacy_founder_redirects_to_console(self, client, ctx, app) -> None:
        _login_founder(client, app)
        response = client.get("/founder/", follow_redirects=False)
        assert response.status_code == 308
        assert "/console/" in response.headers["Location"]

    def test_console_gated_for_non_founders(self, client, ctx, app) -> None:
        _login_student(client, app)
        assert client.get("/console/").status_code == 403
        assert client.get("/console/search").status_code == 403

    def test_platform_intelligence_page(self, client, ctx, app) -> None:
        _login_founder(client, app)
        response = client.get("/console/alpha-observability")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Platform Intelligence" in body
        assert "console-sidebar" in body

    def test_attention_center_page(self, client, ctx, app) -> None:
        _login_founder(client, app)
        response = client.get("/console/attention")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Attention Center" in body

    def test_console_search(self, client, ctx, app) -> None:
        founder = _login_founder(client, app)
        student = _make_user("learner@kwalitec.example")
        ResearchFeedbackService.submit_checkin(
            student.id,
            experience_rating="Good",
            feature_helped_most="Dashboard",
            friction_area="Nothing",
            confidence_rating="High",
            return_intent="Probably",
            submission_source=SOURCE_SETTINGS,
        )
        response = client.get("/console/search?q=learner")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Console Search" in body
        assert "learner@kwalitec.example" in body
        assert founder.email


class TestPortalSeparation:
    def test_learning_workspace_has_no_console_nav(
        self, client, ctx, app
    ) -> None:
        _login_founder(client, app)
        response = client.get("/dashboard/", follow_redirects=True)
        body = response.get_data(as_text=True)
        assert "console-sidebar" not in body
        assert ">Founder<" not in body

    def test_student_portal_has_no_console_chrome(
        self, client, ctx, app
    ) -> None:
        _login_student(client, app)
        # Student home may 404 if experience wiring differs; hit login-gated path.
        response = client.get("/student/")
        if response.status_code == 404:
            response = client.get("/dashboard/")
        body = response.get_data(as_text=True)
        assert "console-sidebar" not in body
        assert "Attention Required" not in body

    def test_console_has_no_student_nav_labels(self, client, ctx, app) -> None:
        _login_founder(client, app)
        body = client.get("/console/").get_data(as_text=True)
        assert "Study Plan" not in body
        assert 'aria-label="Primary"' not in body  # learning workspace sidebar
        assert "console-nav" in body


class TestConsoleAccessibility:
    def test_landmarks_and_skip_link(self, client, ctx, app) -> None:
        _login_founder(client, app)
        body = client.get("/console/").get_data(as_text=True)
        assert "console-skip-link" in body
        assert 'role="main"' in body
        assert 'role="banner"' in body
        assert 'role="contentinfo"' in body
        assert 'aria-current="page"' in body
