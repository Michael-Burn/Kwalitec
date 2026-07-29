# FV-001B Final — UX Findings Register

**Programme:** FV-001B (Final)  
**Classification:** Usability only (see Engineering register for state/transition failures)  
**Date:** 2026-07-29

Every finding is **Usability**. Severity: Critical / Major / Minor.

---

## UX-01 — Stale NEXT STEP after documents Ready

| | |
|---|---|
| **Severity** | Critical |
| **Classification** | Usability |
| **Where** | Workspace CS1F after Official CMP + Syllabus Ready |
| **Observation** | NEXT STEP continues: “Upload the Official CMP and Official Syllabus PDFs, then validate the curriculum” while both slots show STATUS Ready and DOCUMENTS UPLOADED. |
| **Evidence** | `phase4_both_docs_ready.png`, `phase5_validate.png`, `phases.json` P5_* status.next_step |
| **Founder impact** | Undermines trust; Founder re-checks uploads instead of advancing. |

---

## UX-02 — Validation failure messaging contradicts “0 validation errors”

| | |
|---|---|
| **Severity** | Critical |
| **Classification** | Usability |
| **Where** | After Validate Curriculum |
| **Observation** | Flash says blocking findings remain and to review Validation findings. Overview shows “0 validation errors.” Validation needs attention · in_progress. Founder cannot reconcile what to fix. |
| **Evidence** | `phase5_validate.png`, `22_p5_validation_panel.png` |
| **Founder impact** | Cannot confidently complete validation without assistance. |

---

## UX-03 — Preview success vs not_ready + topic count chaos

| | |
|---|---|
| **Severity** | Critical |
| **Classification** | Usability |
| **Where** | After Build Preview |
| **Observation** | Flash: “We've built the preview successfully — 2 curriculum topics ready to review.” Preview card: `not_ready · 2 topics`. Overview Topics: 38. Version history: `preview_ready`. Earlier card showed 26 topics. |
| **Evidence** | `phase6_preview.png`, `phases.json` P6_preview |
| **Founder impact** | Cannot tell whether Preview is Ready for Review. |

---

## UX-04 — Approve Curriculum shows Publish refusal copy

| | |
|---|---|
| **Severity** | Critical |
| **Classification** | Usability |
| **Where** | Approve Curriculum button |
| **Observation** | Pressing Approve yields: “We couldn't **publish** this curriculum. Publication without approval…” — wrong verb for the control; no approval confirmation. |
| **Evidence** | `phase7_approve.png` |
| **Founder impact** | Ambiguity about whether approval exists; Founder cannot proceed. |

---

## UX-05 — Subjects hub never shows Ready / Published Date for CS1F

| | |
|---|---|
| **Severity** | Critical |
| **Classification** | Usability |
| **Where** | Subjects / Studio subjects after publish attempt |
| **Observation** | CS1F displays `2026.1 · Content Sources` only — no Ready, no Published Date. |
| **Evidence** | `phase9_subjects.png` |
| **Founder impact** | Cannot verify publication outcome from the hub. |

---

## UX-06 — All workflow actions visible simultaneously

| | |
|---|---|
| **Severity** | Major |
| **Classification** | Usability |
| **Where** | Workspace Actions |
| **Observation** | Advance, Validate, Build Preview, Approve, and Publish are all available together regardless of stage. |
| **Evidence** | `phase4_workspace.png`, `phase5_validate.png` |
| **Founder impact** | Encourages out-of-order attempts; increases confusion when refusals appear. |

---

## UX-07 — Console Home primary CTA is not curriculum publication

| | |
|---|---|
| **Severity** | Minor |
| **Classification** | Usability |
| **Where** | Console Home |
| **Observation** | Primary button is “Review attention queue”; curriculum path lives in sidebar. |
| **Evidence** | `phase1_console_home.png` |
| **Founder impact** | Slight friction for a Founder arriving to publish. Does not alone block the journey. |

---

## UX-08 — “Uploaded by 38”

| | |
|---|---|
| **Severity** | Minor |
| **Classification** | Usability |
| **Where** | Document slots |
| **Observation** | Uploader shown as numeric id `38`. |
| **Evidence** | `phase4_both_docs_ready.png` |
| **Founder impact** | Low; looks unfinished. |

---

## Summary counts

| Severity | Count |
|---|---|
| Critical | 5 |
| Major | 1 |
| Minor | 2 |
