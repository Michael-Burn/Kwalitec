# DEPLOYMENT_CHECKLIST.md

**Programme:** VERSION1-RC2 — Release Stabilization Sprint  
**Date:** 2026-08-01  
**Target:** https://kwalitec.onrender.com (Render service `kwalitec`)  
**Authority:** `render.yaml`, `docs/production/ENVIRONMENT.md`, `knowledge/archive/releases/v2_0_0_beta_1/release/FOUNDER_DEPLOYMENT_GUIDE.md`, RR-001 verification  
**Status:** Checklist for the **next** intended tip — current LIVE is healthy but **not** RC-clean (RR-001 NO-GO)

---

## A. Pre-deploy repository gates

| # | Check | Owner | Status now | Required before GO |
|---|-------|-------|------------|--------------------|
| A1 | Working tree clean for release set | Release Eng | **FAIL** | Yes |
| A2 | Intended educational inventory committed | Release Eng | **FAIL** | Yes |
| A3 | Intended tip pushed to `origin/main` | Release Eng | **FAIL** (`f066bcf` unpushed; inventory uncommitted) | Yes |
| A4 | Immutable git tag created for RC tip | Release Eng | **FAIL** (no new tag) | Yes |
| A5 | `VERSION` / `pyproject.toml` / `APP_VERSION` agree | Release Eng | PASS at `2.0.0-beta.1` (decide if bump for RC2) | Yes |
| A6 | `flask db heads` single expected head | Release Eng | PASS (`202607310002`) | Yes |
| A7 | pytest + ruff green on tip | Release Eng | **Not re-run this sprint** | Yes |
| A8 | CHANGELOG entry for this RC | Release Eng | Missing for post-`2.0.0-beta.1` tip | Yes |

---

## B. Render service configuration

| # | Check | Expected | Evidence / notes | Status |
|---|-------|----------|------------------|--------|
| B1 | Service name | `kwalitec` | `render.yaml` | Configured |
| B2 | Runtime | Python | `env: python` | Configured |
| B3 | `buildCommand` | `pip install -r requirements.txt` | `render.yaml` | Configured |
| B4 | `releaseCommand` | `flask db upgrade` | `render.yaml` | Configured |
| B5 | `startCommand` | `waitress-serve --port=$PORT wsgi:app` | `render.yaml`; waitress in requirements | Configured |
| B6 | Plan | `free` (blueprint) | Confirm dashboard still matches | Verify on deploy |
| B7 | Auto-deploy | Often off; prefer **manual deploy** of tagged commit | Founder Deployment Guide | Operator action |
| B8 | Deploy API/hook in operator env | Optional | RR-001: absent in `.env` | Manual dashboard |

---

## C. Database

| # | Check | Expected | Status |
|---|-------|----------|--------|
| C1 | Database service | `kwalitec-db` | Blueprint present |
| C2 | `DATABASE_URL` wired | fromDatabase connectionString | Blueprint present |
| C3 | Pre-deploy backup / snapshot | Taken before schema-touching deploy | **Operator** — required if migrations change (none in dirty tree) |
| C4 | Post-deploy migration fingerprint | `/health` migrations `current == head == 202607310002` (or new head if added) | LIVE PASS at RR-001 for current tip |
| C5 | No destructive migrations in RC tip | Additive / merge only preferred | Confirm on tip review |

---

## D. Environment variables

### Required (production)

| Variable | Required | Blueprint / docs | Dashboard verify |
|----------|----------|------------------|------------------|
| `APP_ENV` | Yes | `production` | ☐ |
| `FLASK_APP` | Yes | `wsgi.py` | ☐ |
| `SECRET_KEY` | Yes | generateValue / strong | ☐ non-placeholder |
| `DATABASE_URL` | Yes | from DB | ☐ |
| `ADMIN_EMAIL` | Yes | sync:false | ☐ set |
| `ADMIN_PASSWORD` | Yes | sync:false | ☐ set |

### Strongly recommended

| Variable | Purpose | Dashboard verify |
|----------|---------|------------------|
| `APP_URL` | Canonical origin | ☐ |
| `PREFERRED_URL_SCHEME` | `https` | ☐ |
| `TRUSTED_PROXY_HOPS` | `1` | ☐ |
| `KWALITEC_GIT_COMMIT` / `RENDER_GIT_COMMIT` | Health fingerprint | ☐ (LIVE commit present; `build_number` was `local`) |
| `KWALITEC_BUILD_NUMBER` / `KWALITEC_BUILD_DATE` | Operator metadata | ☐ improve vs `local` |
| `KWALITEC_SUPPORT_CONTACT` | Support UX | ☐ |

### Educational / runtime flags (blueprint defaults)

| Variable | Blueprint | Notes |
|----------|-----------|-------|
| `KWALITEC_V2_STUDENT_EXPERIENCE` | `1` | ☐ |
| `KWALITEC_V2_DURABLE_STORE` | `1` | ☐ |
| `KWALITEC_V2_INJECT_ENGINES` | `1` | ☐ |
| `KWALITEC_V2_SEED_DEMO` | `0` | ☐ keep off in prod |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | `1` | ☐ |
| `KWALITEC_V2_SOLE_RUNTIME` | `1` | ☐ sole student runtime |
| `KWALITEC_COMMERCIAL_LOOP` | `1` | ☐ |
| `KWALITEC_EI_INTERNAL_ALPHA` | `1` | ☐ Internal Alpha — not public marketing |

Reference: `docs/production/ENVIRONMENT.md`, `docs/production/VERSION_1_FLAG_MATRIX.md`.

---

## E. Health endpoints (post-deploy)

| # | Probe | Expect | RR-001 on `613722c` |
|---|-------|--------|---------------------|
| E1 | `GET /health/live` | 200, `status=ok`, commit = deployed SHA | PASS |
| E2 | `GET /health/ready` | 200, `ready=true`, migrations ok | PASS |
| E3 | `GET /health` | 200, `environment=production`, DB connected | PASS |
| E4 | Commit match | `/health.commit` == intended tag tip | **FAIL** vs local intended tip |
| E5 | Version match | `/health.version` == `VERSION` | PASS (`2.0.0-beta.1`) |

---

## F. Startup / release command verification

| # | Step | How to verify | Required |
|---|------|---------------|----------|
| F1 | Build succeeds | Render build logs: pip install OK | Yes |
| F2 | Release command runs | Logs show `flask db upgrade` OK | Yes |
| F3 | Waitress starts | Service live; health 200 | Yes |
| F4 | No crash loop | Stable instance | Yes |

---

## G. Post-deploy smoke (minimum)

| # | Persona | Steps | Required before GO |
|---|---------|-------|--------------------|
| G1 | Founder | Login → experience → console home → curriculum health | Yes |
| G2 | Student | Login → home → Today's Mission → session overview → **start** → **complete** | Yes |
| G3 | Auth | Logout (CSRF POST) returns Sign in | Yes |
| G4 | Inventory | Deployed educational inventory matches release manifest | Yes |

Detail template: `RR001_LIVE_SMOKE_REPORT.md` (re-run on new tip).

---

## H. Rollback

| # | Action | Notes |
|---|--------|-------|
| H1 | Redeploy previous known-good commit/tag on Render | Prefer tagged tip (e.g. last GO fingerprint) |
| H2 | If schema advanced incompatibly | Restore DB snapshot taken in C3 — do not casual `downgrade` on prod |
| H3 | Re-check `/health/ready` | Confirm fingerprint + migrations |
| H4 | Record incident | Ops notes / Vision Journal |

---

## I. Deployment readiness conclusion

| Question | Answer |
|----------|--------|
| Is Render blueprint coherent? | **Yes** |
| Is current LIVE process-healthy? | **Yes** (RR-001) |
| Is deployment of an RC tip ready to execute? | **No** — repository gates A1–A4 open |
| Blocking gap | Clean tip with inventory → push → manual deploy → fingerprint + smoke |

See `RC2_RELEASE_ACTION_PLAN.md`.
