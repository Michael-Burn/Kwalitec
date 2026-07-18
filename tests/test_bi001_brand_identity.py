"""BI-001 — brand identity implementation regression checks."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BRANDING = ROOT / "app" / "static" / "branding"
ASSETS = ROOT / "app" / "static" / "assets" / "branding"
BRAND_CSS = ROOT / "app" / "static" / "css" / "brand.css"
APP_CSS = ROOT / "app" / "static" / "css" / "app.css"


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


class TestOfficialAssetPack:
    def test_master_original_present(self) -> None:
        original = ASSETS / "original" / "Approved-Kwalitec-Logo.png"
        optimised = ASSETS / "original" / "Approved-Kwalitec-Logo-optimised.png"
        assert original.is_file() and original.stat().st_size > 0
        assert optimised.is_file() and optimised.stat().st_size > 0

    def test_runtime_icon_set_complete(self) -> None:
        for name in (
            "favicon.ico",
            "favicon-16.png",
            "favicon-32.png",
            "apple-touch-icon.png",
            "android-chrome-192.png",
            "android-chrome-512.png",
            "maskable-icon.png",
            "logo-icon.svg",
        ):
            path = BRANDING / name
            assert path.is_file(), name
            assert path.stat().st_size > 0

    def test_logo_svg_uses_official_colours(self) -> None:
        svg = (BRANDING / "logo-icon.svg").read_text(encoding="utf-8")
        assert "#3B4FB8" in svg
        assert "#E8B02B" in svg
        assert "#3950A2" not in svg


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
        assert "branding/logo-icon.svg" in html
        assert "#3B4FB8" in (BRANDING / "logo-icon.svg").read_text(encoding="utf-8")

    @pytest.mark.parametrize(
        "path",
        (
            "/static/branding/favicon-32.png",
            "/static/branding/maskable-icon.png",
            "/static/css/brand.css",
        ),
    )
    def test_new_brand_assets_servable(self, client, path: str) -> None:
        resp = client.get(path)
        assert resp.status_code == 200
        assert len(resp.data) > 0
