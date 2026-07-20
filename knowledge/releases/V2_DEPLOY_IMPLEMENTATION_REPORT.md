# Version 2 Deploy Remaining — Implementation Report

**Programme:** Version 2 Educational Platform  
**Scope:** Close production gaps from the “What Remains to Deploy Version 2” plan  
**Status:** Implementation complete (sole runtime remains gated)  
**Date:** 2026-07-19  
**Authority:** ADR-007 dual-run exit criteria · [`VERSION2_ROADMAP.md`](../version2/VERSION2_ROADMAP.md) · [`V2_020_RETIREMENT_RUNBOOK.md`](../version2/V2_020_RETIREMENT_RUNBOOK.md)

---

## Summary

This work closed the deploy-remaining gap between a built Version 2 educational kernel / student–session UX and a **production-coexistence** runtime. Before this task, `/student` and `/session` were wired HTTP end-to-end but ran on **in-memory demo stores** without durable ORM persistence, without shared composition between Student and Session Experience, without Founder Studio UI, and without governed dual-run / cutover controls.

Delivered in this task:

1. **V2-018 follow-on (durable Production Experience Integration)** — SQLAlchemy aggregate / snapshot / evidence tables and repositories; parameterized Experience and Session stores; shared projection store between student and session factories; opaque Phase I engine bridges; session ownership hardening (403 on IDOR).
2. **Dual-run operations** — environment feature flags (`KWALITEC_V2_*`), dual-run status diagnostics, dashboard entry link for dual-run cohorts, Render dual-run env defaults (without enabling sole runtime).
3. **V2-016C+ Curriculum Studio UI** — Founder surfaces at `/founder/studio` over Management / Ingestion adapters (no educational math in Flask).
4. **V2-021 Founder Intelligence** — advisory journey-level signals at `/founder/intelligence`.
5. **Evidence gates surface** — ADR-007 / Product Strategy checklist at `/founder/evidence-gates` (product evidence remains operationally open).
6. **V2-020 cutover infrastructure** — retirement runbook plus `KWALITEC_V2_SOLE_RUNTIME` gate that redirects `/` → Student Home only when explicitly set.

**Explicit non-goal of this task:** silently retiring Version 1 or treating package completeness as educational proof. Version 1 remains the default home until evidence gates pass and `SOLE_RUNTIME` is enabled per the runbook.

---

## Context: problem before this work

| Layer | Pre-change state |
|-------|------------------|
| Phase I engines (V2-001…015) | Complete packages under `app/domain/*` and `app/application/*` |
| Student / Session UX | Complete presentation at `/student`, `/session` |
| Experience “production” adapters | Present but defaulted to **seeded demo + in-memory** stores |
| Session document store | Explicitly “No SQLAlchemy. No durable persistence.” |
| Shared state | Separate Student Experience and Session Experience compositions |
| Engine injection | Adapters supported `*_opaque` hooks, but Flask composition did not inject engines |
| Founder Studio UI | Domain/application complete; UI pending (V2-016C+) |
| Cutover | V1 dashboard at `/` remained the live learner path; no V2 sole-runtime flag |

---

## Work by plan todo

### 1. close-v2-018 — Durable wiring, engines, ownership

**ORM models** (`app/models/v2_aggregate.py`):

- `V2AggregateDocument` — versioned opaque JSON documents (`v2_aggregate_documents`)
- `V2AggregateSnapshot` — append-only snapshots (`v2_aggregate_snapshots`)
- `V2EvidenceEvent` — append-only evidence (`v2_evidence_events`)

Registered in `app/models/__init__.py` and imported in `create_app` → `_init_extensions` so metadata is available for `create_all` / migrations.

**SQLAlchemy repositories** (`app/infrastructure/repositories/sqlalchemy/`):

- `SqlAlchemyAggregateRepository` — get/save/delete/list_ids with optimistic locking; commits when UoW is inactive, flushes when UoW is active
- `SqlAlchemySnapshotRepository` — save_snapshot / load_latest
- `SqlAlchemyEvidenceRepository` — append_evidence / list_evidence

Exported from `app/infrastructure/repositories/__init__.py`.

**Alembic:**

- `migrations/versions/202607190001_create_v2_aggregate_tables.py` — creates the three V2 tables (revises twin snapshots head `202611120001`)
- `migrations/versions/202607190002_merge_v2_aggregate_heads.py` — merges heads `202607170003` and `202607190001` so Alembic has a single tip (`202607190002`)

**Store parameterization:**

- `ExperienceProjectionStore` accepts `repository_factory` and `durable_snapshots` instead of hardcoding only `InMemoryAggregateRepository`
- `SessionDocumentStore` optionally backs namespace+id keys through an `AggregateRepository` (LearningSessionDocument aggregate)

**Composition root** (`app/infrastructure/composition.py`):

- `build_experience_projection_store(flags=…)` — durable vs in-memory from V2 flags; wires `SqlAlchemyUnitOfWork(db.session)` when durable
- `build_session_document_store(flags=…, experience_store=…)`
- `build_opaque_engines(flags=…)` — constructs opaque bridges when injection is enabled

**Opaque engine bridges** (`app/infrastructure/engines/opaque_bridges.py`):

- Bridges for Adaptive, Twin, Mission, Journey, Session Runtime, and Activity exposing `*_opaque` methods expected by Experience/Session adapters
- `AdaptiveOpaqueBridge` attempts `AdaptiveDecisionEngine.decide` when signature-compatible; otherwise returns authority-labelled fallback documents (does not invent mastery math)
- Wired from `build_production_experience` / `build_production_session_experience` when `INJECT_PHASE_I_ENGINES` or durable store is on

**Shared store between Student and Session:**

- Student factory stores `EXPERIENCE_PROJECTION_STORE` on the Flask app config
- Session factory reuses that store when present so Twin / Mission / Adaptive projections are shared across surfaces

**Session ownership hardening:**

- New `SessionOwnershipError` in `app/application/session_experience/exceptions.py`
- `assert_session_owned` in presentation views compares workspace `student_id` to `current_user.id`
- Session routes catch ownership errors and `abort(403)`

**Exit criteria met for this todo (technical):** restart-safe persistence path exists when durable flag is on; demo seed defaults off under durable mode unless explicitly overridden; ownership checks on session routes.

---

### 2. dual-run-ops — Flags, observability, coexistence wiring

**Feature flags** (`app/application/config/v2_flags.py`), exported via `app/application/config/__init__.py`:

| Env var | Effect |
|---------|--------|
| `KWALITEC_V2_STUDENT_EXPERIENCE` | Enable dual-run student path / dashboard link |
| `KWALITEC_V2_DURABLE_STORE` | SQLAlchemy-backed Experience/Session stores |
| `KWALITEC_V2_INJECT_ENGINES` | Inject opaque Phase I bridges (also implied by durable) |
| `KWALITEC_V2_SEED_DEMO` | Explicit demo seed override; defaults to off when durable |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | Founder Intelligence enablement flag |
| `KWALITEC_V2_SOLE_RUNTIME` | Cutover: `/` → `student.home` (implies student experience) |

**Dual-run status** (`app/infrastructure/diagnostics/dual_run.py`):

- Projects flags into an ops-facing `DualRunStatus` (`v1-primary` / `dual-run-active` / `sole-runtime-v2`)
- Embeds ADR-007 cutover checklist strings for Founder surfaces

**Dashboard coexistence:**

- `resolve_v2_feature_flags()` passed into dashboard template context as `v2_flags`
- When student experience is on and sole runtime is off, dashboard header shows a dual-run CTA to `/student`

**Deploy config:**

- `.env.example` documents all `KWALITEC_V2_*` variables
- `render.yaml` sets dual-run flags for production coexistence (`STUDENT_EXPERIENCE`, `DURABLE_STORE`, `INJECT_ENGINES`, `SEED_DEMO=0`, `FOUNDER_INTELLIGENCE`) — **does not** set `SOLE_RUNTIME`

---

### 3. studio-ui-016c — Founder Curriculum Studio UI

New presentation package `app/presentation/curriculum_studio/`:

| Module | Role |
|--------|------|
| `__init__.py` | Blueprint `curriculum_studio`, prefix `/founder/studio` |
| `factory.py` | `CurriculumStudioService.create` with `CurriculumManagementAdapter` + `CurriculumIngestionAdapter` |
| `forms.py` | WTForms for subject, workspace, validate, preview, approve, publish, version |
| `view_models.py` | Snapshot → UI projections; workflow stage chrome |
| `views.py` | Dashboard / workspace loaders (DTO fields only) |
| `routes.py` | `@founder_required` thin HTTP handlers |

Templates:

- `app/templates/curriculum_studio/dashboard.html`
- `app/templates/curriculum_studio/workspace.html`

Registration in `app/__init__.py` `_register_blueprints` via `load_studio_routes()` + `studio_bp`.

Founder nav updates (`app/founder/dashboard/nav.py`):

- Primary nav item **Studio** → `curriculum_studio.index`
- `active_section_id` maps `curriculum_studio.*` endpoints to `studio`
- Context processor treats `curriculum_studio.*` as Founder Command Centre chrome

Roadmap: V2-016C+ marked complete in `VERSION2_ROADMAP.md`; README Studio blurb updated to include presentation package.

---

### 4. founder-intel-021 — Founder Intelligence

Package `app/founder/intelligence/`:

- `FounderIntelligenceService.build(...)` reads Experience projection store documents when available
- Emits advisory signals only: inactive journeys, stalled completion, reflection gaps, recommendation thrash
- Explicit notes that Founder Intelligence must not mutate Learning Mode

Route: `GET /founder/intelligence` (`founder_dashboard.founder_intelligence`)  
Template: `founder_dashboard/founder_intelligence.html`  
Nav: primary **Intelligence** item

---

### 5. evidence-gates — Product Strategy / ADR-007 checklist surface

Service `app/infrastructure/diagnostics/evidence_gates.py`:

- Builds `EvidenceGatesReport` with six gates aligned to ADR-007
- Marks **product_evidence** as not technically auto-satisfied (requires real alpha observation)
- Other gates reflect dual-run flag / durable / engine / studio readiness hints

Route: `GET /founder/evidence-gates`  
Template: `founder_dashboard/evidence_gates.html`  
Secondary nav: **Evidence Gates**

This implements the **operational checklist surface** for evidence gates — it does not invent or claim that Internal Alpha product evidence has been collected.

---

### 6. v2-020-cutover — Gated retirement infrastructure

**Runbook:** [`knowledge/version2/V2_020_RETIREMENT_RUNBOOK.md`](../version2/V2_020_RETIREMENT_RUNBOOK.md)

- Preconditions, dual-run phase, sole-runtime steps, rollback, must-nots
- Environment blocks for dual-run vs sole runtime

**Code gate:**

- `app/__init__.py` index route: if `SOLE_RUNTIME`, redirect to `student.home`; otherwise `dashboard.index`

**Roadmap:** V2-020 marked “Runbook ready — execute only after ADR-007 evidence gates”.

Sole runtime was **not** enabled in Render or defaults.

---

## Files Created

### Persistence / infrastructure

- `app/models/v2_aggregate.py`
- `app/infrastructure/repositories/sqlalchemy/__init__.py`
- `app/infrastructure/repositories/sqlalchemy/aggregate_repository.py`
- `app/infrastructure/repositories/sqlalchemy/snapshot_repository.py`
- `app/infrastructure/repositories/sqlalchemy/evidence_repository.py`
- `app/infrastructure/composition.py`
- `app/infrastructure/engines/__init__.py`
- `app/infrastructure/engines/opaque_bridges.py`
- `app/infrastructure/diagnostics/dual_run.py`
- `app/infrastructure/diagnostics/evidence_gates.py`
- `migrations/versions/202607190001_create_v2_aggregate_tables.py`
- `migrations/versions/202607190002_merge_v2_aggregate_heads.py`

### Application / config

- `app/application/config/v2_flags.py`

### Founder Intelligence

- `app/founder/intelligence/__init__.py`
- `app/founder/intelligence/service.py`

### Curriculum Studio presentation

- `app/presentation/curriculum_studio/__init__.py`
- `app/presentation/curriculum_studio/factory.py`
- `app/presentation/curriculum_studio/forms.py`
- `app/presentation/curriculum_studio/view_models.py`
- `app/presentation/curriculum_studio/views.py`
- `app/presentation/curriculum_studio/routes.py`
- `app/templates/curriculum_studio/dashboard.html`
- `app/templates/curriculum_studio/workspace.html`

### Founder templates (new)

- `app/founder/dashboard/templates/founder_dashboard/founder_intelligence.html`
- `app/founder/dashboard/templates/founder_dashboard/evidence_gates.html`

### Docs / ops

- `knowledge/version2/V2_020_RETIREMENT_RUNBOOK.md`
- `knowledge/releases/V2_DEPLOY_IMPLEMENTATION_REPORT.md` (this file)

### Tests

- `tests/application/config/__init__.py`
- `tests/application/config/test_v2_flags.py`
- `tests/infrastructure/repositories/test_sqlalchemy_repositories.py`
- `tests/presentation/session/test_ownership.py`
- `tests/presentation/curriculum_studio/__init__.py`
- `tests/presentation/curriculum_studio/test_studio_factory.py`

---

## Files Modified

### Persistence / composition wiring

- `app/infrastructure/adapters/student_experience/projection_store.py` — repository factory + durable snapshots
- `app/infrastructure/session/store.py` — optional AggregateRepository backing
- `app/infrastructure/adapters/student_experience/composition.py` — flags, shared store, engine injection
- `app/infrastructure/session/composition.py` — same for Session Experience
- `app/infrastructure/repositories/__init__.py` — export SQLAlchemy repos
- `app/models/__init__.py` — export V2 aggregate models
- `app/presentation/student/factory.py` — build/share durable store on app config
- `app/presentation/session/factory.py` — reuse shared store + durable session docs

### Security / session presentation

- `app/application/session_experience/exceptions.py` — `SessionOwnershipError`
- `app/application/session_experience/__init__.py` — export ownership error
- `app/presentation/session/views.py` — ownership asserts
- `app/presentation/session/routes.py` — 403 on ownership failure

### Dual-run / cutover / app shell

- `app/application/config/__init__.py` — export V2 flags
- `app/config.py` — unchanged (flags live in application config module)
- `app/__init__.py` — model imports, studio blueprint, sole-runtime index redirect
- `app/dashboard/routes.py` — pass `v2_flags` to template
- `app/templates/dashboard/index.html` — dual-run CTA
- `.env.example` — document `KWALITEC_V2_*`
- `render.yaml` — dual-run env (no sole runtime)

### Founder shell

- `app/founder/dashboard/routes.py` — intelligence + evidence-gates routes; nav chrome for studio
- `app/founder/dashboard/nav.py` — Studio, Intelligence, Evidence Gates nav entries / section mapping

### Knowledge

- `knowledge/version2/VERSION2_ROADMAP.md` — V2-016C+, V2-018, V2-021, V2-020 status notes
- `knowledge/version2/README.md` — Studio presentation + retirement runbook + pointer to this report

---

## Behavioural outcomes

```text
Default (no V2 flags)
  / → dashboard (V1)
  /student, /session available but demo/in-memory unless durable flag set

Dual-run (Render defaults after this change)
  KWALITEC_V2_STUDENT_EXPERIENCE=1
  KWALITEC_V2_DURABLE_STORE=1
  KWALITEC_V2_INJECT_ENGINES=1
  KWALITEC_V2_SEED_DEMO=0
  / → still V1 dashboard
  Dashboard shows link to /student
  Experience docs persist in v2_* tables after flask db upgrade

Sole runtime (manual, after evidence)
  KWALITEC_V2_SOLE_RUNTIME=1
  / → student.home
  Follow V2_020_RETIREMENT_RUNBOOK.md
```

Founder surfaces added:

| URL | Purpose |
|-----|---------|
| `/founder/studio` | Curriculum Studio dashboard |
| `/founder/studio/workspaces/<id>` | Validate / preview / approve / publish / version |
| `/founder/intelligence` | Advisory journey signals |
| `/founder/evidence-gates` | ADR-007 readiness checklist |

---

## Tests Executed

```bash
python3 -m pytest \
  tests/application/config/test_v2_flags.py \
  tests/infrastructure/repositories/test_sqlalchemy_repositories.py \
  tests/presentation/session/test_ownership.py \
  tests/presentation/curriculum_studio/test_studio_factory.py \
  -q
# Result: 12 passed

python3 -m pytest \
  tests/infrastructure/session/test_independence.py \
  tests/infrastructure/adapters/student_experience/test_persistence_regression.py \
  -q
# Result: 23 passed

python3 -m ruff check \
  app/presentation/curriculum_studio \
  app/infrastructure/engines \
  app/infrastructure/composition.py \
  app/founder/intelligence \
  app/infrastructure/diagnostics/dual_run.py \
  app/infrastructure/diagnostics/evidence_gates.py \
  app/infrastructure/repositories/sqlalchemy \
  ...
# Result: All checks passed
```

App factory smoke check confirmed blueprints for `/founder/studio`, `/founder/intelligence`, `/founder/evidence-gates`, `/student`, `/session`, and default `/` → `/dashboard/` without sole runtime.

---

## Migration Impact

| Revision | Role |
|----------|------|
| `202607190001` | Creates `v2_aggregate_documents`, `v2_aggregate_snapshots`, `v2_evidence_events` |
| `202607190002` | Empty merge of `202607170003` + `202607190001` → single Alembic head |

**Required for durable mode in any environment:**

```bash
flask db upgrade
# head should be 202607190002
```

No drops of Version 1 tables. Additive only. Curriculum V1/V2 JSON traversal untouched.

---

## Architecture Compliance

- **Layering preserved:** educational law stays in Phase I engines; adapters/stores hold opaque documents; Flask routes remain thin.
- **ADR-005:** Adaptive Decision remains next-action authority on V2 paths; bridges do not introduce a second recommendation authority in presentation.
- **ADR-007:** V1 safe until explicit cutover; feature flags + observability before traffic flip; sole runtime gated.
- **Curriculum V1/V2 (syllabus formats):** unchanged and still loadable.
- **StartupService:** no destructive migration behaviour introduced.

---

## Technical Debt

1. **Opaque bridges are projection bridges**, not a full deep wiring of every Phase I facade method for all learner contexts (e.g. `AdaptiveDecisionEngine.decide` still requires a real `TwinSnapshot` for full decision quality; bridge falls back safely when that path is unavailable).
2. **ExperienceTwin projection docs** remain separate from durable `TwinSnapshot` ORM history (`TwinRepository`) — intentional for Experience opacity, but long-term unification may be needed for continuity migration (called out as a later programme in ADR-007 / Migration Strategy).
3. **Studio UI** covers dashboard + workspace actions; rich source-upload / blueprint-assignment UX may still expand as Founder workflows deepen.
4. **`datetime.utcnow` deprecation warnings** on new ORM defaults (same pattern as existing Twin snapshot model); cleanup is cosmetic.

---

## Known Limitations

- Enabling durable flags without running Alembic leaves SQLAlchemy writes failing until `flask db upgrade`.
- Product Strategy **evidence gates** are surfaced and technically hinted; **passing them requires real Internal Alpha observation** — this report does not claim that evidence was collected.
- `KWALITEC_V2_SOLE_RUNTIME` must not be set in production until the retirement runbook preconditions are met.
- Session ownership protects workspaces already bound to a student; first-touch open of an unbound `session_id` still materialises a workspace for the current user (expected create-on-open behaviour).

---

## Recommended next ops steps (outside this code change)

1. Deploy with dual-run env (already sketched in `render.yaml`).
2. Run `flask db upgrade` to head `202607190002`.
3. Invite alpha cohort via dashboard dual-run link; exercise `/student` → `/session` → complete.
4. Monitor `/founder/intelligence` and `/founder/evidence-gates`.
5. Only after evidence recording: execute [`V2_020_RETIREMENT_RUNBOOK.md`](../version2/V2_020_RETIREMENT_RUNBOOK.md).

---

## Related documents

- [`VERSION2_ROADMAP.md`](../version2/VERSION2_ROADMAP.md)
- [`PRODUCTION_INTEGRATION.md`](../version2/PRODUCTION_INTEGRATION.md)
- [`AUTHORITY_MATRIX.md`](../version2/AUTHORITY_MATRIX.md)
- [`ADR-007-Legacy-Retirement-Strategy.md`](../version2/ARCHITECTURE_DECISIONS/ADR-007-Legacy-Retirement-Strategy.md)
- [`V2_020_RETIREMENT_RUNBOOK.md`](../version2/V2_020_RETIREMENT_RUNBOOK.md)
- [`CURRICULUM_STUDIO.md`](../version2/CURRICULUM_STUDIO.md)
- [`LEARNING_SESSION_EXPERIENCE.md`](../version2/LEARNING_SESSION_EXPERIENCE.md)
- [`STUDENT_EXPERIENCE.md`](../version2/STUDENT_EXPERIENCE.md)
