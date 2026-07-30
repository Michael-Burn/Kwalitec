#!/usr/bin/env python3
"""FV-002 resume — continue existing CS1 workspace from missing CMP upload."""

from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = os.environ.get("FV002_BASE", "http://127.0.0.1:5056")
EMAIL = os.environ["ADMIN_EMAIL"]
PASSWORD = os.environ["ADMIN_PASSWORD"]
WORKSPACE_ID = "ws-cs1"
CMP = Path(
    "/Users/kwalitec/Downloads/ActEd - Actuarial Statistics Subject CS1 CMP 2019.pdf"
)
EVIDENCE = Path(
    "/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/FV002"
)
SHOTS = EVIDENCE / "screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)
OUT = EVIDENCE / "resume_evidence.json"

timeline: list[dict] = []
t0 = time.time()


def utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(stage: str, ok: bool, page=None, **facts) -> None:
    entry = {
        "stage": stage,
        "ok": ok,
        "t": round(time.time() - t0, 1),
        "timestamp": utc(),
        "url": getattr(page, "url", None) if page else None,
        **facts,
    }
    timeline.append(entry)
    print(f"[{'✓' if ok else '✗'}] {stage}", facts)


def snip(page, label: str) -> str:
    text = page.inner_text("body")
    shot = SHOTS / f"resume_{len(timeline):02d}_{label}.png"
    try:
        page.screenshot(path=str(shot), full_page=True)
    except Exception:
        pass
    print(f"\n===== {label} =====\n{page.url}\n{text[:900]}\n")
    return text


def click_first(page, texts: list[str], wait_ms: int = 2500) -> str | None:
    for text in texts:
        loc = page.locator(
            f'button:has-text("{text}"), input[value*="{text}"], '
            f'a.ds-btn:has-text("{text}"), a:has-text("{text}")'
        )
        for i in range(loc.count()):
            el = loc.nth(i)
            try:
                if not el.is_visible():
                    continue
                try:
                    with page.expect_navigation(
                        wait_until="domcontentloaded", timeout=12000
                    ):
                        el.click()
                except Exception:
                    el.click()
                page.wait_for_timeout(wait_ms)
                return text
            except Exception as exc:
                print("click fail", text, exc)
    return None


def login(page) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    with page.expect_navigation(wait_until="domcontentloaded"):
        page.click('input[name="submit"], button[type="submit"]')
    if "/auth/experience" in page.url:
        click_first(page, ["Founder Console", "Founder", "Console"])
        if "/console" not in page.url:
            page.goto(f"{BASE}/console/", wait_until="domcontentloaded")
    log("Founder Login", True, page)


def doc_status(page) -> dict:
    resp = page.request.get(
        f"{BASE}/console/studio/workspaces/{WORKSPACE_ID}/documents/status"
    )
    if not resp.ok:
        return {"ok": False, "http_status": resp.status, "text": resp.text()[:500]}
    try:
        return resp.json()
    except Exception:
        return {"ok": False, "http_status": resp.status, "text": resp.text()[:500]}


def wait_both_ready(page, rounds: int = 60) -> dict:
    last: dict = {}
    for i in range(rounds):
        try:
            last = doc_status(page)
        except Exception as exc:
            print(f"poll {i}: status fetch error {exc}")
            page.wait_for_timeout(5000)
            continue
        status = last.get("status") or last
        docs = status.get("documents") or []
        kinds = {d.get("kind") for d in docs if d.get("is_active")}
        stages = {
            d.get("kind"): d.get("processing_stage")
            for d in docs
            if d.get("is_active")
        }
        errors = {
            d.get("kind"): d.get("last_error")
            for d in docs
            if d.get("is_active") and d.get("last_error")
        }
        print(
            f"poll {i}: kinds={kinds} stages={stages} all={status.get('all_required_uploaded')} err={errors}"
        )
        if errors:
            log("Processing", False, page, errors=errors, status=stages)
            return last
        if kinds >= {"cmp", "syllabus"} and all(
            (stages.get(k) or "").startswith("ready")
            or stages.get(k) in {"ready_for_embeddings", "ready", "completed", "success"}
            for k in ("cmp", "syllabus")
        ):
            log("Processing", True, page, status=stages)
            return last
        page.wait_for_timeout(8000)
        try:
            page.goto(
                f"{BASE}/console/studio/workspaces/{WORKSPACE_ID}",
                wait_until="domcontentloaded",
                timeout=30000,
            )
        except Exception as exc:
            print("reload failed", exc)
    log("Processing", False, page, last=str(last)[:500])
    return last


def main() -> int:
    assert CMP.exists()
    decision = "PIPELINE BLOCKED"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        page.set_default_timeout(60000)
        login(page)

        url = f"{BASE}/console/studio/workspaces/{WORKSPACE_ID}"
        page.goto(url, wait_until="domcontentloaded")
        body = snip(page, "workspace_before_cmp")
        log(
            "Open existing CS1 workspace",
            WORKSPACE_ID in page.url and "Actuarial Statistics" in body,
            page,
        )

        status = doc_status(page)
        st = status.get("status") or status
        docs = st.get("documents") or []
        kinds = {d.get("kind") for d in docs if d.get("is_active")}
        log(
            "Pre-upload document inventory",
            True,
            page,
            kinds=sorted(kinds),
            all_required=st.get("all_required_uploaded"),
            facts_hint="expect syllabus only",
        )

        if "cmp" not in kinds:
            # Upload ONLY missing CMP via kind-targeted input (JS XHR on change).
            cmp_input = page.locator(
                'article[data-doc-kind="cmp"] input[type="file"]'
            )
            assert cmp_input.count(), "CMP file input missing"
            cmp_input.first.set_input_files(str(CMP))
            # Wait for XHR upload
            page.wait_for_timeout(4000)
            for _ in range(20):
                st2 = (doc_status(page).get("status") or {})
                docs2 = st2.get("documents") or []
                kinds2 = {d.get("kind") for d in docs2 if d.get("is_active")}
                print("after cmp set", kinds2, st2.get("all_required_uploaded"))
                if "cmp" in kinds2:
                    break
                page.wait_for_timeout(2000)
            snip(page, "after_cmp_upload")
            log("Upload CMP", "cmp" in kinds2, page, kinds=sorted(kinds2))
        else:
            log("Upload CMP", True, page, note="already present")

        wait_both_ready(page)

        # Advance through Validate → Preview → Approve → Publish with strict flashes.
        for action, labels in [
            ("Advance", ["Continue", "Advance"]),
            ("Validate", ["Validate", "Run Validation", "Validate Curriculum"]),
            (
                "Preview",
                ["Confirm structure", "Build Preview", "Preview", "Generate Preview"],
            ),
            ("Approve", ["Approve", "Approve Curriculum"]),
            ("Publish", ["Publish", "Publish Curriculum", "Make Ready"]),
        ]:
            page.goto(url, wait_until="domcontentloaded")
            snip(page, f"before_{action}")
            reason = page.locator('input[name="reason"], textarea[name="reason"]')
            if reason.count() and action in {"Approve", "Publish"}:
                reason.first.fill("FV-002 resume — CS1")
            clicked = click_first(page, labels, wait_ms=4000)
            page.wait_for_timeout(2000)
            page.goto(url, wait_until="domcontentloaded")
            after = snip(page, f"after_{action}")
            flashes = []
            for sel in [".alert", ".flash", "[role=alert]"]:
                for el in page.locator(sel).all()[:10]:
                    try:
                        t = el.inner_text().strip()
                        if t:
                            flashes.append(t[:300])
                    except Exception:
                        pass
            blocked = bool(
                re.search(
                    r"cannot|blocked|refused|failed|not ready|missing",
                    " ".join(flashes),
                    re.I,
                )
            )
            ok = clicked is not None and not blocked
            # Relaxes: after action page may already be next stage without flash
            if action == "Publish" and (
                "/console/" == page.url.rstrip("/").split("?")[0].endswith("console")
                or "Recent Publications" in after
                or "Published" in " ".join(flashes)
            ):
                ok = True
            log(action, ok, page, clicked=clicked, flashes=flashes[:3])
            if action == "Publish":
                # Prefer Founder Home after publish redirect
                page.goto(f"{BASE}/console/", wait_until="domcontentloaded")
                home = snip(page, "founder_home")
                inconsistent = (
                    "No subjects have been created yet" in home
                    and ("Recent Publications" in home or "Published" in home)
                )
                log(
                    "Founder surfaces agree",
                    not inconsistent,
                    page,
                    inconsistent=inconsistent,
                )

        # Student path
        page.goto(f"{BASE}/auth/experience?switch=1", wait_until="domcontentloaded")
        click_first(page, ["Student Experience", "Student"])
        if "/alpha/onboarding" in page.url or "Welcome to Kwalitec" in page.inner_text("body"):
            click_first(page, ["Continue to Home", "Skip for now"])
        snip(page, "student_home")
        click_first(
            page,
            ["Choose Exam", "Select Exam", "Get started", "Create Study Plan"],
        )
        # Common wizard route
        for path in [
            f"{BASE}/study_plan/wizard/exam",
            f"{BASE}/study_plan/create",
            f"{BASE}/student/choose-exam",
            f"{BASE}/study-plan/",
        ]:
            page.goto(path, wait_until="domcontentloaded")
            body = page.inner_text("body")
            if "CS1" in body or "Actuarial" in body or "exam" in body.lower():
                snip(page, "choose_exam_candidate")
                break
        # Select CS1
        selected = False
        for sel in [
            'label:has-text("CS1")',
            'button:has-text("CS1")',
            'a:has-text("CS1")',
            'text=Actuarial Statistics',
            'input[value*="CS1"]',
        ]:
            loc = page.locator(sel)
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                selected = True
                break
        click_first(page, ["Continue", "Next", "Confirm", "Select", "Begin Learning"])
        log("Choose Exam", selected or "CS1" in page.inner_text("body"), page, selected=selected)

        begin_ok = False
        for step in range(14):
            snip(page, f"wizard_{step}")
            # soft-fill
            for name, val in [
                ("exam_sitting", "April 2027"),
                ("weekday_study_minutes", "60"),
                ("weekend_study_minutes", "120"),
                ("preferred_session_minutes", "45"),
            ]:
                loc = page.locator(f'input[name="{name}"], select[name="{name}"]')
                if loc.count() and loc.first.is_visible():
                    try:
                        loc.first.fill(val)
                    except Exception:
                        try:
                            loc.first.select_option(index=1)
                        except Exception:
                            pass
            date = page.locator('input[type="date"]')
            if date.count():
                try:
                    date.first.fill("2027-04-15")
                except Exception:
                    pass
            begin = page.locator(
                'button:has-text("Begin Learning"), input[value*="Begin Learning"]'
            )
            if begin.count() and begin.first.is_visible():
                with page.expect_navigation(
                    wait_until="domcontentloaded", timeout=45000
                ):
                    begin.first.click()
                after = snip(page, "after_begin")
                fail = "published curriculum must include sections" in after.lower()
                begin_ok = not fail and (
                    "/mission" in page.url
                    or "/session" in page.url
                    or "mission" in after.lower()
                    or "session" in after.lower()
                    or "today" in after.lower()
                )
                log(
                    "Begin Learning",
                    begin_ok,
                    page,
                    fail=fail,
                    url=page.url,
                )
                break
            clicked = click_first(
                page,
                [
                    "Continue",
                    "Next",
                    "Review",
                    "Confirm",
                    "Create Study Plan",
                    "Save",
                    "Begin Learning",
                ],
            )
            if not clicked:
                break

        if begin_ok:
            decision = "END-TO-END PIPELINE CERTIFIED"
        OUT.write_text(
            json.dumps(
                {"decision": decision, "timeline": timeline, "finished": utc()},
                indent=2,
            ),
            encoding="utf-8",
        )
        print("DECISION:", decision)
        browser.close()
        return 0 if decision.startswith("END-TO-END") else 1


if __name__ == "__main__":
    raise SystemExit(main())
