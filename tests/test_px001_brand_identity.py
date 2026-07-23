"""PX-001 — brand & visual identity refinement regression checks."""

from __future__ import annotations

from pathlib import Path

from app.brand_identity import (
    APPROVED_LOGO_MASTER_STATIC_PATH,
    APPROVED_LOGO_STATIC_PATH,
    PRODUCT_DESCRIPTOR,
    PRODUCT_NAME,
    PRODUCT_VALUE_PROPOSITION,
)
from app.version import PRODUCT_TAGLINE

ROOT = Path(__file__).resolve().parents[1]


class TestBrandPositioningConstants:
    def test_product_descriptor_is_education_os(self) -> None:
        assert PRODUCT_NAME == "Kwalitec"
        assert PRODUCT_DESCRIPTOR == "Education Operating System"
        assert PRODUCT_VALUE_PROPOSITION == "Know exactly what to study next."
        assert PRODUCT_TAGLINE == PRODUCT_DESCRIPTOR

    def test_master_logo_archive_present(self) -> None:
        master = ROOT / "app" / "static" / APPROVED_LOGO_MASTER_STATIC_PATH
        display = ROOT / "app" / "static" / APPROVED_LOGO_STATIC_PATH
        assert master.is_file() and master.stat().st_size > 0
        assert display.is_file() and display.stat().st_size > 0


class TestAuthBrandHierarchy:
    def test_login_template_brand_hierarchy(self) -> None:
        text = (ROOT / "app/templates/auth/login.html").read_text(encoding="utf-8")
        assert "partials/brand_logo.html" in text
        assert "landing-brand-name" in text
        assert "landing-descriptor" in text
        assert "landing-value" in text
        assert "product_descriptor" in text
        assert "product_value_proposition" in text
        assert "Disciplined Exam Preparation" not in text
        assert "Study Plan Wizard" not in text
        assert "Burnout Monitoring" not in text

    def test_login_page_renders_brand_first(self, client) -> None:
        resp = client.get("/auth/login")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert APPROVED_LOGO_STATIC_PATH in html
        assert PRODUCT_NAME in html
        assert PRODUCT_DESCRIPTOR in html
        assert PRODUCT_VALUE_PROPOSITION in html
        assert "Disciplined Exam Preparation" not in html
        # Brand stack appears before the sign-in card title.
        brand_idx = html.index("landing-brand-name")
        signin_idx = html.index("landing-card-title")
        assert brand_idx < signin_idx
        # Outcome-oriented capabilities, not implementation labels.
        assert "Always know what to study next" in html
        assert "Study Plan Wizard" not in html

    def test_sidebar_uses_education_os_descriptor(self, logged_in_client) -> None:
        resp = logged_in_client.get("/dashboard/")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "sidebar-brand-descriptor" in html
        assert PRODUCT_DESCRIPTOR in html
        assert APPROVED_LOGO_STATIC_PATH in html


class TestLogoPresentationRules:
    def test_brand_css_forbids_sticker_chrome(self) -> None:
        css = (ROOT / "app/static/css/brand.css").read_text(encoding="utf-8")
        assert "border-radius: 0" in css
        assert "box-shadow: none" in css
        assert "background: transparent" in css

    def test_brand_logo_partial_preserves_aspect_attrs(self) -> None:
        text = (ROOT / "app/templates/partials/brand_logo.html").read_text(
            encoding="utf-8"
        )
        assert 'width="1418"' in text
        assert 'height="372"' in text
        assert "approved-kwalitec-logo.png" in text
