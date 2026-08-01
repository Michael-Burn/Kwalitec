# EA-002 — Publication Workflow

**Programme:** Educational Excellence Programme EA-002  
**Status:** Binding — educational publication and maintenance workflow  
**Effective:** 2026-08-01  
**Parent:** `EA002_EDUCATIONAL_AUTHORING_FRAMEWORK.md` · `EA002_CERTIFICATION_WORKFLOW.md` · `EA001_QUALITY_GATES.md`  
**Nature:** Process law — not curriculum content, not application code  

---

## 1. Purpose

Define how certified educational artefacts move from approval into student exposure — and how they stay true after publication.

**Governing distinction:**

| Gate family | Question answered |
|-------------|-------------------|
| Technical / lifecycle publish (e.g. Curriculum Studio, RF-002) | Is the package schema-valid and consistent? |
| **Educational publication (this document)** | May students rely on these artefacts as primary study guidance? |

Technical green is **necessary but not sufficient**. Educational publication requires Certification Workflow PASS and Publication Approval.

---

## 2. Publication principle

> **Nothing educational reaches students unless it is certified and publication-approved for a named subject package version.**

A single failed review or gate blocks publication. There is no “publish placeholders and fix voice later” path.

---

## 3. Preconditions to enter publication

Before Publication Approval may be requested:

1. Authoring pack complete under `EA002_EDUCATIONAL_AUTHORING_FRAMEWORK.md`  
2. Style Guide and Tutor Voice Guide self-check recorded  
3. Multi-stage review complete with all stages PASS (`EA002_CERTIFICATION_WORKFLOW.md`)  
4. Relevant EA-001 gates PASS (or HOLD only with documented waiver expiry and student-visible honesty where required)  
5. Joint composition rules satisfied (Mission ⇄ Session ⇄ Episodes ⇄ Reflection ⇄ Tomorrow)  
6. Universal preconditions U1–U7 PASS  
7. Cross-surface truth audit prepared for the sample set  

---

## 4. Publication units

| Unit | What publishes together |
|------|-------------------------|
| **Mission bundle** | Mission + linked Session arc + all Episodes + Reflection + Tomorrow Preview |
| **Revision bundle** | Revision plan/activity (+ Session/Episodes if revision is Session-shaped) |
| **Subject sample package** | Minimum certification package per EA-001 §9 / Certification Workflow |
| **Subject full package** | All student-reachable educational artefacts for the package version |

**Rule:** Do not publish an orphan Mission brief. Do not publish Episodes without a parent Session story. Do not publish Tomorrow Preview that disagrees with Mission handoff.

---

## 5. Publication workflow stages

```text
CERTIFICATION COMPLETE (all review stages PASS)
        ↓
PUBLICATION REQUEST
  - Subject / package version
  - Artefact inventory + gate evidence
  - Regression checklist vs EV-001 failure classes
        ↓
PUBLICATION APPROVAL (human)
  - Approver signs PASS for scoped version
  - Records reviewer IDs, dates, HOLD waivers if any
        ↓
RELEASE TO STUDENT SURFACE
  - Only artefacts in the approved inventory
  - Unapproved / HOLD items remain unavailable or honest-blocked
        ↓
POST-PUBLISH VERIFICATION
  - Spot-check live surfaces for One Educational Truth
  - Confirm no placeholder / contaminant leakage
        ↓
MAINTENANCE CYCLE (ongoing)
```

---

## 6. Publication Approval requirements

### 6.1 Approver

Human **Publication Approver** (Academic Board / Founder Educational Gate Owner or designate). Automation may assemble the pack; automation alone may not approve Version 1 educational publication.

### 6.2 Approval record (minimum)

| Field | Required |
|-------|----------|
| Subject ID + package version | Yes |
| Inventory of artefact IDs | Yes |
| Certification evidence reference | Yes |
| Gate results (MG/LE/SS/RV/TP as applicable) | Yes |
| EV-001 regression checklist outcome | Yes |
| Approver name + date | Yes |
| HOLD items + expiry + student-visible treatment | If any |
| Explicit statement: technical publish ≠ educational PASS acknowledged | Yes |

### 6.3 Approval outcomes

| Result | Meaning |
|--------|---------|
| **APPROVED** | Scoped inventory may reach students |
| **REJECTED** | Nothing in the request publishes; defects returned to Author |
| **PARTIAL HOLD** | Only explicitly listed PASS artefacts publish; HOLD items blocked with honesty |

PARTIAL HOLD must never silently omit tomorrow/revision in a way that creates dual truth.

---

## 7. Student exposure rules

1. **Unavailable beats unfit.** If a Mission’s Session fails certification, show honest unavailable / recovery — never a premium brief over an empty player.  
2. **No placeholder degrade.** Failed resolution at runtime must not insert “Today’s topic.” Prefer block + recovery.  
3. **Version pinning.** Students see artefacts from an approved package version; mixed uncertified drafts must not leak.  
4. **Mode honesty.** Revision-labelled work must appear as revision when not first-pass Current Learning Topic.  
5. **Truth alignment.** Home, History, Journey, Revision, and Decision Journal must project the same facts for the published day.

---

## 8. Relationship to technical publish

| Step | Owner | Educational constraint |
|------|-------|------------------------|
| Schema / package build | Engineering / Curriculum Studio | May proceed for staging |
| Lifecycle consistency (RF-002 class) | Release engineering | Necessary |
| Educational Certification | Academic reviewers | Mandatory before student reliance |
| Educational Publication Approval | Publication Approver | Mandatory before student reliance |
| Production traffic to students | Ops / release | Only after Approval |

Staging may hold certified and uncertified drafts for review. **Production student pathways** may only serve APPROVED inventory.

---

## 9. Maintenance workflow

Publication is not the end of educational duty. Maintenance keeps One Educational Truth and Tutor Voice intact as the world changes.

### 9.1 Maintenance triggers (mandatory review)

| Trigger | Action |
|---------|--------|
| CMP edition / locus change | Re-verify all dependent Guided Reading / Example loci; recertify affected Episodes |
| Syllabus / weight update | Re-verify Mission why-now, Revision priorities, Tomorrow chains |
| Contaminant discovery | Quarantine node; emergency unpublish pathway; recertify package |
| Twin / evidence model change affecting copy assumptions | Audit explainability and Revision empty states |
| Sitting date regime change | Refresh Exam Focus cues; Revision intensity language |
| EVF / dogfood FAIL on published artefact | Open defect; HOLD or unpublish until recertified |
| Author style drift complaints | Tutor Review sample audit against Voice + Style Guides |
| Package version bump | Full certification package floor applies |

### 9.2 Maintenance process

```text
TRIGGER
  ↓
IMPACT INVENTORY (which AF-MS/LE/SS/RV/TP/RF artefacts)
  ↓
AUTHOR PATCH (Framework + Style + Voice)
  ↓
DELTA REVIEW (stages as required by Certification Workflow change-class)
  ↓
RECERTIFY affected gates
  ↓
PUBLICATION APPROVAL for new package version or patch inventory
  ↓
RELEASE + post-publish verification
```

### 9.3 Change classes

| Class | Examples | Review depth |
|-------|----------|--------------|
| **Cosmetic** | Typo that does not change meaning | Educational Review abbreviated; Tutor spot-check |
| **Educational** | New prompt, objective, locus, success criterion | Full stages for affected artefacts |
| **Structural** | New Episode, stage count change, Mission–Session relink | Full Gate LE/SS/MG joint rules |
| **Truth-risk** | Progress language, Revision empty state, Tomorrow node | Full + cross-surface truth audit |

Cosmetic must not be used to smuggle educational changes.

### 9.4 Unpublish / HOLD after release

If a live artefact fails trust (contaminant, empty shell, dual truth):

1. Publication Approver (or Gate Owner) may **HOLD** or **unpublish** immediately.  
2. Student-visible honesty preferred over silent wrong guidance.  
3. Recertification required before restore.  
4. Record linked to EV-001 failure classes when applicable.

---

## 10. EV-001 regression checklist (publication pack)

Every Publication Request must confirm absence of:

| ID | Failure class |
|----|---------------|
| TB-001 | “Today’s topic” / placeholder collapse |
| TB-002 | Syllabus-paste Mission |
| TB-003 | Contaminant topics |
| TB-004 | Boilerplate explainability |
| TB-005 | Mastery/coverage theatre vs empty practice memory |
| TB-007 | Empty reading shells |
| TB-008 | Broken stage advance / incomplete N of M |

(Use full Trust Break Register for subject-specific audits.)

---

## 11. Roles in publication and maintenance

| Role | Duty |
|------|------|
| Educational Author | Supplies pack; patches maintenance |
| Quality Gate Owner | Confirms gate evidence still valid |
| Publication Approver | APPROVED / REJECTED / PARTIAL HOLD |
| Maintenance Owner | Watches triggers; schedules recertification |
| EVF / validators | May FAIL published experience; cannot alone APPROVE |

---

## 12. Closing rules

1. Technical publish ≠ educational publication.  
2. Joint bundles only.  
3. Maintenance is part of the lifecycle — not optional polish.  
4. Unpublish is a feature of trust, not a failure of process.  

**Students deserve only APPROVED guidance.** Everything else stays out of the pathway.
