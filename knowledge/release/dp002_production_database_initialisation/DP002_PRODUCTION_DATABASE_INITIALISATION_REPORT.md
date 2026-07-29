# DP-002 — Production Database Initialisation Report

**Programme:** Production Deployment  
**Phase:** Production Database Initialisation (DATABASE PREPARATION)  
**Date:** 2026-07-29  
**Status:** Documentation only — **no production connection, no deploy, no data import executed**  
**Release freeze tip:** `43cdd46f21d459373eb0489c843fd204f094ebdd`  
(`release(v1.0.0-rc1): freeze commercially certified product`)  
**Certification baseline:** CQ-008B — **COMMERCIAL READY WITH MINOR CONDITIONS**  
**Authorities:** DP-001 / DP-001A, CQ-008B, `docs/production/DEPLOYMENT.md`, `app/services/startup_service.py`, RC-001 `DATABASE_CERTIFICATION.md`

---

## Executive Summary

Production must start from an **empty PostgreSQL database**. The certified application already contains a complete, single-headed Alembic migration chain and an idempotent bootstrap path (schema → Founder/Admin → bundled official curriculum reference rows). No development database, learner history, Studio workspaces, or temporary uploads may be copied into production.

This phase **documents** the reproducible initialisation procedure. It does **not** create a production database, connect to production services, or seed sample users.

**Verdict: READY FOR DP-003.**

---

## Current Schema

### Authority

| Item | Value |
|------|--------|
| ORM | SQLAlchemy via Flask-SQLAlchemy (`app/extensions.py`) |
| Migrations | Flask-Migrate + Alembic under `migrations/` |
| Script count | **51** revisions in `migrations/versions/` |
| Single head | **`202607280080`** (LP-001 learner lifecycle) |
| Production DB | **PostgreSQL only** (`DATABASE_URL` required; SQLite rejected under `ProductionConfig`) |
| Driver normalisation | `postgres://` / `postgresql://` → `postgresql+psycopg://` (`app/config.py`) |

### What the schema covers (complete after `upgrade head`)

The migration chain creates the full commercial schema, including (non-exhaustive):

- **Identity:** `users`, `user_roles`, `user_capabilities`
- **Curriculum reference (V1/V2 tables):** `curricula`, `sections`, `topics`, `learning_objectives`
- **Learning runtime:** study plans, missions, progress, decisions, twin snapshots, recommendation commitments
- **Curriculum Studio / publication:** studio foundation subjects/versions/documents, published curriculum packages
- **Intelligence / evidence / analytics:** CKG, CIP, EI, analytics event/outbox tables, research feedback, founder tooling tables as introduced by post-alpha programmes

### Parallel note (out of Flask-Migrate scope)

A separate Alembic tree exists under `src/infrastructure/persistence/` for Education OS packages. **Production initialisation for the certified commercial Flask app (`wsgi.py` → `app.create_app()`) uses only `migrations/` via `flask db upgrade`.** Do not conflate the two chains for DP-002.

### Orphans / obsolete migrations

- **No multiple heads** at freeze tip — `flask db heads` resolves to a single revision `202607280080`.
- Historical dual-head incidents were merged (e.g. `202607190002_merge_v2_aggregate_heads.py`); no manual SQL patches are required for a greenfield database.
- Filename dates that appear “later” than the head (e.g. `20260907*`, `20261007*`, `20261112*`) sit **below** the merged head in the graph — expected historical shape, not orphaned tips.

---

## Migration Status

| Check | Result |
|-------|--------|
| Chain produces complete schema from empty DB | **Yes** — `flask db upgrade` / Alembic `upgrade head` |
| Historical row data required | **No** |
| Manual SQL patches required | **No** |
| Greenfield stamp needed | **No** — empty DB upgrades from base |
| Idempotent re-run | **Yes** — already-at-head is a no-op |
| Production auto-migrate | `StartupService._apply_migrations()` when `APP_ENV=production` |
| Explicit operator migrate | `APP_ENV=production flask --app wsgi.py db upgrade` |

**Recommended practice:** run **`flask db upgrade` explicitly** in the release/deploy command (e.g. Render `releaseCommand`) so schema application is visible in deploy logs. Treat `StartupService` migration as a safety net, not the sole path.

---

## Bootstrap Requirements

### Persistent data that must exist before first successful Founder login

| # | Requirement | Mechanism | Notes |
|---|-------------|-----------|-------|
| 1 | **Complete schema** at head `202607280080` | `flask db upgrade` | Empty Postgres → full DDL |
| 2 | **Founder/Administrator account** | `flask create-admin` and/or production `StartupService._ensure_admin()` | From `ADMIN_EMAIL` / `ADMIN_PASSWORD`; creates roles + capabilities |
| 3 | **Production env integrity** | Host secrets | `SECRET_KEY` (≥32), `DATABASE_URL`, `APP_ENV=production`, CSRF on |
| 4 | **Bundled official curriculum reference rows** | `StartupService._run_curriculum_import()` on **web** process start | Idempotent import from `app/curriculum/data/**/*.json` — **not** a copy of development SQLite |

### What does *not* need to exist before first login

- Studio subjects / documents / published packages (Founder creates via Console after login)
- Student users (no public registration; provision later via controlled CLI if needed)
- Study plans, missions, sessions, progress, calibration, analytics events
- CKG / CIP extraction artefacts
- Document upload blobs (`DOCUMENT_STORAGE_ROOT` / `instance/curriculum_documents` must start empty)

### RBAC model (no role lookup seed table)

Roles and capabilities are **code-defined** (`app/security/roles.py`, `capabilities.py`, `permissions.py`). Database stores only **assignments** on users (`user_roles`, `user_capabilities`). Bootstrap grants for the admin:

- Roles: Founder + Administrator + Student  
- Capabilities: defaults for those roles (including Console access) via `IdentityService.ensure_founder_admin`

Legacy bridge: `FOUNDER_EMAILS` / `ADMIN_EMAIL` allowlist can sync Founder RBAC on Console access if email matches — keep `ADMIN_EMAIL` consistent with the bootstrap user.

---

## Required Seed Data

**Minimal production seed (allowed):**

1. **Schema** — Alembic head only.  
2. **One operator user** — Founder/Admin from environment credentials.  
3. **Official bundled curricula** — product JSON packages shipped in the release artefact:

   | Path | Purpose |
   |------|---------|
   | `app/curriculum/data/ifoa/cs1/2026.json` | Official CS1 reference |
   | `app/curriculum/data/ifoa/cb2/2026.json` | Official CB2 reference |
   | `app/curriculum/data/ifoa/cm1/2026.json` | Official CM1 reference |
   | `app/curriculum/data/ifoa/cs9/2099.json` | Test/fixture paper in tree — imported if discoverable; treat as product fixture, not learner history |

   Import is **idempotent** (`CurriculumService.import_curricula`) and skips existing `(exam_name, version)` pairs. It populates `curricula` / `sections` / `topics` / `learning_objectives` only.

**Clarification vs “no historical syllabus imports”:**

- **Forbidden:** copying development DB rows, Studio workspaces, published packages, or operator uploads from `instance/`.  
- **Required (product reference):** importing **bundled** official JSON that ships with the certified application. This is application content, not development learner/activity history.  
- **Student catalogue “Ready” subjects** remain empty until Founder publishes via Curriculum Studio — matching RC-001 fresh seed posture (`published_curriculum_packages = 0`).

**No SQL seed scripts** are required beyond migrations + the mechanisms above.

---

## Excluded Data

Do **not** migrate, restore, or seed any of the following from development or RC working databases:

| Class | Examples |
|-------|----------|
| Users (except bootstrap admin) | Students, test accounts, Internal Alpha participants |
| Learner profiles / bindings | `subjects` (per-user), runtime enrolments, SCI bindings |
| Study activity | Study plans, week plans, missions, mission tasks, sessions, attempts, mistakes |
| Progress / twin / decisions | `topic_progress`, twin snapshots, adaptive decisions, recommendation commitments |
| Calibration / assessments | Calibration responses, assessment pipeline artefacts |
| Notifications / analytics | Analytics events, outbox, research feedback submissions |
| Studio / publication history | `studio_foundation_*`, `published_curriculum_packages`, CKG subject graphs built in dev |
| Uploads / files | `instance/curriculum_documents/`, harness DBs, corrupt SQLite backups |
| Dev-only CLI seeds | `flask create-test-user`, demo session composition seeds |
| Local secrets | `.env`, ops `*.local.*`, credential dumps |

**RC-001 certified empty posture** (reference, SQLite RC file — pattern applies to Postgres greenfield):

- `users = 1` (admin only)  
- Studio subjects / documents / published packages / CKG subjects / per-user subjects = **0**

---

## Founder Bootstrap Process

### Credentials

Set in the production host environment (never commit):

```bash
ADMIN_EMAIL=<founder-operator@example.com>
ADMIN_PASSWORD=<strong-unique-secret>
# Optional allowlist bridge (comma-separated); ADMIN_EMAIL is typically sufficient
# FOUNDER_EMAILS=<same-or-additional-founder-emails>
```

### Create admin (idempotent)

```bash
APP_ENV=production flask --app wsgi.py create-admin
```

Behaviour (`app/cli.py` + `AdminBootstrapService`):

- If `users` table missing → warn and exit 0 (run migrations first).  
- If any user exists → **no-op** (does not change passwords).  
- If empty → create admin, hash password, grant Founder/Administrator/Student + capabilities.

### Production startup safety net

When `APP_ENV=production`, `StartupService` also calls `_ensure_admin()` once. Same rules: create only if zero users; **never** sync passwords on boot.

### Password drift (local/dev only — not part of greenfield prod init)

`flask sync-admin` updates password + verifies Founder RBAC for `ADMIN_EMAIL`. Use deliberately for recovery; do **not** treat as the primary production bootstrap path.

### After first login

1. Sign in with `ADMIN_EMAIL` / `ADMIN_PASSWORD`.  
2. Confirm Console / Curriculum Studio access.  
3. Create subjects and publish via the certified Studio pipeline (empty catalogue until then is correct).  
4. Provision learners later through controlled processes (**not** public registration; **not** development `create-test-user` unless Internal Alpha policy explicitly requires it).

---

## Production Initialisation Sequence

Documented procedure for a **brand-new** PostgreSQL database. **Do not execute against production in DP-002.**

```text
1. Provision empty PostgreSQL database
        ↓
2. Set production environment
   APP_ENV=production
   DATABASE_URL=postgresql+psycopg://...
   SECRET_KEY=<≥32 char random>
   ADMIN_EMAIL=...
   ADMIN_PASSWORD=...
   (+ proxy/HTTPS vars as required: TRUSTED_PROXY_HOPS, PREFERRED_URL_SCHEME)
        ↓
3. Deploy release artefact at freeze tip (DP-001A)
   pip install -r requirements.txt
        ↓
4. Alembic upgrade head
   APP_ENV=production flask --app wsgi.py db upgrade
   APP_ENV=production flask --app wsgi.py db current   # expect 202607280080 (head)
        ↓
5. Bootstrap Founder/Admin
   APP_ENV=production flask --app wsgi.py create-admin
        ↓
6. Start WSGI (gunicorn / Render / equivalent) → wsgi:app
   StartupService: migrations no-op; admin no-op; curriculum import runs
        ↓
7. Verify
   /health/live · /health/ready · /health
   Confirm: one admin user; zero Studio publications; curricula reference rows present
        ↓
8. Ready for first Founder login
   (Student catalogue Ready subjects appear only after Studio publish)
```

### Explicit non-steps

| Do not | Why |
|--------|-----|
| Restore `instance/kwalitec.sqlite3` or any dev dump | Imports learner/Studio history |
| Run `flask create-test-user` during init | Seeds non-production identities |
| Copy `instance/curriculum_documents/` | Development uploads |
| Run ad-hoc SQL inserts | Bypasses idempotent bootstrap |
| Point production at SQLite | Rejected by `ProductionConfig` |
| Assume Studio subjects exist | Founder-operated after login |

### Alignment with existing ops docs

Canonical narrative matches `docs/production/DEPLOYMENT.md` (backup → env → upgrade → create-admin → WSGI → health). DP-002 specialises that guide for **greenfield** commercial release: empty Postgres, no legacy restore, curriculum reference via startup import only.

---

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Dual migrate paths (`releaseCommand` + `StartupService`) | Low | Both idempotent; prefer explicit upgrade in deploy logs |
| `ADMIN_EMAIL` ≠ login email / allowlist drift | Medium | Single source of truth for Founder email; verify Console access after create-admin |
| Operators copying local SQLite “to save time” | High | Procedural ban; fresh Postgres only; RC binding rule as precedent |
| Bundled curriculum import misunderstood as “legacy syllabus history” | Medium | Document distinction: product JSON ≠ Studio/dev history |
| `create-test-user` / demo seeds in prod | Medium | Omit from init runbook; gate CLI use by policy |
| Stale checklists citing old Alembic heads (e.g. Internal Alpha docs expecting `202607270013`) | Low | Authoritative head is **`202607280080`** at freeze tip |
| Separate `src/` EOS migrations confused with app chain | Low | Use Flask-Migrate `migrations/` only for commercial `wsgi` app |
| Empty student catalogue mistaken for failure | Low | Expected until Founder publishes |

---

## Recommendation

1. Treat **empty PostgreSQL + `upgrade head` + `create-admin` + first web boot curriculum import** as the sole commercial initialisation path.  
2. Keep Studio publication and learner provisioning **post-login** and out of DB init.  
3. Ban restore/import of any development or RC working databases into production.  
4. Proceed to DP-003 (deployment preparation / execution planning) using this sequence as the database contract.  
5. Carry forward DP-001 residual regression failures as **known CQ-008B minor-condition follow-up**, not as a database-init blocker.

---

## Decision

# READY FOR DP-003

| Success criterion | Met? |
|-------------------|------|
| Brand-new production database (procedure) | **Yes** — empty Postgres prescribed |
| Current schema only | **Yes** — head `202607280080` |
| No legacy learner data | **Yes** — excluded by design |
| No historical syllabus / Studio imports from dev | **Yes** — only bundled product JSON |
| No historical study activity | **Yes** |
| Minimal bootstrap records defined | **Yes** — schema + admin + reference curricula |
| Safe to initialise production | **Yes** — reproducible, idempotent, documented |

**Not performed in DP-002:** production connection, deployment, development DB import, sample user creation.
