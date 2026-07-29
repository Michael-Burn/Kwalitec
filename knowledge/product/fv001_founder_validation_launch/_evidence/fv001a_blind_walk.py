"""FV-001A blind founder acceptance walkthrough — visible UX capture only."""

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

phases: list[dict] = []
timeline: list[dict] = []
term_hits: list[dict] = []
FORBIDDEN_TERMS = [
    "SCI",
    "Runtime",
    "Twin",
    "Educational Decision",
    "Educational Intelligence",
    "Experience Model",
    "Learner Lifecycle",
    "Inference",
    "CKG",
    "Digital Twin",
    "Preferred Authority",
]

t0 = time.time()


def elapsed() -> float:
    return round(time.time() - t0, 1)


def snip(page, label: str, n: int = 2800) -> dict:
    text = page.inner_text("body")
    clean = re.sub(r"\n{3,}", "\n\n", text).strip()
    links = []
    for a in page.locator("a").all()[:50]:
        try:
            t = a.inner_text().strip()
            h = a.get_attribute("href") or ""
            if t:
                links.append({"text": t[:80], "href": h[:140]})
        except Exception:
            pass
    buttons: list[str] = []
    for sel in ["button", "input[type=submit]", "a.btn"]:
        for el in page.locator(sel).all()[:30]:
            try:
                t = (el.inner_text() or el.get_attribute("value") or "").strip()
                if t:
                    buttons.append(t[:100])
            except Exception:
                pass
    found = []
    for term in FORBIDDEN_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", text, re.I):
            found.append(term)
            term_hits.append({"phase": label, "term": term, "url": page.url})
    shot = OUT / f"{len(phases):02d}_{re.sub(r'[^a-z0-9]+', '_', label.lower())[:45]}.png"
    try:
        page.screenshot(path=str(shot), full_page=True)
    except Exception:
        shot = None
    rec = {
        "phase": label,
        "t": elapsed(),
        "url": page.url,
        "title": page.title(),
        "text": clean[:n],
        "text_len": len(clean),
        "links": links[:30],
        "ctas": list(dict.fromkeys(buttons))[:25],
        "terms_found": found,
        "screenshot": str(shot) if shot else None,
    }
    phases.append(rec)
    timeline.append(
        {"t": elapsed(), "phase": label, "url": page.url, "title": page.title()}
    )
    print(f"\n===== {label} t={elapsed()}s =====")
    print("URL:", page.url)
    print("TITLE:", page.title())
    print("CTAs:", rec["ctas"][:12])
    print("TERMS:", found)
    print(clean[:1100].replace("\n\n", "\n"))
    return rec


def try_click(page, selectors, timeout: int = 4000):
    for sel in selectors:
        loc = page.locator(sel)
        if loc.count() and loc.first.is_visible():
            try:
                with page.expect_navigation(
                    wait_until="domcontentloaded", timeout=timeout
                ):
                    loc.first.click(timeout=timeout)
                return True, sel
            except Exception:
                try:
                    loc.first.click(timeout=timeout)
                    page.wait_for_timeout(500)
                    return True, sel
                except Exception:
                    continue
    return False, None


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.set_default_timeout(15000)

        # PHASE 1
        page.goto(f"{BASE}/", wait_until="domcontentloaded")
        snip(page, "PHASE1_root")
        page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
        snip(page, "PHASE1_landing_login")
        body = page.inner_text("body").lower()
        reg_links = [
            l
            for l in phases[-1]["links"]
            if any(
                k in (l["text"] + l["href"]).lower()
                for k in ["register", "sign up", "signup", "create account"]
            )
        ]
        phases[-1]["registration_visible"] = any(
            x in body for x in ["create account", "sign up", "register"]
        ) or bool(reg_links)
        phases[-1]["registration_links"] = reg_links

        # PHASE 2 — natural registration attempts
        for path in ["/auth/register", "/register", "/signup", "/auth/signup", "/join"]:
            resp = page.goto(f"{BASE}{path}", wait_until="domcontentloaded")
            snip(page, f"PHASE2_try_{path.strip('/').replace('/', '_')}")
            phases[-1]["status"] = resp.status if resp else None

        # Methodological exception: continue with provisioned invite credentials
        page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        with page.expect_navigation(wait_until="domcontentloaded"):
            page.click('input[name="submit"], button[type="submit"]')
        snip(page, "PHASE2_after_provisioned_login")

        # PHASE 3
        snip(page, "PHASE3_post_login_home")
        print(
            "founder links",
            page.locator('a[href*="/founder"]').count(),
            "studio links",
            page.locator('a[href*="curriculum"], a:has-text("Curriculum Studio")').count(),
        )
        clicked, sel = try_click(
            page,
            [
                'a:has-text("Curriculum Studio")',
                'a:has-text("Founder Console")',
                'a:has-text("Console")',
                'a[href="/founder/"]',
                'a[href*="/founder"]',
            ],
        )
        if clicked:
            snip(page, "PHASE3_nav_click")
        else:
            snip(page, "PHASE3_no_console_link_visible")
            page.goto(f"{BASE}/founder/", wait_until="domcontentloaded")
            snip(page, "PHASE3_founder_direct_NOTE_HIDDEN_ROUTE")

        # PHASE 4 — Create Subject
        page.goto(f"{BASE}/curriculum-studio/", wait_until="domcontentloaded")
        snip(page, "PHASE4_curriculum_studio_index")
        clicked, _ = try_click(
            page,
            [
                'a:has-text("Create Subject")',
                'button:has-text("Create Subject")',
                'a:has-text("New Subject")',
                'button:has-text("New Subject")',
                'a:has-text("Add Subject")',
                'a:has-text("Create subject")',
                'button:has-text("Create subject")',
            ],
        )
        if clicked:
            snip(page, "PHASE4_create_subject_form")
            for name, value in [
                ("subject_code", "CS1"),
                ("code", "CS1"),
                ("name", "CS1 — Actuarial Statistics"),
                ("subject_name", "CS1 — Actuarial Statistics"),
                ("title", "CS1 — Actuarial Statistics"),
                ("description", "IFoA CS1 Actuarial Statistics"),
                ("display_name", "CS1 — Actuarial Statistics"),
            ]:
                loc = page.locator(f'input[name="{name}"], textarea[name="{name}"]')
                if loc.count():
                    loc.first.fill(value)
            selects = page.locator("select")
            for i in range(min(selects.count(), 6)):
                try:
                    opts = selects.nth(i).locator("option").all_inner_texts()
                    print("select", i, opts[:8])
                    for o in opts:
                        if o.strip() and "select" not in o.lower():
                            selects.nth(i).select_option(label=o)
                            break
                except Exception as e:
                    print("select err", e)
            try_click(
                page,
                [
                    'button:has-text("Create")',
                    'input[type="submit"]',
                    'button[type="submit"]',
                    'button:has-text("Save")',
                ],
                timeout=10000,
            )
            page.wait_for_timeout(1000)
            snip(page, "PHASE4_after_create_subject")
        else:
            # Maybe inline form on index
            forms = page.locator("form")
            print("forms on studio index", forms.count())
            snip(page, "PHASE4_create_subject_NOT_FOUND_or_inline")
            for name, value in [
                ("subject_code", "CS1"),
                ("code", "CS1"),
                ("name", "CS1 — Actuarial Statistics"),
                ("subject_name", "CS1 — Actuarial Statistics"),
            ]:
                loc = page.locator(f'input[name="{name}"], textarea[name="{name}"]')
                if loc.count():
                    loc.first.fill(value)
            try_click(
                page,
                [
                    'button:has-text("Create")',
                    'button[type="submit"]',
                    'input[type="submit"]',
                ],
            )
            page.wait_for_timeout(800)
            snip(page, "PHASE4_after_inline_attempt")

        # Workspace
        try_click(
            page,
            [
                'a:has-text("Open")',
                'a:has-text("Workspace")',
                'a:has-text("CS1")',
                'button:has-text("Create Workspace")',
                'a:has-text("Create Workspace")',
                'button:has-text("New Workspace")',
            ],
        )
        page.wait_for_timeout(600)
        snip(page, "PHASE5_workspace_entry")
        for name, value in [
            ("name", "CS1 Workspace"),
            ("workspace_name", "CS1 Workspace"),
            ("label", "CS1 Workspace"),
        ]:
            loc = page.locator(f'input[name="{name}"]')
            if loc.count():
                loc.first.fill(value)
        try_click(
            page,
            [
                'button:has-text("Create Workspace")',
                'button:has-text("Create")',
                'button[type="submit"]',
                'input[type="submit"]',
            ],
        )
        page.wait_for_timeout(800)
        snip(page, "PHASE5_after_workspace")

        # PHASE 5/6 uploads
        dummy_syl = OUT / "dummy_syllabus.pdf"
        dummy_cmp = OUT / "dummy_cmp.pdf"
        pdf = b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"
        dummy_syl.write_bytes(pdf)
        dummy_cmp.write_bytes(pdf)
        file_inputs = page.locator('input[type="file"]')
        print("file inputs", file_inputs.count())
        if file_inputs.count() >= 1:
            file_inputs.nth(0).set_input_files(str(dummy_syl))
            page.wait_for_timeout(1500)
            snip(page, "PHASE5_after_syllabus_file_select")
            try_click(
                page,
                [
                    'button:has-text("Upload")',
                    'button:has-text("Submit")',
                    'button[type="submit"]',
                ],
            )
            page.wait_for_timeout(2500)
            snip(page, "PHASE5_after_syllabus_upload")
        if file_inputs.count() >= 2:
            file_inputs.nth(1).set_input_files(str(dummy_cmp))
            page.wait_for_timeout(1500)
            try_click(
                page,
                ['button:has-text("Upload")', 'button[type="submit"]'],
            )
            page.wait_for_timeout(2500)
            snip(page, "PHASE6_after_cmp_upload")
        elif file_inputs.count() == 1:
            file_inputs.nth(0).set_input_files(str(dummy_cmp))
            page.wait_for_timeout(1500)
            try_click(
                page,
                ['button:has-text("Upload")', 'button[type="submit"]'],
            )
            page.wait_for_timeout(2500)
            snip(page, "PHASE6_after_cmp_upload")
        else:
            snip(page, "PHASE5_6_upload_inputs_NOT_FOUND")

        # PHASE 7/8
        try_click(
            page,
            [
                'a:has-text("Review")',
                'button:has-text("Review")',
                'a:has-text("Preview")',
                'button:has-text("Preview")',
                'a:has-text("Validate")',
                'button:has-text("Validate")',
                'a:has-text("Advance")',
                'button:has-text("Advance")',
                'button:has-text("Run")',
            ],
        )
        page.wait_for_timeout(800)
        snip(page, "PHASE7_curriculum_review")
        try_click(
            page,
            [
                'button:has-text("Publish")',
                'a:has-text("Publish")',
                'button:has-text("Approve")',
                'a:has-text("Approve")',
            ],
        )
        page.wait_for_timeout(1000)
        snip(page, "PHASE8_publish")

        # PHASE 9 — student / study plan
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "PHASE9_student_home")
        page.goto(f"{BASE}/study-plan/", wait_until="domcontentloaded")
        snip(page, "PHASE9_study_plan_index")
        page.goto(f"{BASE}/study-plan/wizard/1", wait_until="domcontentloaded")
        snip(page, "PHASE9_wizard_step1")
        for step in range(1, 8):
            for name, value in [
                ("exam_date", "2026-09-15"),
                ("weekly_hours", "10"),
                ("study_days", "5"),
                ("session_length", "60"),
                ("target_grade", "Pass"),
            ]:
                loc = page.locator(f'input[name="{name}"], select[name="{name}"]')
                if loc.count():
                    tag = loc.first.evaluate("e => e.tagName")
                    if tag == "SELECT":
                        try:
                            loc.first.select_option(index=1)
                        except Exception:
                            pass
                    else:
                        try:
                            loc.first.fill(value)
                        except Exception:
                            pass
            checks = page.locator('input[type="checkbox"]')
            for i in range(min(checks.count(), 4)):
                try:
                    if not checks.nth(i).is_checked():
                        checks.nth(i).check()
                except Exception:
                    pass
            radios = page.locator('input[type="radio"]')
            if radios.count():
                try:
                    radios.first.check()
                except Exception:
                    pass
            selects = page.locator("select")
            for i in range(min(selects.count(), 5)):
                try:
                    if selects.nth(i).locator("option").count() > 1:
                        selects.nth(i).select_option(index=1)
                except Exception:
                    pass
            before = page.url
            try_click(
                page,
                [
                    'button:has-text("Continue")',
                    'button:has-text("Next")',
                    'input[value="Continue"]',
                    'button[type="submit"]',
                    'input[type="submit"]',
                    'button:has-text("Create")',
                    'button:has-text("Finish")',
                    'button:has-text("Confirm")',
                ],
                timeout=10000,
            )
            page.wait_for_timeout(700)
            snip(page, f"PHASE9_wizard_after_step_{step}")
            if page.url == before and step > 2:
                break
            if "wizard" not in page.url and step > 1:
                break

        # PHASE 10
        page.goto(f"{BASE}/dashboard/", wait_until="domcontentloaded")
        snip(page, "PHASE10_dashboard")
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "PHASE10_student_home_dashboard")

        # PHASE 11
        try_click(
            page,
            [
                'a:has-text("Today")',
                'a:has-text("Mission")',
                'button:has-text("Start")',
                'a:has-text("Start")',
                'button:has-text("Begin")',
                'a:has-text("Open Mission")',
            ],
        )
        page.goto(f"{BASE}/missions/", wait_until="domcontentloaded")
        snip(page, "PHASE11_missions")

        # PHASE 12
        try_click(
            page,
            [
                'button:has-text("Start Study Session")',
                'a:has-text("Start Study Session")',
                'button:has-text("Start Session")',
                'a:has-text("Start Session")',
                'button:has-text("Begin")',
                'form[action*="session"] button',
                'form[action*="session/start"] button',
            ],
            timeout=10000,
        )
        page.wait_for_timeout(1000)
        snip(page, "PHASE12_study_session")
        try_click(
            page,
            [
                'button:has-text("Begin")',
                'a:has-text("Begin")',
                'button:has-text("Continue")',
                'button:has-text("Start")',
                'button:has-text("Next")',
            ],
        )
        page.wait_for_timeout(800)
        snip(page, "PHASE12_session_active")

        # PHASE 13
        try_click(
            page,
            [
                'button:has-text("Finish Study Session")',
                'a:has-text("Finish Study Session")',
                'button:has-text("Finish")',
                'a:has-text("Finish")',
                'button:has-text("Complete")',
            ],
        )
        page.wait_for_timeout(1000)
        snip(page, "PHASE13_session_completion")

        # PHASE 14
        for path in [
            "/student/revision",
            "/student/revision/",
            "/revision",
            "/analytics/",
        ]:
            try:
                page.goto(f"{BASE}{path}", wait_until="domcontentloaded", timeout=8000)
                snip(page, f"PHASE14_{path.strip('/').replace('/', '_') or 'root'}")
            except Exception as e:
                print("revision path fail", path, e)

        # PHASE 15
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        clicked, _ = try_click(
            page,
            [
                'a:has-text("Coach")',
                'a:has-text("Ask")',
                'button:has-text("Coach")',
                'a:has-text("Help")',
                'a:has-text("Insights")',
            ],
        )
        if clicked:
            snip(page, "PHASE15_coach_from_nav")
        else:
            snip(page, "PHASE15_coach_NOT_DISCOVERABLE")
        for path in ["/student/coach", "/coach", "/alpha/help"]:
            try:
                page.goto(f"{BASE}{path}", wait_until="domcontentloaded", timeout=8000)
                snip(page, f"PHASE15_try_{path.strip('/').replace('/', '_')}")
            except Exception:
                pass

        # PHASE 16
        clicked, _ = try_click(
            page,
            [
                'button:has-text("Sign out")',
                'a:has-text("Sign out")',
                'button:has-text("Log out")',
                'a:has-text("Log out")',
                'form[action*="logout"] button',
            ],
        )
        if not clicked and page.locator('form[action*="logout"]').count():
            page.locator('form[action*="logout"]').first.evaluate("f => f.submit()")
            page.wait_for_timeout(800)
        snip(page, "PHASE16_after_logout")
        page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        with page.expect_navigation(wait_until="domcontentloaded"):
            page.click('input[name="submit"], button[type="submit"]')
        snip(page, "PHASE16_return_login")
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "PHASE16_return_student_home")

        browser.close()

    (OUT / "phases.json").write_text(
        json.dumps(
            {
                "phases": phases,
                "timeline": timeline,
                "term_hits": term_hits,
                "elapsed_s": elapsed(),
            },
            indent=2,
        )
    )
    print("\nDONE phases", len(phases), "terms", len(term_hits), "elapsed", elapsed())


if __name__ == "__main__":
    main()
