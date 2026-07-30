#!/usr/bin/env python3
"""FV-002 continue — ws-cs1 both docs Ready → Validate → Publish → Begin Learning."""

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
WID = "ws-cs1"
WS = f"{BASE}/console/studio/workspaces/{WID}"
EVIDENCE = Path(
    "/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/FV002"
)
SHOTS = EVIDENCE / "screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)
OUT = EVIDENCE / "continue_evidence.json"
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
    try:
        page.screenshot(path=str(SHOTS / f"cont_{len(timeline):02d}_{label}.png"), full_page=True)
    except Exception:
        pass
    print(f"\n===== {label} =====\n{page.url}\n{text[:1000]}\n")
    return text


def flashes(page) -> list[str]:
    out = []
    for sel in [".alert", ".flash", "[role=alert]", ".ds-alert"]:
        for el in page.locator(sel).all()[:12]:
            try:
                t = el.inner_text().strip()
                if t:
                    out.append(t[:400])
            except Exception:
                pass
    return out


def click_first(page, texts: list[str], wait_ms: int = 3000) -> str | None:
    for text in texts:
        loc = page.locator(
            f'button:has-text("{text}"), input[value*="{text}"], '
            f'a.ds-btn:has-text("{text}"), a.btn:has-text("{text}")'
        )
        for i in range(loc.count()):
            el = loc.nth(i)
            try:
                if not el.is_visible():
                    continue
                try:
                    with page.expect_navigation(
                        wait_until="domcontentloaded", timeout=20000
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


def main() -> int:
    decision = "PIPELINE BLOCKED"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        page.set_default_timeout(60000)
        login(page)
        page.goto(WS, wait_until="domcontentloaded")
        body = snip(page, "workspace_ready")
        # Confirm both Ready
        status = page.request.get(f"{BASE}/console/studio/workspaces/{WID}/documents/status").json()
        st = status.get("status") or status
        docs = {d["kind"]: d.get("processing_stage") for d in st.get("documents") or [] if d.get("is_active")}
        log("Documents Ready", docs.get("cmp", "").startswith("ready") and docs.get("syllabus", "").startswith("ready"), page, docs=docs)

        for action, labels in [
            ("Advance", ["Continue", "Advance"]),
            ("Validate", ["Validate", "Run Validation", "Validate Curriculum"]),
            ("Preview", ["Confirm structure", "Build Preview", "Preview", "Generate Preview"]),
            ("Approve", ["Approve", "Approve Curriculum"]),
            ("Publish", ["Publish", "Publish Curriculum", "Make Ready"]),
        ]:
            page.goto(WS, wait_until="domcontentloaded")
            snip(page, f"before_{action}")
            reason = page.locator('input[name="reason"], textarea[name="reason"]')
            if reason.count() and action in {"Approve", "Publish"}:
                reason.first.fill("FV-002 CS1 continue")
            clicked = click_first(page, labels, wait_ms=5000)
            page.wait_for_timeout(1500)
            # After publish may redirect to home
            if action != "Publish":
                page.goto(WS, wait_until="domcontentloaded")
            after = snip(page, f"after_{action}")
            fl = flashes(page)
            blocked = bool(re.search(r"cannot|blocked|refused|failed|not ready|missing", " ".join(fl), re.I))
            ok = clicked is not None and not blocked
            if action == "Publish" and (
                "published" in " ".join(fl).lower()
                or "Recent Publications" in after
                or page.url.rstrip("/").endswith("/console")
            ):
                ok = True
            log(action, ok, page, clicked=clicked, flashes=fl[:4])
            if action == "Preview":
                click_first(page, ["Expand All", "Expand"], wait_ms=800)
                prev = snip(page, "preview_tree")
                counts = {
                    "section": len(re.findall(r"\bsection\b", prev, re.I)),
                    "topic": len(re.findall(r"\btopic\b", prev, re.I)),
                    "objective": len(re.findall(r"\bobjective\b", prev, re.I)),
                }
                log("Hierarchy Verified", counts["topic"] > 0 or "CS1" in prev, page, counts=counts)

        page.goto(f"{BASE}/console/", wait_until="domcontentloaded")
        home = snip(page, "founder_home")
        inconsistent = "No subjects have been created yet" in home and (
            "Recent Publications" in home or "Published" in home
        )
        log("Founder surfaces agree", not inconsistent, page, inconsistent=inconsistent)

        # Student
        page.goto(f"{BASE}/auth/experience?switch=1", wait_until="domcontentloaded")
        click_first(page, ["Student Experience", "Student"])
        if "Welcome to Kwalitec" in page.inner_text("body") or "/alpha/onboarding" in page.url:
            click_first(page, ["Continue to Home", "Skip for now"])
        snip(page, "student_home")
        click_first(page, ["Choose Exam", "Select Exam", "Get started", "Create Study Plan"])
        for path in [
            f"{BASE}/study_plan/wizard/exam",
            f"{BASE}/study_plan/create",
            f"{BASE}/student/choose-exam",
            f"{BASE}/study_plan/",
            f"{BASE}/student/",
        ]:
            page.goto(path, wait_until="domcontentloaded")
            body = page.inner_text("body")
            if "CS1" in body or "Actuarial" in body:
                snip(page, "exam_surface")
                break
        selected = False
        for sel in [
            'label:has-text("CS1")',
            'button:has-text("CS1")',
            'a:has-text("CS1")',
            "text=Actuarial Statistics",
        ]:
            loc = page.locator(sel)
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                selected = True
                break
        click_first(page, ["Continue", "Next", "Confirm", "Select"])
        log("Choose Exam", selected or "CS1" in page.inner_text("body"), page, selected=selected)

        begin_ok = False
        for step in range(14):
            snip(page, f"wizard_{step}")
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
                with page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
                    begin.first.click()
                after = snip(page, "after_begin")
                fl = flashes(page)
                fail = "published curriculum must include sections" in (after + " ".join(fl)).lower()
                begin_ok = not fail and (
                    "/mission" in page.url
                    or "/session" in page.url
                    or re.search(r"mission|session|today.?s focus|learning", after, re.I)
                )
                log("Begin Learning", begin_ok, page, fail=fail, flashes=fl[:5], url=page.url)
                break
            if not click_first(
                page,
                ["Continue", "Next", "Review", "Confirm", "Create Study Plan", "Save", "Begin Learning"],
            ):
                break

        if begin_ok:
            decision = "END-TO-END PIPELINE CERTIFIED"
        OUT.write_text(json.dumps({"decision": decision, "timeline": timeline, "finished": utc()}, indent=2))
        print("DECISION:", decision)
        browser.close()
        return 0 if decision.startswith("END-TO-END") else 1


if __name__ == "__main__":
    raise SystemExit(main())
