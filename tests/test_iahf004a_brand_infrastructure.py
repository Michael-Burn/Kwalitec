"""IAHF-004A — brand infrastructure regression checks."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
BRANDING = ROOT / "app" / "static" / "branding"

REQUIRED_ASSETS = (
    "logo-primary.svg",
    "logo-primary.png",
    "logo-white.svg",
    "logo-white.png",
    "logo-monochrome.svg",
    "logo-icon.svg",
    "logo-icon.png",
    "favicon.ico",
    "apple-touch-icon.png",
    "android-chrome-192.png",
    "android-chrome-512.png",
    "social-preview.png",
    "manifest.webmanifest",
)


class TestBrandAssetInventory:
    def test_canonical_branding_directory_exists(self) -> None:
        assert BRANDING.is_dir()

    @pytest.mark.parametrize("filename", REQUIRED_ASSETS)
    def test_required_asset_present(self, filename: str) -> None:
        path = BRANDING / filename
        assert path.is_file(), f"missing canonical brand asset: {filename}"
        assert path.stat().st_size > 0

    def test_no_logo_assets_under_static_images(self) -> None:
        images = ROOT / "app" / "static" / "images"
        if not images.is_dir():
            return
        logo_like = {
            p.name
            for p in images.iterdir()
            if p.is_file()
            and p.suffix.lower() in {".svg", ".png", ".ico", ".webp", ".jpg", ".jpeg"}
        }
        assert logo_like == set()

    def test_manifest_is_valid_and_points_at_canonical_icons(self) -> None:
        manifest_text = (BRANDING / "manifest.webmanifest").read_text(
            encoding="utf-8"
        )
        manifest = json.loads(manifest_text)
        assert manifest["name"] == "Kwalitec"
        assert manifest["short_name"] == "Kwalitec"
        assert manifest["theme_color"] == "#0D1B2A"
        assert manifest["background_color"] == "#0D1B2A"
        icon_srcs = [icon["src"] for icon in manifest["icons"]]
        assert any(src.endswith("android-chrome-192.png") for src in icon_srcs)
        assert any(src.endswith("android-chrome-512.png") for src in icon_srcs)
        for src in icon_srcs:
            relative = src.removeprefix("/static/")
            assert (ROOT / "app" / "static" / relative).is_file()


class TestBrandTemplateWiring:
    """Static template checks — no Flask app boot required."""

    def test_layouts_include_brand_meta(self) -> None:
        for relative in (
            "app/templates/layouts/base.html",
            "app/templates/layouts/auth_base.html",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            assert "partials/brand_meta.html" in text

    def test_brand_meta_partial_standardises_identity(self) -> None:
        path = ROOT / "app/templates/partials/brand_meta.html"
        text = path.read_text(encoding="utf-8")
        assert "branding/favicon.ico" in text
        assert "branding/favicon.svg" in text
        assert "branding/manifest.webmanifest" in text
        assert "branding/social-preview.png" in text
        assert 'content="#0D1B2A"' in text
        assert 'content="Kwalitec"' in text
        assert "og:image" in text
        assert "twitter:image" in text

    def test_login_uses_canonical_logo_partial(self) -> None:
        text = (ROOT / "app/templates/auth/login.html").read_text(encoding="utf-8")
        assert "partials/brand_logo.html" in text
        assert "brand_variant='icon'" in text
        assert "M12 2L2 7l10 5 10-5-10-5z" not in text

    def test_sidebar_uses_canonical_logo_partial(self) -> None:
        path = ROOT / "app/templates/partials/sidebar.html"
        text = path.read_text(encoding="utf-8")
        assert "partials/brand_logo.html" in text
        assert "sidebar-brand-mark" in text


class TestBrandHttpWiring:
    def test_login_page_uses_canonical_assets(self, client) -> None:
        resp = client.get("/auth/login")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "branding/favicon.ico" in html
        assert "branding/favicon.svg" in html
        assert "branding/logo-icon.svg" in html  # login chrome mark
        assert "branding/manifest.webmanifest" in html
        assert "branding/social-preview.png" in html
        assert 'name="theme-color" content="#0D1B2A"' in html
        assert 'name="application-name" content="Kwalitec"' in html
        assert 'property="og:image"' in html
        assert "M12 2L2 7l10 5 10-5-10-5z" not in html

    def test_authenticated_shell_uses_canonical_logo(self, logged_in_client) -> None:
        resp = logged_in_client.get("/dashboard/")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "branding/logo-icon.svg" in html
        assert "branding/favicon.svg" in html
        assert "branding/favicon.ico" in html
        assert "sidebar-brand-mark" in html

    def test_static_brand_assets_are_servable(self, client) -> None:
        for filename in (
            "branding/favicon.ico",
            "branding/favicon.svg",
            "branding/logo-icon.svg",
            "branding/manifest.webmanifest",
            "branding/social-preview.png",
            "branding/android-chrome-192.png",
        ):
            resp = client.get(f"/static/{filename}")
            assert resp.status_code == 200, filename
            assert len(resp.data) > 0
