# RC-002 — Deployment Verification

**Programme:** Release Candidate RC-002  
**Date:** 2026-07-31  
**Host:** https://kwalitec.onrender.com  

---

## Status

**PENDING DEPLOY** of RC-002 commit — local founder smoke **PASS**; production verification runs after Render deploy of the release commit.

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

## Production verification (post-deploy)

| Check | Result | Notes |
|---|---|---|
| Build successful | _pending_ | |
| Database connected | _pending_ | `/health` |
| Application available | _pending_ | `/auth/login` |
| Static assets loading | _pending_ | |
| Health endpoint | _pending_ | `/health/live`, `/health/ready` |
| Login → Home → Mission → Session → Episode → Evidence → Sitting Report → Journey → Tomorrow → Logout | _pending_ | Founder browser pass |
| No runtime exceptions | _pending_ | |
| No broken educational flow | _pending_ | |

---

## Update instruction

After Render finishes deploying the RC-002 commit, re-run health probes and one founder browser sitting; fill results above and set overall **PASS** / **FAIL**.
