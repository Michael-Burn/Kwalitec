"""BI-001 — brand identity implementation regression checks."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.brand_identity import APPROVED_LOGO_STATIC_PATH

ROOT = Path(__file__).resolve().parents[1]
BRANDING = ROOT / "app" / "static" / "branding"
ASSETS = ROOT / "app" / "static" / "assets" / "branding"
BRAND_CSS = ROOT / "app" / "static" / "css" / "brand.css"
APP_CSS = ROOT / "app" / "static" / "css" / "app.css"
APPROVED_LOGO = ROOT / "app" / "static" / APPROVED_LOGO_STATIC_PATH


class TestBrandThemeTokens:
    def test_brand_css_declares_official_palette(self) -> None:
        css = BRAND_CSS.read_text(encoding="utf-8")
        for token in (
            "--brand-blue:",
            "--brand-blue-dark:",
            "--brand-navy:",
            "--brand-midnight:",
            "--brand-gold:",
            "--brand-gold-hover:",
            "--surface:",
            "--surface-alt:",
            "--text-primary:",
            "--text-secondary:",
            "--divider:",
        ):
            assert token in css, f"missing {token}"
        assert "#3B4FB8" in css
        assert "#E8B02B" in css
        assert "#020D24" in css

    def test_app_css_uses_official_primary_and_gold(self) -> None:
        css = APP_CSS.read_text(encoding="utf-8")
        assert "#3B4FB8" in css or "var(--brand-blue" in css
        assert "#E8B02B" in css
        assert "#2563eb" not in css
        assert "#D4AF37" not in css
        assert '"Inter"' in css or "Inter" in css

    def test_layouts_load_brand_css_and_inter(self) -> None:
        for relative in (
            "app/templates/layouts/base.html",
            "app/templates/layouts/auth_base.html",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            assert "css/brand.css" in text
            assert "@fontsource/inter" in text

    def test_brand_css_preserves_logo_aspect_ratio(self) -> None:
        css = BRAND_CSS.read_text(encoding="utf-8")
        assert ".brand-logo" in css
        assert "object-fit: contain" in css
        assert "width: auto" in css
        assert "height: auto" in css


class TestOfficialAssetPack:
    def test_approved_logo_is_single_display_source(self) -> None:
        assert APPROVED_LOGO.is_file() and APPROVED_LOGO.stat().st_size > 0
        assert APPROVED_LOGO.name == "approved-kwalitec-logo.png"
        # Master archive remains available and shares the same bytes.
        original = ASSETS / "original" / "Approved-Kwalitec-Logo.png"
        assert original.is_file()
        assert APPROVED_LOGO.read_bytes() == original.read_bytes()

    def test_runtime_icon_set_complete(self) -> None:
        for name in (
            "favicon.ico",
            "favicon-16.png",
            "favicon-32.png",
            "apple-touch-icon.png",
            "android-chrome-192.png",
            "android-chrome-512.png",
            "maskable-icon.png",
        ):
            path = BRANDING / name
            assert path.is_file(), name
            assert path.stat().st_size > 0

    def test_runtime_branding_has_no_recreated_logo_svgs(self) -> None:
        logo_svgs = list(BRANDING.glob("logo-*.svg"))
        assert logo_svgs == [], f"obsolete logo SVGs still present: {logo_svgs}"


class TestSidebarBrandChrome:
    def test_sign_out_follows_share_feedback(self) -> None:
        """BI-001A: Sign Out sits immediately under Share Feedback (not viewport-pinned)."""
        import re

        text = (ROOT / "app/templates/partials/sidebar.html").read_text(
            encoding="utf-8"
        )
        feedback_idx = text.index("Share Feedback")
        signout_idx = text.index("Sign out")
        assert feedback_idx < signout_idx
        assert "mt-auto" not in text
        # Logout form must be the next interactive block after Share Feedback.
        assert re.search(
            r"Share Feedback\s*</a>\s*<form method=\"post\"[^>]*url_for\('auth\.logout'\)",
            text,
            re.DOTALL,
        )
        # Must live inside the System nav section, not a bottom-pinned footer.
        system_block = text.split('nav-section-label">System', 1)[1]
        system_block = system_block.split("</nav>", 1)[0]
        assert "Sign out" in system_block
        assert "px-3 py-3 mt-auto" not in text

    def test_sidebar_nav_does_not_stretch_for_bottom_pin(self) -> None:
        """BI-001A: nav must not flex-grow; that created the Feedback↔Sign Out gap."""
        css = APP_CSS.read_text(encoding="utf-8")
        assert ".sidebar nav{flex:1" not in css
        assert "margin-top:auto" not in css.replace(" ", "").lower()
        assert ".sidebar .sidebar-signout{" in css
        assert "rgba(255, 255, 255, 0.55)" in css
        assert ".sidebar .nav-link:focus-visible" in css

    def test_active_nav_uses_brand_blue(self) -> None:
        css = APP_CSS.read_text(encoding="utf-8")
        assert "brand-blue" in css
        assert ".sidebar .nav-link.active" in css


class TestBrandHttp:
    def test_login_loads_brand_stylesheet(self, client) -> None:
        resp = client.get("/auth/login")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "css/brand.css" in html
        assert APPROVED_LOGO_STATIC_PATH in html
        assert "branding/favicon.svg" in html
        assert "#0D1B2A" in (BRANDING / "favicon.svg").read_text(encoding="utf-8")

    @pytest.mark.parametrize(
        "path",
        (
            "/static/branding/favicon-32.png",
            "/static/branding/maskable-icon.png",
            f"/static/{APPROVED_LOGO_STATIC_PATH}",
            "/static/css/brand.css",
        ),
    )
    def test_new_brand_assets_servable(self, client, path: str) -> None:
        resp = client.get(path)
        assert resp.status_code == 200
        assert len(resp.data) > 0
