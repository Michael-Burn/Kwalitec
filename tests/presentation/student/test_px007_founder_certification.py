"""PX-007 — Founder dogfood defect guards + Premium Certification contracts.

Presentation / identity only. Does not change educational packages, selection,
Twin, or Runtime authority.
"""

from __future__ import annotations

from pathlib import Path

from app.application.student_experience.student_microcopy import (
    FEEDBACK_QUICK_DESCRIPTION,
    FEEDBACK_SUGGEST_DESCRIPTION,
    FEEDBACK_THANKS_FLASH,
    STUDENT_RELEASE_LABEL,
)
from app.brand_identity import PRODUCT_DESCRIPTOR
from app.brand_identity import STUDENT_RELEASE_LABEL as BRAND_RELEASE

ROOT = Path(__file__).resolve().parents[3]


class TestPx007FeedbackIdentity:
    """Close PX7-001 / PX7-002 student feedback identity leaks."""

    def test_feedback_microcopy_student_grade(self) -> None:
        assert STUDENT_RELEASE_LABEL == "Private Beta"
        assert BRAND_RELEASE == "Private Beta"
        assert "Internal Alpha" not in FEEDBACK_THANKS_FLASH
        assert "Private Beta" in FEEDBACK_THANKS_FLASH
        assert "Internal Alpha" not in FEEDBACK_SUGGEST_DESCRIPTION
        assert "Internal Alpha" not in FEEDBACK_QUICK_DESCRIPTION
        assert "Kwalitec" in FEEDBACK_SUGGEST_DESCRIPTION

    def test_feedback_templates_no_internal_alpha_voice(self) -> None:
        templates = [
            ROOT / "app/templates/alpha/feedback_beta.html",
            ROOT / "app/templates/alpha/feedback_suggest.html",
            ROOT / "app/templates/alpha/feedback_mission_helpful.html",
            ROOT / "app/templates/alpha/feedback_explanation_clear.html",
        ]
        for path in templates:
            html = path.read_text(encoding="utf-8")
            assert "Internal Alpha" not in html, path.name
            assert "Closed Beta" not in html, path.name

    def test_feedback_beta_uses_private_beta_eyebrow(self) -> None:
        html = (ROOT / "app/templates/alpha/feedback_beta.html").read_text(
            encoding="utf-8"
        )
        assert "student_release_label" in html or "Private Beta" in html

    def test_feedback_flash_route_uses_microcopy(self) -> None:
        routes = (ROOT / "app/alpha/routes.py").read_text(encoding="utf-8")
        assert "FEEDBACK_THANKS_FLASH" in routes
        assert "helps Internal Alpha" not in routes


class TestPx007PremiumContracts:
    """Spot-check that Phase 1–4 premium contracts remain intact at certification."""

    def test_student_descriptor_not_eos(self) -> None:
        assert PRODUCT_DESCRIPTOR == "Exam-ready study guidance"
        assert "Education Operating System" not in PRODUCT_DESCRIPTOR

    def test_house_motion_tokens_present(self) -> None:
        tokens = (ROOT / "app/static/css/tokens.css").read_text(encoding="utf-8")
        assert "--motion-page-enter" in tokens
        assert "--motion-success-in" in tokens
        assert "--motion-disclosure" in tokens
        assert "prefers-reduced-motion" in tokens

    def test_touch_target_token(self) -> None:
        tokens = (ROOT / "app/static/css/tokens.css").read_text(encoding="utf-8")
        assert "--touch-target-min" in tokens
        assert "2.75rem" in tokens

    def test_error_reference_guidance(self) -> None:
        for name in ("404.html", "403.html", "500.html"):
            html = (ROOT / f"app/templates/errors/{name}").read_text(encoding="utf-8")
            assert "ERROR_REFERENCE" in html or "Reference ID" in html

    def test_finish_confirm_modal_wired(self) -> None:
        body = (
            ROOT / "app/templates/session/partials/session_body.html"
        ).read_text(encoding="utf-8")
        assert "data-confirm-trigger" in body
        base = (ROOT / "app/templates/session/base.html").read_text(encoding="utf-8")
        assert "confirm_modal.html" in base
        assert "confirm-modal.js" in base

    def test_login_private_beta_not_internal_alpha_badge(self) -> None:
        login = (ROOT / "app/templates/auth/login.html").read_text(encoding="utf-8")
        assert "student_release_badge.html" in login
        assert "internal_alpha_badge.html" not in login

    def test_skeleton_macros_wired(self) -> None:
        home = (ROOT / "app/templates/student/home.html").read_text(encoding="utf-8")
        assert "skeleton_student_home" in home
        session = (
            ROOT / "app/templates/session/partials/session_body.html"
        ).read_text(encoding="utf-8")
        assert "skeleton_mission" in session or "skeleton_mission_hero" in session


class TestPx007StudentSurfaces:
    def test_login_renders_student_identity(self, client) -> None:
        resp = client.get("/auth/login")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert PRODUCT_DESCRIPTOR in html
        assert "Education Operating System" not in html
        assert "Internal Alpha · Founding Cohort" not in html
        assert "Private Beta" in html or STUDENT_RELEASE_LABEL in html
