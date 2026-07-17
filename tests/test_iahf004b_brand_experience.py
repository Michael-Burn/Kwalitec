"""IAHF-004B — brand experience & application shell regression checks."""

from __future__ import annotations

from pathlib import Path

from app.brand_identity import (
    FOUNDER_COMMAND_CENTRE_LABEL,
    FOUNDING_COHORT_LABEL,
    INTERNAL_ALPHA_BUILD_LABEL,
    INTERNAL_ALPHA_LABEL,
    LEARNING_WORKSPACE_LABEL,
    STUDENT_DASHBOARD_LABEL,
)
from app.extensions import db
from app.models.user import User
from app.version import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]


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


class TestBrandIdentityConstants:
    def test_internal_alpha_programme_labels(self) -> None:
        assert INTERNAL_ALPHA_LABEL == "Internal Alpha"
        assert FOUNDING_COHORT_LABEL == "Founding Cohort"
        assert INTERNAL_ALPHA_BUILD_LABEL == "RC2"

    def test_official_product_area_names(self) -> None:
        assert FOUNDER_COMMAND_CENTRE_LABEL == "Founder Command Centre"
        assert LEARNING_WORKSPACE_LABEL == "Learning Workspace"
        assert STUDENT_DASHBOARD_LABEL == "Student Dashboard"


class TestShellTemplateWiring:
    def test_layouts_include_shared_footer(self) -> None:
        for relative in (
            "app/templates/layouts/base.html",
            "app/templates/layouts/auth_base.html",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            assert "partials/app_footer.html" in text

    def test_sidebar_includes_alpha_badge(self) -> None:
        text = (ROOT / "app/templates/partials/sidebar.html").read_text(
            encoding="utf-8"
        )
        assert "partials/internal_alpha_badge.html" in text
        assert "partials/brand_logo.html" in text

    def test_topnav_includes_alpha_badge(self) -> None:
        text = (ROOT / "app/templates/partials/topnav.html").read_text(
            encoding="utf-8"
        )
        assert "partials/internal_alpha_badge.html" in text
        assert "topnav-end" in text

    def test_login_includes_alpha_identity(self) -> None:
        text = (ROOT / "app/templates/auth/login.html").read_text(encoding="utf-8")
        assert "landing-alpha-identity" in text
        assert "partials/internal_alpha_badge.html" in text

    def test_user_facing_founder_templates_avoid_legacy_names(self) -> None:
        forbidden = (
            "Founder Dashboard",
            "Founder Home",
            "Founder Portal",
            "Founder Operating System",
            "Research Command Centre",
        )
        paths = [
            ROOT / "app/founder/dashboard/templates/founder_dashboard",
            ROOT / "app/templates/research",
        ]
        for base in paths:
            for path in base.rglob("*.html"):
                text = path.read_text(encoding="utf-8")
                for phrase in forbidden:
                    assert phrase not in text, f"{phrase!r} still in {path}"


class TestBrandExperienceHttp:
    def test_login_shows_alpha_identity_and_canonical_logo(self, client) -> None:
        resp = client.get("/auth/login")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert INTERNAL_ALPHA_LABEL in html
        assert FOUNDING_COHORT_LABEL in html
        assert INTERNAL_ALPHA_BUILD_LABEL in html
        assert "branding/logo-icon.svg" in html
        assert f"Kwalitec v{APP_VERSION}" in html
        assert "alpha-identity" in html

    def test_authenticated_shell_shows_alpha_identity(self, logged_in_client) -> None:
        resp = logged_in_client.get("/dashboard/")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "alpha-identity" in html
        assert INTERNAL_ALPHA_LABEL in html
        assert FOUNDING_COHORT_LABEL in html
        assert f"Build {INTERNAL_ALPHA_BUILD_LABEL}" in html
        assert STUDENT_DASHBOARD_LABEL in html
        assert LEARNING_WORKSPACE_LABEL in html
        assert "branding/logo-icon.svg" in html
        assert "sidebar-brand-mark" in html

    def test_settings_and_checkin_keep_shell_identity(self, logged_in_client) -> None:
        for path in ("/settings/", "/research/checkin"):
            resp = logged_in_client.get(path)
            assert resp.status_code == 200, path
            html = resp.get_data(as_text=True)
            assert INTERNAL_ALPHA_LABEL in html
            assert f"Kwalitec v{APP_VERSION}" in html

    def test_study_plan_uses_section_header_pattern(self, logged_in_client) -> None:
        resp = logged_in_client.get("/study-plan/plans/all")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert LEARNING_WORKSPACE_LABEL in html
        assert "section-title" in html
        assert "display-6" not in html


class TestFounderCommandCentreNaming:
    def test_overview_uses_official_name(self, client, ctx, app) -> None:
        _login_founder(client, app)
        resp = client.get("/founder/")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert FOUNDER_COMMAND_CENTRE_LABEL in html
        assert "Founder Dashboard" not in html
        assert "Founder Operating System" not in html
        assert INTERNAL_ALPHA_LABEL in html
