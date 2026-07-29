# FV-001B Re-run — Executive Summary

**Programme:** FV-001B (Re-run) — Founder Studio Blind Validation  
**Date:** 2026-07-29  
**Persona:** Founder of Kwalitec (curriculum authority)  
**Method:** Visible UI only (Playwright walkthrough). No application code, logs, or databases consulted to justify behaviour.  
**Verdict:** **NO-GO**

---

## Verdict

Founder Studio is **not** ready for internal production curriculum publication.

A Founder can recognise the Console, locate Subjects, create a subject, and upload Official CMP / Official Syllabus into the labelled slots. Document processing reaches **Ready** and curriculum structure shows real topics. The journey then **stalls**: validation reports blocking findings without a usable findings list, preview success contradicts `not_ready`, Approve returns a Publish refusal message, and Publish never succeeds. Subject Catalogue never shows **Ready**, current published version, or published date for the exercised subjects.

---

## Acceptance scorecard

| Criterion | Result | Evidence |
|---|---|---|
| Recognise Founder environment | Pass | `_evidence/screenshots/phase1_console_home.png` |
| Locate Subjects | Pass | `phase2_subjects.png` |
| Create subject | Pass | `phase3_created.png` |
| Upload Official CMP | Pass (when slot correct) | `phase4_both_docs_ready.png` |
| Upload Official Syllabus | Pass (when slot correct) | `phase4_both_docs_ready.png` |
| Successfully validate | **Fail** | `phase5_validate_blocked.png`, `complete.json` C2 |
| Meaningful preview | Partial / contradictory | `phase6_preview_contradiction.png`, `phase6_structure_topics.png` |
| Approve curriculum | **Fail** | `phase7_approve_confused.png` |
| Publish successfully | **Fail** | `phase8_publish_refused.png` |
| Subject status = Ready | **Fail** | `phase9_subjects_not_ready.png` |
| Current Version displayed | Fail (no published Ready row) | `phase9_subjects_not_ready.png` |
| Published Date displayed | **Fail** | `phase9_subjects_not_ready.png` |
| No contradictory messaging | **Fail** | Preview / Validation / Approve flashes |
| No unnecessary EI terminology (primary) | Pass | `phases.json` term_hits = [] |

---

## What works

- Console branding and **CURRICULUM AUTHORITY** navigation are immediately recognisable.
- Subjects + Curriculum Studio entry points are obvious.
- Create Subject succeeds with clear success copy; empty create is refused.
- Official CMP / Syllabus slots are labelled with purpose; correct files bind and show Ready.
- Empty-preview path refuses success (`regression_empty_preview.png`).
- Incomplete publish is refused (safety still visible).
- Primary chrome avoids Educational Intelligence jargon (SCI, Twin, Runtime, etc.).

---

## What blocks launch

1. **Validation cannot complete** after both official documents are Ready, with **no actionable findings list** under the failure flash.  
2. **Preview success vs `not_ready`** contradictory messaging while topics exist.  
3. **Approve Curriculum** surfaces a **Publish** refusal message; approval never confirms.  
4. **Publish never succeeds**; Subject Catalogue never reaches Ready.  
5. **NEXT STEP** and status cards stay stale relative to documents / topics already present.

---

## Recommendation

Do **not** proceed to **FV-001C — Student Blind Validation** until a Founder can complete Create → Upload → Validate → Preview → Approve → Publish → Ready on the visible path without contradictory messaging.

Re-run FV-001B after the P0 actions in [`PRIORITISED_ACTIONS.md`](PRIORITISED_ACTIONS.md) are cleared.

---

## Artefacts

| File | Purpose |
|---|---|
| [`FOUNDER_STUDIO_REVIEW.md`](FOUNDER_STUDIO_REVIEW.md) | Phase-by-phase journey |
| [`SCREEN_BY_SCREEN_REVIEW.md`](SCREEN_BY_SCREEN_REVIEW.md) | Per-screen template |
| [`REGRESSION_AUDIT.md`](REGRESSION_AUDIT.md) | Safety / gate regressions |
| [`TERMINOLOGY_AUDIT.md`](TERMINOLOGY_AUDIT.md) | Language audit |
| [`NAVIGATION_AUDIT.md`](NAVIGATION_AUDIT.md) | Next-action clarity |
| [`UX_DEFECT_REGISTER.md`](UX_DEFECT_REGISTER.md) | Defects |
| [`LAUNCH_BLOCKERS.md`](LAUNCH_BLOCKERS.md) | Blockers LB-R1… |
| [`PRIORITISED_ACTIONS.md`](PRIORITISED_ACTIONS.md) | P0 / P1 / P2 |
| [`FINAL_VERDICT.md`](FINAL_VERDICT.md) | Sign-off |
| [`_evidence/`](_evidence/) | Screenshots + JSON captures |
