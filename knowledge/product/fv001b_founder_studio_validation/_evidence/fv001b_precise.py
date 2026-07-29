"""FV-001B precise Founder Studio workflow — visible UX only."""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5130"
EMAIL = "founder.studio@kwalitec.example"
PASSWORD = "StudioBlind2026!"
OUT = Path("/tmp/fv001b_blind_capture")
OUT.mkdir(parents=True, exist_ok=True)
EVIDENCE = Path(
    "/Users/kwalitec/Developer/kwalitec/knowledge/product/"
    "fv001b_founder_studio_validation/_evidence"
)
EVIDENCE.mkdir(parents=True, exist_ok=True)

SYLLABUS = OUT / "official_syllabus.pdf"
CMP = OUT / "official_cmp.pdf"

FORBIDDEN = [
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
    "Knowledge Graph",
]

records: list[dict] = []
term_hits: list[dict] = []
t0 = time.time()


def elapsed() -> float:
    return round(time.time() - t0, 1)


def snip(page, label: str, n: int = 4500) -> dict:
    text = re.sub(r"\n{3,}", "\n\n", page.inner_text("body")).strip()
    flashes = []
    for sel in [".alert", ".flash", "[role=alert]", ".toast", ".banner"]:
        for el in page.locator(sel).all()[:12]:
            try:
                t = el.inner_text().strip()
                if t:
                    flashes.append(t[:300])
            except Exception:
                pass
    ctas: list[str] = []
    for sel in ["button", "input[type=submit]", "a.btn", "[role=button]"]:
        for el in page.locator(sel).all()[:50]:
            try:
                t = (el.inner_text() or el.get_attribute("value") or "").strip()
                if t:
                    ctas.append(t[:120])
            except Exception:
                pass
    links = []
    for a in page.locator("a").all()[:40]:
        try:
            t = a.inner_text().strip()
            h = a.get_attribute("href") or ""
            if t:
                links.append({"text": t[:80], "href": h[:140]})
        except Exception:
            pass
    headings = []
    for sel in ["h1", "h2", "h3"]:
        for el in page.locator(sel).all()[:20]:
            try:
                t = el.inner_text().strip()
                if t:
                    headings.append(t[:160])
            except Exception:
                pass
    labels = []
    for el in page.locator("label").all()[:30]:
        try:
            t = el.inner_text().strip()
            if t:
                labels.append(t[:120])
        except Exception:
            pass
    found = []
    for term in FORBIDDEN:
        if re.search(rf"\b{re.escape(term)}\b", text, re.I):
            found.append(term)
            term_hits.append({"phase": label, "term": term, "url": page.url})
    shot = OUT / f"precise_{len(records):02d}_{re.sub(r'[^a-z0-9]+', '_', label.lower())[:45]}.png"
    try:
        page.screenshot(path=str(shot), full_page=True)
    except Exception:
        shot = None
    rec = {
        "phase": label,
        "t": elapsed(),
        "url": page.url,
        "title": page.title(),
        "text": text[:n],
        "text_len": len(text),
        "flashes": flashes,
        "ctas": list(dict.fromkeys(ctas))[:30],
        "links": links[:30],
        "headings": list(dict.fromkeys(headings))[:20],
        "labels": list(dict.fromkeys(labels))[:25],
        "terms_found": found,
        "screenshot": str(shot) if shot else None,
    }
    records.append(rec)
    print(f"\n===== {label} t={elapsed()}s =====")
    print("URL:", page.url)
    print("TITLE:", page.title())
    print("HEADINGS:", rec["headings"][:8])
    print("FLASH:", flashes[:3])
    print("CTAs:", rec["ctas"][:14])
    print("TERMS:", found)
    print(text[:1300].replace("\n\n", "\n"))
    return rec


def login(page) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
    snip(page, "P1_login")
    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    with page.expect_navigation(wait_until="domcontentloaded"):
        page.click('input[name="submit"], button[type="submit"]')
    snip(page, "P1_after_login")


def click_nav(page, text: str) -> bool:
    loc = page.locator(f'a:has-text("{text}")')
    if loc.count() and loc.first.is_visible():
        with page.expect_navigation(wait_until="domcontentloaded"):
            loc.first.click()
        return True
    return False


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.set_default_timeout(25000)

        login(page)

        # Phase 1 — founder environment cues
        snip(page, "P1_console_home")

        # Phase 2 — Subjects catalogue
        if click_nav(page, "Subjects"):
            snip(page, "P2_subjects")
        else:
            page.goto(f"{BASE}/console/subjects", wait_until="domcontentloaded")
            snip(page, "P2_subjects_direct")

        # Other authority nav surfaces (for screen review completeness)
        for label in ["Review Queue", "Publishing", "Versions", "Quality"]:
            if click_nav(page, label):
                snip(page, f"P2_nav_{label.lower().replace(' ', '_')}")

        # Curriculum Studio
        if not click_nav(page, "Curriculum Studio"):
            page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "P2_studio_index")

        # Phase 3 — Create Subject (inline form)
        create_card = page.locator(
            'section[aria-label="Create Subject or workspace"] .command-card'
        ).first
        if create_card.count():
            create_card.locator('input[name="subject_code"]').fill("CS1B")
            title = create_card.locator('input[name="title"]')
            if title.count():
                title.fill("CS1B — Actuarial Statistics (Blind)")
            # Empty-ish validation probe: capture form state
            snip(page, "P3_create_form_filled")
            with page.expect_navigation(wait_until="domcontentloaded"):
                create_card.locator(
                    'input[type="submit"], button[type="submit"]'
                ).first.click()
            snip(page, "P3_after_create_subject")
        else:
            # Fallback: any Create Subject form
            snip(page, "P3_create_card_missing_fallback")
            codes = page.locator('input[name="subject_code"]')
            if codes.count():
                codes.first.fill("CS1B")
            titles = page.locator('input[name="title"]')
            if titles.count():
                titles.first.fill("CS1B — Actuarial Statistics (Blind)")
            page.locator(
                'button:has-text("Create Subject"), input[value*="Create"]'
            ).first.click()
            page.wait_for_timeout(1200)
            snip(page, "P3_after_create_fallback")

        # Open Workspace
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "P3_studio_after_create")
        open_card = page.locator(
            'section[aria-label="Create Subject or workspace"] .command-card'
        ).nth(1)
        if open_card.count():
            open_card.locator('input[name="subject_code"]').fill("CS1B")
            with page.expect_navigation(wait_until="domcontentloaded"):
                open_card.locator(
                    'input[type="submit"], button[type="submit"]'
                ).first.click()
            snip(page, "P4_workspace_opened")
        else:
            # Click workspace link if listed
            loc = page.locator('a:has-text("CS1B"), a:has-text("Open")')
            if loc.count():
                with page.expect_navigation(wait_until="domcontentloaded"):
                    loc.first.click()
                snip(page, "P4_workspace_link")
            else:
                snip(page, "P4_workspace_open_failed")

        # Phase 4 — Upload
        snip(page, "P4_pre_upload")
        files = page.locator('input[type="file"]')
        print("file inputs", files.count())
        records[-1]["file_input_count"] = files.count()
        # Document why each slot exists from visible labels
        records[-1]["upload_labels"] = records[-1]["labels"]

        if files.count() >= 1:
            files.nth(0).set_input_files(str(SYLLABUS))
            page.wait_for_timeout(2000)
            snip(page, "P4_syllabus_selected")
        if files.count() >= 2:
            files.nth(1).set_input_files(str(CMP))
            page.wait_for_timeout(2000)
            snip(page, "P4_cmp_selected")
        for text in ["Upload Documents", "Upload", "Save Documents"]:
            loc = page.locator(f'button:has-text("{text}")')
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                page.wait_for_timeout(2500)
                snip(page, f"P4_upload_{text.replace(' ', '_')}")

        # Phase 5 — Extraction / review actions
        for text in [
            "Advance",
            "Extract",
            "Run Extraction",
            "Validate",
            "Preview",
            "Review",
            "Approve",
            "Verify",
        ]:
            loc = page.locator(
                f'button:has-text("{text}"), input[value*="{text}"], a:has-text("{text}")'
            )
            if loc.count() and loc.first.is_visible():
                try:
                    loc.first.click()
                    page.wait_for_timeout(2000)
                    snip(page, f"P5_action_{text}")
                except Exception as e:
                    print("action fail", text, e)

        # Poll progress a few times
        for i in range(3):
            page.wait_for_timeout(2500)
            page.reload(wait_until="domcontentloaded")
            snip(page, f"P5_progress_{i}")

        # Phase 6 — Publish
        reason = page.locator('input[name="reason"], textarea[name="reason"]')
        if reason.count():
            reason.first.fill("FV-001B blind validation — publish verified curriculum")
        pub = page.locator(
            'button:has-text("Publish"), input[value*="Publish"], a:has-text("Publish")'
        )
        if pub.count() and pub.first.is_visible():
            try:
                pub.first.click()
                page.wait_for_timeout(2000)
                snip(page, "P6_after_publish")
            except Exception as e:
                print("publish fail", e)
                snip(page, "P6_publish_error")
        else:
            snip(page, "P6_publish_not_visible")

        snip(page, "P6_workspace_final")

        # Phase 7 — catalogue verification
        if click_nav(page, "Subjects"):
            snip(page, "P7_subjects_catalogue")
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "P7_studio_catalogue")
        body = records[-1]["text"]
        records[-1]["cs1b_visible"] = "CS1B" in body
        records[-1]["ready_mentioned"] = bool(
            re.search(r"\bReady\b|\bPublished\b", body, re.I)
        )

        # Attempt open CS1B workspace again for version/status cues
        open_card = page.locator(
            'section[aria-label="Create Subject or workspace"] .command-card'
        ).nth(1)
        if open_card.count():
            open_card.locator('input[name="subject_code"]').fill("CS1B")
            with page.expect_navigation(wait_until="domcontentloaded"):
                open_card.locator(
                    'input[type="submit"], button[type="submit"]'
                ).first.click()
            snip(page, "P7_reopen_workspace")

        browser.close()

    payload = {
        "programme": "FV-001B",
        "kind": "precise",
        "base": BASE,
        "elapsed_s": elapsed(),
        "records": records,
        "term_hits": term_hits,
        "pdfs": {
            "syllabus_bytes": SYLLABUS.stat().st_size if SYLLABUS.exists() else 0,
            "cmp_bytes": CMP.stat().st_size if CMP.exists() else 0,
        },
    }
    path = EVIDENCE / "precise.json"
    path.write_text(json.dumps(payload, indent=2))
    (OUT / "precise.json").write_text(json.dumps(payload, indent=2))
    print("\nWROTE", path, "records", len(records), "term_hits", len(term_hits))


if __name__ == "__main__":
    main()
