"""Tests for Capability 4.3 Universal Theme System."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS_CSS = ROOT / "app" / "static" / "css" / "tokens.css"
THEME_JS = ROOT / "app" / "static" / "js" / "theme.js"


REQUIRED_TOKENS = (
    "--background",
    "--surface",
    "--surface-elevated",
    "--surface-primary",
    "--surface-secondary",
    "--surface-overlay",
    "--border",
    "--border-primary",
    "--primary",
    "--primary-hover",
    "--accent-primary",
    "--secondary",
    "--text-primary",
    "--text-secondary",
    "--text-muted",
    "--chrome-text",
    "--chrome-text-muted",
    "--success",
    "--warning",
    "--danger",
    "--shadow",
    "--radius",
    "--color-text-primary",
    "--session-primary",
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
        css = TOKENS_CSS.read_text(encoding="utf-8")
        for token in REQUIRED_TOKENS:
            assert token in css, f"Missing semantic token {token}"

    def test_app_css_defines_dark_theme(self):
        css = TOKENS_CSS.read_text(encoding="utf-8")
        assert '[data-theme="dark"]' in css
        assert '[data-theme="light"]' in css

    def test_dark_theme_keeps_brand_emphasis_readable(self):
        """Brand emphasis must not collapse to near-black chrome in dark mode."""
        css = TOKENS_CSS.read_text(encoding="utf-8")
        dark_block_start = css.index('[data-theme="dark"]')
        dark_block = css[dark_block_start : dark_block_start + 2200]
        assert "--chrome:" in dark_block
        assert "--brand: #A3B8D9" in dark_block
        assert "--brand: #0f131a" not in dark_block
        assert "--on-primary: #1A1816" in dark_block
        assert "--chrome-text:" in dark_block

    def test_app_css_avoids_pure_black_background(self):
        css = TOKENS_CSS.read_text(encoding="utf-8")
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
        assert "data-appearance-cycle" in body
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


DESIGN_SYSTEM_CSS = ROOT / "app" / "static" / "css" / "design_system.css"
APP_CSS = ROOT / "app" / "static" / "css" / "app.css"
BRAND_CSS = ROOT / "app" / "static" / "css" / "brand.css"


def _rel_lum(rgb: tuple[int, int, int]) -> float:
    def chan(c: int) -> float:
        x = c / 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4

    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    l1, l2 = _rel_lum(a), _rel_lum(b)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def _rule_block(css: str, selector: str) -> str:
    needle = selector + " {"
    start = css.index(needle)
    end = css.index("}", start)
    return css[start:end]


class TestProgressTrackContrast:
    """Syllabus progress trough must be a visible UI boundary (WCAG 1.4.11)."""

    # Token hex from tokens.css / brand.css, both themes.
    LIGHT_SURFACE = (247, 242, 234)  # --surface #F7F2EA
    LIGHT_MUTED = (122, 115, 106)  # --text-muted #7A736A
    DARK_SURFACE = (36, 33, 32)  # --surface #242120
    DARK_MUTED = (154, 146, 136)  # --text-muted #9A9288

    def test_track_uses_muted_outline_not_card_fill(self) -> None:
        block = _rule_block(
            DESIGN_SYSTEM_CSS.read_text(encoding="utf-8"),
            ".ds-os-progress__track",
        )
        assert "border: 1px solid var(--text-muted)" in block
        assert "background: transparent" in block
        assert "background: var(--surface-secondary" not in block

    def test_muted_outline_meets_ui_component_contrast(self) -> None:
        light = _contrast(self.LIGHT_MUTED, self.LIGHT_SURFACE)
        dark = _contrast(self.DARK_MUTED, self.DARK_SURFACE)
        assert light >= 3.0, f"light track outline only {light:.2f}:1"
        assert dark >= 3.0, f"dark track outline only {dark:.2f}:1"


class TestSessionBriefingClosedChrome:
    def test_closed_briefing_has_no_card_chrome(self) -> None:
        css = DESIGN_SYSTEM_CSS.read_text(encoding="utf-8")
        closed = _rule_block(css, ".ds-session-briefing")
        assert "padding:" not in closed
        assert "background:" not in closed
        assert "border:" not in closed
        opened = _rule_block(css, ".ds-session-briefing[open]")
        assert "padding: var(--space-4)" in opened
        assert "background: var(--surface)" in opened
        assert "border: 1px solid var(--border-subtle)" in opened


class TestDarkSuccessBadgeTone:
    def test_dark_active_badge_uses_warm_mastered_tokens(self) -> None:
        css = APP_CSS.read_text(encoding="utf-8")
        assert (
            ".badge.text-bg-success{background-color:var(--learning-mastered)"
            " !important;color:var(--on-success) !important;}"
        ) in css
        brand_dark = BRAND_CSS.read_text(encoding="utf-8")
        dark_start = brand_dark.index('[data-theme="dark"]')
        dark_block = brand_dark[dark_start : dark_start + 1600]
        assert "--learning-state-mastered: #6B8F7E" in dark_block
        assert "--status-success: #4ade80" in dark_block

