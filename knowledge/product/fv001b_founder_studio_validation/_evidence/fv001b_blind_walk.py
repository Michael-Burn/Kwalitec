"""FV-001B Founder Studio blind validation — visible UX capture only.

Scope: Founder Studio curriculum-authoring journey (Phases 1–7).
Does not evaluate student experience or Educational Intelligence internals.
"""

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

SYLLABUS_PDF = OUT / "official_syllabus.pdf"
CMP_PDF = OUT / "official_cmp.pdf"

phases: list[dict] = []
timeline: list[dict] = []
term_hits: list[dict] = []
nav_notes: list[dict] = []

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
    "Knowledge Graph",
    "Entity Details",
    "Pipeline",
]

t0 = time.time()


def elapsed() -> float:
    return round(time.time() - t0, 1)


def snip(page, label: str, n: int = 4000) -> dict:
    text = page.inner_text("body")
    clean = re.sub(r"\n{3,}", "\n\n", text).strip()
    links = []
    for a in page.locator("a").all()[:60]:
        try:
            t = a.inner_text().strip()
            h = a.get_attribute("href") or ""
            if t:
                links.append({"text": t[:100], "href": h[:160]})
        except Exception:
            pass
    buttons: list[str] = []
    for sel in ["button", "input[type=submit]", "a.btn", "[role=button]"]:
        for el in page.locator(sel).all()[:40]:
            try:
                t = (el.inner_text() or el.get_attribute("value") or "").strip()
                if t:
                    buttons.append(t[:120])
            except Exception:
                pass
    headings = []
    for sel in ["h1", "h2", "h3", "[class*='title']", "legend"]:
        for el in page.locator(sel).all()[:20]:
            try:
                t = el.inner_text().strip()
                if t and len(t) < 200:
                    headings.append(t)
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
    for term in FORBIDDEN_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", text, re.I):
            found.append(term)
            term_hits.append({"phase": label, "term": term, "url": page.url})
    shot = OUT / f"{len(phases):02d}_{re.sub(r'[^a-z0-9]+', '_', label.lower())[:50]}.png"
    try:
        page.screenshot(path=str(shot), full_page=True)
    except Exception:
        shot = None
    flash = ""
    for sel in [".flash", ".alert", ".message", "[role=alert]", ".toast"]:
        try:
            if page.locator(sel).count():
                flash = page.locator(sel).first.inner_text().strip()[:400]
                if flash:
                    break
        except Exception:
            pass
    rec = {
        "phase": label,
        "t": elapsed(),
        "url": page.url,
        "title": page.title(),
        "text": clean[:n],
        "text_len": len(clean),
        "links": links[:40],
        "ctas": list(dict.fromkeys(buttons))[:30],
        "headings": list(dict.fromkeys(headings))[:25],
        "labels": list(dict.fromkeys(labels))[:25],
        "terms_found": found,
        "flash": flash,
        "screenshot": str(shot) if shot else None,
    }
    phases.append(rec)
    timeline.append(
        {"t": elapsed(), "phase": label, "url": page.url, "title": page.title()}
    )
    print(f"\n===== {label} t={elapsed()}s =====")
    print("URL:", page.url)
    print("TITLE:", page.title())
    print("HEADINGS:", rec["headings"][:8])
    print("CTAs:", rec["ctas"][:12])
    print("TERMS:", found)
    if flash:
        print("FLASH:", flash)
    print(clean[:1400].replace("\n\n", "\n"))
    return rec


def try_click(page, selectors, timeout: int = 5000):
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
                    page.wait_for_timeout(600)
                    return True, sel
                except Exception:
                    continue
    return False, None


def fill_first(page, names_values: list[tuple[str, str]]) -> list[str]:
    filled = []
    for name, value in names_values:
        loc = page.locator(
            f'input[name="{name}"], textarea[name="{name}"], select[name="{name}"]'
        )
        if not loc.count():
            continue
        tag = loc.first.evaluate("el => el.tagName.toLowerCase()")
        if tag == "select":
            try:
                loc.first.select_option(label=value)
                filled.append(name)
            except Exception:
                try:
                    loc.first.select_option(value=value)
                    filled.append(name)
                except Exception:
                    pass
        else:
            loc.first.fill(value)
            filled.append(name)
    return filled


def note_nav(phase: str, observation: str) -> None:
    nav_notes.append({"phase": phase, "observation": observation, "t": elapsed()})


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.set_default_timeout(20000)

        # ------------------------------------------------------------------
        # PHASE 1 — Login / Founder environment recognition
        # ------------------------------------------------------------------
        page.goto(f"{BASE}/", wait_until="domcontentloaded")
        snip(page, "P1_root")

        page.goto(f"{BASE}/auth/login", wait_until="domcontentloaded")
        snip(page, "P1_login")

        page.fill('input[name="email"]', EMAIL)
        page.fill('input[name="password"]', PASSWORD)
        with page.expect_navigation(wait_until="domcontentloaded"):
            page.click('input[name="submit"], button[type="submit"]')
        snip(page, "P1_after_login")
        note_nav(
            "P1",
            "After login, visible founder/studio cues: "
            + str(
                [
                    l["text"]
                    for l in phases[-1]["links"]
                    if any(
                        k in (l["text"] + l["href"]).lower()
                        for k in [
                            "founder",
                            "studio",
                            "curriculum",
                            "subject",
                            "console",
                            "content",
                        ]
                    )
                ][:15]
            ),
        )

        # Try natural navigation into Founder / Studio / Subjects
        clicked, sel = try_click(
            page,
            [
                'a:has-text("Founder Studio")',
                'a:has-text("Curriculum Studio")',
                'a:has-text("Subjects")',
                'a:has-text("Subject Catalogue")',
                'a:has-text("Founder Console")',
                'a:has-text("Console")',
                'a:has-text("Content")',
                'a[href*="/founder"]',
                'a[href*="curriculum-studio"]',
                'a[href*="curriculum_studio"]',
            ],
        )
        if clicked:
            note_nav("P1", f"Clicked into environment via {sel}")
            snip(page, "P1_env_nav_click")
        else:
            note_nav("P1", "No obvious Founder/Studio link from post-login land")
            snip(page, "P1_no_env_link")

        # Explore founder home / console if present
        for path, label in [
            ("/founder/", "P1_founder_home"),
            ("/founder/dashboard/", "P1_founder_dashboard"),
            ("/console/", "P1_console"),
        ]:
            resp = page.goto(f"{BASE}{path}", wait_until="domcontentloaded")
            if resp and resp.status < 400:
                snip(page, label)

        # ------------------------------------------------------------------
        # PHASE 2 — Subject Catalogue
        # ------------------------------------------------------------------
        catalogue_paths = [
            "/curriculum-studio/",
            "/curriculum-studio/hub",
            "/curriculum-studio/subjects",
            "/founder/studio/",
            "/founder/subjects",
            "/console/content",
        ]
        catalogue_found = False
        for path in catalogue_paths:
            resp = page.goto(f"{BASE}{path}", wait_until="domcontentloaded")
            status = resp.status if resp else None
            snip(page, f"P2_try_{path.strip('/').replace('/', '_')}")
            phases[-1]["http_status"] = status
            body = phases[-1]["text"].lower()
            if status and status < 400 and any(
                k in body
                for k in ["subject", "catalogue", "catalog", "curriculum studio", "ready", "draft"]
            ):
                catalogue_found = True
                note_nav("P2", f"Catalogue-like surface at {path} status={status}")
                break

        # Also try clicking Subjects / Create from current page
        clicked, sel = try_click(
            page,
            [
                'a:has-text("Subjects")',
                'a:has-text("Subject Catalogue")',
                'a:has-text("All Subjects")',
                'a:has-text("Browse Subjects")',
                'a:has-text("Curriculum Studio")',
                'a:has-text("Manage Subjects")',
            ],
        )
        if clicked:
            snip(page, "P2_subjects_nav_click")
            note_nav("P2", f"Subjects nav via {sel}")

        snip(page, "P2_catalogue_state")
        body_l = phases[-1]["text"].lower()
        phases[-1]["ready_visible"] = "ready" in body_l
        phases[-1]["draft_visible"] = "draft" in body_l
        phases[-1]["coming_soon_visible"] = "coming soon" in body_l or "coming-soon" in body_l
        phases[-1]["create_cta_visible"] = any(
            k in " ".join(phases[-1]["ctas"]).lower()
            for k in ["create subject", "new subject", "add subject"]
        ) or any(
            "create subject" in (l["text"] + l["href"]).lower()
            or "new subject" in l["text"].lower()
            for l in phases[-1]["links"]
        )

        # ------------------------------------------------------------------
        # PHASE 3 — Create Subject
        # ------------------------------------------------------------------
        clicked, sel = try_click(
            page,
            [
                'a:has-text("Create Subject")',
                'button:has-text("Create Subject")',
                'a:has-text("New Subject")',
                'button:has-text("New Subject")',
                'a:has-text("Add Subject")',
                'button:has-text("Add Subject")',
                'a:has-text("Create subject")',
                'button:has-text("Create subject")',
                'a[href*="create"]',
            ],
        )
        if clicked:
            note_nav("P3", f"Create Subject via {sel}")
            snip(page, "P3_create_form")
        else:
            note_nav("P3", "Create Subject CTA not found — checking forms on page")
            snip(page, "P3_create_cta_missing")
            # Try known create routes without assuming implementation
            for path in [
                "/curriculum-studio/subjects/new",
                "/curriculum-studio/create",
                "/curriculum-studio/subjects/create",
                "/founder/studio/subjects/new",
            ]:
                resp = page.goto(f"{BASE}{path}", wait_until="domcontentloaded")
                snip(page, f"P3_try_{path.strip('/').replace('/', '_')}")
                phases[-1]["http_status"] = resp.status if resp else None
                if resp and resp.status < 400 and page.locator("form").count():
                    break

        filled = fill_first(
            page,
            [
                ("subject_code", "CS1B"),
                ("code", "CS1B"),
                ("exam_code", "CS1B"),
                ("name", "CS1B — Actuarial Statistics (Blind)"),
                ("subject_name", "CS1B — Actuarial Statistics (Blind)"),
                ("title", "CS1B — Actuarial Statistics (Blind)"),
                ("display_name", "CS1B — Actuarial Statistics (Blind)"),
                ("description", "IFoA CS1 Actuarial Statistics — FV-001B blind validation subject"),
            ],
        )
        phases[-1]["fields_filled"] = filled
        # Select first sensible option on each select
        selects = page.locator("select")
        for i in range(min(selects.count(), 8)):
            try:
                opts = selects.nth(i).locator("option").all_inner_texts()
                print("select", i, opts[:10])
                for o in opts:
                    if o.strip() and "select" not in o.lower() and "—" not in o[:1]:
                        selects.nth(i).select_option(label=o)
                        break
            except Exception as e:
                print("select err", e)

        # Capture empty-submit validation if form present
        if page.locator("form").count():
            # Snapshot form labels before submit
            snip(page, "P3_form_before_submit")
            try_click(
                page,
                [
                    'button:has-text("Create")',
                    'button:has-text("Save")',
                    'button:has-text("Continue")',
                    'input[type="submit"]',
                    'button[type="submit"]',
                ],
                timeout=12000,
            )
            page.wait_for_timeout(1000)
            snip(page, "P3_after_create_submit")
        else:
            snip(page, "P3_no_form")

        # ------------------------------------------------------------------
        # PHASE 4 — Upload Official Documents
        # ------------------------------------------------------------------
        # Enter workspace / subject detail if needed
        clicked, sel = try_click(
            page,
            [
                'a:has-text("Open Workspace")',
                'button:has-text("Open Workspace")',
                'a:has-text("Workspace")',
                'a:has-text("Open")',
                'a:has-text("CS1B")',
                'a:has-text("Continue")',
                'a:has-text("Upload")',
                'a:has-text("Documents")',
                'button:has-text("Create Workspace")',
                'a:has-text("Create Workspace")',
            ],
        )
        if clicked:
            note_nav("P4", f"Workspace/subject entry via {sel}")
            snip(page, "P4_workspace_entry")
        else:
            snip(page, "P4_workspace_cta_not_found")

        # Workspace create form if present
        fill_first(
            page,
            [
                ("name", "CS1B Workspace"),
                ("workspace_name", "CS1B Workspace"),
                ("label", "CS1B Workspace"),
                ("subject_code", "CS1B"),
            ],
        )
        try_click(
            page,
            [
                'button:has-text("Create Workspace")',
                'button:has-text("Create")',
                'button:has-text("Open")',
                'button[type="submit"]',
                'input[type="submit"]',
            ],
        )
        page.wait_for_timeout(800)
        snip(page, "P4_pre_upload_state")

        # File inputs
        file_inputs = page.locator('input[type="file"]')
        print("file inputs", file_inputs.count())
        phases[-1]["file_input_count"] = file_inputs.count()

        upload_ok = False
        if file_inputs.count() >= 1:
            # Prefer named slots
            syllabus_input = page.locator(
                'input[type="file"][name*="syllabus" i], '
                'input[type="file"][id*="syllabus" i], '
                'input[type="file"][accept*="pdf"]'
            )
            cmp_input = page.locator(
                'input[type="file"][name*="cmp" i], '
                'input[type="file"][id*="cmp" i], '
                'input[type="file"][name*="core" i]'
            )
            # Upload syllabus
            target = syllabus_input.first if syllabus_input.count() else file_inputs.first
            target.set_input_files(str(SYLLABUS_PDF))
            page.wait_for_timeout(500)
            snip(page, "P4_syllabus_selected")
            try_click(
                page,
                [
                    'button:has-text("Upload Syllabus")',
                    'button:has-text("Upload")',
                    'button:has-text("Save")',
                    'button[type="submit"]',
                    'input[type="submit"]',
                ],
            )
            page.wait_for_timeout(1500)
            snip(page, "P4_after_syllabus_upload")

            # Re-find file inputs after possible navigation
            file_inputs = page.locator('input[type="file"]')
            cmp_target = None
            if cmp_input.count():
                cmp_target = cmp_input.first
            elif file_inputs.count() >= 2:
                cmp_target = file_inputs.nth(1)
            elif file_inputs.count() == 1:
                cmp_target = file_inputs.first
            if cmp_target:
                cmp_target.set_input_files(str(CMP_PDF))
                page.wait_for_timeout(500)
                snip(page, "P4_cmp_selected")
                try_click(
                    page,
                    [
                        'button:has-text("Upload CMP")',
                        'button:has-text("Upload Core")',
                        'button:has-text("Upload")',
                        'button:has-text("Save")',
                        'button[type="submit"]',
                        'input[type="submit"]',
                    ],
                )
                page.wait_for_timeout(1500)
                snip(page, "P4_after_cmp_upload")
                upload_ok = True
            else:
                snip(page, "P4_cmp_input_missing")
        else:
            # Look for separate upload pages / buttons
            for label, sels in [
                (
                    "syllabus",
                    [
                        'a:has-text("Upload Syllabus")',
                        'button:has-text("Upload Syllabus")',
                        'a:has-text("Syllabus")',
                    ],
                ),
                (
                    "cmp",
                    [
                        'a:has-text("Upload CMP")',
                        'button:has-text("Upload CMP")',
                        'a:has-text("CMP")',
                        'a:has-text("Core Reading")',
                    ],
                ),
            ]:
                clicked, sel = try_click(page, sels)
                if clicked:
                    snip(page, f"P4_{label}_upload_page")
                    fi = page.locator('input[type="file"]')
                    if fi.count():
                        pdf = SYLLABUS_PDF if label == "syllabus" else CMP_PDF
                        fi.first.set_input_files(str(pdf))
                        try_click(
                            page,
                            [
                                'button:has-text("Upload")',
                                'button[type="submit"]',
                                'input[type="submit"]',
                            ],
                        )
                        page.wait_for_timeout(1200)
                        snip(page, f"P4_after_{label}_upload")
                        upload_ok = True
            if not upload_ok:
                snip(page, "P4_upload_inputs_not_found")

        phases[-1]["upload_attempted"] = upload_ok or file_inputs.count() > 0

        # ------------------------------------------------------------------
        # PHASE 5 — Extraction Review
        # ------------------------------------------------------------------
        # Advance / extract / validate / review actions
        for action_label, sels in [
            (
                "extract",
                [
                    'button:has-text("Extract")',
                    'a:has-text("Extract")',
                    'button:has-text("Run Extraction")',
                    'button:has-text("Start Extraction")',
                ],
            ),
            (
                "advance",
                [
                    'button:has-text("Advance")',
                    'a:has-text("Advance")',
                    'button:has-text("Continue")',
                    'a:has-text("Continue")',
                    'button:has-text("Next")',
                ],
            ),
            (
                "validate",
                [
                    'button:has-text("Validate")',
                    'a:has-text("Validate")',
                    'button:has-text("Run Validation")',
                ],
            ),
            (
                "preview",
                [
                    'button:has-text("Preview")',
                    'a:has-text("Preview")',
                    'a:has-text("Review")',
                    'button:has-text("Review")',
                    'a:has-text("Review Curriculum")',
                    'a:has-text("Curriculum Review")',
                ],
            ),
            (
                "approve",
                [
                    'button:has-text("Approve")',
                    'a:has-text("Approve")',
                    'button:has-text("Verify")',
                    'a:has-text("Verify")',
                ],
            ),
        ]:
            clicked, sel = try_click(page, sels, timeout=10000)
            if clicked:
                page.wait_for_timeout(2000)
                snip(page, f"P5_action_{action_label}")
                note_nav("P5", f"Action {action_label} via {sel}")

        # Poll for progress language
        for i in range(4):
            page.wait_for_timeout(2000)
            page.reload(wait_until="domcontentloaded")
            snip(page, f"P5_progress_poll_{i}")
            body = phases[-1]["text"].lower()
            if any(
                k in body
                for k in [
                    "complete",
                    "ready to review",
                    "extraction complete",
                    "failed",
                    "error",
                    "nodes",
                    "topics",
                    "outcomes",
                ]
            ):
                break

        # Explore review tabs / sections
        for sel in [
            'a:has-text("Review")',
            'button:has-text("Review")',
            'a:has-text("Curriculum")',
            'a:has-text("Structure")',
            'a:has-text("Issues")',
            'a:has-text("Corrections")',
            'a:has-text("Edit")',
            '[role="tab"]:has-text("Review")',
            '[role="tab"]:has-text("Curriculum")',
        ]:
            clicked, _ = try_click(page, [sel])
            if clicked:
                snip(page, "P5_review_surface")
                break
        snip(page, "P5_extraction_review_final")

        # ------------------------------------------------------------------
        # PHASE 6 — Publish
        # ------------------------------------------------------------------
        clicked, sel = try_click(
            page,
            [
                'button:has-text("Publish")',
                'a:has-text("Publish")',
                'button:has-text("Publish Curriculum")',
                'a:has-text("Publish Curriculum")',
                'button:has-text("Publish Subject")',
                'button:has-text("Make Ready")',
                'a:has-text("Make Ready")',
            ],
            timeout=10000,
        )
        if clicked:
            note_nav("P6", f"Publish via {sel}")
            page.wait_for_timeout(1500)
            snip(page, "P6_after_publish_click")
            # Confirm dialogs
            try_click(
                page,
                [
                    'button:has-text("Confirm")',
                    'button:has-text("Yes")',
                    'button:has-text("Publish now")',
                    'button:has-text("Publish")',
                    'input[type="submit"]',
                ],
            )
            page.wait_for_timeout(1500)
            snip(page, "P6_after_publish_confirm")
        else:
            snip(page, "P6_publish_cta_not_found")
            note_nav("P6", "Publish CTA not visible")

        # ------------------------------------------------------------------
        # PHASE 7 — Verification back at catalogue
        # ------------------------------------------------------------------
        for path in [
            "/curriculum-studio/",
            "/curriculum-studio/hub",
            "/curriculum-studio/subjects",
            "/founder/studio/",
        ]:
            resp = page.goto(f"{BASE}{path}", wait_until="domcontentloaded")
            if resp and resp.status < 400:
                snip(page, f"P7_catalogue_{path.strip('/').replace('/', '_')}")
                body = phases[-1]["text"]
                phases[-1]["cs1b_visible"] = "CS1B" in body or "cs1b" in body.lower()
                phases[-1]["ready_for_cs1b"] = bool(
                    re.search(r"CS1B[\s\S]{0,200}Ready|Ready[\s\S]{0,200}CS1B", body, re.I)
                )
                if phases[-1]["cs1b_visible"]:
                    break

        # Open subject detail if listed
        clicked, _ = try_click(
            page,
            [
                'a:has-text("CS1B")',
                'tr:has-text("CS1B") a',
                'a:has-text("View")',
                'a:has-text("Open")',
            ],
        )
        if clicked:
            snip(page, "P7_subject_detail")

        snip(page, "P7_verification_final")

        browser.close()

    payload = {
        "programme": "FV-001B",
        "base": BASE,
        "email": EMAIL,
        "elapsed_s": elapsed(),
        "phases": phases,
        "timeline": timeline,
        "term_hits": term_hits,
        "nav_notes": nav_notes,
        "pdfs": {
            "syllabus": str(SYLLABUS_PDF),
            "syllabus_bytes": SYLLABUS_PDF.stat().st_size if SYLLABUS_PDF.exists() else 0,
            "cmp": str(CMP_PDF),
            "cmp_bytes": CMP_PDF.stat().st_size if CMP_PDF.exists() else 0,
        },
    }
    out_json = EVIDENCE / "phases.json"
    out_json.write_text(json.dumps(payload, indent=2))
    (OUT / "phases.json").write_text(json.dumps(payload, indent=2))
    print("\n\nWrote", out_json)
    print("Phases:", len(phases))
    print("Term hits:", len(term_hits))
    print("Forbidden unique:", sorted({h["term"] for h in term_hits}))


if __name__ == "__main__":
    main()
