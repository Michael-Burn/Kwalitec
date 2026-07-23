# Incident Response

**Programme:** PR-001

## Severity

| Level | Example | Response |
|---|---|---|
| SEV-1 | Site down, data loss risk, auth bypass | Page on-call; freeze deploys; restore from backup if needed |
| SEV-2 | Console/student partial outage, elevated 5xx | Mitigate; hotfix or rollback |
| SEV-3 | Degraded latency, non-critical job failures | Schedule fix; document |

## Immediate checklist

1. Capture correlation IDs from error pages / `X-Correlation-ID`.
2. Check `/health/live`, `/health/ready`, `/health/details`.
3. Confirm last deploy fingerprint (`commit` / `build_number` in health JSON).
4. Search logs for `presentation_error`, `slow_request`, `job_dead_letter`, `CONFIGURATION ERROR`.
5. If schema-related: do **not** run ad-hoc DDL — use Alembic; prefer restore for destructive mistakes.
6. Communicate status to Internal Alpha operators.

## Security incidents

1. Rotate `SECRET_KEY` only with planned session invalidation.
2. Rotate `ADMIN_PASSWORD` / user passwords as needed.
3. Revoke compromised roles via `user_roles` / `user_capabilities` (IdentityService).
4. Preserve logs; do not wipe evidence.

## Post-incident

1. Timeline, root cause, blast radius.
2. Follow-ups in the next release notes.
3. Update this runbook if a new failure mode appeared.
