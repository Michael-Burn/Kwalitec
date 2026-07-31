# RF-001 — Deployment Report

**Programme:** Release Freeze Programme RF-001  
**Date:** 2026-07-31  
**Host:** https://kwalitec.onrender.com  

---

## Verdict

**Production configuration READY.** RF-001 validation build must be cut over via push to `main` + Manual Deploy (Render auto-deploy may remain off, as observed in RC-002).

---

## Dependency verification (Phase 2)

| Check | Result |
|-------|--------|
| Python packages (`requirements.txt`) | **PASS** — Flask 3.1.0, SQLAlchemy 2.0.51, Waitress 3.0.2, psycopg 3.2.13, Alembic 1.18.5 |
| `pip check` (`.venv`) | **PASS** — no broken requirements |
| JavaScript build pipeline | **N/A** — no `package.json` / Vite; first-party assets under `app/static/` |
| Flask entry | **PASS** — `wsgi:app` / `create_app()` |
| Reproduce from clean checkout | **PASS** — `pip install -r requirements.txt` + env vars per `docs/production/ENVIRONMENT.md` |
| Local SQLite Alembic drift | **WARN (local only)** — dogfood SQLite can lag head; production already at `202607300005` |

---

## Production configuration review (Phase 3 — verification only)

| Item | Status | Evidence |
|------|--------|----------|
| Render `render.yaml` | **PASS** | Waitress start; `flask db upgrade` release; `APP_ENV=production`; V2 sole-runtime + commercial loop flags |
| `SECRET_KEY` | **PASS** | `generateValue: true`; factory rejects insecure / short keys under `ProductionConfig` |
| `DATABASE_URL` | **PASS** | From Render DB `kwalitec-db`; live `/health` `database: connected` |
| CSRF | **PASS** | `WTF_CSRF_ENABLED=True` outside tests |
| Session cookies | **PASS** | Secure / HttpOnly / SameSite=Lax in production |
| Static files | **PASS** | Fingerprinted `?v=`; long-cache `SEND_FILE_MAX_AGE_DEFAULT` |
| Logging | **PASS** | Production INFO; no debug logging introduced in PX |
| Health endpoints | **PASS** | `/health`, `/health/live`, `/health/ready` → 200 on live host |
| Alembic | **PASS** | Live migrations `current=head=202607300005` |

No behavioural configuration changes in RF-001.

---

## Pre-cutover live probe (RC-002 tip still serving)

Captured 2026-07-31 before RF-001 push:

| Probe | Result |
|-------|--------|
| `/health` | 200 — `status=ok`, `environment=production`, `version=2.0.0-beta.1` |
| Commit served | `d94d5140878cea4c1cf5216443a0f3f3b08ddbaa` (RC-002 docs tip) |
| Migrations | `202607300005` / `202607300005` |
| DB latency | ~2–12 ms |
| `/auth/login` | 200 (~0.5 s) |
| Static CSS/JS | 200 (fingerprint still `2.0.0-beta.1-rc001` until RF-001 deploy) |

---

## RF-001 deploy sequence

1. Commit UX-001 + PX-001…PX-004 presentation baseline + RF-001 docs + static fingerprint `rf001`.
2. Push to `origin/main`.
3. Manual Deploy on Render service `kwalitec`.
4. Confirm `/health.commit` = RF-001 hash; static `?v=2.0.0-beta.1-rf001`.
5. Re-probe login + health after cutover.

---

## Deployment version record

| Field | Value |
|-------|--------|
| Build identifier | `FV-001` / `2.0.0-beta.1-rf001` |
| Pre-deploy live commit | `d94d514…` |
| RF-001 release commit | `8915930c913d5cd08f19c1ab69fc8a8f6bf37696` |
| Database revision | `202607300005` |
| Runtime | Waitress on Render free plan |

---

## Known non-blockers

- `/health/details` remains public operator JSON (deferred auth gate — RC-002)
- `gunicorn` present in requirements but unused in production start
- Local instance Alembic stamp may lag; does not affect production
