# VP-001 — Founder Acceptance Criteria

**Programme:** VP-001 — Version 1 Product Completion  
**Date:** 2026-07-28  
**Status:** Complete (acceptance artefact)

---

## 1. Capability statement (target)

> Kwalitec delivers a complete, coherent and explainable Version 1 learning
> experience powered by a single Educational Intelligence Platform.

---

## 2. Version 1 product acceptance criteria

A Version 1 student product is **accepted for Founder Validation dogfood** when
all of the following hold:

| ID | Criterion | Evidence |
|----|-----------|----------|
| **A1** | New student enrolment can create SCI + initial decisions + experience models without manual founder rebuild when a published CKG edition exists | LP-001 onboard hooks; `tests/application/version1_product/` |
| **A2** | Student Home / Mission framing / Coach metadata / Revision / Session consume Experience Models via Runtime Integration when SCI+decisions exist | RI-001 + VP-001 surface wiring |
| **A3** | Study activity records Learning Evidence and refreshes Twin / Decisions / Experiences without manual intervention | Session evidence hook; E2E test |
| **A4** | Presentation does not contain educational reasoning or a parallel recommendation engine | Architecture review; RI-002 surface inventory tests |
| **A5** | Sole-runtime student path covers Home → Session → Revision → Progress | Journey audit; existing consolidation |
| **A6** | Runtime A Temporary compatibility remains when no published edition / SCI | Fail-open hooks; RIS fallback telemetry |

---

## 3. Explicit non-claims

VP-001 **does not** declare:

- Version 1 **production-ready** (P-002.1 G1–G12 all green)
- Validated KSI ≥ 80
- Founder Validated CRI promotion
- Hard removal of Runtime A (RI-005)
- Public registration or notification delivery product

Those remain governed by P-002.1, FV-001, and CQ-007 constraints.

---

## 4. Remaining blockers for Founder Validation

| Blocker | Severity | Owner track |
|---------|----------|-------------|
| Founder Validated CRI still **0% Open** — needs genuine FV-001 sessions | Critical for commercial claim | FV-001 |
| Validated KSI below ≥ 80 bar | Blocks V1 production-ready (G1) | Product measurement |
| Published CKG edition required for Preferred Authority on a subject | Major for EI adoption | EI-003 publish + enrolment subject coverage |
| Runtime A still Temporary compatibility for JSON-only subjects | Expected | RI-005 when fallback → 0 |
| Notifications delivery UI absent | Minor for V1 dogfood | Future product |
| G7 performance HOLD | Release framework | Ops / G7 evidence |

---

## 5. Founder Validation readiness (CQ-007 / FV-001)

| Question | Answer |
|----------|--------|
| Can the founder use `/student` + `/session` as exclusive daily OS? | **Yes** (unchanged CQ-007 GO WITH CONSTRAINTS) |
| Will educational interactions prefer the EI Platform when published? | **Yes** after VP-001 wiring |
| May Engineering CRI be inflated from VP-001 alone? | **No** — ΔCRI = 0 provisional infra |
| May Critical/Major FV blockers trigger engineering fixes? | **Yes** per FV-001 protocol |

---

## 6. Acceptance decision for VP-001 scope

| Decision | Result |
|----------|--------|
| VP-001 product completion (EI-powered journey wiring) | **Accept** |
| Version 1 production-ready declaration | **Not claimed** |
| Ready to continue FV-001 dogfood under CQ-007 constraints | **Yes** |

---

**End of Founder Acceptance Criteria**
