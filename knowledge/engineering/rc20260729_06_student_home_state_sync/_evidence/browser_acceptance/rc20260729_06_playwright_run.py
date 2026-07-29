#!/usr/bin/env python3
"""RC-2026.07.29-06 — Student Home state sync browser smoke.

Walk: login → wizard → calibration → Student Home
Assert Home shows active study context (not empty "No exam selected").
Capture: student_home_after_plan.png
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

# Import wizard helpers from RC-05 run script (sibling engineering folder).
RC05 = (
    Path(__file__).resolve().parents[3]
    / "rc20260729_05_browser_acceptance_final"
    / "_evidence"
    / "browser_acceptance"
)
ROOT = Path(__file__).resolve().parents[2]
REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(RC05))

from rc20260729_05_playwright_run import (  # noqa: E402
    BASE_URL,
    click_wizard_continue,
    dismiss_welcome_modal,
    fill_calibration,
    fill_wizard_step,
    is_authenticated,
    login,
)

OUT_DIR = ROOT / "_evidence" / "browser_acceptance"
SHOT = OUT_DIR / "student_home_after_plan.png"
EVIDENCE = OUT_DIR / "evidence.json"

STUDENT_CANDIDATES = [
    ("rc06.sync@kwalitec.example", "Rc06Sync2026!"),
    ("rc05.accept2@kwalitec.example", "Rc05Accept2026!"),
    ("v1.empty@kwalitec.example", "ReviewPackage2026!"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def app_up(base: str) -> bool:
    try:
        with urlopen(f"{base}/auth/login", timeout=3) as r:
            body = r.read(20_000).decode("utf-8", errors="replace")
            return r.status == 200 and ("Sign in" in body or "Kwalitec" in body)
    except Exception:
        return False


def ensure_fresh_student() -> tuple[str, str]:
    """Create a dedicated user with no study plan for a clean empty→active path."""
    from app import create_app
    from app.extensions import db
    from app.models.user import User

    email, password = STUDENT_CANDIDATES[0]
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(email=email, is_active_user=True)
            user.set_password(password)
            user.alpha_onboarding_completed = True
            user.welcome_dismissed = True
            db.session.add(user)
            db.session.commit()
        else:
            from app.models.study_plan import StudyPlan

            for plan in StudyPlan.query.filter_by(user_id=user.id, active=True).all():
                plan.active = False
            db.session.commit()
    return email, password


def home_state(page) -> dict:
    return page.evaluate(
        """() => {
          const empty = document.querySelector('[data-student-state="empty"]');
          const quiet = document.querySelector('[data-student-state="quiet"]');
          const mission = document.querySelector('.ds-mission-panel');
          const primary = document.querySelector('[data-student-cta="primary"]');
          const body = ((document.querySelector('main') || document.body).innerText || '');
          return {
            url: location.href,
            h1: ((document.querySelector('h1') || {}).innerText || '').trim(),
            has_empty: !!empty,
            has_quiet: !!quiet,
            has_mission_panel: !!mission,
            primary_label: primary ? (primary.innerText || '').trim() : '',
            mentions_no_exam: /No exam selected/i.test(body),
            subject: ((document.querySelector('.ds-mission-panel__subject') || {}).innerText || '').trim(),
            objective: ((document.querySelector('.ds-mission-panel__objective') || {}).innerText || '').trim(),
            body_snippet: body.slice(0, 500),
          };
        }"""
    )


def walk_wizard(page, evidence: dict) -> None:
    if "/study-plan/wizard/" not in page.url:
        page.goto(f"{BASE_URL}/study-plan/wizard/1", wait_until="networkidle")

    for _ in range(12):
        url = page.url
        evidence.setdefault("journey", []).append({"t": utc_now(), "url": url})
        if "/student/" in url and "/study-plan/" not in url:
            return
        if "/calibration/" in url:
            fill_calibration(page)
            continue
        if "/study-plan/review" in url or page.locator(
            'button:has-text("Begin Learning"), button:has-text("Begin learning")'
        ).count():
            click_wizard_continue(page)
            continue
        if "/study-plan/wizard/" in url:
            fill_wizard_step(page)
            click_wizard_continue(page)
            continue
        if is_authenticated(page) and "/auth/" not in url:
            # Landed elsewhere (mission/session) — go Home next.
            return
        time.sleep(0.4)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    evidence: dict = {
        "rc": "RC-2026.07.29-06",
        "started_at": utc_now(),
        "base_url": BASE_URL,
    }

    if not app_up(BASE_URL):
        evidence["error"] = "APPLICATION NOT AVAILABLE"
        EVIDENCE.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
        print("APPLICATION NOT AVAILABLE")
        return 2

    email, password = ensure_fresh_student()
    evidence["student"] = email

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1366, "height": 768})
        page = ctx.new_page()

        if not login(page, BASE_URL, email, password):
            evidence["login_ok"] = False
            EVIDENCE.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
            print("LOGIN FAILED")
            return 3
        evidence["login_ok"] = True

        if "/alpha/onboarding" in page.url:
            try:
                page.locator(
                    'form[action*="onboarding"] button[type="submit"]'
                ).first.click(timeout=5_000)
                page.wait_for_load_state("networkidle", timeout=20_000)
            except Exception:
                pass

        # Baseline: empty (or quiet) before plan — optional capture of starting state.
        page.goto(f"{BASE_URL}/student/", wait_until="networkidle")
        dismiss_welcome_modal(page, start_session=False)
        before = home_state(page)
        evidence["home_before"] = before

        walk_wizard(page, evidence)
        dismiss_welcome_modal(page, start_session=False)

        page.goto(f"{BASE_URL}/student/", wait_until="networkidle")
        dismiss_welcome_modal(page, start_session=False)
        after = home_state(page)
        evidence["home_after"] = after
        page.screenshot(path=str(SHOT), full_page=True)
        evidence["screenshot"] = str(SHOT.relative_to(ROOT))

        # Refresh persistence
        page.reload(wait_until="networkidle")
        dismiss_welcome_modal(page, start_session=False)
        refreshed = home_state(page)
        evidence["home_after_refresh"] = refreshed

        # Logout / login persistence
        page.goto(f"{BASE_URL}/auth/logout", wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        # Explicit login page — logout may redirect to public home.
        page.goto(f"{BASE_URL}/auth/login", wait_until="networkidle")
        if not login(page, BASE_URL, email, password):
            evidence["relogin_ok"] = False
        else:
            evidence["relogin_ok"] = True
            page.goto(f"{BASE_URL}/student/", wait_until="networkidle")
            dismiss_welcome_modal(page, start_session=False)
            after_relogin = home_state(page)
            evidence["home_after_relogin"] = after_relogin

        after_relogin = evidence.get("home_after_relogin") or {}
        ok = (
            not after.get("has_empty")
            and not after.get("mentions_no_exam")
            and (
                after.get("has_mission_panel")
                or after.get("has_quiet")
                or bool(after.get("primary_label"))
            )
            and not refreshed.get("has_empty")
            and (
                not after_relogin
                or (
                    not after_relogin.get("has_empty")
                    and not after_relogin.get("mentions_no_exam")
                )
            )
        )
        evidence["pass"] = ok
        evidence["finished_at"] = utc_now()
        EVIDENCE.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

        print(json.dumps({"pass": ok, "home_after": after}, indent=2))
        ctx.close()
        browser.close()
        return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
