"""Tests for Capability 4.3 Universal Theme System."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_CSS = ROOT / "app" / "static" / "css" / "app.css"
THEME_JS = ROOT / "app" / "static" / "js" / "theme.js"


REQUIRED_TOKENS = (
    "--background",
    "--surface",
    "--surface-elevated",
    "--border",
    "--primary",
    "--primary-hover",
    "--secondary",
    "--text-primary",
    "--text-secondary",
    "--text-muted",
    "--success",
    "--warning",
    "--danger",
    "--shadow",
    "--radius",
)


class TestThemeAssets:
    """Static theme assets exist and declare the required contract."""

    def test_theme_js_exists(self):
        assert THEME_JS.is_file()

    def test_theme_js_supports_light_dark_system(self):
        source = THEME_JS.read_text(encoding="utf-8")
        assert 'STORAGE_KEY = "kwalitec-appearance"' in source
        assert "light" in source
        assert "dark" in source
        assert "system" in source
        assert "prefers-color-scheme" in source
        assert "data-theme" in source
        assert "data-bs-theme" in source
        assert "data-appearance" in source

    def test_app_css_declares_semantic_tokens(self):
        css = APP_CSS.read_text(encoding="utf-8")
        for token in REQUIRED_TOKENS:
            assert token in css, f"Missing semantic token {token}"

    def test_app_css_defines_dark_theme(self):
        css = APP_CSS.read_text(encoding="utf-8")
        assert '[data-theme="dark"]' in css
        assert '[data-theme="light"]' in css

    def test_dark_theme_keeps_brand_emphasis_readable(self):
        """Brand emphasis must not collapse to near-black chrome in dark mode."""
        css = APP_CSS.read_text(encoding="utf-8")
        dark_block_start = css.index('[data-theme="dark"]')
        dark_block = css[dark_block_start : dark_block_start + 1600]
        assert "--chrome:" in dark_block
        assert "--brand: #A5B4F0" in dark_block
        assert "--brand: #0f131a" not in dark_block
        assert "--on-primary: #0f131a" in dark_block

    def test_app_css_avoids_pure_black_background(self):
        css = APP_CSS.read_text(encoding="utf-8")
        # Dark background should not be pure #000
        dark_block_start = css.index('[data-theme="dark"]')
        dark_block = css[dark_block_start : dark_block_start + 1200]
        assert "--background: #000" not in dark_block
        assert "--background: #000000" not in dark_block


class TestThemeSurface:
    """Theme switcher is present on authenticated and public surfaces."""

    def test_dashboard_includes_theme_bootstrap_and_switcher(self, logged_in_client):
        response = logged_in_client.get("/dashboard/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "js/theme.js" in body
        assert 'data-appearance-option="light"' in body
        assert 'data-appearance-option="dark"' in body
        assert 'data-appearance-option="system"' in body
        assert 'aria-label="Appearance"' in body

    def test_login_includes_theme_bootstrap_and_switcher(self, client):
        response = client.get("/auth/login")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "js/theme.js" in body
        assert 'data-appearance-option="light"' in body
        assert 'data-appearance-option="dark"' in body
        assert 'data-appearance-option="system"' in body

    def test_settings_preferences_includes_appearance(self, logged_in_client):
        response = logged_in_client.get("/settings/preferences")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "Appearance" in body
        assert "data-appearance-select" in body
        assert 'data-appearance-option="system"' in body

    def test_missions_page_loads_with_theme(self, logged_in_client):
        response = logged_in_client.get("/missions/")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "js/theme.js" in body
        assert "appearance-switcher" in body

    def test_study_plans_page_loads_with_theme(self, logged_in_client):
        response = logged_in_client.get("/study-plan/wizard/1")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "js/theme.js" in body
