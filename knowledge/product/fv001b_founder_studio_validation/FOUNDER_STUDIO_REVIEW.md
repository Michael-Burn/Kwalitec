# FV-001B — Founder Studio Review

**Programme:** FV-001B — Founder Studio Blind Validation  
**Date:** 2026-07-28  
**Reviewer persona:** Founder of Kwalitec — prepare official IFoA curricula, upload CMP + syllabus, verify extraction, publish  
**Scope:** Founder Studio / Curriculum Authority Console only  
**Out of scope:** Student experience, EI internals, Runtime Integration, Learning Platform implementation  
**Method:** Blind visible walkthrough. Observations ≠ assumptions.

---

## Journey completion

| Phase | Tasks | Outcome | Score /10 |
|---|---|---|---|
| 1 Login | Recognise Founder environment; know next action | **Partial** — Console + CURRICULUM AUTHORITY clear; Home is ops metrics | 5 |
| 2 Subject Catalogue | Open Subjects; Ready/Draft/Coming Soon; create CTA | **Partial** — Subjects findable; workflow strip good; status model weak | 5 |
| 3 Create Subject | Create new subject | **Pass** — code + title; success flash | 8 |
| 4 Upload documents | Official syllabus + CMP | **Partial** — why-required copy excellent; files swap slots | 4 |
| 5 Extraction review | Wait; review; correct | **Fail** — pipeline timings yes; 0 nodes; no correctable structure | 2 |
| 6 Publish | Publish verified curriculum | **Fail** — correctly blocked; journey cannot finish | 3 |
| 7 Verification | Catalogue shows Ready + version | **Fail** — CS1B stuck at Validation; Published 0 | 2 |

**Weighted completion (Pass=1, Partial=0.5, Fail=0):** **≈ 36%** (2.5 / 7)

---

## Phase narratives (evidence-only)

### Phase 1 — Login

After sign-in with provisioned credentials, the product opens **Console Home** (`/console/`) titled *Kwalitec Console*, sidebar labelled **CURRICULUM AUTHORITY**, items: Overview, Subjects, Curriculum Studio, Review Queue, Publishing, Versions, Quality, Students, Settings, Support.

**Positive:** Role chrome is explicit. Curriculum Studio is one click away.

**Confusing:** First viewport is *Operational pulse* — Platform Health **0%**, Product Check-ins, Support inbox — not “prepare CS1 / upload official documents.” Login marketing still speaks student language (*Know exactly what to study next*).

### Phase 2 — Subject Catalogue

**Subjects** (`/console/studio/subjects`) explains: *Students only see a subject as Ready after you publish a verified curriculum.* A **Curriculum workflow** strip lists: New Subject → Upload Official CMP → Upload Official Syllabus → Extraction → Review & Corrections → Publish Verified Curriculum → Available to Students (Ready).

**Positive:** Founder job story is stated in plain language.

**Gaps:** Empty state shows no Ready / Draft / Coming Soon legend. After CS1B exists, list shows `CS1B · 2026.1 · Content Sources` then later `· Validation` — stage crumbs, not catalogue confidence states. Review Queue / Publishing / Versions / Quality pages largely repeat the same strip + workspace link (thin hubs).

### Phase 3 — Create Subject

On Curriculum Studio / Subjects: **Create Subject** with Subject code * and Title. Hint: *Use a short syllabus code such as CS1.* Creating **CS1B** yields *We've created your subject successfully.* and activity `subject_created: Created subject CS1B`.

**Required fields:** Code is marked required; Title optional in UI. Validation messages for empty submit were not forced in this walk (form uses required attribute on code).

### Phase 4 — Upload Official Documents

Opening workspace (Open Workspace with CS1B) lands on `/console/studio/workspaces/ws-cs1b` with clear REQUIRED slots:

- **Official CMP** — *Curriculum Master Pack — the authoritative source for sections, topics, and learning objectives.*
- **Official Syllabus** — *Official syllabus PDF grounding authorised curriculum order.*

Upload progress: STATUS Ready, VERSION v1/v2, SIZE, timestamp. Pipeline shows Extracted/Parsed/Mapped timings in ms.

**Critical observation:** After selecting files in DOM order, **official_syllabus.pdf** appears under Official CMP and **official_cmp.pdf** under Official Syllabus. A Founder trusting filenames would believe documents are swapped.

### Phase 5 — Extraction Review

Pipeline reports Knowledge Graph Built / Ready for documents. Validation tab notes *Document has topics/concepts but no learning objectives* (Passed · 1 issues). Summary still shows **Preview · not_ready · 0 nodes** and **3 of 8 checklist items ready**.

Validate Curriculum flash: *We couldn't complete validation. Blocking findings prevent a safe student curriculum…* while NEXT STEP says *Validation looks ready — build a student-facing preview* and Curriculum Intelligence shows *0 validation errors*.

**Review Queue** hub does not present extracted topics/objectives for correction — only a link back to the workspace.

### Phase 6 — Publish

Approve flash: *Approval without a version and preview risks publishing the wrong package…*  
Publish flash: *Publication without approval and a version would expose incomplete material to students…*

Safety messaging is understandable and inspires appropriate caution. The Founder still cannot complete publication of a verified curriculum in this walkthrough.

### Phase 7 — Verification

Studio index: **Published 0**, **Drafts 1**, **Pending validation 1**. Subjects list: CS1B at Validation stage. No Ready badge. Re-using **Open Workspace** with CS1B errors: *We couldn't open a new workspace because one already exists… Open the existing workspace from the dashboard* — while the workspace link is labelled as a list row, not an obvious “dashboard.”

**Trust question:** Would I trust this subject for students? **No** — 0 nodes, not published, status not Ready.

---

## Critical issues

1. End-to-end publish → Ready path incomplete on visible evidence.  
2. Preview 0 nodes with “built successfully” contradiction.  
3. Validation messaging contradictions (failed vs ready vs 0 errors).  
4. CMP/Syllabus file slot swap.  
5. EI/engineering terminology on primary workspace chrome.

## Major issues

1. Console Home does not lead with curriculum next action.  
2. Open Workspace creates-or-fails instead of opening existing.  
3. Catalogue lacks Ready/Draft/Coming Soon clarity.  
4. Hub pages (Review, Publishing, Quality, Versions) add little beyond Studio.  
5. `UPLOADED BY 1` exposes internal user id.

## Minor improvements

1. Login page remains student-value oriented for a Curriculum Authority user.  
2. Activity feed uses snake_case event names (`sources_uploaded:`).  
3. Duplicate flash banners appear stacked.  
4. Title field on Create Subject not marked required while code is.

---

## Overall product score (Founder Studio only)

**38 / 100** — onboarding and document intent improved; publication trust not achieved.
