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
        brand = BRAND_CSS.read_text(encoding="utf-8")
        assert "#3B4FB8" in css or "var(--brand-blue" in css or "var(--primary)" in css
        # Official gold lives on the brand token (--brand-gold: #E8B02B); app.css
        # consumes it via var(--brand-gold) rather than repeating the hex.
        assert "#E8B02B" in brand
        assert "brand-gold" in css or "#E8B02B" in css
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
            # UX-001 self-hosts Inter via fonts.css (Fontsource files under
            # static/fonts/inter). CDN @fontsource/inter must not appear in shells.
            assert "css/fonts.css" in text
            assert "@fontsource/inter" not in text

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
        # Final Approved master remains archived; display lockup originates from it.
        master = ASSETS / "original" / "Final-Approved-Kwalitec-Logo.png"
        legacy = ASSETS / "original" / "Approved-Kwalitec-Logo.png"
        assert master.is_file() and master.stat().st_size > 0
        assert legacy.is_file() and legacy.read_bytes() == master.read_bytes()
        # Display asset is transparent lockup derived from master (not a redraw).
        from PIL import Image

        display = Image.open(APPROVED_LOGO)
        assert display.mode in {"RGBA", "LA", "PA"} or (
            display.mode == "P" and "transparency" in display.info
        )
        assert display.size[0] > 0 and display.size[1] > 0

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

    def test_favicon_svg_embeds_derived_mark_not_path_redraw(self) -> None:
        text = (BRANDING / "favicon.svg").read_text(encoding="utf-8")
        assert "#0D1B2A" in text
        assert "data:image/png;base64," in text
        assert 'id="k-mark"' not in text
        assert "hand-built vector" not in text


class TestStudentShellBrandChrome:
    def test_eos_shell_sign_out_beside_nav(self) -> None:
        """RC-2026.07.29-03: Sign out lives in the EOS topbar, not a pinned sidebar."""
        text = (ROOT / "app/templates/layouts/eos_student.html").read_text(
            encoding="utf-8"
        )
        assert "auth.logout" in text
        assert "student-signout" in text
        assert "mt-auto" not in text
        assert "student/components/navigation.html" in text
        assert "appearance_switcher" in text

    def test_eos_shell_active_nav_uses_brand_tokens(self) -> None:
        css = (ROOT / "app/static/css/student/student.css").read_text(
            encoding="utf-8"
        )
        assert ".student-nav-link.is-active" in css
        # Active chrome uses inverse/chrome text tokens (not a brand-white alias).
        assert (
            "brand-white" in css
            or "#fff" in css
            or "--chrome-text" in css
            or "--text-inverse" in css
        )

    def test_active_nav_uses_brand_blue(self) -> None:
        css = APP_CSS.read_text(encoding="utf-8")
        assert "brand-blue" in css
        student = (ROOT / "app/static/css/student/student.css").read_text(
            encoding="utf-8"
        )
        assert "59, 79, 184" in student or "brand-blue" in student

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
