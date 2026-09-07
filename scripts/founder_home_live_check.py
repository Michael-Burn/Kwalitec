"""Founder Home live-rendering check (Wave 1 and later waves).

The original Wave 1 founder walk matched the literal button text
``Start Session`` and sampled ``body.inner_text()[:80]``. Home's primary
CTA is ``Start Today's Session``, and the first 80 characters of the page
are navigation chrome (including the ``Choose Exam`` nav link). Those two
predicates produced a false report that the founder account could not
start a session.

This check uses the durable Home contracts instead:
- ``data-session-control="start"`` (or ``resume``) for a session CTA
- ``data-workspace-section="todays-mission"`` for mission hero content
- ``data-student-state="empty"`` for a genuine empty Home

CTA copy is recorded for diagnosis only. It is never the matcher.

Usage (local app already running)::

    python scripts/founder_home_live_check.py
    python scripts/founder_home_live_check.py --base-url http://127.0.0.1:5001
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]

STARTABLE_SELECTOR = '[data-session-control="start"]'
RESUMABLE_SELECTOR = '[data-session-control="resume"]'
MISSION_HERO_SELECTOR = '[data-workspace-section="todays-mission"]'
EMPTY_STATE_SELECTOR = '[data-student-state="empty"]'
HOME_SURFACE_SELECTOR = '[data-home="decision-surface"]'
PRIMARY_CTA_SELECTOR = '[data-student-cta="primary"]'


class _HomeSignalParser(HTMLParser):
    """Collect Home session-control signals from markup."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.session_controls: list[str] = []
        self.empty_state = False
        self.has_mission_hero = False
        self.has_home_surface = False
        self.primary_labels: list[str] = []
        self._capture_primary = False
        self._primary_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: (value or "") for key, value in attrs}
        control = data.get("data-session-control", "").strip()
        if control:
            self.session_controls.append(control)
        if data.get("data-student-state") == "empty":
            self.empty_state = True
        if data.get("data-workspace-section") == "todays-mission":
            self.has_mission_hero = True
        if data.get("data-home") == "decision-surface":
            self.has_home_surface = True
        if data.get("data-student-cta") == "primary":
            self._capture_primary = True
            self._primary_chunks = []

    def handle_data(self, data: str) -> None:
        if self._capture_primary:
            self._primary_chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._capture_primary and tag in {"button", "a"}:
            label = "".join(self._primary_chunks).strip()
            if label:
                self.primary_labels.append(label)
            self._capture_primary = False
            self._primary_chunks = []


def verdict_from_signals(
    *,
    session_controls: list[str],
    empty_state: bool,
    has_mission_hero: bool,
    has_home_surface: bool = False,
    primary_labels: list[str] | None = None,
    mission_hero_text: str = "",
) -> dict[str, Any]:
    """Turn Home data-attribute signals into a startable-session verdict."""
    has_start = "start" in session_controls
    has_resume = "resume" in session_controls
    can_enter = (has_start or has_resume) and not empty_state
    if empty_state and not can_enter:
        status = "empty"
    elif has_start:
        status = "startable"
    elif has_resume:
        status = "resumable"
    elif has_mission_hero:
        status = "mission_without_session_control"
    else:
        status = "no_session_control"
    labels = [label.replace("→", "").strip() for label in (primary_labels or [])]
    return {
        "status": status,
        "startable": has_start and not empty_state,
        "can_enter_session": can_enter,
        "session_control": (
            "start" if has_start else ("resume" if has_resume else None)
        ),
        "empty_state": empty_state,
        "has_mission_hero": has_mission_hero,
        "has_home_surface": has_home_surface,
        "primary_labels": labels,
        "mission_hero_text": mission_hero_text.strip(),
    }


def evaluate_home_html(html: str) -> dict[str, Any]:
    """Inspect Home HTML for a startable session without CTA-copy matching."""
    parser = _HomeSignalParser()
    parser.feed(html)
    return verdict_from_signals(
        session_controls=parser.session_controls,
        empty_state=parser.empty_state,
        has_mission_hero=parser.has_mission_hero,
        has_home_surface=parser.has_home_surface,
        primary_labels=parser.primary_labels,
    )


def evaluate_home_page(page: Any) -> dict[str, Any]:
    """Inspect a live Playwright Home page using data attributes, not copy."""
    start_count = page.locator(STARTABLE_SELECTOR).count()
    resume_count = page.locator(RESUMABLE_SELECTOR).count()
    empty = page.locator(EMPTY_STATE_SELECTOR).count() > 0
    mission = page.locator(MISSION_HERO_SELECTOR)
    has_mission = mission.count() > 0
    hero_text = ""
    if has_mission:
        hero_text = mission.first.inner_text()
    primary = page.locator(PRIMARY_CTA_SELECTOR)
    labels: list[str] = []
    for index in range(primary.count()):
        labels.append(primary.nth(index).inner_text())
    controls: list[str] = []
    if start_count:
        controls.append("start")
    if resume_count:
        controls.append("resume")
    result = verdict_from_signals(
        session_controls=controls,
        empty_state=empty,
        has_mission_hero=has_mission,
        has_home_surface=page.locator(HOME_SURFACE_SELECTOR).count() > 0,
        primary_labels=labels,
        mission_hero_text=hero_text,
    )
    result["url"] = page.url
    return result


def _load_local_credentials() -> tuple[str, str]:
    env_path = ROOT / ".env"
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path)
    except Exception:
        pass
    email = (os.getenv("ADMIN_EMAIL") or "").strip()
    password = os.getenv("ADMIN_PASSWORD") or ""
    return email, password


def _app_available(base_url: str) -> bool:
    try:
        with urlopen(f"{base_url.rstrip('/')}/auth/login", timeout=3) as response:
            body = response.read(20_000).decode("utf-8", errors="replace")
            return response.status == 200 and (
                "Sign in" in body or "Kwalitec" in body
            )
    except (URLError, OSError, TimeoutError):
        return False


def run_live_check(base_url: str) -> dict[str, Any]:
    """Log in as the local founder admin and inspect Home."""
    email, password = _load_local_credentials()
    if not email or not password:
        return {
            "ok": False,
            "skipped": True,
            "reason": "local admin credentials not available in process environment",
        }
    if not _app_available(base_url):
        return {
            "ok": False,
            "skipped": True,
            "reason": f"app not reachable at {base_url}",
        }

    from playwright.sync_api import sync_playwright

    origin = base_url.rstrip("/")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(f"{origin}/auth/login", wait_until="networkidle", timeout=30000)
        page.fill("input[name=email], input#email, input[type=email]", email)
        page.fill(
            "input[name=password], input#password, input[type=password]",
            password,
        )
        page.click("button[type=submit], input[type=submit]")
        page.wait_for_load_state("networkidle")
        if "/auth/login" in page.url:
            browser.close()
            return {"ok": False, "skipped": False, "reason": "login failed"}
        page.goto(f"{origin}/student/", wait_until="networkidle", timeout=30000)
        verdict = evaluate_home_page(page)
        browser.close()

    verdict["ok"] = bool(verdict["can_enter_session"])
    verdict["skipped"] = False
    return verdict


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check founder Home for a startable session via data attributes."
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("KWALITEC_BASE_URL", "http://127.0.0.1:5001"),
        help="Local app origin (default http://127.0.0.1:5001)",
    )
    args = parser.parse_args(argv)
    result = run_live_check(args.base_url)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    if result.get("skipped"):
        print("FOUNDER_HOME_LIVE skipped:", result.get("reason"), file=sys.stderr)
        return 0
    if result.get("startable"):
        print("FOUNDER_HOME_LIVE startable session (data-session-control=start)")
        return 0
    if result.get("can_enter_session"):
        print(
            "FOUNDER_HOME_LIVE resumable session "
            f"(data-session-control={result.get('session_control')})"
        )
        return 0
    print("FOUNDER_HOME_LIVE no enterable session", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
