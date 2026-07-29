"""FV-001A focus2 — studio + student with corrected Content navigation."""

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


def snip(page, label: str, n: int = 3200) -> dict:
    text = re.sub(r"\n{3,}", "\n\n", page.inner_text("body")).strip()
    links = []
    for a in page.locator("a").all()[:100]:
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
                    ctas.append(t[:120])
            except Exception:
                pass
    headings = []
    for h in page.locator("h1, h2, h3, label, .section-eyebrow").all()[:35]:
        try:
            t = h.inner_text().strip()
            if t:
                headings.append(t[:120])
        except Exception:
            pass
    shot = OUT / f"focus2_{len(records):02d}_{re.sub(r'[^a-z0-9]+', '_', label.lower())[:40]}.png"
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
        "links": links[:50],
        "ctas": list(dict.fromkeys(ctas))[:30],
        "headings": headings[:30],
        "screenshot": str(shot) if shot else None,
    }
    records.append(rec)
    print(f"\n===== {label} =====\nURL: {page.url}\nTITLE: {page.title()}")
    print("CTAs:", rec["ctas"][:12])
    print("HEAD:", headings[:10])
    print(text[:1100])
    return rec


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        page.set_default_timeout(20000)

        page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        with page.expect_navigation(wait_until="domcontentloaded"):
            page.click('input[name="submit"], button[type="submit"]')
        snip(page, "console_home")

        nav = page.locator(
            'a[href*="/console/studio"], a[href*="studio"]:not([href^="#"])'
        )
        print("studio nav count", nav.count())
        for i in range(min(nav.count(), 8)):
            print("NAV", nav.nth(i).inner_text().strip(), nav.nth(i).get_attribute("href"))
        if nav.count():
            with page.expect_navigation(wait_until="domcontentloaded"):
                nav.first.click()
            snip(page, "nav_to_studio")
        else:
            mc = page.locator('a:has-text("Manage content")')
            if mc.count():
                print("Manage content href", mc.first.get_attribute("href"))
                with page.expect_navigation(wait_until="domcontentloaded"):
                    mc.first.click()
                snip(page, "manage_content")

        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "studio_index")

        create = page.locator(
            'a:has-text("Create Subject"), button:has-text("Create Subject"), '
            'a[href*="subject/create"], a[href*="create-subject"], a[href*="subjects/new"]'
        )
        print("create subject count", create.count())
        for i in range(min(page.locator("a, button").count(), 40)):
            el = page.locator("a, button").nth(i)
            try:
                t = el.inner_text().strip()
                if t and any(
                    k in t.lower()
                    for k in ("create", "subject", "workspace", "upload", "new")
                ):
                    print(
                        "CTA-ish",
                        t[:70],
                        el.get_attribute("href") if el.evaluate("e=>e.tagName")=="A" else "button",
                    )
            except Exception:
                pass

        if create.count():
            create.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(400)
            snip(page, "create_subject_page")
        else:
            # try any create link
            any_create = page.locator('a:has-text("Create"), button:has-text("Create")')
            if any_create.count():
                any_create.first.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(400)
            snip(page, "create_attempt")

        for el in page.locator("input, select, textarea").all()[:30]:
            try:
                print(
                    "FIELD",
                    el.get_attribute("name"),
                    el.get_attribute("type"),
                    el.evaluate("e=>e.tagName"),
                    (el.get_attribute("placeholder") or "")[:40],
                )
            except Exception:
                pass

        filled = False
        for name, value in [
            ("code", "CS1X"),
            ("subject_code", "CS1X"),
            ("name", "CS1X Blind Review Subject"),
            ("subject_name", "CS1X Blind Review Subject"),
            ("title", "CS1X Blind Review Subject"),
            ("display_name", "CS1X Blind Review Subject"),
            ("description", "Dummy subject for blind acceptance"),
        ]:
            loc = page.locator(f'[name="{name}"]')
            if not loc.count():
                continue
            tag = loc.first.evaluate("e=>e.tagName")
            try:
                if tag == "SELECT":
                    if loc.first.locator("option").count() > 1:
                        loc.first.select_option(index=1)
                        filled = True
                else:
                    loc.first.fill(value)
                    filled = True
            except Exception as e:
                print("fill err", name, e)
        for i in range(min(page.locator("select").count(), 6)):
            sel = page.locator("select").nth(i)
            try:
                if sel.locator("option").count() > 1:
                    sel.select_option(index=1)
                    filled = True
            except Exception:
                pass
        if filled:
            sub = page.locator(
                'button:has-text("Create"), button[type="submit"], input[type="submit"]'
            )
            if sub.count():
                sub.first.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(800)
            snip(page, "after_create_subject")

        for text in [
            "Create Workspace",
            "New Workspace",
            "Open workspace",
            "Open",
            "Workspaces",
        ]:
            loc = page.locator(f'a:has-text("{text}"), button:has-text("{text}")')
            if loc.count() and loc.first.is_visible():
                print("clicking", text)
                try:
                    loc.first.click()
                    page.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(500)
                    snip(page, f"after_{text.replace(' ', '_')}")
                except Exception as e:
                    print("click fail", text, e)

        for name, value in [
            ("name", "CS1X Workspace"),
            ("workspace_name", "CS1X Workspace"),
        ]:
            loc = page.locator(f'input[name="{name}"]')
            if loc.count():
                loc.first.fill(value)
                page.locator(
                    'button:has-text("Create"), button[type="submit"]'
                ).first.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(800)
                snip(page, "after_workspace_create")
                break

        ws = page.locator('a[href*="/workspace"], a[href*="/console/studio/"]')
        print("workspace-like", ws.count())
        for i in range(min(ws.count(), 10)):
            print(
                " WS",
                ws.nth(i).inner_text().strip()[:50],
                ws.nth(i).get_attribute("href"),
            )
            href = ws.nth(i).get_attribute("href") or ""
            if "/console/studio/" in href and href.rstrip("/") != "/console/studio":
                page.goto(f"{BASE}{href}", wait_until="domcontentloaded")
                snip(page, "opened_workspace_link")
                break

        dummy = OUT / "dummy_syllabus.pdf"
        dummy.write_bytes(b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n")
        files = page.locator('input[type="file"]')
        print("files", files.count())
        snip(page, "pre_upload_state")
        if files.count():
            files.nth(0).set_input_files(str(dummy))
            page.wait_for_timeout(2000)
            snip(page, "after_file_select")
            up = page.locator('button:has-text("Upload")')
            if up.count():
                up.first.click()
                page.wait_for_timeout(2500)
                snip(page, "after_upload_click")
            if files.count() >= 2:
                files.nth(1).set_input_files(str(dummy))
                page.wait_for_timeout(2000)
                if up.count():
                    up.first.click()
                    page.wait_for_timeout(2500)
                snip(page, "after_cmp_upload")

        for text in [
            "Advance",
            "Validate",
            "Preview",
            "Approve",
            "Publish",
            "Run pipeline",
            "Extract",
        ]:
            loc = page.locator(f'button:has-text("{text}"), a:has-text("{text}")')
            if loc.count() and loc.first.is_visible():
                print("ACTION", text)
                try:
                    loc.first.click()
                    page.wait_for_timeout(1200)
                    snip(page, f"action_{text}")
                except Exception as e:
                    print("action fail", text, e)
        snip(page, "studio_end")

        # Student path
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "student_entry")
        skip = page.locator(
            'a:has-text("Skip for now"), button:has-text("Skip for now")'
        )
        if skip.count():
            skip.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(500)
            snip(page, "after_skip")
        snip(page, "student_home")

        page.goto(f"{BASE}/study-plan/wizard/1", wait_until="domcontentloaded")
        snip(page, "wizard1")
        try:
            page.locator('label[for="exam_category-0"]').click(force=True)
        except Exception:
            page.locator(".wizard-option").first.click(force=True)
        page.wait_for_timeout(300)
        page.locator('button:has-text("Next")').first.click(force=True)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(600)
        snip(page, "wizard2")

        for step in range(2, 8):
            opts = page.locator(".wizard-option, label.wizard-option")
            if opts.count():
                try:
                    opts.first.click(force=True)
                except Exception:
                    pass
            for name in [
                "exam_date",
                "target_exam_date",
                "hours_per_week",
                "weekly_hours",
            ]:
                loc = page.locator(f'input[name="{name}"]')
                if loc.count():
                    try:
                        if "date" in name:
                            loc.first.fill("2026-09-15")
                        else:
                            loc.first.fill("12")
                    except Exception:
                        pass
            for i in range(min(page.locator("select").count(), 4)):
                try:
                    s = page.locator("select").nth(i)
                    if s.locator("option").count() > 1:
                        s.select_option(index=1)
                except Exception:
                    pass
            before = page.url
            nxt = page.locator(
                'button:has-text("Next"), button:has-text("Continue"), '
                'button:has-text("Create"), button:has-text("Finish"), '
                'button:has-text("Confirm"), button[type="submit"]'
            )
            if nxt.count():
                try:
                    nxt.first.click(force=True)
                    page.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(700)
                except Exception as e:
                    print("next", e)
            snip(page, f"wizard_step_{step}")
            if "wizard" not in page.url or page.url == before:
                break

        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "home_after_plan")
        start = page.locator(
            'button:has-text("Start Session"), a:has-text("Start Session")'
        )
        if start.count():
            start.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)
            snip(page, "session")
            begin = page.locator(
                'button:has-text("Begin"), a:has-text("Begin"), '
                'button:has-text("Continue")'
            )
            if begin.count():
                begin.first.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(800)
                snip(page, "session_active")
            fin = page.locator(
                'button:has-text("Finish Study Session"), button:has-text("Finish")'
            )
            if fin.count():
                page.once("dialog", lambda d: d.accept())
                fin.first.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(1000)
                snip(page, "session_done")
        snip(page, "end")
        browser.close()

    (OUT / "focus2.json").write_text(json.dumps(records, indent=2))
    print("\nWROTE", len(records), OUT / "focus2.json")


if __name__ == "__main__":
    main()
