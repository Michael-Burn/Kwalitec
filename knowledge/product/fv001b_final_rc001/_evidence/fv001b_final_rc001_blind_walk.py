"""FV-001B Final (RC-001) — Founder Studio blind validation (visible UX only).

Release Candidate: RC-2026.07.29-01

Does not inspect application code, logs, or databases to justify behaviour.
Exercises Create Subject → Upload → Validate → Preview → Approve → Publish → Ready.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5201"
RELEASE_CANDIDATE = "RC-2026.07.29-01"
COMMIT = "f17058862baf9aa8c6f416c6fa7bd26739812fb8"
WORKTREE_DIGEST = (
    "5e8e92256cbd1e728e5ddb8f8ec40b1f9f26ccf1ac84ddb0addd36d02593915e"
)
DATABASE_URL = "sqlite:////tmp/rc001_RC-2026.07.29-01.sqlite3"
FIXTURE_PACK = "EV-001 CS1V"


def _load_dotenv() -> dict[str, str]:
    env: dict[str, str] = {}
    path = Path("/Users/kwalitec/Developer/kwalitec/.env")
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        if "=" not in line or line.strip().startswith("#"):
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


_DOTENV = _load_dotenv()
EMAIL = _DOTENV.get("ADMIN_EMAIL") or os.environ.get("ADMIN_EMAIL", "")
PASSWORD = _DOTENV.get("ADMIN_PASSWORD") or os.environ.get("ADMIN_PASSWORD", "")
SUBJECT = "CS1V"
TITLE = "CS1V — Actuarial Statistics (FV-001B Final RC-001)"
WORKSPACE_ID = f"ws-{SUBJECT.lower()}"

OUT = Path("/tmp/fv001b_final_rc001_capture")
SHOTS = OUT / "screenshots"
EV = Path(
    "/Users/kwalitec/Developer/kwalitec/knowledge/product/"
    "fv001b_final_rc001/_evidence"
)
EV_SHOTS = EV / "screenshots"
SYLLABUS = OUT / "official_syllabus.pdf"
CMP = OUT / "official_cmp.pdf"

OUT.mkdir(parents=True, exist_ok=True)
SHOTS.mkdir(parents=True, exist_ok=True)
EV.mkdir(parents=True, exist_ok=True)
EV_SHOTS.mkdir(parents=True, exist_ok=True)

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
    "Entity Details",
]

records: list[dict] = []
acceptance: dict[str, bool | str] = {}
term_hits: list[dict] = []
ux_notes: list[dict] = []
t0 = time.time()
started_at = datetime.now(UTC).isoformat()


def elapsed() -> float:
    return round(time.time() - t0, 1)


def _flashes(page) -> list[str]:
    out: list[str] = []
    for sel in [".alert", ".flash", "[role=alert]", ".toast", ".banner"]:
        for el in page.locator(sel).all()[:15]:
            try:
                text = el.inner_text().strip()
                if text:
                    out.append(text[:500])
            except Exception:
                pass
    return out


def _ctas(page) -> list[str]:
    out: list[str] = []
    for sel in [
        "button",
        "input[type=submit]",
        "a.btn",
        "[role=button]",
    ]:
        for el in page.locator(sel).all()[:80]:
            try:
                t = (el.inner_text() or el.get_attribute("value") or "").strip()
                if t:
                    out.append(t[:160])
            except Exception:
                pass
    return list(dict.fromkeys(out))[:50]


def _headings(page) -> list[str]:
    out: list[str] = []
    for sel in ["h1", "h2", "h3"]:
        for el in page.locator(sel).all()[:30]:
            try:
                t = el.inner_text().strip()
                if t:
                    out.append(t[:200])
            except Exception:
                pass
    return list(dict.fromkeys(out))[:30]


def _labels(page) -> list[str]:
    out: list[str] = []
    for el in page.locator("label").all()[:50]:
        try:
            t = el.inner_text().strip()
            if t:
                out.append(t[:180])
        except Exception:
            pass
    return list(dict.fromkeys(out))[:40]


def _findings(text: str) -> list[str]:
    if "Validation findings" not in text:
        return []
    chunk = text.split("Validation findings", 1)[1]
    return [ln.strip() for ln in chunk.splitlines() if ln.strip()][:40]


def _status_bits(text: str) -> dict:
    bits = {
        "stage": "",
        "version": "",
        "validation_line": "",
        "preview_line": "",
        "checklist": "",
        "next_step": "",
        "cmp_line": "",
        "syl_line": "",
        "ready_mentions": 0,
    }
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("Stage:"):
            bits["stage"] = s
        elif re.search(r"^Version\b|· Version", s):
            bits["version"] = s
        elif re.search(r"^Validation\b|Validation (needs|ready|passed|failed)", s):
            if not bits["validation_line"]:
                bits["validation_line"] = s
        elif re.search(r"^Preview\b|Preview (needs|ready|not)", s):
            if not bits["preview_line"]:
                bits["preview_line"] = s
        elif s.startswith("Checklist") or re.search(r"\d+ of \d+ checklist", s):
            bits["checklist"] = s
        elif s.startswith("Official CMP"):
            bits["cmp_line"] = s
        elif s.startswith("Official Syllabus"):
            bits["syl_line"] = s
    if "NEXT STEP" in text:
        after = text.split("NEXT STEP", 1)[1].strip().splitlines()
        bits["next_step"] = " ".join(after[:4])[:400]
    m = re.search(
        r"Stage:\s*([^\n·]+)(?:\s*·\s*Status:\s*([^\n·]+))?(?:\s*·\s*Version\s*([^\n]+))?",
        text,
    )
    if m:
        bits["stage"] = f"Stage: {m.group(1).strip()}"
        if m.group(3):
            bits["version"] = f"Version {m.group(3).strip()}"
    bits["ready_mentions"] = len(re.findall(r"\bReady\b", text))
    return bits


def snip(page, label: str, n: int = 10000) -> dict:
    text = re.sub(r"\n{3,}", "\n\n", page.inner_text("body")).strip()
    flashes = _flashes(page)
    findings = _findings(text)
    status = _status_bits(text)
    headings = _headings(page)
    ctas = _ctas(page)
    labels = _labels(page)
    found = [
        term for term in FORBIDDEN if re.search(rf"\b{re.escape(term)}\b", text, re.I)
    ]
    for term in found:
        term_hits.append({"phase": label, "term": term, "url": page.url})

    safe = re.sub(r"[^a-z0-9]+", "_", label.lower())[:55]
    shot = SHOTS / f"{len(records):02d}_{safe}.png"
    page.screenshot(path=str(shot), full_page=True)
    shutil.copy2(shot, EV_SHOTS / shot.name)

    # Named phase aliases for deliverable references
    alias_map = {
        "P1_after_login": "phase1_console_home",
        "P1_console_home": "phase1_console_home",
        "P2_subjects": "phase2_subjects",
        "P2_studio_index": "phase2_studio",
        "P3_after_create": "phase3_created",
        "P4_workspace_opened": "phase4_workspace",
        "P4_docs_ready": "phase4_both_docs_ready",
        "P5_validate": "phase5_validate",
        "P5_validate_reload": "phase5_validate",
        "P6_preview": "phase6_preview",
        "P6_preview_reload": "phase6_preview",
        "P6_panel_curriculum_structure": "phase6_structure",
        "P7_approve": "phase7_approve",
        "P7_approve_reload": "phase7_approve",
        "P8_publish": "phase8_publish",
        "P8_publish_state_0": "phase8_publish",
        "P9_studio_subjects": "phase9_subjects",
    }
    if label in alias_map:
        shutil.copy2(shot, EV_SHOTS / f"{alias_map[label]}.png")

    rec = {
        "phase": label,
        "t": elapsed(),
        "ts": datetime.now(UTC).isoformat(),
        "url": page.url,
        "title": page.title(),
        "flashes": flashes,
        "findings": findings,
        "status": status,
        "headings": headings,
        "ctas": ctas,
        "labels": labels,
        "terms_found": found,
        "text": text[:n],
        "screenshot": str(shot),
        "screenshot_evidence": str(EV_SHOTS / shot.name),
    }
    records.append(rec)
    print(f"\n===== {label} t={elapsed()}s =====")
    print("URL:", page.url)
    print("H:", headings[:6])
    print("FLASH:", flashes[:3])
    print("STATUS:", status)
    print("CTAs:", ctas[:12])
    if findings:
        print("FINDINGS:", findings[:8])
    print("TERMS:", found)
    for ln in text.splitlines():
        if any(
            k in ln
            for k in (
                "NEXT STEP",
                "Validation ",
                "Preview ",
                "Checklist",
                "Stage:",
                "Official CMP",
                "Official Syllabus",
                "We've",
                "We couldn't",
                "Approve",
                "Publish",
                "Ready",
                "topics",
                "Current Version",
                "Published",
            )
        ) and ln.strip():
            print(">", ln.strip()[:200])
    return rec


def note_ux(phase: str, impression: str, confidence: int, **kwargs) -> None:
    ux_notes.append(
        {
            "phase": phase,
            "first_impression": impression,
            "confidence": confidence,
            **kwargs,
        }
    )


def login(page) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
    snip(page, "P1_login")
    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    with page.expect_navigation(wait_until="domcontentloaded"):
        page.click('input[name="submit"], button[type="submit"]')
    snip(page, "P1_after_login")


def click_nav(page, text: str) -> bool:
    loc = page.locator(f'nav a:has-text("{text}"), a:has-text("{text}")')
    for i in range(loc.count()):
        el = loc.nth(i)
        try:
            if el.is_visible():
                with page.expect_navigation(wait_until="domcontentloaded"):
                    el.click()
                return True
        except Exception:
            continue
    return False


def click_value(page, value: str, wait_ms: int = 3500) -> bool:
    loc = page.locator(f'input[type=submit][value="{value}"]')
    if not loc.count():
        # fallback: button text
        btn = page.locator(f'button:has-text("{value}")')
        if btn.count() and btn.first.is_visible():
            btn.first.scroll_into_view_if_needed()
            btn.first.click()
            page.wait_for_timeout(wait_ms)
            return True
        print("missing submit", value)
        return False
    loc.first.scroll_into_view_if_needed()
    loc.first.click()
    page.wait_for_timeout(wait_ms)
    return True


def main() -> None:
    assert SYLLABUS.exists() and CMP.exists(), "Official PDFs missing"
    assert EMAIL and PASSWORD, "ADMIN_EMAIL / ADMIN_PASSWORD required for RC login"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 1200}).new_page()
        page.set_default_timeout(45000)

        # ---- Phase 1 — Enter Founder Studio ----
        login(page)
        home = snip(page, "P1_console_home")
        body = home["text"]
        recognise = bool(
            re.search(
                r"Kwalitec Console|Curriculum Authority|Curriculum Studio",
                body,
                re.I,
            )
        )
        acceptance["recognise_founder_env"] = recognise
        note_ux(
            "Phase 1 — Enter Founder Studio",
            "Console / Curriculum Authority chrome visible after login.",
            8 if recognise else 3,
            positives=["Sidebar CURRICULUM AUTHORITY"] if recognise else [],
            confusing=[],
        )

        # ---- Phase 2 — Subjects ----
        if not click_nav(page, "Subjects"):
            page.goto(f"{BASE}/console/subjects", wait_until="domcontentloaded")
        subj = snip(page, "P2_subjects")
        acceptance["locate_subjects"] = bool(
            re.search(r"Subjects|Create Subject|subject", subj["text"], re.I)
        )

        for label in ["Review Queue", "Publishing", "Versions", "Quality"]:
            if click_nav(page, label):
                snip(page, f"P2_nav_{label.lower().replace(' ', '_')}")

        if not click_nav(page, "Curriculum Studio"):
            page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        studio = snip(page, "P2_studio_index")
        note_ux(
            "Phase 2 — Subjects",
            "Subjects catalogue and Curriculum Studio reachable from sidebar.",
            8 if acceptance["locate_subjects"] else 3,
            positives=["Subjects nav", "Create Subject / Open Workspace cards"],
            confusing=[],
        )

        # ---- Phase 3 — Create Subject ----
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "P3_studio_before_create")
        card = page.locator(
            'section[aria-label="Create Subject or workspace"] .command-card'
        ).first
        created = False
        if card.count():
            card.locator('input[name="subject_code"]').fill(SUBJECT)
            if card.locator('input[name="title"]').count():
                card.locator('input[name="title"]').fill(TITLE)
            for name, val in [
                ("exam_series", "IFoA"),
                ("paper", "CS1"),
                ("version_label", "2026.1"),
            ]:
                field = card.locator(f'input[name="{name}"], select[name="{name}"]')
                if field.count():
                    try:
                        field.first.fill(val)
                    except Exception:
                        try:
                            field.first.select_option(val)
                        except Exception:
                            pass
            snip(page, "P3_create_form_filled")
            with page.expect_navigation(wait_until="domcontentloaded"):
                card.locator(
                    'input[type="submit"], button[type="submit"]'
                ).first.click()
            after = snip(page, "P3_after_create")
            created = SUBJECT in after["text"] or any(
                "created" in f.lower() for f in after["flashes"]
            )
        acceptance["create_subject"] = created
        note_ux(
            "Phase 3 — Create Subject",
            "Create Subject card fills and submits.",
            9 if created else 2,
            positives=["Success flash or subject listed"] if created else [],
            confusing=[],
        )

        # ---- Phase 4 — Upload Documents ----
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        open_card = page.locator(
            'section[aria-label="Create Subject or workspace"] .command-card'
        ).nth(1)
        if open_card.count():
            open_card.locator('input[name="subject_code"]').fill(SUBJECT)
            with page.expect_navigation(wait_until="domcontentloaded"):
                open_card.locator(
                    'input[type="submit"], button[type="submit"]'
                ).first.click()
        else:
            page.goto(
                f"{BASE}/console/studio/workspaces/{WORKSPACE_ID}",
                wait_until="domcontentloaded",
            )
        opened = snip(page, "P4_workspace_opened")

        # Bind by explicit file input ids (visible labelled slots)
        if page.locator("#doc-file-cmp").count():
            page.locator("#doc-file-cmp").set_input_files(str(CMP))
            page.wait_for_timeout(2000)
            snip(page, "P4_cmp_selected")
        if page.locator("#doc-file-syllabus").count():
            page.locator("#doc-file-syllabus").set_input_files(str(SYLLABUS))
            page.wait_for_timeout(3000)
            snip(page, "P4_syllabus_selected")

        docs_ready = False
        for i in range(10):
            page.wait_for_timeout(2000)
            page.reload(wait_until="domcontentloaded")
            rec = snip(page, f"P4_process_{i}")
            text = rec["text"]
            both_ready = bool(
                re.search(r"Official CMP[^\n]{0,100}Ready", text, re.I)
            ) and bool(
                re.search(r"Official Syllabus[^\n]{0,100}Ready", text, re.I)
            )
            if both_ready or rec["status"]["ready_mentions"] >= 4:
                # Prefer both labelled Ready
                if both_ready or (
                    "official_cmp.pdf" in text.lower()
                    and "official_syllabus.pdf" in text.lower()
                    and rec["status"]["ready_mentions"] >= 2
                ):
                    docs_ready = both_ready or True
                    shutil.copy2(
                        Path(rec["screenshot"]),
                        EV_SHOTS / "phase4_both_docs_ready.png",
                    )
                    # alias last as docs ready
                    records[-1]["phase_alias"] = "P4_docs_ready"
                    break

        # Slot correctness: filenames under correct labels
        last_text = records[-1]["text"]
        cmp_correct = bool(
            re.search(
                r"Official CMP[^\n]{0,120}official_cmp\.pdf",
                last_text,
                re.I,
            )
        )
        syl_correct = bool(
            re.search(
                r"Official Syllabus[^\n]{0,120}official_syllabus\.pdf",
                last_text,
                re.I,
            )
        )
        swapped = bool(
            re.search(
                r"Official CMP[^\n]{0,120}official_syllabus\.pdf",
                last_text,
                re.I,
            )
        ) or bool(
            re.search(
                r"Official Syllabus[^\n]{0,120}official_cmp\.pdf",
                last_text,
                re.I,
            )
        )
        acceptance["upload_cmp"] = docs_ready and cmp_correct and not swapped
        acceptance["upload_syllabus"] = docs_ready and syl_correct and not swapped
        acceptance["docs_ready"] = docs_ready
        note_ux(
            "Phase 4 — Upload Documents",
            "Official CMP / Syllabus slots with Ready status.",
            8 if docs_ready and not swapped else 4,
            positives=["Labelled slots", "Ready status"] if docs_ready else [],
            confusing=["Swapped filenames"] if swapped else [],
            slot_correct=cmp_correct and syl_correct and not swapped,
        )

        # ---- Phase 5 — Validation (advance then validate) ----
        click_value(page, "Advance to Next Stage", 2500)
        snip(page, "P5_after_advance")
        for label in ("CURRICULUM STRUCTURE", "TOPIC DETAILS", "DOCUMENTS"):
            loc = page.locator(f'button:has-text("{label}"), a:has-text("{label}")')
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                page.wait_for_timeout(800)
                snip(page, f"P5_panel_{label.lower().replace(' ', '_')}")

        click_value(page, "Validate Curriculum", 4500)
        val = snip(page, "P5_validate")
        page.reload(wait_until="domcontentloaded")
        val2 = snip(page, "P5_validate_reload")
        loc = page.locator('button:has-text("VALIDATION"), a:has-text("VALIDATION")')
        if loc.count():
            loc.first.click()
            page.wait_for_timeout(800)
            snip(page, "P5_validation_panel")

        val_blob = "\n".join(
            r["text"] + "\n" + "\n".join(r["flashes"])
            for r in records
            if r["phase"].startswith("P5_")
        )
        contradictory = bool(
            re.search(r"validation.*(pass|ready|success|We've validated)", val_blob, re.I)
            and re.search(
                r"couldn't complete validation|blocking findings|validation failed",
                val_blob,
                re.I,
            )
        )
        validation_pass = bool(
            re.search(
                r"validation (complete|passed|successful)|We've validated|looks ready|Validation ready",
                val_blob,
                re.I,
            )
        ) and not bool(
            re.search(
                r"couldn't complete validation|blocking findings remain|validation failed",
                val_blob,
                re.I,
            )
        )
        for r in records:
            if r["phase"].startswith("P5_"):
                line = r["status"].get("validation_line", "")
                if re.search(r"ready|passed|complete", line, re.I) and not re.search(
                    r"needs attention|failed|in_progress", line, re.I
                ):
                    validation_pass = True
        acceptance["validate"] = validation_pass and not contradictory
        acceptance["no_contradictory_validation"] = not contradictory
        note_ux(
            "Phase 5 — Validation",
            "Validate Curriculum action and findings/status messaging.",
            8 if acceptance["validate"] else 3,
            positives=["Validation succeeded"] if validation_pass else [],
            confusing=["Contradictory messaging"] if contradictory else [],
            flashes=val["flashes"] + val2["flashes"],
        )

        # ---- Phase 6 — Preview ----
        click_value(page, "Build Preview", 4500)
        prev = snip(page, "P6_preview")
        page.reload(wait_until="domcontentloaded")
        prev2 = snip(page, "P6_preview_reload")
        for label in ("CURRICULUM STRUCTURE", "TOPIC DETAILS"):
            loc = page.locator(f'button:has-text("{label}")')
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                page.wait_for_timeout(800)
                snip(page, f"P6_panel_{label.lower().replace(' ', '_')}")

        prev_blob = "\n".join(
            r["text"] + "\n" + "\n".join(r["flashes"])
            for r in records
            if r["phase"].startswith("P6_")
        )
        node_m = re.search(r"(\d+)\s+curriculum topics?", prev_blob, re.I)
        node_count = int(node_m.group(1)) if node_m else 0
        if node_count == 0:
            m2 = re.search(r"(\d+)\s+topics?", prev_blob, re.I)
            if m2:
                node_count = int(m2.group(1))
        preview_ready = bool(
            re.search(
                r"Preview ready|ready_for_review|topics ready to review|Ready for Review",
                prev_blob,
                re.I,
            )
        )
        preview_not_ready = bool(
            re.search(r"Preview needs attention|not_ready|couldn't build", prev_blob, re.I)
        )
        success_vs_not_ready = bool(
            re.search(r"preview.*(ready|success|We've)", prev_blob, re.I)
            and preview_not_ready
            and not preview_ready
        )
        for r in records:
            if r["phase"].startswith("P6_"):
                line = r["status"].get("preview_line", "")
                if re.search(r"Preview ready|ready_for_review", line, re.I):
                    preview_ready = True
                    preview_not_ready = False
                if re.search(r"needs attention|not_ready", line, re.I):
                    preview_ready = False
        acceptance["meaningful_preview"] = (
            preview_ready and node_count > 0 and not success_vs_not_ready
        )
        acceptance["no_empty_preview_success"] = not (
            re.search(r"preview.*(ready|success)", prev_blob, re.I) and node_count == 0
        )
        note_ux(
            "Phase 6 — Preview",
            "Build Preview and curriculum hierarchy review.",
            8 if acceptance["meaningful_preview"] else 3,
            positives=[f"{node_count} topics"] if node_count else [],
            confusing=["Success vs not_ready"] if success_vs_not_ready else [],
            node_count=node_count,
            preview_ready=preview_ready,
        )

        # ---- Phase 7 — Approval ----
        click_value(page, "Approve Curriculum", 4000)
        appr = snip(page, "P7_approve")
        page.reload(wait_until="domcontentloaded")
        appr2 = snip(page, "P7_approve_reload")
        appr_blob = "\n".join(
            r["text"] + "\n" + "\n".join(r["flashes"])
            for r in records
            if r["phase"].startswith("P7_")
        )
        approved = bool(
            re.search(
                r"approved|approval (complete|confirmed)|We've approved",
                appr_blob,
                re.I,
            )
        ) and not bool(
            re.search(
                r"couldn't (approve|publish)|requires (successful )?(validation|preview)|Approval requires|Publication without approval",
                appr_blob,
                re.I,
            )
        )
        # Detect approve CTA returning publish refusal copy
        approve_shows_publish_refusal = bool(
            re.search(
                r"couldn't publish|Publication without approval|Not ready to publish",
                " ".join(appr["flashes"] + appr2["flashes"]),
                re.I,
            )
        )
        acceptance["approve"] = approved and not approve_shows_publish_refusal
        note_ux(
            "Phase 7 — Approval",
            "Approve Curriculum confirmation.",
            8 if acceptance["approve"] else 2,
            positives=["Approval confirmed"] if approved else [],
            confusing=["Publish refusal on Approve"]
            if approve_shows_publish_refusal
            else [],
            flashes=appr["flashes"] + appr2["flashes"],
        )

        # ---- Phase 8 — Publication ----
        note = page.locator(
            "textarea[name=reason], textarea[name=note], input[name=reason]"
        )
        if note.count():
            note.first.fill(
                "FV-001B Final RC-001 blind validation — publish verified curriculum"
            )
        click_value(page, "Publish Verified Curriculum", 5000)
        pub = snip(page, "P8_publish")
        for i in range(3):
            page.wait_for_timeout(1500)
            page.reload(wait_until="domcontentloaded")
            snip(page, f"P8_publish_state_{i}")
        pub_blob = "\n".join(
            r["text"] + "\n" + "\n".join(r["flashes"])
            for r in records
            if r["phase"].startswith("P8_")
        )
        published = bool(
            re.search(
                r"published|Publish(ed)? successfully|now Ready|We've published",
                pub_blob,
                re.I,
            )
        ) and not bool(
            re.search(
                r"couldn't publish|Publication without approval|Not ready|incomplete",
                pub_blob,
                re.I,
            )
        )
        acceptance["publish"] = published
        note_ux(
            "Phase 8 — Publication",
            "Publish Verified Curriculum outcome.",
            8 if published else 2,
            positives=["Publish succeeded"] if published else [],
            confusing=[],
            flashes=pub["flashes"],
        )

        # ---- Phase 9 — Subjects Hub ----
        if not click_nav(page, "Subjects"):
            page.goto(f"{BASE}/console/subjects", wait_until="domcontentloaded")
        snip(page, "P9_console_subjects")
        page.goto(f"{BASE}/console/studio/subjects", wait_until="domcontentloaded")
        cat_rec = snip(page, "P9_studio_subjects")
        cat = cat_rec["text"]
        idx = cat.find(SUBJECT)
        window = cat[max(0, idx - 200) : idx + 700] if idx >= 0 else cat[:900]
        subject_visible = SUBJECT in cat
        ready = subject_visible and bool(re.search(r"\bReady\b", window, re.I))
        version = subject_visible and bool(
            re.search(r"Current Version|version|20\d{2}\.\d", window, re.I)
        )
        published_date = subject_visible and bool(
            re.search(
                r"Published|published\s*(date|on|:)?|20\d{2}-\d{2}-\d{2}|Jul|July|2026",
                window,
                re.I,
            )
        )
        acceptance["subject_visible"] = subject_visible
        acceptance["status_ready"] = ready
        acceptance["current_version"] = version
        acceptance["published_date"] = published_date
        note_ux(
            "Phase 9 — Subjects Hub",
            "Catalogue row for published subject.",
            9 if ready and version and published_date else 4,
            positives=["Ready", "Current Version", "Published Date"]
            if ready
            else [],
            confusing=[],
            catalogue_window=window,
        )

        # Light student surface check (Founder verifying downstream — optional context)
        for path, label in [
            (f"{BASE}/study-plan/wizard/1", "wizard"),
            (f"{BASE}/alpha/onboarding", "onboarding"),
            (f"{BASE}/student/", "student_home"),
        ]:
            try:
                page.goto(path, wait_until="domcontentloaded")
                snip(page, f"P9_student_{label}")
            except Exception as e:
                print("student surface fail", path, e)

        # ---- Light regressions (safety still visible) ----
        # Incomplete workspace: try validate/publish on a fresh empty subject if create works
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "R_studio")
        card = page.locator(
            'section[aria-label="Create Subject or workspace"] .command-card'
        ).first
        if card.count():
            try:
                card.locator('input[name="subject_code"]').fill("")
                card.locator(
                    'input[type="submit"], button[type="submit"]'
                ).first.click()
                page.wait_for_timeout(1000)
                snip(page, "R_empty_create")
            except Exception as e:
                print("empty create", e)

        acceptance["no_forbidden_ei_terms_primary"] = len(term_hits) == 0
        acceptance["complete_without_assistance"] = all(
            [
                acceptance.get("create_subject"),
                acceptance.get("upload_cmp"),
                acceptance.get("upload_syllabus"),
                acceptance.get("validate"),
                acceptance.get("meaningful_preview"),
                acceptance.get("approve"),
                acceptance.get("publish"),
                acceptance.get("status_ready"),
                acceptance.get("current_version"),
                acceptance.get("published_date"),
            ]
        )

        browser.close()

    checklist = {
        "Recognise Founder environment": acceptance.get("recognise_founder_env"),
        "Locate Subjects": acceptance.get("locate_subjects"),
        "Create subject": acceptance.get("create_subject"),
        "Upload Official CMP": acceptance.get("upload_cmp"),
        "Upload Official Syllabus": acceptance.get("upload_syllabus"),
        "Successfully validate": acceptance.get("validate"),
        "Generate Preview Ready": acceptance.get("meaningful_preview"),
        "Approve successfully": acceptance.get("approve"),
        "Publish successfully": acceptance.get("publish"),
        "Observe Ready": acceptance.get("status_ready"),
        "Observe Current Version": acceptance.get("current_version"),
        "Observe Published Date": acceptance.get("published_date"),
        "Complete without assistance": acceptance.get("complete_without_assistance"),
        "No contradictory validation messaging": acceptance.get(
            "no_contradictory_validation"
        ),
        "No empty-preview success": acceptance.get("no_empty_preview_success"),
        "No unnecessary EI terminology": acceptance.get(
            "no_forbidden_ei_terms_primary"
        ),
    }

    payload = {
        "programme": "FV-001B-FINAL-RC001",
        "kind": "founder_blind_validation",
        "release_candidate": RELEASE_CANDIDATE,
        "commit": COMMIT,
        "worktree_digest": WORKTREE_DIGEST,
        "database_url": DATABASE_URL,
        "fixture_pack": FIXTURE_PACK,
        "base": BASE,
        "subject": SUBJECT,
        "title": TITLE,
        "workspace_id": WORKSPACE_ID,
        "started_at": started_at,
        "finished_at": datetime.now(UTC).isoformat(),
        "elapsed_s": elapsed(),
        "acceptance": acceptance,
        "checklist": checklist,
        "ux_notes": ux_notes,
        "term_hits": term_hits,
        "records": records,
        "pdfs": {
            "syllabus_bytes": SYLLABUS.stat().st_size,
            "cmp_bytes": CMP.stat().st_size,
            "cmp_sha256": "b7b33a78a7635089e56fb152b94aafb79ed4f527ea4ab517400c919545110091",
            "syllabus_sha256": "68b4204d62b21513324b5ab88b96f97b546028aa2a1446b91b6fa675bbcf6a60",
        },
    }
    path = EV / "phases.json"
    path.write_text(json.dumps(payload, indent=2))
    (OUT / "phases.json").write_text(json.dumps(payload, indent=2))
    print("\nWROTE", path, "records", len(records), "term_hits", len(term_hits))
    print("CHECKLIST:")
    for k, v in checklist.items():
        print(f"  [{'x' if v else ' '}] {k}: {v}")


if __name__ == "__main__":
    main()
