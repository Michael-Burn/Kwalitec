# RC-003 — Production Cutover Report

**Programme:** Release Cutover Programme RC-003  
**Phase:** Production Cutover & G1 Launch  
**Date:** 2026-07-31  
**Host:** https://kwalitec.onrender.com  
**Authority:** RF-001 PASS · BF-001 PASS · RF-001A GO WITH ACCEPTED DEBT · SB-001A PASS · RF-002 GO FOR G1 FOUNDER VALIDATION

---

## Final recommendation

**GO FOR G1 FOUNDER VALIDATION — PENDING MANUAL RENDER DEPLOY CONFIRMATION**

The verified RF-002 educational candidate is sealed on `main` at `e953ee1` with a single Alembic head, G1 protocol, and release tag `v1.0.0-G1`. No feature work was introduced in RC-003 beyond migration merge and cutover identity (static fingerprint `*-g1`).

Live equivalence gates below flip to PASS only after Render **Manual Deploy** of this commit.

---

## Repository readiness

| Check | Result |
|-------|--------|
| Working tree before seal | Dirty — uncommitted SB-001A / BF-001 / RF-002 candidate |
| Artefacts committed | SB-001A · BF-001 · RF-001A · RF-002 · RC-003 merge + protocol |
| Untracked educational implementation | Cleared by release commit |
| Branch | `main` |

### Repository Status Summary

RC-003 seals the RF-002 candidate that was verified locally but not yet on live production tip `e4d5a1b`. Pre-cutover live state: migrations `202607300005`, `/baseline/` **404**, product version `2.0.0-beta.1`.

---

## Migration merge evidence

| Item | Value |
|------|-------|
| Heads merged | `202607300005` (PB-001, live) + `202607310001` (SB-001A) |
| Merge revision | `202607310002` |
| File | `migrations/versions/202607310002_merge_pb001_sb001a_heads.py` |
| History rewrite | **None** (empty merge only) |
| Single head | **PASS** — `flask db heads` → `202607310002` |
| Fresh upgrade | **PASS** → `202607310002` + `student_baselines` table |
| Production-path upgrade | **PASS** — stamp `202607300005` then `upgrade` applies `202607310001` then merge |
| Downgrade of merge | **PASS** — empty downgrade returns to dual heads; re-upgrade restores merge |

Evidence: `knowledge/evidence/releases/RC003/alembic_heads.txt`

---

## Production candidate build

| Fingerprint | Value |
|-------------|-------|
| Application version | `2.0.0-beta.1` (`VERSION` / `APP_VERSION`) |
| Static asset fingerprint | `2.0.0-beta.1-g1` (cache-bust for BF-001 JS) |
| Git commit | `e953ee196d94af65eb7b8307f8fbf7cfb8bd1caf` |
| Migration head | `202607310002` |
| Database compatibility | Additive `student_baselines` + empty merge; PostgreSQL-compatible types |
| Dependency lock | `requirements.txt` pinned (no separate lockfile; matches RC-002 posture) |
| Static asset build | Served from repo `app/static/` (no separate frontend build) |
| Local-only config | None introduced; `render.yaml` production flags unchanged |

Candidate verification tests (local): **81 passed** — SB-001A + BF-001 + baseline mapper + `tests/test_smoke.py`.

---

## Deployment evidence

| Check | Result | Notes |
|-------|--------|-------|
| Pre-cutover live health | **PASS** | `status: ok`, DB connected, tip `e4d5a1b` |
| Pre-cutover migrations | `current=head=202607300005` | Baseline not live |
| Push to `origin/main` | **PASS** | `e4d5a1b..2bfb231` (seal `e953ee1` + docs) |
| Tag `v1.0.0-G1` | **PASS** | Annotated tag → `e953ee1` on origin |
| Render auto-deploy | **NOT OBSERVED** | ~2+ min post-push; live still `e4d5a1b` |
| Render deploy | **REQUIRES MANUAL DEPLOY** | Same posture as RC-002 / RF-001 |
| Post-deploy commit match | **PENDING** — expect `e953ee1…` or docs tip `2bfb231…` | |
| Post-deploy migration | Expect `202607310002` | Via `releaseCommand: flask db upgrade` |
| Startup / health | Pre-cutover healthy; post-cutover **PENDING** | |
| Auth `/auth/login` | Pre-cutover **200** | Re-confirm after deploy |
| Logging / health details | Pre-cutover **PASS** | Re-confirm after deploy |
| Live `/baseline/` pre-cutover | **404** (expected) | Must become auth-gated after deploy |
| Live Studio JS pre-cutover | Still `var byId = Object` | BF-001 not live until deploy |

Evidence: `knowledge/evidence/releases/RC003/push_and_deploy_status.txt`, `post_push_health.json`

### Operator action (blocking for live G1 Baseline claims)

1. Render → service `kwalitec` → **Manual Deploy** → latest `main` (`2bfb231` or at least seal `e953ee1`).
2. Confirm release command upgrades to `202607310002`.
3. Confirm `/health` `commit` starts with `e953ee1` or `2bfb231`.
4. Confirm `/baseline/` is auth-gated (**302** to login, not **404**).
5. Confirm live JS contains `var byId = {};` (not `Object`).
6. Execute production Founder + Student smoke paths; file `knowledge/evidence/releases/RC003/prod_smoke.txt`.
7. Begin daily G1 under `G1_VALIDATION_PROTOCOL.md`.

---

## Smoke test evidence

### Candidate (local automated) — PASS

| Path | Result |
|------|--------|
| Availability → Baseline | PASS (SB-001A + smoke) |
| Calibration → Baseline redirect | PASS |
| Baseline wizard → Twin / plan bridge | PASS |
| Study plan lifecycle / mission smoke | PASS (`tests/test_smoke.py`) |
| Studio BF-001 Expand/Collapse remediation | PASS |

### Production browser path — PENDING MANUAL DEPLOY

Founder: Login → Curriculum Studio → Expand All → Collapse All → Back → Restart → Assign Version → Publish → Archive → Logout  

Student: Login → Exam Selection → Availability → Baseline → Twin Birth → Dashboard → Today's Mission → Study Session → Reflection → Complete Session → Logout  

Re-run immediately after Manual Deploy; record results in `knowledge/evidence/releases/RC003/prod_smoke.txt`.

---

## Educational continuity verification

Candidate equivalence to RF-002 (local):

| Claim | Candidate |
|-------|-----------|
| Baseline available | PASS |
| Calibration redirects correctly | PASS |
| Twin initialises | PASS (honest skip disclosed) |
| Runtime A begins correctly | PASS |
| Runtime C bridge functions | PASS |
| Study Plan generated | PASS |
| Mission generated | PASS |
| History retained | PASS |
| No duplicate educational state | PASS (RF-002) |

Production continuity: **PENDING** until deploy proves `/baseline/` live and migrations at merge head.

---

## Known accepted debt

Unchanged from RF-002 / RF-001A (not fixed in RC-003):

- Thin Runtime C SCI seed
- Runtime C Twin birth may honestly skip
- Narrow Baseline gate (Home-centric)
- Session finish → Sitting Report test drift (Category D)
- Full-tree pytest residual (~159)
- No dedicated per-student Twin viewer
- Public `/health/details`
- Presentation polish debt (PX)

---

## Release tag

| Item | Value |
|------|-------|
| Tag | `v1.0.0-G1` |
| Commit | `e953ee196d94af65eb7b8307f8fbf7cfb8bd1caf` |
| Deployment | Manual Deploy required on Render service `kwalitec` |
| Migration | `202607310002` |
| Release date | 2026-07-31 |
| Protocol | `G1_VALIDATION_PROTOCOL.md` |

---

## Success criteria ledger

| Criterion | Status |
|-----------|--------|
| Single Alembic head | **PASS** (`202607310002`) |
| Production deployment succeeds | **PENDING MANUAL DEPLOY** |
| Production smoke tests pass | **PENDING MANUAL DEPLOY** |
| Baseline reachable in production | **PENDING MANUAL DEPLOY** |
| Calibration redirects correctly | **PASS** on candidate |
| Runtime A operational | **PASS** on candidate |
| Runtime C bridge operational | **PASS** on candidate |
| Founder Studio BF-001 fixes live | **PENDING MANUAL DEPLOY** |
| Educational continuity preserved | **PASS** on candidate; prod pending |
| Release tagged | **PASS** (`v1.0.0-G1` → `e953ee1`) |
| Founder Validation Protocol created | **PASS** (`G1_VALIDATION_PROTOCOL.md`) |

---

## Classification of issues discovered in RC-003

| Class | Finding | Disposition |
|-------|---------|-------------|
| Migration issue | Dual Alembic heads | **Resolved** by `202607310002` |
| Deployment issue | Auto-deploy off | Operator Manual Deploy (same as RC-002/RF-001) |
| Configuration issue | None new | — |
| Operational issue | Pre-cutover `/baseline/` 404 | Expected until deploy |

No feature development was performed.

---

## Architecture compliance

- Layering preserved (blueprints → services → models).
- Curriculum V1/V2 loadability unchanged.
- Additive schema only (`student_baselines` + empty merge).
- No Runtime A/C, SCI, recommendation, Study Plan, or Twin redesign.
