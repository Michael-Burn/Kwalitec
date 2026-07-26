#!/usr/bin/env python3
"""RC-001 evidence capture — B7 responsive validation + live B4/B5/B6 checks.

Runs against a local Flask dev server seeded by `seed_rc001.py`. Captures
real screenshots at the 9 required breakpoints for every canonical
student-facing screen, and runs live keyboard/focus/ARIA checks for the
Welcome modal (B4) and navigation drawer (B5).

Usage:
    python capture_rc001.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5099"
OUT = Path(__file__).resolve().parent.parent / "screens"
RESULTS_PATH = Path(__file__).resolve().parent / "results.json"

FULL_EMAIL = "rc001.full@kwalitec.example"
EMPTY_EMAIL = "rc001.empty@kwalitec.example"
PASSWORD = "RC001Evidence!2026"

BREAKPOINTS = [
    ("320", 320, 844),
    ("375", 375, 812),
    ("390", 390, 844),
    ("414", 414, 896),
    ("768", 768, 1024),
    ("820", 820, 1180),
    ("1024", 1024, 1366),
    ("1280", 1280, 800),
    ("1440", 1440, 900),
]

TABLET_MIN = 768
DESKTOP_MIN = 1024


def tier_for(width: int) -> str:
    if width < TABLET_MIN:
        return "mobile"
    if width < DESKTOP_MIN:
        return "tablet"
    return "desktop"


# Canonical screens under SOLE_RUNTIME, grouped by shell.
SCREENS: list[tuple[str, str, str]] = [
    # (name, path, shell)
    ("home", "/student/", "student"),
    ("journey", "/student/journey", "student"),
    ("revision", "/student/revision", "student"),
    ("history", "/student/history", "student"),
    ("profile", "/student/profile", "student"),
    ("study-plan", "/study-plan/", "legacy"),
    ("settings-profile", "/settings/profile", "legacy"),
    ("settings-preferences", "/settings/preferences", "legacy"),
    ("settings-data", "/settings/data", "legacy"),
    ("settings-account-status", "/settings/internal-alpha", "legacy"),
    ("help", "/alpha/help", "legacy"),
]

results: dict = {"breakpoints": {}, "checks": {}, "errors": []}


def log(msg: str) -> None:
    print(msg, flush=True)


def login(page, email: str) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="networkidle")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', PASSWORD)
    with page.expect_navigation(wait_until="networkidle"):
        page.click('button[type="submit"], input[type="submit"]')
    time.sleep(0.2)


def logout(page) -> None:
    page.goto(f"{BASE}/auth/logout", wait_until="networkidle")
    # logout is POST-only; use a direct form submit via JS if GET 405s
    page.evaluate(
        """() => {
            const f = document.querySelector('form[action*="/auth/logout"]');
            if (f) f.submit();
        }"""
    )
    time.sleep(0.2)


def dismiss_welcome(page) -> None:
    modal = page.locator("#welcome-modal")
    if modal.count() and modal.first.is_visible():
        page.locator("[data-welcome-dismiss]").last.click()
        time.sleep(0.2)


def check_horizontal_overflow(page) -> dict:
    return page.evaluate(
        """() => {
            const doc = document.documentElement;
            const body = document.body;
            const scrollW = Math.max(doc.scrollWidth, body.scrollWidth);
            const clientW = doc.clientWidth;
            return {scrollWidth: scrollW, clientWidth: clientW, overflow: scrollW - clientW};
        }"""
    )


def shot(page, name: str) -> str:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.png"
    page.screenshot(path=str(path), full_page=True)
    return str(path.relative_to(OUT.parent))


def capture_breakpoint(browser, label: str, width: int, height: int) -> None:
    tier = tier_for(width)
    log(f"\n=== Breakpoint {label}px ({tier}) ===")
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()
    bp_result: dict = {"tier": tier, "screens": {}}

    login(page, FULL_EMAIL)
    dismiss_welcome(page)

    for name, path, shell in SCREENS:
        try:
            page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=15000)
            dismiss_welcome(page)
            time.sleep(0.15)
            overflow = check_horizontal_overflow(page)
            shot_name = f"{tier}-{label}px-{name}"
            rel = shot(page, shot_name)
            bp_result["screens"][name] = {
                "path": path,
                "shell": shell,
                "status": "ok",
                "overflow_px": overflow["overflow"],
                "screenshot": rel,
            }
            flag = " ⚠ HORIZONTAL OVERFLOW" if overflow["overflow"] > 1 else ""
            log(f"  {name:28s} overflow={overflow['overflow']:>4d}px{flag}")
        except Exception as exc:  # noqa: BLE001
            bp_result["screens"][name] = {"path": path, "status": "error", "error": str(exc)}
            log(f"  {name:28s} ERROR: {exc}")

    # Mobile-only: nav drawer + hamburger touch target (legacy shell only)
    if tier == "mobile":
        page.goto(f"{BASE}/settings/profile", wait_until="networkidle")
        dismiss_welcome(page)
        toggle_box = page.locator("[data-sidebar-toggle]").first.bounding_box()
        bp_result["touch_target_hamburger"] = toggle_box
        if toggle_box:
            min_dim = min(toggle_box["width"], toggle_box["height"])
            flag = " ⚠ BELOW 44px" if min_dim < 44 else ""
            log(f"  hamburger touch target: {min_dim:.0f}px{flag}")

    context.close()
    results["breakpoints"][label] = bp_result


def capture_empty_states(browser) -> None:
    log("\n=== Empty states (rc001.empty account, desktop 1440) ===")
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    login(page, EMPTY_EMAIL)
    # First-time login should land on onboarding (B8)
    onboarding_url = page.url
    shot(page, "onboarding-1440px-onboarding")
    results["checks"]["b8_onboarding_gate"] = {
        "landed_on_onboarding": "/alpha/onboarding" in onboarding_url,
        "url": onboarding_url,
    }
    log(f"  post-login URL: {onboarding_url}")

    # Complete onboarding, then capture empty states
    page.locator('form[action*="/onboarding/complete"] button').click()
    page.wait_for_load_state("networkidle")
    dismiss_welcome(page)

    for name, path, shell in SCREENS:
        if shell != "student":
            continue
        try:
            page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=15000)
            dismiss_welcome(page)
            time.sleep(0.15)
            shot(page, f"desktop-1440px-empty-{name}")
        except Exception as exc:  # noqa: BLE001
            log(f"  empty-{name} ERROR: {exc}")
    context.close()


def arm_welcome_eligibility() -> None:
    """Set ``welcome_eligible=True`` on the full account directly via the app
    context — mirrors what ``WelcomeService.mark_eligible`` does after real
    Study Plan + Calibration completion, without re-running that whole flow
    just to capture the modal for evidence."""
    import os
    import subprocess

    script = (
        "from app import create_app; from app.extensions import db; "
        "from app.models.user import User; "
        "app = create_app(); "
        "app.app_context().push(); "
        f"u = User.query.filter_by(email={FULL_EMAIL!r}).first(); "
        "u.welcome_eligible = True; u.welcome_dismissed = False; "
        "db.session.commit(); "
        "print('armed', u.id)"
    )
    env = dict(os.environ)
    env["DATABASE_URL"] = "sqlite:////tmp/rc001_evidence.sqlite3"
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, env=env
    )
    log(f"  arm_welcome_eligibility: {result.stdout.strip()} {result.stderr.strip()[-300:]}")


def check_welcome_modal_a11y(browser) -> None:
    log("\n=== B4: Welcome modal live focus/keyboard check ===")
    arm_welcome_eligibility()
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    login(page, FULL_EMAIL)
    page.goto(f"{BASE}/student/", wait_until="networkidle")
    modal = page.locator("#welcome-modal")
    check: dict = {"modal_present": modal.count() > 0}
    if modal.count() > 0:
        active_id = page.evaluate("() => document.activeElement.className")
        check["initial_focus_class"] = active_id
        check["focus_on_card"] = "welcome-modal-card" in (active_id or "")

        # Tab through and confirm focus stays within the card
        classes_seen = []
        for _ in range(6):
            page.keyboard.press("Tab")
            cls = page.evaluate(
                "() => document.activeElement.closest('.welcome-modal-card') !== null"
            )
            classes_seen.append(cls)
        check["tab_stayed_trapped"] = all(classes_seen)

        # Escape closes and focus returns. Dismissal is a real form POST
        # (full navigation), so wait for that navigation explicitly rather
        # than racing networkidle against the keydown handler.
        with page.expect_navigation(wait_until="networkidle", timeout=5000):
            page.keyboard.press("Escape")
        check["escape_closed_modal"] = page.locator("#welcome-modal").count() == 0
        check["escape_landed_url"] = page.url
        shot(page, "a11y-b4-after-escape")
    results["checks"]["b4_welcome_modal"] = check
    for k, v in check.items():
        log(f"  {k}: {v}")
    context.close()


def check_nav_drawer_a11y(browser) -> None:
    log("\n=== B5: Nav drawer live focus/keyboard/ARIA check ===")
    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()
    login(page, FULL_EMAIL)
    dismiss_welcome(page)
    page.goto(f"{BASE}/settings/profile", wait_until="networkidle")

    toggle = page.locator("[data-sidebar-toggle]").first
    check: dict = {}
    check["aria_expanded_before"] = toggle.get_attribute("aria-expanded")
    check["aria_controls"] = toggle.get_attribute("aria-controls")

    toggle.click()
    time.sleep(0.3)
    check["aria_expanded_after_open"] = toggle.get_attribute("aria-expanded")
    sidebar_role = page.locator("#app-sidebar").get_attribute("role")
    check["sidebar_role_when_open"] = sidebar_role
    active_in_sidebar = page.evaluate(
        "() => document.activeElement.closest('#app-sidebar') !== null"
    )
    check["focus_entered_drawer"] = active_in_sidebar
    shot(page, "a11y-b5-drawer-open")

    # Tab trap check
    trapped = []
    for _ in range(10):
        page.keyboard.press("Tab")
        inside = page.evaluate(
            "() => document.activeElement.closest('#app-sidebar') !== null"
        )
        trapped.append(inside)
    check["tab_stayed_trapped"] = all(trapped)

    page.keyboard.press("Escape")
    time.sleep(0.2)
    check["aria_expanded_after_escape"] = toggle.get_attribute("aria-expanded")
    focus_returned = page.evaluate(
        "(sel) => document.activeElement === document.querySelector(sel)",
        "[data-sidebar-toggle]",
    )
    check["focus_returned_to_toggle"] = focus_returned
    results["checks"]["b5_nav_drawer"] = check
    for k, v in check.items():
        log(f"  {k}: {v}")
    context.close()


def check_b9_b10(browser) -> None:
    log("\n=== B9/B10: legacy settings redirect + internal language ===")
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    login(page, FULL_EMAIL)
    dismiss_welcome(page)

    resp = page.goto(f"{BASE}/settings/", wait_until="networkidle")
    check = {
        "settings_index_final_url": page.url,
        "redirected_to_profile": "/student/profile" in page.url,
        "settings_index_status": resp.status if resp else None,
    }

    page.goto(f"{BASE}/settings/internal-alpha", wait_until="networkidle")
    body = page.content()
    check["account_status_heading_present"] = "Account Status" in body
    check["learning_profile_status_absent"] = "Learning profile status" not in body
    check["personalised_recommendations_present"] = "Personalised recommendations" in body
    shot(page, "b10-settings-account-status")
    results["checks"]["b9_b10"] = check
    for k, v in check.items():
        log(f"  {k}: {v}")
    context.close()


REFLECTION_NOTE_TEXT = "I still find deferred tax tricky — need another pass."


# NOTE: this is a comma-separated selector *list*. Interpolating it directly
# after a descendant combinator (e.g. f'form[...] {SUBMIT_SELECTOR}') silently
# breaks scoping — CSS parses "A B, C" as two independent selectors ("A B" and
# unscoped "C"), so the raw string must always be wrapped in :is(...) when
# combined with an ancestor selector.
SUBMIT_SELECTOR = 'button[type="submit"], input[type="submit"]'
SUBMIT_IN = f":is({SUBMIT_SELECTOR})"


def walk_session_to_reflection(page, max_steps: int = 12) -> bool:
    """Drive the real session flow (Overview -> Activity* -> Reflection) via
    the rendered UI, submitting placeholder answers as needed. Session forms
    render WTForms ``SubmitField``s as ``<input type="submit">``, not
    ``<button>``, so every selector here checks both."""
    for _ in range(max_steps):
        if "/reflection" in page.url:
            return True
        begin = page.locator(f'form[action$="/begin"] {SUBMIT_IN}')
        if begin.count() > 0 and begin.first.is_visible():
            begin.first.click()
            page.wait_for_load_state("networkidle")
            continue
        textarea = page.locator("textarea.session-textarea")
        if textarea.count() > 0 and textarea.first.is_visible():
            textarea.first.fill("Evidence-capture placeholder answer.")
            page.locator(f"form.session-answer-form {SUBMIT_IN}").first.click()
            page.wait_for_load_state("networkidle")
            continue
        advance = page.locator(f'form[action*="/advance"] {SUBMIT_IN}')
        if advance.count() > 0 and advance.first.is_visible():
            advance.first.click()
            page.wait_for_load_state("networkidle")
            continue
        break
    return "/reflection" in page.url


def check_session_flow(browser) -> None:
    log("\n=== B1/B3: Session flow -> Reflection screen + duration ===")
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()
    login(page, FULL_EMAIL)
    dismiss_welcome(page)
    page.goto(f"{BASE}/student/", wait_until="networkidle")
    dismiss_welcome(page)
    start = page.locator(
        f'form[action*="/session/start"] {SUBMIT_IN}, form[action*="/student/session"] {SUBMIT_IN}'
    )
    check: dict = {"start_cta_present": start.count() > 0}
    if start.count() > 0 and start.first.is_enabled():
        start.first.click()
        page.wait_for_load_state("networkidle")
        shot(page, "session-1440px-overview")
        check["overview_url"] = page.url

        reached = walk_session_to_reflection(page)
        check["reached_reflection"] = reached
        if reached:
            shot(page, "session-1440px-reflection")
            note_field = page.locator("#reflection_note, textarea[name='reflection_note']")
            if note_field.count() > 0:
                note_field.first.fill(REFLECTION_NOTE_TEXT)
                shot(page, "session-1440px-reflection-filled")
                page.locator(f'form[action*="/reflection/continue"] {SUBMIT_IN}').first.click()
                page.wait_for_load_state("networkidle")
                check["post_reflection_url"] = page.url
                shot(page, "session-1440px-summary")
    results["checks"]["session_flow"] = check
    for k, v in check.items():
        log(f"  {k}: {v}")
    context.close()


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for label, width, height in BREAKPOINTS:
            capture_breakpoint(browser, label, width, height)
        capture_empty_states(browser)
        check_welcome_modal_a11y(browser)
        check_nav_drawer_a11y(browser)
        check_b9_b10(browser)
        check_session_flow(browser)
        browser.close()

    RESULTS_PATH.write_text(json.dumps(results, indent=2, default=str))
    log(f"\nResults written to {RESULTS_PATH}")
    log(f"Screenshots in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
