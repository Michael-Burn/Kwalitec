# EI-001.2 — Test Report

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.2 — Dependency Assurance & Security Controls  
**Date:** 2026-07-28  
**Companion:** `EI001_2_IMPLEMENTATION_REPORT.md`  
**Environment:** `.venv` (local); CI unit matrix remains 3.11–3.13

---

## Commands executed

```bash
# Hard dependency audit (accepted HOLDs applied)
./scripts/dependency_audit.sh
./scripts/dependency_audit.sh --output /tmp/ei0012-pip-audit.txt

# Architecture + dependency assurance + CI integrity + release artefacts
.venv/bin/python -m pytest \
  tests/architecture/ \
  tests/application/educational_intelligence_pipeline/test_health_and_ci.py::TestCiIntegration \
  -v --tb=line -q

# Focused module confirmation
.venv/bin/python -m pytest \
  tests/architecture/test_dependency_assurance.py \
  tests/architecture/test_ci_integrity.py \
  tests/architecture/test_release_artefacts.py \
  -v --tb=line -q

# Lint touched Python
.venv/bin/ruff check \
  tests/architecture/test_dependency_assurance.py \
  tests/architecture/test_ci_integrity.py \
  --ignore=F401
```

---

## Outcome

| Suite / check | Result |
|---------------|--------|
| `./scripts/dependency_audit.sh` | **exit 0** — “No known vulnerabilities found, 4 ignored” |
| `tests/architecture/` + `TestCiIntegration` | **2129 passed** |
| `test_dependency_assurance.py` | **8 passed** |
| `test_ci_integrity.py` (incl. hard-gate assert) | **9 passed** (includes new hard-gate test) |
| `test_release_artefacts.py` | **passed** |
| Focused trio | **27 passed** |
| `ruff` on touched Python | **All checks passed** |

---

## Verification coverage

| Acceptance / finding | How verified |
|----------------------|--------------|
| ER-RB-07 — explicit enforceable policy | Policy doc + architecture assertions |
| Hard CI gate (no soft fail) | `ci.yml` text asserts; soft patterns forbidden |
| Accepted findings sync | `.txt` IDs ⊆ `DEPENDENCY_ACCEPTED_FINDINGS.md` |
| Reproducible release evidence | Script run exit 0; `--output` supported |
| Integration with release docs | Doc updates; fingerprint hard-gate wording |
| No application behaviour change | No `app/` product logic edits in this WP |

---

## Intentionally not executed here

| Item | Rationale |
|------|-----------|
| Full remote GitHub Actions on a Version 1 RC tag | Release operator step; local architecture + script are WP evidence |
| Flask pin upgrade regression | Out of scope (ER-TD-M04) |
| Educational / recommendation / UI suites | Frozen educational governance |

---

## Engineering fingerprint for this remediation (local)

| Field | Value |
|-------|-------|
| purpose | EI-001.2 dependency assurance remediation evidence |
| ci_workflow | `.github/workflows/ci.yml` (hard `scripts/dependency_audit.sh`) |
| dependency_command | `./scripts/dependency_audit.sh` |
| accepted_findings | `docs/security/DEPENDENCY_ACCEPTED_FINDINGS.md` |
| recorder | Engineering (EI-001.2) |

---

**End of EI001_2_TEST_REPORT**
