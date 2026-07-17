"""Founder Dashboard route, auth, and rendering tests (FOS-004 / FSI-002)."""

from __future__ import annotations

from app.extensions import db
from app.founder.dashboard.access import founder_emails, is_founder_user
from app.founder.dashboard.tests.helpers import make_service
from app.models.user import User


def _make_user(email: str) -> User:
    user = User(email=email, is_active_user=True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user


class TestFounderAccess:
    def test_founder_emails_merge_config(self, app) -> None:
        app.config["FOUNDER_EMAILS"] = "a@x.example, b@x.example"
        with app.app_context():
            emails = founder_emails()
        assert "a@x.example" in emails
        assert "b@x.example" in emails

    def test_is_founder_user_matches_email(self, app, ctx) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        user = _make_user("founder@kwalitec.example")
        assert is_founder_user(user) is True

    def test_is_founder_user_rejects_ordinary(self, app, ctx) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        user = _make_user("student@kwalitec.example")
        assert is_founder_user(user) is False


class TestFounderDashboardAuth:
    def test_anonymous_redirects_to_login(self, client) -> None:
        response = client.get("/founder/")
        assert response.status_code == 302
        assert "/auth/login" in response.headers["Location"]

    def test_ordinary_user_forbidden(self, client, ctx, app) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        _make_user("student@kwalitec.example")
        client.post(
            "/auth/login",
            data={
                "email": "student@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        response = client.get("/founder/")
        assert response.status_code == 403

    def test_founder_user_allowed(self, client, ctx, app) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        _make_user("founder@kwalitec.example")
        client.post(
            "/auth/login",
            data={
                "email": "founder@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        response = client.get("/founder/")
        assert response.status_code == 200


class TestFounderDashboardRoutes:
    def test_blueprint_registered(self, app) -> None:
        assert "founder_dashboard" in app.blueprints

    def test_overview_renders_command_centre(self, client, ctx, app) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        _make_user("founder@kwalitec.example")
        client.post(
            "/auth/login",
            data={
                "email": "founder@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        response = client.get("/founder/")
        assert response.status_code == 200
        html = response.data
        assert b"Founder Command Centre" in html
        assert b"Overview" in html
        assert b"Needs action" in html
        assert b"Operational alerts" in html
        assert b"Recent feedback" in html
        assert b"Programme pulse" in html

    def test_operations_renders_system_sections(
        self, client, ctx, app, monkeypatch
    ) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        _make_user("founder@kwalitec.example")
        client.post(
            "/auth/login",
            data={
                "email": "founder@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        from app.founder.dashboard.services import command_centre_service as ccs

        monkeypatch.setattr(
            ccs, "build_operations_page", lambda: make_service().build_page()
        )
        response = client.get("/founder/operations")
        assert response.status_code == 200
        html = response.data
        assert b"Operations" in html
        assert b"Engineering Health" in html
        assert b"Offline week processing" in html
        assert b"not wired" in html or b"Unavailable" in html

    def test_founder_nav_visible_only_to_founder(self, client, ctx, app) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        _make_user("founder@kwalitec.example")
        _make_user("student@kwalitec.example")

        client.post(
            "/auth/login",
            data={
                "email": "founder@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        founder_home = client.get("/dashboard/")
        assert founder_home.status_code == 200
        assert b'href="/founder' in founder_home.data

        client.post("/auth/logout", follow_redirects=True)
        client.post(
            "/auth/login",
            data={
                "email": "student@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        ordinary_home = client.get("/dashboard/")
        assert ordinary_home.status_code == 200
        assert b'href="/founder' not in ordinary_home.data

    def test_legacy_research_founder_redirects(self, client, ctx, app) -> None:
        app.config["FOUNDER_EMAILS"] = "founder@kwalitec.example"
        _make_user("founder@kwalitec.example")
        client.post(
            "/auth/login",
            data={
                "email": "founder@kwalitec.example",
                "password": "password123",
            },
            follow_redirects=True,
        )
        response = client.get("/research/founder", follow_redirects=False)
        assert response.status_code == 302
        assert "/founder/feedback" in response.headers["Location"]
