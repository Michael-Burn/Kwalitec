# FOUNDER_VALIDATION_BUILD

**Build identifier:** `FV-001`  
**Product version:** `2.0.0-beta.1`  
**Static fingerprint:** `2.0.0-beta.1-rf001`  
**Programme that sealed the build:** RF-001 — Founder Release Freeze & Validation Build Preparation  
**Deployment date:** 2026-07-31  
**Environment:** Production — https://kwalitec.onrender.com  
**Database revision:** Alembic `202607300005`  

This document is the **official Founder Validation Build baseline for G1**.  
Programme companion: `RF001_VALIDATION_BUILD.md`.

---

## Commit hash

| Role | Hash |
|------|------|
| RF-001 validation build | `8915930c913d5cd08f19c1ab69fc8a8f6bf37696` |
| Docs annotation | `4befe800bd9e25d8fa3dc024376fb5661a015cd4` |
| Git tag | `v1.0.0-fv1` → `8915930…` |
| Prior RC-002 tip (pre-cutover live) | `d94d5140878cea4c1cf5216443a0f3f3b08ddbaa` |
| RC-002 educational freeze core | `f2cbdc5db014b33357628ef2bb0460f5ee6770fd` (`v1.0.0-rc2`) |

---

## What is included

Educational Runtime singularity and integrity from V1S-008 / RC-002, plus presentation programmes:

- UX-001 — Student Home session split
- PX-001 — Product experience foundation
- PX-002 — Founder experience density
- PX-003 — Workflow transparency & confidence
- PX-004 — Premium craft & release polish

No new features, curriculum engines, recommendation ranking, or architecture changes in RF-001 itself.

---

## Test summary

| Suite | Result |
|-------|--------|
| Founder + Student smoke walkthrough | **17/17 PASS** |
| Workflow + educational integrity smoke | **84/84 PASS** (targeted) |
| Release-critical presentation / studio / home / V1S-008 | **773 passed**, 12 failed (known debt), 1 skipped |
| Full `tests/` tree | **45616 passed**, **159 failed**, 9 skipped, ~67k warnings |

Full-tree zero is **not** claimed. Residual failures match RC-002 Category B–D posture (stale fixtures, snapshots, commercial-loop finish→summary redirect, soft CSS budget). **No Category A blockers** on Founder/Student primary validation paths.

---

## Known accepted limitations

1. Full pytest residual debt (time-engine fixtures, tutor/EOS snapshots, outdated chrome assertions).
2. `/health/details` public operator JSON (deferred auth gate).
3. Legacy Founder Bootstrap islands (Vision / Beta / Findings) — PX-004 accepted debt.
4. Settings still hosts advanced lifecycle shortcuts (PX-003 debt).
5. Pause may appear twice in session chrome (PX-003 debt).
6. History cards may use generic “Session complete” labels.
7. Render Manual Deploy may be required (auto-deploy observed off in RC-002).

---

## Outstanding non-blocking debt

- Branding asset duplication under `app/static/branding/` and `assets/branding/`
- Split prod vs dev requirements (`gunicorn` + test tools in prod install)
- Soft first-party CSS/JS budget warning (`test_v1sp003_performance`)
- Local dogfood SQLite Alembic stamp hygiene

---

## Validation objectives (G1)

1. Complete real founder study sessions on this exact build.
2. Collect evidence for educational usefulness — not intuition-driven UX changes.
3. Treat every change request as: production defect, study blocker, security issue, or data integrity issue — otherwise backlog.
4. Advance G1 consecutive-week evidence toward Version 1 production-ready gates (P-002.1).

---

## Freeze statement

From RF-001 completion, this application build is **frozen for Founder Validation**.  
Next programme: **G1 — Founder Validation**.
