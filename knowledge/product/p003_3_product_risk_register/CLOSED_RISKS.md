# Closed Risks

**Programme:** P-003.3 — Product Risk Register  
**Date:** 2026-07-26  
**Status:** CLOSED / FIXED index  
**Canonical open cards:** [`PRODUCT_RISK_REGISTER.md`](PRODUCT_RISK_REGISTER.md)

Risks listed here are **not** open Version 1 release blockers. They are retained so the Board does not re-open fixed issues without cause, and so recurring *classes* of risk remain visible (e.g. adapter-contract gaps).

**Rule:** Closed ≠ “never relevant again.” Re-open via [`RISK_REVIEW_PROCESS.md`](RISK_REVIEW_PROCESS.md) if evidence regresses.

---

## Closed / fixed (evidenced)

### CR-001 — Home → Start Session HTTP 500 (private beta P0)

| Field | Content |
|---|---|
| **Category** | Technical · Deployment |
| **Status** | CLOSED |
| **Description** | P0 defect: Home → Start Session returned HTTP 500, blocking study start for beta operators. |
| **Evidence** | `knowledge/product/ep004_private_beta/ROOT_CAUSE_ANALYSIS.md` — FIXED and verified (regression tests cited) |
| **Closed date** | Per EP-004 private beta RCA (pre-2026-07-26 dossier freeze) |
| **Closure proof** | Fix + regression tests passing as recorded in RCA |
| **Why retained** | Recurring class: opaque engine/adapter contract gaps can create student-blocking incidents |
| **Related open risks** | PR-013 (reliability packaging); PR-025 (authority/contract integrity watch) |
| **Related Programmes** | EP-004 private beta |

---

### CR-002 — Production CSP blocking inline scripts (RC2 critical)

| Field | Content |
|---|---|
| **Category** | Technical · Privacy |
| **Status** | CLOSED |
| **Description** | Critical CSP configuration blocked required inline scripts in production review. |
| **Evidence** | RC2 operational readiness report (cited in architecture / readiness lineage; residual CSP *hardening* remains open as PR-023) |
| **Closed date** | During RC2 review cycle |
| **Closure proof** | Critical CSP blocking fixed during that review |
| **Why retained** | Distinguishes fixed critical CSP failure from residual hardening (PR-023) |
| **Related open risks** | PR-023 |
| **Related Programmes** | Operational readiness / GA lineage |

---

### CR-003 — EP-002.9 programme exit risks (R1–R7, R9, R10 class) mitigated

| Field | Content |
|---|---|
| **Category** | Technical · Educational |
| **Status** | CLOSED (mitigated at programme exit) |
| **Description** | Architecture programme exit certified Twin soak/authority risks as Mitigated under production defaults OFF / fail-open legacy. |
| **Evidence** | `knowledge/architecture/ep002_9_programme_exit_certification/` risk / ownership artefacts; EP-002 soak rollback verifiers |
| **Closed date** | EP-002.9 programme exit |
| **Closure proof** | Exit certification; production defaults Twin/Authority OFF |
| **Why retained** | Re-opens if Twin/cutover ON as production default without re-certification → see PR-012, PR-025 |
| **Related open risks** | PR-012, PR-025 |
| **Related Programmes** | EP-002.*, EP-002.9 |

---

### CR-004 — EP-003.1–003.4 architecture / quality residual “Acceptable”

| Field | Content |
|---|---|
| **Category** | Educational · Technical |
| **Status** | CLOSED (acceptable residual at programme exit) |
| **Description** | Programme `RISK_ASSESSMENT.md` files rated residuals Acceptable after quality contracts, tests, and claim boundaries (honest refusal, no over-claim without cohort). |
| **Evidence** | `ep003_1_.../RISK_ASSESSMENT.md`; `ep003_2_.../RISK_ASSESSMENT.md`; `ep003_3_.../RISK_ASSESSMENT.md`; `ep003_4_.../RISK_ASSESSMENT.md` |
| **Closed date** | Respective EP-003.* exits |
| **Closure proof** | Tests green + constitutional / claim-boundary mitigations recorded |
| **Why retained** | Over-claiming K2/K3 without cohort remains an *open release* theme via PR-001/PR-002 — programme engineering residuals closed; educational evidence not closed |
| **Related open risks** | PR-001, PR-002, PR-025 |
| **Related Programmes** | EP-003.1–EP-003.4 |

---

### CR-005 — EP-004.1–004.3 personalisation “second brain” risks mitigated (flags OFF)

| Field | Content |
|---|---|
| **Category** | Educational · Technical |
| **Status** | CLOSED (mitigated while flags OFF) |
| **Description** | Profile-as-second-recommender/planner risks mitigated by no-decision-API architecture and production flags OFF. |
| **Evidence** | EP-004.1–004.3 `RISK_ASSESSMENT.md`; constitutional verifications; DR-006 / DR-039 |
| **Closed date** | Respective EP-004.* exits |
| **Closure proof** | Architecture + flag defaults; residual thin-sample / durability accepted separately (PR-026) |
| **Why retained** | Re-opens on personalisation ON without G12 + re-certification → PR-012, PR-016, PR-025 |
| **Related open risks** | PR-012, PR-016, PR-025, PR-026 |
| **Related Programmes** | EP-004.1–EP-004.3 |

---

## Explicitly not closed

Do **not** treat these as closed merely because perception or structural packs improved:

| Theme | Why still open | Active ID |
|---|---|---|
| Educational effectiveness | G1.9 FAIL; N_external=0 | PR-001, PR-006 |
| KSI ≥ 80 | Validated KSI 62 | PR-002 |
| Privacy signatures | Unsigned checklist | PR-003 |
| G12 flag matrix | Not scored | PR-012 |
| Gate package | Multiple IN PROGRESS / FAIL | PR-019 |

---

## Counts

| Set | Count |
|---|---:|
| Closed / mitigated entries | 5 (CR-001…CR-005) |
| Open product risks | 26 (PR-001…PR-026) |
