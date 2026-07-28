# EI-001.3 — Test Report

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.3 — Release Operations & Deployment Evidence  
**Date:** 2026-07-28  
**Environment:** Local macOS · Python 3.14.6 (`.venv`) · repo `/Users/kwalitec/Developer/kwalitec`  
**Application behaviour:** Unchanged

---

## 1. Commands executed

```bash
./scripts/dependency_audit.sh

.venv/bin/python -m pytest \
  tests/architecture/ \
  tests/application/educational_intelligence_pipeline/test_health_and_ci.py::TestCiIntegration \
  tests/ga/test_documentation.py \
  tests/ga/test_performance_benchmarks.py \
  tests/ga/test_recovery.py \
  -v --tb=line -q

.venv/bin/ruff check \
  tests/architecture/test_release_operations.py \
  tests/ga/test_documentation.py \
  tests/ga/helpers.py \
  --ignore=F401
```

---

## 2. Outcomes

| Suite | Result |
|-------|--------|
| Dependency audit | Exit 0 — clean (4 ignored HOLDs) |
| Pytest (architecture + CI integration + GA docs/perf/recovery) | **2179 passed**, 8 warnings (pre-existing `utcnow` deprecations) |
| Ruff (changed test paths) | All checks passed |

---

## 3. Gate-linked verification

| Gate evidence | How verified |
|---------------|--------------|
| G7.1 Soft budgets | `tests/ga/test_performance_benchmarks.py` green |
| G7 HOLD artefact integrity | `tests/architecture/test_release_operations.py` |
| G8 / G10 / G12 artefacts | Architecture release-ops tests + GA documentation presence |
| G12 ↔ `render.yaml` / `.env.example` | Architecture tests via `render_env_map()` |
| G10.5 Dependency policy | `./scripts/dependency_audit.sh` |
| Backup / rollback docs | `tests/ga/test_recovery.py` |

---

## 4. Not executed (documented residual)

| Activity | Reason |
|----------|--------|
| Staging/production HTTP operator sample | G7 HOLD — high-traffic claims restricted |
| Live production rollback / restore | Behaviour freeze; tabletop only in `G8_RELIABILITY_EVIDENCE.md` |
| Tagged RC Actions green URL | Release operator / G11 (EI-001.1 process) |

---

## 5. Conclusion

Regression verification required for EI-001.3 operational release evidence **passed**. No application behaviour regressions introduced.

---

**End of EI001_3_TEST_REPORT**
