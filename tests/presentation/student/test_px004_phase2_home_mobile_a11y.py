"""PX-004 Phase 2 — Home, mobile nav, accessibility presentation checks."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


class TestHomeComposition:
    """WS-04 — PX-B-010 / PX-B-048."""

    def test_home_marks_composition_and_density(self, student_client):
        html = student_client.get("/student/").get_data(as_text=True)
        assert 'data-px004="home-composition"' in html
        assert "data-density=" in html
        assert 'data-student-cta="primary"' in html or "Choose an exam" in html

    def test_home_secondary_uses_disclosure(self):
        home = (ROOT / "app/templates/student/home.html").read_text(encoding="utf-8")
        assert 'data-px004="secondary-progress"' in home
        assert 'data-px004="secondary-actions"' in home
        assert "<details" in home
        assert "show_progress_strip" in home

    def test_density_helper_day_zero(self):
        from app.presentation.student.services.student_home_service import (
            StudentHomeService,
        )
        from app.presentation.student.view_models import HomePageViewModel

        density = StudentHomeService._density_presentation(
            state="mission",
            mission=None,
            history=None,
            home=HomePageViewModel(),
        )
        assert density["density_mode"] == "day_zero"
        assert density["show_progress_strip"] is False


class TestAnalyticsPresentation:
    """WS-04 — PX-B-011 / PX-B-012."""

    def test_analytics_kpi_row_capped_and_day_zero_framed(self):
        html = (ROOT / "app/templates/analytics/index.html").read_text(
            encoding="utf-8"
        )
        assert 'data-px004="analytics-kpis"' in html
        assert "text-danger" not in html.split("analytics-kpis")[1].split(
            "{% if readiness_narrative %}"
        )[0]
        assert "Nothing here is a failure" in html
        assert "stat-value text-warning" not in html.split("Key Metrics")[1].split(
            "Charts Row"
        )[0]

    def test_study_hours_rounded_honestly(self):
        src = (ROOT / "app/services/analytics_service.py").read_text(encoding="utf-8")
        assert "PX-B-011" in src
        assert "int(round(total_minutes / 60.0))" in src


class TestJourneyHistoryCraft:
    """WS-04 — PX-B-013."""

    def test_journey_up_next_enrichment(self):
        html = (ROOT / "app/templates/student/journey.html").read_text(
            encoding="utf-8"
        )
        assert 'data-px004="journey-up-next"' in html
        assert 'data-px004="why-next-duration"' in html

    def test_history_continuity_and_why_next(self):
        hist = (ROOT / "app/templates/student/history.html").read_text(
            encoding="utf-8"
        )
        assert 'data-px004="history-continuity"' in hist
        card = (
            ROOT / "app/templates/student/components/history_card.html"
        ).read_text(encoding="utf-8")
        assert 'data-px004="history-why-next"' in card


class TestMobileNav:
    """WS-05 — PX-B-036."""

    def test_canonical_drawer_pattern_marked(self, student_client):
        html = student_client.get("/student/").get_data(as_text=True)
        assert 'data-mobile-nav="drawer"' in html
        assert 'data-px004="mobile-nav"' in html
        assert 'data-student-nav-toggle' in html
        assert 'aria-controls="student-nav-list"' in html


class TestAccessibilityFoundation:
    """WS-06 — PX-B-023…030."""

    def test_confirm_modal_dialog_roles_and_fallback(self):
        modal = (ROOT / "app/templates/partials/confirm_modal.html").read_text(
            encoding="utf-8"
        )
        assert 'role="dialog"' in modal
        assert 'aria-modal="true"' in modal
        assert 'data-px004="confirm-fallback"' in modal
        js = (ROOT / "app/static/js/confirm-modal.js").read_text(encoding="utf-8")
        assert "Confirmation dialog is unavailable" in js
        assert "bootstrap.Modal" in js

    def test_session_timer_live_region_throttled(self):
        """Timer chrome removed; throttle logic remains in session EOS JS."""
        body = (
            ROOT / "app/templates/session/partials/session_body.html"
        ).read_text(encoding="utf-8")
        assert "data-session-timer-live" not in body
        assert "ds-session-position" in body
        js = (ROOT / "app/static/js/session/study_session_eos.js").read_text(
            encoding="utf-8"
        )
        assert "PX-B-024" in js
        assert "lastAnnouncedMinute" in js

    def test_touch_target_token_on_student_nav(self):
        css = (ROOT / "app/static/css/student/student.css").read_text(
            encoding="utf-8"
        )
        assert "min-height: var(--touch-target-min" in css
        assert ".student-nav-link" in css
        assert "button.student-signout" in css
        app_css = (ROOT / "app/static/css/app.css").read_text(encoding="utf-8")
        assert "ctx-help-trigger" in app_css
        assert "var(--touch-target-min" in app_css.split("ctx-help-trigger")[1][
            :400
        ]

    def test_focus_visible_not_shared_with_mouse_transform(self):
        app_css = (ROOT / "app/static/css/app.css").read_text(encoding="utf-8")
        assert "btn-primary:focus-visible" in app_css
        # Legacy :focus with transform must not couple mouse focus to lift.
        primary_block = app_css.split(".btn-primary:hover")[1].split(
            ".btn-primary:active"
        )[0]
        assert ":focus," not in primary_block or "focus-visible" in primary_block

    def test_student_reduced_motion_covers_nav(self):
        css = (ROOT / "app/static/css/student/student.css").read_text(
            encoding="utf-8"
        )
        # Prefer the student-shell block that disables nav transitions.
        assert (
            ".student-nav-link,\n  .student-nav-toggle" in css
            or ".student-nav-link,\n  .student-btn-primary" in css
            or (
                "prefers-reduced-motion: reduce" in css
                and css.count(".student-nav-link") >= 2
            )
        )
        assert "animation: none !important" in css

    def test_keyboard_primary_path_markers(self, student_client):
        """PX-B-029 — primary path retains labelled controls for keyboard use."""
        home = student_client.get("/student/").get_data(as_text=True)
        assert "<h1" in home
        assert "student-nav" in home
        assert 'aria-current="page"' in home
        journey = student_client.get("/student/journey").get_data(as_text=True)
        assert "<h1" in journey

    def test_automated_a11y_static_contracts(self, student_client):
        """PX-B-030 — expanded static a11y contracts on primary routes."""
        for path in ("/student/", "/student/journey", "/student/history"):
            html = student_client.get(path).get_data(as_text=True)
            assert 'lang="en"' in html
            assert "viewport" in html
            assert "<h1" in html
            assert 'role="main"' in html or "<main" in html


@pytest.mark.parametrize(
    "token",
    [
        "data-mobile-nav",
        "data-px004",
        "touch-target-min",
    ],
)
def test_px004_tokens_present_in_shipped_assets(token):
    joined = "\n".join(
        [
            (ROOT / "app/templates/student/components/navigation.html").read_text(
                encoding="utf-8"
            ),
            (ROOT / "app/static/css/tokens.css").read_text(encoding="utf-8"),
            (ROOT / "app/templates/student/home.html").read_text(encoding="utf-8"),
        ]
    )
    assert token in joined
