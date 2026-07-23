# Production Runbook

**Programme:** PR-001

## Daily checks

1. `GET /health/ready` → `ready: true`
2. `GET /health/details` → review `dead_letters` and component latencies
3. Confirm no elevated 5xx rate in platform logs (`kwalitec.observability`)
4. Confirm Alembic head matches deploy (`components.migrations`)

## Common operations

### Create Internal Alpha student

```bash
flask --app wsgi.py create-test-user
```

Grants `student` role + `student_portal` capability.

### Create / refresh bootstrap admin

```bash
flask --app wsgi.py create-admin
```

No-op if any user already exists. New admins receive Founder RBAC.

### Apply migrations manually

```bash
APP_ENV=production flask --app wsgi.py db upgrade
flask --app wsgi.py db current   # expect head
```

### Schema audit (indexes / FKs / constraints)

In a Flask shell:

```python
from app.services.database_readiness_service import DatabaseReadinessService
print(DatabaseReadinessService.migration_status().to_dict())
print(DatabaseReadinessService.schema_audit().to_dict())
```

### Run automation with retries

```python
from app.automation.services.automation_service import AutomationService
AutomationService().run_with_retries("founder_internal_alpha")
```

Failures after retries are recorded in the in-process dead-letter buffer (visible on `/health/details`).

## Console operations

- Console requires `console` capability + `console.access` (Founder/Administrator/staff roles).
- Legacy `ADMIN_EMAIL` ∪ `FOUNDER_EMAILS` still grants access and syncs Founder role once.
- Prefer assigning durable roles over expanding the email allowlist.

See also [Console Operations](CONSOLE_OPERATIONS.md).

## Alerts

| Signal | Threshold | Action |
|---|---|---|
| `/health/ready` ≠ 200 | immediate | Check DB + migrations |
| `slow_request` logs | ≥ `SLOW_REQUEST_THRESHOLD_MS` | Profile with `PROFILE_SQL=1` |
| DB latency degraded | ≥ `HEALTH_ALERT_DB_LATENCY_MS` | Check pool / Postgres |
| Dead letters present | any | Inspect `/health/details`, re-run job |
