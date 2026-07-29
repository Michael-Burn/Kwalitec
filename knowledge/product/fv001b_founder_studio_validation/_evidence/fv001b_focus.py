"""FV-001B focus — open CS1B workspace and exercise upload/review/publish."""

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
EVIDENCE = Path(
    "/Users/kwalitec/Developer/kwalitec/knowledge/product/"
    "fv001b_founder_studio_validation/_evidence"
)
SYLLABUS = OUT / "official_syllabus.pdf"
CMP = OUT / "official_cmp.pdf"

FORBIDDEN = [
    "SCI", "Runtime", "Twin", "Educational Decision", "Educational Intelligence",
    "Experience Model", "Learner Lifecycle", "Inference", "CKG", "Digital Twin",
    "Preferred Authority", "Knowledge Graph", "Pipeline", "Entity Details",
]

records: list[dict] = []
term_hits: list[dict] = []
t0 = time.time()


def elapsed() -> float:
    return round(time.time() - t0, 1)


def snip(page, label: str, n: int = 5000) -> dict:
    text = re.sub(r"\n{3,}", "\n\n", page.inner_text("body")).strip()
    flashes = []
    for sel in [".alert", ".flash", "[role=alert]", ".toast"]:
        for el in page.locator(sel).all()[:12]:
            try:
                t = el.inner_text().strip()
                if t:
                    flashes.append(t[:350])
            except Exception:
                pass
    ctas = []
    for sel in ["button", "input[type=submit]", "a.btn", "[role=button]"]:
        for el in page.locator(sel).all()[:60]:
            try:
                t = (el.inner_text() or el.get_attribute("value") or "").strip()
                if t:
                    ctas.append(t[:140])
            except Exception:
                pass
    tabs = []
    for sel in ["[role=tab]", "nav a", ".tabs a", ".tab"]:
        for el in page.locator(sel).all()[:40]:
            try:
                t = el.inner_text().strip()
                if t:
                    tabs.append(t[:80])
            except Exception:
                pass
    headings = []
    for sel in ["h1", "h2", "h3"]:
        for el in page.locator(sel).all()[:25]:
            try:
                t = el.inner_text().strip()
                if t:
                    headings.append(t[:160])
            except Exception:
                pass
    labels = []
    for el in page.locator("label").all()[:40]:
        try:
            t = el.inner_text().strip()
            if t:
                labels.append(t[:140])
        except Exception:
            pass
    found = [term for term in FORBIDDEN if re.search(rf"\b{re.escape(term)}\b", text, re.I)]
    for term in found:
        term_hits.append({"phase": label, "term": term, "url": page.url})
    shot = OUT / f"focus_{len(records):02d}_{re.sub(r'[^a-z0-9]+', '_', label.lower())[:45]}.png"
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
        "flashes": flashes,
        "ctas": list(dict.fromkeys(ctas))[:40],
        "tabs": list(dict.fromkeys(tabs))[:30],
        "headings": list(dict.fromkeys(headings))[:25],
        "labels": list(dict.fromkeys(labels))[:30],
        "terms_found": found,
        "screenshot": str(shot) if shot else None,
    }
    records.append(rec)
    print(f"\n===== {label} =====\nURL: {page.url}\nH: {rec['headings'][:8]}\nFLASH: {flashes[:2]}\nCTAs: {rec['ctas'][:16]}\nTABS: {rec['tabs'][:16]}\nTERMS: {found}")
    print(text[:1500])
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
        page = browser.new_context(viewport={"width": 1440, "height": 900}).new_page()
        page.set_default_timeout(30000)
        login(page)

        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "01_studio")

        # Open existing CS1B workspace from list
        ws = page.locator('a:has-text("CS1B"), a:has-text("Content Sources"), a:has-text("2026.1")')
        print("workspace anchors", ws.count())
        if ws.count():
            with page.expect_navigation(wait_until="domcontentloaded"):
                ws.first.click()
            snip(page, "02_workspace_opened")
        else:
            # Try any workspace row link
            row = page.locator("table a, .workspace a, li a").filter(has_text=re.compile("CS1B|ws-", re.I))
            print("row links", row.count())
            if row.count():
                with page.expect_navigation(wait_until="domcontentloaded"):
                    row.first.click()
                snip(page, "02_workspace_row")
            else:
                snip(page, "02_workspace_not_found")

        # Capture all visible chrome on workspace
        snip(page, "03_workspace_state")
        files = page.locator('input[type="file"]')
        print("file inputs", files.count())
        records[-1]["file_input_count"] = files.count()

        # Re-upload if slots empty / failed
        if files.count() >= 1:
            files.nth(0).set_input_files(str(SYLLABUS))
            page.wait_for_timeout(2000)
            snip(page, "04_syllabus")
        if files.count() >= 2:
            files.nth(1).set_input_files(str(CMP))
            page.wait_for_timeout(2000)
            snip(page, "05_cmp")

        # Click every meaningful workflow control once
        for text in [
            "Upload Documents", "Upload", "Advance", "Extract", "Run Extraction",
            "Validate", "Preview", "Review", "Approve", "Verify", "Correct",
            "Publish", "Make Ready",
        ]:
            loc = page.locator(
                f'button:has-text("{text}"), input[value*="{text}"], a.btn:has-text("{text}")'
            )
            visible = [i for i in range(loc.count()) if loc.nth(i).is_visible()]
            if not visible:
                continue
            reason = page.locator('input[name="reason"], textarea[name="reason"]')
            if text == "Publish" and reason.count():
                reason.first.fill("FV-001B publish attempt after review")
            try:
                loc.nth(visible[0]).click()
                page.wait_for_timeout(2200)
                snip(page, f"06_action_{text.replace(' ', '_')}")
            except Exception as e:
                print("fail", text, e)

        # Explore tabs / secondary surfaces
        for text in [
            "Content Sources", "Pipeline", "Validation", "Preview", "Approval",
            "Publish", "Knowledge Graph", "Evidence", "Issues", "Structure",
            "Documents", "Curriculum", "Review",
        ]:
            loc = page.locator(f'a:has-text("{text}"), [role=tab]:has-text("{text}"), button:has-text("{text}")')
            if loc.count() and loc.first.is_visible():
                try:
                    loc.first.click()
                    page.wait_for_timeout(1000)
                    snip(page, f"07_tab_{text.replace(' ', '_')}")
                except Exception as e:
                    print("tab fail", text, e)

        # Final workspace snapshot
        page.reload(wait_until="domcontentloaded")
        snip(page, "08_workspace_final")

        # Subjects + Publishing surfaces
        page.goto(f"{BASE}/console/studio/subjects", wait_until="domcontentloaded")
        snip(page, "09_subjects")
        page.goto(f"{BASE}/console/studio/publishing", wait_until="domcontentloaded")
        snip(page, "10_publishing")
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "11_studio_final")

        browser.close()

    payload = {
        "programme": "FV-001B",
        "kind": "focus",
        "elapsed_s": elapsed(),
        "records": records,
        "term_hits": term_hits,
    }
    path = EVIDENCE / "focus.json"
    path.write_text(json.dumps(payload, indent=2))
    (OUT / "focus.json").write_text(json.dumps(payload, indent=2))
    print("\nWROTE", path, len(records), "term_hits", term_hits)


if __name__ == "__main__":
    main()
