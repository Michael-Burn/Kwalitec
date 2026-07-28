# EI-001.1 — Traceability Matrix

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.1 — CI Integrity & Release Evidence  
**Date:** 2026-07-28  
**Rule:** Every remediation references ER finding → control → artefact → release impact.  
**Companion:** `EI001_1_IMPLEMENTATION_REPORT.md` · `ER001_1_RELEASE_BLOCKERS.md`

---

## 1. Finding → evidence

| Finding | ER debt / risk | Control | Artefact(s) | Release impact | Closure |
|---------|----------------|---------|-------------|----------------|---------|
| **ER-RB-01** | ER-TD-C01 · ER-R-01 | Sole CI authority; retire stale workflow | Deleted `tests.yml`; `ci.yml` header; `test_ci_integrity.py`; CONTRIBUTING / release docs | No contradictory Actions signals; G11 cites one workflow | **Closed** |
| **ER-RB-05** | ER-TD-H08 | Reproducible RC fingerprint + evidence chain | `docs/production/RELEASE_CANDIDATE_FINGERPRINT.md`; RELEASE_PROCESS / PROTOCOL / CHECKLIST updates | G11 claim packages can file SHA+tag+CI run; process binding | **Process closed** (formal RC tag = Release operator) |

---

## 2. Evidence chain map

| Link | Requirement | EI-001.1 delivery |
|------|-------------|-------------------|
| CI execution | Canonical jobs green | `ci.yml` sole file; integrity tests assert job set / Python |
| RC verification | Tag ↔ SHA ↔ VERSION | Fingerprint procedure §§3–5 |
| Release documentation | Notes / checklist cite fingerprint | RELEASE_PROCESS, RELEASE_CHECKLIST, RELEASE_PROTOCOL Tests section |

---

## 3. Gate mapping (P-002.1)

| Gate criterion | How advanced |
|----------------|--------------|
| G11.1 Required pytest suites | Sole `ci.yml` job set documented; integrity regression |
| G11.2 Ruff policy | Unchanged in CI; docs cite `ci.yml` lint job |
| G11.3 Architecture / curriculum | Architecture job + new CI integrity module |
| G11.4–G11.6 | Unchanged policy; fingerprint requires full required-job success |

Educational G1–G6: **not in scope** (frozen).

---

## 4. Explicit non-claims

| Item | Why not claimed |
|------|-----------------|
| Version 1 production-ready | Other ER-RB-02…07 residuals; educational G1–G6 |
| Hard `pip-audit` fail | ER-RB-07 unchanged |
| G12 flag matrix | ER-RB-06 unchanged |
| Application behaviour change | Forbidden by WP |

---

**End of EI001_1_TRACEABILITY_MATRIX**
