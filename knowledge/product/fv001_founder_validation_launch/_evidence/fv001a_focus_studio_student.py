"""FV-001A — focused Curriculum Studio + student session capture."""

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


def snip(page, label: str, n: int = 3000) -> dict:
    text = re.sub(r"\n{3,}", "\n\n", page.inner_text("body")).strip()
    links = []
    for a in page.locator("a").all()[:80]:
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
    for h in page.locator("h1,h2,h3,label,.section-eyebrow,.form-label").all()[:40]:
        try:
            t = h.inner_text().strip()
            if t:
                headings.append(t[:120])
        except Exception:
            pass
    shot = OUT / f"focus_{len(records):02d}_{re.sub(r'[^a-z0-9]+', '_', label.lower())[:40]}.png"
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
        "links": links[:40],
        "ctas": list(dict.fromkeys(ctas))[:30],
        "headings": headings[:30],
        "screenshot": str(shot) if shot else None,
    }
    records.append(rec)
    print(f"\n===== {label} =====\nURL: {page.url}\nTITLE: {page.title()}")
    print("CTAs:", rec["ctas"][:15])
    print("HEAD:", headings[:12])
    print(text[:1200])
    return rec


def login(page) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    with page.expect_navigation(wait_until="domcontentloaded"):
        page.click('input[name="submit"], button[type="submit"]')


def click_label(page, text: str) -> bool:
    # Prefer visible card/label click for radio options
    loc = page.locator(f"label:has-text('{text}'), .wizard-option:has-text('{text}'), button:has-text('{text}'), a:has-text('{text}')")
    if loc.count():
        try:
            loc.first.click(force=True, timeout=5000)
            page.wait_for_timeout(300)
            return True
        except Exception:
            pass
    return False


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        page.set_default_timeout(15000)
        login(page)
        snip(page, "A_console_home")

        # Natural discovery: Content nav
        content = page.locator('a:has-text("Content")').first
        content.click()
        page.wait_for_load_state("domcontentloaded")
        snip(page, "B_content_nav")

        # Also open Manage content quick action path from home
        page.goto(f"{BASE}/console/", wait_until="domcontentloaded")
        mc = page.locator('a:has-text("Manage content")')
        if mc.count():
            mc.first.click()
            page.wait_for_load_state("domcontentloaded")
            snip(page, "C_manage_content")

        # Direct studio index (route under console)
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "D_studio_index")

        # Create subject if CTA present
        create = page.locator(
            'a:has-text("Create Subject"), button:has-text("Create Subject"), '
            'a:has-text("New Subject"), button:has-text("Create subject")'
        )
        if create.count():
            create.first.click()
            page.wait_for_load_state("domcontentloaded")
            snip(page, "E_create_subject_form")
            # Dump inputs
            for el in page.locator("input, select, textarea").all()[:25]:
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
            # Fill common fields
            mapping = {
                "code": "CS1",
                "subject_code": "CS1",
                "name": "CS1 Actuarial Statistics",
                "subject_name": "CS1 Actuarial Statistics",
                "title": "CS1 Actuarial Statistics",
                "display_name": "CS1 Actuarial Statistics",
                "description": "IFoA CS1 for founder blind review",
                "exam_body": "IFoA",
                "board": "IFoA",
            }
            for name, value in mapping.items():
                loc = page.locator(f'[name="{name}"]')
                if not loc.count():
                    continue
                tag = loc.first.evaluate("e=>e.tagName")
                try:
                    if tag == "SELECT":
                        # try value or first real option
                        try:
                            loc.first.select_option(value=value)
                        except Exception:
                            if loc.first.locator("option").count() > 1:
                                loc.first.select_option(index=1)
                    else:
                        loc.first.fill(value)
                except Exception as e:
                    print("fill", name, e)
            submit = page.locator(
                'button:has-text("Create"), button[type="submit"], input[type="submit"]'
            )
            if submit.count():
                submit.first.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(800)
            snip(page, "F_after_create_subject")
        else:
            snip(page, "E_no_create_subject_cta")

        # Create workspace / open existing
        for sel in [
            'a:has-text("Create Workspace")',
            'button:has-text("Create Workspace")',
            'a:has-text("New Workspace")',
            'button:has-text("Create workspace")',
            'a:has-text("Open")',
            'a:has-text("CS1")',
        ]:
            loc = page.locator(sel)
            if loc.count() and loc.first.is_visible():
                try:
                    loc.first.click()
                    page.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(500)
                    snip(page, f"G_click_{sel[:40]}")
                    break
                except Exception:
                    pass

        # If create workspace form
        for name, value in [
            ("name", "CS1 Founder Workspace"),
            ("workspace_name", "CS1 Founder Workspace"),
            ("label", "CS1 Founder Workspace"),
        ]:
            loc = page.locator(f'input[name="{name}"]')
            if loc.count():
                loc.first.fill(value)
        ws_submit = page.locator(
            'button:has-text("Create Workspace"), button:has-text("Create"), button[type="submit"]'
        )
        if ws_submit.count() and "workspace" in page.inner_text("body").lower():
            ws_submit.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(800)
            snip(page, "H_after_workspace")

        # Upload documents
        dummy_syl = OUT / "dummy_syllabus.pdf"
        dummy_cmp = OUT / "dummy_cmp.pdf"
        pdf = b"%PDF-1.4\n1 0 obj<< /Type /Catalog >>endobj\ntrailer<<>>\n%%EOF\n"
        dummy_syl.write_bytes(pdf)
        dummy_cmp.write_bytes(pdf)
        file_inputs = page.locator('input[type="file"]')
        print("file inputs", file_inputs.count())
        snip(page, "I_before_upload")
        if file_inputs.count():
            # slot 0 syllabus
            file_inputs.nth(0).set_input_files(str(dummy_syl))
            page.wait_for_timeout(2000)
            snip(page, "J_syllabus_selected")
            up = page.locator('button:has-text("Upload"), button:has-text("Upload Documents")')
            if up.count():
                up.first.click()
                page.wait_for_timeout(2500)
            snip(page, "K_after_syllabus_upload")
            if file_inputs.count() >= 2:
                file_inputs.nth(1).set_input_files(str(dummy_cmp))
                page.wait_for_timeout(2000)
                if up.count():
                    up.first.click()
                    page.wait_for_timeout(2500)
                snip(page, "L_after_cmp_upload")
            else:
                # try second upload on same or next available
                file_inputs.nth(0).set_input_files(str(dummy_cmp))
                page.wait_for_timeout(2000)
                snip(page, "L_second_file_same_input")

        # Review / publish actions visible
        for label, sels in [
            (
                "M_advance",
                ['button:has-text("Advance")', 'button:has-text("Next stage")'],
            ),
            (
                "N_validate",
                ['button:has-text("Validate")', 'button:has-text("Run validation")'],
            ),
            ("O_preview", ['button:has-text("Preview")']),
            ("P_approve", ['button:has-text("Approve")']),
            ("Q_publish", ['button:has-text("Publish")']),
        ]:
            for sel in sels:
                loc = page.locator(sel)
                if loc.count() and loc.first.is_visible():
                    try:
                        loc.first.click()
                        page.wait_for_timeout(1200)
                        snip(page, label)
                        break
                    except Exception as e:
                        print("action fail", label, e)

        snip(page, "R_studio_final_state")

        # ---- Student path: skip onboarding, study plan, session ----
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "S_student_entry")
        # Skip onboarding if present
        skip = page.locator('a:has-text("Skip for now"), button:has-text("Skip for now")')
        if skip.count():
            skip.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(500)
            snip(page, "T_after_skip_onboarding")
        else:
            # Continue through
            for i in range(7):
                cont = page.locator(
                    'button:has-text("Continue to Home"), button:has-text("Continue"), a:has-text("Continue")'
                )
                if cont.count() and (
                    "onboarding" in page.url or "Welcome to Kwalitec" in page.inner_text("body")
                ):
                    cont.first.click()
                    page.wait_for_load_state("domcontentloaded")
                    page.wait_for_timeout(400)
                    snip(page, f"T_onboard_{i}")
                else:
                    break

        snip(page, "U_student_home")

        # Study plan wizard with proper label clicks
        page.goto(f"{BASE}/study-plan/wizard/1", wait_until="domcontentloaded")
        snip(page, "V_wizard1")
        click_label(page, "IFoA")
        nxt = page.locator('button:has-text("Next"), a:has-text("Next")')
        if nxt.count():
            nxt.first.click(force=True)
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(600)
        snip(page, "V_wizard1_after")

        # subsequent steps: pick CS1 if shown, fill dates, etc.
        for step in range(2, 9):
            body = page.inner_text("body")
            print("WIZARD URL", page.url)
            # click CS1 card if present
            click_label(page, "CS1")
            # dates
            for name in ["exam_date", "target_exam_date", "start_date"]:
                loc = page.locator(f'input[name="{name}"]')
                if loc.count():
                    try:
                        loc.first.fill("2026-09-15")
                    except Exception:
                        pass
            for name in ["hours_per_week", "weekly_hours", "study_hours"]:
                loc = page.locator(f'input[name="{name}"]')
                if loc.count():
                    try:
                        loc.first.fill("12")
                    except Exception:
                        pass
            # select first real option on selects
            for i in range(min(page.locator("select").count(), 5)):
                sel = page.locator("select").nth(i)
                try:
                    if sel.locator("option").count() > 1:
                        sel.select_option(index=1)
                except Exception:
                    pass
            # click option cards
            cards = page.locator(".wizard-option, label.wizard-option, .wizard-option-body")
            if cards.count():
                try:
                    cards.first.click(force=True)
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
                    print("next fail", e)
            snip(page, f"W_wizard_step_{step}")
            if "wizard" not in page.url:
                break
            if page.url == before:
                # stuck
                snip(page, f"W_wizard_stuck_{step}")
                break

        # Student home + session
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "X_student_home_post_plan")
        # Explain
        expl = page.locator('button:has-text("Explain"), a:has-text("Explain")')
        if expl.count():
            expl.first.click()
            page.wait_for_timeout(800)
            snip(page, "Y_explain")
        start = page.locator(
            'button:has-text("Start Session"), a:has-text("Start Session"), '
            'button:has-text("Start Study Session")'
        )
        if start.count():
            start.first.click()
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)
            snip(page, "Z_session_started")
            # begin
            begin = page.locator(
                'button:has-text("Begin"), a:has-text("Begin"), button:has-text("Continue")'
            )
            if begin.count():
                begin.first.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(800)
                snip(page, "Z_session_begun")
            # finish if available
            fin = page.locator(
                'button:has-text("Finish Study Session"), button:has-text("Finish"), '
                'a:has-text("Finish Study Session")'
            )
            if fin.count():
                page.once("dialog", lambda d: d.accept())
                fin.first.click()
                page.wait_for_load_state("domcontentloaded")
                page.wait_for_timeout(1000)
                snip(page, "Z_session_finished")
        snip(page, "ZZ_final")

        browser.close()

    (OUT / "focus.json").write_text(json.dumps(records, indent=2))
    print("\nWROTE", len(records), OUT / "focus.json")


if __name__ == "__main__":
    main()
