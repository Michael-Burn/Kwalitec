# FV-001B Final — Screen-by-Screen Review

**Date:** 2026-07-29  
**Subject:** CS1F  
**Evidence:** `_evidence/screenshots/`

For every major screen: first impression, positives, confusing elements, issues, confidence (0–10).

---

## S1 — Login

| Field | Notes |
|---|---|
| First impression | Clean Sign in · Kwalitec |
| Positive | Familiar auth; no jargon |
| Confusing | None material |
| Critical | None |
| Major | None |
| Minor | None |
| Confidence | 9/10 |
| Evidence | `00_p1_login.png` |

---

## S2 — Console Home (Founder environment)

| Field | Notes |
|---|---|
| First impression | Operational dashboard, not curriculum-first |
| Positive | CURRICULUM AUTHORITY sidebar; INTERNAL ALPHA badge; brand clear |
| Confusing | Primary CTA is “Review attention queue,” not publish curriculum |
| Critical | None |
| Major | None |
| Minor | Home could surface “Open Curriculum Studio / Subjects” as primary for Founder publishing sessions |
| Confidence | 7/10 |
| Evidence | `phase1_console_home.png` |

---

## S3 — Subjects hub

| Field | Notes |
|---|---|
| First impression | Clear catalogue + workflow strip |
| Positive | Ready explained; Create Subject / Open Workspace / Open Curriculum Studio obvious |
| Confusing | Status strings mix version + stage (`2026.1 · Validation`) |
| Critical | None |
| Major | None |
| Minor | Explicit columns for Ready / Current Version / Published Date would match Founder expectations after publish |
| Confidence | 8/10 |
| Evidence | `phase2_subjects.png` |

---

## S4 — Curriculum Studio index

| Field | Notes |
|---|---|
| First impression | Create / Open workspace cards front-and-centre |
| Positive | “Review, validate, preview, approve, and publish” purpose line |
| Confusing | Published / Draft counters without deep links |
| Critical | None |
| Major | None |
| Minor | None |
| Confidence | 8/10 |
| Evidence | `phase2_studio.png` |

---

## S5 — After Create Subject

| Field | Notes |
|---|---|
| First impression | Success flash; return to Studio |
| Positive | “We've created your subject successfully.” |
| Confusing | Must Open Workspace separately (acceptable) |
| Critical | None |
| Major | None |
| Minor | Deep-link into new workspace after create would reduce a step |
| Confidence | 9/10 |
| Evidence | `phase3_created.png` |

---

## S6 — Workspace (pre / post upload)

| Field | Notes |
|---|---|
| First impression | Dense but structured: stage, NEXT STEP, slots, processing, review tabs, actions |
| Positive | Official CMP / Syllabus slots labelled with purpose; Ready status; processing tracker |
| Confusing | Validation findings can appear before upload; NEXT STEP lags document Ready; many simultaneous CTAs (Advance / Validate / Preview / Approve / Publish) |
| Critical | Stale NEXT STEP after docs Ready (see UX-01) |
| Major | All gate actions visible at once encourages out-of-order clicks |
| Minor | “Uploaded by 38” is opaque |
| Confidence | 5/10 |
| Evidence | `phase4_workspace.png`, `phase4_both_docs_ready.png` |

---

## S7 — After Validate Curriculum

| Field | Notes |
|---|---|
| First impression | Failure flash about blocking findings |
| Positive | Safety-oriented refusal language |
| Confusing | Docs Ready + 0 validation errors + Validation `in_progress` + flash “blocking findings”; Validation tab shows warning only |
| Critical | Cannot complete validation; inconsistent messaging (ENG-01, UX-02) |
| Major | NEXT STEP still “Upload…” |
| Minor | Duplicate flash rendering |
| Confidence | 2/10 |
| Evidence | `phase5_validate.png`, `22_p5_validation_panel.png` |

---

## S8 — After Build Preview

| Field | Notes |
|---|---|
| First impression | Success flash (“2 curriculum topics ready to review”) |
| Positive | Structure content looks like real curriculum |
| Confusing | Preview card `not_ready`; version `preview_ready`; Topics 38 vs 2 |
| Critical | Contradictory readiness (ENG-02, UX-03) |
| Major | Cannot trust “Ready for Review” |
| Minor | Overview metrics blank after reload in one capture |
| Confidence | 3/10 |
| Evidence | `phase6_preview.png`, `phase6_structure.png` |

---

## S9 — After Approve Curriculum

| Field | Notes |
|---|---|
| First impression | Publish refusal flash on Approve |
| Positive | Gate language references student safety |
| Confusing | Wrong action named in message; version already present |
| Critical | Approval never confirms (ENG-03, UX-04) |
| Major | Founder cannot tell if approval is blocked or misrouted |
| Minor | None |
| Confidence | 1/10 |
| Evidence | `phase7_approve.png` |

---

## S10 — After Publish Verified Curriculum

| Field | Notes |
|---|---|
| First impression | Same refusal as Approve |
| Positive | Does not falsely claim publish success |
| Confusing | Checklist increments while publish refused; NEXT STEP still upload |
| Critical | Publish never succeeds (ENG-04) |
| Major | Contradictory workflow guidance |
| Minor | None |
| Confidence | 1/10 |
| Evidence | `phase8_publish.png` |

---

## S11 — Subjects after attempted publish

| Field | Notes |
|---|---|
| First impression | CS1F still Content Sources |
| Positive | Catalogue honesty: Ready only after publish |
| Confusing | No Ready / Published Date for CS1F |
| Critical | Phase 9 acceptance unmet (UX-05) |
| Major | None |
| Minor | Status column density |
| Confidence | 3/10 |
| Evidence | `phase9_subjects.png` |

---

## Confidence roll-up

| Screen | Score |
|---|---|
| Login | 9 |
| Console Home | 7 |
| Subjects | 8 |
| Studio index | 8 |
| After create | 9 |
| Workspace upload | 5 |
| After validate | 2 |
| After preview | 3 |
| After approve | 1 |
| After publish | 1 |
| Subjects post-publish | 3 |
| **Journey mean (weighted toward blockers)** | **~3** |
