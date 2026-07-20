# Internal Alpha Launch Checklist (ARP-005)

**Authority:** Operational (Internal Alpha readiness)  
**Status:** Ready for Internal Alpha dual-run  
**Scope:** Deploy, exercise, observe, and roll back Version 2 coexistence — **no new features**.  
**Related:** [`ALPHA_WORKFLOW_VALIDATION.md`](ALPHA_WORKFLOW_VALIDATION.md) · [`ALPHA_READINESS_FOUNDER_UX.md`](ALPHA_READINESS_FOUNDER_UX.md) · [`V2_020_RETIREMENT_RUNBOOK.md`](V2_020_RETIREMENT_RUNBOOK.md) · [`V2_DEPLOY_IMPLEMENTATION_REPORT.md`](../releases/V2_DEPLOY_IMPLEMENTATION_REPORT.md)

Internal Alpha means **trusted operators and invited learners** exercise Version 2 beside Version 1. It does **not** mean Version 1 retirement or public launch.

---

## Alpha posture (confirmed)

| Concern | Expected Internal Alpha posture |
|---------|----------------------------------|
| Home (`/`) | Version 1 dashboard (`dashboard.index`) |
| Student path | Available at `/student` when dual-run flags are on |
| Session path | Available at `/session/...` |
| Sole runtime | **Off** — do not set `KWALITEC_V2_SOLE_RUNTIME` |
| Persistence | Durable SQLAlchemy stores when `KWALITEC_V2_DURABLE_STORE=1` |
| Evidence gates | Surfaced at `/founder/evidence-gates`; product evidence still open |

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
| D6 | Dual-run flags match Render defaults (below) | Compare host env ↔ `render.yaml` |

**Required dual-run environment (Internal Alpha):**

```bash
KWALITEC_V2_STUDENT_EXPERIENCE=1
KWALITEC_V2_DURABLE_STORE=1
KWALITEC_V2_INJECT_ENGINES=1
KWALITEC_V2_SEED_DEMO=0
KWALITEC_V2_FOUNDER_INTELLIGENCE=1
# Do NOT set KWALITEC_V2_SOLE_RUNTIME
```

Optional (separate from V2): `KWALITEC_EI_INTERNAL_ALPHA=1` enables the V1 Educational Intelligence dashboard card only.

Documented in [`.env.example`](../../.env.example); production defaults sketched in [`render.yaml`](../../render.yaml).

### 1.2 Database

| # | Check | How |
|---|--------|-----|
| D7 | Backup Postgres before upgrade | Provider snapshot / `pg_dump` |
| D8 | `flask db upgrade` to Alembic head | Head must be `202607190002` |
| D9 | V2 aggregate tables exist | `v2_aggregate_documents`, `v2_aggregate_snapshots`, `v2_evidence_events` |
| D10 | Startup log shows Alembic current == head | Look for `Alembic: database is up to date.` |

```bash
flask db upgrade
flask db current   # expect 202607190002 (head)
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
| D17 | `GET /` redirects to `/dashboard/` (sole runtime off) | HTTP smoke |
| D18 | Static assets resolve (session CSS, founder CSS) | Browser network / curl versioned URLs |
| D19 | 403 / 404 / 500 templates render | Hit a protected/missing path; no bare Werkzeug HTML in prod |
| D20 | Founder Intelligence dual-run label = `dual-run-active` | `/founder/intelligence` |

### 1.4 Feature-flag / behaviour alignment

| Flag | Application behaviour |
|------|------------------------|
| `KWALITEC_V2_STUDENT_EXPERIENCE` | Dashboard dual-run CTA; Student shell “Back to Dashboard” when sole runtime off |
| `KWALITEC_V2_DURABLE_STORE` | Experience/Session stores use SQLAlchemy; implies engine injection |
| `KWALITEC_V2_INJECT_ENGINES` | Opaque Phase I bridges wired into adapters |
| `KWALITEC_V2_SEED_DEMO` | Explicit override; defaults **off** when durable is on |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | Founder Intelligence surface enablement |
| `KWALITEC_V2_SOLE_RUNTIME` | `/` → Student Home — **forbidden for Internal Alpha** |

Resolver: `app/application/config/v2_flags.py` → `resolve_v2_feature_flags()`.

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

## 5. Known limitations (accepted for Internal Alpha)

### Intentionally deferred

- Version 1 sole-runtime retirement (`KWALITEC_V2_SOLE_RUNTIME`) — gated on ADR-007 product evidence
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

### Operational caveats

- Enabling durable flags **without** `flask db upgrade` to `202607190002` will fail writes
- `/student` routes remain registered even when the student flag is off; the flag mainly gates entry CTA and dual-run chrome
- Session create-on-open binds unbound `session_id`s to the current user; foreign workspaces return 403
- Internal Alpha is **not** educational proof that Version 2 outperforms Version 1

---

## 6. Success criteria

Internal Alpha is ready when **all** of the following are true:

1. Deployment checklist §1 complete (secrets, flags, migrations, health, sole runtime off)
2. Automated operational tests in `tests/operational/` pass
3. Founder smoke §2.1 pass (create → publish, Intelligence, Evidence Gates)
4. Student smoke §2.2 pass (home → session → complete, including resume)
5. Rollback path §3 understood and soft-rollback verified in staging (or documented dry-run)
6. Operators know limitations §5 and will not enable sole runtime until evidence gates pass

When the above hold, mark:

> **Internal Alpha ready** — dual-run coexistence for invited operators and learners.

Sole-runtime cutover remains a **separate** programme under [`V2_020_RETIREMENT_RUNBOOK.md`](V2_020_RETIREMENT_RUNBOOK.md).

---

## 7. Quick reference — endpoints

| Surface | URL |
|---------|-----|
| Health | `GET /health` |
| V1 home | `GET /` → `/dashboard/` |
| Student Home | `/student/` |
| Journey | `/student/journey` |
| Learning Insights | `/student/revision` |
| Session | `/session/<id>/overview` … `/complete` |
| Curriculum Studio | `/founder/studio/` |
| Founder Intelligence | `/founder/intelligence` |
| Evidence Gates | `/founder/evidence-gates` |
