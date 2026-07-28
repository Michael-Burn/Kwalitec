# Programme Dashboard

**Programme:** OA-001 — Operational Architecture & Product Lifecycle Framework  
**Version:** 1.0  
**Status:** Active — living board index  
**Effective:** 2026-07-28  
**Owner capacity:** Founder — Product Owner  
**Update rule:** Refresh at programme start/end, quarterly risk review, and before claim-class expansion.  
**Constraint:** Status index only — does not amend gate outcomes or release artefacts.

---

## 1. Purpose

Single operational view of **where Kwalitec stands** across governance, engineering, product, and operating frameworks so teams need not reconstruct status from chat history.

Detail always lives in the cited authoritative artefacts. If this Dashboard conflicts with a cited source, **the cited source wins** — then fix this Dashboard.

---

## 2. Claim-class snapshot (as of 2026-07-28)

| Dimension | Status | Authoritative source |
|-----------|--------|----------------------|
| **Engineering claim class** | **Conditional GO** — invite-only Internal Alpha / private dogfood (low concurrency) | `knowledge/release/ER-002/ER002_RELEASE_RECOMMENDATION.md` |
| **Engineering confidence** | 82 / 100 (Conditional band) | `ER002_ENGINEERING_SCORECARD.md` |
| **Product Version 1 production-ready** | **NO GO** (educational hard gates, notably G1 FAIL) | P-003.1 dossier · P-002.1 framework |
| **Validated KSI** | **64** (below ≥ 80 bar) | EP-008.1B / EP-008.3B hold chain |
| **Commercial Readiness Index (CRI)** | **45%** (provisional) | `knowledge/product/cq001_commercial_readiness/COMMERCIAL_READINESS_BOARD.md` |
| **Educational governance baseline** | DG-001 corpus Active; not reopened by ER-002 | `knowledge/governance/` |
| **Student presentation runtime** | Sole-runtime Education OS certified path; legacy Contained | RR-002.3 |
| **G7 performance** | **HOLD** | `docs/production/G7_PERFORMANCE_HOLD.md` |
| **G12 flag matrix** | PASS for invite-only / engineering class | `docs/production/VERSION_1_FLAG_MATRIX.md` |

**Forbidden until cleared:** Unqualified Version 1 production-ready; G7 PASS / high-traffic claims; “fully converged” architecture; Stage 1 expansion as G10-complete; educational gates cleared by engineering programmes.

---

## 3. Domain health

| Domain | Posture | Notes |
|--------|---------|-------|
| **Governance** | Operating | DG-001 Active; OA-001 operating model Active |
| **Engineering** | Conditional | ER-002 Conditional GO; residuals ER2-NC-01…08 |
| **Product** | Blocked on V1 declaration | G1 / effectiveness evidence; privacy enrollment HOLD for Stage 1 |
| **Operations** | Invite-only capable | Release Playbook + Protocol; observe ER-002 C1–C7 |

---

## 4. Framework programmes (recent)

| ID | Name | Status | Outcome | Path |
|----|------|--------|---------|------|
| **DG-001** | Educational Governance | Complete (corpus Active) | Educational governance constitution & companions | `knowledge/governance/` |
| **RR-002** | Governance Convergence | Complete (in-scope Pass) | Sole-runtime path documented; legacy Contained | `knowledge/release/RR-002/` |
| **EI-001** | Engineering Improvement | Complete (historical provenance) | CI / dependency / G-pack improvements | `knowledge/release/EI-001/` |
| **ER-002** | Engineering Recertification | Complete | **Engineering Conditional GO** | `knowledge/release/ER-002/` |
| **OA-001** | Operational Architecture | Complete | Permanent operating model | `knowledge/operations/oa001/` |
| **CQ-001** | Commercial Readiness First | Complete (docs/governance) | CRI framework; baseline **43%** provisional; living board | `knowledge/product/cq001_commercial_readiness/` |
| **CQ-002** | Core Study Loop Reliability | Complete | CR1 polish; CRI **45%** provisional (+2); no `cri-45` tag | `knowledge/product/cq002_core_study_loop_reliability/` |

---

## 5. Open High residuals (engineering / architecture)

Track via ER-002 non-compliance + Technical Debt Register. Top items:

| ID | Theme | Constraint on claims |
|----|-------|----------------------|
| ER2-NC-01 | G7 HOLD | No high-traffic / load-proven marketing |
| ER2-NC-02 | G11 RC fingerprint | No unqualified V1 RC engineering PASS |
| ER2-NC-03 | G10 Stage 1 claim-class | No Stage 1 as G10-complete |
| ER2-NC-04 | G8 tagged-deploy bind | Required at V1 declaration |
| ER2-NC-05 | Flask Medium Security HOLD | No “dependency-clean” without HOLD citation |
| ER2-NC-06…08 | Contained dual-stack / dual-authority | No fully converged runtime marketing |

Canonical debt file: `docs/TECHNICAL_DEBT_REGISTER.md`.

---

## 6. Cadence tracker

| Cadence | Last done | Next due | Owner |
|---------|-----------|----------|-------|
| Engineering claim-class certification | 2026-07-28 (ER-002) | On trigger or ≤ 12 months | Engineering Owner |
| Quarterly risk review | See P-003.3 posture date 2026-07-26 | Next quarterly board | Product Owner |
| Epic debt review | Per programme completions | End of next Epic | Engineering Owner |
| Architectural Contained residual review | ER-002 / RR-002.3 | Before consolidation epic | Engineering + Educational |
| Documentation ownership sweep | OA-001 establish | With OA-001 amendments | Operations Owner |

---

## 7. How to run the next unit of work

1. Read `OPERATIONAL_ARCHITECTURE.md` and `PRODUCT_CONSTITUTION.md`.  
2. Classify via `CHANGE_MANAGEMENT_STANDARD.md`.  
3. Execute the matching lifecycle standard.  
4. Update **this Dashboard** at start (row/notes) and completion (status/outcome).  
5. Keep claim language ≤ evidence.

---

## 8. OA-001 artefact index

| Document | Path |
|----------|------|
| Operational Architecture | `OPERATIONAL_ARCHITECTURE.md` |
| Product Constitution | `PRODUCT_CONSTITUTION.md` |
| ADR Standard | `ARCHITECTURE_DECISION_RECORD_STANDARD.md` |
| Feature Lifecycle | `FEATURE_LIFECYCLE.md` |
| Technical Debt Governance | `TECHNICAL_DEBT_GOVERNANCE.md` |
| Release Governance Model | `RELEASE_GOVERNANCE_MODEL.md` |
| Change Management Standard | `CHANGE_MANAGEMENT_STANDARD.md` |
| Risk Review Standard | `RISK_REVIEW_STANDARD.md` |
| This Dashboard | `PROGRAMME_DASHBOARD.md` |
| Completion Report | `OA001_COMPLETION_REPORT.md` |

All paths relative to `knowledge/operations/oa001/`.

---

**End of Programme Dashboard**
