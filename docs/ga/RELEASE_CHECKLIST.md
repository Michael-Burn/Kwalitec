# GA Deployment Release Checklist

**Programme:** GA-001  
**Audience:** operators performing a production deploy  
**Companion:** [`.cursor/RELEASE_CHECKLIST.md`](../../.cursor/RELEASE_CHECKLIST.md), [RELEASE_PROCESS.md](../production/RELEASE_PROCESS.md)

Every production deployment must verify all sections below. Mark each item only with evidence (command output, health JSON, or operator sign-off).

---

## Configuration

- [ ] `APP_ENV=production`
- [ ] `SECRET_KEY` is unique, ≥ 32 characters, not a documented default
- [ ] `DATABASE_URL` points at PostgreSQL (psycopg v3)
- [ ] `TRUSTED_PROXY_HOPS` / `PREFERRED_URL_SCHEME=https` set behind TLS terminator
- [ ] Alpha / V2 flags match the intended dual-run or sole-runtime posture
- [ ] No secrets committed; `.env` absent from the release artefact

## Database

- [ ] Pre-deploy backup completed ([BACKUP_AND_RECOVERY.md](../production/BACKUP_AND_RECOVERY.md))
- [ ] `flask --app wsgi.py db current` matches Alembic head
- [ ] `flask --app wsgi.py db upgrade` applied on staging first, then production
- [ ] Schema audit reviewed if this release includes migrations

## Health

- [ ] `GET /health/live` → 200, `status: ok`
- [ ] `GET /health/ready` → 200, `ready: true`
- [ ] `GET /health` → 200, database connected
- [ ] `GET /health/details` → no unexpected `dead_letters`; alerts thresholds present
- [ ] Health JSON `version` / `commit` match the tagged release

## Telemetry

- [ ] Correlation IDs echoed (`X-Correlation-ID` / `X-Request-ID`)
- [ ] Structured `http_request` logs visible for a smoke request
- [ ] Platform Intelligence (`/console/alpha-observability`) loads for a Founder identity
- [ ] Error pages show a Reference ID (spot-check a 404)

## Background jobs

- [ ] JobRunner dead-letter buffer empty or reviewed after smoke automation
- [ ] Operators understand dead letters are **in-process** (not durable across restart)
- [ ] Manual automation / founder workflows exercised if this release touches them

## Console

- [ ] Founder / Administrator login succeeds
- [ ] `/console/` returns 200
- [ ] Operational health and Platform Intelligence surfaces load
- [ ] Student identity without Console capability receives 403 on `/console/`

## Student portal

- [ ] Student login succeeds
- [ ] `/student/` home loads
- [ ] Journey, revision planner, and session overview load
- [ ] Support help (`/alpha/help`) and Settings export path reachable
- [ ] Mission list / study-plan list load without 5xx

## Rollback

- [ ] Previous release tag / artefact identified before deploy
- [ ] Rollback procedure understood: redeploy prior artefact; prefer DB restore over `downgrade`
- [ ] Post-rollback `/health/ready` verification planned
- [ ] Incident channel / on-call notified for high-risk deploys

---

## Stop conditions

**Do not proceed** if any of the following is true:

- Architecture or GA pytest gates red
- `/health/ready` not green on staging
- Unreviewed migration on production
- Secrets detected in the release diff
- Open P0 security finding without waiver

---

## Sign-off

| Role | Name | Date | Evidence |
|---|---|---|---|
| Deploy operator | | | |
| Founder / release owner | | | |
