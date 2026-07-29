# FV-001B Final — Engineering Findings Register

**Programme:** FV-001B (Final)  
**Classification:** Engineering (visible symptoms only — no code inspection)  
**Date:** 2026-07-29

These are failures of transition, state consistency, or unexpected outcomes observed in the visible product. They are distinguished from pure usability copy/layout issues.

---

## ENG-01 — Validate Curriculum fails after both official documents Ready

| | |
|---|---|
| **Severity** | Critical |
| **Classification** | Engineering |
| **Observation** | With Official CMP and Official Syllabus both STATUS Ready and structure extracted, Validate Curriculum returns: “We couldn't complete validation because blocking findings remain.” Status stays `Validation needs attention · in_progress`. Workflow does not advance to Validation complete. |
| **Evidence** | `phase5_validate.png`; `phases.json` P5_validate flashes; docs Ready in same screenshots |
| **Expected (Founder)** | Validation completes successfully, or lists concrete blocking findings that match document state. |

---

## ENG-02 — Preview success flash with persistent not_ready state

| | |
|---|---|
| **Severity** | Critical |
| **Classification** | Engineering |
| **Observation** | Build Preview shows success (“We've built the preview successfully — 2 curriculum topics ready to review”) while Preview card remains `not_ready`. Version history simultaneously shows `2026.1 (preview_ready)`. Topic counts disagree (2 vs 38 vs earlier 26). |
| **Evidence** | `phase6_preview.png`; `phases.json` P6_preview |
| **Expected (Founder)** | One authoritative readiness state after Build Preview. |

---

## ENG-03 — Approve Curriculum returns Publish refusal; approval never confirms

| | |
|---|---|
| **Severity** | Critical |
| **Classification** | Engineering |
| **Observation** | Approve Curriculum yields publish-gate copy (“We couldn't publish… Publication without approval and a version…”). No “approved” confirmation. Version label `2026.1` already visible. |
| **Evidence** | `phase7_approve.png` |
| **Expected (Founder)** | Approve either confirms approval or explains why *approval* (not publish) is blocked. |

---

## ENG-04 — Publish Verified Curriculum never succeeds

| | |
|---|---|
| **Severity** | Critical |
| **Classification** | Engineering |
| **Observation** | Publish Verified Curriculum returns the same refusal as Approve. Subject does not become Ready. Stage remains Content Sources. |
| **Evidence** | `phase8_publish.png`; `phase9_subjects.png` (`CS1F` → `2026.1 · Content Sources`) |
| **Expected (Founder)** | After successful validate → preview → approve, publish marks Ready with version and published date. |

---

## ENG-05 — Validation panel warning vs blocking-findings flash

| | |
|---|---|
| **Severity** | Major |
| **Classification** | Engineering |
| **Observation** | After failed Validate, Validation tab shows Document 6 Passed · 0 issues and Document 7 Passed · 1 **warning** (`missing_learning_objective`). Flash claims **blocking** findings. Overview: 0 validation errors. |
| **Evidence** | `22_p5_validation_panel.png`; `phase5_validate.png` |
| **Expected (Founder)** | Severity of findings matches refusal language. |

---

## ENG-06 — Checklist advances without successful publish

| | |
|---|---|
| **Severity** | Minor |
| **Classification** | Engineering |
| **Observation** | Checklist moves from 4 of 8 to 5 of 8 around publish attempt while publish is refused and Ready is not achieved. |
| **Evidence** | `phases.json` P7 vs P8 status.checklist; `phase8_publish.png` |
| **Expected (Founder)** | Checklist progress reflects completed gates only. |

---

## Summary counts

| Severity | Count |
|---|---|
| Critical | 4 |
| Major | 1 |
| Minor | 1 |

---

## Note on prior engineering programmes

Pre-conditions listed PI-002 / PI-002R / EV-001 / EE-001 as complete. This Final blind walk still observed the above **visible** publication-path failures on CS1F. Engineering reports were not used to excuse or reinterpret the UI.
