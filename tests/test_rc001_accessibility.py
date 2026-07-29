"""RC-001 accessibility regression tests (B4, B5, B6).

These tests assert the server-rendered ARIA contract for the Welcome dialog
and the navigation chrome. Focus-trap/focus-return *behaviour* lives in
JavaScript (``app/static/js/app.js``) and is evidenced separately in
``knowledge/product/rc001/ACCESSIBILITY_VALIDATION.md`` via a Playwright
keyboard-navigation harness, since this project has no in-repo JS test
runner. What we can and must assert here is that the markup the browser
receives carries the attributes that JS behaviour depends on.

B4's own dialog-markup coverage lives in
``tests/presentation/student/test_accessibility.py`` (the canonical
``student/`` shell — see that file's ``TestWelcomeModalOnCanonicalStudentHome``
for why ``/dashboard/`` is not the right target for that assertion).

RC-2026.07.29-03: authenticated Student chrome is the EOS topbar + compact
mobile Menu toggle (not the retired legacy sidebar drawer).
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_CSS = (ROOT / "app" / "static" / "css" / "app.css").read_text()
STUDENT_CSS = (
    ROOT / "app" / "static" / "css" / "student" / "student.css"
).read_text()


class TestTouchTargets:
    """B7 — appearance option hit targets meet --touch-target-min at mobile."""

    def test_appearance_option_meets_touch_target_min_at_mobile_width(self):
        assert (
            ".appearance-option{padding:0.45rem;"
            "min-width:var(--touch-target-min, 2.75rem);"
            "min-height:var(--touch-target-min, 2.75rem);"
            "justify-content:center;}"
        ) in APP_CSS
        assert "min-width: var(--touch-target-min, 2.75rem)" in STUDENT_CSS
        assert "min-height: var(--touch-target-min, 2.75rem)" in STUDENT_CSS


class TestNavigationDrawerAccessibility:
    """B5 — EOS compact mobile nav aria scaffolding (RC-2026.07.29-03)."""

    def test_toggle_has_label_and_controls_target(self, logged_in_client):
        body = logged_in_client.get("/settings/profile").get_data(as_text=True)
        assert "student-shell" in body
        assert "data-student-nav-toggle" in body
        assert 'aria-controls="student-nav-list"' in body
        assert 'aria-label="Student experience"' in body
        assert 'id="app-sidebar"' not in body

    def test_sidebar_backdrop_retired_with_legacy_shell(self, logged_in_client):
        body = logged_in_client.get("/settings/profile").get_data(as_text=True)
        assert "data-sidebar-close" not in body
        assert "student-nav" in body
