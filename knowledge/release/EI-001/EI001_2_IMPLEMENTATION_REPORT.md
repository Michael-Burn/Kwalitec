# EI-001.2 — Implementation Report

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.2 — Dependency Assurance & Security Controls  
**Date:** 2026-07-28  
**Authority:** ER-001.1 · `ER001_1_RELEASE_BLOCKERS.md` · `ER001_1_RISK_REGISTER.md` · `ER001_1_TECHNICAL_DEBT_REGISTER.md`  
**Findings:** ER-RB-07  
**Governance stance:** Educational baselines frozen — no product / schema / educational changes

---

## 1. Objective

Close ER-RB-07 by making dependency audit policy explicit and enforceable, and by making release security evidence reproducible, without changing application behaviour.

---

## 2. Changes delivered

### 2.1 Policy and HOLD register

| Artefact | Role |
|----------|------|
| `docs/security/DEPENDENCY_ASSURANCE_POLICY.md` | Normative severity / CI / tag rules (G10.5) |
| `docs/security/DEPENDENCY_ACCEPTED_FINDINGS.md` | Security HOLD dispositions for Medium/Low residuals |
| `docs/security/dependency_accepted_vulns.txt` | Machine-readable `--ignore-vuln` IDs |

Accepted IDs (initial): PYSEC-2026-1377, PYSEC-2026-2151 (Flask Medium HOLD), PYSEC-2026-1845 (pytest non-prod), PYSEC-2026-2270 (python-dotenv Low).

### 2.2 Reproducible verification

| Artefact | Role |
|----------|------|
| `scripts/dependency_audit.sh` | Shared CI/operator entrypoint; hard-fails unaccepted findings |

### 2.3 CI hard gate (ER-RB-07)

| Location | Change |
|----------|--------|
| `production-gates` | Soft warn/`exit 0` replaced with `./scripts/dependency_audit.sh --output pip-audit.txt` |
| `release-build` | `pip-audit … \|\| true` replaced with same script; assurance artefacts asserted |

### 2.4 Regression guards

| Artefact | Role |
|----------|------|
| `tests/architecture/test_dependency_assurance.py` | Policy artefacts, ID↔register sync, hard-gate wiring |
| `tests/architecture/test_ci_integrity.py` | Assert soft-gate strings absent; script invoked |

### 2.5 Engineering documentation alignment

Updated: `DEPENDENCY_AUDIT_V2.md`, `RELEASE_PROCESS.md`, `RELEASE_CANDIDATE_FINGERPRINT.md`, `RELEASE_PROTOCOL.md`, `RELEASE_CHECKLIST.md`, `V2_RELEASE_CHECKLIST.md`, `CERTIFICATION_REPORT.md`, `SECURITY_REVIEW.md`, `QUALITY_MANUAL.md`, `RELEASE_PLAYBOOK.md`, `CONTRIBUTING.md`, `VERSION_1_READINESS.md`, ER-001.1 registers (ER-RB-07 / ER-TD-H04 / ER-R-03 / partial ER-RB-04 / ER-TD-H07).

### 2.6 Explicitly unchanged

Application code under `app/` / educational behaviour, recommendation / Mission Intelligence, database schema, UI, Flask pin (ER-TD-M04 residual), privacy pack (ER-RB-04 residual).

---

## 3. Justification

G10.5 and ER-RB-07 require Criticals blocked **or** explicit Security HOLD. Soft CI made both impossible to prove. A hard gate plus an accepted-findings register satisfies the clearance criterion while keeping product pins stable in this infrastructure WP.

---

## 4. Residual engineering (out of this WP)

| Item | Status |
|------|--------|
| ER-TD-M04 Flask ≥3.1.3 bump | Open — dependency chore |
| ER-RB-04 privacy pack | Open — G10 residual |
| ER-RB-02 / 03 / 06 | Open — G7 / G8 / G12 |
| Dependabot (ER-TD-E04) | Enhancement |

---

## 5. Companion artefacts

- `EI001_2_DESIGN_REPORT.md`  
- `EI001_2_TRACEABILITY_MATRIX.md`  
- `EI001_2_TEST_REPORT.md`  
- `EI001_2_COMPLETION_REPORT.md`

---

**End of EI001_2_IMPLEMENTATION_REPORT**
