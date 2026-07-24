# Internal Alpha Launch Checklist (ARP-005)

**Authority:** Operational (Internal Alpha readiness)  
**Status:** Superseded for production by **V2-023 RC-1** sole-runtime activation  
**Scope:** Local dual-run soak remains available; production Render runs sole runtime.  
**Related:** [`V2_023_RELEASE_CANDIDATE.md`](../../docs/architecture/V2_023_RELEASE_CANDIDATE.md) · [`V2_020_RETIREMENT_RUNBOOK.md`](V2_020_RETIREMENT_RUNBOOK.md) · [`ALPHA_WORKFLOW_VALIDATION.md`](ALPHA_WORKFLOW_VALIDATION.md)

Internal Alpha originally meant **trusted operators and invited learners** exercise Version 2 beside Version 1. **V2-023** promotes the Education Operating System as the sole production student runtime via `KWALITEC_V2_SOLE_RUNTIME=1` on Render.

---

## Alpha / RC posture

| Concern | Local dual-run (soak / rollback) | Production RC-1 (Render) |
|---------|----------------------------------|---------------------------|
| Home (`/`) | Version 1 dashboard (`dashboard.index`) | Student Dashboard (`student.home`) |
| Student path | `/student` when dual-run flags on | Default home |
| Session path | `/session/...` | Only live session UX |
| Sole runtime | **Off** unless explicitly set | **On** (`KWALITEC_V2_SOLE_RUNTIME=1`) |
| Persistence | Durable SQLAlchemy stores when `KWALITEC_V2_DURABLE_STORE=1` | Same |
| Evidence gates | Surfaced at `/founder/evidence-gates` | Product evidence still operator-recorded |

---

## 1. Deployment checklist

Complete before inviting the alpha cohort.

### 1.1 Environment and secrets

| # | Check | How |
|---|--------|-----|
| D1 | `SECRET_KEY` is a strong random value (not a placeholder) | Host env / Render dashboard |
| D2 | `ADMIN_EMAIL` / `ADMIN_PASSWORD` set for bootstrap only; not logged | Host env |
| D3 | `DATABASE_URL` points at production Postgres | Host env / `render.yaml` |
| D4 | `APP_ENV=production` (or equivalent ProductionConfig selection) | Host env |
| D5 | `.env` is **not** committed; secrets never appear in git | `git status` / repo hygiene |
| D6 | Production flags match Render defaults (below) | Compare host env ↔ `render.yaml` |

**Production RC-1 environment (Render):**

```bash
KWALITEC_V2_STUDENT_EXPERIENCE=1
KWALITEC_V2_DURABLE_STORE=1
KWALITEC_V2_INJECT_ENGINES=1
KWALITEC_V2_SEED_DEMO=0
KWALITEC_V2_FOUNDER_INTELLIGENCE=1
KWALITEC_V2_SOLE_RUNTIME=1
```

**Local dual-run soak (optional — sole runtime off):**

```bash
KWALITEC_V2_STUDENT_EXPERIENCE=1
KWALITEC_V2_DURABLE_STORE=1
KWALITEC_V2_INJECT_ENGINES=1
KWALITEC_V2_SEED_DEMO=0
KWALITEC_V2_FOUNDER_INTELLIGENCE=1
# Leave KWALITEC_V2_SOLE_RUNTIME unset for dual-run soak
```

Optional (separate from V2): `KWALITEC_EI_INTERNAL_ALPHA=1` enables the V1 Educational Intelligence dashboard card only.

Documented in [`.env.example`](../../.env.example); production defaults in [`render.yaml`](../../render.yaml).

### 1.2 Database

| # | Check | How |
|---|--------|-----|
| D7 | Backup Postgres before upgrade | Provider snapshot / `pg_dump` |
| D8 | `flask db upgrade` to Alembic head | Head must be `202607230002` |
| D9 | V2 aggregate tables exist | `v2_aggregate_documents`, `v2_aggregate_snapshots`, `v2_evidence_events` |
| D10 | Startup log shows Alembic current == head | Look for `Alembic: database is up to date.` |

```bash
flask db upgrade
flask db current   # expect 202607230002 (head)
```

### 1.3 Application startup

| # | Check | How |
|---|--------|-----|
| D11 | Process starts without traceback | Deploy logs / `waitress-serve … wsgi:app` |
| D12 | Logging configured at INFO (production) | Startup: `Kwalitec logging configured at level INFO` |
| D13 | Config validation accepts production `SECRET_KEY` | No `CONFIGURATION ERROR` / no abort |
| D14 | Curriculum import idempotent (V1 + V2 loadable) | Startup curriculum log: imported/skipped, no fatal errors |
| D15 | Blueprints registered | `auth`, `dashboard`, `student`, `session`, `curriculum_studio`, `founder_dashboard`, … |
| D16 | `GET /health` returns `status: ok`, `database: connected` | HTTP smoke |
| D17 | `GET /` → `/student/` when sole runtime on; `/dashboard/` when off | HTTP smoke |
| D18 | Static assets resolve (session CSS, founder CSS) | Browser network / curl versioned URLs |
| D19 | 403 / 404 / 500 templates render | Hit a protected/missing path; no bare Werkzeug HTML in prod |
| D20 | Founder Intelligence dual-run label = `sole-runtime-v2` (RC) or `dual-run-active` (soak) | `/founder/intelligence` |

### 1.4 Feature-flag / behaviour alignment

| Flag | Application behaviour |
|------|------------------------|
| `KWALITEC_V2_STUDENT_EXPERIENCE` | Enables Student Experience surfaces |
| `KWALITEC_V2_DURABLE_STORE` | Experience/Session stores use SQLAlchemy; implies engine injection |
| `KWALITEC_V2_INJECT_ENGINES` | Opaque Phase I bridges wired into adapters |
| `KWALITEC_V2_SEED_DEMO` | Explicit override; defaults **off** when durable is on |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | Founder Intelligence surface enablement |
| `KWALITEC_V2_SOLE_RUNTIME` | `/` → Student Home; legacy list + nested LXP session routes redirect |

Resolver: `app/application/config/v2_flags.py` → `resolve_v2_feature_flags()`.

---

## Rollback

1. Unset `KWALITEC_V2_SOLE_RUNTIME` (or set to `0`) on the host / Render.
2. Redeploy / restart.
3. Confirm `/` redirects to Version 1 `/dashboard/`.
4. Leave durable V2 tables intact (do not drop).

See also [`V2_020_RETIREMENT_RUNBOOK.md`](V2_020_RETIREMENT_RUNBOOK.md) § Rollback.

---

## 2. Smoke test checklist

Run after deploy. Prefer an admin/founder account plus one learner account.

### 2.1 Founder workflow

| # | Step | Path / action | Pass criteria |
|---|------|---------------|---------------|
| F1 | Create curriculum | `/founder/studio/` → create subject / workspace | Workspace appears on Studio dashboard |
| F2 | Validate | Workspace → Validate | Success flash; stage advances |
| F3 | Preview | Workspace → Preview | Preview succeeds; version-label guidance visible |
| F4 | Approve | Workspace → Approve (with version label) | Approval succeeds |
| F5 | Publish | Workspace → Publish | “Curriculum published successfully.” (or equivalent) |
| F6 | Version history | Workspace version history section | Labels visible; empty state guided if none |
| F7 | Founder Intelligence | `/founder/intelligence` | Page 200; advisory notes; dual-run label shown |
| F8 | Evidence Gates | `/founder/evidence-gates` | Six gates listed; product evidence not auto-passed |

Primary Founder nav must show **Studio**, **Intelligence**, and **Evidence Gates**.

### 2.2 Student workflow

| # | Step | Path / action | Pass criteria |
|---|------|---------------|---------------|
| S1 | Student Home | `/student/` | Home renders; Start Session CTA present when ready |
| S2 | Journey | `/student/journey` | Journey surface renders without kernel jargon |
| S3 | Learning Insights | `/student/revision` (product: Learning Insights) | Insights / revision surface renders |
| S4 | Start Session | Home → Start Session | Lands on session Overview |
| S5 | Resume Session | Leave mid-session → re-enter | Resumes active surface (no Overview rewind) |
| S6 | Reflection | Advance to Reflection | Reflection card renders |
| S7 | Session Summary | Advance to Summary | Summary renders |
| S8 | Completion | Complete → Return Home | Finish success; return to Student Home |

Dual-run chrome: Student shell shows **Back to Dashboard** while sole runtime is off.

### 2.3 Automated operational suite

```bash
python3 -m pytest tests/operational/ -q
```

Target: configuration, startup, flags, blueprint registration, and HTTP smoke for alpha surfaces (see § Tests Executed in the ARP-005 completion report when committed).

---

## 3. Rollback checklist

Internal Alpha rollback restores Version 1 as the only learner home and stops dual-run traffic. It does **not** drop V2 tables.

### 3.1 Soft rollback (recommended first)

| # | Action | Verify |
|---|--------|--------|
| R1 | Unset or set to `0`: `KWALITEC_V2_STUDENT_EXPERIENCE` | Dashboard dual-run CTA gone |
| R2 | Optionally leave durable store on (data preserved) or set `KWALITEC_V2_DURABLE_STORE=0` | App still starts; V1 unaffected |
| R3 | Confirm `KWALITEC_V2_SOLE_RUNTIME` is unset | `/` → `/dashboard/` |
| R4 | Redeploy / restart | `/health` ok; no startup traceback |
| R5 | Spot-check V1 dashboard, missions, study plan | Core V1 journey works |

### 3.2 If sole runtime was enabled accidentally

Follow [`V2_020_RETIREMENT_RUNBOOK.md`](V2_020_RETIREMENT_RUNBOOK.md) § Rollback:

1. Unset `KWALITEC_V2_SOLE_RUNTIME`
2. Restart
3. Confirm `/` → Version 1 dashboard
4. **Do not drop** V2 aggregate tables

### 3.3 Database rollback

- Prefer **forward fix** (`flask db upgrade`) over downgrade for alpha.
- If a schema rollback is unavoidable, restore from the pre-upgrade Postgres backup (D7). Do not invent destructive Alembic downgrades during alpha.

---

## 4. Operational readiness (live)

| Signal | Expectation |
|--------|-------------|
| Application logs | INFO startup lines; request errors logged with path |
| Warnings | Expected: Alembic-behind only **before** upgrade; insecure SECRET_KEY only in non-production |
| Tracebacks | None on happy-path Founder/Student flows |
| Assets | No 404 for `session.css` / `founder_dashboard.css` |
| Templates | No `TemplateNotFound` |
| Health | `/health` → `ok` / `connected` |

---

## 5. Known limitations (accepted for Internal Alpha / RC soak)

### Intentionally deferred

- Full deletion of legacy dashboard / analytics / LXP templates (kept as redirect shells for soak + rollback)
- Analytics chart parity: Twin History vs V1 `/analytics/` charts
- Public / open registration and broad cohort marketing
- Dedicated Content Sources upload UI in Studio (stage still advances; upload remains port-level)
- Labelled “Resume Session” Home CTA (resume works via workspace redirect)
- Deep unification of Experience Twin projections with durable TwinSnapshot ORM history
- Full Phase I method surface behind every opaque bridge (bridges fall back safely)

### Technical debt accepted

- Opaque engine bridges are projection bridges, not complete educational facades for every context
- Studio UI covers dashboard + workspace actions; richer source/blueprint UX may follow alpha feedback
- Product Strategy **product_evidence** gate cannot auto-pass from code — requires real observation
- Cosmetic `datetime.utcnow` deprecation warnings on some ORM defaults
- `StudySessionService` retained for dual-run rollback; not deleted under V2-023

### Operational caveats

- Enabling durable flags **without** `flask db upgrade` to `202607230002` will fail writes
- `/student` routes remain registered even when the student flag is off; the flag mainly gates entry CTA and dual-run chrome
- Session create-on-open binds unbound `session_id`s to the current user; foreign workspaces return 403
- Production RC enables sole runtime; local soak may leave it unset

---

## 6. Success criteria

Internal Alpha / RC-1 is ready when **all** of the following are true:

1. Deployment checklist §1 complete (secrets, flags, migrations, health)
2. Automated operational tests in `tests/operational/` pass
3. Founder smoke §2.1 pass (create → publish, Intelligence, Evidence Gates)
4. Student smoke §2.2 pass (home → session → complete, including resume)
5. Rollback path § Rollback / §3 understood and verified in staging (or documented dry-run)
6. Operators know limitations §5

When the above hold, mark:

> **RC-1 ready** — Education Operating System sole runtime on production; dual-run available for local soak / rollback.

Cutover programme: [`V2_020_RETIREMENT_RUNBOOK.md`](V2_020_RETIREMENT_RUNBOOK.md) · [`V2_023_RELEASE_CANDIDATE.md`](../../docs/architecture/V2_023_RELEASE_CANDIDATE.md).

---

## 7. Quick reference — endpoints

| Surface | URL |
|---------|-----|
| Health | `GET /health` |
| Home (sole on) | `GET /` → `/student/` |
| Home (sole off) | `GET /` → `/dashboard/` |
| Student Dashboard | `/student/` |
| Journey | `/student/journey` |
| Revision | `/student/revision` |
| Analytics | `/student/history` |
| Session | `/session/<id>/overview` … `/complete` |
| Curriculum Studio | `/founder/studio/` |
| Founder Intelligence | `/founder/intelligence` |
| Evidence Gates | `/founder/evidence-gates` |
