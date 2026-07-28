# EI-001.3 — Traceability Matrix

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.3 — Release Operations & Deployment Evidence  
**Date:** 2026-07-28  
**Rule:** Every remediation references ER finding → control → artefact → release impact.  
**Companion:** `EI001_3_IMPLEMENTATION_REPORT.md` · `ER001_1_RELEASE_BLOCKERS.md`

---

## 1. Finding → evidence

| Finding | ER debt / risk | Control | Artefact(s) | Release impact | Closure |
|---------|----------------|---------|-------------|----------------|---------|
| **ER-RB-02** | ER-TD-H05 · ER-R-02 | G7.1 CI budgets + G7.2 HOLD | `G7_PERFORMANCE_HOLD.md`; Performance Baseline; GA perf tests | High-traffic claims restricted; invite-only allowed | **Closed** (HOLD) |
| **ER-RB-03** | ER-TD-H06 · ER-R-02 | G8.4 tabletop + G8.5 backup ack | `G8_RELIABILITY_EVIDENCE.md`; DEPLOYMENT / BACKUP docs | Rollback + backup posture evidenced for claim class | **Closed** |
| **ER-RB-04** (ops) | ER-TD-H07 · ER-R-09 | Operational G10 ack | `G10_OPERATIONAL_EVIDENCE.md` (+ EI-001.2 G10.5) | Secrets/startup/no-secrets documented; privacy still open | **Partial** |
| **ER-RB-06** | ER-TD-H09 · ER-R-10 | Published G12 matrix | `VERSION_1_FLAG_MATRIX.md`; `render.yaml` / `.env.example` pointers; architecture tests | Flag defaults intentional + reversible | **Closed** |

---

## 2. Evidence chain map

| Link | Requirement | EI-001.3 delivery |
|------|-------------|-------------------|
| Performance | G7.1 green + G7.2 sample or HOLD | Soft budgets re-verified; HOLD filed |
| Reliability | G8.4 + G8.5 | Tabletop drill + backup acknowledgement |
| Security ops | G10 operational residual | Ops evidence pack; privacy excluded |
| Feature flags | G12.1–G12.6 | Matrix + kill-switch + config alignment |
| Deployment docs | Reproducible | DEPLOYMENT / Process / Playbook cross-links |

---

## 3. Gate mapping (P-002.1)

| Gate criterion | How advanced |
|----------------|--------------|
| G7.1 | CI soft budgets green (test report) |
| G7.2 | **HOLD** with high-traffic restriction |
| G7.3 | Invite-only: no unexplained P1 vs certified production SLO |
| G8.4 / G8.5 | Filed in `G8_RELIABILITY_EVIDENCE.md` |
| G8.1–G8.3 | Procedures bound; tagged-deploy fingerprint remains Release operator at declaration |
| G10.2 / G10.6 / G10.7 | Operational ack |
| G10 privacy | **Not closed** (ER-RB-04 residual) |
| G12.1–G12.6 | Matrix PASS for invite-only / engineering claim class |

Educational G1–G6: **not in scope** (frozen).

---

## 4. Explicit non-claims

| Item | Why not claimed |
|------|-----------------|
| Version 1 production-ready | Educational G1–G6; ER-RB-04 privacy; G11 formal RC tag; G7 HOLD |
| G7 PASS without restriction | Load sample / concurrency not filed |
| Privacy pack complete | Out of scope; ER-RB-04 residual |
| Application behaviour change | Forbidden by WP |
| Live production rollback / restore executed | Tabletop only (behaviour freeze) |

---

**End of EI001_3_TRACEABILITY_MATRIX**
