# Stage-by-Stage Evidence

**Programme:** EV-001  
**Screenshots:** `_evidence/screenshots/`  
**Raw walk:** `_evidence/lifecycle.json`  
**Engineering probe:** `_evidence/engineering_analysis.json`

Official documents used (realistic Founder PDFs generated for verification content; uploaded via UI slots):

- Official CMP — `_evidence` companion `/tmp/ev001_capture/official_cmp.pdf` (1844 bytes)
- Official Syllabus — `/tmp/ev001_capture/official_syllabus.pdf` (1731 bytes)

---

## Stage 1 — Subject Creation

**Screenshots:** `02_s1_studio_before_create.png` … `05_s1_workspace_opened.png`

| Check | Evidence |
|---|---|
| Subject created | CS1V created via Curriculum Studio Create Subject |
| Initial lifecycle = Draft | Workspace opened at `/console/studio/workspaces/ws-cs1v`; Stage Subject |
| Subject identifier | `CS1V` / workspace `ws-cs1v` / Foundation subject id `1` |
| Creation timestamp | `2026-07-28 22:34:48.468006` (Foundation subject.created_at) |

---

## Stage 2 — Document Upload

**Screenshots:** `06_s2_cmp_selected.png` … `08_s2_process_0.png`

| Check | Evidence |
|---|---|
| Correct slot assignment | Bound via `#doc-file-cmp` and `#doc-file-syllabus` |
| Upload complete | Active docs: cmp `official_cmp.pdf`, syllabus `official_syllabus.pdf` |
| Documents Ready | UI Ready cues; processing_stage `ready_for_embeddings` for both |

Document metadata (DB):

| id | kind | filename | stage |
|---|---|---|---|
| 1 | cmp | official_cmp.pdf | ready_for_embeddings |
| 2 | syllabus | official_syllabus.pdf | ready_for_embeddings |

---

## Stage 3 — Structure Preparation

**Screenshots:** `09_s3_after_advance.png` … `12_s3_panel_documents.png`

| Check | Evidence |
|---|---|
| Curriculum extracted | CIP entities created for both documents |
| Structure prepared | StructurePreparation / CIP projection available to validate/preview |
| Topics generated | 21 topics/subtopics (CIP); package topic_count=21 |
| Objectives present | 5 learning_objective entities; package objective_count=5 |

Structure summary: subject CS1V chapters/probability/distributions/inference/regression + syllabus subtopics; objectives include Bayes, distributions, confidence intervals, regression coefficients.

---

## Stage 4 — Validation

**Screenshots:** `13_s4_validate.png` … `15_s4_validation_panel.png`

| Check | Evidence |
|---|---|
| Validation succeeds | Body: “We've completed validation successfully.” |
| Findings displayed | Validation findings panel present; no blocking findings |
| Readiness = Validated | `Validation completed successfully · passed` |
| Blocking issues | **0** |
| Warnings | **0** (none shown) |

---

## Stage 5 — Preview

**Screenshots:** `16_s5_preview.png` … `19_s5_panel_topic_details.png`

| Check | Evidence |
|---|---|
| Preview generated | “We've built the preview successfully — 23 curriculum topics ready to review.” |
| Preview Ready | `Preview ready · ready_for_review · 23 topics` |
| Hierarchy matches prepared structure | Structure/Topic panels show extracted CMP/syllabus nodes |

Node count: **23** (UI); package topic_count **21** plus subject/title nodes in hierarchy.

---

## Stage 6 — Approval

**Screenshots:** `20_s6_approve.png`, `21_s6_approve_reload.png`

| Check | Evidence |
|---|---|
| Approval succeeds | “We've approved your curriculum successfully.” |
| Confirmation shown | Success message + checklist 6 of 8 |
| preview_approved created | Preview line: `Preview ready · approved · 23 topics` |
| Approval timestamp | Walk capture `2026-07-28T22:35:18.677236+00:00` |

---

## Stage 7 — Publication

**Screenshots:** `22_s7_publish.png` … `25_s7_publish_state_2.png`

| Check | Evidence |
|---|---|
| Publication succeeds | “We've published your verified curriculum successfully.” |
| Rollback snapshot | Publish path requires checklist including rollback (Studio publish succeeded; version retained) |
| Current version assigned | Status: `Published · Version 2026.1` |
| Publication record | `published_curriculum_packages` id=1, subject=CS1V, version_label=2026.1, is_active=1 |
| Publication timestamp | `2026-07-28 22:35:19.805952` |

---

## Stage 8 — Ready

**Screenshots:** `26_s8_studio_subjects.png`

| Check | Evidence |
|---|---|
| Lifecycle = Ready | Subjects hub: `CS1V Ready · Current Version 2026.1 · Published 2026-07-28` |
| Current Version visible | `2026.1` |
| Published Date visible | `2026-07-28` |

---

## Stage 9 — Student Discovery

**Screenshots:** `28_s9_student_catalogue_wizard.png` … `30_s9_student_home.png`

| Check | Evidence |
|---|---|
| Subject appears in catalogue UI | **No** — `/study-plan/wizard/1` Internal Server Error |
| Ready status displayed | **No** (page failed before catalogue render) |
| Student can enrol | **Not verified** (discoverability blocked by 500) |
| Data-layer Ready package | **Yes** — active package CS1V / 2026.1 |

Root cause (engineering):

```text
AttributeError: 'str' object has no attribute 'strftime'
File app/application/platform_integration/subject_catalogue.py
  _format_release → value.strftime(...)
called from SubjectCatalogueService._from_published
```

Did not begin studying (per brief).

---

## Screenshot index

| File | Stage |
|---|---|
| `00_s0_login.png` … `01_s0_after_login.png` | Auth |
| `02`–`05` | Stage 1 |
| `06`–`08` | Stage 2 |
| `09`–`12` | Stage 3 |
| `13`–`15` | Stage 4 |
| `16`–`19` | Stage 5 |
| `20`–`21` | Stage 6 |
| `22`–`25` | Stage 7 |
| `26`–`27` | Stage 8 |
| `28`–`30` | Stage 9 |
| `31`–`35` | Regression UI probes |
