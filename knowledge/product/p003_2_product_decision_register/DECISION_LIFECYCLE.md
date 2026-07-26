# Decision Lifecycle

**Programme:** P-003.2 — Product Decision Register  
**Date:** 2026-07-26  
**Status:** Active process for maintaining the Product Decision Register  
**Does not:** Amend Vision, PSF, P-002.1 gates, Educational Constitution, or runtime

---

## 1. Purpose

Decisions that govern Version 1 must remain:

1. **Discoverable** — Product Board can find them without reading every programme folder.  
2. **Traceable** — every decision cites programme + evidence.  
3. **Honest** — posture snapshots update when evidence changes; law does not silently rewrite.  
4. **Stable** — Decision IDs (`DR-NNN`) do not change meaning; supersession creates history.

This lifecycle governs the **register**, not educational algorithms.

---

## 2. Decision classes

| Class | Meaning | Examples | Change frequency |
|---|---|---|---|
| **Law** | Standing rule of product/architecture/governance | DR-001 ownership; DR-025 KSI ≥ 80; DR-030 G1–G12 | Rare; requires higher-authority amendment first (`GOVERNANCE.md` hierarchy) |
| **Contract** | Binding Runtime A quality/behaviour contract | DR-052 EP-003 contracts; DR-019 MES pass-through | Programme-driven; verify against constitution |
| **Posture** | Current board state under existing law | DR-041 NO GO; DR-051 KSI 62; DR-040 beta GO WITH CONDITIONS | Updates when evidence programmes complete |
| **Operational default** | Production flag/environment default | DR-009 Twin OFF; DR-039 personalisation OFF | Changes only with G12/matrix + board awareness |

---

## 3. Lifecycle stages

```
Propose → Evidence → Register → Active → Review → (Confirm | Amend | Supersede)
```

### 3.1 Propose

A candidate decision may arise from:

- Programme completion (EP/P)  
- ADR acceptance  
- Educational Constitution / governance amendment  
- Board go/no-go or release dossier update  

**Required before registration:**

- Decision statement (one or two sentences)  
- Category  
- Evidence path(s) that already exist  
- Programme ID(s)  
- Why it governs Version 1 (not a one-off task note)

**Forbidden:** Registering aspirational wishes, unbacked estimates, or “we should eventually…” items as ACTIVE law.

### 3.2 Evidence

Minimum evidence:

| Decision class | Minimum evidence |
|---|---|
| Law | Higher-authority document or accepted ADR / constitution article |
| Contract | Programme completion + tests/reviews cited |
| Posture | Signed or programme-issued go/no-go, gate status, or validated KSI board |
| Operational default | Architecture baseline or flag matrix / env policy artefact |

If evidence is missing → label **Evidence currently unavailable** and **do not** create DR as ACTIVE.

### 3.3 Register

1. Allocate next free `DR-NNN` (never reuse IDs).  
2. Add full card to `PRODUCT_DECISION_REGISTER.md`.  
3. Add row to `ACTIVE_DECISIONS.md`.  
4. Add row to `DECISION_TRACEABILITY.md`.  
5. If replacing a prior posture/law interpretation, add `SD-NNN` in `SUPERSEDED_DECISIONS.md` and link successors.

P-003.2 itself only packages existing decisions; future programmes that create new product law should update this register in the same change set (docs-only OK).

### 3.4 Active

ACTIVE decisions govern Version 1 behaviour, claims, or release posture. Implementers and reviewers must not contradict them without amending higher authority first.

### 3.5 Review

Triggers (any one):

- Stated **Future Review Trigger** on the card fires  
- New validated KSI board or gate status change  
- Feature flag production-default change  
- Educational Constitution / PSF / P-002.1 amendment  
- Architecture baseline re-certification (EP-002.9 successor)  
- Board request

Review outcomes:

| Outcome | Action |
|---|---|
| **Confirm** | Note review date in traceability or completion report; leave ACTIVE |
| **Amend** | Edit card fields that do not change ID meaning (evidence paths, programme list, risks). If the *statement* changes materially → supersede instead |
| **Supersede** | Move to SUPERSEDED (SD-NNN); create successor DR or update posture DR; never silently rewrite history |

### 3.6 Supersede

1. Create `SD-NNN` with former posture, why superseded, successor IDs, evidence, date.  
2. Update or add successor `DR-NNN`.  
3. Remove superseded ID from ACTIVE index (or mark historical).  
4. Keep full cards/history readable.

Posture updates (e.g. KSI 62 → 65) typically:

- Supersede old posture as SD  
- Update DR-051 statement/evidence **or** allocate a new posture DR and retire the old one  

Prefer **updating** a dedicated posture card (DR-051) with supersession note over proliferating posture IDs — but always record the prior number in SUPERSEDED or in the card history section.

---

## 4. Authority and conflicts

When a new programme conflicts with an ACTIVE decision:

1. **STOP**  
2. Identify higher authority per `knowledge/GOVERNANCE.md` §1  
3. Amend higher authority **or** abandon the conflicting change  
4. Then update the Decision Register  

The Decision Register **does not** outrank Vision, Educational Constitution, PSF, Explainability/Recommendation standards, or P-002.1. It **indexes** decisions those authorities and programmes have already made.

Conflict rank reminder:

Vision → Product standards (KSI / Explainability / Recommendation / Release) → Educational Constitution → EVF → Architecture → ADRs → Engineering → PRDs

---

## 5. Relationship to other artefacts

| Artefact | Role vs Decision Register |
|---|---|
| Vision 2030 | Source of philosophy / Final Test / Never-Build |
| P-001.* / P-002.1 | Source of measurement and release law |
| P-003.1 Release Dossier | Evidence synthesis; may update posture DRs |
| EP-002.9 baseline | Source of Runtime A ownership DRs |
| ADRs | Source of architecture DRs |
| Programme completion reports | Evidence; may propose new DRs |
| This register (P-003.2) | Permanent index + lifecycle; ΔKSI = 0 |

---

## 6. Version 1 vs Version 2

- Version 1 student-visible defaults are governed by Runtime A decisions (DR-001 family).  
- V2 ADRs may be ACTIVE for V2/EOS paths without superseding V1 defaults (see DR-053).  
- Do not collapse V1 and V2 authorities into one DR unless a cutover programme explicitly does so with evidence.

---

## 7. Maintenance checklist (programme exit)

When completing a future EP/P that changes governing behaviour or board posture:

- [ ] Identify affected DR IDs  
- [ ] Add/amend/supersede cards  
- [ ] Update ACTIVE / SUPERSEDED / TRACEABILITY  
- [ ] Cite evidence paths in SIA / completion report  
- [ ] Record ΔKSI honestly (docs-only → 0)  
- [ ] Do not invent DRs without evidence  

---

## 8. Non-goals

This lifecycle does **not**:

- Replace PRD approval  
- Replace EVF Educational Release Gate  
- Replace P-002.1 go/no-go board  
- Authorize runtime changes  
- Auto-promote estimated ΔKSI into validated KSI  

---

**End of Decision Lifecycle**
