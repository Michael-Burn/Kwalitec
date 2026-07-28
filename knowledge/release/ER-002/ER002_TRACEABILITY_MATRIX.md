# ER-002 — Traceability Matrix

**Programme:** ER-002 — Engineering Recertification  
**Date:** 2026-07-28  
**Audit SHA:** `11d8a224cb4f40de94d7e48e65d467e569408d1c`  
**Purpose:** Map ER-001 findings → live evidence → ER-002 disposition (independent of EI-001 success claims)

---

## 1. ER-001 Critical / High blockers → ER-002

| ER-001 ID | Finding | Live evidence inspected | Independent verification | ER-002 disposition |
|-----------|---------|-------------------------|--------------------------|--------------------|
| ER-RB-01 | Stale `tests.yml` | `.github/workflows/` listing; `test_ci_integrity.py` | Only `ci.yml`; 27 architecture gate tests include CI integrity | **Cleared** |
| ER-RB-02 | G7 incomplete | `docs/production/G7_PERFORMANCE_HOLD.md`; release-ops tests | Artefact present; HOLD terms explicit | **Cleared via HOLD** (ER2-NC-01 residual) |
| ER-RB-03 | G8 incomplete | `G8_RELIABILITY_EVIDENCE.md` | Pack present; tabletop + backup ack | **Cleared** (ER2-NC-04 declaration residual) |
| ER-RB-04 | G10 claim-class | Policy + `G10_OPERATIONAL_EVIDENCE.md` + privacy Stage 1 posture | G10.5 hard gate Pass; expansion residual | **Partial** (ER2-NC-03) |
| ER-RB-05 | G11 fingerprinted RC | `RELEASE_CANDIDATE_FINGERPRINT.md` | Process complete; no current V1 fingerprint filed | **Partial** (ER2-NC-02) |
| ER-RB-06 | G12 matrix | `VERSION_1_FLAG_MATRIX.md`; `render.yaml`; `.env.example` | ON flags match Render sample; tests assert presence | **Cleared** |
| ER-RB-07 | Soft pip-audit | `dependency_audit.sh`; `ci.yml`; accepted register | Script exit 0; hard wiring in CI | **Cleared** |
| ER-RB-08 | Parallel `src/` | `app/__init__.py` `_ensure_src_on_path`; ~1095 `src/` files | Still bridged | **Contained** (ER2-NC-06) |
| ER-RB-09 | Dual authorities | `app/services/` vs `app/application/` / `app/domain/` | Still dual | **Contained** (ER2-NC-07) |
| ER-RB-10 | Legacy shells | RR-002.3 Contained posture; sole-runtime ON | Still Contained | **Contained** (ER2-NC-08) |

---

## 2. ER-001 debt items → ER-002

| ER-001 debt | Live state | ER-002 ID |
|-------------|------------|-----------|
| ER-TD-C01 CI workflow | Closed | — |
| ER-TD-H01 `src/` stack | Open Contained | ER2-NC-06 |
| ER-TD-H02 Dual authorities | Open Contained | ER2-NC-07 |
| ER-TD-H03 Dual factory ownership | Contained (docs + CI verify both) | ER2-NC-06 related |
| ER-TD-H04 Soft pip-audit | Closed | — |
| ER-TD-H05 G7 sample | HOLD residual | ER2-NC-01 |
| ER-TD-H06 G8 pack | Closed (declaration fingerprint open) | ER2-NC-04 |
| ER-TD-H07 G10 incomplete | Partial | ER2-NC-03 |
| ER-TD-H08 G11 RC | Process closed / tag open | ER2-NC-02 |
| ER-TD-H09 G12 matrix | Closed | — |
| ER-TD-H10 Unit CI scope | Open | ER2-NC-09 |
| ER-TD-H11 SQLAlchemy 2.x legacy | Open (not re-swept) | Medium residual |
| ER-TD-H12 Dual Mission types | Open Contained | Architecture residual |
| ER-TD-M01…M05 security Mediums | Open | ER2-NC-05, 10–13 |
| ER-TD-M12 Dual migration | Open | ER2-NC-14 |
| ER-TD-M14 Coverage unused | Open | ER2-NC-15 |

---

## 3. Audit scope domains → evidence → verdict

| Scope domain | Evidence paths | Verification | Verdict |
|--------------|----------------|--------------|---------|
| CI integrity | `.github/workflows/ci.yml`; `tests/architecture/test_ci_integrity.py` | Listing + pytest | Pass |
| Release evidence | `docs/production/G7_*`, `G8_*`, `G10_*`, `VERSION_1_FLAG_MATRIX.md`, `RELEASE_CANDIDATE_FINGERPRINT.md` | File presence + content review + release-ops tests | Conditional |
| Dependency assurance | `docs/security/DEPENDENCY_*`; `scripts/dependency_audit.sh`; `ci.yml` production-gates/release-build | Script run + pytest | Pass (HOLD) |
| Operational documentation | `docs/production/*`; playbooks | Inventory | Pass |
| Deployment readiness | `render.yaml`; `wsgi.py`; DEPLOYMENT.md | Config review | Pass (invite-only) |
| G7–G12 | Artefacts + `Release_Gates.md` | Independent rescore | Mixed |
| Technical debt | ER-001 register vs live code | Spot checks | Contained High structural |
| Architecture integrity | `app/__init__.py`; `src/`; ARCHITECTURE.md | Path + bridge check | Conditional Pass |
| Repository governance | Sole CI + fingerprint process | Tests | Pass |
| Engineering documentation | Production/GA/CONTRIBUTING/readiness | Review | Pass w/ Low drift |
| Test infrastructure | `tests/`; `ci.yml` job scopes | Review + gate pytest | Pass w/ Medium residual |
| Security controls | Factory validation; CSP; auth; G10 ops | Code + docs review | Conditional Pass |
| Release reproducibility | Fingerprint + dependency audit templates | Process review | Process Pass; tag pending |

---

## 4. Historical EI-001 provenance (not proof)

EI-001 work packages are cited only as historical provenance of artefacts independently re-verified:

| Artefact | Historical programme | ER-002 treatment |
|----------|----------------------|------------------|
| Sole `ci.yml` / retired `tests.yml` | EI-001.1 | Re-verified live |
| RC fingerprint process | EI-001.1 | Re-verified process; tag not filed |
| Dependency policy / hard gate | EI-001.2 | Re-verified live (script + CI text) |
| G7 HOLD / G8 / G10 ops / G12 matrix | EI-001.3 | Re-verified file presence + content + tests |

---

## 5. Local verification commands (reproducible)

```bash
ls .github/workflows/
test ! -f .github/workflows/tests.yml
./scripts/dependency_audit.sh
.venv/bin/python -m pytest \
  tests/architecture/test_ci_integrity.py \
  tests/architecture/test_dependency_assurance.py \
  tests/architecture/test_release_operations.py \
  -q --tb=line
```

**Recorded outcome (2026-07-28):** workflows = `ci.yml` only; dependency audit exit 0 (4 ignores); **27 passed**.

---

## 6. Deliverable cross-map

| Requirement | Deliverable |
|-------------|-------------|
| Independent engineering assessment | `ER002_ENGINEERING_AUDIT.md` |
| Remaining blockers / residuals | `ER002_NON_COMPLIANCE_REGISTER.md` |
| Confidence rescore | `ER002_ENGINEERING_SCORECARD.md` |
| Finding ↔ evidence map | This matrix |
| Version 1 engineering recommendation | `ER002_RELEASE_RECOMMENDATION.md` |
| Certification outcome + report sections | `ER002_CERTIFICATION_REPORT.md` |

---

**End of ER-002 Traceability Matrix**
