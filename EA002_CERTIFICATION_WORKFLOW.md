# EA-002 — Certification Workflow

**Programme:** Educational Excellence Programme EA-002  
**Status:** Binding — multi-stage educational certification before publication  
**Effective:** 2026-08-01  
**Parent:** `EA002_EDUCATIONAL_AUTHORING_FRAMEWORK.md` · `EA001_QUALITY_GATES.md` · EA-001 Principles  
**Consumers:** Educational Authors · Reviewers · Publication Approvers · EVF · successor rewrite programmes  
**Nature:** Process law — not content generation, not application code  

---

## 1. Purpose

Define the mandatory multi-stage review that every educational artefact must pass before Publication Approval.

EA-001 defines **what** PASS means (gates MG / LE / SS / RV / TP).  
EA-002 Certification defines **how** human review reaches that PASS — in order, with independence, and with evidence.

> **A single failed gate or review stage blocks publication.**

---

## 2. Certification pipeline

```text
AUTHORING COMPLETE
        ↓
① EDUCATIONAL REVIEW
        ↓
② TUTOR REVIEW
        ↓
③ CURRICULUM REVIEW
        ↓
④ QUALITY GATE REVIEW
        ↓
⑤ PUBLICATION APPROVAL   ← see EA002_PUBLICATION_WORKFLOW.md
```

Stages are **sequential**. Later stages must not begin on artefacts that failed earlier stages (except documented rework loops that restart at the failed stage).

HOLD is not PASS. HOLD blocks publication of the held artefact unless Publication Workflow PARTIAL HOLD rules apply with student-visible honesty.

---

## 3. Stage ① — Educational Review

### 3.1 Job

Judge educational substance against EA-001 principles EP-01–EP-10 and the artefact class standard in the Authoring Framework.

### 3.2 Reviewer

Educational Reviewer (Academic Board designate). Should not be the sole Author for Version 1 commercial certification packs.

### 3.3 Checklist (all required)

| ID | Criterion |
|----|-----------|
| ER-01 | Purpose of artefact class is clear and correct (Mission ≠ Session ≠ Episode, etc.) |
| ER-02 | Required inputs declared and used (syllabus node, CMP locus, prior/next as applicable) |
| ER-03 | Required outputs present for the class (AF-MS/LE/SS/RV/TP/RF) |
| ER-04 | Mandatory educational elements present |
| ER-05 | Educational reasoning sound (leverage, deliberate study, exam focus) |
| ER-06 | Prohibited shortcuts absent (universal + class-specific) |
| ER-07 | Style Guide structural patterns followed |
| ER-08 | Active cognitive demand present where required (Episodes / Sessions) |
| ER-09 | Reflection topic-specific and student-authored path exists (Session) |
| ER-10 | Completion language does not claim mastery |

### 3.4 Outcomes

| Result | Next |
|--------|------|
| PASS | Advance to Tutor Review |
| FAIL | Return to Author with principle IDs and defect notes |
| HOLD | Block; resolve missing educational evidence (e.g. locus TBD) with expiry |

---

## 4. Stage ② — Tutor Review

### 4.1 Job

Judge Tutor Voice, continuity feel, and the IFoA-tutor brief test using `EA002_TUTOR_VOICE_GUIDE.md`.

### 4.2 Reviewer

Tutor Reviewer (experienced educator or Founder Educational Gate Owner). Human mandatory for Version 1 PASS on voice and continuity.

### 4.3 Checklist (all required)

| ID | Criterion |
|----|-----------|
| TR-01 | Tone calm, specific, exam-serious |
| TR-02 | Language prefers assessable verbs; bans placeholders and platform meta |
| TR-03 | Transitions cite concrete educational referents |
| TR-04 | Questions are hunt / retrieve / justify / diagnose — not vague |
| TR-05 | Guided Reading prompts name locus, hunt, action, stop, return |
| TR-06 | Reflection prompts are topic-bound triad |
| TR-07 | Tomorrow bridge educational (or honest empty) |
| TR-08 | Explainability unique and specific (not TB-004 stamp) |
| TR-09 | Voice anti-patterns TV-A1–TV-A12 absent |
| TR-10 | IFoA-tutor brief test: would send to a candidate tonight |

### 4.4 Outcomes

PASS → Curriculum Review · FAIL → Author (+ optional Educational Review if substance drifted) · HOLD → rare; usually FAIL for voice.

**Automation may pre-fail** placeholders and boilerplate similarity; **automation may not PASS** Tutor Review alone in Version 1.

---

## 5. Stage ③ — Curriculum Review

### 5.1 Job

Judge syllabus lawfulness, CMP locus accuracy, contaminant quarantine, and V1/V2 curriculum integrity of referenced nodes.

### 5.2 Reviewer

Curriculum Reviewer (curriculum owner / Academic Board designate).

### 5.3 Checklist (all required)

| ID | Criterion |
|----|-----------|
| CR-01 | Topic identity resolves to lawful syllabus node (U1) |
| CR-02 | Objective/outcomes language compatible with official LOs without heading-only paste |
| CR-03 | CMP locus exists in authorised materials for this package edition |
| CR-04 | No address / publisher metadata / boilerplate contaminants (TB-003) |
| CR-05 | Tomorrow / handoff nodes lawful when present |
| CR-06 | Revision targets previously studied or evidence-warranted nodes |
| CR-07 | No silent invention of parallel topic trees |
| CR-08 | Package version and CMP edition recorded |
| CR-09 | Learning Mode order assumptions respect Constitution Article VI where claimed |
| CR-10 | Joint links (Mission topic = Session topic = Episode parent) hold |

### 5.4 Outcomes

PASS → Quality Gate Review · FAIL → Author / curriculum package fix · HOLD → e.g. CMP locus pending Founder waiver with expiry.

---

## 6. Stage ④ — Quality Gate Review

### 6.1 Job

Execute EA-001 gates formally and record PASS / FAIL / HOLD with evidence.

### 6.2 Reviewer

Quality Gate Owner (may combine with prior reviewers only if independence rules for commercial packs are met; preferred second signature).

### 6.3 Gate mapping

| Artefacts in pack | Gates required |
|-------------------|----------------|
| Mission | MG (+ joint Session rule) |
| Each Learning Episode | LE |
| Full Session arc | SS (implies LE set + MG joint) |
| Revision | RV |
| Tomorrow Preview | TP |
| Reflection | Covered under SS-04 / EP-07 inside SS |
| All | Universal U1–U7 |

Checklists: `EA001_QUALITY_GATES.md` §§3–8 verbatim — do not weaken.

### 6.4 Joint rules (reaffirmed)

- Mission PASS requires linked Session/Episodes PASS **or** Mission shown unavailable.  
- Session PASS requires all constituent Episodes LE PASS and parent Mission MG PASS (or Session not offered).  
- Advertised N of M stages must all exist and advance.

### 6.5 Outcomes

| Result | Meaning |
|--------|---------|
| PASS | Eligible for Publication Approval request |
| FAIL | Block publication; list failing gate IDs |
| HOLD | Block until evidence; not a silent PASS |

---

## 7. Stage ⑤ — Publication Approval

Defined in `EA002_PUBLICATION_WORKFLOW.md`.

Certification Workflow ends when Quality Gate Review PASS is recorded and the Publication Request pack is assembled. **Student exposure** begins only after Publication Approval APPROVED.

---

## 8. Certification evidence package

### 8.1 Per-artefact minimum

| Evidence item | Required |
|---------------|----------|
| Artefact ID + class | Yes |
| Subject / package version | Yes |
| Author + draft date | Yes |
| Educational Review result + reviewer + date | Yes |
| Tutor Review result + reviewer + date | Yes |
| Curriculum Review result + reviewer + date | Yes |
| Quality Gate checklist outcomes | Yes |
| Principle IDs cited | Yes |
| Defect/rework log | If any FAIL cycles |

### 8.2 Subject-version floor (from EA-001 §9)

For a subject version to expose Missions/Sessions to students:

1. Curriculum package free of contaminant topics (U1)  
2. Sample Mission set (≥5 across journey positions) Gate MG PASS  
3. Sample Session set covering those Missions Gate SS PASS  
4. At least one Revision path Gate RV PASS **or** documented HOLD with student-visible honesty  
5. Tomorrow Preview spots Gate TP PASS on those samples  
6. Cross-surface truth audit (Home ↔ History ↔ Journal ↔ Revision) with no dual-truth defects  
7. Written sign-off referencing EV-001 failure classes as regression checks  

Spot-check sizes may increase for commercial cohorts; they must not decrease below this floor without Board amendment of EA-001.

### 8.3 Cross-surface truth audit

Confirm for sample students/scenarios:

- Home Mission identity matches Session Overview topic  
- Decision Journal why-now agrees with Mission explainability  
- Completion claims agree with History sittings (or disclosed waiver)  
- Revision empty states explainable when coverage implies revisable material  
- Tomorrow Preview agrees with Mission handoff and next assignment  

Fail any → Quality Gate / Publication block (EP-10).

---

## 9. Rework loop

```text
FAIL at stage N
  → defects logged with IDs (ER/TR/CR/MG/LE/…)
  → Author patches under Framework + Style + Voice
  → Restart at stage N (or earlier if patch changes substance/curriculum)
  → Do not skip stages
```

**Rule:** A Tutor-only wording fix may restart at Tutor Review if Educational and Curriculum reviewers confirm no substance/locus change. Structural or locus changes restart at Educational Review (and Curriculum Review as needed).

---

## 10. Independence and Version 1 rules

1. Human PASS required for Tutor Voice, continuity, and exam-focus judgement.  
2. Automation assist may **pre-fail** (placeholders, title==objective, contaminant lint, empty episode body, boilerplate similarity) — see EA-001 §10.  
3. Automation alone may **not** issue educational PASS for Version 1 student exposure.  
4. For commercial cohort packages, prefer Author ≠ final Quality Gate Owner ≠ Publication Approver where staffing allows; at minimum, two human signatures on the certification pack.  
5. Generative AI may draft or polish only behind ports that cannot invent syllabus order, mastery, or rankings; output still faces full human pipeline.

---

## 11. Relationship to other authorities

| Authority | Relationship |
|-----------|--------------|
| Educational Constitution | Superior — mastery/evidence/mode lawfulness |
| EA-001 Quality Gates | Gate criteria this workflow executes |
| EVF / EV-001 | May FAIL live trust; consumes certification evidence |
| RF-002 / technical publish | Necessary ≠ sufficient |
| Publication Workflow | Downstream exposure and maintenance |

---

## 12. Closing

Certification is how Kwalitec refuses to repeat EV-001.

**Educational Review → Tutor Review → Curriculum Review → Quality Gate Review → Publication Approval.**

Miss a stage, weaken a gate, or skip human voice sign-off — and the artefact does not reach the student.
