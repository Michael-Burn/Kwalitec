# FV-001B Final — Founder Studio Review

**Programme:** FV-001B (Final)  
**Release Candidate:** RC-2026.07.29-01  
**Date:** 2026-07-29  
**Subject exercised:** CS1V — Actuarial Statistics (FV-001B Final RC-001)  
**Workspace:** `ws-cs1v`  
**Evidence root:** [`_evidence/`](_evidence/)  
**Method:** Visible product only

---

## Phase 1 — Login / Enter Founder Studio

**What happened**

- Signed in at `/auth/login`.
- Landed on **Console Home** with sidebar **CURRICULUM AUTHORITY** (Overview, Subjects, Curriculum Studio, Review Queue, Publishing, Versions, Quality, …).
- INTERNAL ALPHA badge visible.

**Evaluation**

- Founder environment is immediately recognisable.
- Home emphasises attention/operations; Subjects / Curriculum Studio are one click away.

**Confidence:** 8/10  
**Evidence:** `screenshots/00_p1_login.png`, `phase1_console_home.png`

---

## Phase 2 — Subjects

**What happened**

- **Subjects** explains students only see a subject as Ready after publish.
- Curriculum workflow strip lists New Subject → Upload Official CMP → Upload Official Syllabus → Extraction → Review & Corrections → Publish → Available to Students (Ready).
- Create Subject / Open Workspace controls present; Curriculum Studio reachable from sidebar and page CTA.

**Evaluation**

- Subjects are easy to find; Create Subject is obvious.
- Secondary nav (Review Queue, Publishing, Versions, Quality) is discoverable but not required for the happy path.

**Confidence:** 8/10  
**Evidence:** `screenshots/phase2_subjects.png`, `phase2_studio.png`

---

## Phase 3 — Create Subject

**What happened**

- Created **CS1V** via Studio Create Subject (code + title + exam series / paper / version).
- Success: “We've created your subject successfully.”
- Empty submit refused with incomplete-details messaging (safety regression check).

**Evaluation**

- Create flow is clear and trustworthy.
- Opening the workspace is a separate intentional step (acceptable).

**Confidence:** 9/10  
**Evidence:** `screenshots/phase3_created.png`, `39_r_empty_create.png` (if captured as `R_empty_create`)

---

## Phase 4 — Upload Documents

**What happened**

- Opened workspace `ws-cs1v`.
- Uploaded Official CMP and Official Syllabus into labelled slots (RC EV-001 CS1V fixtures).
- Both slots show **STATUS Ready**; document processing reaches Ready for both.
- Curriculum Structure lists chapters and learning objectives.

**Evaluation**

- Correct slots and Ready status are clear.
- **NEXT STEP** still says “Confirm the subject…” then “Upload the Official CMP…” after both files are Ready — trust friction (Condition 1).

**Confidence:** 7/10  
**Evidence:** `screenshots/phase4_workspace.png`, `phase4_both_docs_ready.png`

---

## Phase 5 — Validation

**What happened**

- Advanced to Content Sources.
- Clicked **Validate Curriculum**.
- Success: “We've completed validation successfully.” Status: “Validation completed successfully · passed.”
- Overview: 0 awaiting review · 0 validation errors.
- Findings panel still shows “Missing learning objectives asset reference” with guidance to re-validate (Condition 2).

**Evaluation**

- Validation **succeeds** from a Founder perspective; publication is not blocked.
- Findings panel vs “passed” / “0 validation errors” remains confusing but non-blocking on this RC.

**Confidence:** 7/10  
**Evidence:** `screenshots/phase5_validate.png`, `20_p5_validate.png`

---

## Phase 6 — Preview

**What happened**

- Clicked **Build Preview**.
- Success: “We've built the preview successfully — 23 curriculum topics ready to review.”
- Status: “Preview ready · ready_for_review · 23 topics.”
- Structure panel shows topic hierarchy; Overview Topics tile shows **28**.

**Evaluation**

- Preview Ready is achieved honestly (no success-vs-not_ready contradiction).
- Topic count 28 vs 23 is a minor presentation inconsistency (Condition 3).

**Confidence:** 8/10  
**Evidence:** `screenshots/phase6_preview.png`, `phase6_structure.png`

---

## Phase 7 — Approve

**What happened**

- Clicked **Approve Curriculum**.
- Success: “We've approved your curriculum successfully.”
- Preview card advances to “Preview ready · approved · 23 topics.”
- Version history shows `2026.1 (approved)`.

**Evaluation**

- Approval confirms correctly (no Publish-refusal copy on Approve).
- NEXT STEP remains stale; Stage strip still on Content Sources.

**Confidence:** 8/10  
**Evidence:** `screenshots/phase7_approve.png`

---

## Phase 8 — Publish

**What happened**

- Clicked **Publish Verified Curriculum**.
- Success: “We've published your verified curriculum successfully.”
- Header Status: **Published** · Version 2026.1.
- Checklist: All 8 checklist items are ready.
- Version history: `2026.1 (published)`.

**Evaluation**

- Publish succeeds and is clearly communicated.
- Workflow strip / NEXT STEP still lag behind Status Published (Condition 1).

**Confidence:** 8/10  
**Evidence:** `screenshots/phase8_publish.png`

---

## Phase 9 — Return to Subjects / Verify Ready

**What happened**

- Returned to Subjects / Studio subjects list.
- CS1V row: **Ready · Current Version 2026.1 · Published 2026-07-28**.

**Evaluation**

- Ready, Current Version, and Published Date are all visible without assistance.
- This closes the Founder publication loop for this RC.

**Confidence:** 9/10  
**Evidence:** `screenshots/phase9_subjects.png`, `33_p9_console_subjects.png`

---

## Overall Founder confidence

| Area | Score |
|---|---|
| Enter Studio / navigate | 8 |
| Create + upload | 8 |
| Validate → Preview → Approve → Publish | 8 |
| Observe Ready outcomes | 9 |
| Trust in guidance chrome (NEXT STEP / findings) | 5 |

**Net:** Operational for internal Alpha Founder publication, with residual guidance honesty conditions.
