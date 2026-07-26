"""RC-001 accessibility regression tests (B4, B5, B6).

These tests assert the server-rendered ARIA contract for the Welcome dialog
and the navigation drawer. Focus-trap/focus-return *behaviour* lives in
JavaScript (``app/static/js/app.js``) and is evidenced separately in
``knowledge/product/rc001/ACCESSIBILITY_VALIDATION.md`` via a Playwright
keyboard-navigation harness, since this project has no in-repo JS test
runner. What we can and must assert here is that the markup the browser
receives carries the attributes that JS behaviour depends on.

B4's own dialog-markup coverage lives in
``tests/presentation/student/test_accessibility.py`` (the canonical
``student/`` shell — see that file's ``TestWelcomeModalOnCanonicalStudentHome``
for why ``/dashboard/`` is not the right target for that assertion). The
nav-drawer (B5) checks below use ``/settings/profile`` rather than
``/dashboard/``: both render the same ``partials/sidebar.html`` +
``partials/topnav.html`` chrome via ``layouts/base.html``, but
``/dashboard/`` currently 302s in this branch for reasons unrelated to
RC-001 (pre-existing legacy-dashboard template WIP, out of B1-B10 scope).
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_CSS = (ROOT / "app" / "static" / "css" / "app.css").read_text()


class TestTouchTargets:
    """B7 — PX-003 flagged the icon-only appearance-switcher buttons at
    <=575.98px as a "plausible" (unconfirmed) mobile failure candidate.
    Live Playwright measurement at 375px confirmed it: 36.375x36.375px,
    below --touch-target-min (44px). Fixed by applying the token inside the
    existing narrow-width media query; this test locks that in.
    """

    def test_appearance_option_meets_touch_target_min_at_mobile_width(self):
        assert (
            ".appearance-option{padding:0.45rem;"
            "min-width:var(--touch-target-min, 2.75rem);"
            "min-height:var(--touch-target-min, 2.75rem);"
            "justify-content:center;}"
        ) in APP_CSS


class TestNavigationDrawerAccessibility:
    """B5 — nav drawer aria-expanded / aria-controls scaffolding.

    The toggle's aria-expanded state itself flips at runtime (JS), but the
    static attributes it depends on — an id on the drawer to point
    aria-controls at, and an aria-label on the toggle — must be present in
    every server response.
    """

    def test_toggle_has_label_and_controls_target(self, logged_in_client):
        body = logged_in_client.get("/settings/profile").get_data(as_text=True)
        assert "data-sidebar-toggle" in body
        assert 'aria-label="Toggle navigation"' in body
        assert 'id="app-sidebar"' in body

    def test_sidebar_backdrop_present_for_close_on_outside_click(
        self, logged_in_client
    ):
        body = logged_in_client.get("/settings/profile").get_data(as_text=True)
        assert "data-sidebar-close" in body
