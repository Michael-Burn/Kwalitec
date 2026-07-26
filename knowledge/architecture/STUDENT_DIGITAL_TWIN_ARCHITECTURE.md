# MS-004 Engineering Directive 001 — Student Digital Twin Architecture

**Milestone:** MS-004 — Student Digital Twin  
**Directive:** Engineering Directive 001 (Architecture Design)  
**Status:** Architecture Design — accepted for implementation; **T0 Contracts → Implemented**; **T1 Facet Synthesis → Implemented**; **T2 Snapshot Builder → Implemented**; **T3 Explainability → Implemented**; **T4 Adaptive Integration → Implemented**; **T5 Experience Projection → Implemented**; **T6 Shadow Validation → Implemented**  
**Companions:** `DIGITAL_TWIN_DATA_MODEL.md`, `DIGITAL_TWIN_LIFECYCLE.md`, `DIGITAL_TWIN_INTERFACE_SPECIFICATION.md`, `DIGITAL_TWIN_TRACEABILITY.md`, `DIGITAL_TWIN_EXPLAINABILITY.md`, `MIGRATION_PLAN_MS004.md`, `RISK_ANALYSIS_MS004.md`  
**Prior foundation:** MS-001 Educational Runtime Bridge; MS-002 Journey / History Continuity; MS-003 Adaptive Learning Engine  
**Domain vocabulary (reference, not authority):** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), `app/domain/twin/`

---

## T0 Contracts

| Item | Status |
|---|---|
| **T0 Contracts** | **Implemented** |
| Package | `app/infrastructure/adapters/digital_twin/` |
| Flag | `KWALITEC_DIGITAL_TWIN` → `ENABLE_DIGITAL_TWIN` (default **OFF**) |
| Behaviour | Contracts / DTOs / TwinAdapter DI only — **no** synthesis, persistence, Experience cutover, Adaptive attach, Runtime A writes, or UI |

**T0 deliverables:** `StudentDigitalTwinContract`, `TwinProfile`, Twin facet DTOs (Learning Rhythm, Consistency, Persistence, Revision Behaviour, Confidence Trend, Session Habits, Cognitive Load Indicators), `TwinSnapshot` (profile version, source evidence version, generated timestamp, provenance, completeness), `TwinAdapter` interface, DI via `build_digital_twin_adapter`, contract / unit / serialization / immutability tests.

**EP-001.1 Foundation (additive):** `CanonicalLearnerState` / `StudentDigitalTwinFoundation` packages Runtime A pass-through learner state (mastery, progress, evidence, practice, streaks, missions, behaviour/consistency facets) as the canonical consumer read model. Optional `KWALITEC_DIGITAL_TWIN_AUTHORITY` routes Experience `StudentTwinPort` to Foundation (default OFF). See `knowledge/architecture/ep001_1_student_digital_twin_foundation/`.

**EP-001.2 Adaptive Study Planner (additive consumer):** Runtime A `PlanningService.build_daily_study_plan` consumes Foundation state for today's mission slots, revision priorities, topic ordering, and recommended workload. Planner owns planning; Twin owns learner state. `MissionOptimizer.generate_balanced_mission` is **quarantined** (EP-002.2 — do not wire to production). See `knowledge/architecture/ep001_2_adaptive_study_planner/` and `knowledge/architecture/ep002_2_shared_foundation_di/MISSION_OPTIMIZER_DECISION.md`.

**EP-001.3 Readiness Intelligence (additive consumer):** Runtime A `ReadinessService.build_readiness_intelligence` consumes Foundation state (+ optional planner daily plan) for score, confidence, strongest/weakest areas, drivers, and recommended next actions. Readiness owns evaluation; Twin owns learner state; Planner owns planning. Legacy readiness getters remain unchanged for `ReadinessCollector` pass-through. See `knowledge/architecture/ep001_3_readiness_intelligence/`.

**EP-001.4 Insight & Recommendation Layer (additive consumer):** Runtime A `RecommendationService.build_study_insights` consumes Foundation state + planner daily plan + readiness intelligence for student-facing guidance (today's focus, strongest area, greatest risk, next action, workload/readiness explanations, motivational progress). Insight owns communication; Twin owns learner state; Planner owns planning; Readiness owns evaluation. Legacy `generate_recommendations` remains unchanged. See `knowledge/architecture/ep001_4_insight_recommendation_layer/`.

**EP-001.5 Architectural Integration Review (assurance):** EP-001.1–4 reviewed as one integrated architecture. Verdict: coherent constitutional consumer chain and suitable foundation for future capabilities; not HTTP/Authority cutover complete. No redesign of EP-001.1–4 justified. See `knowledge/architecture/ep001_5_architectural_integration_review/`.

**EP-002 Student Intelligence Surface (Complete — EP-002.1–9):** Successor programme that activated EP-001 consumer outputs on student-facing Runtime A surfaces via observability → soak → insights → readiness → plan/mission cutover → presentation consolidation → programme exit. Highest-value capability: explainable daily study guidance. **EP-002.9 certified:** constitutional compliance; authoritative architecture baseline at `knowledge/architecture/ep002_9_programme_exit_certification/AUTHORITATIVE_ARCHITECTURE_BASELINE.md`; production recommendation **Ready for Controlled Pilot**; production defaults remain Twin / Authority / Cutover OFF. **Twin Ready (T7) is not declared** by EP-002. Distinct from product **EP-002 Analytics**. Twin quarantine: `knowledge/architecture/TWIN_STACK_QUARANTINE.md`.

---

## T1 Facet Synthesis

| Item | Status |
|---|---|
| **T1 Facet Synthesis** | **Implemented** |
| Package | `app/infrastructure/adapters/digital_twin/` (`assembler.py`, `builders.py`, `evidence.py`, `provenance.py`, `validation.py`) |
| Flag | `KWALITEC_DIGITAL_TWIN` → `ENABLE_DIGITAL_TWIN` (default **OFF**) |
| Behaviour | Runtime A collectors → immutable Twin facets (`TwinFacetBundle` / `TwinProfile`); provenance + completeness; **no** snapshot persistence, Adaptive integration, Experience cutover, Runtime A writes, or UI |

**T1 deliverables:** `TwinFacetAssembler`, facet builders (`LearningRhythmBuilder`, `ConsistencyBuilder`, `PersistenceBuilder`, `RevisionBehaviourBuilder`, `ConfidenceTrendBuilder`, `SessionHabitsBuilder`, `CognitiveLoadBuilder`), `TwinRuntimeEvidence`, facet provenance helpers, validation, DI via `build_twin_facet_assembler`, unit / integration / determinism / provenance / missing-data tests.

**Rules:** Each facet derives directly from Runtime A only; no facet depends on another facet; missing evidence → unavailable (never estimate / fabricate); identical Runtime A evidence → identical facet values.

---

## T2 Snapshot Builder

| Item | Status |
|---|---|
| **T2 Snapshot Builder** | **Implemented** |
| Package | `app/infrastructure/adapters/digital_twin/` (`snapshot_builder.py`, `completeness.py`; provenance aggregation in `provenance.py`; version / summary DTOs in `contracts.py`) |
| Flag | `KWALITEC_DIGITAL_TWIN` → `ENABLE_DIGITAL_TWIN` (default **OFF**) |
| Behaviour | Assembles immutable `TwinFacetBundle` facets into coherent versioned `TwinSnapshot`; provenance aggregation + structural completeness; **no** snapshot persistence, Adaptive integration, Experience cutover, Runtime A writes, or UI |

**T2 deliverables:** `TwinSnapshotBuilder`, `SnapshotVersion` (snapshot / schema / evidence triad), `CompletenessEvaluator`, `SnapshotProvenanceSummary`, `UnavailableSummary`, provenance aggregation (`aggregate_snapshot_provenance`), DI via `build_twin_snapshot_builder`, unit / integration / determinism / equality / completeness tests.

### Snapshot version semantics

| Field | Meaning |
|---|---|
| `snapshot_version` | Construction rules version (`t2.0`) — which builder algorithm produced the snapshot |
| `schema_version` | Material TwinSnapshot schema version (`twin_snapshot.v2`) |
| `source_evidence_version` | Runtime A evidence fingerprint (evidence version) |
| `profile_version` | Facet synthesis profile version from T1 (`t1.0`) |

Identical Runtime A evidence + identical decision clock (`generated_at` / `as_of`) → identical `TwinSnapshot.serialize()` every execution.

### Atomicity guarantees

- One `build` / `build_from_bundle` call yields a **single** immutable `TwinSnapshot`.
- All seven facets, version triad, provenance summary, completeness status, and unavailable summary are constructed together — no partial mutable snapshot is published.
- Updates never mutate an existing snapshot; a new snapshot must be assembled.
- Completeness is **structural only** (facet available vs unavailable). Missing evidence → explicit `unavailable`; no estimation / fabricated scores (`completeness.score` remains `None`).

---

## T3 Explainability

| Item | Status |
|---|---|
| **T3 Explainability** | **Implemented** |
| Package | `app/infrastructure/adapters/digital_twin/` (`explainability.py`; DTOs in `contracts.py`; provenance expansion in `provenance.py`) |
| Flag | `KWALITEC_DIGITAL_TWIN` → `ENABLE_DIGITAL_TWIN` (default **OFF**) |
| Behaviour | Deterministic `FacetExplanation` / `SnapshotExplanation` from immutable `TwinSnapshot` + Runtime A provenance; **no** snapshot persistence, Adaptive integration, Experience cutover, Runtime A writes, or UI |

**T3 deliverables:** `TwinExplainabilityService`, `FacetExplanationBuilder`, `SnapshotExplanationBuilder`, `FacetExplanation` / `SnapshotExplanation` DTOs, provenance expansion (`ProvenanceExpansion`, `expand_facet_provenance`, `expand_snapshot_provenance`), DI via `build_twin_explainability_service`, unit / integration / determinism / provenance / missing-data tests.

### Explanation contracts

| DTO | Required fields |
|---|---|
| **`FacetExplanation`** | `contributing_runtime_a_evidence`, `derivation_summary`, `completeness_reasoning`, `unavailable_reasoning`, `provenance_refs` (+ registered `rule_or_model_id`) |
| **`SnapshotExplanation`** | `overall_completeness_explanation`, `unavailable_summary_explanation`, `evidence_coverage_summary`, ordered `facet_explanations` (all seven facets) |

### Guarantees

- Identical `TwinSnapshot` material inputs → identical explanations every execution.
- No hidden calculations; no inferred / fabricated evidence ids.
- Unavailable facets use `twin.insight.sparse_evidence` and explicit unavailable reasoning — never estimates.
- Provenance remains complete: every facet explanation cites expanded Runtime A provenance references.
- Runtime A remains read-only; explainability is a pure projection over assembled snapshots.

---

## T4 Adaptive Integration

| Item | Status |
|---|---|
| **T4 Adaptive Integration** | **Implemented** |
| Package | `app/infrastructure/adapters/adaptive_engine/` (`twin_input.py`; `TwinAdaptiveInputAttachment` + `AdaptiveInputBundle.twin` in `contracts.py`; assembler / executor / provenance extensions) |
| Flag | `KWALITEC_DIGITAL_TWIN` → `ENABLE_DIGITAL_TWIN` (default **OFF**) — Adaptive TwinInput DI is **bundled under Twin ON** (no separate `KWALITEC_DIGITAL_TWIN_ADAPTIVE_INPUT` env flag in code; see EP-001.5 TD-ARCH-06 / EP-002.1) |
| Behaviour | Adaptive Engine may **consume** immutable `TwinSnapshot` (+ optional explanations / provenance) via `TwinInputAdapter` as optional `AdaptiveInputBundle` enrichment; **no** Twin persistence, Experience cutover, Twin writes, Adaptive authority changes, Runtime A writes, or UI |

**T4 deliverables:** `TwinInputAdapter`, `TwinAdaptiveInputAttachment`, `AdaptiveInputBundle.twin` extension, feature-flagged DI (`build_twin_input_adapter` → `AdaptiveInputAssembler.twin_input`), unit / integration / dependency-boundary / determinism / read-only tests.

### Dependency direction (binding)

```
Runtime A
  ↓
Student Digital Twin
  ↓
Adaptive Engine  (TwinInputAdapter — consume only)
  ↓
Experience
```

No reverse dependency is permitted for Twin ownership. Adaptive may import Twin contracts; Twin must not import `TwinInputAdapter` / Experience cutover adapters.

### Read-only guarantees

| Rule | Binding meaning |
|---|---|
| Adaptive **reads** Twin | May read `TwinSnapshot`, Twin explanations, and Twin provenance |
| Adaptive **must not** mutate Twin | No Twin state writes; snapshots remain immutable |
| Adaptive **must not** synthesise Twin | `TwinInputAdapter` never calls `TwinSnapshotBuilder` / `TwinFacetAssembler` |
| Adaptive **must not** persist Twin | No Twin store / Alembic / ORM writes from Twin consumption |
| Adaptive **must not** depend on Experience | No Experience TwinPort / facade imports in `twin_input.py` |
| Runtime A remains primary | Twin absence / unavailability → fail-open unavailable attachment; Runtime A collectors unchanged |
| Adaptive authority independent | Existing Adaptive Engine / Shadow / Authority flags remain governing Adaptive UX authority |

**Stop:** Do not begin Experience Twin projection / `StudentTwinPort` cutover (T5) until architecture review of T4.

---

## T5 Experience Projection

| Item | Status |
|---|---|
| **T5 Experience Projection** | **Implemented** |
| Package | `app/infrastructure/adapters/digital_twin/` (`experience_projection.py`; projection DTOs in `contracts.py`) |
| Flag | `KWALITEC_DIGITAL_TWIN` → `ENABLE_DIGITAL_TWIN` (default **OFF**) |
| Behaviour | Project immutable `TwinSnapshot` (+ optional explanations / provenance) into Experience-facing `StudentTwinProjection` via `StudentTwinProjector` / `StudentTwinProjectionPort`; **no** Experience UX authority cutover, Twin persistence, Adaptive authority changes, Runtime A writes, or UI |

**T5 deliverables:** `StudentTwinProjection`, `FacetSummaryProjection`, `ExplanationSummaryProjection`, `ProjectionProvenance`, `StudentTwinProjector`, `StudentTwinProjectionPort` (`StudentTwinPort` implementation), DI via `build_student_twin_projector` / `build_student_twin_projection_port`, unit / integration / determinism / read-only / projection-consistency tests.

### Projection boundaries

| May expose | Must not expose |
|---|---|
| Learner profile summary | Internal Twin builder / assembler internals |
| Facet summaries (label / note / availability / evidence refs) | Mutable Twin state |
| Completeness (structural) | Runtime A entity objects |
| Explanation summaries | Invented readiness / mastery scores |
| Provenance references (`twin_snapshot_ref`, Runtime A source refs) | Demo-seeded theatre under Twin projection |

### Mapping guarantees

| Port method | Projection mapping |
|---|---|
| `get_learner_summary` | Profile summary + facet summaries + completeness + provenance refs (opaque Experience shape) |
| `get_readiness_summary` | Authentic empty readiness (`readiness_pass_through_deferred`) — Twin must not invent readiness maths |
| `get_learning_insights` | Facet / explanation summaries + provenance refs; no fabricated session cards (History Bridge remains narrative SoT) |

Identical `TwinSnapshot` (+ optional `SnapshotExplanation`) material → identical `StudentTwinProjection.serialize()` every execution.

### Read-only / authority guarantees

| Rule | Binding meaning |
|---|---|
| Experience consumes projections only | `StudentTwinProjectionPort` returns projection-derived opaque dicts — never TwinSnapshot / builder objects |
| Twin internals encapsulated | Projector reads snapshot / explanation / provenance; does not publish assembler / builder state |
| No Twin synthesis from Experience | Port never calls `TwinSnapshotBuilder` / `TwinFacetAssembler` |
| No Twin mutation / persistence | Snapshots remain immutable; no Twin store / Alembic writes |
| Runtime A remains authoritative | Readiness / mastery facts stay Runtime A; projection fails open to unavailable / empty authentic |
| No Experience UX authority cutover | `ExperienceTwinAdapter` remains live `composition.twin`; projection port is additive DI |
| No Adaptive authority changes | Adaptive Engine / Shadow / Authority flags unchanged |
| Feature flag isolation | Projection DI constructed only when `ENABLE_DIGITAL_TWIN` is ON |

**Stop:** Do not begin Shadow Validation / observational Twin traceability (T6) until architecture review of T5.

---

## T6 Shadow Validation

| Item | Status |
|---|---|
| **T6 Shadow Validation** | **Implemented** |
| Package | `app/infrastructure/adapters/digital_twin/` (`shadow.py`, `shadow_monitors.py`, `shadow_health.py`, `shadow_rollback.py`, `shadow_telemetry.py`) |
| Flag | `KWALITEC_DIGITAL_TWIN` → `ENABLE_DIGITAL_TWIN` (default **OFF**) — Shadow DI is **bundled under Twin ON** (no separate `KWALITEC_DIGITAL_TWIN_SHADOW` env flag in code; see EP-001.5 TD-ARCH-06 / EP-002.1) |
| Behaviour | Run complete Twin pipeline (facet synthesis → snapshot → explainability → Experience projection) in **observational mode**; measure stability / consistency / health; **discard** for UX — **no** Experience authority cutover, Twin persistence, Adaptive authority changes, Runtime A writes, or UI |

**T6 deliverables:** `TwinShadowValidator`, `SnapshotStabilityMonitor`, `ProjectionConsistencyMonitor`, `ExplainabilityConsistencyMonitor`, `TwinShadowHealthMetrics`, `TwinRollbackVerifier`, `TWIN_SHADOW_*` telemetry, unit / integration / determinism / projection-stability / rollback / long-running replay tests, `ADAPTIVE`-style ops dashboard hook (`build_twin_shadow_ops_dashboard`), readiness report.

### Validation scope

| Validate | Guarantee |
|---|---|
| Facet synthesis | Assembler path exercised via `TwinSnapshotBuilder` |
| Snapshot construction | Deterministic `TwinSnapshot.serialize()` replay |
| Explainability | Deterministic `SnapshotExplanation.serialize()` replay |
| Projection mapping | Deterministic `StudentTwinProjection.serialize()` replay |
| Feature-flag isolation | Twin DI present only when `ENABLE_DIGITAL_TWIN` ON |
| Read-only guarantees | No educational writes; outputs discarded for UX |

### Observational metrics (telemetry only)

| Metric | Source |
|---|---|
| Snapshot generation success rate | `TwinShadowHealthMetrics` |
| Projection success rate | `TwinShadowHealthMetrics` |
| Explainability success rate | `TwinShadowHealthMetrics` |
| Unavailable facet frequency | Completeness facets_unavailable / execution |
| Deterministic replay success | Stability monitors |
| Rollback success | `TwinRollbackVerifier` |
| Feature-flag isolation checks | Rollback / composition drills |

### Rollback

Disabling `KWALITEC_DIGITAL_TWIN` immediately removes Twin participation (`digital_twin`, assemblers, snapshot builder, explainability, Twin-input adapter, projection port, `twin_shadow`) while preserving existing Experience TwinPort behaviour (`ExperienceTwinAdapter`). Adaptive Engine / Shadow / Authority flags remain independent.

### Operational readiness criteria

Shadow Validation is **engineering-ready for observational dual-run** when:

1. Snapshot generation is deterministic for a frozen `as_of` Runtime A view.  
2. Projection remains stable across repeated shadow cycles.  
3. Explainability is deterministic for identical TwinSnapshots.  
4. Rollback (`KWALITEC_DIGITAL_TWIN=0`) is immediate and verified.  
5. Runtime A remains authoritative (no Twin educational writes).  
6. Feature-flag isolation is preserved (Twin DI absent when flag OFF).  
7. Unit + integration + determinism + rollback + long-running replay tests pass.  
8. Experience UX TwinPort is unchanged (no authority cutover in T6).

**Twin Ready / MS-004 complete** still requires T7 soak + architecture review — do **not** declare Twin Authority or Experience cutover from T6 alone.

**Stop:** Do not begin Experience UX authority cutover / Twin Ready (T7) until architecture review of T6.

---

## 0. Constraints (binding)

| Constraint | Meaning |
|---|---|
| **Architecture only** | No production code, tests, schema, or UI changes in this directive |
| **No Runtime A modification** | Twin must not change Planning, StudySession, Evidence Authority, mastery write paths |
| **No Adaptive Engine redesign** | Engine contracts and flags remain; Twin is an optional consumed input later |
| **No UI redesign** | Existing Experience Twin / Profile / History surfaces retain shapes |
| **No schema changes** | No Alembic; Twin snapshots are logical DTOs / projections over Runtime A |
| **Runtime A authority** | Twin consumes authoritative evidence; never replaces Runtime A as educational SoT |
| **Stop after documentation** | Do not begin implementation until architecture review |

---

## 1. Purpose

Design the **Student Digital Twin** as a **persistent educational model** that synthesises authoritative Runtime A educational evidence into a **longitudinal learner profile**.

MS-001 established authoritative educational **transactions**.  
MS-002 established authoritative educational **continuity** (Journey / History).  
MS-003 established **future-decision intelligence** that reads Runtime A (and must never write it).  
MS-004 designs the **standing learner profile** that sits between immutable educational facts and decision/experience consumers — without inventing a second educational truth.

**Non-goals for this directive:**

- Implementing Twin adapters, engines, or persistence  
- Changing Runtime A write paths or Adaptive Engine algorithms  
- Redesigning student UI  
- Changing Alembic schemas  
- Replacing `TopicProgress` / Evidence Authority with Twin-owned mastery  
- Promoting demo-seeded Experience Twin projections as educational SoT  

---

## 2. Problem statement

| Concern | Today | Problem |
|---|---|---|
| Learner profile | Split across SQL progress, Experience `StudentTwinPort` demo seeds, V2 `app/domain/twin` vocabulary, unwired `StudentTwinEngine` | No governed longitudinal profile grounded in Runtime A |
| Authority confusion | Classic Twin docs call Twin “learner-state SoT”; MS programme established Runtime A as educational fact SoT | Competing narratives risk Twin inventing mastery / readiness / history |
| Adaptive inputs | Adaptive Assembler reads Runtime A collectors directly | No stable longitudinal synthesis for behaviour, retention structure, prediction snapshots |
| Experience Twin port | May still surface fabricated readiness / insights when unbridged | Students see Twin theatre without evidence lineage (EP-004 distrust) |
| Explainability | Adaptive Engine has six-question bundles; Twin-facing insights often lack provenance | Profile claims without “which evidence / as-of / confidence” |

Without an explicit Twin architecture, Kwalitec either (a) keeps demo Twin projections, or (b) accidentally lets Twin estimates overwrite Runtime A facts — both violate DP-001, DP-008, DP-009, and DP-013.

---

## 3. Architectural decision (summary)

**Decision:** Introduce the **Student Digital Twin** as a **synthesis subsystem**:

1. **Consumes** authoritative Runtime A educational evidence and derived Runtime A aggregates (attempts, missions, topic progress, readiness reads, lifecycle, goals, curriculum identity).  
2. **Maintains** a longitudinal **Learner Profile Snapshot** (logical aggregate: Identity, Goals, Knowledge structure, Memory structure, Behaviour structure, Performance structure, Prediction snapshots, Confidence calibration slots).  
3. **Projects** read-only Twin DTOs to Experience via `StudentTwinPort` when Twin authority flags are on.  
4. **May supply** optional enriched inputs to the Adaptive Learning Engine — Adaptive Engine **consumes, never owns**, the Twin.  
5. **Never writes** Missions, StudyAttempts, Evidence acceptance, TopicProgress mastery, StudyPlans, or Journey/History narrative authority.

**Runtime A remains the sole educational authority for facts.**  
**Curriculum remains the sole syllabus structure authority.**  
**Adaptive Engine remains advice-only relative to educational history.**  
**Twin is the longitudinal synthesis of learner state estimates — not a transaction store and not a planner.**

**ADR required:** ADR-MS004-001 (see §14). Companion ADRs for snapshot materialisation policy and Adaptive consumption policy (see Final Report).

---

## 4. Twin placement in the stack

```
Templates / JS (Profile, Home readiness, History insights cards)
      ↓
Presentation (student blueprints / view models)
      ↓
Application facades (StudentExperienceService, HistoryService, …)
      ↓
Experience Ports (StudentTwinPort — read-only)
      ↓
╔══════════════════════════════════════════════════════════════╗
║  STUDENT DIGITAL TWIN SEAM (new MS-004 synthesis seam)       ║
║  TwinAssembler / TwinProjection / TwinLifecycle (logical)    ║
║  Feature-flagged; empty authentic over demo when ON          ║
╚══════════════════════════════════════════════════════════════╝
      ↓ (read only)
Canonical Educational Services (Runtime A)
      ↓
SQL models / Curriculum Engine / Evidence Authority

Optional lateral read (flagged, later phases):
Adaptive Learning Engine  ←── Twin Snapshot (consume, do not own)
     ↑
Runtime A evidence (still primary Adaptive inputs; Twin never replaces them)
```

**Invariants:**

- Experience facades never import Twin domain packages or Runtime A services directly for Twin synthesis.  
- Twin adapters own assembly, provenance annotation, empty authentic fallbacks, and telemetry.  
- Twin **never** calls Planning generate, StudySession start/finish, mastery writes, or Evidence accept.  
- `ExperienceProjectionStore` may cache Twin DTOs; it is **not** educational SoT.  
- When Twin estimate conflicts with Runtime A fact (e.g. “mastered” vs `TopicProgress`), **Runtime A wins** for factual claims; Twin must expose the conflict as a limitation / provenance note, not silently overwrite.

---

## 5. Responsibilities

### 5.1 Twin owns

| Responsibility | Notes |
|---|---|
| Longitudinal learner profile synthesis | Aggregate profile facets from Runtime A evidence |
| Structural Knowledge / Memory / Behaviour / Performance slots | References + structural evolution rules — scoring algorithms deferred / gated |
| Prediction / readiness *snapshot* packaging | Packages Runtime A readiness and Twin-derived prediction slots with `as_of` — does not invent readiness formulae |
| Provenance and explainability for profile claims | Every material claim cites evidence refs + confidence + limitations |
| Twin lifecycle orchestration (logical) | Create / update / freeze / recompute policies — see `DIGITAL_TWIN_LIFECYCLE.md` |
| Privacy / governance boundaries | Student-scoped reads; no cross-student leakage; retention of derived snapshots policy |

### 5.2 Twin must not own

| Non-responsibility | True owner |
|---|---|
| Evidence acceptance / rejection | Educational Evidence Authority (Runtime A) |
| Mission / session lifecycle writes | StudySessionService / MissionService |
| Topic mastery writes | AdaptiveLearningService (gated) + Evidence Authority |
| Study plan generation / mutation | PlanningService / StudyPlanService |
| Syllabus structure / topic order | CurriculumService |
| Journey / History narrative authority | JourneyBridge / HistoryBridge (Runtime A projections) |
| Next-action decision computation | Adaptive Learning Engine / RecommendationService |
| UI composition / chrome | Experience presentation |

### 5.3 Authority matrix

| Artefact | Write authority | Read authority | Twin role |
|---|---|---|---|
| StudyAttempt / Evidence | Runtime A | Runtime A, Twin, Adaptive, Bridges | Consume |
| TopicProgress | Runtime A | Runtime A, Twin, Adaptive, Bridges | Consume (pass-through + structural refs) |
| Mission / Session | Runtime A | Runtime A, Twin, Adaptive, Bridges | Consume |
| StudyPlan / Goals | Runtime A | Runtime A, Twin, Adaptive | Consume / project Identity+Goals facets |
| Curriculum | Curriculum Engine | All | Reference only |
| Journey / History events | Runtime A (via bridges) | Experience | Twin must not invent timeline events |
| Adaptive decisions | Adaptive Engine (advice) | Experience (flagged) | Twin may inform inputs; never author decisions |
| Twin Snapshot | Twin synthesis (derived) | Experience TwinPort; Adaptive (optional) | Own derived profile only |
| Demo Twin seeds | Forbidden when Twin flags ON | — | Empty authentic |

---

## 6. Relationship with Runtime A

```
Runtime A (educational SoT)
  → Evidence, Missions, TopicProgress, Plans, Readiness reads, Lifecycle
       ↓
Student Digital Twin (synthesis)
  → Learner Profile Snapshot (derived, provenance-tagged)
```

| Rule | Binding meaning |
|---|---|
| **Consume, never replace** | Twin reads Runtime A; never becomes the store of record for attempts, missions, or mastery |
| **Pass-through before estimate** | Factual fields (attempt counts, mission status, TopicProgress status) remain Runtime A values |
| **Estimates are labelled** | Beliefs / predictions / pattern metrics are marked `derived` with confidence and limitations |
| **Recomputable** | Twin snapshots must be reconstructable from Runtime A evidence + Twin version + `as_of` (DP-012) |
| **No write-back** | Twin updates never mutate Runtime A tables |

---

## 7. Relationship with Adaptive Engine

```
Runtime A evidence  ──┐
                      ├──→ AdaptiveInputAssembler → Adaptive Engine → advice
Twin Snapshot (opt.) ─┘         (consume Twin; do not own)
```

| Rule | Binding meaning |
|---|---|
| Adaptive **consumes** Twin | Optional enriched fields (behaviour consistency structure, memory slots, prediction snapshots) |
| Adaptive **does not own** Twin | Engine never runs Twin update strategies; never persists Twin; never claims Twin write authority |
| Runtime A remains primary Adaptive input | Twin absence / staleness → Adaptive proceeds with Runtime A collectors only + limitation codes |
| Twin never routes Adaptive authority | Experience AdaptiveDecisionPort cutover remains MS-003 flags; Twin flags are independent |
| No feedback write loop via Twin | Adaptive advice → student action → Runtime A evidence → Twin recompute. Twin must not short-circuit by writing “predicted mastery” into Runtime A |
| Learning Feedback is observational only (EP-003.4) | `ENABLE_LEARNING_FEEDBACK` records Runtime A behavioural events for future analytics; it does not grant Twin write authority and must not be treated as mastery evidence |
| Personal Learning Profile summarises evidence only (EP-004.1) | `ENABLE_PERSONAL_LEARNING_PROFILE` aggregates Learning Feedback into an explainable behavioural profile; it does not make educational decisions, does not write Twin Knowledge State, and must not receive delegated Rec / Readiness / Planning authority — see `PERSONAL_LEARNING_PROFILE_ARCHITECTURE.md` |

---

## 8. Relationship with Experience

```
StudentTwinPort
  → TwinProjectionAdapter (when Twin authority ON)
  → Learner Profile Snapshot DTOs
  → Profile / Home readiness / History insights surfaces

When Twin flags OFF:
  → Prior Experience / demo / opaque path (unchanged) — rollback
```

| Rule | Binding meaning |
|---|---|
| Experience is read-only | `StudentTwinPort` must never mutate Twin or invent readiness scores (existing port contract) |
| Empty authentic over demo | When Twin authority ON and no Runtime A plan/evidence → honest empty / unavailable contracts |
| No second Journey/History SoT | Twin insights must not contradict Journey/History bridges; prefer shared Runtime A ids |
| UI unchanged | DTOs map into existing opaque shapes; no redesign |

---

## 9. Twin lifecycle (summary)

See `DIGITAL_TWIN_LIFECYCLE.md` for full state machine.

| Stage | Meaning |
|---|---|
| **Absent** | No Twin snapshot yet (new learner / flag off) |
| **Initialised** | Identity + Goals projected from StudyPlan / User; empty structural domains |
| **Active** | Updated from Runtime A evidence triggers |
| **Stale** | Snapshot older than freshness window relative to latest evidence |
| **Frozen** | Point-in-time snapshot retained for audit / Adaptive `as_of` (immutable) |
| **Recomputed** | Deterministic rebuild from Runtime A + Twin version |

**Update triggers (summary):** SessionCompleted / EvidenceCommitted / ProgressChanged / PlanActivated / LifecycleStageChanged / GoalsChanged / explicit recompute / Adaptive `as_of` request. Twin never triggers Runtime A writes.

---

## 10. Explainability and traceability (summary)

Every student-visible Twin claim must answer the Twin explainability questions (see `DIGITAL_TWIN_EXPLAINABILITY.md`) and carry TraceRefs (see `DIGITAL_TWIN_TRACEABILITY.md`):

```
Runtime A Evidence → Twin Update → Profile Facet Claim → Experience Projection → (optional) Adaptive Input
```

Incomplete explainability → claim must not ship as guidance / insight authority (`TWIN_EXPLAINABILITY_INCOMPLETE`).

---

## 11. Privacy and governance boundaries

| Boundary | Rule |
|---|---|
| **Ownership scope** | Twin reads and projections are always scoped to authenticated `student_id` |
| **No cross-student synthesis** | Aggregates across students are Founder / research surfaces — out of Twin student path |
| **Minimum necessary** | Twin snapshots retain evidence **references**, not raw answer payloads / PII beyond educational need |
| **Secrets** | Never embed credentials, session cookies, or full DB URLs in Twin DTOs or telemetry |
| **Retention** | Derived snapshots are recomputable; durable retention policy deferred (ADR-MS004-002) — MS-004 Ready requires no new tables |
| **Right to honest absence** | Unavailable facets use explicit null / unavailable contracts — never fabricate |
| **Human-centred copy** | Twin insights must not overclaim certainty (DP-008, DP-010) |
| **Audit** | Material Twin updates emit observational telemetry; educational SoT remains Runtime A |

---

## 12. Feature-flag rollout strategy

| Flag (env → config) | Default | Effect |
|---|---|---|
| `KWALITEC_DIGITAL_TWIN` → `ENABLE_DIGITAL_TWIN` | **OFF** | Construct Twin assembler / contracts / facets / snapshots / explainability / **Shadow validator DI** / **Adaptive TwinInput DI** / Experience projection port / Foundation; no Experience authority |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` → `ENABLE_DIGITAL_TWIN_AUTHORITY` | **OFF** | `StudentTwinPort` serves Runtime-A-grounded Twin Foundation (requires Twin ON; falls back to `ExperienceTwinAdapter`) |

**Implemented bundling (code truth):** There are **no** separate `KWALITEC_DIGITAL_TWIN_SHADOW` or `KWALITEC_DIGITAL_TWIN_ADAPTIVE_INPUT` env flags. Shadow Validation (T6) and Adaptive TwinInput (T4) wire when `ENABLE_DIGITAL_TWIN` is ON. Historical architecture drafts that named separate Shadow / Adaptive-input flags are superseded by this table (EP-001.5 TD-ARCH-06; EP-002.1 alignment).

**Operator quarantine:** See [`TWIN_STACK_QUARANTINE.md`](TWIN_STACK_QUARANTINE.md) for MS-004 vs Epic / V2 / EOS Twin stacks.

**Rollout order:** Twin ON (contracts + shadow + TwinInput + Foundation + `build_*`) → Authority soak (non-prod) → Experience TwinPort cutover → consumer-chain HTTP cutover (EP-002) → Twin Ready (T7).  
**Never** flip Twin Authority + Adaptive Authority + Sole Runtime together.  
**Rollback:** `KWALITEC_DIGITAL_TWIN=0` → prior Experience Twin / Adaptive paths restored immediately.

Phases: `MIGRATION_PLAN_MS004.md` (T0–T7).

---

## 13. Relationship to existing Twin packages (governance)

| Artefact | MS-004 posture |
|---|---|
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Domain vision / vocabulary — **reinterpreted** under MS programme: Twin is learner-profile synthesis SoT for *derived profile facets*; Runtime A remains educational *fact* SoT |
| `app/domain/twin/` | Pure domain vocabulary + update strategy shapes — reference for facet names; not production educational writer |
| `app/application/student_twin/` | V2 application services — not promoted as SoT by this directive |
| Experience `StudentTwinPort` | Correct seam for Twin projection; bridged to Runtime-A-grounded Twin when Authority ON |
| Demo / seeded Twin insights | Forbidden as educational narrative when Twin Authority ON |

MS-004 does **not** delete or refactor these packages. Implementation directives later may adapt vocabulary behind flags without changing Runtime A.

---

## 14. Architecture Decision Record — ADR-MS004-001

### Title

Student Digital Twin as Runtime-A-grounded longitudinal synthesis (not educational transaction SoT)

### Status

Proposed (Architecture Design)

### Context

Kwalitec requires a persistent learner profile for explainable readiness insights, behaviour structure, and optional Adaptive enrichment. Classic Twin documentation asserts Twin as learner-state SoT. MS-001–MS-003 established Runtime A as sole educational authority for missions, evidence, and progress writes. Experience Twin surfaces remain partly demo-seeded.

### Decision

1. Twin **synthesises** longitudinal profile facets from Runtime A evidence.  
2. Runtime A remains sole educational **fact** authority.  
3. Adaptive Engine may **consume** Twin snapshots; it does **not own** Twin.  
4. Experience reads Twin only via `StudentTwinPort`; never invents Twin scores when Authority ON.  
5. Twin never writes educational history.  
6. Feature flags default OFF; shadow before serve.

### Consequences

- Clear separation of fact vs estimate.  
- Recomputable Twin from Runtime A reduces schema pressure for Twin Ready.  
- Classic Twin “single SoT” language is narrowed to **derived profile facets**.  
- Demo Twin insights must be gated off under Authority.  
- Implementation deferred until architecture review.

### Alternatives considered

| Alternative | Rejected because |
|---|---|
| Twin replaces Runtime A as educational SoT now | Violates MS-001–003; high educational integrity risk |
| Skip Twin; Adaptive reads Runtime A only forever | Leaves Experience Twin port / longitudinal behaviour synthesis ungoverned |
| Promote V2 Twin engine as writer of TopicProgress | Dual write / dual truth; schema and migration risk |
| Twin owns Adaptive decisions | Collapses MS-003 boundary; feedback loops opaque |

---

## 15. Acceptance criteria (Directive 001)

| ID | Criterion | Status |
|---|---|---|
| DT-A1 | Responsibilities clearly separated (Twin / Runtime A / Adaptive / Experience) | Met by §§5–8 |
| DT-A2 | Runtime A remains authoritative for educational facts | Met by §§3, 6, 14 |
| DT-A3 | Adaptive Engine consumes — not owns — Twin | Met by §7 |
| DT-A4 | Explainability and traceability are first-class | Met by §10 + companion docs |
| DT-A5 | No implementation artefacts introduced | Met — docs only |
| DT-A6 | Privacy / governance + feature-flag strategy defined | Met by §§11–12 |
| DT-A7 | Lifecycle and update triggers defined | Met by §9 + `DIGITAL_TWIN_LIFECYCLE.md` |

---

## 16. Definition of Student Digital Twin Ready (future)

**Twin Ready** (post-implementation, not this directive) means:

1. Twin Assembler produces deterministic Learner Profile Snapshots from Runtime A behind flags.  
2. Shadow Twin runs without student-visible effect.  
3. Explainability gate PASSes for student-visible Twin claims.  
4. `StudentTwinPort` serves bridged Twin when Authority ON; demo Twin insights disabled for those surfaces.  
5. Adaptive optional Twin input (if enabled) is consume-only and fails open to Runtime-A-only inputs.  
6. Traceability chain Evidence → Twin Update → Claim → Projection reconstructable.  
7. Acceptance DT-1…DT-n from migration plan met; rollback verified.  
8. No schema changes required for Ready unless a later ADR expands scope.

**Twin Ready does not require:** UI redesign; Runtime A rewrite; Adaptive Authority ON; Sole Runtime; V2 Twin engine promotion.

---

## Final Report

### Implementation order (recommended — after architecture review)

1. Accept MS-004 architecture docs + ADR-MS004-001.  
2. **T0** Contracts / fixtures (inert) — **Implemented** (`app/infrastructure/adapters/digital_twin/`).  
3. **T1** Twin Facet Synthesis (Runtime A collectors → immutable facets) — **Implemented** (`TwinFacetAssembler` + builders).  
4. **T2** Twin Snapshot Builder (assembly / versioning / provenance / structural completeness — **no persistence**) — **Implemented** (`TwinSnapshotBuilder`).
5. **T3** Twin Explainability (facet + snapshot explanations from Runtime A provenance) — **Implemented** (`TwinExplainabilityService`).
6. **T4** Adaptive Twin-input consumption (flagged, read-only) — **Implemented** (`TwinInputAdapter` / `AdaptiveInputBundle.twin`).
7. **T5** Experience Twin projection (`StudentTwinProjector` / `StudentTwinProjectionPort`) — **Implemented** (projection only; no UX authority cutover).
8. **T6** Observational Twin traceability / Shadow Validation — **Implemented** (`TwinShadowValidator` + monitors / health / rollback / telemetry).
9. **T7** Shadow soak + Internal Alpha — Twin Ready.

### Complexity estimate

| Workstream | Complexity | Notes |
|---|---|---|
| Architecture (this directive) | **S** (docs) | Done when artefacts accepted |
| Assembler + provenance | **M–L** | Reuse Adaptive collector patterns; V1/V2 curriculum |
| Lifecycle / freshness | **M** | Trigger taxonomy; avoid write-back |
| Experience TwinPort cutover | **M** | Map opaque DTOs; kill demo under flag |
| Adaptive Twin input | **M** | Optional; fail-open |
| Soak / Alpha | **M** | Observational |
| **Overall to Twin Ready** | **L** | Dominated by explainability honesty + demo eradication |

### Architectural risks (summary)

| Risk | Severity | Mitigation |
|---|---|---|
| Twin treated as fact SoT | **Critical** | ADR-MS004-001; Runtime A wins conflicts |
| Twin invents mastery / readiness | **High** | Pass-through + forbidden local formulae without ADR |
| Adaptive owns Twin | **High** | Separate flags; consume-only contract |
| Demo Twin remains under Authority | **High** | Empty authentic gate; Alpha checklist |
| Privacy leakage via snapshots | **Medium–High** | Refs not payloads; student scope |
| Stale Twin → wrong insights | **High** | Freshness windows; stale limitations |

Full analysis: `RISK_ANALYSIS_MS004.md`.

### ADRs required

| ADR | Topic | When |
|---|---|---|
| **ADR-MS004-001** | Twin as synthesis; Runtime A fact SoT | Before implementation |
| **ADR-MS004-002** | Snapshot materialisation / retention without new tables | Before durable Twin store |
| **ADR-MS004-003** | Adaptive Engine Twin-input consumption policy | Before Adaptive Twin-input flag ON |
| **ADR-MS004-004** (optional) | Twin scoring algorithms (mastery belief / decay) | Before non-structural estimates ship as Authority |

---

## Stop condition

Directive 001 (architecture) complete when the eight deliverables exist and this document is accepted for review.

**T0 Contracts (Directive 002):** Implemented — stop after contracts.  
**T1 Facet Synthesis (Directive 003):** Implemented — `TwinFacetAssembler`, facet builders, provenance, validation, DI, tests.  
**T2 Snapshot Builder (Directive 004):** Implemented — `TwinSnapshotBuilder`, version triad, provenance aggregation, structural completeness, DI, tests.  
**T3 Explainability (Directive 005):** Implemented — `TwinExplainabilityService`, facet / snapshot explanation DTOs + builders, provenance expansion, DI, tests.  
**T4 Adaptive Integration (Directive 006):** Implemented — `TwinInputAdapter`, `TwinAdaptiveInputAttachment`, AdaptiveInputBundle extension, feature-flagged DI, read-only / determinism / boundary tests.  
**T5 Experience Projection (Directive 007):** Implemented — `StudentTwinProjection`, `StudentTwinProjector`, `StudentTwinProjectionPort`, projection provenance / mapping, feature-flagged DI, unit / integration / determinism / read-only tests.  
**T6 Shadow Validation (Directive 008):** Implemented — `TwinShadowValidator`, stability / projection / explainability monitors, health metrics, rollback verification, `TWIN_SHADOW_*` telemetry, DI, unit / integration / determinism / rollback / long-running replay tests.  
**Do NOT begin Experience UX authority cutover / Twin Ready declaration (T7).**  
**Do NOT implement Twin snapshot persistence, UI, or schema changes for T6.**  
Await architecture review of T6 before T7 / declaring MS-004 complete.
