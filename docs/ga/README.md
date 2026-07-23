# GA-001 — General Availability Readiness

**Programme:** GA-001  
**Product version under certification:** `2.0.0` (see `VERSION`)  
**Scope:** Operational readiness only — no educational feature work, no Student Experience / Console / Education OS redesigns, no recommendation-logic changes.

## Objective

Prove that Kwalitec is ready for General Availability through validation, verification, resilience testing, and release preparation.

## Workstream index

| # | Workstream | Artefact |
|---|---|---|
| 1 | Release candidate validation | [WORKFLOW_VALIDATION.md](WORKFLOW_VALIDATION.md) |
| 2 | End-to-end testing | `tests/ga/test_e2e_workflows.py` |
| 3 | Load & performance | [PERFORMANCE_BASELINE.md](PERFORMANCE_BASELINE.md), `tests/ga/test_performance_benchmarks.py` |
| 4 | Security review | [SECURITY_REVIEW.md](SECURITY_REVIEW.md), `tests/ga/test_security_review.py` |
| 5 | Failure testing | `tests/ga/test_failure_modes.py` |
| 6 | Recovery testing | `tests/ga/test_recovery.py`, [BACKUP_AND_RECOVERY](../production/BACKUP_AND_RECOVERY.md) |
| 7 | Observability validation | `tests/ga/test_observability.py` |
| 8 | Production documentation | `tests/ga/test_documentation.py`, [docs/production](../production/) |
| 9 | Release checklist | [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) |
| 10 | Version 1.0 / GA certification | [CERTIFICATION_REPORT.md](CERTIFICATION_REPORT.md) |

## How to run GA gates

```bash
python -m pytest tests/ga/ -v --tb=short
ruff check tests/ga/
```

CI `production-gates` includes `tests/ga/` alongside PR-001 and operational suites.

## Related governance

- [`.cursor/RELEASE_CHECKLIST.md`](../../.cursor/RELEASE_CHECKLIST.md)
- [`docs/production/README.md`](../production/README.md)
- [`docs/process/RELEASE_PROTOCOL.md`](../process/RELEASE_PROTOCOL.md)
