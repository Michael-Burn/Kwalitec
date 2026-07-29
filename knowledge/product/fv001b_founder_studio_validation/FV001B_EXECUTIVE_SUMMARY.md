# FV-001B — Executive Summary

**Programme:** FV-001B — Founder Studio Blind Validation  
**Date:** 2026-07-28  
**Predecessor:** PX-002 — Product Experience Implementation  
**Persona:** Founder / Curriculum Authority preparing official IFoA curricula  
**Method:** Visible Founder Console / Curriculum Studio only (Playwright walkthrough on a clean instance). No source inspection. No architecture defence.

**Evidence:** [`_evidence/precise.json`](_evidence/precise.json) · [`_evidence/focus.json`](_evidence/focus.json) · [`_evidence/phases.json`](_evidence/phases.json) · [`_evidence/screenshots/`](_evidence/screenshots/)

---

## Verdict

# NO-GO

Founder Studio is **not** ready for reliable internal production curriculum publication.

A Founder can enter the Curriculum Authority environment, find Subjects, create a subject, open a workspace, and upload Official CMP / Official Syllabus PDFs. The workflow **stops** before a trustworthy publish: validation refuses completion, preview reports **0 nodes**, approve/publish are blocked, and the subject never becomes **Ready**.

---

## What worked

| Capability | Observation |
|---|---|
| Role recognition after login | Landed in **Kwalitec Console** with sidebar badge **CURRICULUM AUTHORITY** and Subjects / Curriculum Studio nav |
| Locate Subjects | **Subjects** is a primary sidebar item; page states students only see Ready after publish |
| Create Subject | Inline form (code + title); confirmation *“We've created your subject successfully.”* |
| Upload rationale | Official CMP and Official Syllabus slots explain why each PDF is required |
| Upload acceptance | PDFs accepted with STATUS **Ready**, version, size, timestamp |
| Safety gates | Incomplete approve/publish correctly refused with plain-language flashes |

---

## What failed (evidence)

1. **Cannot publish a verified curriculum** — Publish flash: *“Publication without approval and a version would expose incomplete material…”*; Studio counters remain **Published 0 / Drafts 1**.
2. **Nothing trustworthy to review** — Preview: *“Preview ready · not_ready · 0 nodes”* while flash says preview built successfully.
3. **Validation contradicts itself** — Flash: validation could not complete (blocking findings); same screen NEXT STEP: *“Validation looks ready”*; panel also shows *“0 validation errors”*.
4. **Documents land in the wrong slots** — `official_syllabus.pdf` under Official CMP; `official_cmp.pdf` under Official Syllabus (slot order vs file chooser order).
5. **Subject Catalogue does not communicate Ready** — CS1B listed as `2026.1 · Validation` / Content Sources; no Ready / Draft / Coming Soon status model a Founder can trust.
6. **Engineering chrome on the Founder surface** — Workspace tabs: PIPELINE, KNOWLEDGE GRAPH, EVIDENCE EXPLORER, ENTITY DETAILS; Pipeline audit mentions *Inference*.

---

## Acceptance criteria scorecard

| Criterion | Result |
|---|---|
| Understand Founder environment immediately | **Partial** — Console + CURRICULUM AUTHORITY yes; Console Home is ops pulse, not curriculum-first |
| Locate Subjects without confusion | **Pass** |
| Create a new subject | **Pass** |
| Upload official syllabus | **Pass** (slot confusion risk) |
| Upload official CMP | **Pass** (slot confusion risk) |
| Understand extraction progress | **Partial** — timings visible; technical Pipeline language |
| Review extracted curriculum | **Fail** — 0 nodes; Review Queue has no structure to correct |
| Publish verified curriculum | **Fail** |
| Confirm subject is Ready | **Fail** |
| No unnecessary Educational Intelligence terminology | **Fail** — Knowledge Graph, Pipeline, Entity Details, Inference |

**Pass count:** 3 / 10 · **Partial:** 2 · **Fail:** 5

---

## Recommendation

Do **not** proceed to wider Founder Studio deployment or treat PX-002 as Founder-validated until Critical blockers in [`LAUNCH_BLOCKERS.md`](LAUNCH_BLOCKERS.md) are cleared and a re-run of FV-001B can reach **Ready**.

FV-001C — Student Blind Validation should wait until at least one subject can be published Ready through the visible Founder path (or FV-001C is explicitly scoped to built-in Ready subjects only).

---

## Companion artefacts

| Artefact | Purpose |
|---|---|
| [`FOUNDER_STUDIO_REVIEW.md`](FOUNDER_STUDIO_REVIEW.md) | Journey phases + scores |
| [`SCREEN_BY_SCREEN_REVIEW.md`](SCREEN_BY_SCREEN_REVIEW.md) | Per-screen template reviews |
| [`TERMINOLOGY_AUDIT.md`](TERMINOLOGY_AUDIT.md) | Forbidden / mismatched terms |
| [`NAVIGATION_AUDIT.md`](NAVIGATION_AUDIT.md) | Next-action clarity |
| [`UX_DEFECT_REGISTER.md`](UX_DEFECT_REGISTER.md) | Defect inventory |
| [`LAUNCH_BLOCKERS.md`](LAUNCH_BLOCKERS.md) | Critical blockers |
| [`PRIORITISED_ACTIONS.md`](PRIORITISED_ACTIONS.md) | Ordered fixes |
| [`FINAL_VERDICT.md`](FINAL_VERDICT.md) | Sign-off verdict |
