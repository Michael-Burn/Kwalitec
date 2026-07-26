# MS-002 Engineering Directive 001 / 002 / 003 — Educational Journey Bridge Architecture

**Milestone:** MS-002 — Educational Continuity  
**Directives:** Engineering Directive 001 (Architecture Design); Engineering Directive 002 (Journey Read Bridge); Engineering Directive 003 (History Read Bridge)  
**Status:** Architecture Design complete; **Journey Read Bridge (J1) — Implemented**; **History Read Bridge (J2) — Implemented**  
**Companions:** `JOURNEY_SEQUENCE_DIAGRAM.md`, `HISTORY_SEQUENCE_DIAGRAM.md`, `JOURNEY_INTERFACE_SPECIFICATION.md`, `JOURNEY_DATA_MODEL.md`, `JOURNEY_TRACEABILITY_MATRIX.md`, `MIGRATION_PLAN_MS002.md`, `RISK_ANALYSIS_MS002.md`  
**Prior foundation:** MS-001 Educational Runtime Bridge (`EDUCATIONAL_RUNTIME_BRIDGE.md`) — Mission Read / Start / Resume / Session Completion / Recommendation Read implemented

---

## 0. Implementation status (Directives 002–003)

| Component | Status | Notes |
|---|---|---|
| **Journey Adapter** (`JourneyBridge` read) | **Implemented** | `app/infrastructure/adapters/educational_runtime_bridge/journey_adapter.py` |
| **History Adapter** (`HistoryBridge` read) | **Implemented** | `app/infrastructure/adapters/educational_runtime_bridge/history_adapter.py` |

### Bridge Coverage

| Bridge | Status |
|---|---|
| Mission Read | **Implemented** (MS-001) |
| Mission Start | **Implemented** (MS-001) |
| Mission Resume | **Implemented** (MS-001) |
| Session Completion | **Implemented** (MS-001) |
| Recommendation | **Implemented** (MS-001) |
| Journey | **Implemented** |
| History | **Implemented** |

### Journey Read Bridge — implementation notes

- **Flags:** `KWALITEC_JOURNEY_BRIDGE` and umbrella `KWALITEC_EDUCATIONAL_CONTINUITY_BRIDGE` (also enabled by `KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE`) → `Version2FeatureFlags.ENABLE_JOURNEY_BRIDGE` (default **off**).
- **Path:** Experience `LearningJourneyPort` → `ExperienceJourneyAdapter` → `JourneyAdapter` → StudyPlan / Mission / StudyAttempt / TopicProgress / Lifecycle / Readiness → SQL.
- **Translator only:** projects Runtime A records into opaque Journey DTOs; does **not** calculate mastery/readiness formulas, alter evidence, create timeline events as authority, or write educational state.
- **No demo fallback:** when the bridge is on and Runtime A has no plan, returns empty authentic (`has_journey=false`, `NO_ACTIVE_PLAN`); never `seeded_demo_journey`.
- **Traceability:** every timeline item carries `trace` (what / why / evidence_refs / recommendation). Missing recommendation history returns explicit null contracts (`recommendation_history: null`, `unavailable_reason: "unavailable"`).
- **Rollback:** disable the flag — prior Experience / seed journey behaviour restored immediately.
- **Telemetry (observational):** `JOURNEY_BRIDGE_REQUESTED`, `JOURNEY_BRIDGE_SUCCESS`, `JOURNEY_BRIDGE_FAILURE`, `JOURNEY_BRIDGE_LATENCY`.
- **Tests:** `tests/infrastructure/adapters/educational_runtime_bridge/test_journey_*.py` (unit, integration, contract, behavioural parity).

### History Read Bridge — implementation notes

- **Flags:** `KWALITEC_HISTORY_BRIDGE` and umbrella `KWALITEC_EDUCATIONAL_CONTINUITY_BRIDGE` (also enabled by `KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE`) → `Version2FeatureFlags.ENABLE_HISTORY_BRIDGE` (default **off**).
- **Path:** Experience `HistoryService` → `HistoryAdapter` → StudyAttempt / Mission / TopicProgress / Lifecycle → SQL.
- **Translator only:** projects Runtime A records into opaque History DTOs; does **not** calculate educational state, infer recommendation history, create timeline entries as authority, or write SQL.
- **Canonical event stream:** shares `canonical_event_stream.py` with Journey so ordering, timestamps, and evidence refs stay identical (narrative consistency).
- **Pagination:** offset + optional cursor (`before_date:id`); hard max 100; deterministic reverse-chronological order by `mission_date` then `id`.
- **No demo fallback:** when the bridge is on, Twin demo insights are not used for History; empty authentic sessions when Runtime A has none.
- **Missing data:** recommendation history and durable readiness progression return explicit null contracts (`unavailable_reason: "unavailable"`); never fabricated.
- **Rollback:** disable the flag — prior Twin insights History path restored immediately.
- **Telemetry (observational):** `HISTORY_BRIDGE_REQUESTED`, `HISTORY_BRIDGE_SUCCESS`, `HISTORY_BRIDGE_FAILURE`, `HISTORY_BRIDGE_LATENCY`.
- **Tests:** `tests/infrastructure/adapters/educational_runtime_bridge/test_history_*.py` (unit, integration, contract, behavioural parity / narrative consistency).

---

## 0b. Constraints (binding for architecture directive)

| Constraint | Meaning |
|---|---|
| Architecture only (Directive 001) | No production code in Directive 001 |
| Implementation (Directive 002) | Journey Read Bridge only — stop before History |
| Implementation (Directive 003) | History Read Bridge only — stop before Adaptive / Revision |
| No schema changes | Reuse existing SQL tables / models |
| No UI redesign | Existing Journey / History templates and view models remain |
| Runtime A authority | All educational narrative originates from legacy SQL educational services |
| Read-only adapters | Journey and History bridges never write educational state |

---

## 1. Purpose

Design the architecture so Experience **Journey** and **History** present a complete, authoritative learning narrative sourced **exclusively** from Runtime A.

MS-001 established Runtime A as the single educational authority for Mission Read, Start, Resume, Session Completion, and Recommendation Projection. Journey and History still rely on Experience-side projections (`seeded_demo_journey`, Twin insights seeded with fabricated sessions). This directive designs the **read-only continuity bridges** that close that gap.

**Non-goals for this directive:**

- Implementing Journey or History adapters  
- Redesigning student UI  
- Changing Alembic schemas  
- Replacing Runtime A with V2 `LearningJourneyEngine` as writer  
- Implementing Revision begin (covered under MS-001 P5 Revision slice; referenced only for continuity)

---

## 2. Problem statement

| Surface | Current source | Problem |
|---|---|---|
| Journey (`student.journey` + Home journey card) | `seeded_demo_journey` via `LearningJourneyPort` / `ExperienceProjectionStore` | Fabricated progress ratio, topics, and completion labels — not StudyPlan / TopicProgress |
| History (`student.history` + Home history card) | Twin `insights` (demo-seeded completed sessions, readiness series) | Fabricated session cards and readiness points — not Mission / StudyAttempt |
| Traceability | Absent on Experience | Student cannot answer “what happened / why / which evidence / which recommendation changed” |

This violates DP-013 (Continuity of Learning History) and Foundational Trust: educational narrative must not be invented by Experience.

---

## 3. Architectural decision (summary)

**Decision:** Introduce **JourneyBridge** and **HistoryBridge** as read-only Educational Runtime Bridge adapters that project Runtime A educational records into existing Experience ports / facades — without calculating educational state in Experience or the adapter.

**Runtime A remains the sole educational authority.** Adapters translate and project only.

**ADR required:** ADR-MS002-001 (see §12). Companion ADRs may be required for readiness time-series derivation and recommendation-history linkage (see Final Report).

---

## 4. Bridge placement

```
Templates / JS (journey.html, history.html, Home cards)
      ↓
Presentation (student blueprints / view models)
      ↓
Application facades (JourneyService, HistoryService, StudentExperienceService)
      ↓
Experience Ports (LearningJourneyPort, StudentTwinPort insights / History reads)
      ↓
╔══════════════════════════════════════════════════════╗
║  JOURNEY BRIDGE / HISTORY BRIDGE (new MS-002 seam)   ║
║  Read-only translators + DTO projection + telemetry  ║
╚══════════════════════════════════════════════════════╝
      ↓
Canonical Educational Services (Runtime A)
      ↓
SQL models / Curriculum Engine / Evidence Authority
```

**Invariants (inherited from MS-001, extended):**

- Experience facades never import `app/services/*` directly.  
- Bridge adapters own translation, ownership checks, empty authentic fallbacks, and telemetry.  
- Bridges **never** call Planning generate, StudySession start/finish, mastery writes, or recommendation recalculation.  
- Educational law remains inside Runtime A services.  
- `ExperienceProjectionStore` may cache bridged DTOs; it is **not** educational SoT.

---

## 5. Canonical Educational Timeline

The authoritative timeline of a student’s learning journey is an ordered sequence of **Educational Timeline Events**, each owned by Runtime A. Experience may display projections of these events; it must not invent them.

### 5.1 Event catalogue

| Event type | What it records | Authoritative owner (write) | Authoritative store | Readable by Journey? | Readable by History? |
|---|---|---|---|---|---|
| **PlanActivated** | Active StudyPlan window begins / changes | `StudyPlanService` | `StudyPlan` | Yes (context) | Yes (context) |
| **MissionEnsured** | Today’s Mission created / ensured | `PlanningService` | `Mission` | Yes (active mission) | Optional |
| **SessionStarted** | Mission → In Progress | `StudySessionService` | `Mission.status` | Yes (active) | Yes |
| **SessionCompleted** | Mission → Completed (after Evidence Before Completion) | `StudySessionService` + Evidence path | `Mission` + evidence | Yes | Yes (primary) |
| **EvidenceCommitted** | Practice / attempt accepted for mastery | `EducationalEvidenceAuthority` via StudySession / Learning | `StudyAttempt` (+ gated `TopicProgress`) | Yes (timeline) | Yes (inspect) |
| **ProgressChanged** | Topic mastery / coverage delta | `AdaptiveLearningService` (gated) | `TopicProgress` | Yes | Yes (mastered topics) |
| **RecommendationProjected** | Explainable “next” for a date | `RecommendationService` (+ mission alignment rule) | Computed; optional audit via existing decision/telemetry surfaces | Yes (history of labels) | Yes |
| **LifecycleStageChanged** | Learning ↔ Revision stage | `LearningLifecycleService` | Derived from plan + leaf completion | Yes (milestone) | Yes |
| **RevisionActivity** | Revision-stage study / weak-topic review session | Planning revision templates + Session lifecycle | `Mission` (revision lifecycle) + attempts | Yes | Yes |
| **ContinuityPreserved** | History protected across plan edit | `EducationalContinuityService` | `TopicProgress` continuity fields | Yes (milestone) | Yes (context) |
| **ReadinessSample** | Aggregate readiness at a point | `ReadinessService` | Derived aggregates (no new table in MS-002) | Yes (progress) | Yes (progression series) |
| **ProgressMilestone** | Educationally meaningful coverage / stage gate | Derived projection from StudyPlan coverage + Lifecycle + TopicProgress | Derived (projection only) | Yes | Yes (achievements-style cards) |

### 5.2 Ownership rules

| Concern | Owner | Non-owner |
|---|---|---|
| Creating / selecting mission topics | `PlanningService` | JourneyBridge, HistoryBridge, Experience |
| Session lifecycle writes | `StudySessionService` / `MissionService` | Journey / History bridges |
| Mastery writes | Evidence Authority + AdaptiveLearning | Experience, projection store |
| Recommendation calculation | `RecommendationService` (+ MS-001 alignment) | Journey / History bridges |
| Continuity across plan changes | `EducationalContinuityService` | Experience |
| Ordering topics on Journey | `CurriculumService` traversal + TopicProgress status mapping | Adapter must not invent order |
| Timeline ordering for display | Bridge projects by Runtime A timestamps / mission_date / study_date | Experience must not re-rank educationally |

### 5.3 Timeline identity

Every projected timeline item carries:

| Field | Meaning |
|---|---|
| `event_id` | Stable projection id (prefer SQL primary keys: `mission_id`, `attempt_id`, or deterministic hash of type+keys) |
| `event_type` | From catalogue §5.1 |
| `occurred_at` | Canonical timestamp / date from Runtime A |
| `student_id` | Ownership scope |
| `authority` | Service tag (`mission_service`, `evidence_authority`, …) |
| `trace` | Pointers required by §7 / `JOURNEY_TRACEABILITY_MATRIX.md` |

---

## 6. Journey Projection

### 6.1 Role

**JourneyAdapter** (`JourneyBridge`) is a **read-only** translator:

```
LearningJourneyPort
  → ExperienceJourneyAdapter (thin) OR Journey-backed composition
  → JourneyAdapter
  → Runtime A reads (StudyPlan, Mission, TopicProgress, Lifecycle, Readiness, Recommendation reads)
  → Opaque journey DTO compatible with existing JourneyService / templates
```

### 6.2 Must project

| Projection slice | Runtime A sources | Notes |
|---|---|---|
| Completed sessions (summary) | Completed `Mission` rows for student | Cards / counts; no fabrication |
| Active missions | Today’s / In Progress `Mission` via MissionService | Align with Mission Read Bridge identity |
| Recommendation history | Prior recommendation projections / dated RecommendationService outputs as available without new schema | Prefer mission-aligned labels when mission existed that day |
| Evidence timeline | `StudyAttempt` (+ evidence accept metadata where exposed by services) | Summaries only — not raw event dumps |
| Progress changes | `TopicProgress` deltas / status transitions projected as milestones | Ratios from Readiness / plan coverage — **not recalculated in adapter** |

### 6.3 Must not do

- Calculate educational state (mastery, readiness score, next topic, revision stage)  
- Call `generate_today_mission`, start/complete session, or mastery APIs  
- Invent topics, sessions, or progress ratios when Runtime A is empty  
- Use `seeded_demo_journey` when Journey bridge flag is on  
- Surfacing raw event logs (`events` / `raw_events` / `event_log`) — same ban as current HistoryService

### 6.4 Empty authentic contract

| Condition | Projection |
|---|---|
| No active StudyPlan | `has_journey=false`, empty topics, progress ratio `0.0`, CTA-friendly empty labels |
| Plan exists, no TopicProgress yet | Topics from curriculum traversal with status `upcoming` / not started; ratio from ReadinessService (likely 0) |
| Bridge / service unavailable | Documented failure code; empty authentic snapshot — **not** demo |

Full contracts: `JOURNEY_INTERFACE_SPECIFICATION.md`. Data shapes: `JOURNEY_DATA_MODEL.md`.

---

## 7. History Projection

### 7.1 Role

**HistoryAdapter** (`HistoryBridge`) projects the learner’s accomplished learning narrative for History page and Home history card. Entirely derived from Runtime A.

```
HistoryService / Twin insights path
  → HistoryAdapter
  → Mission history + StudyAttempt + Readiness progression + Revision labels
  → HistoryProjection / HistorySnapshot (existing DTOs)
```

### 7.2 Pagination, filtering, ordering

| Concern | Contract |
|---|---|
| **Pagination** | `limit` (default page size, e.g. 20), `offset` or cursor (`before_date` / `after_mission_id`). Hard max (e.g. 100) to protect query cost. |
| **Filtering** | Optional: `event_types`, `from_date`, `to_date`, `lifecycle_stage` (`learning` \| `revision`), `topic_code`. Filters applied in Runtime A query / service layer where possible; adapter does not invent filter semantics. |
| **Ordering** | Default: **reverse chronological** by `occurred_at` / `mission_date` / `study_date` (most recent first). Secondary key: SQL id for stability. |
| **Traceability** | Every History item includes `trace` fields (mission_id, attempt_ids, recommendation_id / decision_id if any, reason codes). |
| **Projection contracts** | Map to existing `HistoryProjection` / `HistorySnapshot` fields: completed_sessions, total_study_minutes, readiness_progression, mastered_topics, revision_history, recent_achievements — enriched with optional `trace` without UI redesign (unused fields ignored by templates). |

### 7.3 Must not do

- Fabricate completed sessions or readiness points  
- Recompute mastery or readiness independently of Runtime A  
- Accept or forward raw event dumps  
- Write SQL  

### 7.4 Relationship to Journey

| Bridge | Narrative focus |
|---|---|
| Journey | Forward path: where am I on the syllabus, stage, next focus, progress milestones |
| History | Backward path: what I accomplished, evidence trail, readiness over time |

Both share the same Canonical Educational Timeline (§5). History emphasises completed sessions and inspectable evidence; Journey emphasises plan coverage and current position.

---

## 8. Traceability (design principle)

Every Journey (and History) item must answer:

1. **What happened?** — event type + human-readable summary  
2. **Why did it happen?** — reason codes / educational justification from Runtime A (Planning label, recommendation explanation, lifecycle transition reason, continuity copy)  
3. **Which evidence supports it?** — `attempt_id`s / evidence acceptance flags / linked Mission  
4. **Which recommendation changed because of it?** — prior vs subsequent recommendation label / decision_id when available; else explicit `recommendation_delta: null` with reason (`not_applicable` / `unavailable`)

Full matrix: `JOURNEY_TRACEABILITY_MATRIX.md`.

---

## 9. Sequence flows (index)

| Flow | Document |
|---|---|
| Load Journey | `JOURNEY_SEQUENCE_DIAGRAM.md` |
| Load History | `HISTORY_SEQUENCE_DIAGRAM.md` |
| Inspect Evidence | `HISTORY_SEQUENCE_DIAGRAM.md` |
| View Recommendation Change | `JOURNEY_SEQUENCE_DIAGRAM.md` |

Layer order in every diagram: **UI → Experience Layer → Bridge → Educational Services → Database**.

---

## 10. Migration strategy (index)

Full plan: `MIGRATION_PLAN_MS002.md`.

Principles (same as MS-001):

- Incremental, independently releasable phases  
- Each phase reversible via feature flags  
- No big-bang replacement of Journey/History  
- No schema changes  
- No UI redesign  

MS-002 phases refine MS-001 **P5** into Journey-first then History, with dual-run parity and flag rollout.

---

## 11. Acceptance criteria

Under Journey / History bridge flags in Internal Alpha:

| ID | Criterion |
|---|---|
| JC-1 | Journey projections originate **exclusively** from Runtime A (no `seeded_demo_journey`) |
| JC-2 | History projections originate **exclusively** from Runtime A (no demo Twin insights for sessions / readiness) |
| JC-3 | Both bridges are **read-only** (no educational writes from adapter paths) |
| JC-4 | Educational **traceability** present on Journey items (What / Why / Evidence / Recommendation delta) |
| JC-5 | **No educational logic** in Experience facades beyond projection formatting / student-language translation already allowed |
| JC-6 | **Feature-flag** rollout: off by default; independently disable Journey vs History |
| JC-7 | Progress ratios / mastered topics **match** ReadinessService / TopicProgress within agreed tolerance (no divergent formula in adapter) |
| JC-8 | Empty plan → authentic empty Journey/History (not demo) |
| JC-9 | Ownership: never return another student’s timeline |
| JC-10 | Curriculum V1/V2 topic ordering remains via `CurriculumService` |

---

## 12. Architecture Decision Record (draft)

### ADR-MS002-001: Journey and History read bridges — Runtime A as narrative authority

**Status:** Proposed (architecture; accept before implementation)  
**Date:** 2026-07-25  
**Context:** MS-001 bridged mission lifecycle and recommendation reads; Journey/History still demo-seeded. DP-013 requires continuity of learning history.

**Decision:** Experience Journey and History consume Runtime A exclusively through read-only `JourneyBridge` and `HistoryBridge` adapters. Adapters project StudyPlan, Mission, StudyAttempt, TopicProgress, Lifecycle, Readiness, and Recommendation outputs. They do not calculate educational state and do not promote V2 `LearningJourneyEngine` to authority.

**Consequences:**

- Positive: Single narrative truth; sole-runtime cutover safer; preserves Evidence / Continuity services.  
- Negative: Recommendation-history and readiness time-series may need derived projections without new tables (see risks).  
- Neutral: Existing Experience DTO shapes retained; optional `trace` enrichment.

**Alternatives rejected:**

1. **Wire `LearningJourneyEngine` as SoT** — unwired relative to SQL Evidence; behaviour change risk.  
2. **Keep Twin demo insights as History** — violates Foundational Trust.  
3. **Big-bang dual write Experience store ← SQL** — unnecessary persistence; cache only if needed.

---

## 13. Experience consumption map (MS-002 delta)

| Surface | Current | Future (MS-002 Bridge) |
|---|---|---|
| Journey page | `seeded_demo_journey` | `JourneyBridge` → StudyPlan + TopicProgress + Lifecycle + Mission + Readiness |
| Home journey card | Same seed | Same JourneyBridge snapshot (snippet fields) |
| History page | Twin demo insights | `HistoryBridge` → Missions + StudyAttempts + Readiness series + revision labels |
| Home history card | Same | Same HistoryBridge (limited page) |
| Inspect evidence (in-History) | N/A / opaque | HistoryBridge detail read → StudyAttempt + Evidence metadata |
| Recommendation change view | N/A | Journey/History item `trace.recommendation_*` from RecommendationService dated projections |

Revision **options** remain MS-001 P5 / Lifecycle + AdaptiveLearning (out of Journey Bridge Complete unless product expands scope).

---

## 14. Feature flags (design)

| Flag | Maps to | Default | Effect |
|---|---|---|---|
| `KWALITEC_JOURNEY_BRIDGE` | `ENABLE_JOURNEY_BRIDGE` | off | JourneyPort backed by JourneyAdapter |
| `KWALITEC_HISTORY_BRIDGE` | `ENABLE_HISTORY_BRIDGE` | off | History / Twin insights path backed by HistoryAdapter |
| Umbrella `KWALITEC_EDUCATIONAL_CONTINUITY_BRIDGE` | `ENABLE_JOURNEY_BRIDGE` + `ENABLE_HISTORY_BRIDGE` | off | MS-002 continuity umbrella |
| Umbrella `KWALITEC_EDUCATIONAL_RUNTIME_BRIDGE` | existing | off | May enable Journey when product chooses (same pattern as MS-001) |

Rollback: disable flag → prior Experience adapters; under Bridge Alpha prefer empty authentic over re-enabling demo seeds.

---

## 15. Telemetry (observational)

| Event | When |
|---|---|
| `JOURNEY_BRIDGE_REQUESTED` / `SUCCESS` / `FAILURE` / `LATENCY` | Journey project calls |
| `HISTORY_BRIDGE_REQUESTED` / `SUCCESS` / `FAILURE` / `LATENCY` | History project / paginate / evidence inspect |
| `bridge.authority` | Tag `journey_bridge` / `history_bridge` + underlying service authorities |
| `bridge.fallback` | Empty authentic path used |

No PII beyond existing student_id scoping patterns; no passwords / full DB URLs.

---

## 16. Definition of “Journey Bridge Complete”

**Journey Bridge Complete** means:

1. `LearningJourneyPort` (Journey page + Home journey card) is backed by `JourneyBridge` to Runtime A when `ENABLE_JOURNEY_BRIDGE` is on.  
2. History page + Home history card are backed by `HistoryBridge` to Runtime A when `ENABLE_HISTORY_BRIDGE` is on.  
3. `seeded_demo_journey` and demo Twin session/readiness insights are **not** used for authenticated learners under those flags.  
4. Acceptance criteria JC-1…JC-10 are met.  
5. Traceability fields answer What / Why / Evidence / Recommendation delta for Journey items (and History items that participate in inspect flows).  
6. Both bridges are read-only; rollback via flags verified.  
7. Sequence diagrams for Load Journey, Load History, Inspect Evidence, and View Recommendation Change match implemented behaviour and pass contract tests (in a later engineering milestone).

**Journey Bridge Complete does not require:**

- UI redesign  
- Schema migrations  
- Revision options bridge (separate MS-001 P5 slice)  
- Promoting V2 Learning Journey engine  
- Enabling `SOLE_RUNTIME` in production  
- Deleting legacy Analytics UI

---

## Final Report

### Implementation order (recommended)

1. Freeze Journey/History contracts + golden fixtures (docs/tests only) — this directive.  
2. **JourneyAdapter** (read) behind `ENABLE_JOURNEY_BRIDGE` — **Implemented** (Directive 002).  
3. Dual-run / parity vs ReadinessService + TopicProgress; gate off `seeded_demo_journey` when flag on — **Implemented**.  
4. **HistoryAdapter** list projection (completed missions, minutes, mastered topics) behind `ENABLE_HISTORY_BRIDGE` — **Implemented** (Directive 003).  
5. History pagination / filters + readiness progression null contracts — **Implemented** (durable readiness series deferred; explicit `unavailable`).  
6. Inspect Evidence detail path (`get_evidence_summary`) — **Implemented**.  
7. Home card snippets switch to same bridges (no second SoT) — History/Journey wired via composition flags.  
8. Internal Alpha gate for Journey + History Bridge Complete.  
9. (Later) Adaptive / Revision bridges — **not started** (stop after History).

### Complexity estimate

| Workstream | Complexity | Notes |
|---|---|---|
| Architecture (this directive) | **S** (docs) | Done when artefacts accepted |
| JourneyAdapter read | **M** | Mapping StudyPlan/TopicProgress/Lifecycle; avoid divergent % |
| HistoryAdapter list + pagination | **M** | Mission/Attempt queries; performance |
| Evidence inspect + recommendation delta | **M–L** | Depends on available recommendation audit trail without schema |
| Dual-run / golden fixtures | **M** | Parity with Analytics / Readiness |
| **Overall to Journey Bridge Complete** | **M–L** | Lower than MS-001 Evidence write path; dominated by traceability richness |

### Architectural risks (summary)

| Risk | Severity | Mitigation |
|---|---|---|
| Divergent progress % vs ReadinessService | High (educational trust) | Adapter calls ReadinessService; never invents formula |
| No durable recommendation history table | Medium | Project from Mission dates + RecommendationService recompute / telemetry; explicit `unavailable` when not reconstructable |
| Query cost on History | Medium | Pagination hard max; indexed date filters; soak in Alpha |
| Twin still seeds History when only Journey flag on | Medium | Independent flags; Alpha checklist both on for Complete |
| Continuity across plan edits misunderstood | Medium | Document ContinuityService events; never invent wiped history |

Full analysis: `RISK_ANALYSIS_MS002.md`.

### ADRs required

| ADR | Topic | When |
|---|---|---|
| **ADR-MS002-001** | Journey/History bridges → Runtime A narrative authority | Before implementation |
| **ADR-MS002-002** | Readiness progression without new tables (derived series policy) | Before History readiness series ships |
| **ADR-MS002-003** (optional) | Recommendation-change reconstructability / “unavailable” policy | Before View Recommendation Change ships if no audit store |

### Definition of Journey Bridge Complete

See §16.

---

## Stop condition

Directive 001 (architecture) complete. Directive 002 (**Journey Read Bridge**) implemented. **Do not begin History Bridge** until architecture review.
