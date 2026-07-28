# EI-001.1 — Test Report

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.1 — CI Integrity & Release Evidence  
**Date:** 2026-07-28  
**Companion:** `EI001_1_IMPLEMENTATION_REPORT.md`  
**Environment:** `.venv` (Python 3.14 local interpreter; CI unit matrix remains 3.11–3.13)

---

## Commands executed

```bash
# Workflow inventory
test ! -f .github/workflows/tests.yml
test -f .github/workflows/ci.yml
ls .github/workflows/

# Architecture governance + CI integrity + EI CI integration
.venv/bin/python -m pytest \
  tests/architecture/ \
  tests/application/educational_intelligence_pipeline/test_health_and_ci.py::TestCiIntegration \
  -v --tb=line -q

# Lint touched Python
ruff check tests/architecture/test_ci_integrity.py --ignore=F401
```

---

## Outcome

| Suite | Result |
|-------|--------|
| `tests/architecture/` + `TestCiIntegration` | **2120 passed** |
| New `test_ci_integrity.py` | **8 passed** (sole workflow, job keys/names, Python matrix, gate signals, fingerprint doc) |
| `ruff` on new module | **All checks passed** |
| `tests.yml` absent | **Confirmed** |
| Sole workflow file | **`ci.yml` only** |

---

## Verification coverage

| Acceptance / finding | How verified |
|----------------------|--------------|
| ER-RB-01 — no stale `tests.yml` | Filesystem assert + architecture test |
| Sole CI authority | `test_workflows_directory_contains_only_canonical_ci` |
| Required `ci.yml` jobs | Job key + display-name markers |
| Supported Python only | Matrix string; no `3.14` in workflow |
| Hard-gate signals | architecture path, ruff, EI cert job, pip-audit |
| ER-RB-05 fingerprint doc | `test_release_candidate_fingerprint_doc_present` |
| EI cert CI wiring unchanged | `TestCiIntegration` |
| No application behaviour change | No `app/` diffs in this WP |

---

## Intentionally not executed here

| Item | Rationale |
|------|-----------|
| Full remote GitHub Actions run on a Version 1 RC tag | Requires push/tag by Release operator; process documented for that step |
| Full `integration` / `production-gates` / `release-build` job wall-clock on Actions | Same — local architecture gate is the WP regression surface; remote green remains claim source for tagged RC |
| Educational / recommendation / UI suites | Out of scope; educational governance frozen |

---

## Engineering fingerprint for this remediation (local)

| Field | Value |
|-------|-------|
| purpose | EI-001.1 engineering controls remediation evidence (not a Version 1 product RC tag) |
| branch | (commit branch at landing) |
| ci_workflow | `.github/workflows/ci.yml` (sole) |
| local_suites | architecture + TestCiIntegration — 2120 passed |
| recorder | Engineering (EI-001.1) |

Formal G11 RC fingerprint (annotated tag + Actions `ci_run_url`) uses `docs/production/RELEASE_CANDIDATE_FINGERPRINT.md` when Release cuts the candidate.

---

**End of EI001_1_TEST_REPORT**
