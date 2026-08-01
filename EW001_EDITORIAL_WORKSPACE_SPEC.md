# EW-001 — Editorial Authoring Workspace Specification

**Programme:** Editorial Production Infrastructure EW-001 — Editorial Authoring Workspace  
**Status:** Binding — editorial production workspace design  
**Effective:** 2026-08-01  
**Authority:** Educational Excellence Framework (Frozen) · Educational Operations (Frozen) · TV-001 PASS · EJ-001 PASS  
**Nature:** Authoring productivity design only — **no** redesign of Educational Excellence, Educational Operations, Runtime A/C, SCI, Student Digital Twin, or Recommendation Engine; **no** application implementation; **no** educational content; **no** framework redesign  

**Companion deliverables:** `EW001_AUTHOR_WORKFLOW.md` · `EW001_AUTHOR_CHECKLIST.md` · `EW001_IMPLEMENTATION_REPORT.md`

---

## 1. Purpose

Design a **single Editorial Authoring Workspace** that operationalises the frozen Educational Excellence Framework as an authoring journey — not as a library of governance documents authors must hunt.

The workspace does **not** invent new educational law.  
It **embeds** existing law so authors experience one coherent production path from Mission objective through Publication dossier.

> **Excellence is the operating system.**  
> **The Editorial Workspace is the application authors open.**  
> Authors should not need to open EA-001–EA-008, EO-001, EJ-001, or TV-001 as primary reading to produce a compliant Mission.

---

## 2. Design posture

Think like the Editorial Director of a global educational publisher building an authoring desk:

| Principle | Meaning for EW-001 |
|-----------|-------------------|
| **One journey** | Ten ordered stages; one workfile; one status bar |
| **Progressive disclosure** | Authors see the next required prompt, not the full gate catalogue |
| **Law behind the glass** | Frozen principles, gates, J1–J10, and trust criteria fire as stage rules — not as homework |
| **Craft preserved** | Tutor Voice, misconception design, and stop integrity remain human craft — the workspace sequences them; it does not automate pedagogy |
| **Throughput without theatre** | Reduce document-switching and memory load; never lower Gate MG / LE / SS / RV / TP or EJ hard rules |
| **Editorial artefacts stay editorial** | Justification and dossier remain internal; student surfaces stay Tutor Voice only |

### Explicit non-goals

| Out of scope | Why |
|--------------|-----|
| Redesign of EA / EO / TV / EJ law text | Freeze is superior |
| Application / UI implementation | This programme is design only |
| Live Mission / Session content | No educational content authoring |
| Runtime A / C, SCI, Twin, recommendations | Untouched product systems |
| New certification gates | Workspace orchestrates existing gates; does not invent replacements |

---

## 3. Position in the authority stack

| Rank | Authority | EW-001 relationship |
|-----:|-----------|---------------------|
| 1 | Vision 2030 | Superior |
| 2 | Product Blueprint / experience guidelines | Superior |
| 3 | Educational Constitution | Superior |
| 3a | EA-001–EA-008 Educational Excellence (Frozen) | **Operating system** — substance, gates, schemas, certification |
| 3b | EO-001 Educational Operations (Frozen) | **Publishing spine** — Stage 0–9 orchestration; Volume Dossier |
| 3c | TV-001 Educational Trust (PASS) | Consumed — T1–T7 corroboration targets for authored judgement |
| 3d | EJ-001 Educational Justification (PASS) | Consumed — mandatory J1–J10 dossier inside Stage 4 |
| **3e** | **EW-001 Editorial Authoring Workspace (this family)** | Binding **productivity shell** under frozen OS — does not amend OS law |

If workspace practice would contradict frozen Excellence, Operations, EJ, or higher law, **stop**. Amend the superior document first — do not weaken quality via “authoring convenience.”

---

## 4. What the Editorial Workspace is

### 4.1 Definition

The **Editorial Authoring Workspace** is the single production journey (process + workfile + stage prompts) through which an Educational Author creates a publishable Mission bundle:

**Mission + linked Session arc + Episodes (knowledge checks) + Reflection + Tomorrow bridge + Educational Justification + Certification evidence + Publication dossier entries.**

### 4.2 Metaphor

| Layer | Analogy | Kwalitec reality |
|-------|---------|------------------|
| OS | Kernel + drivers | Frozen EA/EO law, Gate MG/LE/SS/RV/TP, EJ hard rule |
| Workspace | Authoring application | Ten-stage journey (this programme) |
| Workfile | Manuscript + dossier | Volume Dossier slot + Mission pack + Justification pack |
| Student book | Published volume | Student-facing Tutor Voice artefacts only |

Authors work in the Workspace. Reviewers and Approvers still apply frozen certification and EO stages. The Workspace prepares artefacts so those later stages are evidence-complete, not surprise audits against unread PDFs.

### 4.3 Audiences

| Audience | Workspace experience |
|----------|----------------------|
| **Educational Author** | Primary user — guided stages, checklist, progressive prompts |
| **Educational / Tutor Reviewer** | Receives complete pack; may open workspace in review mode |
| **Quality Gate / Publication Approver** | Consumes Certification evidence + Publication dossier; does not re-teach framework |
| **Founder / Trust Validation** | May cite Justification + lived T1–T7; workspace is not a validation walk |
| **New Subject Lead / new author** | Onboard via Workspace + Checklist — not via reading every EA/EO file first |

Students are **not** an audience for the Workspace.

---

## 5. Cognitive load model

### 5.1 Problem EW-001 solves

Today a diligent new author must mentally assemble:

- EA-001 principles + Mission / Session philosophies + Quality Gates  
- EA-002 Authoring / Style / Voice / Certification / Publication  
- EA-003 Mission schema + authoring order  
- EA-004 Session / Episode / Reflection / Tomorrow law  
- EJ-001 J1–J10 + Template  
- EO-001 Authoring → Approval dossier obligations  
- TV-001 T1–T7 as expert-defence targets  

That is **many disconnected governance documents**. Quality stays high only for authors who already internalised the house. Throughput and onboarding suffer.

### 5.2 Load-reduction strategy (without lowering the bar)

| Mechanism | Effect |
|-----------|--------|
| **Ordered stages S1–S10** | One job per stage; next stage unlocked when exit criteria met |
| **Stage prompts replace document lookup** | Each prompt maps to frozen law IDs behind the glass |
| **Single Author Checklist** | Day-to-day instrument; frameworks remain reference law |
| **Justification nested in Stage 4** | EJ-001 becomes a workspace step, not a separate programme hunt |
| **Certification evidence assembled as you go** | Stage 9 collates; authors do not reconstruct from memory |
| **Publication dossier fields pre-wired** | Stage 10 maps to EO Volume Dossier — no second inventory invent |
| **Silent enforcement** | Missing CMP locus / empty J field / orphan Mission blocks advance |

### 5.3 What must remain hard (craftsmanship)

The Workspace **must not**:

- auto-generate Tutor Voice that passes Gate MG without human craft,
- invent CMP loci,
- fill J1–J10 with boilerplate templates that pass EJ-R checks,
- skip joint publication (Mission alone),
- or mark Certification PASS without human review stages.

Productivity means **less hunting**; not **less teaching judgement**.

---

## 6. Workspace architecture

### 6.1 Workfile structure

Every Mission production run maintains one **Editorial Workfile**:

```text
Editorial Workfile
├── Identity (subject, package version, mission_id, mode, author of record)
├── Stage status (S1…S10: locked | active | complete | blocked)
├── Student-facing pack (Mission / Session / Episodes / Reflection / Tomorrow)
├── Editorial pack (Educational Justification J1–J10 + expert-defence)
├── Evidence pack (self-checks, review stubs, gate IDs, defect log)
└── Publication dossier pointers (Volume membership, inventory, Approver-ready fields)
```

The Workfile is the author’s single source of production truth until Publication Approval locks versions under EO-001.

### 6.2 Stage map (canonical order)

| Stage | Collects | Student vs editorial | Primary frozen law (behind the glass) |
|------:|----------|----------------------|---------------------------------------|
| **S1** | Mission objective | Student-facing seed + Tutor Intent | EA-001 M2/M5/M6; EA-003 Steps 1–2 |
| **S2** | Syllabus objectives | Identity inputs | Constitution VI; EA-001 M1; EA-003 Inputs |
| **S3** | CMP references | Material locus | EP-01/EP-04; EA-001 M8; EA-003 Step 4 |
| **S4** | Educational Justification (J1–J10) | **Editorial only** | EJ-001 Standard + Template |
| **S5** | Tutor Voice mission | Student-facing Mission prose | EA-002 Voice/Style; EA-003 Steps 8–10; Gate MG |
| **S6** | Knowledge checks | Episode active demands | EA-004; Gate LE; SS-03 |
| **S7** | Reflection | Session close | EP-07; SS-04; AF-RF |
| **S8** | Tomorrow bridge | Continuity | EA-001 M10; Gate TP; AF-TP |
| **S9** | Certification evidence | Editorial evidence | EA-002 Certification; Gate MG/LE/SS/TP |
| **S10** | Publication dossier | EO operational dossier | EO-001; EA-002 Publication; EJ locked |

Stages **S1 → S10** are the author-facing order. Internal EA-003 / EJ recommended micro-orders may run *inside* a stage; authors need not know those micro-orders as separate programmes.

### 6.3 Unlock rules

| Rule | Behaviour |
|------|-----------|
| **Sequential default** | S(*n*+1) becomes `active` only when S(*n*) is `complete` |
| **Soft preview** | Authors may *preview* later stage prompts read-only; may not mark later stages complete early |
| **Hard blocks** | Missing topic identity (S2), missing CMP open/stop (S3), incomplete J1–J10 (S4), orphan Mission without Session/Episodes (S5–S6), empty Reflection path (S7), contradictory Tomorrow (S8) |
| **Rework loop** | Review FAIL returns author to the earliest failing stage; Justification status reverts from `complete` if Mission educational decisions change |

### 6.4 Modes

| Mode | Who | Capability |
|------|-----|------------|
| **Author** | Educational Author of Record | Edit stages; submit for review |
| **Review** | Educational / Tutor / Curriculum reviewers | Annotate; PASS/FAIL/HOLD stages; cannot rewrite Justification to invent defence |
| **Approver read** | Publication Approver | Read-only inventory + evidence; sign outside workspace under EO-001 |
| **Audit** | Founder / Trust Validation | Read Justification + evidence; run T1–T7 elsewhere |

---

## 7. Stage specifications (summary)

Detailed author prompts live in `EW001_AUTHOR_WORKFLOW.md`.  
Day-to-day ticks live in `EW001_AUTHOR_CHECKLIST.md`.  
This section defines **workspace contracts** only.

### S1 — Mission objective

**Job:** Establish the one skill/move of the day and Tutor Intent before syllabus paste.  
**Exit:** Distinct learning objective + concept focus + success criterion draft + private Tutor Intent.  
**Silent OS checks:** Objective ≠ syllabus heading string; assessable verb present.

### S2 — Syllabus objectives

**Job:** Bind lawful topic identity and syllabus learning outcomes the Mission serves.  
**Exit:** Official topic code + title; syllabus LO pointers; mode (Learning/Revision); prior/cold-start context.  
**Silent OS checks:** No placeholders; contaminant strings blocked; Learning Mode order honesty.

### S3 — CMP references

**Job:** Pin authorised reading craft — open, aim, stop, out-of-scope.  
**Exit:** CMP edition + TOC locus + stop condition + out-of-scope note.  
**Silent OS checks:** Guidance-Over-Content; no second-textbook invention; no raw CMP dump as Mission body.

### S4 — Educational Justification (J1–J10)

**Job:** Defend the Mission as authored for institutional audit.  
**Exit:** EJ Template status `complete`; expert-defence paragraph; EJ-R self-check recorded.  
**Silent OS checks:** All J1–J10 Mission-unique; no student-facing paste of Justification; contradiction check vs pack (EJ-R13).

### S5 — Tutor Voice mission

**Job:** Write the student-facing Mission brief in Study Sensei voice.  
**Exit:** Full AF-MS / EA-003 Mission fields; Style + Voice self-check; P1–P12 denied.  
**Silent OS checks:** IFoA-tutor brief test ready; explainability unique; linked Session intent present.

### S6 — Knowledge checks

**Job:** Author Episode-level active cognitive demands that force misconceptions into the open.  
**Exit:** Linked Episode set with ≥1 active demand; success criteria align with Mission; Gate LE self-check.  
**Silent OS checks:** Session intent matches Episode count; no advertised stages without authored substance.

### S7 — Reflection

**Job:** Design topic-specific Reflection that harvests residual uncertainty.  
**Exit:** Reflection prompts + student-authored path; `reflection_goal` aligned to concept/misconceptions.  
**Silent OS checks:** Not generic wellness copy; SS-04 ready.

### S8 — Tomorrow bridge

**Job:** Hand off continuity honestly.  
**Exit:** `tomorrow_bridge` known or honest empty; continuity line agrees with Summary/Home handoff.  
**Silent OS checks:** Gate TP self-check; no heavy new teaching after Reflection.

### S9 — Certification evidence

**Job:** Assemble the evidence pack reviewers need — without reopening every framework doc.  
**Exit:** Gate MG/LE/SS/TP self-evidence; Style/Voice check refs; Justification attached; defect log empty or resolved; ready for EA-002 stages ①–④.  
**Silent OS checks:** Joint composition complete; U1–U7 self-denied where applicable.

### S10 — Publication dossier

**Job:** Hand the Volume/ops spine a complete dossier slot for EO-001 Publication Approval.  
**Exit:** Inventory IDs; package version; Justification status ready to lock; Approver-facing evidence URIs; FP anti-mirage denials.  
**Silent OS checks:** Author does not self-approve; no student-pathway release from Authoring.

---

## 8. Mapping: Workspace → frozen programmes

| Workspace element | Consumes (does not amend) |
|-------------------|---------------------------|
| S1–S3, S5–S8 student pack | EA-001, EA-003, EA-004, EA-002 Style/Voice |
| S4 Justification | EJ-001 Standard, Template, Authoring Guidelines |
| S6 knowledge checks | EA-004 Episode/Session law; Gate LE; SS-03 |
| S9 evidence | EA-002 Certification Workflow; EA-001 Quality Gates |
| S10 dossier | EO-001 Publishing Workflow + Volume Standard; EA-002 Publication |
| Expert-defence / trust posture | TV-001 T1–T7 as corroboration targets |
| Joint publication | EA-002 Publication units; EA-008 when Campaign-scoped |

---

## 9. Relationship to EO-001 stages

EW-001 lives primarily inside **EO-001 Stage 1 — Authoring**, and prepares artefacts for Stages 2–5.

```text
EO-001 Stage 0 COMMISSION
      ↓
EO-001 Stage 1 AUTHORING  ←── EW-001 Workspace (S1–S10) runs here
      ↓
EO-001 Stage 2 PEER REVIEW      ←── consumes Workspace evidence pack
      ↓
EO-001 Stage 3 EDUCATIONAL AUDIT
      ↓
EO-001 Stage 4 FOUNDER REVIEW
      ↓
EO-001 Stage 5 PUBLICATION APPROVAL
```

EW-001 does **not** replace Peer Review, Audit, Founder Review, or Approver. It makes Authoring exit criteria (AU-01…AU-06 spirit) naturally satisfied by completing S1–S10.

---

## 10. Invisibility contract

### 10.1 What authors see

1. Ten stage titles in plain production language (Mission objective → Publication dossier).  
2. Short prompts and fields.  
3. One checklist.  
4. Block messages in plain language (“Name where the candidate opens the CMP”) — optionally with law IDs in a “Why this matters” drawer.

### 10.2 What authors should not need as primary reading

- Full EA-001–EA-008 suite before first draft  
- Full EO-001 lifecycle text before first draft  
- TV-001 philosophy before first draft  
- Scattered programme implementation reports  

### 10.3 What remains available as reference

Frozen law documents remain binding reference. The Workspace cites them; it does not delete them. Advanced reviewers and Approvers still use gate IDs and EJ-R codes.

---

## 11. Success properties (design acceptance)

| Property | Design requirement |
|----------|-------------------|
| Quality unchanged | Every Gate MG/LE/SS/TP and EJ hard rule still required at exit |
| Cognitive load reduced | One journey + checklist replaces multi-document assembly for day-to-day authoring |
| New-author compliance | A new author can complete S1–S10 using Workflow + Checklist without consulting numerous framework docs as primary guides |
| Craftsmanship preserved | Tutor Intent, misconception hunt, CMP stop, and Justification remain human judgements |
| OS frozen | No amendment to Excellence / Operations / Runtime / Twin / SCI / recommendations |

---

## 12. Future implementation note (out of scope for EW-001)

A later engineering programme may implement this Workspace as software (forms, validation, dossier UI). **EW-001 does not implement that.** Any future build must treat this specification as the product brief and must not invent new educational gates.

---

## 13. Closing law

> **Authors walk one production journey.**  
> **The Educational Excellence Framework runs underneath — almost invisible, never optional.**  
> **Nothing educational is published because the workspace felt easy; it is published because the journey made every required educational decision explicit, justified, and certifiable.**
