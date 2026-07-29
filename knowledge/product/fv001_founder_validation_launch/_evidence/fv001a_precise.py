"""FV-001A — precise Create Subject / Workspace / Upload / Session capture."""

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


def snip(page, label: str, n: int = 3500) -> dict:
    text = re.sub(r"\n{3,}", "\n\n", page.inner_text("body")).strip()
    flashes = []
    for sel in [".alert", ".flash", "[role=alert]", ".toast"]:
        for el in page.locator(sel).all()[:10]:
            try:
                t = el.inner_text().strip()
                if t:
                    flashes.append(t[:200])
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
    shot = OUT / f"precise_{len(records):02d}_{re.sub(r'[^a-z0-9]+', '_', label.lower())[:40]}.png"
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
        "flashes": flashes,
        "ctas": list(dict.fromkeys(ctas))[:30],
        "screenshot": str(shot) if shot else None,
    }
    records.append(rec)
    print(f"\n===== {label} =====\nURL: {page.url}\nFLASH: {flashes}\nCTAs: {rec['ctas'][:12]}")
    print(text[:1200])
    return rec


def login(page) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    with page.expect_navigation(wait_until="domcontentloaded"):
        page.click('input[name="submit"], button[type="submit"]')


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.set_default_timeout(20000)
        login(page)
        snip(page, "01_console")

        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "02_studio")

        # Create Subject — fill ONLY the create-subject form fields
        # There are two subject_code inputs; scope to Create Subject card.
        create_card = page.locator('section[aria-label="Create Subject or workspace"] .command-card').first
        create_card.locator('input[name="subject_code"]').fill("CS1X")
        create_card.locator('input[name="title"]').fill("CS1X Blind Review Subject")
        with page.expect_navigation(wait_until="domcontentloaded"):
            create_card.locator('input[type="submit"], button[type="submit"]').first.click()
        snip(page, "03_after_create_subject")

        # Open Workspace with same code
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        open_card = page.locator('section[aria-label="Create Subject or workspace"] .command-card').nth(1)
        open_card.locator('input[name="subject_code"]').fill("CS1X")
        with page.expect_navigation(wait_until="domcontentloaded"):
            open_card.locator('input[type="submit"], button[type="submit"]').first.click()
        snip(page, "04_after_open_workspace")

        # Upload
        dummy_syl = OUT / "dummy_syllabus.pdf"
        dummy_cmp = OUT / "dummy_cmp.pdf"
        pdf = b"%PDF-1.4\n1 0 obj<< /Type /Catalog >>endobj\ntrailer<<>>\n%%EOF\n"
        dummy_syl.write_bytes(pdf)
        dummy_cmp.write_bytes(pdf)
        files = page.locator('input[type="file"]')
        print("file inputs", files.count())
        snip(page, "05_workspace_before_upload")
        if files.count() >= 1:
            files.nth(0).set_input_files(str(dummy_syl))
            page.wait_for_timeout(2500)
            snip(page, "06_syllabus_selected")
        if files.count() >= 2:
            files.nth(1).set_input_files(str(dummy_cmp))
            page.wait_for_timeout(2500)
            snip(page, "07_cmp_selected")
        # Upload buttons / status
        for text in ["Upload", "Upload Documents"]:
            loc = page.locator(f'button:has-text("{text}")')
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                page.wait_for_timeout(2500)
                snip(page, f"08_upload_{text.replace(' ', '_')}")

        # Workflow actions
        for text in ["Advance", "Validate", "Preview", "Approve", "Publish"]:
            loc = page.locator(f'button:has-text("{text}"), input[value*="{text}"]')
            if loc.count() and loc.first.is_visible():
                # publish may need reason
                reason = page.locator('input[name="reason"], textarea[name="reason"]')
                if text == "Publish" and reason.count():
                    reason.first.fill("Blind acceptance review publish attempt")
                try:
                    loc.first.click()
                    page.wait_for_timeout(1500)
                    snip(page, f"09_action_{text}")
                except Exception as e:
                    print("action fail", text, e)

        snip(page, "10_workspace_final")

        # Student session — keep same context, skip onboarding, start session
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "11_student")
        skip = page.locator('a:has-text("Skip for now"), button:has-text("Skip for now")')
        if skip.count():
            skip.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(500)
            snip(page, "12_skip_onboarding")

        # Explain mission
        expl = page.locator('button:has-text("Explain"), a:has-text("Explain")')
        if expl.count():
            expl.first.click()
            page.wait_for_timeout(1000)
            snip(page, "13_explain")

        start = page.locator(
            'button:has-text("Start Session"), a:has-text("Start Session")'
        )
        if start.count():
            with page.expect_navigation(wait_until="domcontentloaded"):
                start.first.click()
            page.wait_for_timeout(1000)
            snip(page, "14_session_start")
            for text in ["Begin", "Continue", "Start", "I'm ready"]:
                loc = page.locator(f'button:has-text("{text}"), a:has-text("{text}")')
                if loc.count() and loc.first.is_visible():
                    try:
                        loc.first.click()
                        page.wait_for_load_state("domcontentloaded")
                        page.wait_for_timeout(800)
                        snip(page, f"15_{text}")
                    except Exception:
                        pass
            # Try complete activities
            for _ in range(3):
                radios = page.locator('input[type="radio"]')
                if radios.count():
                    radios.first.check(force=True)
                sub = page.locator(
                    'button:has-text("Submit"), button:has-text("Check"), '
                    'button:has-text("Next"), button:has-text("Continue")'
                )
                if sub.count() and sub.first.is_visible():
                    try:
                        sub.first.click()
                        page.wait_for_timeout(800)
                        snip(page, "16_activity_step")
                    except Exception:
                        break
                else:
                    break
            fin = page.locator(
                'button:has-text("Finish Study Session"), button:has-text("Finish"), '
                'a:has-text("Finish Study Session")'
            )
            if fin.count():
                page.once("dialog", lambda d: d.accept())
                try:
                    with page.expect_navigation(wait_until="domcontentloaded"):
                        fin.first.click()
                except Exception:
                    fin.first.click()
                    page.wait_for_timeout(1000)
                snip(page, "17_finish")
            snip(page, "18_after_session")

        # Return journey
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "19_return_home")
        page.goto(f"{BASE}/student/revision", wait_until="domcontentloaded")
        snip(page, "20_revision")
        page.goto(f"{BASE}/alpha/help", wait_until="domcontentloaded")
        snip(page, "21_help_coach_proxy")

        browser.close()

    (OUT / "precise.json").write_text(json.dumps(records, indent=2))
    print("\nWROTE", len(records), OUT / "precise.json")


if __name__ == "__main__":
    main()
