# UX-002A — Founder Reset & Data Lifecycle Hardening Report

**Programme:** Product Integrity  
**Status:** Complete  
**Date:** 2026-07-29  
**Predecessor:** UX-002 (clean production Founder baseline)  
**Scope:** Harden Study Plan deletion and make `InternalAlphaResetService` the canonical Founder reset — no UI redesign, no feature work, no schema redesign.

---

## Summary

UX-002 exposed two operational gaps: Study Plan delete could HTTP 500 when `research_feedback_submissions` still referenced the plan, and Founder reset required manual SQL beyond `InternalAlphaResetService`. This programme closes both.

Study Plan deletion now releases every nullable plan pointer (missions + research feedback) before delete, maps residual integrity failures to a user-facing validation message, and never surfaces a 500 to the operator. `InternalAlphaResetService` now deletes the full learner-generated operational surface (plans, progress, analytics, research feedback, V2 aggregates, runtime/SCI bindings, twin projections) while preserving users, canonical curricula, Studio configuration, and published curriculum metadata. Reset is idempotent.

---

## Root Cause

| Weakness | Cause |
|----------|--------|
| Study Plan delete → HTTP 500 | `EducationalContinuityService.release_plan_planning_artifacts` cleared `missions.study_plan_id` only. `research_feedback_submissions.study_plan_id` remained an FK to `study_plans.id`, so PostgreSQL raised `IntegrityError` and the route had no friendly handler. |
| Incomplete Founder reset | `RESET_MODELS` covered Runtime A educational tables only. Research feedback, analytics, V2 aggregates, runtime enrolments, recommendation commitments, and SDT rows were out of scope — UX-002 had to run ad-hoc SQL. |

---

## Services Updated

| Path | Change |
|------|--------|
| `app/services/educational_continuity_service.py` | Release research-feedback plan pointers alongside missions |
| `app/services/study_plan_service.py` | Catch `IntegrityError` on delete → `ValueError` with operator-safe message |
| `app/study_plan/routes.py` | Defence-in-depth: catch unexpected errors, flash archive guidance (no 500) |
| `app/services/internal_alpha_reset_service.py` | Expand reset / preserve model sets; skip missing tables; keep Alembic intact |
| `app/cli.py` | Align `flask internal-alpha-reset` copy with Founder-complete reset semantics |

---

## Dependencies Reviewed

### StudyPlan foreign keys (blocking delete)

| Dependent | Column | Nullable | Delete strategy |
|-----------|--------|----------|-----------------|
| `week_plans` | `study_plan_id` | No | ORM cascade `delete-orphan` |
| `missions` | `study_plan_id` | Yes | **Release** (EIP-005 continuity) |
| `research_feedback_submissions` | `study_plan_id` | Yes | **Release** (retain submission) |

Non-FK soft references (`runtime_enrolment_routing_audits.study_plan_id`) do not block deletion.

### Reset coverage model set (child → parent order)

Research feedback graph → analytics → V2 aggregates → Runtime C / SCI → SDT → recommendation commitments → Runtime A educational history (`Mistake` … `Subject`).

### Preserved

Users; curricula / sections / topics / learning objectives; `published_curriculum_packages`; Studio foundation subjects / versions / documents / audit events; Alembic version stamp.

---

## Delete Workflow

```text
POST /study-plan/<id>/delete
        │
        ├─ ownership checks
        │
        ├─ EducationalContinuityService.release_plan_planning_artifacts
        │         • missions.study_plan_id → NULL
        │         • research_feedback_submissions.study_plan_id → NULL
        │
        ├─ delete StudyPlan (week_plans cascade)
        │
        ├─ IntegrityError? → ValueError + flash (archive guidance)
        │
        └─ unexpected Exception? → log + flash (no HTTP 500)
```

EIP-005 continuity is unchanged: progress, attempts, missions, and research submissions are retained; only plan pointers and planning rows are removed.

---

## Reset Coverage

### Removed (learner-generated)

Study plans, week plans, missions, mission tasks, topic progress, study attempts, mistakes, decisions, twin snapshots, per-user subjects, research feedback (+ reviews / contributions / badges / findings graph), recommendation commitments, analytics events / outbox / audit, V2 aggregate documents / snapshots / evidence, runtime enrolments / study-plan instances / mission instances / educational events, runtime enrolment routing audits, SCI instances / node states, SDT twin projections.

### Preserved

Founder / Administrator (and any other) user accounts; canonical curricula; Curriculum Studio configuration; published curriculum metadata; system configuration / Alembic.

---

## Validation Results

```bash
python -m pytest \
  tests/test_ux002a_data_lifecycle.py \
  tests/test_internal_alpha_reset.py \
  tests/test_eip005_educational_continuity.py \
  tests/test_services.py::TestStudyPlanService::test_delete_study_plan_removes_plan \
  tests/test_services.py::TestStudyPlanService::test_delete_study_plan_cascades_week_plans \
  tests/test_services.py::TestStudyPlanService::test_delete_study_plan_preserves_topic_progress \
  -q
```

| Suite | Result |
|-------|--------|
| UX-002A delete lifecycle (release + service delete + HTTP route) | **Pass** (3) |
| Internal Alpha reset (including expanded artefacts + idempotency) | **Pass** |
| EIP-005 continuity regressions | **Pass** |
| StudyPlanService delete baselines | **Pass** |
| **Total** | **25 passed** |

Delete validation: temporary Study Plan + research feedback + mission → delete succeeds; feedback/mission retained with `study_plan_id=NULL`; route returns **302**, not **500**.

---

## Idempotency Results

`test_execute_is_idempotent`:

1. Seed full learner history → first `execute()` deletes ≥ 1 row and leaves all `RESET_MODELS` at **0**.  
2. Second `execute()` deletes **0** rows; users and curricula remain.

`preview()` / `execute()` also skip models whose tables are absent (`inspect`), so partial schemas do not break the utility.

---

## Remaining Technical Debt

1. **Filesystem uploads** (`DOCUMENT_STORAGE_ROOT` / instance PDFs) are outside this DB reset — still an ops concern under DP-003 R-C2.  
2. **Founder-authored research product findings** are cleared with the research graph on reset (same as UX-002 ops cleanup). If product findings must survive learner wipe in future, split “learner check-ins” from “Founder findings” into separate reset policies.  
3. Legacy `Query.get()` call sites remain (pre-existing warnings); unrelated to this programme.

---

## Recommendation

1. **Ship as-is** — Study Plan delete is production-safe; `flask internal-alpha-reset --yes` is the sole operator path for Founder baseline restore.  
2. Prefer reset over ad-hoc SQL for any future commercial / Internal Alpha wipe.  
3. After deploy, optionally run reset once on a staging clone to confirm expanded model list against live Postgres inventory.

---

## Files Created

- `tests/test_ux002a_data_lifecycle.py`
- `knowledge/product/ux002_production_state/UX002A_DATA_LIFECYCLE_HARDENING_REPORT.md`

## Files Modified

- `app/services/educational_continuity_service.py`
- `app/services/study_plan_service.py`
- `app/services/internal_alpha_reset_service.py`
- `app/study_plan/routes.py`
- `app/cli.py`
- `tests/test_internal_alpha_reset.py`

## Tests Executed

See Validation Results — **25 passed**.

## Migration Impact

**None** — no Alembic revisions; no schema changes.

## Architecture Compliance

Layering preserved (routes → services → models). Curriculum V1/V2 reference rows remain in the preserve set. EIP-005 educational continuity for Study Plan delete is retained (history not destroyed on plan delete).

## Technical Debt

Listed under Remaining Technical Debt above.

## Known Limitations

Reset does not purge ephemeral document storage. Schema was intentionally not modified (nullable FKs released in application code rather than `ON DELETE SET NULL` DDL).
