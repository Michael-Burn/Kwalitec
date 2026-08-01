# EO-001 — Publishing Workflow

**Programme:** Educational Operations Programme EO-001 — Educational Publishing Operations  
**Status:** Binding — Educational Publishing Lifecycle  
**Effective:** 2026-08-01  
**Authority:** EA-001 through EA-008 COMPLETE · EP-001 PASS  
**Nature:** Publishing operations law — not educational architecture redesign, not application code, not Runtime/SCI work, not educational content authoring  
**Parents:** `EO001_EDUCATIONAL_VOLUME_STANDARD.md` · `EA002_PUBLICATION_WORKFLOW.md` · `EA002_CERTIFICATION_WORKFLOW.md` · `EA008_CAMPAIGN_PUBLICATION_POLICY.md` · `EP001_PUBLICATION_READINESS.md`  
**Reference quality bar:** Campaign Alpha (`CS1-EP001-CAMPAIGN-ALPHA` · `ep001-1.0.0`)  

---

## 1. Purpose

Define a **complete, repeatable Educational Publishing Lifecycle** so every future Educational Volume is produced to the same standard as Campaign Alpha — deterministically, not by institutional memory.

### Design posture

Think like the Editorial Director of a global educational publisher:

- Quality is a **process**, not a hero author.  
- Every stage has **entry criteria, exit criteria, evidence, and a named authority**.  
- Failures return to a defined stage — they do not “skip to Approver because the calendar is tight.”  
- Publication is **deterministic**: same inputs and same evidence yield the same decision class.

### What this workflow governs

Authoring → Peer Review → Educational Audit → Founder Review → Publication Approval → Version Control → Edition Management → Revision Requests → Errata → Retirement → Replacement → Archive.

Nested educational certification (EA-002 stages, Gate MG/LE/SS/RV/TP, Gate CG) remains **mandatory substance law**. This workflow **orchestrates** those gates into an operational publishing pipeline; it does not replace them.

---

## 2. Lifecycle overview

```text
0. COMMISSION
      ↓
1. AUTHORING
      ↓
2. PEER REVIEW
      ↓
3. EDUCATIONAL AUDIT
      ↓
4. FOUNDER REVIEW
      ↓
5. PUBLICATION APPROVAL
      ↓
6. RELEASE / ACTIVATION GATE
      ↓
7. POST-PUBLISH VERIFICATION
      ↓
8. MAINTENANCE CYCLE  ←── revision requests / errata / edition bumps
      ↓
9. RETIREMENT / REPLACEMENT / ARCHIVE
```

Stages 1–5 are the **production spine**. Stages 6–9 are the **service spine**. Both are mandatory parts of Volume life.

---

## 3. Stage 0 — Commission

### 3.1 Job

Authorise work on a new Educational Volume (or major edition) before content labour begins.

### 3.2 Entry

- Subject series strategy known  
- Curriculum package + CMP edition pins available  
- Reference bar (Campaign Alpha floor) acknowledged  

### 3.3 Exit artefacts

| Artefact | Required |
|----------|----------|
| Volume Commission brief | Yes |
| Provisional `volume_id` + scope class | Yes |
| Target Campaign span / membership intent | Yes |
| Owner role assignment | Yes |
| Claims forbidden at commission (anti-mirage) | Yes |

### 3.4 Authority

**Founder** (or designate) commissions commercial Volumes. **Future Subject Lead** may commission within an approved series charter once that role is staffed.

### 3.5 Fail conditions

Commission FAIL if scope class is dishonest, if isolated Golden Day is proposed as a Volume, or if Alpha-bar non-compliance is pre-accepted.

---

## 4. Stage 1 — Authoring

### 4.1 Job

Produce educational substance and the Volume Dossier workfile to EA/EP law.

### 4.2 Role

**Educational Author** (primary). May be supported by co-authors; one named Author of Record.

### 4.3 Educational obligations (consumed, not redesigned)

| Obligation | Authority |
|------------|-----------|
| Artefact authoring | EA-002 Authoring Framework / Style / Voice |
| Mission / Session / Package gates | EA-003 / EA-004 / EA-001 |
| Campaign dossier + continuity | EA-008 Architecture |
| Production quality bar | EP-001 method (Alpha) |

### 4.4 Operational obligations (this programme)

1. Open Volume Dossier (`EO001_EDUCATIONAL_VOLUME_STANDARD.md` §11).  
2. Maintain Campaign membership worklist.  
3. Log defects and rework.  
4. Complete Author self-check against Alpha floor worksheet.  
5. Do not request Publication Approval from Authoring stage.

### 4.5 Exit criteria

| ID | Criterion |
|----|-----------|
| AU-01 | All intended member packages authored |
| AU-02 | Campaign Gate CG evidence pack prepared (or prior EP PASS cited) |
| AU-03 | Volume Dossier identity + membership draft complete |
| AU-04 | FP-01…FP-06 self-denied |
| AU-05 | Style + Tutor Voice self-checks recorded |
| AU-06 | No student-pathway release performed by Author |

**Exit status:** `draft` → may enter `in_review`.

---

## 5. Stage 2 — Peer Review

### 5.1 Job

Independent educational substance and craft review before formal audit.

### 5.2 Role

**Educational Reviewer** (must not be sole Author of Record for commercial Volumes).

### 5.3 Maps to nested law

Consumes EA-002 Certification stages **Educational Review** and **Tutor Review** (and Curriculum Review when staffing requires separation). Peer Review here is the **operational stage name**; nested checklists remain binding.

### 5.4 Checklist (operational)

| ID | Criterion |
|----|-----------|
| PR-01 | Nested EA-002 Educational Review PASS for all member bundles |
| PR-02 | Tutor Review PASS (voice continuity across Volume membership) |
| PR-03 | Alpha floor comparison: Tutor Intent uniqueness, Reading Guidance presence, reciprocal bridges |
| PR-04 | No syllabus-paste / placeholder / contaminant patterns (EV-001 classes) |
| PR-05 | Defects logged with return stage = Authoring |

### 5.5 Outcomes

| Result | Next |
|--------|------|
| **PASS** | Advance to Educational Audit |
| **FAIL** | Return to Authoring with defect IDs |
| **HOLD** | Block; missing evidence with expiry |

Peer Review PASS does **not** authorise publication.

---

## 6. Stage 3 — Educational Audit

### 6.1 Job

Independent audit of certification evidence, continuity measurement, trust regression, and Volume dossier honesty — as Academic Auditor, not as co-author.

### 6.2 Role

**Academic Auditor**.

### 6.3 Checklist (operational)

| ID | Criterion |
|----|-----------|
| EA-01 | Gate CG PASS evidence complete and internally consistent |
| EA-02 | Continuity Index + bridge integrity recorded and within scope-class floors |
| EA-03 | Per-package Gate MG/LE/SS/RV/TP (or Board desk equivalents) evidenced |
| EA-04 | EV-001 / EA-007 regression checklists complete |
| EA-05 | Volume status honesty (`certified` not claimed as `released`) |
| EA-06 | Dependency register complete (CMP, curriculum, activation) |
| EA-07 | Claims allowed/forbidden drafted for Approver |
| EA-08 | Grandfather / absorption notes explicit where relevant |

### 6.4 Outcomes

| Result | Next |
|--------|------|
| **PASS** | Volume may move to `certified`; advance to Founder Review |
| **FAIL** | Return to Authoring or Peer Review per defect class |
| **HOLD** | Block publication path; expiry + honesty plan required |

Educational Audit PASS does **not** authorise commercial exposure.

---

## 7. Stage 4 — Founder Review

### 7.1 Job

Judge whether the Volume meets the **house catalogue bar** — the same question EP-001 Founder Review answered for Campaign Alpha: Would we put the house name on this journey?

### 7.2 Role

**Founder** (or Founder Educational Gate Owner).

### 7.3 Checklist (operational)

| ID | Criterion |
|----|-----------|
| FR-01 | Educational journey purpose is real (not calendar coverage theatre) |
| FR-02 | Quality never drops below Alpha floor across membership days |
| FR-03 | Scope claims are honest (Pilot Arc ≠ Spine) |
| FR-04 | Revision Strategy present and non-ceremonial |
| FR-05 | Publication would not recreate orphan-excellence trust damage |
| FR-06 | Series fit: does not collide with or silently supersede another Volume |
| FR-07 | Activation / marketing constraints acknowledged |

### 7.4 Outcomes

| Result | Next |
|--------|------|
| **PASS** | Volume may move to `publication_ready` |
| **FAIL** | Return with catalogue-bar defects (often Authoring / Campaign redesign) |
| **HOLD** | Strategic pause; not a soft PASS |

Founder Review PASS is required for commercial Volumes. It is **necessary but not sufficient** for release.

---

## 8. Stage 5 — Publication Approval

### 8.1 Job

Human authorisation that the named Volume version may proceed toward student exposure under declared claims.

### 8.2 Role

**Publication Approver**.

### 8.3 Preconditions (all required)

1. Peer Review PASS  
2. Educational Audit PASS  
3. Founder Review PASS  
4. Gate CG PASS for every primary member Campaign  
5. EA-002 / EA-008 publication preconditions satisfied  
6. Volume Dossier complete  
7. FP-01…FP-06 denied  
8. Explicit: technical publish ≠ educational Volume PASS  
9. Activation engineering dependencies listed (may gate `released` without blocking `approved`)  

### 8.4 Approval outcomes

| Result | Meaning |
|--------|---------|
| **APPROVED** | Volume version → `approved`; release may proceed when activation gates clear |
| **REJECTED** | Nothing new publishes; defects returned |
| **PARTIAL HOLD** | Only listed PASS members inside an otherwise PASS Volume; cannot invent a Golden Day |

### 8.5 Approval record

Minimum fields per Volume Standard §7 plus:

- Claims allowed / forbidden  
- Activation dependencies  
- Supersession notes if replacing a prior Volume  
- Errata policy acknowledgement  

---

## 9. Stage 6 — Release / Activation Gate

### 9.1 Job

Move `approved` → `released` only when student-pathway activation is safe and joint.

### 9.2 Rules (from EP-001 lesson)

1. Do not activate a single day of a multi-day Volume alone (FP-01 recreation).  
2. Joint inventory publication only.  
3. If activation engineering is incomplete, Volume remains `approved` / `publication_ready` — **status honesty over silent partial release**.  
4. Technical deploy owners execute release; they do not redefine educational Approval.

### 9.3 Exit

| Result | Status |
|--------|--------|
| Activation complete + post-checks scheduled | `released` |
| Activation blocked | remain `approved` |

---

## 10. Stage 7 — Post-publish verification

### 10.1 Job

Spot-check live surfaces for One Educational Truth and absence of orphan-excellence framing.

### 10.2 Minimum checks

| ID | Check |
|----|-------|
| PV-01 | Inventory matches Approval record |
| PV-02 | No placeholder / contaminant leakage |
| PV-03 | Home / History / Journey / Revision project same Volume membership facts |
| PV-04 | Mode honesty on Revision days |
| PV-05 | Marketing claims match claims-allowed list |

FAIL → immediate **HOLD** path (Stage 8 / Operations).

---

## 11. Stage 8 — Maintenance cycle

### 11.1 Job

Keep One Educational Truth and Alpha-bar quality after release.

### 11.2 Triggers (mandatory)

All EA-002 / EA-008 maintenance triggers, plus Volume-level:

| Trigger | Typical path |
|---------|--------------|
| CMP edition / locus change | Revision request → educational change class |
| Syllabus / weight update | Impact inventory → possible edition bump |
| Contaminant / trust FAIL | HOLD → errata or unpublish |
| Tutor style drift | Peer / Tutor re-sample |
| Longitudinal dogfood FAIL | Scale claims withdrawn; Gate CG recertify |
| Loss of reciprocal bridge | HOLD until repaired |
| Student / Board defect report | Revision request triage |
| Activation engineering change | Dependency register update |

### 11.3 Maintenance subprocess

```text
TRIGGER
  → IMPACT INVENTORY
  → CHANGE CLASS ASSIGNMENT (Versioning Guide)
  → AUTHOR PATCH (if needed)
  → REVIEW DEPTH PER CHANGE CLASS
  → RECERTIFY affected gates / Gate CG if required
  → PUBLICATION APPROVAL for new Volume version or errata notice
  → RELEASE + verification
```

Cosmetic must not smuggle educational change.

---

## 12. Stage 9 — Retirement, Replacement, Archive

### 12.1 Retirement

Follow Volume Standard §10. Publication Approver signs; Founder acknowledges commercial Volumes.

### 12.2 Replacement

A **Replacement Volume** is a new Volume (or major edition) commissioned to supersede a prior one.

| Requirement | Rule |
|-------------|------|
| Continuity of trust | Students redirected; no silent disappearance |
| Quality | Replacement must meet Alpha floor |
| Supersession record | Prior Volume → `superseded` then `retired` |
| Evidence | Both Volumes archived with link |

### 12.3 Archive

Archive Acceptance records:

- Final Volume Dossier snapshot  
- All approval / errata / retirement records  
- Campaign membership versions  
- Claims history  
- Reason for archive  

Archived Volumes remain auditable. They are not student-reachable.

---

## 13. Revision requests (operational path)

### 13.1 Definition

A **Revision Request** is the ticket that starts maintenance work without pretending the Volume was never published.

### 13.2 Lifecycle

```text
OPEN → TRIAGE → ACCEPT / REJECT / DEFER / ERRATA
     → WORK (Authoring…)
     → RE-ENTER lifecycle at required stage
     → CLOSE with resulting version or notice
```

### 13.3 Triage authority

| Severity | Triage owner |
|----------|--------------|
| Cosmetic | Educational Reviewer or Maintenance Owner |
| Educational / Structural | Academic Auditor + Author |
| Truth-risk / trust FAIL | Publication Approver (may HOLD immediately) |

Detail: `EO001_PUBLICATION_OPERATIONS.md`.

---

## 14. Errata

### 14.1 Definition

**Errata** correct released Volumes when full edition bump is unnecessary or when urgency requires a published notice before a versioned republish.

### 14.2 Errata classes

| Class | Example | Exposure rule |
|-------|---------|---------------|
| **E1 Notice** | Typo that could mislead locus slightly | Publish notice; patch on next minor |
| **E2 Patch** | Wrong bridge target, mild educational error | Patch version (`x.y.Z` or `x.Y.z` per Versioning Guide); recertify delta |
| **E3 Emergency** | Contaminant, dual truth, unsafe guidance | Immediate HOLD/unpublish; fix; full recertify |

### 14.3 Errata record (minimum)

`errata_id`, Volume version, class, description, student-visible notice text, opened/closed dates, resulting version if any, Approver initials for E2/E3.

---

## 15. Version control and edition management

Normative rules live in `EO001_VERSIONING_GUIDE.md`.

**Workflow obligations:**

1. Every APPROVED release stamps `volume_version` + `edition_label`.  
2. Edition bumps that change CMP pin or curriculum package require Founder Review re-entry.  
3. Students remain pinned to the approved version until migrated under a published plan.

---

## 16. Determinism guarantees (anti-memory)

To prevent quality drift when people change:

| Guarantee | Mechanism |
|-----------|-----------|
| Same bar | Alpha floor worksheet mandatory every Volume |
| Same stages | No stage skipping for commercial Volumes |
| Same evidence | Dossier field floor mandatory |
| Same reject list | FP-01…FP-06 + EV-001 classes |
| Same authorities | Role matrix in Operations doc |
| Same version meaning | Versioning Guide |
| Same retirement honesty | Retirement policy |

If a future team cannot produce the dossier evidence, they do not publish — regardless of schedule.

---

## 17. Relationship to EA-002 / EA-008 workflows

| Existing law | EO-001 relationship |
|--------------|---------------------|
| EA-002 Certification Workflow | Nested inside Peer Review / Audit evidence |
| EA-002 Publication Workflow | Nested day/bundle publication constrained by Volume Approval |
| EA-008 Campaign Publication Policy | Nested journey publication; Volume is operational wrapper |
| EP-001 Publication Readiness | Reference instance of `publication_ready` posture |

**Conflict rule:** Stricter student-protection rule wins. EO-001 may not loosen EA/EP gates.

---

## 18. Closing rules

1. The lifecycle is complete only when Archive is defined — not when Approval is signed.  
2. Peer Review → Audit → Founder → Approver is sequential for commercial Volumes.  
3. Revision, errata, retirement, replacement, and archive are first-class stages.  
4. Determinism beats lore.  
5. Campaign Alpha is the living proof that the bar is achievable; EO makes the bar repeatable.

**Produce Volumes as a publisher — not as a sequence of one-off miracles.**

Signed notionally: Editorial Director · EO-001 · Publishing Workflow · 2026-08-01
