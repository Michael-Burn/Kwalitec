# RC-003 — Production Cutover Report

**Programme:** Release Cutover Programme RC-003  
**Phase:** Production Cutover & G1 Launch  
**Date:** 2026-07-31  
**Host:** https://kwalitec.onrender.com  
**Authority:** RF-001 PASS · BF-001 PASS · RF-001A GO WITH ACCEPTED DEBT · SB-001A PASS · RF-002 GO FOR G1 FOUNDER VALIDATION

---

## Final recommendation

**GO FOR G1 FOUNDER VALIDATION — CUTOVER CONFIRMED**

Production now matches the verified RF-002 candidate. Manual Deploy landed tip `6d8b931` (includes seal `e953ee1`), migrations at merge head `202607310002`, `/baseline/` auth-gated (**302**), and BF-001 Studio JS live (`var byId = {}`).

Begin daily Founder use under `G1_VALIDATION_PROTOCOL.md`. Complete one authenticated Founder + Student browser smoke on Day 1 and file observations — no engineering unless a verified Category A defect appears.

---

## Repository readiness

| Check | Result |
|-------|--------|
| Working tree before seal | Dirty — uncommitted SB-001A / BF-001 / RF-002 candidate |
| Artefacts committed | SB-001A · BF-001 · RF-001A · RF-002 · RC-003 merge + protocol |
| Untracked educational implementation | Cleared by release commit |
| Branch | `main` |

### Repository Status Summary

RC-003 sealed the RF-002 candidate and cut it over to production. Pre-cutover live tip was `e4d5a1b` (migrations `202607300005`, `/baseline/` 404). Post-cutover live tip is `6d8b931` (migrations `202607310002`, `/baseline/` 302).

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
| Live production stamp | **PASS** — `current=head=202607310002` |

Evidence: `knowledge/evidence/releases/RC003/alembic_heads.txt`, `cutover_verification.txt`

---

## Production candidate build

| Fingerprint | Value |
|-------------|-------|
| Application version | `2.0.0-beta.1` (`VERSION` / `APP_VERSION`) |
| Static asset fingerprint | `2.0.0-beta.1-g1` (cache-bust for BF-001 JS) |
| Seal commit | `e953ee196d94af65eb7b8307f8fbf7cfb8bd1caf` |
| Live deployed commit | `6d8b93161cb1680216b24a7854387efe0b9cf8b7` |
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
| Pre-cutover live health | **PASS** | tip `e4d5a1b`, migrations `202607300005` |
| Push to `origin/main` | **PASS** | seal `e953ee1` + docs through `6d8b931` |
| Tag `v1.0.0-G1` | **PASS** | → `e953ee1` on origin |
| Render auto-deploy | **NOT OBSERVED** | Manual Deploy required |
| Render Manual Deploy | **PASS** | Operator verified 2026-07-31 |
| Live commit | **PASS** | `6d8b93161cb1680216b24a7854387efe0b9cf8b7` |
| Live migrations | **PASS** | `current=head=202607310002` |
| `/health` + `/health/ready` | **PASS** | `status: ok`, `ready: true` |
| Database | **PASS** | `connected` |
| `/baseline/` | **PASS** | **302** (auth gate; was 404) |
| Studio JS BF-001 | **PASS** | `var byId = {};` live |

Evidence: `knowledge/evidence/releases/RC003/cutover_verification.txt`, `post_cutover_health.json`, `post_cutover_ready.json`

---

## Smoke test evidence

### Candidate (local automated) — PASS

| Path | Result |
|------|--------|
| Availability → Baseline | PASS |
| Calibration → Baseline redirect | PASS |
| Baseline wizard → Twin / plan bridge | PASS |
| Study plan lifecycle / mission smoke | PASS |
| Studio BF-001 Expand/Collapse remediation | PASS |

### Production operational probes — PASS

| Probe | Result |
|-------|--------|
| Health / ready | PASS |
| Migration head live | PASS (`202607310002`) |
| Baseline reachable (auth-gated) | PASS (302) |
| BF-001 JS live | PASS |

### Production authenticated browser path — Day 1 G1

Founder: Login → Curriculum Studio → Expand All → Collapse All → Back → Restart → Assign Version → Publish → Archive → Logout  

Student: Login → Exam Selection → Availability → Baseline → Twin Birth → Dashboard → Today's Mission → Study Session → Reflection → Complete Session → Logout  

File results under `knowledge/evidence/releases/G1/` per `G1_VALIDATION_PROTOCOL.md`.

---

## Educational continuity verification

| Claim | Candidate | Production |
|-------|-----------|------------|
| Baseline available | PASS | **PASS** (302 auth gate) |
| Calibration redirects correctly | PASS | Expected equivalent (candidate-verified) |
| Twin initialises | PASS | Live path available post-Baseline |
| Runtime A / Runtime C bridge | PASS | Live on cutover build |
| Study Plan / Mission | PASS | Live on cutover build |
| BF-001 Studio Expand/Collapse | PASS | **PASS** (`var byId = {}`) |
| No duplicate educational state | PASS (RF-002) | Monitor in G1 |

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
| Seal commit | `e953ee196d94af65eb7b8307f8fbf7cfb8bd1caf` |
| Deployed commit | `6d8b93161cb1680216b24a7854387efe0b9cf8b7` |
| Migration | `202607310002` |
| Release date | 2026-07-31 |
| Protocol | `G1_VALIDATION_PROTOCOL.md` |

---

## Success criteria ledger

| Criterion | Status |
|-----------|--------|
| Single Alembic head | **PASS** (`202607310002`) |
| Production deployment succeeds | **PASS** |
| Production operational smoke | **PASS** |
| Baseline reachable in production | **PASS** (302) |
| Calibration redirects correctly | **PASS** (candidate; live path cut over) |
| Runtime A operational | **PASS** (cutover build) |
| Runtime C bridge operational | **PASS** (cutover build) |
| Founder Studio BF-001 fixes live | **PASS** |
| Educational continuity preserved | **PASS** at cutover; G1 monitors daily |
| Release tagged | **PASS** (`v1.0.0-G1` → `e953ee1`) |
| Founder Validation Protocol created | **PASS** |

---

## Classification of issues discovered in RC-003

| Class | Finding | Disposition |
|-------|---------|-------------|
| Migration issue | Dual Alembic heads | **Resolved** by `202607310002` |
| Deployment issue | Auto-deploy off | **Resolved** by Manual Deploy |
| Configuration issue | None new | — |
| Operational issue | Pre-cutover `/baseline/` 404 | **Resolved** — now 302 |

No feature development was performed.

---

## Architecture compliance

- Layering preserved (blueprints → services → models).
- Curriculum V1/V2 loadability unchanged.
- Additive schema only (`student_baselines` + empty merge).
- No Runtime A/C, SCI, recommendation, Study Plan, or Twin redesign.
