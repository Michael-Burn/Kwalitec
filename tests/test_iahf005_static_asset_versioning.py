"""IAHF-005 — centralized static asset cache versioning."""

from __future__ import annotations

from pathlib import Path

from app.brand_identity import APPROVED_LOGO_STATIC_PATH
from app.static_assets import versioned_static
from app.version import STATIC_ASSET_VERSION

ROOT = Path(__file__).resolve().parents[1]


class TestStaticAssetVersionSource:
    def test_static_asset_version_is_non_empty(self) -> None:
        assert STATIC_ASSET_VERSION
        assert " " not in STATIC_ASSET_VERSION

    def test_app_config_uses_canonical_version(self, app) -> None:
        assert app.config["STATIC_ASSET_VERSION"] == STATIC_ASSET_VERSION


class TestVersionedStaticHelper:
    def test_returns_static_url_with_configured_version(self, app) -> None:
        with app.test_request_context("/"):
            url = versioned_static(APPROVED_LOGO_STATIC_PATH)
        assert url.startswith(f"/static/{APPROVED_LOGO_STATIC_PATH}")
        assert f"v={STATIC_ASSET_VERSION}" in url

    def test_supports_external_urls(self, app) -> None:
        with app.test_request_context("/"):
            url = versioned_static("branding/social-preview.png", _external=True)
        assert url.startswith("http")
        assert "branding/social-preview.png" in url
        assert f"v={STATIC_ASSET_VERSION}" in url

    def test_supports_blueprint_static_endpoint(self, app) -> None:
        with app.test_request_context("/"):
            url = versioned_static(
                "css/founder_dashboard.css",
                endpoint="founder_dashboard.static",
            )
        assert "founder_dashboard.css" in url
        assert f"v={STATIC_ASSET_VERSION}" in url

    def test_url_for_static_also_receives_fingerprint(self, app) -> None:
        """url_defaults safety net still versions raw url_for calls."""
        with app.test_request_context("/"):
            from flask import url_for

            url = url_for("static", filename="css/brand.css")
        assert f"v={STATIC_ASSET_VERSION}" in url


class TestTemplateVersionedStaticWiring:
    """Static template checks — no Flask app boot required."""

    def test_layouts_use_versioned_static(self) -> None:
        for relative in (
            "app/templates/layouts/base.html",
            "app/templates/layouts/auth_base.html",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            assert "versioned_static(" in text
            assert "url_for('static'" not in text

    def test_brand_partials_use_versioned_static(self) -> None:
        for relative in (
            "app/templates/partials/brand_meta.html",
            "app/templates/partials/brand_logo.html",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            assert "versioned_static(" in text
            assert "url_for('static'" not in text
            assert "?v=" not in text

    def test_brand_meta_still_references_canonical_assets(self) -> None:
        text = (ROOT / "app/templates/partials/brand_meta.html").read_text(
            encoding="utf-8"
        )
        for asset in (
            "branding/favicon.ico",
            "branding/favicon.svg",
            "branding/favicon-16.png",
            "branding/favicon-32.png",
            "branding/apple-touch-icon.png",
            "branding/manifest.webmanifest",
            "branding/social-preview.png",
        ):
            assert asset in text


class TestRenderedAssetVersioning:
    def test_login_page_appends_asset_version(self, client, app) -> None:
        resp = client.get("/auth/login")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        version = app.config["STATIC_ASSET_VERSION"]
        assert f"{APPROVED_LOGO_STATIC_PATH}?v={version}" in html
        assert f"branding/favicon.ico?v={version}" in html
        assert f"branding/favicon.svg?v={version}" in html
        assert f"css/brand.css?v={version}" in html
        assert f"css/app.css?v={version}" in html
        assert f"branding/manifest.webmanifest?v={version}" in html
        assert f"branding/social-preview.png?v={version}" in html

    def test_dashboard_shell_appends_asset_version(self, logged_in_client, app) -> None:
        resp = logged_in_client.get("/dashboard/")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        version = app.config["STATIC_ASSET_VERSION"]
        assert f"{APPROVED_LOGO_STATIC_PATH}?v={version}" in html
        assert f"js/theme.js?v={version}" in html
        assert f"js/app.js?v={version}" in html

    def test_branding_assets_still_servable(self, client) -> None:
        for filename in (
            "branding/favicon.ico",
            "branding/favicon.svg",
            APPROVED_LOGO_STATIC_PATH,
            "branding/manifest.webmanifest",
            "branding/social-preview.png",
            "branding/android-chrome-192.png",
        ):
            resp = client.get(f"/static/{filename}")
            assert resp.status_code == 200, filename
            assert len(resp.data) > 0

    def test_manifest_still_references_correct_assets(self, client) -> None:
        resp = client.get("/static/branding/manifest.webmanifest")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "android-chrome-192.png" in body
        assert "android-chrome-512.png" in body
        assert "/static/branding/" in body
