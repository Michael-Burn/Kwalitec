# RF-002 — Deployment Verification

**Programme:** RF-002 Educational System Verification  
**Phase:** Phase 7 — Deployment Verification  
**Date:** 2026-07-31  
**Live host:** `https://kwalitec.onrender.com`  
**Candidate:** Working tree = RF-001 seal + BF-001 + SB-001A (not yet live)

---

## Executive deployment verdict

| Scope | Verdict |
|-------|---------|
| Live RF-001 production tip | **HEALTHY** (unchanged RF-001A posture) |
| Live SB-001A Baseline surface | **NOT DEPLOYED** — `/baseline` returns 404 |
| Candidate educational system | **VERIFIED** in test harness |
| Production cutover readiness | **BLOCKED** until Alembic head merge + Manual Deploy |

---

## Live production probe (2026-07-31)

| Check | Result | Notes |
|-------|--------|-------|
| Deployment / process | **PASS** | `/health` `status: ok` |
| Database | **PASS** | `database: connected` |
| Migrations (live) | **PASS at RF-001 head** | `current=head=202607300005` |
| Authentication | **PASS** | `/auth/login` 200 |
| Static assets | **PASS** | `/static/css/design_system.css` 200 |
| Logging / health detail | **PASS** | `/health/details` returns build metadata |
| Health ready | **PASS** | `/health/ready` `ready: true` |
| Baseline endpoints | **FAIL (expected)** | `/baseline/` → **404** (SB-001A not on live) |
| Student runtime endpoints | **PASS (auth gate)** | `/student/` → 302 to login |

**Live commit:** `e4d5a1b6271630f5bcd6047239d087fa075176da`  
Evidence: `knowledge/evidence/releases/RF002/live_endpoints.txt` (and prior RF-001A `live_health.json` same tip)

---

## Candidate migration state

Alembic currently has **two heads**:

```text
202607300005 (head)   — live production head
202607310001 (head)   — SB-001A student_baselines (revises 202611120001)
```

`flask db current` / startup logging warn: multiple heads — migrate cannot advance cleanly without an Alembic merge revision.

| Risk | Impact |
|------|--------|
| Deploy SB-001A without merge | Migration tooling ambiguity; production may not apply `student_baselines` |
| Deploy without Manual Deploy | Live continues pre-Baseline Calibration path |

---

## Candidate endpoint inventory (verified in tests)

| Surface | Candidate status |
|---------|------------------|
| `/baseline/` progressive wizard | Registered; tests green |
| `/baseline/for-plan/<id>` | Calibration compatibility |
| `/student/` Baseline gate | Active plan without Baseline → redirect |
| Founder `/founder/participants/<id>/baseline` | Inspect / reset / restart |
| Runtime `/session/*`, `/student/*` | Unchanged behaviour suites |
| Studio publish / archive | BF-001 remediation suites green |

---

## Deployment checklist before G1 on live

1. Commit BF-001 + SB-001A + RF-002 reports.
2. Add Alembic **merge revision** joining `202607300005` and `202607310001`.
3. Push `main` and **Manual Deploy** on Render.
4. Confirm live `/health/details` migrations include `202607310001` (or merge head).
5. Confirm authenticated `/baseline/` is reachable (not 404).
6. Confirm live Studio JS contains `var byId = {}` (BF-001 cutover).
7. Smoke: Availability → Baseline → Home on production.

Until steps 1–7 complete, G1 Founder Validation must use the **candidate build** (local/staging), not the current live tip, for Baseline continuity claims.

---

## No deployment regressions (RF-001 tip)

Relative to RF-001A: live health, DB, auth, static assets remain healthy. No new live regressions introduced by RF-002 (verification-only; no live deploy performed).
