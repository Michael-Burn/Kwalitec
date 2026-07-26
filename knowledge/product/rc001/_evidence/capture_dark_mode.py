#!/usr/bin/env python3
"""RC-001 evidence capture — dark mode + light mode side-by-side.

theme.js resolves ``data-theme`` from ``prefers-color-scheme`` (with a
stored override once a student picks one explicitly), so Playwright's
``color_scheme`` context option drives the same code path a real browser
would use for an OS-level dark-mode preference.
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5099"
OUT = Path(__file__).resolve().parent.parent / "screens"
FULL_EMAIL = "rc001.full@kwalitec.example"
PASSWORD = "RC001Evidence!2026"

SCREENS = [
    ("home", "/student/"),
    ("reflection", "/session/sess-1/overview"),  # overview shares session shell styling
    ("settings-account-status", "/settings/internal-alpha"),
    ("study-plan", "/study-plan/"),
]


def login(page) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="networkidle")
    page.fill('input[name="email"]', FULL_EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    with page.expect_navigation(wait_until="networkidle"):
        page.click('button[type="submit"], input[type="submit"]')


def dismiss_welcome(page) -> None:
    modal = page.locator("#welcome-modal")
    if modal.count() and modal.first.is_visible():
        page.locator("[data-welcome-dismiss]").last.click()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for scheme in ("light", "dark"):
            context = browser.new_context(
                viewport={"width": 1440, "height": 900}, color_scheme=scheme
            )
            page = context.new_page()
            login(page)
            dismiss_welcome(page)
            for name, path in SCREENS:
                page.goto(f"{BASE}{path}", wait_until="networkidle")
                dismiss_welcome(page)
                data_theme = page.evaluate(
                    "() => document.documentElement.getAttribute('data-theme')"
                )
                shot = OUT / f"{scheme}-1440px-{name}.png"
                page.screenshot(path=str(shot), full_page=True)
                print(f"{scheme:5s} {name:26s} data-theme={data_theme} -> {shot.name}")
            context.close()
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
