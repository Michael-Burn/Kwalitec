# FV-001B Final — UX Findings Register

**Programme:** FV-001B (Final)  
**Release Candidate:** RC-2026.07.29-01  
**Date:** 2026-07-29  
**Method:** Visible product only

Severity: Critical / Major / Minor.

---

## UX-01 — Stale NEXT STEP after documents Ready / after Publish

| | |
|---|---|
| **Severity** | Major |
| **Classification** | Usability |
| **Where** | Workspace CS1V after Official CMP + Syllabus Ready; still present after Validate / Preview / Approve / Publish |
| **Observation** | NEXT STEP continues: “Upload the Official CMP and Official Syllabus PDFs, then validate the curriculum” while both slots show STATUS Ready, Status is Published, and Subjects shows Ready. |
| **Evidence** | `phase4_both_docs_ready.png`, `phase5_validate.png`, `phase8_publish.png`, `phases.json` status.next_step |
| **Founder impact** | Undermines trust; Founder may re-check uploads instead of advancing. Did **not** block publication on this RC. |
| **Recommendation** | Drive NEXT STEP from authoritative lifecycle state (docs Ready → Validate; validated → Preview; …; Published → Subjects Ready). |

---

## UX-02 — Validation findings panel vs Validation passed

| | |
|---|---|
| **Severity** | Major |
| **Classification** | Usability |
| **Where** | After Validate Curriculum through Publish |
| **Observation** | Status card: “Validation completed successfully · passed.” Overview: “0 validation errors.” Findings panel still shows “Missing learning objectives asset reference” with copy implying unresolved findings can block publication. |
| **Evidence** | `phase5_validate.png`, `phase8_publish.png` |
| **Founder impact** | Trust friction; Founder may hesitate to Approve/Publish. On this RC, Approve and Publish still succeeded. |
| **Recommendation** | Hide or demote non-blocking findings after pass; or label severity explicitly (warning vs blocking) and align “0 validation errors” with the panel. |

---

## UX-03 — Workflow stage chrome lags Status Published

| | |
|---|---|
| **Severity** | Major |
| **Classification** | Usability / Workflow |
| **Where** | Workspace header + workflow strip after Publish |
| **Observation** | Status line shows Status: **Published**, but Stage remains **Content Sources** and the strip highlight stays on Content Sources. |
| **Evidence** | `phase8_publish.png` |
| **Founder impact** | Mixed signals about “where am I?”; Status + Subjects Ready still allow completion. |
| **Recommendation** | Advance workflow chrome with lifecycle (Publish highlight / completed stages) when Status becomes Published. |

---

## UX-04 — Topic count inconsistency (28 vs 23)

| | |
|---|---|
| **Severity** | Minor |
| **Classification** | Presentation |
| **Where** | Curriculum review Overview Topics vs Preview status card |
| **Observation** | Overview tile shows Topics **28**; Preview status shows **23 topics**. |
| **Evidence** | `phase6_preview.png`, `phase8_publish.png` |
| **Founder impact** | Mild uncertainty about structure completeness; did not block Preview Ready. |
| **Recommendation** | Use one authoritative topic count for overview and preview cards. |

---

## UX-05 — Console Home is operations-first

| | |
|---|---|
| **Severity** | Minor |
| **Classification** | Usability |
| **Where** | Console Home after login |
| **Observation** | Primary attention is review/support pulse, not “publish a curriculum.” |
| **Evidence** | `phase1_console_home.png` |
| **Founder impact** | One extra click to Subjects / Studio; path still discoverable. |
| **Recommendation** | Optional publishing quick action for Founder Alpha sessions. |

---

## Cleared vs prior FV-001B Final (non-RC)

| Prior critical finding | This RC outcome |
|---|---|
| Validate fails / blocking findings vs 0 errors | **Cleared** — Validate succeeds; publish proceeds |
| Preview success vs not_ready | **Cleared** — Preview ready with 23 topics |
| Approve shows Publish refusal | **Cleared** — Approve confirms successfully |
| Publish never succeeds / no Ready | **Cleared** — Published; Ready · Version · Date visible |

---

## Non-findings

- “Inference” in Curriculum Structure is a **syllabus chapter title**, not product EI jargon.
- Empty Create Subject correctly refused incomplete details.
