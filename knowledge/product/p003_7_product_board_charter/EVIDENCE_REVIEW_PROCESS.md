# Evidence Review Process

**Programme:** P-003.7 — Product Board Charter  
**Version:** 1.0  
**Status:** Active — Board procedure  
**Effective:** 2026-07-26  
**Companion:** [`PRODUCT_BOARD_CHARTER.md`](PRODUCT_BOARD_CHARTER.md)  
**Claim law (unchanged):** `../p003_5_evidence_hierarchy/`  
**Does not:** Amend Evidence Hierarchy levels, claim freezes, or validation methodology  

---

## 1. Purpose

Define how the Product Board **admits, classifies, uses, and retires** evidence for product, release, and marketing claims.

Canonical levels E1–E5 and claim codes remain in P-003.5. This document is the Board’s operating procedure around that law.

---

## 2. Principles

| Principle | Rule |
|---|---|
| Prefer lower | Conflict → lower claim set |
| Necessary ≠ sufficient | E2/E3 do not unlock E5 claims |
| Freshness | Stale evidence → treat weaker or DEFER |
| Linked paths | Unlinked anecdote is not evidence |
| Separable verdicts | Programme GO ≠ C-EDU ≠ C-V1 |
| No invention | Missing = **Evidence currently unavailable** |
| Registers stay authoritative | Evidence may update PR/PA/DR posture; it does not silently rewrite IDs |

---

## 3. Evidence intake flow

```
Submit packet → Classify (E1–E5 / Unavailable / Stale / Falsifier)
        → Map permitted claims (C-*)
        → Board accept for use?
        → Update claims / posture / risks / assumptions as needed
        → Archive citation in minutes or package index
```

### 3.1 Submit packet

| Field | Required |
|---|---|
| Exact claim(s) the evidence is meant to support | Yes |
| Audience (eng / Board / cohort / public) | Yes |
| Claim window (e.g. W-PROD) | Yes |
| Immutable path(s) in repository or signed external store | Yes |
| Method summary (Tier A–D / cohort N / internal vs external) | Yes |
| Known limitations / falsifiers | Yes |
| Owner | Yes |

### 3.2 Classify

Evidence Lead applies `EVIDENCE_CLASSIFICATION.md`:

| Outcome | Meaning |
|---|---|
| **E5** | External educational outcome |
| **E4** | Structured external perception |
| **E3** | Structured internal / persona validation |
| **E2** | Engineering verification |
| **E1** | Architectural / product reasoning |
| **Unavailable** | Required level missing |
| **Stale** | Outside freshness rules |
| **Falsifier** | Lowers or blocks claims |

**As of 2026-07-26:** E5 and E4 for Version 1 educational-outcome claims remain **Unavailable** (`N_external = 0`; effectiveness NO-GO). This Charter does not invent them.

### 3.3 Map permitted claims

Use `CLAIM_STANDARD.md` matrix + standing freezes. Walk `CLAIM_DECISION_TREE.md` when publication is requested.

### 3.4 Board accept for use?

| Decision | Effect |
|---|---|
| **Accept** | Evidence may be cited in dossier, DR posture, claim ack |
| **Accept with cap** | Limited C-* codes or Board-only audience |
| **Reject** | Not claim-grade; may still inform engineering |
| **DEFER** | Need method disclosure, N floors, or re-measure |

### 3.5 Downstream updates (when Accept changes story)

| If evidence changes… | Then review… |
|---|---|
| Gate / KSI / effectiveness | Release dossier + DR posture (e.g. DR-041 / DR-051) |
| Material release exposure | Risk Register (P-003.3) |
| Known vs believed vs disproved | Assumption Register (P-003.4) |
| Capability proof class | Maturity re-assessment (P-003.6) — prefer lower |

Register **mechanics** follow existing review processes; Board authorises material posture shifts.

---

## 4. How assumptions become validated

Assumptions are not “validated” by Board vote alone.

| Path | Requirement |
|---|---|
| Law / invariant | Higher-authority citation → PA Validated for that claim window |
| Methodology certified | Explicit method certification for claim class |
| Universal root-cause + remediation accepted | Documented acceptance |
| External outcome | E5 floors met for effectiveness-class assumptions |

Hypothesis → Supported needs Tier B / structural evidence.  
Supported → Validated needs the Validated bar above.  
Rejected stays Rejected unless methodology changes with new evidence.

Detail: `../p003_4_product_assumption_register/ASSUMPTION_REVIEW_PROCESS.md`.

---

## 5. How risks are closed

| Closure type | Evidence bar |
|---|---|
| Fixed | Fix / RCA / programme exit with proof |
| Controlled → Watch | Controls proven; reopen triggers named |
| Accepted residual | Conscious acceptance under invite-only / OFF flags / NO GO — **not** a silent close |
| Re-open | Regression evidence |

Detail: `../p003_3_product_risk_register/RISK_REVIEW_PROCESS.md`.

---

## 6. Evidence review meeting (agenda skeleton)

1. Packets submitted since last review  
2. Classification results (table: path → E-level → permitted C-*)  
3. Freeze impacts (recommendation-effectiveness, Exam Ready, C-COM, etc.)  
4. Register impacts (DR / PR / PA candidates)  
5. Release dossier delta (if any)  
6. Actions and owners  

Cadence: [`MEETING_CADENCE.md`](MEETING_CADENCE.md).

---

## 7. Anti-patterns

| Anti-pattern | Correction |
|---|---|
| Treating pytest Pass as educational effectiveness | Cap at E2 / C-IMP–style claims |
| Treating Tier B N=9 persona as E4 | Keep E3; disclose internal |
| Using estimated ΔKSI for G1 | Estimated ≠ validated (DR-026) |
| Publishing before Board ack | Claim tree Step D |
| Maturity Green → public ready | Maturity ≠ C-V1 |

---

## 8. Success check

A new Board member can take a proposed sentence (“students learn better with Kwalitec”) and determine, using this folder + P-003.5 citations:

- required E-level,  
- whether evidence exists,  
- whether the claim is frozen,  
- whether Board may Approve, HOLD, or STOP —

without reading engineering source trees.

---

**End of Evidence Review Process**
