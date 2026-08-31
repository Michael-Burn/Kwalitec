# Manual Deploy Runbook (Render)

**Programme:** Pre-deploy rigor pass (ADR-027 Phase 2 Stage 4 + Twin daily-loop resume + readiness honesty)  
**Audience:** Operator executing deploy via the Render dashboard (no CLI deploy from this repo)  
**Host:** https://kwalitec.onrender.com  
**Service:** `kwalitec` (web) · **Database:** `kwalitec-db` (PostgreSQL)  
**Authority:** `render.yaml` · `docs/production/DEPLOYMENT.md` · `docs/production/BACKUP_AND_RECOVERY.md` · `docs/production/VERSION_1_FLAG_MATRIX.md`

---

## Scope of this deploy

This runbook covers a **manual deploy** of the current `main` tip that includes:

| Change | Detail |
|--------|--------|
| Alembic migrations | Production is expected at `202607310002`. This deploy advances through `202608240001` → `202608240002` → `202608270001` → **`202608300001` (head)** |
| Destructive migration | `202608300001` **drops** `topic_progress.mastery_score` and `topic_progress.average_accuracy`. Downgrade can recreate empty columns but **cannot restore dropped values**. Columns are confirmed unused (ADR-027 Phase 2 Stage 4; Estimated Knowledge authority moved to the Learner Twin Query Port). |
| Twin daily loop | `SR_TWIN_DAILY_LOOP` hold ended 2026-08-31. `render.yaml` no longer sets `SR_TWIN_DAILY_LOOP=0`; the flag inherits **ON** from `KWALITEC_COMMERCIAL_LOOP=1`. New Twin writes resume after deploy. |
| Readiness honesty | Fresh accounts must show **not yet assessed** (or equivalent honest absence) for Estimated Knowledge / readiness figures, not fabricated `0%` values. |

**Intended deploy commit (local tip at runbook authoring):** `16cf075e2c7d6d1ee1b68455bd22449f6d2c1206`  
Replace with the exact SHA you push if it differs.

**Product version (unchanged):** `2.0.0-beta.1` (`VERSION`, `/health.version`)

---

## 1. Pre-deploy state confirmation

Complete these checks **before** backup or deploy. Record the values; you will compare them after deploy.

### 1.1 Live health probes

From any machine with network access:

```bash
BASE_URL=https://kwalitec.onrender.com

curl -fsS "$BASE_URL/health/live" | python3 -m json.tool
curl -fsS "$BASE_URL/health/ready" | python3 -m json.tool
curl -fsS "$BASE_URL/health" | python3 -m json.tool
```

| Field | Where | Pre-deploy expectation | Action if unexpected |
|-------|-------|------------------------|----------------------|
| Process up | `/health/live` → `status: ok` | 200 | Stop. Fix live service before migrating. |
| Readiness | `/health/ready` → `ready: true` | 200 | Stop if `ready: false`. Investigate DB / migrations. |
| Database | `/health` or `/health/ready` → `components.database.status: ok` | `ok` | Stop if `error`. |
| **Alembic current** | `components.migrations.meta.current` | **`202607310002`** (last verified production evidence) | If already at `202608300001`, migration may already have run; confirm commit matches intended release. |
| **Alembic head (live code)** | `components.migrations.meta.head` | Will still show **`202607310002`** until new code deploys | Expected pre-deploy. After deploy, both must equal **`202608300001`**. |
| Commit fingerprint | `commit` (from `/health/live` or `/health`) | Note current SHA (e.g. `4ff8c95…` from Aug-2026 RO/PB evidence) | After deploy, must match intended tip. |
| Version | `version` | `2.0.0-beta.1` | Informational unless you intentionally bumped `VERSION`. |
| Environment | `environment` | `production` | Must not be `development`. |

If `components.migrations.status` is `degraded` with `database behind head`, the running app code is already newer than the database. Proceed only after you understand which migrations already ran.

### 1.2 Render dashboard (service `kwalitec`)

| Check | Location | Pre-deploy action |
|-------|----------|-------------------|
| Current deploy commit | Render → **kwalitec** → **Events** / latest deploy | Record SHA; this is rollback target **A** |
| Service status | Dashboard | Must be **Live** (not failed / suspended) |
| Build / release / start commands | Settings | Must match `render.yaml`: build `pip install -r requirements.txt`, release `flask db upgrade`, start `waitress-serve --port=$PORT wsgi:app` |
| Auto-deploy | Settings | Prefer **manual deploy** of a known commit (see `DEPLOYMENT_CHECKLIST.md` B7) |

### 1.3 Render dashboard (database `kwalitec-db`)

| Check | Action |
|-------|--------|
| Database attached | Confirm web service `DATABASE_URL` still comes from `kwalitec-db` (`render.yaml` `fromDatabase`) |
| Plan | Blueprint declares `plan: free`. **Confirm current plan in dashboard** (backup features depend on plan tier). |

### 1.4 Environment flags (Render → kwalitec → Environment)

Confirm production posture matches `render.yaml` and `docs/production/VERSION_1_FLAG_MATRIX.md`:

| Variable | Required value | Notes |
|----------|----------------|-------|
| `APP_ENV` | `production` | |
| `FLASK_APP` | `wsgi.py` | |
| `SECRET_KEY` | Strong / generated | Must not be default placeholder |
| `DATABASE_URL` | From `kwalitec-db` | |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` | Set | Bootstrap admin |
| `KWALITEC_V2_SOLE_RUNTIME` | `1` | Canonical `/student` runtime |
| `KWALITEC_V2_DURABLE_STORE` | `1` | |
| `KWALITEC_V2_INJECT_ENGINES` | `1` | |
| `KWALITEC_V2_SEED_DEMO` | `0` | Must stay off in production |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | `1` | |
| `KWALITEC_EI_INTERNAL_ALPHA` | `1` | |
| `KWALITEC_COMMERCIAL_LOOP` | `1` | Enables commercial SR bundle |
| `SR_TWIN_DAILY_LOOP` | **Unset or absent** | **Do not set to `0`.** Hold ended; flag should inherit ON from commercial loop. Remove explicit `0` override if still present from the 2026-08-30 hold. |

Optional but useful: `APP_URL`, `PREFERRED_URL_SCHEME=https`, `TRUSTED_PROXY_HOPS=1`, `KWALITEC_SUPPORT_CONTACT`.

### 1.5 Repository gates (local)

Before triggering Render:

- [ ] Intended commit is on `origin/main` (push if needed)
- [ ] `flask db heads` shows single head **`202608300001`**
- [ ] pytest + ruff green on the deploy commit (per `DEPLOYMENT_CHECKLIST.md` A7)

---

## 2. Backup step (required before this deploy)

This deploy runs migration `202608300001`, which **drops columns**. Treat backup as mandatory.

### What this repo documents

| Source | Backup posture |
|--------|----------------|
| `docs/production/BACKUP_AND_RECOVERY.md` | Render platform automated backups **plus** pre-migrate manual `pg_dump` |
| `FOUNDER_DEPLOYMENT_GUIDE.md` | "Render PostgreSQL snapshot or logical dump" before upgrade |
| `docs/production/G8_RELIABILITY_EVIDENCE.md` | Same strategy acknowledged for invite-only Alpha |
| `render.yaml` | Declares `kwalitec-db` on **`plan: free`**; does **not** configure backup schedules |

### What this repo does **not** verify

The repository **does not** record whether Render automated backups, point-in-time recovery (PITR), or on-demand snapshots are enabled for your current `kwalitec-db` plan. Render backup capabilities vary by **database plan tier**; free-tier Postgres may offer limited or no operator-visible snapshot UI.

**You must confirm directly in the Render dashboard** (Postgres → `kwalitec-db` → Backups / Recovery, or equivalent tab for your plan).

### Recommended operator sequence

1. **Render native backup (if available on your plan)**  
   - Open Render → **Databases** → **`kwalitec-db`**.  
   - If the dashboard offers **Create backup**, **Snapshot**, or **Export**, create one **now**.  
   - Record backup id / timestamp / filename in your ops notes.  
   - If no backup UI appears on a free plan, proceed to step 2 and treat logical dump as the primary backup.

2. **Logical dump (always recommended; documented in repo)**  
   Run from a trusted machine that can reach Postgres (Render **External** connection string, or shell with `DATABASE_URL`):

   ```bash
   pg_dump "$DATABASE_URL" --format=custom --file="kwalitec-pre-$(date -u +%Y%m%dT%H%M%SZ).dump"
   ```

   Store the file offline. **Never commit** dumps to git.

3. **Verify backup exists**  
   - [ ] Render snapshot id recorded **or** logical dump file size > 0 and integrity checked (`pg_restore --list` on the dump).  
   - [ ] Backup timestamp noted **before** deploy start.

**Do not deploy** until at least one restorable backup from step 1 or 2 is confirmed.

---

## 3. Deploy step

### 3.1 Trigger manual deploy

1. Render → **kwalitec** → **Manual Deploy** (or **Deploy latest commit** if auto-deploy is off and `main` is already pushed).
2. Select commit **`16cf075e…`** (or your verified tip SHA).
3. Start deploy. Render runs in order:
   - **Build:** `pip install -r requirements.txt`
   - **Release:** `flask db upgrade` (applies pending migrations through `202608300001`)
   - **Start:** `waitress-serve --port=$PORT wsgi:app`

### 3.2 What to expect in logs

| Phase | Success signal | Failure signal |
|-------|----------------|----------------|
| Build | pip install completes | Dependency / build error → deploy aborts |
| Release | Alembic runs upgrades; ends without traceback | Migration error (often DDL on `topic_progress`) → **release fails**; old instance may keep running |
| Start | Waitress listening; service → Live | Crash loop → `/health/live` fails |

Expected migration sequence on a DB at `202607310002`:

```text
202607310002 → 202608240001 → 202608240002 → 202608270001 → 202608300001
```

The final step drops `topic_progress.mastery_score` and `topic_progress.average_accuracy`.

### 3.3 If release command fails

- **Do not** immediately redeploy a different commit without reading the Alembic error.
- Check whether the DB is partially upgraded (`flask db current` against production, or Render shell if available).
- If schema is inconsistent, use **rollback plan B** (restore backup), not repeated blind redeploys.

---

## 4. Post-deploy verification

### 4.1 Health and fingerprint

Re-run probes:

```bash
curl -fsS "$BASE_URL/health/live" | python3 -m json.tool
curl -fsS "$BASE_URL/health/ready" | python3 -m json.tool
```

| Check | Pass criteria |
|-------|---------------|
| `/health/live` | 200, `status: ok` |
| `/health/ready` | 200, `ready: true` |
| Migrations | `components.migrations.meta.current` = `head` = **`202608300001`**, `status: ok` |
| Commit | `commit` matches deployed SHA |
| Version | `version` = `2.0.0-beta.1` (unless intentionally bumped) |
| Database | `components.database.status: ok` |

Optional operator detail: `GET /health/details` for dead letters and latency.

### 4.2 Smoke path (student)

Use a **fresh or low-activity test account** where possible for readiness checks.

| Step | Action | Pass criteria |
|------|--------|---------------|
| 1 | Log in at `/auth/login` | Redirect to student home |
| 2 | Open **Home** (`/student/` or canonical home route) | Page loads; no 500 |
| 3 | **Readiness / Estimated Knowledge honesty** | For an account with no practice evidence, figures show honest **not yet assessed** (or empty / unavailable posture), **not** `0%` masquerading as a measurement. Check Home progress area and Settings → weekly report export if used. |
| 4 | Start **Today's Mission** / session | Session overview loads |
| 5 | **Complete one practice item** | Item scores; session advances |
| 6 | **Twin daily loop (session work)** | After completing practice with `KWALITEC_COMMERCIAL_LOOP=1` and no `SR_TWIN_DAILY_LOOP=0` override, Twin consumption should not be blocked by the hold. Optional founder check: `/founder/twin` shows updated snapshot after session evidence (Founder capability required). |
| 7 | Log out | CSRF POST logout returns to sign-in |

Founder optional: login → Console home → curriculum health (per `DEPLOYMENT_CHECKLIST.md` G1).

### 4.3 Deploy complete

Consider deploy **done** only when health fingerprint **and** smoke path pass. Record deploy id, commit SHA, migration head, and backup reference in ops notes.

---

## 5. Rollback plan

Choose path based on **whether the migration succeeded**.

### Option A — Fast rollback (migration did **not** run, or DB still at `202607310002`)

**When to use:**

- Build or start failed before `flask db upgrade` completed
- Release failed with **no** schema change (confirm `current` still `202607310002`)
- App bug on new code but database unchanged

**Steps:**

1. Render → **kwalitec** → **Manual Deploy** → select **previous known-good commit** (pre-deploy SHA from section 1.2).
2. Wait for build / release / start.
3. Confirm `/health/ready` → `ready: true`, migrations `current` = `head` = **`202607310002`**.
4. Re-run student smoke (section 4.2).

No database restore required.

### Option B — Restore from backup (migration **partially or fully** applied, especially `202608300001`)

**When to use:**

- `202608300001` applied (columns dropped) and you must return to pre-drop schema **with data**
- Alembic left DB in unknown / partial state
- Data corruption or migration error after DDL ran
- Redeploying old code is **not** enough because old code expects `mastery_score` / `average_accuracy` columns that no longer exist (or reverse: new code on broken partial schema)

**Steps:**

1. **Stop** further deploys. Put service in maintenance if needed.
2. **Restore** using the pre-deploy backup (section 2):
   - Render snapshot restore to a new instance **or**
   - `pg_restore --clean --if-exists --no-owner --dbname="$RESTORE_DATABASE_URL" kwalitec-pre-YYYYMMDD.dump`  
   (Full procedure: `docs/production/BACKUP_AND_RECOVERY.md`)
3. Point `DATABASE_URL` at restored database if Render created a new instance.
4. Redeploy **known-good application commit** compatible with restored schema (typically pre-migration tip with head `202607310002`).
5. Verify `/health/ready`, migration `current` matches restored state, smoke login.
6. Record incident per `docs/production/INCIDENT_RESPONSE.md`.

**Do not** rely on `flask db downgrade` for `202608300001` in production to recover dropped column **data**. Downgrade only recreates empty columns with server defaults.

### Decision summary

| Situation | Rollback |
|-----------|----------|
| New code bad, DB still at `202607310002` | **Option A** — redeploy previous commit |
| Migration `202608300001` succeeded, must undo | **Option B** — restore backup, then redeploy compatible code |
| Migration failed mid-chain | Inspect `alembic_version`; likely **Option B** if unsure |
| New code bad, migration succeeded, columns drop acceptable | Forward-fix on new commit (not rollback); dropped EK columns cannot be recovered from DB |

---

## Related documents

| Document | Path |
|----------|------|
| Deployment guide | `docs/production/DEPLOYMENT.md` |
| Backup and recovery | `docs/production/BACKUP_AND_RECOVERY.md` |
| Environment variables | `docs/production/ENVIRONMENT.md` |
| Flag matrix (Twin hold resume) | `docs/production/VERSION_1_FLAG_MATRIX.md` §2.1 |
| General checklist | `DEPLOYMENT_CHECKLIST.md` |
| Founder deploy guide | `FOUNDER_DEPLOYMENT_GUIDE.md` |
| Destructive migration | `migrations/versions/202608300001_drop_topic_progress_ek_columns.py` |

---

**End of runbook.** Operator executes all steps manually in Render; this document does not trigger deploy or backup actions.
