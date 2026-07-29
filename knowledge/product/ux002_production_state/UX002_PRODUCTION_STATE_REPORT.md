# UX-002 — Production State Report

**Programme:** Product Integrity  
**Status:** Complete  
**Date:** 2026-07-29  
**Host:** `https://kwalitec.onrender.com`  
**Live tip:** `18ffad54b04f500619b82aa7d5e17fb118f63d54`  
**Database:** Render Postgres `kwalitec-db` (`dpg-d97bmbm8bjmc73c497e0-a`, created 2026-07-08)  
**Scope:** Investigate legacy study-plan appearance after commercial deploy; remove non-canonical learner data only. **No schema changes. Canonical curricula preserved.**

---

## Summary

Production showed an active **IFoA CM1** study plan immediately after DP-004R because the Postgres database was **not** a greenfield wipe: learner history from **2026-07-13** Stage 1 / Internal Alpha dogfood remained on the same DB created **2026-07-08**. The plan was **not** seeded, **not** imported by migrations, and **not** auto-created on boot (`KWALITEC_V2_SEED_DEMO=0`; `StartupService` only migrates, bootstraps admin, and imports bundled curricula).

Learner / activity rows were removed safely via Render one-off jobs (`InternalAlphaResetService` + research-feedback and V2 aggregate cleanup). Post-clean HTTP checks show Founder Console healthy and `/study-plan/` landing on the **Choose Exam** wizard with **zero** study plans.

---

## Root cause

| Hypothesis | Verdict | Evidence |
|------------|---------|----------|
| Seeded at boot | **No** | `render.yaml` sets `KWALITEC_V2_SEED_DEMO=0`. `StartupService` never creates `StudyPlan` rows. |
| Imported via Alembic / dump | **No** | Migrations create empty `study_plans` tables only; no seed inserts. DP-002 forbids restoring learner dumps. |
| Created automatically on first login | **No** | Study plans are created only through the wizard / `StudyPlanService.create_study_plan`. |
| Left from previous testing | **Yes** | Plan rows dated **2026-07-13**; serial IDs **11** and **13**; DB created **2026-07-08**; DP-004R noted “Existing admin accepted login”. |

### What appeared after deploy

Authenticated Founder session (DP-004R and UX-002 re-check) on `/study-plan/` resolved an **active** plan:

| Field | Value |
|-------|--------|
| `id` | **13** |
| Exam | **IFoA CM1** |
| Sitting | September 2026 |
| Exam date | 2026-09-14 |
| Status | `active=True`, `archived=False` |
| `created_at` | **2026-07-13 14:45:26** |

A second legacy plan also existed:

| Field | Value |
|-------|--------|
| `id` | **11** |
| Exam | **IFoA CS1** |
| Sitting | September 2026 |
| Status | `active=False`, `archived=True` |
| `created_at` | **2026-07-13 14:36:12** |

Commercial release (DP-004R, 2026-07-29) upgraded schema on this **pre-existing** database. Application code and curriculum import are idempotent; they do not erase learner history. DP-002’s “empty PostgreSQL” rule was therefore violated in practice: the DB retained prior dogfood state.

UI delete of plan 13 during investigation returned **HTTP 500** because `research_feedback_submissions.study_plan_id` still referenced the plan — `EducationalContinuityService.release_plan_planning_artifacts` clears mission pointers but not research-feedback FKs. That is why a full reset path (null FKs → `InternalAlphaResetService`) was required.

---

## Database investigation

### Method

1. Code-path review: `StartupService`, `render.yaml` seed flags, study-plan creation surfaces, `InternalAlphaResetService`.  
2. Live inventory via Render one-off job on web service `srv-d97ji5t7vvec73cbs5l0` (job `job-d9l12v5aeets73abu0jg`).  
3. Authenticated HTTP probes against production.

### Pre-clean inventory (2026-07-29)

| Table | Count | Classification |
|-------|------:|----------------|
| `users` | 1 | Allowed (Founder) |
| `study_plans` | 2 | Learner — remove |
| `week_plans` | 19 | Learner — remove |
| `missions` | 18 | Learner — remove |
| `mission_tasks` | 47 | Learner — remove |
| `topic_progress` | 35 | Learner — remove |
| `subjects` (per-user) | 1 | Learner — remove |
| `study_attempts` | 2 | Learner — remove |
| `twin_snapshots` | 2 | Learner — remove |
| `mistakes` / `decisions` | 0 | — |
| `research_feedback_submissions` | 1 | Analytics / check-in — remove |
| `recommendation_commitments` | 0 | — |
| `runtime_enrolments` (+ related) | 0 | — |
| `curricula` | 3 | Canonical — **keep** |
| `sections` / `topics` / `learning_objectives` | 12 / 62 / 251 | Canonical — **keep** |
| `published_curriculum_packages` | 0 | Empty Studio publication (expected) |
| `studio_foundation_subjects` | 0 | Empty Studio (expected) |
| Alembic | `202607280080` | Head — unchanged |

Follow-on analytics/V2 inventory found **`v2_aggregate_documents=8`**, **`v2_aggregate_snapshots=336`** (durable twin/aggregate residue from prior dogfood). Platform `analytics_events` / outbox / audit were already **0**.

---

## Actions taken

| Step | Action | Result |
|------|--------|--------|
| 1 | Confirm live plan via Founder login | Active CM1 plan `#13` present |
| 2 | Attempt UI `POST /study-plan/13/delete` | **500** — research-feedback FK blocker |
| 3 | Render job: null `research_feedback_submissions.study_plan_id` / `mission_id` | Unblocked delete path |
| 4 | Render job: `InternalAlphaResetService.execute()` | **126** learner rows removed across 10 tables; users + curricula preserved |
| 5 | Delete research feedback chain (submissions, reviews, contributions, badges, transitions) | Product check-in analytics cleared |
| 6 | Delete V2 aggregate documents/snapshots | 8 docs + 336 snapshots removed |
| 7 | HTTP re-verify Founder / Study Plan / Student | Clean Founder-first state |

**Jobs (Render):**

- Inventory: `job-d9l12v5aeets73abu0jg` (succeeded)  
- Learner reset + research cleanup: `job-d9l144u1egvs738htbeg` (succeeded)  
- Analytics / V2 aggregate cleanup: `job-d9l14mu417fc73cuqo40` (succeeded)

**Not touched:** Alembic schema, curriculum JSON packages, Founder user row / password, production env configuration.

---

## Final production contents

### Confirmed present

| Content | State |
|---------|--------|
| Founder / Admin account | **1** user |
| Canonical curricula | **3** (`curricula`); sections/topics/LOs intact |
| Migrations | Head `202607280080` |
| System configuration | Production env / flags unchanged (`SEED_DEMO=0`, sole-runtime, etc.) |

### Confirmed absent (post-clean)

| Content | Count |
|---------|------:|
| Study plans | 0 |
| Week plans | 0 |
| Missions / mission tasks | 0 / 0 |
| Topic progress | 0 |
| Per-user subjects | 0 |
| Study attempts / mistakes / decisions | 0 |
| Twin snapshots | 0 |
| Research feedback submissions | 0 |
| Runtime enrolments / SCI instances | 0 |
| Published Studio packages / Studio subjects | 0 |
| Analytics events / outbox / audit | 0 |
| V2 aggregate documents / snapshots | 0 / 0 |

### HTTP verification (Founder session)

| Path | Result |
|------|--------|
| `POST /auth/login` | **302 → `/console/`** |
| `/console/` | **200** — Home · Kwalitec Console |
| `/study-plan/` | **200** — **Choose Exam · Kwalitec** (wizard; no plan ids) |
| `/study-plan/plans/all` | **200** — empty plan list |
| `/student/` | **200** — no active CM1 plan chrome |

---

## Recommendation

1. **Treat current DB as clean Founder baseline** for subsequent UX work — do not recreate study plans unless deliberately dogfooding.  
2. **Before any future “commercial reset” deploy**, either provision a **new empty Postgres** (DP-002) or run `flask internal-alpha-reset --yes` (plus research-feedback / V2 aggregate cleanup) and verify counts. Schema upgrade alone does not wipe learner history.  
3. **Hardening follow-up (optional, not done in UX-002):**  
   - Extend `EducationalContinuityService.release_plan_planning_artifacts` to null `research_feedback_submissions.study_plan_id` (fixes UI delete 500).  
   - Extend `InternalAlphaResetService` to include research-feedback and V2 aggregate / analytics tables so one CLI covers full Founder-clean posture.  
4. **Do not** re-enable `KWALITEC_V2_SEED_DEMO` in production.

---

## Files Created

- `knowledge/product/ux002_production_state/UX002_PRODUCTION_STATE_REPORT.md`

## Files Modified

- None (application code and schema unchanged)

## Tests Executed

- Production inventory + reset via Render jobs (succeeded; see Actions).  
- Authenticated HTTP smoke after cleanup (Console / Study Plan wizard / Student).  
- No local pytest suite required (ops / data integrity only).

## Migration Impact

**None** — no Alembic revisions added or applied beyond existing head.

## Architecture Compliance

- Curriculum V1/V2 reference rows preserved (`curricula` / `sections` / `topics` / `learning_objectives`).  
- Layering untouched.  
- Cleanup used existing `InternalAlphaResetService` semantics (users + curricula preserved; generated educational state removed).

## Technical Debt

- UI study-plan delete fails when research-feedback rows reference the plan (IntegrityError → 500).  
- `InternalAlphaResetService` does not yet cover research-feedback or V2 aggregate stores — required manual SQL in UX-002 jobs.

## Known Limitations

- Studio document blobs on ephemeral instance storage were not audited (DP-003 R-C2 residual).  
- Founder email / roles were not re-bootstrapped (already correct; create-admin remains a no-op when users exist).  
- No change to Stage 1 pilot credentials (still stale per DP-004R).
