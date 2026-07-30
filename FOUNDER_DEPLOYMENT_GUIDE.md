# Founder Deployment Guide

**Version:** `2.0.0-beta.1`  
**Host:** `https://kwalitec.onrender.com`  
**Programme:** RC-001 — Private Beta Release Candidate

---

## Objective

Deploy a reproducible production baseline for Private Beta. Prefer stability and recoverability over optimisation.

---

## Pre-flight checklist

- [ ] Working tree committed; tag `v2.0.0-beta.1` exists
- [ ] `VERSION`, `pyproject.toml`, and runtime `/health` version agree on `2.0.0-beta.1`
- [ ] Alembic head is `202607300005`
- [ ] Tests + ruff green on the release commit
- [ ] Render service `kwalitec` targets the release commit (manual deploy; auto-deploy may be off)
- [ ] Production env: `APP_ENV=production`, strong `SECRET_KEY`, PostgreSQL `DATABASE_URL`, `ADMIN_EMAIL` / `ADMIN_PASSWORD`
- [ ] Database backup taken (Render PostgreSQL snapshot or logical dump) before upgrade

---

## Environment (Render)

Required:

| Variable | Notes |
|---|---|
| `APP_ENV` | `production` |
| `FLASK_APP` | `wsgi.py` |
| `SECRET_KEY` | Generated / strong; never placeholder |
| `DATABASE_URL` | From `kwalitec-db` |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Bootstrap Founder admin |

Strongly recommended:

| Variable | Notes |
|---|---|
| `TRUSTED_PROXY_HOPS` | `1` |
| `PREFERRED_URL_SCHEME` | `https` |
| `KWALITEC_V2_SOLE_RUNTIME` | `1` (and related V2 flags per `render.yaml`) |
| `KWALITEC_GIT_COMMIT` / Render commit | Fingerprint in `/health` |
| `KWALITEC_SUPPORT_CONTACT` | Student-facing support |

See `docs/production/ENVIRONMENT.md` and `render.yaml`.

---

## Deploy sequence

1. **Backup** production PostgreSQL.
2. **Push** release commit to `origin/main` and push tag `v2.0.0-beta.1`.
3. **Manual Deploy** on Render for service `kwalitec` to the release commit (dashboard or API).
4. Confirm **build** succeeds (`pip install -r requirements.txt`).
5. Confirm **releaseCommand** `flask db upgrade` advances to head `202607300005`.
6. Confirm **start** `waitress-serve --port=$PORT wsgi:app`.
7. Probe health:

```bash
curl -fsS https://kwalitec.onrender.com/health/live
curl -fsS https://kwalitec.onrender.com/health/ready
curl -fsS https://kwalitec.onrender.com/health
```

Expect `version` = `2.0.0-beta.1`, migrations `current` = `head` = `202607300005`, `environment` = `production`.

---

## Post-deploy smoke (must all succeed)

Founder:

1. Founder login → Console Home
2. Create / open subject
3. Upload syllabus + CMP
4. Run certification
5. Publish
6. Open Curriculum Health + Private Beta Dashboard

Student:

1. Student login → onboarding / Begin Learning
2. Generate / open Daily Mission
3. Open Tutor
4. Open Knowledge Map
5. Complete a study session
6. Verify Progress / Journey
7. Submit Private Beta feedback

---

## Database

| Item | Value |
|---|---|
| Head (this RC) | `202607300005` |
| New tables | Generation store (EI-001), private beta participants/feedback/observations (PB-001) |
| Destructive migrations | **None** in this RC chain — additive only |
| Rollback | Prefer restore from backup; `downgrade` only in controlled non-prod rehearsal |

Backup instructions: `docs/production/BACKUP_AND_RECOVERY.md`.

---

## Rollback

1. Redeploy previous known-good commit / tag on Render.
2. If schema must reverse, **restore backup** taken before this deploy.
3. Re-check `/health/ready`.
4. Record incident in Vision Journal / ops notes.

---

## Security reminders

- `DEBUG` must be false in production (`ProductionConfig`)
- CSRF enabled outside tests
- Secure session / remember cookies on HTTPS
- Founder routes admin-gated; student data scoped to owner
- Never commit `.env` or dump secrets into reports

---

## Related

- `docs/production/DEPLOYMENT.md`
- `docs/production/RUNBOOK.md`
- `PRIVATE_BETA_GUIDE.md`
- `RELEASE_NOTES.md`
- `knowledge/engineering/rc001_private_beta_deployment/RC001_RELEASE_REPORT.md`
