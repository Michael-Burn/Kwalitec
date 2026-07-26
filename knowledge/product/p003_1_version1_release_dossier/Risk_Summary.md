# Risk Summary — Version 1 Release Risk Register

**Programme:** P-003.1 — Version 1 Release Dossier  
**Date:** 2026-07-26  
**Scope:** Board-level **release** risks. Engineering defects are not listed as bugs unless they create release risk.

Severity: **Critical** | **High** | **Medium** | **Low**

---

## Risk register

| ID | Risk | Severity | Evidence | Likelihood | Impact if ignored | Mitigation / control | Residual |
|---|---|---|---|---|---|---|---|
| **R1** | Educational effectiveness unproven while product is described as “ready” | Critical | EP-003 PENDING EVIDENCE; EP-007.3 G1.9 FAIL; N_external=0 | High if claim language slips | Student harm; governance breach; irreversible trust loss | Keep effectiveness **NO-GO**; freeze marketing; Stage 1 after privacy | Open until C5–C6 |
| **R2** | Validated KSI **62** below Version 1 bar **80** | Critical | EP-007.2 board; G1.1 FAIL | Certain today | False Version 1 success claim | Remediation portfolio; prefer-lower; no estimate stacking | Gap **18** |
| **R3** | Privacy / data-protection gate blocks honest cohort expansion | High | `private_beta/PRIVACY_REVIEW.md` unsigned; EP-004 C1; EP-007.3 EFF-02 | High | Either illegal/unethical expansion or permanent evidence stall | Complete checklist signatures before Stage 1 invites | Open |
| **R4** | Premature Version 1 production-ready declaration | Critical | G1 FAIL; incomplete G2–G12 package | Medium without board discipline | Regulatory/reputational; wrong go-to-market | P-002.1 gates; this dossier **NO GO** | Controlled if NO GO held |
| **R5** | Cold-start / sparse-evidence overconfidence | Medium | Prefer-lower notes; readiness honesty path; sparse session content residual | Medium | False readiness / plan confidence | Unknown remains unknown; no Exam Ready | Ongoing |
| **R6** | External evidence floors unmet (N, duration, interviews) | High | EP-004 C5–C6; EP-007.3 | High while privacy blocks ops | G1.9 remains FAIL indefinitely | Privacy → invites → scorecards → interviews | Open |
| **R7** | Operational readiness overstated (perf/load) | Medium | G7 production load test NOT STARTED; G8 residuals | Medium if traffic grows | Outage / degraded study sessions | HOLD with claim limits or complete load sample | Open |
| **R8** | Telemetry overclaim (metrics “live” while gated) | Medium | Analytics COMPLETE flag OFF; Journey emit deferred | Medium | False KPI-based decisions | Claim language must match flag state (G9) | Controlled if honest |
| **R9** | Feature-flag / rollback unreadiness for ON defaults | Medium | G12 not scored; personalisation/Twin OFF | Medium if flags flipped casually | Dual truths; unsafe educational behaviour | Flag matrix; soak; kill-switch; fail-open legacy | Open for declaration |
| **R10** | Confidence Medium ceiling without external N | Medium | All Tier B packs Medium; G1.2 PASS but not High | High | Cannot reach High-confidence G1 without corroboration | External cohort + re-score | Open |
| **R11** | Deployment / release execution vs declaration confusion | Medium | Release Playbook vs P-002.1 split | Medium | Shipping a tag interpreted as V1 ready | Separate “ship build” from “declare V1” | Process control |
| **R12** | Support / commercial unreadiness for public launch | Medium | Commercial NOT STARTED; founder-operated support | High if public launch attempted | Student abandonment; support failure | Keep invite-only; no public registration | Acceptable under NO GO |
| **R13** | Independent KSI re-score (G1.7) unfinished | Medium | G1.7 HOLD | Certain until staffed | Declaration blocked even if KSI≥80 | Schedule second assessor | Open |
| **R14** | Personalisation marketed while OFF | High | EP-005.1 unsupported Δ; flags OFF | Medium without G12 discipline | Dishonest product promise | G12 matrix; claim exclusions | Controlled if enforced |

---

## Risk themes (board narrative)

### Educational effectiveness
The largest release risk is claiming educational value without cohort evidence. Perception packs improved KSI **59→62** and cleared G1.5; they explicitly do **not** satisfy G1.9.

### Privacy
Unsigned Privacy Review is both a compliance control and an evidence bottleneck: Stage 1 ops cannot start, so effectiveness cannot be measured.

### External evidence
Without ≥4 weeks / N floors / interviews (or an approved waiver with claim restrictions), educational GO is impossible under EP-003/004 rules.

### Operational readiness
CI performance budgets and Stage 0 stability are positive signals. Production load testing and full reliability packaging remain open for high-traffic claims.

### Confidence
Medium confidence is acceptable for G1.2 PASS but insufficient for aggressive marketing or High-confidence declaration narratives.

### Deployment and rollback
Architecture defines fail-open rollback for cutovers. Gate G12 still requires a published Version 1 flag matrix and kill-switch documentation before ON defaults.

---

## Risks explicitly out of scope here

- Individual code defects tracked in engineering backlogs (unless they create the release risks above).  
- Speculative market risks without evidence.  
- Version 2 product strategy items without validation.

---

## Board control statement

> Release risk is currently dominated by **unproven educational effectiveness** and **sub-bar validated KSI**, compounded by **privacy-blocked external evidence**. Under P-002.1, these force **NO GO** on Version 1 production-ready declaration. Continuing Stage 0 private beta under EP-004 conditions does not clear these risks.
