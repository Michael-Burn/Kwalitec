"""Complete CS1U path via input[value] submits; capture findings + catalogue."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5130"
EV = Path(
    "/Users/kwalitec/Developer/kwalitec/knowledge/product/"
    "fv001b_rerun_validation/_evidence"
)
SHOTS = EV / "screenshots"
OUT = Path("/tmp/fv001b_rerun_capture/screenshots")
records: list[dict] = []

KEYS = (
    "NEXT STEP",
    "Preview ",
    "Validation ",
    "Checklist",
    "Stage:",
    "We have",
    "Weve",
    "We've",
    "couldn't",
    "topics",
    "Publish",
    "Approve",
    "blocking",
    "Ready",
)


def snip(page, label: str) -> dict:
    text = re.sub(r"\n{3,}", "\n\n", page.inner_text("body")).strip()
    flashes: list[str] = []
    for sel in [".alert", ".flash", "[role=alert]"]:
        for el in page.locator(sel).all()[:10]:
            try:
                t = el.inner_text().strip()
                if t:
                    flashes.append(t[:500])
            except Exception:
                pass
    findings: list[str] = []
    if "Validation findings" in text:
        findings = [
            ln.strip()
            for ln in text.split("Validation findings", 1)[1].splitlines()
            if ln.strip()
        ][:35]
    shot = OUT / f"complete_{len(records):02d}_{label}.png"
    page.screenshot(path=str(shot), full_page=True)
    shutil.copy2(shot, SHOTS / shot.name)
    rec = {
        "phase": label,
        "url": page.url,
        "flashes": flashes,
        "findings": findings,
        "text": text[:7000],
        "screenshot": str(shot),
    }
    records.append(rec)
    print(f"\n===== {label} =====")
    print("FLASH", flashes[:2])
    print("FINDINGS", findings[:12])
    for ln in text.splitlines():
        if any(x in ln for x in KEYS) and ln.strip():
            print(">", ln.strip()[:170])
    return rec


def click_value(page, value: str) -> bool:
    loc = page.locator(f'input[type=submit][value="{value}"]')
    if not loc.count():
        print("missing", value)
        return False
    loc.first.scroll_into_view_if_needed()
    loc.first.click()
    page.wait_for_timeout(3500)
    return True


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 1200}).new_page()
        page.goto(f"{BASE}/auth/login")
        page.fill('input[name=email]', "founder.studio@kwalitec.example")
        page.fill('input[name=password]', "StudioBlind2026!")
        with page.expect_navigation():
            page.click('input[name=submit], button[type=submit]')

        page.goto(
            f"{BASE}/console/studio/workspaces/ws-cs1u",
            wait_until="networkidle",
        )
        snip(page, "C0_open")

        click_value(page, "Advance to Next Stage")
        snip(page, "C1_advance")
        click_value(page, "Validate Curriculum")
        snip(page, "C2_validate")
        click_value(page, "Build Preview")
        snip(page, "C3_preview")

        loc = page.locator(
            'button:has-text("CURRICULUM STRUCTURE"), a:has-text("CURRICULUM STRUCTURE")'
        )
        if loc.count():
            loc.first.click()
            page.wait_for_timeout(800)
            snip(page, "C3_structure")

        click_value(page, "Approve Curriculum")
        snip(page, "C4_approve")

        note = page.locator(
            "textarea[name=reason], textarea[name=note], input[name=reason]"
        )
        if note.count():
            note.first.fill("FV-001B re-run publish attempt")
        click_value(page, "Publish Verified Curriculum")
        snip(page, "C5_publish")
        page.wait_for_timeout(2000)
        page.reload(wait_until="domcontentloaded")
        snip(page, "C5_publish_reload")

        page.goto(f"{BASE}/console/studio/subjects")
        snip(page, "C6_subjects")
        page.goto(f"{BASE}/student/")
        snip(page, "C6_student")

        page.goto(f"{BASE}/console/studio/workspaces/ws-cs1t")
        snip(page, "C7_incomplete")
        click_value(page, "Publish Verified Curriculum")
        snip(page, "C7_incomplete_publish")
        click_value(page, "Approve Curriculum")
        snip(page, "C7_incomplete_approve")
        click_value(page, "Build Preview")
        snip(page, "C7_incomplete_preview")

        browser.close()

    (EV / "complete.json").write_text(json.dumps({"records": records}, indent=2))
    print("WROTE", len(records))


if __name__ == "__main__":
    main()
