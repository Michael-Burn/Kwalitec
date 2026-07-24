# V2-021 — Canonical Runtime Validation

**Branch:** `feature/educational-architecture-consolidation`  
**Date:** 2026-07-23  
**Status:** MANDATORY VALIDATION COMPLETE  
**Mode:** Validation and classification only — no feature work, no UI redesign, no optimisation, no deletions  

**Authority:** [PHASE_0_ARCHITECTURE_INVENTORY.md](PHASE_0_ARCHITECTURE_INVENTORY.md) · [PHASE_1_CANONICAL_DECLARATION.md](PHASE_1_CANONICAL_DECLARATION.md) · [PHASE_1_CONSOLIDATION_REPORT.md](PHASE_1_CONSOLIDATION_REPORT.md)

---

## Recommendation

# NO GO

The Experience projection path (Dashboard / Journey / Revision / Analytics / Coach) correctly consumes a shared `EducationalStateService` snapshot and does not invent readiness, mastery, or progress. That is not yet a single Education Operating System at runtime.

Blocking inconsistencies remain:

1. **Dual educational truth** — default runtime (`KWALITEC_V2_SOLE_RUNTIME` unset / `False`) still serves Legacy Dashboard, Analytics, and Missions via `ReadinessService` / ORM calculators in parallel with Twin-backed Educational State.
2. **Settings / Profile bypass** — `ProfileService` reads Twin ports directly and is **not** wired through `EducationalStateService` (duplicate Twin assembly on Dashboard `include_all_surfaces`).
3. **Incomplete sole-runtime redirects** — only `/dashboard/`, `/analytics/`, and `/missions/` list redirect; nested legacy Session UX (`/missions/<id>/session*`, review shims) remains a live educational path under sole runtime.

Educational correctness is incomplete while two readiness models and two session stacks can serve the same learner. Do not declare consolidation complete. Do not enable sole runtime as the product default until the corrections below land and V2-020 evidence gates pass.

---

## Architecture diagram (validated runtime)

```
                    ┌─────────────────────────────────────┐
                    │     EducationalStateService         │
                    │  (single snapshot cache per learner)│
                    └───────────────┬─────────────────────┘
                                    │
          Twin │ Adaptive │ Mission │ Journey ports (authorities)
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
   HomeService                 JourneyService              RevisionService
   (Dashboard + Coach)         (progress viz)              (Adaptive options)
        │                           │                           │
        └─────────────┬─────────────┴─────────────┬─────────────┘
                      │                           │
                      ▼                           ▼
               HistoryService              ProfileService ⚠
               (Analytics)                 Twin direct — NOT via
                                           EducationalStateService

   Session Experience / Reflection
   ────────────────────────────────
   SessionRuntime / Activity / Twin / Adaptive ports
   (no EducationalStateService; no parallel mastery math)
   Completion → Runtime.complete_session → Twin apply_session_outcome

   Legacy (default dual-run) ⚠
   ────────────────────────────────
   /dashboard  → ReadinessService + RecommendationService + MissionService
   /analytics  → ReadinessService + AnalyticsService
   /missions/* → ReadinessService + StudySessionService (evidence writer)
```

---

## Objective 1 — Educational State verification

| Page | Data source | EducationalStateService? | Additional services | Duplicate calculations? | Independent state? | Result |
|------|-------------|--------------------------|---------------------|-------------------------|--------------------|--------|
| **Dashboard** (`/student/`) | Twin learner + readiness; Adaptive recommendation; Mission session | **Yes** (`HomeService` via shared facade) | `ExplanationService` (wording only); sibling Journey/History/Revision for coach story | No educational formulas | No | **PASS** |
| **Journey** | Journey progress + topic list from Learning Journey port | **Yes** | Status bucketing / label translation only | No | No | **PASS** |
| **Revision** | Adaptive `revision_options` | **Yes** | `ExplanationService` | No | No | **PASS** |
| **Analytics** (`/student/history`) | Twin `learning_insights` | **Yes** | Band labels from existing readiness values | No | No | **PASS** |
| **Coach** (Home panel) | HomeSnapshot explanation / recommendation summary | **Yes** (via Home) | `_compose_coach_insight` clips sentences | No — interpretation only | No | **PASS** |
| **Readiness** (cards on Home / Profile) | Twin `readiness_summary` | **Partial** — Home yes; Profile **no** | Legacy `ReadinessService` still on V1 surfaces | **Yes** vs Legacy ORM composite when dual-run | Profile independent Twin read | **FAIL** |
| **Study Session** (`/session/<id>/*`) | Session Runtime / Activity / Mission ports | **No** (by Phase 1 contract) | Completion may read Twin/Adaptive for summary projection | No mastery math observed | Session workflow state only | **PASS*** |
| **Reflection** (`/session/<id>/reflection`) | Session Runtime reflection payload | **No** | None educational | No | No | **PASS*** |

\*PASS under Phase 1 contract (“consume Twin/session ports; no parallel mastery math”). **FAIL** against a strict reading of “every page must be driven from EducationalStateService.” Session/Reflection are workflow surfaces, not progress dashboards; they must not become a second calculator.

**STOP condition triggered:** Readiness is not a single consumer model across the full product surface (Experience Twin vs Legacy `ReadinessService`). Documented; not hidden.

---

## Objective 2 — End-to-end educational flow

Validated with wired Session Experience test doubles (`tests/presentation/workflows/test_workflow_student_session.py::test_full_session_happy_path`) and Educational State unit assembly.

| Transition | Verified? | Notes |
|------------|-----------|-------|
| Create / obtain study mission | Yes | Mission port `get_todays_session` / Home CTA |
| Open session | Yes | `POST /session/<id>/begin` → Activity |
| Complete study (activity) | Yes | Answer + advance |
| Complete practice | Yes | Activity engine port (fake) |
| Submit reflection | Yes | Continue → Summary |
| Evidence / Runtime close | Yes | `CompletionService` → `runtime.complete_session` |
| Digital Twin updated | Structural path yes | Adapter `apply_session_outcome` / twin_engine when composed; full production Twin soak is V2-020 territory |
| Educational State updated | Yes (on next load) | Snapshot re-assembled from ports; request cache is per assembly, not cross-request |
| Dashboard / Journey / Analytics / Coach / Readiness updated | Yes on Experience path | Projections re-read ports; values agree under shared fake Twin |

### Timing

| Probe | Duration |
|-------|----------|
| Full session happy-path pytest call | **~30 ms** (setup ~490 ms) |
| Four Experience projections (Home+Journey+Revision+History) via shared EducationalState | **&lt; 5 ms** in-process with fakes |
| Screenshots | **Not available** in this validation environment |

---

## Objective 3 — Progress consistency

Same learner (`stu-1`) via `StudentExperienceService` + shared fakes:

| Metric | Dashboard (Home) | Journey | Analytics (History) | Coach | Readiness | Revision | Result |
|--------|------------------|---------|---------------------|-------|-----------|----------|--------|
| Exam readiness | 0.62 | n/a (progress ratio) | progression ends 0.62 | interprets explanation only | 0.62 (Home); Profile 0.62 | n/a | **Agree** (Experience) |
| Study minutes | via History sibling on Home | n/a | 120 | n/a | Profile stats 120 | n/a | **Agree** |
| Topic focus | “Revise equity method” | Current “Equity method” | completed sessions | insight from explanation | n/a | Primary “Equity method” | **Agree** (same topic; display strings differ by field) |
| Journey progress ratio | story uses journey sibling | 0.35 from state | n/a | n/a | n/a | n/a | **Agree** with EducationalState |
| Mission / session handle | mission_id / session_id from state | n/a | n/a | n/a | n/a | n/a | **Agree** |

**FAIL vs Legacy:** Under default dual-run, `/dashboard` and `/analytics` compute readiness via `ReadinessService.get_overall_readiness` — a **different model** from Twin `get_readiness_summary`. Same student can see inconsistent readiness if both stacks are open. This is the primary educational inconsistency.

---

## Objective 4 — Navigation validation

Canonical tree (`app/presentation/student/navigation.py` + `SURFACE_LABELS`):

1. Dashboard → `student.home`  
2. Journey → `student.journey`  
3. Revision → `student.revision`  
4. Analytics → `student.history`  
5. Settings → `student.profile`  
6. Study Plan → `study_plan.index`  
7. Help → `alpha.help_centre`  

| Check | Result |
|-------|--------|
| No duplicate destinations in Experience nav | **PASS** |
| No student-visible “Version 2” / competing-experience CTAs | **PASS** (dual-run + terminology suites) |
| Dead routes in Experience tree | **PASS** (smoke + workflow) |
| Second chrome (V1 sidebar) still present outside sole runtime | **FAIL** for “single navigation” product-wide — intentional dual-run debt |

---

## Objective 5 — Legacy redirect validation

| Legacy route | Sole runtime redirect? | Canonical destination | One hop? | READY FOR RETIREMENT? |
|--------------|------------------------|-----------------------|----------|------------------------|
| `/` (index) | Yes → Student Home when sole | `student.home` | Yes | After V2-020 |
| `/dashboard/` | Yes | `student.home` | Yes | **READY FOR RETIREMENT** (after soak) |
| `/analytics/` | Yes | `student.history` | Yes | **READY FOR RETIREMENT** only after chart parity |
| `/missions/` (list) | Yes | `student.home` | Yes | **READY FOR RETIREMENT** (list chrome) |
| `/missions/<id>/session*` | **No** | Still Legacy LXP | n/a | **Not ready** — must redirect or bridge first |
| `/missions/review/*` | **No** (shim to LXP closure) | Legacy closure | n/a | Keep until Session Experience owns evidence writes |
| V1 sidebar destinations | Still live when dual-run | Competing tree | n/a | After sole runtime + Study Plan host migration |

Redirects do not duplicate Educational State by themselves; they only gate entry. Nested Session gap means sole runtime is **not** a complete single-UX cutover yet.

---

## Objective 6 — Coach validation

| Concern | Result |
|---------|--------|
| Mission / recommendation / next topic | From Educational State (recommendation + session) via HomeSnapshot | **PASS** |
| Revision / study advice | From Adaptive explanation fields; `_compose_coach_insight` clips 2–3 sentences | **PASS** |
| Calculates educational truth? | **No** — presentation interpretation only | **PASS** |
| Extra Adaptive explain call when explanation already embedded | Avoided | **PASS** |

---

## Objective 7 — Readiness validation

| Consumer | Model | Result |
|----------|-------|--------|
| Experience Dashboard readiness card | Twin via EducationalState | **PASS** |
| Experience Analytics progression | Twin insights via EducationalState | **PASS** |
| Mission priority / Adaptive | Adaptive Decision (opaque) via EducationalState | **PASS** |
| Legacy Dashboard / Analytics / Missions | `ReadinessService` ORM composite | **FAIL** — parallel implementation |
| Domain Twin aggregation (`domain/readiness`) | Engine authority for Experience | Protected — not deleted |

**Verdict:** Experience path is single-model. Product runtime is **not**.

---

## Objective 8 — Journey validation

| Check | Result |
|-------|--------|
| Visualises Educational State journey progress / topics | **PASS** |
| Maintains independent progress store | **No** | **PASS** |
| Invents progress ratio | Clamps port value only | **PASS** |

---

## Objective 9 — Technical debt classification

Nothing removed. Classification only.

### Legacy templates

- `templates/dashboard/index.html` and related dashboard partials  
- `templates/analytics/index.html`  
- `templates/mission/session.html` and LXP session templates  
- `templates/partials/sidebar.html` (V1 chrome)

### Legacy routes

- `dashboard.index`, `analytics.index`, `mission.missions`, `mission.study_session*`, `mission.review_*`  
- Root `/` still defaults to Legacy when sole runtime is off

### Legacy services (protected / READY FOR MIGRATION)

- `ReadinessService`, `RecommendationService`, `AnalyticsService`  
- `StudySessionService` + Learning Evidence authority (do not delete)  
- `PlanningService` / ORM `MissionService`  
- Duplicate mission engine packages (`mission_engine` / `mission_engine_v2`) with adapter cutover

### Unused / temporary adapters & compatibility

- `app/presentation/consolidation.redirect_if_sole_runtime` — temporary gate  
- Home/Journey/Revision/History **fallback** constructors without `EducationalStateService` (compat for unit tests / incomplete wiring)  
- `ProfileService` Twin-direct path (should become Educational State consumer)  
- Dual-run diagnostics (`infrastructure/diagnostics/dual_run.py`)  
- Experience projection store defaults when Twin engine absent

### Redirects

- Sole-runtime list redirects: Dashboard, Analytics, Missions list — **keep until retirement**  
- Nested mission session — **gap** (must classify as incomplete cutover)

---

## PASS / FAIL matrix (objectives)

| # | Objective | Result |
|---|-----------|--------|
| 1 | Educational State verification (all pages) | **FAIL** (Readiness/Profile/Legacy; Session* conditional) |
| 2 | End-to-end educational flow | **PASS** (Experience Session path) |
| 3 | Progress consistency | **FAIL** product-wide; **PASS** within Experience EducationalState consumers |
| 4 | Navigation validation | **PASS** Experience tree; **FAIL** single product nav under dual-run |
| 5 | Legacy redirect validation | **FAIL** (nested Session not redirected) |
| 6 | Coach validation | **PASS** |
| 7 | Readiness validation | **FAIL** (parallel `ReadinessService`) |
| 8 | Journey validation | **PASS** |
| 9 | Technical debt classified | **PASS** (inventory only) |
| 10 | GO / NO-GO | **NO GO** |

### GO criteria checklist

| Criterion | Met? |
|-----------|------|
| Single educational truth | **No** |
| Single navigation | **No** (dual chrome while sole off) |
| Single coach | **Yes** (Experience) |
| Single readiness | **No** |
| Single analytics | **No** (History vs `/analytics` charts) |
| Single journey | **Yes** (dedicated Journey surface) |
| Single dashboard | **No** (Home vs Legacy `/dashboard`) |
| Protected educational engine intact | **Yes** |

---

## Rollback risk

| Risk | Severity | Mitigation |
|------|----------|------------|
| Enabling `KWALITEC_V2_SOLE_RUNTIME` now | **High** | Nested LXP Session still reachable; Analytics chart parity incomplete; ADR-007 / V2-020 gates |
| Wiring Profile to EducationalState | Low | Additive; keep Twin as authority |
| Redirecting nested `/missions/<id>/session` | Medium | Must preserve Evidence Authority write path via Session Experience bridge |
| Deleting `ReadinessService` / `StudySessionService` | **Critical — forbidden** | READY FOR MIGRATION only |

Rollback of presentation consolidation: leave sole runtime off (current default); Legacy stack remains authoritative for default `/`.

---

## Required corrections (do not ship around these)

1. **Wire `ProfileService` through `EducationalStateService`** (learner + readiness + insights from the same snapshot).  
2. **Close nested Legacy Session routes under sole runtime** (redirect or bridge to `/session/<id>/*` without breaking evidence writes).  
3. **Treat dual readiness as a known defect until Legacy surfaces redirect or consume Twin readiness** — never paper over with UI.  
4. **Keep sole runtime off** until V2-020 evidence gates + analytics chart parity decision.  
5. **Optional:** remove projection fallbacks that bypass EducationalState once all call sites are wired (tests update in lockstep).

---

## Tests executed

```bash
.venv/bin/python -m pytest \
  tests/application/educational_state/ \
  tests/presentation/student/ \
  tests/presentation/workflows/test_workflow_dual_run.py \
  tests/presentation/workflows/test_workflow_consistency.py \
  tests/presentation/workflows/test_workflow_student_session.py \
  tests/operational/test_alpha_smoke_student.py -q
```

**Outcome:** All collected tests in the above selection **passed** (435 + session/dual-run suites as run during validation).  

Additional in-process probes confirmed shared EducationalState cache for Home/Journey/Revision/History and duplicate Twin reads from Profile on Dashboard `include_all_surfaces`.

---

## Migration impact

**None** — validation document only; no Alembic changes.

---

## Architecture compliance

- Curriculum V1/V2 loadability: **untouched**  
- Twin / Evidence / CMP / Adaptive / Journey engines: **preserved**  
- Layering (presentation → application → ports → engines): **honoured** on Experience path  
- ADR-007: sole runtime **correctly remains default-off**

---

## Next milestone

**V2-023 — Legacy Retirement & Sole Runtime Activation** — see [V2_023_RELEASE_CANDIDATE.md](V2_023_RELEASE_CANDIDATE.md).

V2-022 completeness items closed on the consolidation branch before RC-1:

1. Profile → EducationalStateService  
2. Sole-runtime redirect coverage for nested Legacy Session / review entry points  
3. Readiness consumer alignment on Experience path (shared Educational State)  
4. Production `KWALITEC_V2_SOLE_RUNTIME=1` on Render with rollback documented  

---

## Known limitations of this validation

- No production screenshot capture  
- Twin update after session verified on adapter/contract path, not full production DB Twin soak  
- Live ORM `ReadinessService` numeric divergence vs Twin not exhaustively tabulated for a seeded production-like user (architecture dual-model is sufficient to FAIL)  
- Analytics chart parity intentionally unresolved (Phase 1 stop condition)
