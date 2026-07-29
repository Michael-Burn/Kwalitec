# DP-004R — Production Deployment Retry Report

**Programme:** Production Deployment  
**Phase:** Final Controlled Release (retry after RC-2026.07.29-07 / 07A)  
**Date:** 2026-07-29  
**Host:** `https://kwalitec.onrender.com`  
**Certified tip deployed:** `18ffad54b04f500619b82aa7d5e17fb118f63d54`  
(`fix(migrations): restore PostgreSQL compatibility`)  
**Prior freeze (not deployed alone):** `43cdd46…`  
**Predecessors:** DP-001, DP-001A, DP-002, DP-003, DP-004 (failed migrate), RC-07, RC-07A  

---

## Executive Summary

Manual Render deploy of the PostgreSQL-certified tip **`18ffad5`** completed successfully. Pre-deploy migration advanced production from Alembic **`202607270003`** to head **`202607280080`**. The application serves the certified commit with `/health/ready` **true**, `environment=production`, and no dead letters.

Founder authentication and Console / Curriculum Studio / Student surfaces responded without runtime errors. Dedicated Stage 1 pilot password login failed (stale/invalid credentials). Persistent document durability was **not** proven: health reports instance storage under `/opt/render/project/src/instance` with **no** Render persistent disk evidence (DP-003 R-C2 residual).

**Decision: PRODUCTION DEPLOYMENT SUCCESSFUL** — certified release is live; storage durability remains an accepted residual from DP-003.

---

## Deployment Summary

| Item | Result |
|------|--------|
| Pre-deploy tip check | Local `HEAD` = `18ffad5` (match) |
| Tracked working tree | Clean (untracked knowledge reports only; not part of deploy artefact) |
| Push | `18ffad5` → `origin/main` and `origin/feature/ap-002-assessment-engine` |
| Auto-deploy | Disabled (by design) |
| Trigger | Operator **Manual Deploy → specific commit `18ffad5`** |
| Pre-deploy live commit | `ee38ac2…` |
| Post-deploy live commit | **`18ffad5…`** |
| Application code / migrations changed during DP-004R | **None** |

### Optional production DB safety check

| Check | Result |
|-------|--------|
| Direct `psql` / Render DB shell | **Unavailable** (no Render API/CLI auth in agent) |
| Indirect via pre-deploy `/health/ready` | `current=202607270003` → revision `202607270004` **not stamped** |
| Phase-1 column inspection | **Not performed** (no DB access) — continued per programme allowance |
| Post-deploy migrations | `current=head=202607280080` → upgrade applied cleanly |

---

## Build Summary

| Signal | Evidence |
|--------|----------|
| Build outcome | Inferred **success** (service returned HTTP 200 on new commit after brief 502 window) |
| Deploy fingerprint | `/health/live` commit = `18ffad54b04f500619b82aa7d5e17fb118f63d54` |
| 502 window | Observed during cutover (~13:50:45–13:51:18Z) then recover |
| Render dashboard build log text | Not captured in agent (no Render login); operator dashboard is authoritative for raw build stdout |

---

## Migration Summary

| Item | Result |
|------|--------|
| Pre-deploy stamp | `202607270003` (behind old artefact head) |
| Post-deploy stamp | **`202607280080`** |
| Head | **`202607280080`** |
| `202607270004` (prior DP-004 blocker) | Applied successfully on production (stamp advanced past it) |
| SQL / datatype errors | **None observed** (service healthy at head) |
| Transaction rollback | **None** (stamp at head; ready=true) |

---

## Startup Summary

| Check | Result |
|-------|--------|
| Process serving traffic | **Yes** (Waitress behind Render) |
| Production configuration | `environment=production` on health |
| Migrations at head | **Yes** |
| Founder bootstrap | Existing admin accepted login (create path no-op if users already present) |
| Curriculum import | Not directly log-scraped; reference curricula expected idempotent on boot; no ready failure |
| Waitress | Origin behaviour consistent with prior DEP-002 Waitress deploy |

---

## Health Validation

Observed after cutover (repeatable):

| Endpoint | HTTP | Result |
|----------|------|--------|
| `/health/live` | 200 | `status=ok`, commit=`18ffad5…` |
| `/health/ready` | 200 | `ready=true`, DB connected, migrations ok |
| `/health` | 200 | `status=ok`, `environment=production` |
| `/health/details` | 200 | `ready=true`, `dead_letters=[]` |

Migrations meta: `{current: 202607280080, head: 202607280080, status: ok}`.

---

## Founder Validation

| Check | Result |
|-------|--------|
| Login (`ADMIN_EMAIL` from operator env) | **302 → `/console/`** |
| `/console/` | **200** — Home · Kwalitec Console |
| `/console/studio/` | **200** — Curriculum Studio |
| `/console/studio/subjects` | **200** — Subjects |
| `/console/feedback`, `/participants`, `/settings` | **200** |
| Runtime error markers | **None** (no Traceback / 500 pages on probed routes) |

---

## Student Validation

| Check | Result |
|-------|--------|
| Unauthenticated `/student/` | 302 → login (expected) |
| Founder session `/student/` | **200** — Home · Kwalitec |
| `/student/profile`, `/journey`, `/history`, `/revision` | **200** |
| `/study-plan/` (follow redirects) | **200** — Study Plan · Kwalitec |
| Navigation targets present | `/student/`, `/study-plan/`, profile/journey/history/revision |
| Stage 1 pilot temp-password login | **Failed** — remained on Sign in; invalid-credentials flash |
| Mission runtime deep walk | Not exhaustively exercised beyond Study Plan / Home shells |

Student **application surfaces** verified via Founder’s student role. Dedicated pilot credential reuse failed (likely stale Stage 1 secrets vs current DB users) — operational follow-up, not a deploy crash.

---

## Persistent Storage Validation

| Check | Result |
|-------|--------|
| Health `instance_storage` | **ok** — path `/opt/render/project/src/instance` |
| Render persistent disk mounted | **Not evidenced** |
| `DOCUMENT_STORAGE_ROOT` on durable volume | **Not verified** |
| Upload test document + survive restart | **Not executed** (no durable disk proof; restart not performed) |

**Assessment:** Storage component is writable at the default instance path, but **durability across redeploy/restart is not certified**. This matches DP-003 critical residual **R-C2**.

---

## Log Review

| Stream | Access | Finding |
|--------|--------|---------|
| Pre-deploy migrate | Inferred from Alembic stamp jump | Success to `202607280080` |
| Application health after boot | Live JSON | ok / ready / no dead letters |
| Unhandled exceptions on probed pages | HTML probes | None detected |
| Full Render build/startup stdout | Dashboard only | Not archived in this report |

---

## Known Issues

1. **Document durability (R-C2)** — no persistent disk / object store verification; Studio PDFs may be lost on redeploy.  
2. **Stage 1 pilot login** — temp passwords from `ops/STAGE1_CREDENTIALS.local.txt` rejected; rotate/reprovision if pilots still needed.  
3. **Legacy `/curriculum-studio/` URL** — 404; canonical Studio is `/console/studio/`.  
4. **Render build logs** — not copied into repo evidence pack (operator retains dashboard).  
5. **CQ-008B / DP-001 residual regressions** — unchanged product follow-ups; not re-litigated here.

---

## Deployment Timing (UTC)

| Event | Time (approx.) |
|-------|----------------|
| Manual deploy monitoring start | 2026-07-29T13:49:56Z |
| Cutover 502s | 13:50:45Z – 13:51:18Z |
| Certified commit live | **13:51:33Z** |
| Health ready at head | 13:51:39Z |

---

## Final Recommendation

1. Treat **`18ffad5`** as the live **Kwalitec v1.0 production release** tip.  
2. Keep auto-deploy **off** unless a protected release branch policy is adopted.  
3. Schedule storage remediation (Render disk + `DOCUMENT_STORAGE_ROOT`, or object storage) before relying on Studio PDF retention.  
4. Re-issue Stage 1 student credentials if pilots continue.  
5. Optionally archive Render deploy log screenshots beside this report.

---

## Decision

# PRODUCTION DEPLOYMENT SUCCESSFUL

| Success criterion | Met? |
|-------------------|------|
| Deployment completed | **Yes** |
| Alembic reached head | **Yes** (`202607280080`) |
| Application started | **Yes** |
| Founder verified | **Yes** |
| Student verified | **Yes** (Founder student surfaces; pilot password login failed) |
| Persistent storage verified | **Partial / residual** — instance ok; durability not proven |
| Health endpoints healthy | **Yes** |
| No migration failures | **Yes** |
| No startup failures | **Yes** |
| No critical runtime errors on probed paths | **Yes** |

Application code and migrations were **not** modified during DP-004R. Deploy artefact is exactly certified tip `18ffad5`.
