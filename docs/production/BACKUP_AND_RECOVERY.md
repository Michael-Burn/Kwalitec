# Backup & Recovery

**Programme:** PR-001

## Backup strategy

| Asset | Method | Cadence | Retention |
|---|---|---|---|
| PostgreSQL primary | Platform automated backups (Render) + pre-migrate manual dump | Continuous / before every migration | ≥ 7 days (prefer 30) |
| Application secrets | Platform secret store (not in git) | On change | Until rotated |
| Curriculum JSON source | Git repository | Continuous | Git history |
| Build artefacts | CI release-build + git tags | Per release | Indefinite tags |

### Manual dump (operator)

```bash
pg_dump "$DATABASE_URL" --format=custom --file="kwalitec-$(date -u +%Y%m%dT%H%M%SZ).dump"
```

Store offline from the production host. Never commit dumps.

## Restore procedure

1. Announce maintenance / disable traffic if needed.
2. Provision a restore target (prefer new database, then cut over).
3. Restore:

   ```bash
   pg_restore --clean --if-exists --no-owner --dbname="$RESTORE_DATABASE_URL" kwalitec-YYYYMMDD.dump
   ```

4. Point `DATABASE_URL` at the restored instance.
5. Verify:

   ```bash
   curl -fsS "$BASE_URL/health/ready"
   flask --app wsgi.py db current
   ```

6. Smoke login (student + founder), create a study plan read, open Console overview.
7. Record restore in the incident log.

## Disaster recovery checklist

- [ ] Latest backup identified and integrity checked
- [ ] Secrets available in secret store
- [ ] DNS / Render service can be retargeted
- [ ] Alembic head known for the restored schema
- [ ] Internal Alpha operators notified
- [ ] Post-restore `/health/ready` green
- [ ] Sample student + console journeys verified

## Recovery verification

| Check | Pass criteria |
|---|---|
| Health | `/health/ready` → 200, `ready: true` |
| Auth | Login with known admin / test user |
| RBAC | Console 200 for Founder; 403 for student |
| Data | Existing study plans / missions visible for test user |
| Curriculum | V1 + V2 curricula loadable |

## Known limitations

- In-process job dead-letter buffer is **not** durable across restarts.
- Education OS (`src/web`) may use a separate database URL when enabled — back up both if dual-running.
