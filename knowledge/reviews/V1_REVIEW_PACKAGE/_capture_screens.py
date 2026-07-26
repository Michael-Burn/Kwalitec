#!/usr/bin/env python3
"""Capture student-visible screenshots for the V1 blind review package.

Uses the running local app. Does not modify application code.
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5055"
OUT = Path(__file__).resolve().parent / "screens"
EMAIL = "v1.review@kwalitec.example"
PASSWORD = "ReviewPackage2026!"
EMPTY_EMAIL = "v1.empty@kwalitec.example"
VIEWPORT = {"width": 1440, "height": 900}


def shot(page, name: str, *, full_page: bool = True) -> None:
    path = OUT / f"{name}.png"
    page.screenshot(path=str(path), full_page=full_page)
    print(f"OK {name} -> {path.name}")


def login(page, email: str, password: str) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="networkidle")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    with page.expect_navigation(wait_until="networkidle"):
        page.click('input[name="submit"], input[type="submit"]')
    time.sleep(0.4)
    if "/auth/login" in page.url:
        raise RuntimeError(f"Login failed for {email}; still on {page.url}")


def logout(page) -> None:
    # Prefer sidebar sign-out form if present
    form = page.locator('form[action*="/auth/logout"]')
    if form.count():
        form.first.locator('button[type="submit"]').click()
        page.wait_for_load_state("networkidle")
        return
    page.goto(f"{BASE}/auth/logout", wait_until="networkidle")


def dismiss_welcome_if_present(page) -> None:
    modal = page.locator("#welcomeModal, .welcome-modal, [data-welcome-modal]")
    if modal.count() and modal.first.is_visible():
        dismiss = page.locator(
            'button:has-text("Explore"), button:has-text("Got it"), '
            'button:has-text("Dismiss"), [data-bs-dismiss="modal"]'
        )
        if dismiss.count():
            dismiss.first.click()
            time.sleep(0.3)


def capture_errors(page) -> None:
    page.goto(f"{BASE}/this-page-does-not-exist-v1-review", wait_until="networkidle")
    shot(page, "error-404")

    # 403 is harder without privilege; attempt a console path as student
    page.goto(f"{BASE}/console/", wait_until="networkidle")
    # May redirect or 403
    shot(page, "error-or-denied-console")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=2,
            color_scheme="light",
        )
        page = context.new_page()
        page.set_default_timeout(20000)

        # --- Auth ---
        page.goto(f"{BASE}/auth/login", wait_until="networkidle")
        shot(page, "01-login")

        # Invalid credentials flash
        page.fill('input[name="email"]', "nobody@example.com")
        page.fill('input[name="password"]', "wrong-password")
        page.click('button[type="submit"], input[type="submit"]')
        page.wait_for_load_state("networkidle")
        time.sleep(0.3)
        shot(page, "01b-login-invalid")

        # Successful login
        login(page, EMAIL, PASSWORD)
        dismiss_welcome_if_present(page)
        shot(page, "02-post-login-landing")

        # --- Core student screens ---
        for path, name in [
            ("/dashboard/", "03-dashboard-legacy"),
            ("/student/", "04-dashboard-student"),
            ("/student/journey", "05-journey"),
            ("/student/revision", "06-revision"),
            ("/student/history", "07-history-analytics"),
            ("/student/profile", "08-settings-profile-student"),
            ("/missions/", "09-mission"),
            ("/analytics/", "10-analytics-legacy"),
            ("/settings/", "11-settings-general"),
            ("/settings/profile", "12-settings-profile"),
            ("/settings/preferences", "13-settings-preferences"),
            ("/settings/data", "14-settings-data"),
            ("/settings/internal-alpha", "15-settings-internal-alpha"),
            ("/study-plan/", "16-study-plan"),
            ("/study-plan/plans/all", "17-study-plan-list"),
            ("/alpha/help", "18-help"),
            ("/alpha/onboarding", "19-onboarding"),
            ("/research/checkin?source=settings", "20-product-checkin"),
            ("/alpha/feedback/mission-helpful", "21-feedback-mission-helpful"),
            ("/alpha/feedback/explanation-clear", "22-feedback-explanation-clear"),
            ("/alpha/feedback/report-problem", "23-feedback-report-problem"),
            ("/alpha/feedback/suggest", "24-feedback-suggest"),
        ]:
            page.goto(f"{BASE}{path}", wait_until="networkidle")
            dismiss_welcome_if_present(page)
            time.sleep(0.35)
            shot(page, name)

        # Navigation chrome close-ups (viewport only)
        page.goto(f"{BASE}/dashboard/", wait_until="networkidle")
        dismiss_welcome_if_present(page)
        shot(page, "25-navigation-sidebar", full_page=False)

        page.goto(f"{BASE}/student/", wait_until="networkidle")
        shot(page, "26-navigation-student", full_page=False)
        # Coach panel is on student home — crop via full page already; alias
        shot(page, "27-coach-panel-on-dashboard")

        # Study plan wizard steps (may redirect if plan exists — open wizard step URLs)
        for step in range(1, 8):
            page.goto(f"{BASE}/study-plan/wizard/{step}", wait_until="networkidle")
            time.sleep(0.25)
            shot(page, f"28-wizard-step-{step}")

        page.goto(f"{BASE}/study-plan/review", wait_until="networkidle")
        shot(page, "29-wizard-review")

        # Active plan view — discover id from list page
        page.goto(f"{BASE}/study-plan/plans/all", wait_until="networkidle")
        hrefs = page.eval_on_selector_all(
            'a[href*="/study-plan/"]',
            "els => els.map(e => e.getAttribute('href'))",
        )
        plan_ids = []
        for h in hrefs or []:
            m = re.search(r"/study-plan/(\d+)(?:/|$)", h or "")
            if m:
                plan_ids.append(m.group(1))
        if plan_ids:
            pid = plan_ids[0]
            page.goto(f"{BASE}/study-plan/{pid}", wait_until="networkidle")
            shot(page, "30-study-plan-view")
            page.goto(f"{BASE}/study-plan/{pid}/edit", wait_until="networkidle")
            shot(page, "31-study-plan-edit")
            page.goto(f"{BASE}/calibration/after-plan/{pid}", wait_until="networkidle")
            shot(page, "32-calibration")

        # Mission session flow (legacy)
        page.goto(f"{BASE}/missions/", wait_until="networkidle")
        start = page.locator(
            'form[action*="/session/start"] button, button:has-text("Start"), '
            'a:has-text("Open session"), a:has-text("Continue")'
        )
        if start.count():
            # Prefer POST start if form exists
            form = page.locator('form[action*="/session/start"]')
            if form.count():
                form.first.locator("button").click()
            else:
                start.first.click()
            page.wait_for_load_state("networkidle")
            time.sleep(0.4)
            shot(page, "33-mission-session")
            # Try finish / practice outcome
            finish = page.locator(
                'a:has-text("Finish"), button:has-text("Finish"), '
                'a[href*="finish"], form[action*="finish"] button'
            )
            if finish.count():
                finish.first.click()
                page.wait_for_load_state("networkidle")
                time.sleep(0.3)
                shot(page, "34-mission-practice-outcome")

        # Student session experience
        page.goto(f"{BASE}/student/", wait_until="networkidle")
        cta = page.locator('form[action*="/student/session/start"] button')
        session_id = None
        if cta.count() and cta.first.is_enabled():
            cta.first.click()
            page.wait_for_load_state("networkidle")
            time.sleep(0.5)
            m = re.search(r"/session/([^/]+)/", page.url)
            if m:
                session_id = m.group(1)
            shot(page, "35-session-overview")

            begin = page.locator('form[action*="/begin"] button, button:has-text("Begin")')
            if begin.count() and begin.first.is_enabled():
                begin.first.click()
                page.wait_for_load_state("networkidle")
                time.sleep(0.4)
            shot(page, "36-session-activity")

            # Try to reach reflection/summary/complete via URL if we have id
            if session_id:
                for surface, name in [
                    ("reflection", "37-session-reflection"),
                    ("summary", "38-session-summary"),
                    ("complete", "39-session-complete"),
                ]:
                    page.goto(
                        f"{BASE}/session/{session_id}/{surface}",
                        wait_until="networkidle",
                    )
                    time.sleep(0.3)
                    shot(page, name)

        # Success / flash — preferences save
        page.goto(f"{BASE}/settings/preferences", wait_until="networkidle")
        save = page.locator('button[type="submit"], input[type="submit"]')
        if save.count():
            save.first.click()
            page.wait_for_load_state("networkidle")
            time.sleep(0.3)
            shot(page, "40-settings-save-success")

        # Dialogs / confirmations — delete confirm if present on plan list
        page.goto(f"{BASE}/study-plan/plans/all", wait_until="networkidle")
        shot(page, "41-study-plan-list-actions")

        # Empty states with empty user
        logout(page)
        login(page, EMPTY_EMAIL, PASSWORD)
        dismiss_welcome_if_present(page)
        for path, name in [
            ("/dashboard/", "42-empty-dashboard"),
            ("/missions/", "43-empty-mission"),
            ("/student/", "44-empty-student-home"),
            ("/student/journey", "45-empty-journey"),
            ("/student/revision", "46-empty-revision"),
            ("/student/history", "47-empty-history"),
            ("/analytics/", "48-empty-analytics"),
            ("/study-plan/wizard/1", "49-empty-wizard-start"),
        ]:
            page.goto(f"{BASE}{path}", wait_until="networkidle")
            dismiss_welcome_if_present(page)
            time.sleep(0.3)
            shot(page, name)

        # Subject support gate — wizard step 2 coming soon
        page.goto(f"{BASE}/study-plan/wizard/1", wait_until="networkidle")
        # Select IFoA if possible and continue
        ifoa = page.locator('input[value*="IFoA"], button:has-text("IFoA"), label:has-text("IFoA")')
        if ifoa.count():
            ifoa.first.click()
            nxt = page.locator('button[type="submit"], button:has-text("Next")')
            if nxt.count():
                nxt.first.click()
                page.wait_for_load_state("networkidle")
                time.sleep(0.3)
                shot(page, "50-wizard-subject-support")

        # Errors
        capture_errors(page)

        # Appearance / topnav
        login(page, EMAIL, PASSWORD)
        page.goto(f"{BASE}/dashboard/", wait_until="networkidle")
        dismiss_welcome_if_present(page)
        # Toggle dark if switcher exists
        dark = page.locator(
            '[data-theme="dark"], button:has-text("Dark"), '
            '[aria-label*="Dark"], [data-appearance="dark"]'
        )
        if dark.count():
            dark.first.click()
            time.sleep(0.4)
            shot(page, "51-theme-dark")
            light = page.locator(
                '[data-theme="light"], button:has-text("Light"), '
                '[aria-label*="Light"], [data-appearance="light"]'
            )
            if light.count():
                light.first.click()
                time.sleep(0.3)

        # Thank you page after check-in if reachable
        page.goto(f"{BASE}/research/thank-you", wait_until="networkidle")
        shot(page, "52-research-thank-you")

        # Recorded / feedback after mission if route works with known mission
        page.goto(f"{BASE}/missions/15/session/recorded", wait_until="networkidle")
        shot(page, "53-mission-session-recorded")

        browser.close()

    print(f"\nCaptured {len(list(OUT.glob('*.png')))} screenshots in {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
