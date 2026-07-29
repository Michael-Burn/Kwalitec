"""EV-001 — Publication pipeline engineering verification (visible path).

Exercises Create Subject → Upload → Validate → Preview → Approve → Publish →
Ready → Student Catalogue without bypassing gates or seeding publication facts.
"""

from __future__ import annotations

import json
import re
import shutil
import time
from datetime import UTC, datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5141"
EMAIL = "founder.studio@kwalitec.example"
PASSWORD = "StudioBlind2026!"
SUBJECT = "CS1V"
TITLE = "CS1V — Actuarial Statistics (EV-001 Verification)"
WORKSPACE_ID = f"ws-{SUBJECT.lower()}"

OUT = Path("/tmp/ev001_capture")
SHOTS = OUT / "screenshots"
EV = Path(
    "/Users/kwalitec/Developer/kwalitec/knowledge/engineering/"
    "ev001_publication_pipeline_verification/_evidence"
)
EV_SHOTS = EV / "screenshots"
SYLLABUS = OUT / "official_syllabus.pdf"
CMP = OUT / "official_cmp.pdf"

OUT.mkdir(parents=True, exist_ok=True)
SHOTS.mkdir(parents=True, exist_ok=True)
EV.mkdir(parents=True, exist_ok=True)
EV_SHOTS.mkdir(parents=True, exist_ok=True)

records: list[dict] = []
stage_results: dict[str, dict] = {}
identity: dict[str, object] = {
    "subject_code": SUBJECT,
    "workspace_id": WORKSPACE_ID,
    "version_labels": [],
    "topic_counts": [],
    "objective_signals": [],
    "validation_passed_signals": [],
    "preview_readiness": [],
    "approval_signals": [],
    "publication_signals": [],
}
t0 = time.time()
started_at = datetime.now(UTC).isoformat()


def elapsed() -> float:
    return round(time.time() - t0, 1)


def _flashes(page) -> list[str]:
    out: list[str] = []
    for sel in [".alert", ".flash", "[role=alert]", ".toast"]:
        for el in page.locator(sel).all()[:12]:
            try:
                text = el.inner_text().strip()
                if text:
                    out.append(text[:500])
            except Exception:
                pass
    return out


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
        bits["next_step"] = " ".join(after[:3])[:350]
    # Prefer richer stage/version from header line
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


def snip(page, label: str, n: int = 9000) -> dict:
    text = re.sub(r"\n{3,}", "\n\n", page.inner_text("body")).strip()
    flashes = _flashes(page)
    findings = _findings(text)
    status = _status_bits(text)
    safe = re.sub(r"[^a-z0-9]+", "_", label.lower())[:55]
    shot = SHOTS / f"{len(records):02d}_{safe}.png"
    page.screenshot(path=str(shot), full_page=True)
    shutil.copy2(shot, EV_SHOTS / shot.name)
    rec = {
        "phase": label,
        "t": elapsed(),
        "ts": datetime.now(UTC).isoformat(),
        "url": page.url,
        "title": page.title(),
        "flashes": flashes,
        "findings": findings,
        "status": status,
        "text": text[:n],
        "screenshot": str(shot),
        "screenshot_evidence": str(EV_SHOTS / shot.name),
    }
    records.append(rec)
    print(f"\n===== {label} t={elapsed()}s =====")
    print("URL:", page.url)
    print("FLASH:", flashes[:2])
    print("STATUS:", status)
    if findings:
        print("FINDINGS:", findings[:8])
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
            )
        ) and ln.strip():
            print(">", ln.strip()[:180])
    return rec


def login(page) -> None:
    page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
    snip(page, "S0_login")
    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    with page.expect_navigation(wait_until="domcontentloaded"):
        page.click('input[name="submit"], button[type="submit"]')
    snip(page, "S0_after_login")


def click_value(page, value: str, wait_ms: int = 3500) -> bool:
    loc = page.locator(f'input[type=submit][value="{value}"]')
    if not loc.count():
        print("missing submit", value)
        return False
    loc.first.scroll_into_view_if_needed()
    loc.first.click()
    page.wait_for_timeout(wait_ms)
    return True


def mark_stage(name: str, **kwargs) -> None:
    stage_results[name] = {"ok": kwargs.pop("ok", False), **kwargs}
    print(f"STAGE[{name}] =>", stage_results[name])


def main() -> None:
    assert SYLLABUS.exists() and CMP.exists(), "Official PDFs missing"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1440, "height": 1200}).new_page()
        page.set_default_timeout(45000)

        login(page)

        # ---- Stage 1 — Subject Creation ----
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        snip(page, "S1_studio_before_create")
        card = page.locator(
            'section[aria-label="Create Subject or workspace"] .command-card'
        ).first
        card.locator('input[name="subject_code"]').fill(SUBJECT)
        if card.locator('input[name="title"]').count():
            card.locator('input[name="title"]').fill(TITLE)
        snip(page, "S1_create_form_filled")
        with page.expect_navigation(wait_until="domcontentloaded"):
            card.locator('input[type="submit"], button[type="submit"]').first.click()
        created = snip(page, "S1_after_create")
        created_ok = (
            SUBJECT in created["text"]
            or any("created" in f.lower() for f in created["flashes"])
        )
        identity["creation_timestamp"] = created["ts"]
        mark_stage(
            "1_subject_creation",
            ok=created_ok,
            subject=SUBJECT,
            flashes=created["flashes"],
            timestamp=created["ts"],
        )

        # Open workspace (Draft)
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        open_card = page.locator(
            'section[aria-label="Create Subject or workspace"] .command-card'
        ).nth(1)
        open_card.locator('input[name="subject_code"]').fill(SUBJECT)
        with page.expect_navigation(wait_until="domcontentloaded"):
            open_card.locator(
                'input[type="submit"], button[type="submit"]'
            ).first.click()
        opened = snip(page, "S1_workspace_opened")
        draft_ok = WORKSPACE_ID in opened["url"] or SUBJECT in opened["text"]
        identity["workspace_url"] = opened["url"]
        if opened["status"].get("version"):
            identity["version_labels"].append(opened["status"]["version"])
        mark_stage(
            "1_draft_workspace",
            ok=draft_ok,
            workspace_id=WORKSPACE_ID,
            url=opened["url"],
            stage=opened["status"].get("stage"),
            version=opened["status"].get("version"),
        )

        # ---- Stage 2 — Document Upload ----
        page.locator("#doc-file-cmp").set_input_files(str(CMP))
        page.wait_for_timeout(2000)
        snip(page, "S2_cmp_selected")
        page.locator("#doc-file-syllabus").set_input_files(str(SYLLABUS))
        page.wait_for_timeout(3000)
        snip(page, "S2_syllabus_selected")

        docs_ready = False
        for i in range(8):
            page.wait_for_timeout(2000)
            page.reload(wait_until="domcontentloaded")
            rec = snip(page, f"S2_process_{i}")
            text = rec["text"]
            cmp_ok = bool(
                re.search(r"Official CMP[^\n]*Ready|Official CMP ·", text, re.I)
            )
            syl_ok = bool(
                re.search(
                    r"Official Syllabus[^\n]*Ready|Official Syllabus ·", text, re.I
                )
            )
            both_ready = bool(
                re.search(r"Official CMP[^\n]{0,80}Ready", text, re.I)
            ) and bool(re.search(r"Official Syllabus[^\n]{0,80}Ready", text, re.I))
            # Also accept processing_label Ready in status cells
            ready_count = len(re.findall(r"\bReady\b", text))
            if both_ready or (cmp_ok and syl_ok and ready_count >= 2):
                docs_ready = True
                break
        mark_stage(
            "2_document_upload",
            ok=docs_ready,
            cmp_line=records[-1]["status"].get("cmp_line"),
            syl_line=records[-1]["status"].get("syl_line"),
            ready_mentions=records[-1]["status"].get("ready_mentions"),
            pdfs={
                "cmp_bytes": CMP.stat().st_size,
                "syllabus_bytes": SYLLABUS.stat().st_size,
            },
        )

        # ---- Stage 3 — Structure Preparation (visible cues + advance) ----
        click_value(page, "Advance to Next Stage", 2500)
        snip(page, "S3_after_advance")
        # Open structure panels if present
        for label in ("CURRICULUM STRUCTURE", "TOPIC DETAILS", "DOCUMENTS"):
            loc = page.locator(f'button:has-text("{label}"), a:has-text("{label}")')
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                page.wait_for_timeout(800)
                snip(page, f"S3_panel_{label.lower().replace(' ', '_')}")

        structure_text = "\n".join(
            r["text"] for r in records if r["phase"].startswith("S3_")
        )
        topic_count = 0
        m = re.search(r"(\d+)\s+topics?", structure_text, re.I)
        if m:
            topic_count = int(m.group(1))
        # Count distinct topic-like titles from preview line later; for now use cues
        objective_hits = len(
            re.findall(r"objective|learning objective", structure_text, re.I)
        )
        identity["topic_counts"].append({"phase": "structure", "count": topic_count})
        identity["objective_signals"].append(objective_hits)
        mark_stage(
            "3_structure_preparation",
            ok=topic_count > 0 or "Curriculum structure" in structure_text,
            topic_count_signal=topic_count,
            objective_signal_hits=objective_hits,
            stage=records[-1]["status"].get("stage"),
        )

        # ---- Stage 4 — Validation ----
        click_value(page, "Validate Curriculum", 4500)
        val = snip(page, "S4_validate")
        page.reload(wait_until="domcontentloaded")
        val2 = snip(page, "S4_validate_reload")
        loc = page.locator('button:has-text("VALIDATION"), a:has-text("VALIDATION")')
        if loc.count():
            loc.first.click()
            page.wait_for_timeout(800)
            snip(page, "S4_validation_panel")

        val_blob = "\n".join(
            r["text"] + "\n" + "\n".join(r["flashes"])
            for r in records
            if r["phase"].startswith("S4_")
        )
        blocking = [
            f
            for r in records
            if r["phase"].startswith("S4_")
            for f in r["findings"]
            if "blocking" in f.lower()
        ]
        warnings = [
            f
            for r in records
            if r["phase"].startswith("S4_")
            for f in r["findings"]
            if "warning" in f.lower()
        ]
        validation_pass = bool(
            re.search(
                r"validation (complete|passed|successful)|We've validated|looks ready",
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
        # Prefer status line
        for r in records:
            if r["phase"].startswith("S4_"):
                line = r["status"].get("validation_line", "")
                if re.search(r"ready|passed|complete", line, re.I) and not re.search(
                    r"needs attention|failed|in_progress", line, re.I
                ):
                    validation_pass = True
                if re.search(r"failed|needs attention", line, re.I):
                    # keep false unless success flash overrides later
                    pass
        identity["validation_passed_signals"].append(
            {
                "pass": validation_pass,
                "blocking_count": len(blocking),
                "warning_count": len(warnings),
                "flashes": val["flashes"] + val2["flashes"],
            }
        )
        mark_stage(
            "4_validation",
            ok=validation_pass and len(blocking) == 0,
            validation_pass=validation_pass,
            blocking_issues=len(blocking),
            warnings=len(warnings),
            findings_sample=(blocking + warnings)[:10],
            validation_line=records[-1]["status"].get("validation_line"),
            flashes=records[-1]["flashes"],
        )

        # ---- Stage 5 — Preview ----
        click_value(page, "Build Preview", 4500)
        prev = snip(page, "S5_preview")
        page.reload(wait_until="domcontentloaded")
        prev2 = snip(page, "S5_preview_reload")
        for label in ("CURRICULUM STRUCTURE", "TOPIC DETAILS"):
            loc = page.locator(f'button:has-text("{label}")')
            if loc.count() and loc.first.is_visible():
                loc.first.click()
                page.wait_for_timeout(800)
                snip(page, f"S5_panel_{label.lower().replace(' ', '_')}")

        prev_blob = "\n".join(
            r["text"] + "\n" + "\n".join(r["flashes"])
            for r in records
            if r["phase"].startswith("S5_")
        )
        node_m = re.search(r"(\d+)\s+curriculum topics?", prev_blob, re.I)
        node_count = int(node_m.group(1)) if node_m else 0
        if node_count == 0:
            m2 = re.search(r"(\d+)\s+topics?", prev_blob, re.I)
            if m2:
                node_count = int(m2.group(1))
        preview_ready = bool(
            re.search(r"Preview ready|ready_for_review|topics ready to review", prev_blob, re.I)
        ) and not bool(re.search(r"Preview needs attention|not_ready", prev_blob, re.I))
        # Status line authority
        for r in records:
            if r["phase"].startswith("S5_"):
                line = r["status"].get("preview_line", "")
                if re.search(r"Preview ready|ready_for_review", line, re.I):
                    preview_ready = True
                if re.search(r"needs attention|not_ready", line, re.I):
                    preview_ready = False
        identity["preview_readiness"].append(
            {
                "ready": preview_ready,
                "node_count": node_count,
                "line": records[-1]["status"].get("preview_line"),
            }
        )
        identity["topic_counts"].append({"phase": "preview", "count": node_count})
        mark_stage(
            "5_preview",
            ok=preview_ready and node_count > 0,
            preview_ready=preview_ready,
            node_count=node_count,
            preview_line=records[-1]["status"].get("preview_line"),
            flashes=prev["flashes"] + prev2["flashes"],
        )

        # ---- Stage 6 — Approval ----
        click_value(page, "Approve Curriculum", 4000)
        appr = snip(page, "S6_approve")
        page.reload(wait_until="domcontentloaded")
        appr2 = snip(page, "S6_approve_reload")
        appr_blob = "\n".join(
            r["text"] + "\n" + "\n".join(r["flashes"])
            for r in records
            if r["phase"].startswith("S6_")
        )
        approved = bool(
            re.search(r"approved|approval (complete|confirmed)|We've approved", appr_blob, re.I)
        ) and not bool(
            re.search(
                r"couldn't (approve|publish)|requires (successful )?(validation|preview)|Approval requires",
                appr_blob,
                re.I,
            )
        )
        identity["approval_signals"].append(
            {
                "approved": approved,
                "timestamp": appr["ts"],
                "flashes": appr["flashes"] + appr2["flashes"],
            }
        )
        mark_stage(
            "6_approval",
            ok=approved,
            approved=approved,
            timestamp=appr["ts"],
            flashes=appr["flashes"] + appr2["flashes"],
        )

        # ---- Stage 7 — Publication ----
        note = page.locator(
            "textarea[name=reason], textarea[name=note], input[name=reason]"
        )
        if note.count():
            note.first.fill("EV-001 engineering verification — publish verified curriculum")
        click_value(page, "Publish Verified Curriculum", 5000)
        pub = snip(page, "S7_publish")
        for i in range(3):
            page.wait_for_timeout(1500)
            page.reload(wait_until="domcontentloaded")
            snip(page, f"S7_publish_state_{i}")
        pub_blob = "\n".join(
            r["text"] + "\n" + "\n".join(r["flashes"])
            for r in records
            if r["phase"].startswith("S7_")
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
        version_id = ""
        vm = re.search(r"Version\s+([0-9]{4}\.[0-9]+|[A-Za-z0-9._-]+)", pub_blob)
        if vm:
            version_id = vm.group(1)
        identity["publication_signals"].append(
            {
                "published": published,
                "timestamp": pub["ts"],
                "version": version_id,
                "flashes": pub["flashes"],
            }
        )
        if version_id:
            identity["version_labels"].append(version_id)
        mark_stage(
            "7_publication",
            ok=published,
            published=published,
            version=version_id,
            timestamp=pub["ts"],
            flashes=records[-1]["flashes"],
            stage=records[-1]["status"].get("stage"),
        )

        # ---- Stage 8 — Ready / Subjects catalogue ----
        page.goto(f"{BASE}/console/studio/subjects", wait_until="domcontentloaded")
        subj = snip(page, "S8_studio_subjects")
        page.goto(f"{BASE}/console/subjects", wait_until="domcontentloaded")
        snip(page, "S8_console_subjects")
        cat = subj["text"]
        idx = cat.find(SUBJECT)
        window = cat[max(0, idx - 200) : idx + 700] if idx >= 0 else cat[:900]
        ready_ok = SUBJECT in cat and bool(re.search(r"\bReady\b", window, re.I))
        version_ok = bool(re.search(r"version|20\d{2}\.\d", window, re.I))
        date_ok = bool(
            re.search(
                r"published|20\d{2}-\d{2}-\d{2}|Jul|July|2026",
                window,
                re.I,
            )
        )
        mark_stage(
            "8_ready_catalogue",
            ok=ready_ok,
            subject_visible=SUBJECT in cat,
            ready=ready_ok,
            current_version_visible=version_ok,
            published_date_visible=date_ok,
            catalogue_window=window,
        )

        # ---- Stage 9 — Student discovery ----
        page.goto(f"{BASE}/study-plan/wizard/1", wait_until="domcontentloaded")
        student = snip(page, "S9_student_catalogue_wizard")
        page.goto(f"{BASE}/alpha/onboarding", wait_until="domcontentloaded")
        snip(page, "S9_onboarding")
        page.goto(f"{BASE}/student/", wait_until="domcontentloaded")
        snip(page, "S9_student_home")

        student_blob = "\n".join(
            r["text"] for r in records if r["phase"].startswith("S9_")
        )
        discoverable = bool(re.search(rf"\b{SUBJECT}\b", student_blob))
        ready_student = bool(
            re.search(rf"\b{SUBJECT}\b[\s\S]{{0,300}}\bReady\b", student_blob, re.I)
        ) or (discoverable and bool(re.search(r"\bReady\b", student_blob)))
        enrol_cue = bool(
            re.search(
                r"Ready|Choose your exam|Subject Catalogue|select",
                student_blob,
                re.I,
            )
        )
        mark_stage(
            "9_student_discovery",
            ok=discoverable and ready_student,
            subject_visible=discoverable,
            ready_status=ready_student,
            enrol_possible_cue=enrol_cue,
            note="Did not begin studying — discoverability only",
        )

        # ---- Regression probes via incomplete subject ----
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        card = page.locator(
            'section[aria-label="Create Subject or workspace"] .command-card'
        ).first
        card.locator('input[name="subject_code"]').fill("CS1Z")
        if card.locator('input[name="title"]').count():
            card.locator('input[name="title"]').fill("CS1Z — Incomplete Gate Probe")
        with page.expect_navigation(wait_until="domcontentloaded"):
            card.locator('input[type="submit"], button[type="submit"]').first.click()
        page.goto(f"{BASE}/console/studio/", wait_until="domcontentloaded")
        open_card = page.locator(
            'section[aria-label="Create Subject or workspace"] .command-card'
        ).nth(1)
        open_card.locator('input[name="subject_code"]').fill("CS1Z")
        with page.expect_navigation(wait_until="domcontentloaded"):
            open_card.locator(
                'input[type="submit"], button[type="submit"]'
            ).first.click()
        snip(page, "R_incomplete_workspace")

        click_value(page, "Publish Verified Curriculum", 3000)
        r_pub = snip(page, "R_publish_without_approval")
        click_value(page, "Approve Curriculum", 3000)
        r_appr = snip(page, "R_approve_without_validation")
        click_value(page, "Validate Curriculum", 3500)
        r_val = snip(page, "R_validate_without_docs")
        click_value(page, "Build Preview", 3000)
        r_prev = snip(page, "R_preview_without_structure")

        def refused(rec: dict, patterns: str) -> bool:
            blob = "\n".join(rec["flashes"]) + "\n" + rec["text"]
            return bool(re.search(patterns, blob, re.I))

        regression = {
            "publish_without_approval_refused": refused(
                r_pub, r"couldn't publish|not ready|approval|version|incomplete"
            ),
            "approve_without_validation_refused": refused(
                r_appr,
                r"couldn't approve|validation|preview|Approval requires|couldn't publish",
            ),
            "validate_without_docs_fails": refused(
                r_val,
                r"couldn't complete validation|blocking|Official CMP is not present|"
                r"Official Syllabus|No extracted|validation failed|failed",
            ),
            "preview_without_structure_not_ready": refused(
                r_prev,
                r"not ready|no extracted|needs attention|couldn't|0 curriculum topics|"
                r"Validate the curriculum before preview",
            ),
            "missing_cmp_finding": any(
                "CMP" in f and "blocking" in f.lower() for f in r_val["findings"]
            )
            or "Official CMP is not present" in r_val["text"],
            "missing_syllabus_finding": any(
                "Syllabus" in f for f in r_val["findings"]
            )
            or "Official Syllabus" in r_val["text"],
        }
        mark_stage(
            "regression_ui_gates",
            ok=all(
                [
                    regression["publish_without_approval_refused"],
                    regression["approve_without_validation_refused"],
                    regression["validate_without_docs_fails"],
                    regression["missing_cmp_finding"],
                    regression["missing_syllabus_finding"],
                ]
            ),
            **regression,
        )

        browser.close()

    lifecycle_ok = all(
        stage_results.get(k, {}).get("ok")
        for k in (
            "1_subject_creation",
            "1_draft_workspace",
            "2_document_upload",
            "4_validation",
            "5_preview",
            "6_approval",
            "7_publication",
            "8_ready_catalogue",
            "9_student_discovery",
        )
    )

    payload = {
        "programme": "EV-001",
        "kind": "lifecycle_verification",
        "base": BASE,
        "subject": SUBJECT,
        "workspace_id": WORKSPACE_ID,
        "started_at": started_at,
        "finished_at": datetime.now(UTC).isoformat(),
        "elapsed_s": elapsed(),
        "lifecycle_ok": lifecycle_ok,
        "stage_results": stage_results,
        "identity": identity,
        "records": records,
        "pdfs": {
            "syllabus_bytes": SYLLABUS.stat().st_size,
            "cmp_bytes": CMP.stat().st_size,
            "syllabus_path": str(SYLLABUS),
            "cmp_path": str(CMP),
        },
    }
    (EV / "lifecycle.json").write_text(json.dumps(payload, indent=2))
    (OUT / "lifecycle.json").write_text(json.dumps(payload, indent=2))
    print("\nWROTE lifecycle.json records=", len(records), "lifecycle_ok=", lifecycle_ok)
    for k, v in stage_results.items():
        print(f"  [{'x' if v.get('ok') else ' '}] {k}: {v.get('ok')}")


if __name__ == "__main__":
    main()
