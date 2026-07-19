"""V1SP-001B — High-priority operational fix regression tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BRANDING = ROOT / "app" / "static" / "branding"
SIDEBAR = ROOT / "app" / "templates" / "partials" / "sidebar.html"


class TestOpenRedirectProtection:
    """H-1 — harden ``_safe_next_url`` against bypasses."""

    def test_relative_path_allowed(self, app) -> None:
        from app.auth.routes import _safe_next_url

        with app.test_request_context("/auth/login?next=/dashboard/"):
            assert _safe_next_url() == "/dashboard/"

    def test_relative_path_with_query_allowed(self, app) -> None:
        from app.auth.routes import _safe_next_url

        with app.test_request_context(
            "/auth/login?next=/founder/feedback%3Fstatus=new"
        ):
            assert _safe_next_url() == "/founder/feedback?status=new"

    @pytest.mark.parametrize(
        "next_value",
        [
            "https://evil.com",
            "http://evil.com/phish",
            "//evil.com",
            "///evil.com",
            "/\\evil.com",
            "\\\\evil.com",
            "/%2f%2fevil.com",
            "/%2F%2Fevil.com",
            "javascript:alert(1)",
            "dashboard",
        ],
    )
    def test_malicious_next_rejected(self, app, next_value: str) -> None:
        from app.auth.routes import _safe_next_url

        # Pass the value as Flask would see it after one query decode.
        with app.test_request_context("/auth/login", query_string={"next": next_value}):
            assert _safe_next_url() is None

    def test_empty_next_rejected(self, app) -> None:
        from app.auth.routes import _safe_next_url

        with app.test_request_context("/auth/login?next="):
            assert _safe_next_url() is None


class TestProductionCookieSecurity:
    """H-2 — production session / remember-me cookie flags."""

    def test_production_config_sets_secure_cookies(self) -> None:
        from app.config import ProductionConfig

        config = ProductionConfig()
        assert config.SESSION_COOKIE_SECURE is True
        assert config.SESSION_COOKIE_HTTPONLY is True
        assert config.SESSION_COOKIE_SAMESITE == "Lax"
        assert config.REMEMBER_COOKIE_SECURE is True
        assert config.REMEMBER_COOKIE_HTTPONLY is True
        assert config.REMEMBER_COOKIE_SAMESITE == "Lax"
        assert config.SEND_FILE_MAX_AGE_DEFAULT == 31_536_000


class TestSecretKeyProductionGate:
    """H-3 — reject insecure secrets whenever ProductionConfig is active."""

    def test_production_config_rejects_default_secret(self) -> None:
        from app import _validate_env_vars
        from app.config import ProductionConfig

        old = os.environ.get("SECRET_KEY")
        os.environ["SECRET_KEY"] = "dev-change-this-secret-key"
        try:
            with pytest.raises(RuntimeError, match="SECRET_KEY"):
                _validate_env_vars(ProductionConfig)
        finally:
            if old is None:
                os.environ.pop("SECRET_KEY", None)
            else:
                os.environ["SECRET_KEY"] = old

    def test_development_config_warns_but_allows_default(self) -> None:
        from app import _validate_env_vars
        from app.config import DevelopmentConfig

        old = os.environ.get("SECRET_KEY")
        os.environ["SECRET_KEY"] = "dev-change-this-secret-key"
        try:
            _validate_env_vars(DevelopmentConfig)
        finally:
            if old is None:
                os.environ.pop("SECRET_KEY", None)
            else:
                os.environ["SECRET_KEY"] = old


class TestSidebarActiveState:
    """H-4 — student Dashboard must not activate on Founder routes."""

    def test_sidebar_uses_dashboard_prefix_match(self) -> None:
        text = SIDEBAR.read_text(encoding="utf-8")
        assert "request.endpoint.startswith('dashboard.')" in text
        assert "'dashboard' in request.endpoint" not in text

    def test_founder_page_does_not_mark_student_dashboard_active(
        self, client, ctx, app
    ) -> None:
        from tests.test_iahf003_founder_command_centre import _login_founder

        _login_founder(client, app)
        response = client.get("/founder/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        # Founder Command Centre chrome is active.
        assert "founder-cc-nav-link active" in body
        # Student Dashboard link must not carry active while on Founder Overview.
        assert 'href="/dashboard/"' in body or "Dashboard" in body
        # The Dashboard nav-link should not be the active one beside Founder.
        import re

        dashboard_link = re.search(
            r'<a class="nav-link([^"]*)"[^>]*>\s*<svg[^>]*>.*?</svg>\s*Dashboard',
            body,
            re.DOTALL,
        )
        assert dashboard_link is not None
        assert "active" not in dashboard_link.group(1)


class TestFeedbackInboxCapacity:
    """H-5 / H-6 — inbox declutter + pagination honesty."""

    def test_feedback_template_is_inbox_first(self) -> None:
        text = (
            ROOT
            / "app/founder/dashboard/templates/founder_dashboard/feedback.html"
        ).read_text(encoding="utf-8")
        assert "Internal Alpha Summary" not in text
        assert "Product Health" not in text
        assert "Research Insights" not in text
        assert "feedback-pagination" in text
        assert "Showing" in text

    def test_inbox_pagination_surfaces_total(self, ctx, db) -> None:
        from app.models.user import User
        from app.services.founder_research_service import (
            FounderResearchService,
            InboxFilters,
        )
        from app.services.research_feedback_service import (
            SOURCE_SETTINGS,
            ResearchFeedbackService,
        )

        user = User(email="inbox-page@kwalitec.example")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        for i in range(55):
            ResearchFeedbackService.submit_checkin(
                user.id,
                experience_rating="Good",
                feature_helped_most="Dashboard",
                friction_area="Nothing",
                confidence_rating="High",
                return_intent="Probably",
                free_text=f"submission {i}",
                product_version="1.0.0",
                submission_source=SOURCE_SETTINGS,
            )

        page1 = FounderResearchService.build_dashboard_context(
            InboxFilters(),
            inbox_page=1,
            inbox_per_page=50,
        )
        assert page1.inbox_total == 55
        assert len(page1.inbox) == 50
        assert page1.inbox_has_next is True
        assert page1.inbox_page == 1

        page2 = FounderResearchService.build_dashboard_context(
            InboxFilters(),
            inbox_page=2,
            inbox_per_page=50,
        )
        assert len(page2.inbox) == 5
        assert page2.inbox_has_prev is True
        assert page2.inbox_has_next is False


class TestStaticAssetCaching:
    """H-8 — static responses are cacheable; HTML remains no-store."""

    def test_html_responses_remain_no_store(self, client) -> None:
        response = client.get("/auth/login")
        assert response.status_code == 200
        assert response.headers.get("Cache-Control") == "no-store"

    def test_static_assets_are_cacheable(self, client) -> None:
        response = client.get("/static/css/app.css")
        assert response.status_code == 200
        cache = response.headers.get("Cache-Control", "")
        assert "no-store" not in cache
        assert "public" in cache
        assert "immutable" in cache

    def test_static_urls_include_version_fingerprint(self, app) -> None:
        with app.test_request_context("/"):
            from flask import url_for

            url = url_for("static", filename="css/app.css")
            assert "v=" in url
            assert app.config["STATIC_ASSET_VERSION"] in url


class TestBrandAssetOptimisation:
    """H-9 — brand rasters remain within size budgets; display logo is approved PNG."""

    def test_heavy_pngs_under_size_budget(self) -> None:
        from app.brand_identity import APPROVED_LOGO_STATIC_PATH

        # Favicon/social budgets; approved master logo is the intentional UI source.
        budgets = {
            "social-preview.png": 1_000_000,
        }
        for name, limit in budgets.items():
            size = (BRANDING / name).stat().st_size
            assert size <= limit, f"{name} is {size} bytes (budget {limit})"

        approved = ROOT / "app" / "static" / APPROVED_LOGO_STATIC_PATH
        assert approved.is_file()
        # Master PNG (~1MB) is the single display source — keep under 1.5MB.
        assert approved.stat().st_size <= 1_500_000

    def test_social_preview_is_og_dimensions(self) -> None:
        # Lightweight dimension check without Pillow dependency.
        path = BRANDING / "social-preview.png"
        data = path.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        # IHDR chunk starts at byte 8; width/height are big-endian at 16/20.
        import struct

        width, height = struct.unpack(">II", data[16:24])
        assert (width, height) == (1200, 630)
