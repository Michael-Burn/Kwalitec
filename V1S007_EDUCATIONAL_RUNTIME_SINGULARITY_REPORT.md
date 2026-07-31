# V1S-007 — Educational Runtime Singularity Report

**Programme:** V1S-007 · Version 1 Stabilisation  
**Phase:** Educational Runtime Consolidation  
**Date:** 2026-07-31  
**Authority:** V1S-006 · V1S-005 · `V1_RELEASE_CRITERIA.md` · `PRODUCT_BLUEPRINT.md`  
**Nature:** Architectural consolidation only — not educational intelligence, not UI redesign

---

## 1. Executive Summary

V1S-007 establishes permanent architecture principle **A9 — Educational Runtime Singularity**: every student educational interaction for Runtime C enrolments executes through one Educational Runtime. Missing Student Curriculum Instance (SCI) no longer triggers a Runtime A fallback.

**What changed**

- SCI is ensured on Runtime C enrolment, Home load, Session start, session briefing, and evidence hooks.
- When no published CKG edition exists, Educational Runtime provisions a **CKG bridge edition** from the active `PublishedCurriculumPackage`, then onboard creates SCI.
- If SCI still cannot be created, the student receives an **Educational Readiness Message** (`EducationalPrerequisiteMissing`) — never PlanningService / MissionStartAdapter.
- Learning Journey crash (DF-015) fixed as part of journey verification.
- DF-014 (SCI / Runtime A fallback) marked **RESOLVED**.

**Verdict:** Educational Runtime Singularity for Runtime C student paths is **PASS**. Exclusive dogfood week remains HOLD on DF-013 (xp scrub) and incomplete consecutive live days — out of V1S-007 scope.

---

## 2. Runtime Ownership Matrix

| Component | Owner | Entry point | Status |
|---|---|---|---|
| Educational Runtime | `educational_runtime_engine` | `EducationalRuntimeEngineService` + `ensure_active_sci` | ACTIVE — A9 owner |
| Student Curriculum Instance | `student_curriculum_binding` + `sci_lifecycle` | `ensure_active_sci` | ACTIVE — mandatory |
| Published Curriculum | `PublishedCurriculumAuthority` | `get_active` | ACTIVE |
| Session Runtime | `learning_session` | `LearningSessionRuntime` | ACTIVE |
| Session spine glue | `student_runtime` | `StudentRuntimeCoordinator` | ACTIVE |
| Evidence | `EducationalEvidenceAuthority` | evidence services | ACTIVE |
| Progress | `ProgressEngine` | `app.application.progress_engine` | ACTIVE |
| Learning Journey | `educational_memory` + `readiness_forecast` | journey / forecast engines | ACTIVE |
| Educational Authoring | `educational_authoring` | composer | ACTIVE (out of redesign scope) |
| Mission Runtime | ERE + `CertifiedMissionEngine` | generate / accept | ACTIVE |
| JSON / Runtime A substrate | `CurriculumService` / `PlanningService` | import / legacy | SUBSTRATE / TEMPORARY (RI-002) |
| MissionEngineV2 | `mission_engine_v2` | — | ARCHIVE |
| MissionAdapter | `mission_adapter` | — | ARCHIVE |

Canonical registry: `app/services/runtime_ownership.py` (`A9_EDUCATIONAL_RUNTIME_SINGULARITY`, `RUNTIME_OWNERSHIP_MATRIX`, `MISSION_SPINE`).

### Student-facing route ownership (post V1S-007)

| Route | Runtime | Authority | Status |
|---|---|---|---|
| Home (`/student/`) | Educational Runtime (when enrolled) | Published Curriculum | PASS |
| Syllabus Journey (`/student/journey`) | Educational Runtime (when enrolled) | Published Curriculum | PASS |
| Session start (`POST /student/session/start`) | Educational Runtime + LSR | Educational Runtime | PASS — no Runtime A fallback |
| Session surfaces (`/session/*`) | Learning Session Runtime | Educational Runtime | PASS |
| Sitting Report / summary | Learning Session Runtime | Educational Runtime | PASS |
| My Learning Journey | Educational Memory / Forecast | Educational Runtime path | PASS (DF-015 fixed) |
| Revision begin | Same session spine as Home | Educational Runtime when enrolled | PASS |
| Legacy `/dashboard`, `/mission` | TEMPORARY / DEPRECATED | RI-002 | INTERNAL ONLY — not Runtime C fallback |

---

## 3. Educational Runtime Singularity Review

### A9 — adopted

> Every student educational interaction shall execute through one Educational Runtime. Legacy implementations may temporarily remain inside the repository but shall never become an alternative educational execution path. Missing prerequisites shall be resolved or surfaced by the Educational Runtime itself. Student routing into legacy educational infrastructure is prohibited **as a fallback from Educational Runtime**.

### Before (V1S-006 Day 1)

```
Educational Runtime (Home OK)
        ↓
SCI missing
        ↓
ri001_runtime_a_fallback / Session → Runtime A
```

### After (V1S-007)

```
Educational Runtime
        ↓
SCI missing
        ↓
ensure_active_sci
  → published CKG edition, or
  → CKG bridge from PublishedCurriculumPackage
        ↓
SCI created → continue Session
   OR
EducationalPrerequisiteMissing → readiness message → Stop
```

Never: Runtime A as educational execution for an enrolled Runtime C student.

---

## 4. Student Curriculum Instance Lifecycle

| Stage | Behaviour | Owner |
|---|---|---|
| **Creation** | Enrolment bridge (`FounderStudentEnrolmentBridge._enrol_runtime_c`), first Home load, Session start, session briefing, evidence hook via `ensure_active_sci` | Educational Runtime `sci_lifecycle` |
| **Activation** | `SciStudentCurriculumInstance.is_active=True` for subject; one active SCI per student+subject | `StudentCurriculumBindingService` |
| **Persistence** | ORM table `sci_student_curriculum_instances` + node states | EI-004 binding |
| **Completion** | Existing `is_completed` / `completed_at` fields (unchanged) | Binding domain |
| **Retirement** | Inactive / superseded by invariant when rebound to another edition | Binding invariants |
| **Ownership** | Educational Runtime owns *when* SCI must exist; binding package owns *how* rows are written | A9 |

**Session rule:** Session assumes SCI already exists. Session creation never selects runtime ownership. If SCI is missing at Session start → ensure or raise — never change runtime.

---

## 5. Runtime Transition Audit

| Transition | Location | Classification | Disposition |
|---|---|---|---|
| Runtime C → Runtime A on Session start | `start_todays_session` fall-through | **REMOVED** | Raises `EducationalPrerequisiteMissing` when Runtime C enrolled |
| Runtime C Home → Runtime A on load failure | `load_page` | **REMOVED** | Readiness empty page when Runtime C enrolled |
| SCI missing → `ri001_runtime_a_fallback` telemetry | RIS / session briefing | **MITIGATED** | SCI ensured before RIS resolve for Runtime C |
| Non–Runtime-C student → Experience / PlanningService | `start_todays_session` legacy branch | **TEMPORARY** | RI-002 hard removal; not a Runtime C fallback |
| Enrolment routing JSON vs published | `RuntimeRoutingService` | **INTERNAL** | Enrolment-time authority selection only |
| MissionEngineV2 / MissionAdapter | packages | **ARCHIVE** | Unwired |

**Expected Runtime Transition Register for Runtime C → Runtime A educational fallback: NONE.**

---

## 6. Legacy Compatibility Register

| Dependency | Classification | Justification / removal strategy |
|---|---|---|
| `PlanningService.generate_today_mission` | TEMPORARY | Non–Runtime-C students only until RI-002 |
| `MissionStartAdapter` | TEMPORARY | Same |
| `StudentExperienceService` (Runtime A Home) | TEMPORARY | Students without Runtime C enrolment |
| `dashboard` / `mission` blueprints | INTERNAL ONLY / DEPRECATED | Deep links; Sole Runtime redirects Home |
| `MissionEngineV2` | ARCHIVE | Tests-only; REMOVE when independence tests migrate |
| `MissionAdapter` | ARCHIVE | Tests-only |
| `CurriculumService` JSON import | SUBSTRATE | On-disk syllabus loader — not student authority when published package active |
| RI-001 `runtime_a_fallback` callable | INTERNAL ONLY | Callers pass `lambda: None`; telemetry remains for metrics until RI-002 |
| Opaque session demo bridges | TEMPORARY | Fail-closed before stub deletion (existing debt) |

Nothing remains “because it works” without classification.

---

## 7. Educational Runtime Verification

| Check | Evidence |
|---|---|
| SCI auto-created on Runtime C enrol | `tests/test_v1s007_educational_runtime_singularity.py::test_sci_auto_created_on_runtime_c_enrolment` |
| SCI ensure idempotent | `test_ensure_sci_idempotent` |
| CKG bridge from published package | `test_ckg_bridge_from_published_package` |
| Missing prerequisites reported | `test_ensure_sci_reports_missing_prerequisites` |
| Session never routes Runtime C → Runtime A | `test_session_never_routes_runtime_c_to_runtime_a` |
| Single mission spine | `test_mission_spine_is_single_pipeline` |
| Progress owner = ProgressEngine | `test_progress_engine_is_sole_progress_owner` |
| A9 in release criteria | `V1_RELEASE_CRITERIA.md` row A9; `test_release_criteria_includes_a9` |

**Pipeline (sole):**

Published Curriculum → SCI → Educational Runtime → Learning Session → Evidence → Progress → Learning Journey

---

## 8. Student Journey Verification

| Step | Runtime | Notes |
|---|---|---|
| Home | Educational Runtime | SCI ensure soft on load |
| Morning Brief / Today's Mission / Episode | Educational Runtime + Authoring | Unchanged composition (out of scope) |
| Start Session | Educational Runtime → Coordinator → LSR | SCI ensure require=True |
| Learning Session | LSR | No PlanningService |
| Evidence | LP-001 / evidence hook | SCI ensure before skip |
| Sitting Report | LSR summary | Same session authority |
| Learning Journey | Memory + Forecast | DF-015 shell_vm keyword fix |

Verified: one runtime (for Runtime C), one progress engine, one curriculum authority (published package), one session runtime, one evidence path. No legacy execution on this journey.

---

## 9. Architecture Compliance

- Layering preserved: routes → presentation views → Educational Runtime / coordinator → binding / LSR.
- Curriculum V1/V2 loaders untouched (`CurriculumRepository.load_auto` singularity intact).
- No new educational intelligence algorithms.
- No UI redesign beyond fixing Learning Journey crash and readiness flash messages.
- A9 recorded in `runtime_ownership.py` and `V1_RELEASE_CRITERIA.md`.
- CKG bridge is substrate alignment (Published package → CKG edition for SCI binding), not a new recommendation engine.

---

## 10. Technical Debt Remaining

| Item | Severity | Notes |
|---|---|---|
| DF-013 xp scrub | P0 | Educational Authoring copy — out of V1S-007 scope |
| DF-016 title/duration mismatch | P1 | Continuity polish — out of scope |
| RI-002 Runtime A hard removal | High | TEMPORARY legacy path for non–Runtime-C students |
| CKG bridge vs full CKG extraction | Medium | Bridge editions use ordered `CS1.Tnn` ids from package topics; full CMP CKG remain preferred when published |
| Legacy dashboard / mission blueprints | Medium | Archive after Sole Runtime adoption complete |
| MissionEngineV2 / MissionAdapter packages | High | Still ARCHIVE in-repo |

---

## 11. Tests Executed

```text
python3 -m pytest tests/test_v1s007_educational_runtime_singularity.py \
  tests/test_v1s005_dogfood_remediation.py \
  tests/test_v1s006_dogfood_week.py -q
```

Expected: all PASS after this report lands.

Also:

```text
python3 -m ruff check app/application/educational_runtime_engine/ \
  app/presentation/student/views.py app/presentation/student/routes.py \
  app/application/platform_integration/enrolment_bridge.py \
  app/presentation/session/views.py \
  app/infrastructure/adapters/learner_lifecycle/evidence_hook.py \
  app/services/runtime_ownership.py \
  tests/test_v1s007_educational_runtime_singularity.py
```

---

## 12. Migration Impact

**None.** No Alembic migrations. SCI / CKG bridge use existing tables (`sci_student_curriculum_instances`, `ckg_graph_editions`, `ckg_subjects`, `ckg_topics`).

---

## 13. Version 1 Readiness Impact

| Criterion | Result |
|---|---|
| Runtime Ownership Audit complete | PASS |
| Educational Runtime Singularity implemented | PASS |
| Student-facing Runtime A fallback eliminated (Runtime C) | PASS |
| SCI lifecycle complete | PASS |
| One Educational Pipeline | PASS |
| Runtime Transition Register empty (C→A fallback) | PASS |
| Legacy Compatibility Register produced | PASS |
| Home → Session → Sitting Report → Learning Journey one runtime | PASS |
| No educational fallback remains (for Runtime C) | PASS |
| A9 in `V1_RELEASE_CRITERIA.md` | PASS |

**Dogfood week:** still **HOLD** — DF-013 open; consecutive live days incomplete. Private beta remains **NO-GO** until exclusive week bar is met after DF-013.

**CRI / KSI:** ΔCRI = 0 (architecture consolidation; no commercial validation run). ΔKSI provisional architecture contribution via E8 (no dual educational truths on Runtime C path) — not claimed as validated KSI.

---

## Files Created

- `app/application/educational_runtime_engine/sci_lifecycle.py`
- `tests/test_v1s007_educational_runtime_singularity.py`
- `V1S007_EDUCATIONAL_RUNTIME_SINGULARITY_REPORT.md`

## Files Modified

- `app/application/educational_runtime_engine/__init__.py`
- `app/application/educational_runtime_engine/exceptions.py`
- `app/application/educational_runtime_engine/coexistence.py`
- `app/application/platform_integration/enrolment_bridge.py`
- `app/presentation/student/views.py`
- `app/presentation/student/routes.py`
- `app/presentation/session/views.py`
- `app/infrastructure/adapters/learner_lifecycle/evidence_hook.py`
- `app/services/runtime_ownership.py`
- `app/services/dogfood_validation.py`
- `app/services/v1_readiness_dashboard.py`
- `V1_RELEASE_CRITERIA.md`
- `tests/test_v1s005_dogfood_remediation.py`
- `tests/test_v1s006_dogfood_week.py`
