"""FV-001A — explore Console Content + student flows via visible UI."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5128"
EMAIL = "founder.blind@kwalitec.example"
PASSWORD = "BlindReview2026!"
OUT = Path("/tmp/fv001a_blind_capture")
OUT.mkdir(parents=True, exist_ok=True)
records: list[dict] = []
t0 = time.time()


def snip(page, label: str, n: int = 2400) -> dict:
    text = re.sub(r"\n{3,}", "\n\n", page.inner_text("body")).strip()
    links = []
    for a in page.locator("a").all()[:70]:
        try:
            t = a.inner_text().strip()
            h = a.get_attribute("href") or ""
            if t or h:
                links.append({"text": t[:90], "href": h[:180]})
        except Exception:
            pass
    ctas: list[str] = []
    for sel in ["button", "input[type=submit]", "a.btn"]:
        for el in page.locator(sel).all()[:40]:
            try:
                t = (el.inner_text() or el.get_attribute("value") or "").strip()
                if t:
                    ctas.append(t[:100])
            except Exception:
                pass
    shot = OUT / f"explore_{len(records):02d}_{re.sub(r'[^a-z0-9]+', '_', label.lower())[:40]}.png"
    try:
        page.screenshot(path=str(shot), full_page=True)
    except Exception:
        shot = None
    rec = {
        "phase": label,
        "t": round(time.time() - t0, 1),
        "url": page.url,
        "title": page.title(),
        "text": text[:n],
        "links": links,
        "ctas": list(dict.fromkeys(ctas))[:25],
        "screenshot": str(shot) if shot else None,
    }
    records.append(rec)
    print(f"\n===== {label} =====\nURL: {page.url}\nTITLE: {page.title()}")
    print("CTAs:", rec["ctas"][:15])
    print("LINKS:", [(l["text"], l["href"]) for l in links[:18]])
    print(text[:1000])
    return rec


def click_text(page, texts: list[str]):
    for t in texts:
        for role in ("link", "button"):
            loc = page.get_by_role(role, name=re.compile(t, re.I))
            if loc.count():
                try:
                    with page.expect_navigation(
                        wait_until="domcontentloaded", timeout=5000
                    ):
                        loc.first.click()
                    return t
                except Exception:
                    try:
                        loc.first.click()
                        page.wait_for_timeout(400)
                        return t
                    except Exception:
                        pass
        loc = page.locator(f"a:has-text('{t}'), button:has-text('{t}')")
        if loc.count() and loc.first.is_visible():
            try:
                with page.expect_navigation(
                    wait_until="domcontentloaded", timeout=5000
                ):
                    loc.first.click()
                return t
            except Exception:
                try:
                    loc.first.click()
                    page.wait_for_timeout(400)
                    return t
                except Exception:
                    pass
    return None


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        page.set_default_timeout(12000)
        page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        with page.expect_navigation(wait_until="domcontentloaded"):
            page.click('input[name="submit"], button[type="submit"]')
        snip(page, "console_home")

        for label in [
            "Overview",
            "Operations",
            "Students",
            "Learning",
            "Assessments",
            "Content",
            "Analytics",
            "Platform",
            "Settings",
            "Support",
        ]:
            click_text(page, [rf"^{label}$", label])
            snip(page, f"nav_{label}")
            if label == "Content":
                for l in list(records[-1]["links"]):
                    href = l["href"]
                    if not href.startswith("/"):
                        continue
                    keys = (
                        "studio",
                        "curriculum",
                        "subject",
                        "content",
                        "publish",
                        "workspace",
                        "document",
                    )
                    if any(k in href.lower() for k in keys):
                        page.goto(f"{BASE}{href}", wait_until="domcontentloaded")
                        snip(page, f"content_href_{href.strip('/').replace('/', '_')[:40]}")
                for t in [
                    "Curriculum Studio",
                    "Create Subject",
                    "Subjects",
                    "New Subject",
                    "Upload",
                    "Syllabus",
                    "CMP",
                    "Publish",
                    "Workspaces",
                    "Manage content",
                    "Create workspace",
                ]:
                    hit = click_text(page, [t])
                    if hit:
                        snip(page, f"content_click_{hit}")

        page.goto(f"{BASE}/console/", wait_until="domcontentloaded")
        for t in [
            "Manage content",
            "Platform Intelligence",
            "Open operations",
            "Review support inbox",
            "Open Attention Center",
        ]:
            hit = click_text(page, [t])
            if hit:
                snip(page, f"quick_{hit}")
                page.goto(f"{BASE}/console/", wait_until="domcontentloaded")

        for path in [
            "/founder/",
            "/studio/",
            "/curriculum_studio/",
            "/curriculum-studio/",
            "/console/content",
        ]:
            resp = page.goto(f"{BASE}{path}", wait_until="domcontentloaded")
            snip(page, f"guess_{path.strip('/').replace('/', '_')}")
            records[-1]["status"] = resp.status if resp else None

        # Student path
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "student_entry")
        for i in range(8):
            body = page.inner_text("body")
            if "Welcome to Kwalitec" in body or "onboarding" in page.url:
                cont = page.locator(
                    'button:has-text("Continue"), a:has-text("Continue"), '
                    'button:has-text("Continue to Home")'
                )
                if cont.count():
                    try:
                        with page.expect_navigation(
                            wait_until="domcontentloaded", timeout=5000
                        ):
                            cont.first.click()
                    except Exception:
                        cont.first.click()
                        page.wait_for_timeout(400)
                    snip(page, f"onboarding_step_{i}")
                else:
                    break
            else:
                break
        snip(page, "student_after_onboarding")

        click_text(page, ["Study Plan"])
        snip(page, "study_plan_nav")
        for t in [
            "Create Study Plan",
            "New Study Plan",
            "Start",
            "Begin",
            "Create a plan",
            "Create plan",
        ]:
            if click_text(page, [t]):
                snip(page, f"study_plan_{t}")
                break

        for step in range(1, 9):
            if "wizard" not in page.url and step > 1:
                break
            fields = []
            for el in page.locator("input, select, textarea").all()[:40]:
                try:
                    fields.append(
                        {
                            "name": el.get_attribute("name"),
                            "type": el.get_attribute("type"),
                            "tag": el.evaluate("e=>e.tagName"),
                        }
                    )
                except Exception:
                    pass
            print("FIELDS", fields)
            records[-1]["fields"] = fields
            for f in fields:
                name = f.get("name") or ""
                if not name:
                    continue
                loc = page.locator(f'[name="{name}"]')
                if not loc.count():
                    continue
                typ = (f.get("type") or "").lower()
                tag = f.get("tag")
                try:
                    if tag == "SELECT":
                        if loc.locator("option").count() > 1:
                            loc.select_option(index=1)
                    elif typ == "checkbox":
                        if not loc.is_checked():
                            loc.check()
                    elif typ == "radio":
                        loc.first.check()
                    elif typ == "date" or "date" in name:
                        loc.fill("2026-09-15")
                    elif typ == "number" or "hour" in name or "day" in name:
                        loc.fill("10")
                    elif tag == "INPUT" and typ in ("text", "email", ""):
                        if not loc.input_value():
                            loc.fill("CS1")
                except Exception as e:
                    print("fill fail", name, e)
            before = page.url
            click_text(page, ["Continue", "Next", "Create", "Finish", "Confirm", "Save"])
            sub = page.locator('button[type="submit"], input[type="submit"]')
            if sub.count() and page.url == before:
                try:
                    with page.expect_navigation(
                        wait_until="domcontentloaded", timeout=5000
                    ):
                        sub.first.click()
                except Exception:
                    try:
                        sub.first.click()
                        page.wait_for_timeout(500)
                    except Exception:
                        pass
            page.wait_for_timeout(500)
            snip(page, f"wizard_step_{step}")

        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        for t in ["Got it", "Continue", "Close", "Dismiss"]:
            click_text(page, [t])
        snip(page, "student_home_ready")
        if click_text(page, ["Explain today's mission", "Explain"]):
            snip(page, "explain_mission")
        click_text(page, ["Start Session", "Start Study Session", "Begin"])
        snip(page, "after_start_session")
        for t in ["Begin", "Begin session", "Continue", "Start", "I'm ready", "Next"]:
            if click_text(page, [t]):
                snip(page, f"session_{t}")
        radios = page.locator('input[type="radio"]')
        if radios.count():
            radios.first.check()
            click_text(page, ["Submit", "Check", "Continue", "Next"])
            page.wait_for_timeout(500)
            snip(page, "after_answer")
        for t in [
            "Finish Study Session",
            "Finish",
            "Complete",
            "End session",
            "Done",
        ]:
            if click_text(page, [t]):
                snip(page, f"finish_{t}")
                break
        snip(page, "session_end_state")
        page.goto(f"{BASE}/student/journey", wait_until="domcontentloaded")
        snip(page, "journey")
        browser.close()

    (OUT / "explore.json").write_text(json.dumps(records, indent=2))
    print("\nWROTE", len(records), "records to", OUT / "explore.json")


if __name__ == "__main__":
    main()
