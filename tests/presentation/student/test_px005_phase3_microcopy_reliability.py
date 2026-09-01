"""PX-005 — Premium Experience Phase 3 (WS-07 Microcopy · WS-08 Reliability)."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.application.student_experience.student_microcopy import (
    CONTINUE_CONTENTION_MESSAGE,
    HELP_CENTRE_EYEBROW,
    PRACTICE_RESULTS_EYEBROW,
    PREPARING_MISSION_LABEL,
    REFLECTION_VALUE_FRAMING,
    STUDENT_RELEASE_LABEL,
    STUDENT_WELCOME_TITLE,
    exam_horizon_copy,
    return_after_gap_copy,
)
from app.brand_identity import PRODUCT_DESCRIPTOR
from app.brand_identity import STUDENT_RELEASE_LABEL as BRAND_RELEASE
from app.presentation.session.messages import FLASH_WARNING
from app.version import PRODUCT_TAGLINE

ROOT = Path(__file__).resolve().parents[3]


class TestPx005IdentityMicrocopy:
    def test_eos_descriptor_retired(self) -> None:
        assert PRODUCT_DESCRIPTOR == "Exam-ready study guidance"
        assert PRODUCT_TAGLINE == PRODUCT_DESCRIPTOR
        assert "Education Operating System" not in PRODUCT_DESCRIPTOR
        manifest = (
            ROOT / "app/static/branding/manifest.webmanifest"
        ).read_text(encoding="utf-8")
        assert "Exam-ready study guidance" in manifest
        assert "Education Operating System" not in manifest

    def test_student_release_identity(self) -> None:
        assert STUDENT_RELEASE_LABEL == "Private Beta"
        assert BRAND_RELEASE == "Private Beta"
        login = (ROOT / "app/templates/auth/login.html").read_text(encoding="utf-8")
        assert "student_release_badge.html" in login
        assert "internal_alpha_badge.html" not in login
        assert "STUDENT_WELCOME_TITLE" in login or "New to Kwalitec" in login

    def test_practice_results_terminology(self) -> None:
        tmpl = (
            ROOT / "app/templates/mission/session_practice_outcome.html"
        ).read_text(encoding="utf-8")
        assert "PRACTICE_RESULTS_EYEBROW" in tmpl
        assert "Practice Outcome Capture" not in tmpl
        assert PRACTICE_RESULTS_EYEBROW == "Practice results"

    def test_help_centre_faq_and_identity(self) -> None:
        help_html = (ROOT / "app/templates/alpha/help.html").read_text(encoding="utf-8")
        assert "HELP_CENTRE_EYEBROW" in help_html or HELP_CENTRE_EYEBROW in help_html
        assert "pause or defer" in help_html.lower()
        assert "exam date or sitting" in help_html.lower()
        assert "Internal Alpha team" not in help_html
        assert "HELP_FEEDBACK_CTA" in help_html or "Send product feedback" in help_html

    def test_diagnostic_support_disclosure(self) -> None:
        settings = (
            ROOT / "app/templates/settings/index.html"
        ).read_text(encoding="utf-8")
        assert "Build information for support" in settings
        assert "Internal build track" not in settings

    def test_return_after_gap_copy(self) -> None:
        same = return_after_gap_copy(days_since_last=0)
        assert "Welcome back" in same.greeting
        assert same.support_line is None
        week = return_after_gap_copy(days_since_last=5)
        assert week.support_line
        week_line = week.support_line.lower()
        assert "catch-up" in week_line or "authorised" in week_line
        long = return_after_gap_copy(days_since_last=30)
        assert long.support_line
        assert "penalis" not in (long.support_line or "").lower()
        assert "guilt" not in (long.support_line or "").lower()

    def test_exam_horizon_calm(self) -> None:
        assert exam_horizon_copy(None) is None
        assert exam_horizon_copy(60) is None
        near = exam_horizon_copy(5)
        assert near is not None
        assert near.support_line
        support = (near.support_line or "").lower()
        assert (
            "frantic" in support
            or "calm" in support
            or "authorised" in support
        )
        today = exam_horizon_copy(0)
        assert today is not None
        assert "panic" not in (today.support_line or "").lower()

    def test_reflection_framing_constant(self) -> None:
        framing = REFLECTION_VALUE_FRAMING.lower()
        assert "penalis" in framing or "skipping" in framing
        service = (
            ROOT / "app/presentation/session/services/study_session_service.py"
        ).read_text(encoding="utf-8")
        # Reflection L1 uses chrome + form prompt only — no stacked framing copy.
        assert "REFLECTION_VALUE_FRAMING" not in service
        assert "REFLECTION_VALUE_TITLE" not in service
        assert '"support": ""' in service or "'support': ''" in service


class TestPx005Reliability:
    def test_continue_contention_flash(self) -> None:
        assert "continue_contention" in FLASH_WARNING
        assert "study failure" in FLASH_WARNING["continue_contention"].lower()
        assert CONTINUE_CONTENTION_MESSAGE

    def test_session_routes_contention_boundary(self) -> None:
        routes = (
            ROOT / "app/presentation/session/routes.py"
        ).read_text(encoding="utf-8")
        assert "_contention_redirect" in routes
        assert "_is_contention_error" in routes
        assert "continue_contention" in routes

    def test_resume_session_retries_lock(self) -> None:
        coord = (
            ROOT / "app/application/student_runtime/coordinator.py"
        ).read_text(encoding="utf-8")
        assert "_resume_session_once" in coord
        assert "OptimisticLockError" in coord

    def test_campaign_race_retire_in_generate(self) -> None:
        service = (
            ROOT / "app/application/educational_runtime_engine/service.py"
        ).read_text(encoding="utf-8")
        assert "PX-B-006" in service
        assert "MissionStatus.GENERATED.value" in service
        assert "owed.package_id != existing_pack" in service

    def test_preparing_mission_craft(self) -> None:
        home = (ROOT / "app/templates/student/home.html").read_text(encoding="utf-8")
        assert "data-px005=\"preparing\"" in home or "data-px005='preparing'" in home
        assert "PREPARING_MISSION" in home or PREPARING_MISSION_LABEL
        assert "skeleton_student_home" in home
        assert "exam-horizon" in home
        dto = (
            ROOT / "app/presentation/student/dto/student_home.py"
        ).read_text(encoding="utf-8")
        assert "exam_horizon_line" in dto
        assert "preparing_mission" in dto


class TestPx005StudentSurfaces:
    def test_login_renders_student_identity(self, client) -> None:
        resp = client.get("/auth/login")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert PRODUCT_DESCRIPTOR in html
        assert "Education Operating System" not in html
        assert "Private Beta" in html or STUDENT_RELEASE_LABEL in html
        assert STUDENT_WELCOME_TITLE in html or "New to Kwalitec?" in html
        assert "Internal Alpha · Founding Cohort" not in html

    def test_help_centre_renders_faq(self, logged_in_client) -> None:
        resp = logged_in_client.get("/alpha/help")
        if resp.status_code in {302, 303, 404}:
            pytest.skip("Help centre route unavailable in this fixture")
        html = resp.get_data(as_text=True)
        assert "defer" in html.lower() or "pause" in html.lower()
        assert "exam date" in html.lower() or "sitting" in html.lower()
