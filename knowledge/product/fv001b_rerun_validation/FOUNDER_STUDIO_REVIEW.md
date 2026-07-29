# FV-001B Re-run — Founder Studio Review

**Date:** 2026-07-29  
**Subjects exercised:** CS1R (initial), CS1S (slot probe), CS1T (incomplete regression), CS1U (correct dual upload)  
**Evidence root:** [`_evidence/`](_evidence/)

---

## Phase 1 — Login

**What happened**

- Login at `/auth/login` succeeded.
- Landed on **Kwalitec Console** home with sidebar **CURRICULUM AUTHORITY** (Overview, Subjects, Curriculum Studio, Review Queue, Publishing, Versions, Quality).

**Evaluation**

- Founder environment is immediately recognisable.
- Landing page emphasises operational pulse more than curriculum authority, but the sidebar makes authority clear.
- Next action is not a single curriculum CTA on home; Subjects / Curriculum Studio in the sidebar are still obvious.

**Confidence:** 8/10  
**Evidence:** `screenshots/phase1_login.png`, `phase1_console_home.png`

---

## Phase 2 — Subject Catalogue

**What happened**

- **Subjects** opens a catalogue explaining that students only see a subject as Ready after publish.
- Curriculum workflow strip lists: New Subject → Upload Official CMP → Upload Official Syllabus → Extraction → Review & Corrections → Publish → Available to Students (Ready).
- Create Subject / Open Workspace controls are on the page; Curriculum Studio is one click away.

**Evaluation**

- Subjects are easy to locate.
- Ready / Draft / stage labels appear on workspace rows after create (e.g. `Draft · Subject`, `2026.1 · Validation`).
- Create Subject action is obvious.

**Confidence:** 8/10  
**Evidence:** `screenshots/phase2_subjects.png`, `phase2_studio.png`

---

## Phase 3 — Create Subject

**What happened**

- Created subjects CS1R / CS1S / CS1T / CS1U via Studio Create Subject card (code + title).
- Success: “We've created your subject successfully.”
- Empty submit refused: “We couldn't create this subject. Incomplete or invalid details…”

**Evaluation**

- Workflow clarity: good for create.
- Validation: empty create blocked appropriately.
- Terminology: Founder-friendly.
- Confidence to continue: high at this stage.

**Confidence:** 9/10  
**Evidence:** `screenshots/phase3_created.png`

---

## Phase 4 — Upload Official Documents

**What happened**

- Workspace shows labelled **Official CMP** and **Official Syllabus** slots with rationale.
- Selecting PDFs auto-uploads (no separate Upload button required).
- On CS1U, both files bound correctly:
  - `Official CMP · official_cmp.pdf` — Status Ready  
  - `Official Syllabus · official_syllabus.pdf` — Status Ready  
- Document processing tracker reaches Ready for both.
- On CS1R (first walk), files appeared **crossed** in the slot labels (`CMP · official_syllabus.pdf` / `Syllabus · official_cmp.pdf`) when selection order/heuristics were wrong — slots are easy to mis-bind from a Founder perspective if the wrong file is chosen.

**Evaluation**

- Correct binding is possible and visible.
- Upload progress is understandable once files appear with Ready.
- Rationale for each slot is clear.
- Stale **Validation findings** can still claim documents are “not present” briefly after select, before reload/processing settles — confusing.

**Confidence:** 6/10  
**Evidence:** `screenshots/phase4_workspace.png`, `phase4_both_docs_ready.png`

---

## Phase 5 — Validation

**What happened (CS1U, both documents Ready)**

- Clicked **Validate Curriculum**.
- Flash: “We couldn't complete validation because blocking findings remain… Review the Validation findings below…”
- On the same screen after failure:
  - Content Sources: both documents **Ready**
  - Curriculum review: **0 validation errors**, “Extracted curriculum ready for Founder review”
  - Overview: Documents 2 · Topics 23 · Validation errors 0
  - Status card: “Validation needs attention · in_progress”
  - **No dedicated Validation findings list** explaining the block

**Evaluation**

- Messaging is **internally inconsistent** (blocking failure vs 0 validation errors / documents Ready).
- Next action is **not** obvious — Founder is told to fix findings that are not listed.
- Blocking issues are **not** clearly explained after dual upload.

**Confidence:** 2/10  
**Evidence:** `screenshots/phase5_validate_blocked.png`, `_evidence/complete.json` → `C2_validate`

---

## Phase 6 — Preview

**What happened**

- **Build Preview** flash: “We've built the preview successfully — 2 curriculum topics ready to review.”
- Status card simultaneously: “Preview needs attention · not_ready · 2 topics”
- Curriculum Structure tab shows many real topics/chapters (e.g. Chapter 1–5, syllabus objectives) — meaningful content exists.
- Overview Topics count (23) disagrees with preview line (2 topics).
- On incomplete workspace CS1T: empty preview correctly refused (no success flash).

**Evaluation**

- Meaningful curriculum content **exists** in Structure.
- Success flash **contradicts** `not_ready`.
- Success occurs while validation still failed / in_progress — Founder cannot trust the green banner.
- Zero-topic preview correctly fails on incomplete path (positive).

**Confidence:** 3/10  
**Evidence:** `phase6_preview_contradiction.png`, `phase6_structure_topics.png`, `phase6_preview_success_vs_not_ready.png`, `regression_empty_preview.png`

---

## Phase 7 — Approval

**What happened**

- Clicked **Approve Curriculum**.
- Flash shown: “We couldn't **publish** this curriculum. Publication without approval and a version would expose incomplete material… Assign a version label, complete approval, then try again.”
- Version history already lists `2026.1 (preview_ready)`.
- No clear “approved successfully” message ever appeared.
- Workflow stage remained **Validation**.

**Evaluation**

- Approval requirements are **not** understandable (Approve returns Publish copy).
- Approval does **not** succeed after a preview that claimed success.
- Messaging confuses Approve with Publish.

**Confidence:** 1/10  
**Evidence:** `screenshots/phase7_approve_confused.png`

---

## Phase 8 — Publish

**What happened**

- **Publish Verified Curriculum** refused with the same “without approval and a version” message.
- Incomplete CS1T publish also refused (version / completeness) — safety remains visible.
- No successful publish flash observed on any subject.

**Evaluation**

- Publication does **not** succeed on the complete dual-upload path.
- Safety rules remain enforced on incomplete paths (good).
- Success messaging never achieved; refusal messaging is unambiguous but the complete path never clears the gate.

**Confidence:** 2/10  
**Evidence:** `phase8_publish_refused.png`, `regression_incomplete_publish.png`

---

## Phase 9 — Subject Catalogue Verification

**What happened**

- Subjects list after attempts:
  - CS1R — `2026.1 · Subject`
  - CS1S — `2026.1 · Content Sources`
  - CS1T — `Draft · Subject`
  - CS1U — `2026.1 · Validation`
- **None** show Ready.
- No published date column/value for these subjects.
- Student orientation mentions Ready subjects in the Subject Catalogue but does not show CS1U as selectable Ready content in the captured student surface.

**Evaluation**

- Status Ready: **not observed**
- Current Version / Published Date as post-publish catalogue facts: **not observed**
- Student discoverability of a newly published subject: **not achieved** (publication never completed)

**Confidence:** 2/10  
**Evidence:** `phase9_subjects_not_ready.png`, `phase9_student_orientation.png`

---

## Journey confidence (overall)

| Phase | Score |
|---|---|
| 1 Login | 8 |
| 2 Subjects | 8 |
| 3 Create | 9 |
| 4 Upload | 6 |
| 5 Validate | 2 |
| 6 Preview | 3 |
| 7 Approve | 1 |
| 8 Publish | 2 |
| 9 Catalogue Ready | 2 |
| **End-to-end publish** | **1** |

**Conclusion:** The Founder cannot reliably publish a verified curriculum from beginning to end without assistance.
