# Decision Process

**Programme:** P-003.7 — Product Board Charter  
**Version:** 1.0  
**Status:** Active — Board procedure  
**Effective:** 2026-07-26  
**Companion:** [`PRODUCT_BOARD_CHARTER.md`](PRODUCT_BOARD_CHARTER.md)  
**Register lifecycle (unchanged):** `../p003_2_product_decision_register/DECISION_LIFECYCLE.md`  
**Does not:** Amend Decision Register content; invent new DR IDs; change runtime  

---

## 1. Purpose

Define how the Product Board **reaches, records, and revisits** decisions so Version 1 governance is repeatable and auditable.

This process wraps the Decision Lifecycle. The Lifecycle owns register mechanics (`DR-NNN`, supersession). This document owns **Board behaviour**.

---

## 2. Decision principles (binding)

1. **Evidence before opinion.**  
2. **No unsupported educational claims.**  
3. **Evidence Hierarchy governs claims** (P-003.5).  
4. **Registers remain authoritative** (P-003.2 / .3 / .4).  
5. **Version 1 decisions remain active until formally superseded.**  
6. **Prefer lower** when evidence conflicts.  
7. **Hierarchy STOP** — contradicting higher law requires amending higher law first.

---

## 3. What the Board decides vs what it does not

| Board decides | Board does not decide |
|---|---|
| New ACTIVE product / release / claim **law or posture** (DR class) | Implementation design inside a merged PR |
| Supersession of Version 1-governing decisions | Sprint priority order |
| Risk acceptance that changes release story | Individual bug severity (unless escalated as PR) |
| Claim approval for Board / cohort / public audiences | Editorial nits in programme docs |
| Release recommendation class (GO / … / NO GO) | Deploy clock time |

---

## 4. Board decision flow

```
Intake → Classify → Evidence gate → Options → Decision → Record → Communicate → Review trigger
```

### 4.1 Intake

A matter reaches the Board from:

- Programme completion (EP / P) with material Version 1 impact  
- Gate / KSI / effectiveness status change  
- Flag production-default change proposal  
- Honesty incident or claim dispute  
- Chair / Product Governance Lead escalation  

**Required packet (minimum):**

| Field | Required |
|---|---|
| Question (one sentence) | Yes |
| Proposed decision statement | Yes |
| Decision class (Law / Contract / Posture / Operational default) | Yes |
| Evidence paths (existing) | Yes — or explicit Unavailable |
| Related DR / PR / PA / gates | If known |
| Student Impact / ΔKSI note | For EP/P programmes |
| Hierarchy conflict check | Yes (Vision / Constitution / P-002.1) |

Missing packet → **DEFER**, do not decide.

### 4.2 Classify

| Class | Board bar |
|---|---|
| **Law** | Higher-authority citation; rare; often recommend amendment upstream first |
| **Contract** | Programme completion + tests/reviews cited |
| **Posture** | Signed go/no-go, gate status, or validated board |
| **Operational default** | Flag matrix / architecture baseline + G12 awareness |

### 4.3 Evidence gate

| Result | Board action |
|---|---|
| Paths present and classified (E1–E5 or N/A for pure process) | Continue |
| Unavailable for required claim | STOP — open evidence work; do not create ACTIVE educational claim DR |
| Stale | DEFER or require re-measure |
| Falsifier present | Prefer lower; may Reject related assumption |

Evidence Lead signs classification for claim-affecting decisions.

### 4.4 Options and decision

Board states options explicitly (e.g. Confirm current NO GO; CONDITIONAL GO with named HOLDs; open evidence programme).  

Outcomes:

| Outcome | Meaning |
|---|---|
| **Approve** | Create or update DR via Lifecycle; or approve claim for stated audience |
| **Reject** | Do not register; record reason |
| **HOLD** | Conditional path with named claim restriction |
| **DEFER** | Incomplete package; no posture change |
| **Confirm** | Existing ACTIVE DR still stands; note review date |

### 4.5 Record

Minimum record in minutes or completion artefact:

- Date  
- Roles present (quorum)  
- Decision statement  
- Evidence paths  
- Outcome  
- DR/PR/PA IDs created or confirmed  
- Review trigger  

Then execute Decision Lifecycle register steps when a DR changes.

### 4.6 Communicate

| Audience | Channel |
|---|---|
| Implementers | Point to ACTIVE_DECISIONS / specific DR |
| Board only | Minutes + dossier update if release-related |
| Cohort / Public | Only after Claim Decision Tree Steps D–E |

### 4.7 Review triggers

Any of:

- Stated Future Review Trigger on the DR card  
- New validated KSI board or gate status change  
- Production flag default change  
- Constitution / PSF / P-002.1 amendment  
- Architecture baseline re-certification  
- Chair request  

Outcomes: Confirm | Amend (non-statement fields) | Supersede (statement meaning changes).

---

## 5. Special cases

### 5.1 Release recommendation

Follow [`RELEASE_DECISION_PROCESS.md`](RELEASE_DECISION_PROCESS.md). Outcome becomes posture (e.g. DR-041 class) via Lifecycle — **not** a silent README edit.

### 5.2 Public claims

Walk `../p003_5_evidence_hierarchy/CLAIM_DECISION_TREE.md` end-to-end. Board ack is mandatory for C-COM / public educational wording.

### 5.3 Flag defaults

Operational default changes require Architecture + Engineering Representatives and G12 matrix honesty; Product Governance Lead blocks if student-visible educational authority would silently move without evidence programme.

### 5.4 Docs-only programmes

May produce ΔKSI = 0. Board need not meet for every docs package; Product Governance Lead spot-checks that docs do not invent GO or external evidence.

---

## 6. Anti-patterns

| Anti-pattern | Corrective |
|---|---|
| “We’re ready because deploy worked” | Separable verdicts; GA ≠ C-V1 |
| Registering wishes as ACTIVE law | Evidence gate |
| Quiet rewrite of DR statement | Supersede |
| Using Green maturity as GO | Maturity ≠ C-V1 (P-003.6) |
| Skipping Educational Representative on C-EDU | Quorum fail → DEFER |

---

## 7. Success check

A new Board member can, for any proposed decision:

1. Name the class,  
2. Point to evidence or Unavailable,  
3. State Approve / Reject / HOLD / DEFER / Confirm,  
4. Cite the DR ID after recording —

without tribal knowledge.

---

**End of Decision Process**
