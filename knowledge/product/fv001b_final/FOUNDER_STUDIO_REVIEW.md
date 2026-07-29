# FV-001B Final — Founder Studio Review

**Date:** 2026-07-29  
**Subject exercised:** CS1F — Actuarial Statistics (FV-001B Final)  
**Evidence root:** [`_evidence/`](_evidence/)  
**Method:** Visible product only

---

## Phase 1 — Enter Founder Studio

**What happened**

- Signed in at `/auth/login`.
- Landed on **Console Home** with sidebar **CURRICULUM AUTHORITY** (Overview, Subjects, Curriculum Studio, Review Queue, Publishing, Versions, Quality, …).
- Home emphasises operational pulse (“Review attention queue”) more than curriculum publication.

**Evaluation**

- Founder environment is immediately recognisable.
- Navigation is intuitive via the sidebar.
- Primary action on home is operations-oriented, not “publish a curriculum,” but Subjects / Curriculum Studio are one click away.

**Confidence:** 8/10  
**Evidence:** `screenshots/phase1_console_home.png`, `02_p1_console_home.png`

---

## Phase 2 — Subjects

**What happened**

- **Subjects** opens a catalogue explaining that students only see a subject as Ready after publish.
- Curriculum workflow strip lists: New Subject → Upload Official CMP → Upload Official Syllabus → Extraction → Review & Corrections → Publish → Available to Students (Ready).
- Create Subject / Open Workspace controls are on the page; Curriculum Studio is one click away.

**Evaluation**

- Subjects are easy to find.
- Status values on workspace rows are abbreviated stage labels (e.g. `Draft · Subject`, `2026.1 · Validation`) — understandable at a glance once learned.
- Create Subject is obvious.

**Confidence:** 8/10  
**Evidence:** `screenshots/phase2_subjects.png`, `phase2_studio.png`

---

## Phase 3 — Create Subject

**What happened**

- Created **CS1F** via Studio Create Subject card (code + title).
- Success: “We've created your subject successfully.”
- Empty submit refused: “We couldn't create this subject. Incomplete or invalid details…”

**Evaluation**

- Workflow, terminology, and validation feel sound.
- Confidence to continue is high at this stage.

**Confidence:** 9/10  
**Evidence:** `screenshots/phase3_created.png`, `39_r_empty_create.png`

---

## Phase 4 — Upload Documents

**What happened**

- Opened workspace `ws-cs1f`.
- Uploaded Official CMP (`official_cmp.pdf`) and Official Syllabus (`official_syllabus.pdf`) into the labelled slots.
- Both slots show **STATUS Ready**; document processing reaches Ready for both.
- Curriculum Structure lists chapters and learning objectives (e.g. Chapter 1 Data exploration, Chapter 4 Inference).

**Evaluation**

- Correct slots are clear; upload progress and Ready status are visible.
- Document confidence is high once Ready appears.
- **NEXT STEP** still says “Confirm the subject…” / later “Upload the Official CMP…” even after both files are Ready — undermines trust.

**Confidence:** 7/10 (Ready docs strong; stale guidance weakens confidence)  
**Evidence:** `screenshots/phase4_workspace.png`, `phase4_both_docs_ready.png`, `17_p5_panel_curriculum_structure.png`

---

## Phase 5 — Validation

**What happened**

- Advanced to Content Sources (“We've advanced the workflow to the next stage.”).
- Clicked **Validate Curriculum**.
- Flash: “We couldn't complete validation because blocking findings remain… Review the Validation findings below…”
- Overview remains “0 awaiting review · **0 validation errors**.”
- Validation tab shows Document 6 Passed · 0 issues; Document 7 Passed · 1 warning (`missing_learning_objective`).
- Status card: “Validation needs attention · in_progress.”
- NEXT STEP still: “Upload the Official CMP and Official Syllabus PDFs, then validate…”

**Evaluation**

- Validation does **not** complete successfully from a Founder perspective.
- Messaging is internally inconsistent (blocking findings vs 0 validation errors vs in_progress vs Ready documents).
- Next step is not obvious — guidance contradicts Ready document state.

**Confidence:** 2/10  
**Evidence:** `screenshots/phase5_validate.png`, `22_p5_validation_panel.png`

---

## Phase 6 — Preview

**What happened**

- Clicked **Build Preview**.
- Flash: “We've built the preview successfully — 2 curriculum topics ready to review.”
- Preview card remains: “Preview needs attention · **not_ready** · 2 topics.”
- Overview Topics = **38**; earlier status showed **26** topics; Version history shows `2026.1 (preview_ready)`.
- Structure panel still shows chapters and learning objectives.

**Evaluation**

- Hierarchy is understandable when opened.
- “Preview Ready for Review” is **not** trustworthy — success flash, `preview_ready` version label, and `not_ready` status card contradict each other.
- Extracted curriculum looks real, but readiness state is ambiguous.

**Confidence:** 3/10  
**Evidence:** `screenshots/phase6_preview.png`, `phase6_structure.png`

---

## Phase 7 — Approval

**What happened**

- Clicked **Approve Curriculum**.
- Flash: “We couldn't **publish** this curriculum. Publication without approval and a version would expose incomplete material… Assign a version label, complete approval, then try again.”
- Version already shows `2026.1 (preview_ready)`.
- No confirmation that approval succeeded.

**Evaluation**

- Approval does not succeed.
- Messaging is wrong for the control pressed (Approve → Publish refusal).
- High ambiguity about approval state.

**Confidence:** 1/10  
**Evidence:** `screenshots/phase7_approve.png`

---

## Phase 8 — Publication

**What happened**

- Clicked **Publish Verified Curriculum**.
- Same Publish refusal flash as Approve.
- Stage remains Content Sources; checklist advances to “5 of 8” without a published Ready outcome.

**Evaluation**

- Publication does not succeed.
- Success messaging is absent; workflow guidance remains contradictory (NEXT STEP still upload docs).

**Confidence:** 1/10  
**Evidence:** `screenshots/phase8_publish.png`

---

## Phase 9 — Subjects Hub

**What happened**

- Returned to Subjects / Studio subjects.
- CS1F row: `2026.1 · Content Sources`.
- No **Ready** status, no **Published Date** for CS1F.
- Catalogue correctly continues to explain Ready = after publish.

**Evaluation**

- Ready / Current Version / Published Date are **not** immediately visible as a published subject outcome for CS1F.
- Version fragment `2026.1` appears, but without Ready / Published Date it fails Phase 9 acceptance.

**Confidence:** 3/10  
**Evidence:** `screenshots/phase9_subjects.png`

---

## Journey summary

| Phase | Outcome |
|---|---|
| 1 Enter | Pass |
| 2 Subjects | Pass |
| 3 Create | Pass |
| 4 Upload | Pass (with stale NEXT STEP) |
| 5 Validate | **Fail** |
| 6 Preview | **Fail** (contradictory) |
| 7 Approve | **Fail** |
| 8 Publish | **Fail** |
| 9 Subjects Ready | **Fail** |
