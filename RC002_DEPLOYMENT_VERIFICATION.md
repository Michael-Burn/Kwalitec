# RC-002 — Deployment Verification

**Programme:** Release Candidate RC-002  
**Date:** 2026-07-31  
**Host:** https://kwalitec.onrender.com  

---

## Git / tag evidence

| Item | Value |
|---|---|
| Release commit | `f2cbdc5db014b33357628ef2bb0460f5ee6770fd` |
| Docs follow-up | `f69457f80dc3c7987ceb3d0745d7a204c63b62a9` |
| Tag | `v1.0.0-rc2` → `f2cbdc5…` (pushed to origin) |
| `origin/main` | at `f69457f` (includes RC-002) |

---

## Local production-equivalent smoke (pre-push)

Environment: local dogfood SQLite + commercial loop + sole runtime flags.

| Step | Result |
|---|---|
| Application starts / health | **PASS** |
| Login (founder admin) | **PASS** |
| Founder console | **PASS** |
| Student Home / Adaptive Workspace | **PASS** |
| Today's Mission chrome | **PASS** |
| Learning Episode on Home | **PASS** |
| Tomorrow Preview | **PASS** |
| Title integrity (DF-016) | **PASS** — no `Study 1 — .1` |
| Runtime C (no A fallback chrome) | **PASS** |
| Session start → `/session/lsr-…/activity` | **PASS** |
| Activity / Episode surface | **PASS** — no exceptions |
| Sitting Report language on summary path | **PASS** |
| Learning Journey | **PASS** |
| Logout + gate | **PASS** |

**Score:** 19 / 19 automated smoke checks.

---

## Production verification (post-push)

| Check | Result | Notes |
|---|---|---|
| Push to `main` | **PASS** | `ee1101d..f2cbdc5` then docs `f69457f` |
| Tag `v1.0.0-rc2` | **PASS** | Pushed to origin |
| Render auto-deploy | **NOT OBSERVED** | Live `/health` still reports commit `ee1101d…` after push (~15+ min). `FOUNDER_DEPLOYMENT_GUIDE.md`: *manual deploy; auto-deploy may be off* |
| Database connected (current live) | **PASS** | Pre-RC commit still healthy |
| Application available | **PASS** | `/auth/login` 200 on live host |
| Health `/health/live` + `/ready` | **PASS** | Live service healthy on prior commit |
| Static assets | **PASS** | Login page loads (200) |
| RC-002 commit live | **PENDING MANUAL DEPLOY** | Founder must **Manual Deploy** commit `f2cbdc5` (or latest `main`) in Render dashboard |
| Full founder educational journey on new build | **PENDING** | Re-run after Manual Deploy |

---

## Required operator action

1. Open Render → service `kwalitec` → **Manual Deploy** → deploy latest `main` (`f69457f` or at least `f2cbdc5`).
2. Wait for build + `flask db upgrade` release command.
3. Confirm `/health` `commit` starts with `f2cbdc5` or `f69457f`.
4. Execute one founder browser sitting: Login → Home → Mission → Session → Episode → Evidence → Sitting Report → Journey → Tomorrow → Logout.
5. Update this file’s production table to **PASS** and begin G1 study logs.

---

## Overall deployment verification label

**PUSH + TAG COMPLETE / RENDER CUTOVER PENDING MANUAL DEPLOY**
