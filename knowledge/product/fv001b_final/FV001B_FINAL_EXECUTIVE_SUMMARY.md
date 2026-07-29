# FV-001B Final — Executive Summary

**Programme:** FV-001B (Final) — Founder Studio Blind Validation  
**Date:** 2026-07-29  
**Persona:** Founder of Kwalitec (curriculum authority)  
**Method:** Visible UI only (Playwright walkthrough of Create → Upload → Validate → Preview → Approve → Publish → Subjects). No application code, logs, or databases consulted to justify behaviour.  
**Subject exercised:** CS1F — Actuarial Statistics (FV-001B Final)  
**Verdict:** **NO-GO**

---

## Verdict

Founder Studio is **not** production-ready for internal alpha publication.

A Founder can recognise the Console, open Subjects / Curriculum Studio, create a subject, and upload Official CMP and Official Syllabus into the correct labelled slots until both show **Ready** and curriculum structure lists real chapters and learning objectives. The journey then **fails**: validation reports blocking findings while the same screen shows **0 validation errors** and document Ready status; preview announces success while remaining `not_ready`; Approve Curriculum returns a **Publish** refusal message; Publish never succeeds; Subjects never show **Ready** or a published date for CS1F.

---

## Acceptance scorecard

| Criterion | Result | Evidence |
|---|---|---|
| Recognise Founder environment | Pass | `_evidence/screenshots/phase1_console_home.png` |
| Locate Subjects | Pass | `phase2_subjects.png` |
| Create subject | Pass | `phase3_created.png` |
| Upload Official CMP | Pass | `phase4_both_docs_ready.png` |
| Upload Official Syllabus | Pass | `phase4_both_docs_ready.png` |
| Successfully validate | **Fail** | `phase5_validate.png`, `22_p5_validation_panel.png` |
| Generate Preview Ready | **Fail** (contradictory) | `phase6_preview.png` |
| Approve successfully | **Fail** | `phase7_approve.png` |
| Publish successfully | **Fail** | `phase8_publish.png` |
| Observe Ready | **Fail** | `phase9_subjects.png` |
| Observe Current Version | Partial (version label only; not published Ready) | `phase9_subjects.png` |
| Observe Published Date | **Fail** | `phase9_subjects.png` |
| Complete without assistance | **Fail** | Full walk `_evidence/phases.json` |

---

## What works

- **Kwalitec Console / CURRICULUM AUTHORITY** branding and sidebar are immediately recognisable.
- Subjects and Curriculum Studio entry points are obvious; Create Subject succeeds with clear success copy.
- Empty create is refused appropriately.
- Official CMP / Official Syllabus slots are labelled; correct files bind (`official_cmp.pdf` / `official_syllabus.pdf`) and reach Ready with visible processing.
- Curriculum Structure panel shows recognisable chapters and learning objectives after upload.
- Primary chrome avoids Educational Intelligence product jargon (SCI, Twin, Runtime, etc.). Curriculum topic title “Inference” appeared in structure content only — not product chrome.

---

## What blocks launch

1. **Validation cannot complete** after both official documents are Ready; flash cites “blocking findings” while Overview shows **0 validation errors** and the Validation tab shows a document **warning**, not clear blocking findings the Founder can act on as stated.
2. **Preview success vs `not_ready`** — “We've built the preview successfully” while the Preview card stays `not_ready`, with topic counts oscillating (26 / 2 / 38) across cards.
3. **Approve Curriculum** surfaces a **Publish** refusal message; approval never confirms.
4. **Publish never succeeds**; Subjects row for CS1F stays `2026.1 · Content Sources` with no Ready / Published Date.
5. **NEXT STEP** stays stale (“Upload the Official CMP and Official Syllabus…”) after both documents are Ready.

---

## Recommendation

Do **not** proceed to **FV-001C — Student Blind Validation**.

Clear the critical findings in [`UX_FINDINGS_REGISTER.md`](UX_FINDINGS_REGISTER.md) and [`ENGINEERING_FINDINGS_REGISTER.md`](ENGINEERING_FINDINGS_REGISTER.md), then re-run FV-001B Final until a Founder can complete Create → Upload → Validate → Preview → Approve → Publish → Ready on the visible path without contradictory messaging.

---

## Artefacts

| File | Purpose |
|---|---|
| [`FOUNDER_STUDIO_REVIEW.md`](FOUNDER_STUDIO_REVIEW.md) | Phase-by-phase journey |
| [`SCREEN_BY_SCREEN_REVIEW.md`](SCREEN_BY_SCREEN_REVIEW.md) | Per-screen UX template |
| [`UX_FINDINGS_REGISTER.md`](UX_FINDINGS_REGISTER.md) | Usability findings |
| [`ENGINEERING_FINDINGS_REGISTER.md`](ENGINEERING_FINDINGS_REGISTER.md) | Engineering findings (visible symptoms) |
| [`TERMINOLOGY_AUDIT.md`](TERMINOLOGY_AUDIT.md) | Language audit |
| [`NAVIGATION_AUDIT.md`](NAVIGATION_AUDIT.md) | Next-action clarity |
| [`FINAL_VERDICT.md`](FINAL_VERDICT.md) | Sign-off |
| [`_evidence/`](_evidence/) | Screenshots + `phases.json` |
