"""PX-006 — Premium Experience Phase 4 (WS-09 Performance · WS-10 Premium Moments)."""

from __future__ import annotations

from pathlib import Path

from app.application.student_experience.student_microcopy import (
    CF_MILESTONE_ACK_CONTINUITY,
    DILIGENCE_EMPTY_STREAK,
    ERROR_REFERENCE_GUIDANCE,
    ERROR_REFERENCE_LABEL,
    PREFERENCE_APPEARANCE_STICKY,
    PREFERENCE_STUDY_SESSION_SCOPE,
    SESSION_COMPLETE_SUPPORT,
    SKELETON_MISSION_LABEL,
    SKELETON_PLAN_LABEL,
    continuity_front_milestone_ack,
    diligence_reinforcement_copy,
)

ROOT = Path(__file__).resolve().parents[3]


class TestPx006SkeletonCoherence:
    def test_skeleton_macros_exist(self) -> None:
        skel = (ROOT / "app/templates/partials/skeleton.html").read_text(
            encoding="utf-8"
        )
        assert "skeleton_student_home" in skel
        assert "skeleton_mission_hero" in skel
        assert "skeleton_study_plan" in skel
        assert "skeleton_nav_pending" in skel
        assert 'data-px006="skeleton-home"' in skel
        assert 'data-px006="skeleton-mission"' in skel
        assert 'data-px006="skeleton-plan"' in skel

    def test_home_preparing_wires_skeleton(self) -> None:
        home = (ROOT / "app/templates/student/home.html").read_text(encoding="utf-8")
        assert "skeleton_student_home" in home
        assert 'data-px006="skeleton-home"' in home

    def test_plan_surface_wires_skeleton_ref(self) -> None:
        plan = (ROOT / "app/templates/study_plan/list.html").read_text(
            encoding="utf-8"
        )
        assert 'data-px006="plan-surface"' in plan
        assert "skeleton_study_plan" in plan
        assert SKELETON_PLAN_LABEL

    def test_session_mission_surface_marker(self) -> None:
        body = (
            ROOT / "app/templates/session/partials/session_body.html"
        ).read_text(encoding="utf-8")
        assert 'data-px006="mission-surface"' in body
        assert "skeleton_mission_hero" in body
        assert SKELETON_MISSION_LABEL

    def test_eos_shell_nav_skeleton(self) -> None:
        eos = (ROOT / "app/templates/layouts/eos_student.html").read_text(
            encoding="utf-8"
        )
        assert "skeleton_nav_pending" in eos
        assert "defer" in eos


class TestPx006PerformanceBaseline:
    def test_student_css_asset_budget(self) -> None:
        """Perceived-performance hygiene: student CSS stays disciplined."""
        student_css = ROOT / "app/static/css/student/student.css"
        tokens = ROOT / "app/static/css/tokens.css"
        size = student_css.stat().st_size + tokens.stat().st_size
        # Soft budget — document in evidence; fail only on runaway bloat.
        assert size < 450_000, f"student+tokens CSS too large: {size}"

    def test_optimistic_nav_covers_primary_ctas(self) -> None:
        js = (ROOT / "app/static/js/student.js").read_text(encoding="utf-8")
        assert "ds-btn--primary" in js
        assert "data-nav-pending" in js
        assert "data-student-cta" in js

    def test_house_motion_tokens(self) -> None:
        tokens = (ROOT / "app/static/css/tokens.css").read_text(encoding="utf-8")
        assert "--motion-page-enter" in tokens
        assert "--motion-success-in" in tokens
        assert "--motion-disclosure" in tokens
        assert "kw-motion-page" in tokens
        assert "kw-motion-success" in tokens
        assert "prefers-reduced-motion" in tokens


class TestPx006MotionSystem:
    def test_reduced_motion_honoured_in_student_css(self) -> None:
        css = (ROOT / "app/static/css/student/student.css").read_text(
            encoding="utf-8"
        )
        assert "prefers-reduced-motion" in css
        assert "data-nav-pending" in css

    def test_completion_uses_success_reward(self) -> None:
        body = (
            ROOT / "app/templates/session/partials/session_body.html"
        ).read_text(encoding="utf-8")
        # Session redesign: calm honest completion, not celebration theatre.
        assert "data-completion-what-happened" in body
        assert "data-session-milestone" in body
        assert 'data-px006="celebration"' not in body


class TestPx006PremiumMoments:
    def test_icon_default_stroke(self) -> None:
        icons = (ROOT / "app/templates/partials/icons.html").read_text(
            encoding="utf-8"
        )
        assert "stroke_width=1.75" in icons
        assert "icon-btn" in (
            ROOT / "app/static/css/tokens.css"
        ).read_text(encoding="utf-8")

    def test_appearance_icon_only_language(self) -> None:
        switcher = (
            ROOT / "app/templates/partials/appearance_switcher.html"
        ).read_text(encoding="utf-8")
        assert "icon-btn" in switcher
        assert 'data-px006="icon-only"' in switcher
        assert "icon(" in switcher

    def test_error_reference_guidance(self) -> None:
        assert ERROR_REFERENCE_LABEL == "Reference ID"
        assert "Copy this ID" in ERROR_REFERENCE_GUIDANCE
        for name in ("404.html", "500.html", "403.html"):
            html = (ROOT / "app/templates/errors" / name).read_text(
                encoding="utf-8"
            )
            assert "ERROR_REFERENCE_GUIDANCE" in html
            assert 'data-px006="error-reference"' in html
            assert "error-reference" in html

    def test_error_reference_css_tokenised(self) -> None:
        css = (ROOT / "app/static/css/app.css").read_text(encoding="utf-8")
        assert ".error-reference" in css
        assert "--text-secondary" in css or "text-secondary" in css

    def test_login_lockup_led(self) -> None:
        login = (ROOT / "app/templates/auth/login.html").read_text(
            encoding="utf-8"
        )
        assert 'data-px006="login-lockup"' in login
        assert "do not repeat product_name" in login
        # Sign-in card title is "Sign in", not a second Kwalitec wordmark.
        assert 'landing-card-title">Sign in' in login

    def test_legacy_celebration_demotes_research(self) -> None:
        recorded = (
            ROOT / "app/templates/mission/session_recorded.html"
        ).read_text(encoding="utf-8")
        assert 'data-px006="celebration-primary"' in recorded
        assert "Return Home" in recorded
        # Research check-in must not be the primary mark-complete CTA.
        primary_idx = recorded.index('data-px006="celebration-primary"')
        research_idx = recorded.index("research.checkin")
        assert primary_idx < research_idx
        assert "Optional product feedback" in recorded

    def test_cf_milestone_ack_copy(self) -> None:
        ack = continuity_front_milestone_ack("Continuity Front · Day 3")
        assert ack == CF_MILESTONE_ACK_CONTINUITY
        assert "pass" not in ack.lower() or "no pass" in ack.lower()
        mem = continuity_front_milestone_ack("Memory Front CP-D1")
        assert mem is not None
        assert "pass rate" not in (mem or "").lower()
        assert continuity_front_milestone_ack("Random topic") is None

    def test_diligence_without_punishment(self) -> None:
        empty = diligence_reinforcement_copy(
            days_since_last=0, streak_days=0
        )
        assert empty.streak_empty_label == DILIGENCE_EMPTY_STREAK
        assert empty.support_line
        assert "broken" not in (empty.support_line or "").lower()
        assert "lost" not in (empty.support_line or "").lower()
        gap = diligence_reinforcement_copy(days_since_last=5)
        assert gap.support_line
        assert "penalis" not in gap.support_line.lower()
        macros = (
            ROOT / "app/templates/design_system/macros.html"
        ).read_text(encoding="utf-8")
        assert "Streak" in macros
        assert "Study streak" not in macros
        assert "don't break" not in macros.lower()
        assert "Recent study rhythm" not in macros

    def test_preference_stickiness_copy(self) -> None:
        settings = (
            ROOT / "app/templates/settings/index.html"
        ).read_text(encoding="utf-8")
        assert "PREFERENCE_APPEARANCE_STICKY" in settings
        assert "PREFERENCE_STUDY_SESSION_SCOPE" in settings
        assert "saved in this browser" in PREFERENCE_APPEARANCE_STICKY.lower()
        assert "signed-in session" in PREFERENCE_STUDY_SESSION_SCOPE.lower()
        theme = (ROOT / "app/static/js/theme.js").read_text(encoding="utf-8")
        assert "kwalitec-appearance" in theme
        assert "appearancechange" in theme

    def test_home_wires_milestone_and_diligence(self) -> None:
        home = (ROOT / "app/templates/student/home.html").read_text(
            encoding="utf-8"
        )
        assert 'data-px006="cf-milestone"' in home
        assert 'data-px006="diligence"' in home
        assert 'data-px006="day-complete"' in home
        dto = (
            ROOT / "app/presentation/student/dto/student_home.py"
        ).read_text(encoding="utf-8")
        assert "milestone_acknowledgement" in dto
        assert "diligence_line" in dto


class TestPx006StudentSurfaces:
    def test_login_renders(self, client) -> None:
        response = client.get("/auth/login")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'data-px006="login-lockup"' in html
        assert "Sign in" in html

    def test_error_404_guidance(self, client) -> None:
        response = client.get("/this-route-definitely-missing-px006")
        assert response.status_code == 404
        html = response.get_data(as_text=True)
        assert ERROR_REFERENCE_LABEL in html or "Reference ID" in html
        assert (
            "Copy this ID" in html
            or "contact support" in html.lower()
        )

    def test_icon_sourcing_deferred(self) -> None:
        """PX-B-051 Future: macro foundation exists; full migration deferred."""
        icons = (ROOT / "app/templates/partials/icons.html").read_text(
            encoding="utf-8"
        )
        assert "PX-002B" in icons or "Shared icon source" in icons
