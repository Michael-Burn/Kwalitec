# Production Deployment Guide

**Programme:** PR-001 — Production Readiness  
**Audience:** operators deploying the legacy Flask app (`wsgi.py` → `app.create_app()`)

## Prerequisites

- Python 3.11+
- PostgreSQL (required in production — SQLite is rejected when `ProductionConfig` is active)
- Environment secrets provisioned (never commit `.env`)
- Alembic migrations at repository head

## Deploy sequence

1. **Backup** the production database (see [Backup & Recovery](BACKUP_AND_RECOVERY.md)).
2. Set production environment variables (see [Environment Guide](ENVIRONMENT.md)).
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations (or rely on `StartupService` in production):

   ```bash
   APP_ENV=production flask --app wsgi.py db upgrade
   ```

5. Bootstrap the first administrator (idempotent):

   ```bash
   APP_ENV=production flask --app wsgi.py create-admin
   ```

   The admin receives durable **Founder** + **Administrator** roles and Console capability (RBAC).

6. Start the WSGI process (Render / gunicorn / equivalent) pointing at `wsgi:app`.

7. Verify health:

   ```bash
   curl -fsS "$BASE_URL/health/live"
   curl -fsS "$BASE_URL/health/ready"
   curl -fsS "$BASE_URL/health"
   ```

8. Run smoke checks from [Release Protocol](../process/RELEASE_PROTOCOL.md).

## Trusted proxy / HTTPS

Behind Render or another TLS-terminating proxy, set:

```bash
TRUSTED_PROXY_HOPS=1
PREFERRED_URL_SCHEME=https
APP_ENV=production
```

`ProductionConfig` enables secure session/remember cookies and HSTS via security headers.

## Rollback

1. Redeploy the previous release artefact / git tag.
2. If a migration must be reversed, restore from backup first (prefer restore over `downgrade` in production).
3. Confirm `/health/ready` returns 200.

## Related docs

- [Environment Guide](ENVIRONMENT.md)
- [Runbook](RUNBOOK.md)
- [Incident Response](INCIDENT_RESPONSE.md)
- [Release Process](RELEASE_PROCESS.md)
- [Versioning Policy](VERSIONING_POLICY.md)
