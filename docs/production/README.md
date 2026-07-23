# Production Readiness Summary

## Programmes

| Programme | Objective | Status |
|---|---|---|
| **PR-001** | Production deployment readiness (RBAC, config, health, jobs, docs) | Delivered |
| **GA-001** | General Availability certification (validation, E2E, perf, security, failure/recovery, release checklist) | Delivered — see [`docs/ga/`](../ga/README.md) |

## PR-001 workstream status

| # | Workstream | Status |
|---|---|---|
| 1 | Security (RBAC) | Delivered — roles, permissions, guards, helpers, service auth |
| 2 | Identity (capabilities) | Delivered — one identity, multi-portal capabilities |
| 3 | Production configuration | Delivered — validation, cookies, ProxyFix, pool, CSRF audit |
| 4 | Database | Delivered — migration checks, schema audit, pool config |
| 5 | Background services | Delivered — JobRunner retries + dead-letter + structured logs |
| 6 | Observability | Delivered — live/ready/details health, slow requests, alerts |
| 7 | Performance | Delivered — N+1 fixes on dashboard/console hot paths; SQL profiling hook |
| 8 | Accessibility | Delivered — audit notes + base shell skip link / landmarks |
| 9 | CI/CD | Delivered — production-gates job, migration + security steps |
| 10 | Backup & recovery | Delivered — documentation |
| 11 | Documentation | Delivered — `docs/production/*` |
| 12 | Quality gates | Delivered — documented + CI enforced |

## GA-001 artefacts

| Artefact | Path |
|---|---|
| GA index | [`docs/ga/README.md`](../ga/README.md) |
| Deploy checklist | [`docs/ga/RELEASE_CHECKLIST.md`](../ga/RELEASE_CHECKLIST.md) |
| Certification report | [`docs/ga/CERTIFICATION_REPORT.md`](../ga/CERTIFICATION_REPORT.md) |
| Workflow validation | [`docs/ga/WORKFLOW_VALIDATION.md`](../ga/WORKFLOW_VALIDATION.md) |
| Security review | [`docs/ga/SECURITY_REVIEW.md`](../ga/SECURITY_REVIEW.md) |
| Performance baseline | [`docs/ga/PERFORMANCE_BASELINE.md`](../ga/PERFORMANCE_BASELINE.md) |
| Automated gates | `tests/ga/` |

## Remaining blockers

See [GA certification § Remaining GA blockers](../ga/CERTIFICATION_REPORT.md#remaining-ga-blockers) — primarily staging health, backup/restore drill, and dependency-scan review (operator gates).
