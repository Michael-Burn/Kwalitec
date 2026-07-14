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

    def test_founder_user_allowed(self, client, ctx, app, monkeypatch) -> None:
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
        monkeypatch.setattr(
            "app.founder.dashboard.routes._service",
            lambda: make_service(),
        )
        response = client.get("/founder/")
        assert response.status_code == 200


class TestFounderDashboardRoutes:
    def test_blueprint_registered(self, app) -> None:
        assert "founder_dashboard" in app.blueprints

    def test_dashboard_renders_sections(self, client, ctx, app, monkeypatch) -> None:
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
        monkeypatch.setattr(
            "app.founder.dashboard.routes._service",
            lambda: make_service(),
        )
        response = client.get("/founder/")
        assert response.status_code == 200
        html = response.data
        assert b"Founder Operating System" in html
        assert b"Engineering Health" in html
        assert b"Internal Alpha" in html
        assert b"2026-W28" in html
        assert b"Capability Archive" in html
        assert b"FOS-003" in html
        assert b"Engineering Standards" in html
        assert b"Indexed Artefacts" in html
        assert b"Version 1.0" in html

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
