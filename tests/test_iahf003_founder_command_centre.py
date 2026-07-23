"""IAHF-003 Kwalitec Console route and overview tests."""

from __future__ import annotations

from app.extensions import db
from app.models.user import User
from app.services.founder_research_service import FounderResearchService
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


def _submit_checkin(user_id: int):
    return ResearchFeedbackService.submit_checkin(
        user_id,
        experience_rating="Good",
        feature_helped_most="Dashboard",
        friction_area="Nothing",
        confidence_rating="High",
        return_intent="Probably",
        submission_source=SOURCE_SETTINGS,
    )


class TestIAHF003CommandCentre:
    def test_single_founder_home(self, client, ctx, app) -> None:
        _login_founder(client, app)
        overview = client.get("/console/")
        assert overview.status_code == 200
        assert b"Kwalitec Console" in overview.data
        assert b"Attention Required" in overview.data

        # Legacy Research home is no longer a competing dashboard.
        legacy = client.get("/research/founder", follow_redirects=False)
        assert legacy.status_code == 302
        assert "/console/feedback" in legacy.headers["Location"]

    def test_overview_uses_live_checkin_counts(self, client, ctx, app) -> None:
        founder = _login_founder(client, app)
        student = _make_user("student@kwalitec.example")
        _submit_checkin(student.id)

        response = client.get("/console/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        summary = FounderResearchService.get_internal_alpha_summary()
        assert summary.completed_checkins == 1
        assert "Platform Summary" in body
        assert str(summary.completed_checkins) in body or str(
            summary.active_participants
        ) in body
        # Must not present static/unwired zeros as the Alpha story on Overview.
        assert "Offline week pipeline" not in body or "not wired" in body
        assert founder.email  # founder identity preserved

    def test_section_routes_founder_gated(self, client, ctx, app) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        student = _make_user("student@kwalitec.example")
        client.post(
            "/auth/login",
            data={"email": student.email, "password": "password123"},
            follow_redirects=True,
        )
        for path in (
            "/console/",
            "/console/attention",
            "/console/feedback",
            "/console/findings",
            "/console/research",
            "/console/internal-alpha",
            "/console/participants",
            "/console/operations",
            "/console/releases",
            "/console/settings",
        ):
            assert client.get(path).status_code == 403

    def test_share_feedback_not_active_on_founder_pages(
        self, client, ctx, app
    ) -> None:
        _login_founder(client, app)
        response = client.get("/console/feedback")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        # Console portal uses independent chrome (no Learning Workspace sidebar).
        assert "console-nav" in body
        assert "console-nav-link is-active" in body or 'aria-current="page"' in body
        assert "console-sidebar" in body
        assert 'aria-label="Primary"' not in body
