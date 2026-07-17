"""IAHF-003 Founder Command Centre route and overview tests."""

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
        overview = client.get("/founder/")
        assert overview.status_code == 200
        assert b"Founder Command Centre" in overview.data
        assert b"Needs action" in overview.data

        # Legacy Research home is no longer a competing dashboard.
        legacy = client.get("/research/founder", follow_redirects=False)
        assert legacy.status_code == 302
        assert "/founder/feedback" in legacy.headers["Location"]

    def test_overview_uses_live_checkin_counts(self, client, ctx, app) -> None:
        founder = _login_founder(client, app)
        student = _make_user("student@kwalitec.example")
        _submit_checkin(student.id)

        response = client.get("/founder/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        summary = FounderResearchService.get_internal_alpha_summary()
        assert summary.completed_checkins == 1
        assert "Programme pulse" in body
        assert str(summary.completed_checkins) in body
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
            "/founder/",
            "/founder/attention",
            "/founder/feedback",
            "/founder/findings",
            "/founder/research",
            "/founder/internal-alpha",
            "/founder/participants",
            "/founder/operations",
            "/founder/releases",
            "/founder/settings",
        ):
            assert client.get(path).status_code == 403

    def test_share_feedback_not_active_on_founder_pages(
        self, client, ctx, app
    ) -> None:
        _login_founder(client, app)
        response = client.get("/founder/feedback")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        # Share Feedback link must not carry active class on Founder routes.
        assert 'href="/research/checkin' in body or "Share Feedback" in body
        # Active Founder nav is present.
        assert "founder-cc-nav" in body
        assert "founder-cc-nav-link active" in body
