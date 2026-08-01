# EA-008 — Campaign Certification

**Programme:** Educational Excellence Programme EA-008 — Educational Campaign Architecture  
**Status:** Binding — measurable Campaign certification process  
**Effective:** 2026-08-01  
**Parent:** `EA008_EDUCATIONAL_CAMPAIGN_ARCHITECTURE.md`  
**Related:** Gate MG/SS/LE/TP/RV · `EA002_CERTIFICATION_WORKFLOW.md` · `EA001_QUALITY_GATES.md` · EA-007 continuity method  
**Nature:** Process law — not educational content, not application code  

---

## 1. Purpose

Define how an Educational Campaign moves from dossier to Board certification — and the measurable gates that reject journeys unfit for student reliance.

EA-001–EA-004 certify **days**.  
EA-005/EA-006 certify **packages**.  
**EA-008 Gate CG certifies journeys.**

> **A single failed Campaign stage blocks Campaign publication.**  
> Package PASSes inside a FAIL Campaign do not unlock commercial scale.

---

## 2. Certification principle

| Layer | Gate family | Question |
|-------|-------------|----------|
| Artefact | MG / LE / SS / RV / TP | Is this day tutor-grade? |
| Package | EA-002 multi-stage + Publication Approval | May this bundle reach students as a day? |
| **Campaign** | **Gate CG** | May students rely on this **sequence** for weeks? |

Technical schema validity and single-package APPROVED status are **necessary but not sufficient** for Campaign PASS.

---

## 3. Campaign lifecycle

```text
CAMPAIGN INPUTS
  → CAMPAIGN AUTHORING (dossier + package inventory)
    → PACKAGE CERTIFICATION (each member: EA-003/EA-004/EA-002)
      → CONTINUITY REVIEW (layers CL-01…CL-08)
        → TRUST REVIEW (Campaign-level trust + EA-007 pattern families)
          → GATE CG CERTIFICATION
            → CAMPAIGN PUBLICATION APPROVAL
              → MAINTENANCE
                → RETIREMENT / SUPERSESSION
```

| Stage | Owner | Output |
|-------|-------|--------|
| **Inputs** | Curriculum lead / Academic Board | Lawful syllabus span, scope class, CMP pin |
| **Authoring** | Educational author(s) | Complete Campaign dossier + ordered packages |
| **Package certification** | Per-package reviewers | Every inventory member PASS (or documented HOLD) |
| **Continuity Review** | Continuity Reviewer (≠ sole Author) | CL scores + reciprocal bridge audit |
| **Trust Review** | Academic Board / Trust reviewer | Pattern-family denial; Day-N trust simulation |
| **Gate CG** | Quality Gate Owner | Campaign PASS / FAIL / HOLD |
| **Publication** | Publication Approver | Student exposure for Campaign inventory |
| **Maintenance** | Author + Board | Recertify on package/CMP/syllabus/defect triggers |
| **Retirement** | Publication Approver | Campaign removed or superseded |

---

## 4. Preconditions (enter Gate CG)

Fail any → do not open Gate CG:

| ID | Precondition |
|----|--------------|
| CG-U01 | Campaign dossier complete (`EA008_EDUCATIONAL_CAMPAIGN_ARCHITECTURE.md` §12) |
| CG-U02 | Scope class declared (Pilot Arc / Chapter / First-pass Spine / Revision) |
| CG-U03 | Minimum arc length met (≥ 3 contiguous Learning packages for Pilot Arc+) |
| CG-U04 | Every Learning package in inventory individually certified PASS |
| CG-U05 | Universal preconditions U1–U7 hold on every member day |
| CG-U06 | No contaminant nodes on the Campaign map |
| CG-U07 | Revision Strategy present for scope class (Architecture §9) |
| CG-U08 | Continuity plan and dependency graph present |
| CG-U09 | EA-007 orphan-excellence pattern not present inside claimed neighbours |

---

## 5. Gate CG — Campaign

**Applies to:** Named Campaign versions before commercial student-pathway exposure of their inventory as a journey.

### 5.1 Certification dimensions (all required)

| ID | Dimension | PASS threshold | Evidence |
|----|-----------|----------------|----------|
| CG-01 | **Educational coherence** | Board judges Purpose + Objective + day sequence as one journey; no unrelated Mission bag | Dossier §Purpose/Objective; Mission uniqueness audit |
| CG-02 | **Concept progression** | Dependency graph exercised by bridges + Reading Guidance; no unsafe leaps | Dependency graph; hinge sample ≥ 1 per internal boundary |
| CG-03 | **Revision timing** | Revision Strategy placements meet scope-class minimum; return targets named | Revision map; Gate RV packs or HOLD record |
| CG-04 | **Tutor consistency** | One Sensei across packages; Tutor Intent unique per day; Style/Voice Guide held | Voice sample audit ≥ 3 days incl. first, middle, last |
| CG-05 | **Campaign-level trust** | No open recurring trust-break pattern family (EA-007 families); Day-*N* simulation PASS for scope | Trust Review minute; LTB denial table |
| CG-06 | **Campaign completion readiness** | CC-01…CC-07 design satisfied; objective assessable | Completion criteria checklist |
| CG-07 | **Publication approval readiness** | Inventory joint; no isolated Golden Day; Publication Policy preconditions met | Publication Request pack |

**Result rule:** FAIL any CG-01…CG-07 → Gate CG **FAIL**. HOLD only with expiry, student-visible treatment, and explicit non-claim of Campaign PASS.

### 5.2 Continuity Index (objective measure)

Score each continuity layer CL-01…CL-08 on 0–10 (Board protocol in Review Guide).

| Metric | Formula | Pilot Arc PASS | Chapter / Spine PASS |
|--------|---------|----------------|----------------------|
| **Continuity Index (CI)** | mean(CL-01…CL-08) | **CI ≥ 7.0** | **CI ≥ 7.5** |
| **Floor rule** | min(CL-02, CL-03, CL-04, CL-05, CL-07) | **≥ 6** | **≥ 7** |
| **Bridge integrity** | % internal boundaries with reciprocal skill-named bridges | **100%** | **100%** |
| **Package coverage** | certified Learning packages / Learning days in map | **100%** | **100%** |

**CI is mandatory evidence for CG-01 and CG-05.** A narrative “feels continuous” without CI scores is not certification.

### 5.3 Concept progression checklist (CG-02)

| ID | Criterion |
|----|-----------|
| CPX-01 | Every internal day names a concept hinge from prior day |
| CPX-02 | Hinges match the dependency graph |
| CPX-03 | Reading Guidance open/stop advances locus without random chapter jumps |
| CPX-04 | Knowledge Checks do not require untaught Campaign-future skills |
| CPX-05 | Heavy-weight topics receive pacing honest to syllabus weight |

### 5.4 Revision timing checklist (CG-03)

| ID | Criterion |
|----|-----------|
| RTX-01 | At least one Revision placement (Pilot Arc minimum) |
| RTX-02 | Return targets are earlier Campaign (or declared prerequisite Campaign) skills |
| RTX-03 | Spacing is justified relative to forgetting risk / syllabus weight |
| RTX-04 | No empty revision theatre |
| RTX-05 | Chapter / Spine Campaigns: revision density Board-approved for span length |

### 5.5 Tutor consistency checklist (CG-04)

| ID | Criterion |
|----|-----------|
| TVX-01 | Tutor Intent present and Mission-unique every Learning day |
| TVX-02 | No Voice spike on one day and collapse elsewhere (EA-007 Day-13 pattern) |
| TVX-03 | Style Guide / Tutor Voice Guide self-check recorded per package |
| TVX-04 | Sampled student-facing copy reads as one Sensei |
| TVX-05 | Reflection and Tomorrow voice match Mission voice |

### 5.6 Campaign-level trust checklist (CG-05)

Deny all four EA-007 pattern families:

| Family | Denied when |
|--------|-------------|
| Stamp pedagogy | Unique Mission/Session/Reflection/Tomorrow substance across days |
| Orphan excellence | No certified day isolated among claimed neighbours |
| Missing memory system | Revision Strategy present and student-visible in dossier |
| Truth residuals | EV-001 progress/confidence/contaminant classes absent on Campaign path |

**Day-*N* trust simulation (required):**

| Scope class | Simulation horizon *N* | PASS question |
|-------------|------------------------|---------------|
| Pilot Arc | End of arc (≥ Day 3) | Would the Board still endorse primary reliance for this arc? |
| Chapter | End of chapter | Same |
| First-pass Spine | Day 14 and Day 20 composite (EA-007 method) | Same — semester reliance |

Answer **No** → CG-05 FAIL.

### 5.7 Completion readiness checklist (CG-06)

Map Architecture CC-01…CC-07. Design-time PASS means the Campaign **makes completion assessable**; it does not require a live student to have finished.

### 5.8 Publication readiness checklist (CG-07)

Cross-walk `EA008_CAMPAIGN_PUBLICATION_POLICY.md` preconditions. Isolated package APPROVED without Campaign membership → CG-07 FAIL for commercial pathway claims.

---

## 6. Scoring record (minimum)

Every Gate CG attempt records:

| Field | Required |
|-------|----------|
| `campaign_id` + version | Yes |
| Scope class | Yes |
| Package inventory + per-package certification refs | Yes |
| CL-01…CL-08 scores + CI | Yes |
| Bridge integrity % | Yes |
| CG-01…CG-07 outcomes | Yes |
| Trust pattern-family denial table | Yes |
| Day-*N* simulation minute | Yes |
| Reviewer IDs + dates | Yes |
| Defects with principle / LTB IDs | If FAIL/HOLD |
| Explicit: Package PASS ≠ Campaign PASS acknowledged | Yes |

---

## 7. Outcomes

| Result | Meaning |
|--------|---------|
| **PASS** | Campaign may proceed to Campaign Publication Approval for scoped inventory |
| **FAIL** | Campaign must not be publication-claimed; defects listed; member package PASSes remain valid only as packages |
| **HOLD** | Temporary block (e.g. one Revision pack pending) with expiry; not a silent PASS |

**Partial Campaign PASS does not exist.** Either the journey certifies or it does not. PARTIAL HOLD at **publication** of packages is a separate Publication Policy instrument and cannot invent Campaign PASS.

---

## 8. Relationship to EA-002 Certification Workflow

Gate CG **nests after** per-artefact multi-stage certification:

```text
EA-002 stages for each package
        ↓
All packages PASS
        ↓
EA-008 Continuity Review + Trust Review
        ↓
Gate CG
        ↓
EA-008 Campaign Publication Approval
        ↓
(Student exposure of Campaign inventory)
```

Curriculum Review remains required for topic lawfulness of the span.

---

## 9. Recertification triggers

| Trigger | Action |
|---------|--------|
| Any member package educational change | Delta Continuity Review; possibly full Gate CG |
| Add/remove/reorder Campaign day | Full Gate CG |
| CMP edition change affecting multiple days | Full CG-02/CG-04 sample + affected packages |
| Contaminant discovery | Immediate Campaign HOLD / unpublish pathway |
| EA-007-class longitudinal FAIL on published Campaign | Unpublish scale claims; recertify |
| Scope class upgrade (Pilot → Chapter → Spine) | Full Gate CG at higher thresholds |
| Revision Strategy change | CG-03 + CG-05 re-audit |

---

## 10. Roles

| Role | Duty |
|------|------|
| Educational Author | Dossier + packages |
| Continuity Reviewer | CL scores, bridges, artificial-continuity denial |
| Trust Reviewer / Academic Board | Pattern families, Day-*N* simulation |
| Quality Gate Owner | Gate CG sign-off |
| Publication Approver | Campaign Publication Approval (separate document) |
| Package reviewers | Unchanged EA-003/EA-004 duties |

Automation may pre-fail missing bridges, duplicate Tutor Intents, or coverage gaps. Automation alone may **not** PASS Gate CG for Version 1 commercial pathways.

---

## 11. Explicit non-claims

- Gate CG PASS is not claimed for any live CS1 Campaign in EA-008 (architecture only).  
- EA-006 node 4.2 APPROVED ≠ Gate CG PASS.  
- EA-007 FAIL remains the standing continuity result until a successor certifies a contiguous arc under this process.

---

## 12. Closing rule

> **Certify the journey students will live in — not the day that photographs well.**

Signed notionally: Academic Board · EA-008 · Campaign Certification · 2026-08-01
