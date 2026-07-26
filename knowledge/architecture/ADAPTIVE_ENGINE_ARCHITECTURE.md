# MS-003 Engineering Directive 001 / 002 / 003 / 004 / 005 / 006 / 007 / 008 — Adaptive Learning Engine Architecture

**Milestone:** MS-003 — Adaptive Learning Intelligence  
**Directives:** Engineering Directive 001 (Architecture Design); Engineering Directive 002 (Adaptive Decision Contracts A0); Engineering Directive 003 (Adaptive Input Assembler A1); Engineering Directive 004 (Adaptive Shadow Execution A2); Engineering Directive 005 (Explainability Gate A3); Engineering Directive 006 (Experience Port Cutover A4); Engineering Directive 007 (Observational Traceability A5); Engineering Directive 008 (Adaptive Shadow Soak A6)  
**Status:** Architecture Design complete; **A0 Contracts — Implemented**; **A1 Assembler — Implemented**; **A2 Shadow Execution — Implemented**; **A3 Explainability Gate — Implemented**; **A4 Experience Cutover — Implemented**; **A5 Observational Traceability — Implemented**; **A6 Shadow Soak — Implemented**  
**Companions:** `ADAPTIVE_DECISION_PIPELINE.md`, `ADAPTIVE_INTERFACE_SPECIFICATION.md`, `ADAPTIVE_DATA_FLOW.md`, `ADAPTIVE_TRACEABILITY.md`, `ADAPTIVE_EXPLAINABILITY.md`, `ADAPTIVE_ENGINE_READINESS_REPORT.md`, `MIGRATION_PLAN_MS003.md`, `RISK_ANALYSIS_MS003.md`  
**Prior foundation:** MS-001 Educational Runtime Bridge (`EDUCATIONAL_RUNTIME_BRIDGE.md`); MS-002 Journey / History Continuity (`EDUCATIONAL_JOURNEY_ARCHITECTURE.md`)

---

## 0. Implementation status (Directive 002 / 003 / 004 / 005 / 006 / 007 / 008)

| Component | Status |
|---|---|
| **A0 Contracts** (`AdaptiveDecisionContract`, `ExplanationBundle`, `AdaptiveInputBundle`, `AdaptiveOutputBundle`, `AdaptiveEngineBridge`) | **Implemented** |
| Adaptive Engine Adapter (contract surface; executor-backed when A2 wired) | **Implemented** (DI behind `ENABLE_ADAPTIVE_ENGINE` / shadow) |
| Feature flag `KWALITEC_ADAPTIVE_ENGINE` → `ENABLE_ADAPTIVE_ENGINE` | **Implemented** (default **OFF**) |
| **A1 Assembler** (`AdaptiveInputAssembler`, Runtime A collectors, validation, normalization, field provenance) | **Implemented** |
| **A2 Shadow Execution** (`AdaptiveEngineExecutor`, `AdaptiveShadowOrchestrator`, ExplanationBundle population, shadow telemetry) | **Implemented** |
| Feature flag `KWALITEC_ADAPTIVE_SHADOW` (alias `KWALITEC_ADAPTIVE_ENGINE_SHADOW`) → `ENABLE_ADAPTIVE_ENGINE_SHADOW` | **Implemented** (default **OFF**) |
| **A3 Explainability Gate** (`ExplainabilityGate`, ExplanationBundle validator, quality rules, gate telemetry) | **Implemented** |
| **A4 Experience Cutover** (`AdaptiveExperiencePortRouter` → Experience `AdaptiveDecisionPort`) | **Implemented** |
| Feature flag `KWALITEC_ADAPTIVE_AUTHORITY` → `ENABLE_ADAPTIVE_AUTHORITY` | **Implemented** (default **OFF**) |
| **A5 Observational Traceability** (`TraceabilityService`, `DecisionTrace`, correlation IDs, lineage, trace telemetry) | **Implemented** |
| **A6 Shadow Soak** (`ShadowSoakOrchestrator`, comparison / determinism / drift monitors, health metrics, rollback verification, ops dashboard hooks) | **Implemented** |

**Package:** `app/infrastructure/adapters/adaptive_engine/`  
**Behaviour:** Flags default OFF. RecommendationService remains the primary Experience recommendation authority unless **Engine + Shadow + Authority** are all ON **and** the Explainability Gate PASSes. Any adaptive failure or ineligibility falls back to RecommendationService automatically. Runtime A stays read-only from the Adaptive Engine; no Planning / UI / schema changes. A5 traces and A6 soak are observational (in-memory + telemetry); they never write educational state or student-facing history, and soak never influences the student.

### 0.0 A1 Assembler — field provenance rules

Every `AdaptiveInputBundle` field exposes provenance via `field_provenance[field_name]`:

| Provenance key | Meaning |
|---|---|
| `source_service` | Authoritative Runtime A service / authority that supplied the field |
| `source_entity` | Source entity / aggregate name (e.g. `StudyAttempt`, `TopicProgress`) |
| `collected_at` | Collection timestamp — equals assembler `as_of` (decision clock), never wall-clock |
| `availability` | `available` or `unavailable` |
| `unavailable_reason` | Documented reason when unavailable (required); empty when available |

**Missing vs empty:**

| Situation | Contract |
|---|---|
| Collector succeeded; no rows (new learner) | `availability=available`, empty payload (honest emptiness) |
| No active plan / curriculum / collector failure | `availability=unavailable` + documented reason; empty payload — **never estimate** |

**Assembler MAY:** collect, normalize, validate, annotate provenance.  
**Assembler MUST NOT:** estimate missing values, infer educational state beyond pass-through, rank recommendations, score topics, or mutate Runtime A.

**Determinism:** identical Runtime A state + identical `as_of` → identical `AdaptiveInputBundle.serialize()`.

### 0.1 A2 Shadow Execution — deterministic compute (observational)

**Pipeline:**

```
Runtime A → AdaptiveInputAssembler → AdaptiveEngineExecutor → AdaptiveOutputBundle → Discard
```

| Component | Role |
|---|---|
| `AdaptiveEngineExecutor` | Pure deterministic evaluate(AdaptiveInputBundle) → AdaptiveOutputBundle |
| `AdaptiveShadowOrchestrator` | Assemble → execute → emit shadow telemetry → return result for observation only |
| Shadow telemetry | `ADAPTIVE_SHADOW_REQUESTED` / `COMPLETED` / `FAILED` / `LATENCY` |

**Shadow rule:** outputs may be logged, measured, compared, validated. Outputs must **not** change recommendations, missions, planning, Runtime A, or Experience.

**ExplanationBundle (A2 population):** every successful AdaptiveOutputBundle includes evidence refs, rule refs, recommendation rationale, confidence, `inputs_used`, and `inputs_unavailable` (from field provenance).

**Deterministic execution guarantees:**

| Guarantee | Meaning |
|---|---|
| Input→output stability | Identical `AdaptiveInputBundle.serialize()` → identical `AdaptiveOutputBundle.serialize()` |
| No randomness | Decision ids are SHA-256 digests of input serialization (`a2-<hex16>`), not UUIDs |
| No wall-clock in decisions | Executor does not read wall-clock; latency telemetry is observational only and is **not** part of AdaptiveOutputBundle material fields |
| No mutable globals | Executor is stateless; no module-level caches affecting outputs |
| Snapshot consistency | Shadow assumes the Assembler’s AdaptiveInputBundle is a consistent `as_of` snapshot (A1). Concurrent Runtime A writes after assemble are outside the snapshot boundary — replay uses the frozen bundle, not live re-reads |
| No RecommendationService / Planning calls | Executor derives candidates only from the AdaptiveInputBundle snapshot |

**Registered shadow rules (v1.0.0-a2):** `adaptive.shadow.mission_aligned`, `adaptive.shadow.next_incomplete_leaf`, `adaptive.shadow.weak_topic_priority`, `adaptive.shadow.sparse_evidence`.

### 0.2 A3 Explainability Gate — quality validator (no authority)

**Pipeline (when both Engine + Shadow flags are ON):**

```
Runtime A → AdaptiveInputAssembler → AdaptiveEngineExecutor
  → AdaptiveOutputBundle → ExplainabilityGate → Discard
```

| Component | Role |
|---|---|
| `ExplainabilityGate` | Validate AdaptiveOutputBundle completeness without mutation |
| Quality rules | Recommendation, confidence, evidence refs, inputs_used, inputs_unavailable, recommendation rationale, rule refs |
| Gate telemetry | `EXPLAINABILITY_GATE_REQUESTED` / `PASSED` / `FAILED` / `LATENCY` |

**Gate behaviour:**

| Outcome | Meaning |
|---|---|
| **PASS** | Bundle is **eligible** for Experience consumption when Authority is also enabled (A4). |
| **FAIL** | Bundle remains **shadow-only / observational**. Emits validation telemetry. No correction or mutation. |

**Validation criteria (all required):**

| Check | Rule |
|---|---|
| Recommendation present | `topic_code`, `title`, `label`, or `decision_kind` non-empty |
| Confidence present | Top-level or explanation confidence has `band` or `score` |
| Evidence references present | ≥1 `EvidenceRef` with non-empty `kind` + `id` |
| Inputs used populated | `inputs_used` non-empty |
| Inputs unavailable populated | `inputs_unavailable` present (may be empty) |
| Recommendation rationale present | `recommendation_rationale` non-empty |
| Rule references present | ≥1 `RuleRef` with non-empty `rule_or_model_id` |

**Failure semantics:** `EXPLAINABILITY_INCOMPLETE`; `eligible_for_future_authority=false`; AdaptiveOutputBundle unchanged; Experience / Runtime A / RecommendationService untouched until A4 consumes PASS only under Authority flag.

**Gate executes only when** `KWALITEC_ADAPTIVE_ENGINE` **and** `KWALITEC_ADAPTIVE_SHADOW` are enabled (defaults OFF).

### 0.3 A4 Experience Cutover — AdaptiveDecisionPort routing

**Routing precedence:**

```
Default (any flag OFF / Authority OFF)
  → RecommendationService (ExperienceAdaptiveAdapter prior / Recommendation Bridge path)

When ENGINE + SHADOW + AUTHORITY are ON:
  AdaptiveInputAssembler → AdaptiveEngineExecutor → ExplainabilityGate
    PASS (eligible) → Expose via AdaptiveDecisionPort (authority=adaptive_engine)
    FAIL / exception / empty projection → Fallback to RecommendationService
```

| Component | Role |
|---|---|
| `AdaptiveExperiencePortRouter` | Attempt adaptive recommendation; return None to force fallback |
| `ExperienceAdaptiveAdapter` | AdaptiveDecisionPort: try router first, else RecommendationService |
| Cutover telemetry | `ADAPTIVE_ENGINE_REQUESTED` / `SUCCESS` / `FAILURE` / `FALLBACK` / `LATENCY` |

**Authority rules:**

| Condition | Experience recommendation authority |
|---|---|
| Authority flag OFF (default) | RecommendationService remains primary (no UX cutover) |
| Authority ON + Gate PASS | Adaptive recommendation is authoritative (`authority=adaptive_engine`) |
| Authority ON + Gate FAIL / adaptive error | Automatic RecommendationService fallback |

**Fallback:** Every adaptive failure must gracefully return RecommendationService (or prior Experience path). No student-visible degradation from adaptive unavailability.

**Rollback:** Disable `KWALITEC_ADAPTIVE_AUTHORITY` (or Engine / Shadow) → RecommendationService path immediately.

### 0.4 A5 Observational Traceability — DecisionTrace (no educational writes)

**Status → Implemented**

Every shadow or authoritative adaptive execution can produce a reconstructable `DecisionTrace` for audit and analysis — without influencing educational state, RecommendationService algorithms, Planning, schemas, or UI.

| Component | Role |
|---|---|
| `DecisionTrace` | Immutable observational DTO (decision identity + lineage refs) |
| `DecisionLineage` | Ordered reconstruction stages (Evidence → … → Delivery) |
| `TraceabilityService` | Create / store (in-memory) / reconstruct traces; emit telemetry |
| Correlation IDs | One correlation id binds a decision lifecycle’s events |
| Trace telemetry | `ADAPTIVE_TRACE_CREATED` / `FAILED` / `RECONSTRUCTED` |

**Trace fields (required):**

| Field | Meaning |
|---|---|
| `decision_id` | Adaptive decision identity (executor digest when available; minted `a5-…` on failure) |
| `correlation_id` | Shared lifecycle id for related telemetry / reconstruction |
| `engine_version` | Executor / adapter version at decision time |
| `feature_flag_state` | Snapshot of Engine / Shadow / Authority flags |
| `runtime_a_snapshot_id` | `snap-<sha25616>` of AdaptiveInputBundle material serialize |
| `input_bundle_ref` | `input-<sha25616>` reference fingerprint |
| `output_bundle_ref` | `output-<sha25616>` reference fingerprint |
| `explainability_gate_result` | Gate canonical dict (or empty when gate not run) |
| `authority_status` | `shadow_only` / `adaptive_engine` / `gate_ineligible` / `recommendation_fallback` / `failed` |
| `executed_at` | Observational wall-clock ISO timestamp (not part of decision material) |

**Lineage reconstruction workflow:**

```
Evidence
    ↓
AdaptiveInputBundle
    ↓
AdaptiveOutputBundle
    ↓
Explainability Result
    ↓
Routing Decision
    ↓
Recommendation Delivered (or Shadow Only)
```

`TraceabilityService.reconstruct_lineage(decision_id)` rebuilds `DecisionLineage` deterministically from the stored trace (identical serialize on repeat).

**Correlation rules:**

| Rule | Meaning |
|---|---|
| Lifecycle bind | Shadow / cutover bind `CorrelationContext` for the execution |
| Shared id | Trace + related adaptive telemetry share the same `correlation_id` |
| Resolve order | Explicit arg → current context → newly generated id |

**Feature flags:** Traceability DI follows existing Engine / Shadow flags (no new behavioural flag). Authority remains independent. Tracing never changes recommendation routing.

**Forbidden:** Runtime A writes; student-facing history persistence; schema / Alembic; recommendation algorithm changes; Planning / UI changes.

### 0.5 A6 Shadow Soak — dual-run monitors (observational)

**Status → Implemented**

Run the complete adaptive pipeline in production-like conditions while remaining observational. Demonstrate stability, determinism, explainability, and operational safety before Adaptive Engine Ready. No new educational capability.

**Pipeline:**

```
RecommendationService → Baseline Recommendation
Adaptive Engine (shadow) → Adaptive Recommendation
Compare → Measure → Record
Never influence the student
```

| Component | Role |
|---|---|
| `ShadowSoakOrchestrator` | Baseline + shadow execute → compare → measure → record → discard |
| `RecommendationComparisonMonitor` | Agreement / divergence vs RecommendationService primary |
| `DeterminismMonitor` | Identical AdaptiveInputBundle → identical AdaptiveOutputBundle replay |
| `DriftDetectionMonitor` | Unexpected change, determinism failure, unexplained divergence, missing ExplanationBundle, trace failure — telemetry only |
| `SoakHealthMetrics` | Latency, agreement / divergence rates, explainability pass rate, trace creation rate, deterministic replay success, fallback frequency |
| `RollbackVerifier` | Verify Engine OFF or Authority OFF restores RecommendationService sole authority |
| Ops dashboard hook | `build_soak_ops_dashboard` + `DualRunStatus.adaptive_shadow_soak` |

**Metrics (observational only):**

| Metric | Meaning |
|---|---|
| execution latency | Wall-clock soak cycle latency (not decision material) |
| recommendation agreement rate | Comparable cycles where baseline topic/label matches adaptive |
| recommendation divergence rate | Comparable cycles that disagree (measurable, not corrected) |
| explainability pass rate | Gate PASS / complete ExplanationBundle rate |
| trace creation rate | DecisionTrace produced when TraceabilityService wired |
| deterministic replay success | Double-evaluate success on frozen AdaptiveInputBundle |
| fallback frequency | Adaptive failure rate (would route to RecommendationService) |

**Drift detection:** Emits `ADAPTIVE_SOAK_DRIFT` signals only — no automatic correction.

**Rollback verification:** Disabling `KWALITEC_ADAPTIVE_ENGINE` or `KWALITEC_ADAPTIVE_AUTHORITY` immediately deactivates Experience cutover; RecommendationService remains sole authority. Documented + automated via `verify_adaptive_rollback()`.

**Feature flags:** Soak DI follows existing Shadow flag (no new authority). Authority remains OFF by default.

**Forbidden:** Student-visible soak outputs; Runtime A writes from Adaptive Engine; recommendation algorithm / Planning / UI / schema changes.

### Operational readiness criteria (pre–Adaptive Engine Ready)

| Criterion | Evidence |
|---|---|
| Shadow execution stable | Soak batch replay: identical `decision_id` across iterations on frozen snapshot |
| Divergence measurable | Health snapshot exposes agreement + divergence rates |
| Drift detection functions | Determinism / missing explanation / unexplained divergence / thrash / trace signals |
| Rollback immediate | `RollbackVerifier` + flag-off composition checks |
| Runtime A read-only (Engine) | Static write guards + integration mutation checks on adaptive path |
| Automated tests pass | Unit + integration + drift + rollback + long-running replay |
| No behavioural regressions | Experience AdaptiveDecisionPort unchanged when Authority OFF |

**Readiness report:** `ADAPTIVE_ENGINE_READINESS_REPORT.md` (Directive 008). Await architecture review before declaring MS-003 complete / enabling Authority in production.

### 0.6 Constraints (binding)


| Constraint | Meaning |
|---|---|
| Observational A5/A6 only | Traceability + soak record artefacts; no educational SoT |
| No Runtime A mutation from Adaptive Engine | Engine never writes Mission, StudyAttempt, TopicProgress, Evidence, StudyPlan |
| No recommendation algorithm change | Existing `RecommendationService` rules remain; Adaptive Engine composes beside them |
| No UI redesign | Existing Home / Revision / explanation surfaces consume new contracts later |
| No schema changes | Reuse existing SQL / Curriculum JSON; decision artefacts are logical DTOs |
| History immutable | Adaptive Engine may read History/Journey projections; never rewrite educational narrative |
| Feature-flag rollout | Every implementation phase gated; rollback = flag off |

---

## 1. Purpose

Design the **Adaptive Learning Engine** that converts authoritative educational evidence into **future learning decisions**.

MS-001 established authoritative educational **transactions** (mission identity, start/resume/complete, recommendation projection).  
MS-002 established authoritative educational **continuity** (Journey / History read bridges).  
MS-003 introduces adaptive educational **intelligence** that **consumes — but never mutates —** authoritative educational history.

**Non-goals for this directive:**

- Implementing adaptive behaviour or Adaptive Engine code  
- Changing Runtime A write paths or Evidence Authority  
- Redesigning student UI  
- Changing Alembic schemas  
- Replacing or rewriting `RecommendationService` / `PlanningService` algorithms  
- Promoting unwired `AdaptiveDecisionEngine` as SoT without SQL-fed contracts  

---

## 2. Problem statement

| Concern | Today | Problem |
|---|---|---|
| Adaptive intelligence | Split across `AdaptiveLearningService` (mastery writes), `RecommendationService` (rules), unwired `AdaptiveDecisionEngine`, demo `seeded_demo_adaptive` | No single architecture for *future decisions* that is explainable and Runtime-A-grounded |
| Authority | Runtime A owns evidence and progress; Experience Adaptive port may still be seed-backed when flags off | Adaptive “advice” can appear without inspectable evidence linkage |
| Feedback loops | Mastery updates (authorised) influence later recommendations | Without explicit read-only decision boundary, intelligence risk rewriting history or inventing causation |
| Explainability | `EducationalExplainabilityService` narrates recommendations; adaptive *decision* provenance incomplete | Students distrust certainty without working (DP-005, DP-009; EP-004 evidence) |
| Continuity | Journey/History answer what happened | Adaptive layer must answer what should happen *next* without contradicting immutable history |

This violates DP-005 (Explainability), DP-009 (Evidence Before Opinion), DP-010 (Human-Centred Intelligence), and DP-012 (Deterministic Educational Cores) if adaptive outputs are opaque, ungrounded, or write educational truth.

---

## 3. Architectural decision (summary)

**Decision:** Introduce an **Adaptive Learning Engine** as a **read-only decision subsystem** that:

1. **Reads** authoritative Runtime A educational state (Evidence, Topic Progress, Study Attempts, Mission History, Readiness, Curriculum, Recommendations, Student Goals).  
2. **Computes** adaptive **decision outputs** (next-topic advice, revision priority, confidence, study intensity, workload balancing, revision spacing, …).  
3. **Emits** explainable **Adaptive Decision Records** consumed by Recommendation projection / Experience ports.  
4. **Never writes** educational history, evidence, mastery, missions, or plans.

**Runtime A remains the sole educational authority for facts.**  
**PlanningService remains the sole authority for what the student studies when they Start Session** (MS-001 §5.3 dual-“next” policy preserved).  
**RecommendationService remains the authoritative recommendation narrative** until a later ADR explicitly promotes Adaptive Engine outputs as primary narrative — this milestone designs the engine as a **decision producer**, not a silent planner.

**ADR required:** ADR-MS003-001 (see §12). Companion ADRs for decision-record persistence policy and Planning consumption policy (see Final Report).

---

## 4. Placement in the stack

```
Templates / JS (Home recommendation, Revision, explanation cards)
      ↓
Presentation (student blueprints / view models)
      ↓
Application facades (HomeService, EducationalStateService, AdaptiveDecisionPort)
      ↓
╔══════════════════════════════════════════════════════════════╗
║  ADAPTIVE LEARNING ENGINE (new MS-003 decision seam)         ║
║  AdaptiveDecisionPort ← AdaptiveEngineAdapter (read-only)    ║
║  Inputs: Runtime A snapshots via services / MS-001 bridges   ║
║  Outputs: AdaptiveDecisionRecord + ExplanationBundle         ║
║  FORBIDDEN: educational writes                               ║
╚══════════════════════════════════════════════════════════════╝
      ↓ (read only)
Runtime A educational services + SQL
  Evidence Authority (read gates / attempt reads)
  TopicProgress · StudyAttempt · Mission · StudyPlan
  ReadinessService · CurriculumService · LearningLifecycleService
  RecommendationService (read / recompute narrative — algorithms unchanged)
  AdaptiveLearningService (READ APIs only from Adaptive Engine)
  Journey/History bridges (optional continuity context — read only)
```

**Relationship to existing components:**

| Component | Role vs Adaptive Engine |
|---|---|
| `EducationalEvidenceAuthority` | Gates **writes** elsewhere; Adaptive Engine only **reads** accepted evidence |
| `AdaptiveLearningService` | Owns mastery / weak-topic **state updates** after authorised evidence; Engine **reads** mastery/weak/review signals, does not call write APIs |
| `RecommendationService` | Unchanged algorithms; may **consume** Adaptive Decision Records later as inputs, or Engine may **wrap** its outputs with richer explanation — composition only |
| `RecommendationBridge` (MS-001) | Continues mission-aligned projection; Adaptive Engine feeds richer `AdaptiveDecisionPort` behind `ENABLE_ADAPTIVE_ENGINE` |
| `AdaptiveDecisionEngine` (V2 domain) | Candidate implementation vehicle **only after** SQL-fed contracts + ADR; not authority until then |
| Journey / History Bridges (MS-002) | Optional read context for continuity-aware decisions; never written by Engine |

---

## 5. Adaptive Inputs (authoritative)

Every input is **owned** by Runtime A (or Curriculum). The Adaptive Engine holds **no ownership**.

| Input | Authoritative owner | What Engine reads | Mutability from Engine |
|---|---|---|---|
| **Evidence** | `EducationalEvidenceAuthority` + `StudyAttempt` / session completion path | Accepted attempt outcomes, evidence metadata, acceptance status | **Forbidden** |
| **Topic Progress** | `TopicProgress` via `AdaptiveLearningService` (write path elsewhere) + StudyPlan context | Mastery / coverage / last-studied per topic | **Forbidden** |
| **Study Attempts** | `StudySessionService` / SQL `StudyAttempt` | Attempt history, scores, timestamps, mission linkage | **Forbidden** |
| **Mission History** | `MissionService` / SQL `Mission` (+ MissionTask) | Completed / abandoned / in-progress missions, topics, dates | **Forbidden** |
| **Readiness** | `ReadinessService` | Coverage, backlog, composite readiness aggregates | **Forbidden** (no local formula) |
| **Curriculum** | `CurriculumService` + Curriculum Engine JSON | Official topic order, leaves, V1/V2 traversal | **Forbidden** (structure immutable) |
| **Recommendations** | `RecommendationService` (+ mission alignment policy) | Current / dated recommendation narrative and categories | **Forbidden** to alter stored history; may recompute **read** snapshot |
| **Student Goals** | `StudyPlan` / plan wizard fields / user preferences (exam date, minutes, stage) | Exam window, preferred minutes, lifecycle stage, revision flags | **Forbidden** (goals change only via authorised plan UX) |

### 5.1 Ownership rules

1. **Ownership never transfers** to the Adaptive Engine.  
2. Inputs are **snapshots** at decision time (`as_of` timestamp).  
3. Missing inputs yield **honest degradation** (lower confidence / `unavailable` facets) — never invented evidence (DP-008, DP-009).  
4. Curriculum V1 and V2 remain loadable and traversable ([ADR-003](ADR-003-curriculum-v1-v2.md), [ADR-004](ADR-004-canonical-topic-traversal.md)).  
5. Continuity projections (Journey/History) are **derived views** of the same Runtime A facts — Engine may use them for context but must prefer primary service APIs for decision math when both exist.

### 5.2 Input snapshot contract (logical)

```
AdaptiveInputSnapshot {
  student_id,
  as_of,                          # decision clock
  evidence_summary,               # accepted attempts / gates
  topic_progress[],               # per-topic mastery signals
  study_attempts[],               # bounded recent + relevant history
  mission_history[],              # bounded mission list
  readiness,                      # ReadinessService aggregates
  curriculum_context,             # active syllabus + ordered leaves
  recommendation_snapshot,        # RecommendationService output at as_of
  student_goals,                  # plan constraints + preferences
  lifecycle_stage,                # Learning | Revision
  authority_tags[]                # which services supplied each block
}
```

---

## 6. Adaptive Outputs (decisions only)

Outputs are **advice artefacts**, not educational facts. They do **not** become Mission topics or TopicProgress by themselves.

| Output | Meaning | Consumed by (design) |
|---|---|---|
| **next_topic** | Suggested primary syllabus topic for near-term focus | AdaptiveDecisionPort / Home narrative (mission alignment still wins when mission exists) |
| **revision_priority** | Ordered weak / due topics for revision stage | Revision surface / recommendation alternatives |
| **confidence_score** | Engine confidence in the primary decision (0–1 or band) | Explanation UI; gating for assertive copy |
| **study_intensity** | Suggested session intensity / depth band | Optional Home / planning *advice* only |
| **workload_balancing** | Suggested minutes / load relative to goals and recent history | Advice; must not silently override plan minutes without UX |
| **revision_spacing** | Suggested spacing / due windows for review topics | Revision schedule advice (read of AdaptiveLearning schedule signals) |
| **alternatives[]** | Ranked alternatives not selected | Explainability (required) |
| **decision_id** | Stable id for this Adaptive Decision Record | Traceability / telemetry |
| **explanation** | Structured ExplanationBundle | See `ADAPTIVE_EXPLAINABILITY.md` |

**Forbidden outputs:**

- Writes to SQL educational tables  
- Fabricated evidence or mastery  
- Mission creation / topic override of active SQL Mission  
- Silent contradiction of MS-001 mission-alignment when a mission exists  

When a SQL Mission exists: **primary study topic for Start remains the mission**; Adaptive `next_topic` must either **equal** the mission topic or be labelled **advisory / secondary** (`mission_aligned` policy preserved).

---

## 7. Decision pipeline (summary)

```
Runtime A (authoritative educational state)
      ↓  read snapshot
Evidence + Progress + Attempts + Missions + Readiness + Curriculum + Recommendations + Goals
      ↓
Adaptive Learning Engine (pure decision computation)
      ↓  AdaptiveDecisionRecord (explainable)
Recommendation projection / AdaptiveDecisionPort
      ↓
Experience (Home, Revision, explanation — existing UI)
```

**No educational writes** occur inside the Adaptive Engine.  
Full stages: `ADAPTIVE_DECISION_PIPELINE.md`.  
Data movement: `ADAPTIVE_DATA_FLOW.md`.

---

## 8. Explainability (summary)

Every adaptive recommendation / decision must answer:

| Question | Contract field |
|---|---|
| Why? | `explanation.why` |
| Which evidence? | `explanation.evidence_refs` |
| Which topics? | `explanation.topic_refs` |
| Which rule or model? | `explanation.rule_or_model_id` |
| Confidence? | `outputs.confidence_score` + `explanation.confidence_rationale` |
| Alternatives considered? | `outputs.alternatives[]` + `explanation.alternatives_rationale` |

Full contracts: `ADAPTIVE_EXPLAINABILITY.md`.  
If a decision cannot be explained, it is **not ready** to show as guidance (DP-005).

---

## 9. Traceability (summary)

```
Evidence  →  Adaptive Decision  →  Recommendation  →  Student Outcome
```

Matrix: `ADAPTIVE_TRACEABILITY.md`.  
**A5 Implemented:** `TraceabilityService` + `DecisionTrace` record observational linkage for every shadow / cutover execution (in-memory + telemetry). Student Outcome for MS-003 means **observed** Runtime A outcomes after the decision was shown (mission completed, attempt accepted, readiness change) — linked by `decision_id` / timestamps — **without** the Engine writing those outcomes. Outcome soak / durable audit store remain later (ADR-MS003-002 optional).

---

## 10. Feature flags (design)

| Flag | Maps to | Default | Effect |
|---|---|---|---|
| `KWALITEC_ADAPTIVE_ENGINE` | `ENABLE_ADAPTIVE_ENGINE` | off | Construct Adaptive Engine Adapter + Assembler + Executor + TraceabilityService |
| `KWALITEC_ADAPTIVE_SHADOW` (alias `KWALITEC_ADAPTIVE_ENGINE_SHADOW`) | `ENABLE_ADAPTIVE_ENGINE_SHADOW` | off | Shadow orchestrator: compute + telemetry; Gate DI with Engine; shadow traces |
| `KWALITEC_ADAPTIVE_AUTHORITY` | `ENABLE_ADAPTIVE_AUTHORITY` | off | Experience AdaptiveDecisionPort may serve eligible adaptive recommendations |
| Umbrella (optional) `KWALITEC_ADAPTIVE_INTELLIGENCE` | enables Engine (+ optional shadow) | off | MS-003 umbrella (does **not** enable Authority) |

**Rollback:** disable Authority (or Engine / Shadow) → prior Recommendation Read Bridge / Experience adaptive path restored immediately. Prefer empty authentic / prior bridged recommendation over re-enabling `seeded_demo_adaptive` under Alpha.

---

## 11. Telemetry (observational)

| Event | When |
|---|---|
| `ADAPTIVE_SHADOW_REQUESTED` / `COMPLETED` / `FAILED` / `LATENCY` | Shadow execution (A2; observational) |
| `EXPLAINABILITY_GATE_REQUESTED` / `PASSED` / `FAILED` / `LATENCY` | Explainability Gate (A3; observational quality validator) |
| `ADAPTIVE_ENGINE_REQUESTED` / `SUCCESS` / `FAILURE` / `FALLBACK` / `LATENCY` | Experience Port Cutover (A4; UX-bound when Authority on) |
| `ADAPTIVE_TRACE_CREATED` / `FAILED` / `RECONSTRUCTED` | Observational Traceability (A5; DecisionTrace lifecycle) |
| `ADAPTIVE_SOAK_REQUESTED` / `COMPLETED` / `FAILED` / `COMPARE` / `DRIFT` / `LATENCY` / `HEALTH` / `ROLLBACK_VERIFIED` | Shadow Soak (A6; observational dual-run) |
| `ADAPTIVE_ENGINE_SHADOW_COMPARE` | Soak compare vs RecommendationService (A6; dual-emitted with `ADAPTIVE_SOAK_COMPARE`) |
| `adaptive.authority` | Tag `adaptive_engine` + input authority tags |
| `adaptive.confidence_band` | Observability for over-adaptation analysis |
| `adaptive.explainability_complete` | Whether all six explainability questions populated |

No PII beyond existing student_id scoping; no passwords / full DB URLs.

---

## 12. Architectural Decision Record (required)

### ADR-MS003-001 — Adaptive Engine is a read-only decision authority for advice

**Status:** Proposed (architecture)  
**Context:** Multiple adaptive/decision systems coexist; Experience needs explainable future decisions grounded in Runtime A without mutating history.  
**Decision:** Adaptive Learning Engine consumes authoritative snapshots and emits Adaptive Decision Records; educational writes remain exclusively on authorised Runtime A workflows (Evidence Before Completion, Planning, plan wizard).  
**Consequences:** Clear trust boundary; recommendation algorithms unchanged at first; Planning remains Start authority; explainability mandatory; feature-flag rollout required.

Companion ADRs (draft): see Final Report.

---

## 13. Acceptance criteria (architecture)

The architecture ensures:

| ID | Criterion |
|---|---|
| AC-A1 | Adaptive decisions consume authoritative Runtime A evidence (and related inputs in §5) |
| AC-A2 | History / educational narrative remains immutable from the Adaptive Engine |
| AC-A3 | Adaptive outputs are explainable per §8 / `ADAPTIVE_EXPLAINABILITY.md` |
| AC-A4 | No educational writes occur inside the Adaptive Engine |
| AC-A5 | Feature-flag rollout is possible (`ENABLE_ADAPTIVE_ENGINE` / shadow) |
| AC-A6 | MS-001 mission-alignment policy preserved when a mission exists |
| AC-A7 | Curriculum V1/V2 coexistence preserved |
| AC-A8 | Deterministic cores: same `AdaptiveInputSnapshot` → same material decision outputs (DP-012) |

---

## 14. Definition of “Adaptive Engine Ready”

**Adaptive Engine Ready** means:

1. Adaptive Engine Adapter is wired behind `ENABLE_ADAPTIVE_ENGINE` (and optional shadow flag) and reads only Runtime A authoritative inputs listed in §5.  
2. Engine emits Adaptive Decision Records with complete ExplanationBundles (six questions).  
3. Engine call graph contains **no** educational write APIs (architecture + regression tests).  
4. When a mission exists, Start path still uses SQL Mission; Adaptive primary topic does not contradict mission-alignment policy.  
5. Experience AdaptiveDecisionPort (or Recommendation projection) can consume Engine outputs without UI redesign.  
6. Traceability matrix links Evidence → Decision → Recommendation → observed Student Outcome (read linkage).  
7. Shadow / dual-run soak completed per `MIGRATION_PLAN_MS003.md`; rollback drill verified.  
8. Acceptance criteria AC-A1…AC-A8 and implementation gate AE-1…AE-N (migration plan) met.

**Adaptive Engine Ready does not require:**

- UI redesign  
- Schema migrations  
- Changing RecommendationService or PlanningService algorithms  
- Enabling `SOLE_RUNTIME` in production  
- Replacing Evidence Authority or AdaptiveLearning write path  
- LLM / opaque generative cores in the educational centre  

---

## Final Report

### Implementation roadmap (recommended)

1. **Accept architecture + ADR-MS003-001** (Directive 001) — complete.  
2. Freeze Adaptive Decision Record + ExplanationBundle contracts + golden input fixtures — **A0 Implemented** (Directive 002: `AdaptiveInputBundle` / `AdaptiveOutputBundle` / `ExplanationBundle` / `AdaptiveDecisionContract` / `AdaptiveEngineBridge`).  
3. **Shadow Adaptive Engine** behind `ENABLE_ADAPTIVE_ENGINE_SHADOW` — **A2 Implemented** (Directive 004: `AdaptiveEngineExecutor` + `AdaptiveShadowOrchestrator` + shadow telemetry; no Experience switch).  
4. Wire Adaptive Engine Adapter to `AdaptiveDecisionPort` behind Engine + Shadow + Authority — **A4 Implemented** (Directive 006: `AdaptiveExperiencePortRouter` + eligibility + RecommendationService fallback; Authority default OFF).  
5. **Observational Traceability** — **A5 Implemented** (Directive 007: `TraceabilityService` + `DecisionTrace` + correlation + lineage + trace telemetry; no educational persistence).  
6. **Dual-run soak + monitors** — **A6 Implemented** (Directive 008: `ShadowSoakOrchestrator` + comparison / determinism / drift monitors + health metrics + rollback verification + ops hooks).  
7. Optional: RecommendationService **composition** ADR (consume Engine alternatives / confidence) — **without** rewriting existing recommendation algorithms until explicitly approved.  
8. Optional later: Planning **advisory** consumption (never silent mission override) — requires ADR-MS003-003.  
9. Internal Alpha gate for **Adaptive Engine Ready** (A7) — await architecture review.

### Complexity estimate

| Workstream | Complexity | Notes |
|---|---|---|
| Architecture (this directive) | **S** (docs) | Done when artefacts accepted |
| Contracts + golden fixtures | **S–M** | Input snapshots + explanation completeness |
| Shadow engine (read-only compute) | **M** | Mapping existing AdaptiveLearning + Recommendation reads |
| Experience port switch + alignment | **M** | Preserve MS-001 Recommendation Bridge behaviour |
| Traceability Outcome linkage | **M–L** | May use telemetry / decision_id without new tables |
| Planning advisory consumption | **L** | Explicitly out of “Ready” unless product expands |
| **Overall to Adaptive Engine Ready** | **M–L** | Dominated by explainability + feedback-loop safety, not schema |

### ADRs required

| ADR | Topic | When |
|---|---|---|
| **ADR-MS003-001** | Adaptive Engine read-only decision authority | Before implementation |
| **ADR-MS003-002** | Adaptive Decision Record persistence / reconstructability (DTO-only vs optional audit store **without** educational mutation) | Before Outcome linkage / durable “why was this shown” |
| **ADR-MS003-003** (optional) | Whether Planning may consume Adaptive advice (advisory vs never) | Before any Planning integration |
| **ADR-MS003-004** (optional) | Relationship of V2 `AdaptiveDecisionEngine` to Adaptive Engine Adapter | Before promoting V2 engine as implementation vehicle |

### Definition of Adaptive Engine Ready

See §14.

---

## Stop condition

**Directive 001 (architecture) complete when this document and companions are accepted.**  
**Directive 002 (A0 Contracts) complete when Adaptive Decision contracts, DTOs, adapter interface, DI, feature flag (default OFF), contract tests, and this status update are delivered — stop before assembler.**  
**Directive 003 (A1 Assembler) complete when AdaptiveInputAssembler, Runtime A collectors, validation/normalization, field provenance, DI, feature flag (default OFF), unit/integration/determinism/provenance/missing-data tests, and this status update are delivered — stop before shadow execution (A2).**  
**Directive 004 (A2 Shadow Execution) complete when AdaptiveEngineExecutor, AdaptiveShadowOrchestrator, ExplanationBundle population, shadow telemetry, DI, feature flags (default OFF), unit/integration/determinism/explainability/isolation tests, and this status update are delivered — stop before Explainability Gate (A3).**  
**Directive 005 (A3 Explainability Gate) complete when ExplainabilityGate, ExplanationBundle validator, quality rules, gate telemetry, DI (Engine + Shadow flags), unit/integration/validation/failure-path tests, and this status update are delivered — stop before Experience cutover (A4).**  
**Directive 006 (A4 Experience Cutover) complete when AdaptiveExperiencePortRouter, AdaptiveDecisionPort routing, eligibility consumption, Authority flag (default OFF), RecommendationService fallback, unit/integration/fallback/flag tests, and this status update are delivered — stop before observational traceability (A5).**  
**Directive 007 (A5 Observational Traceability) complete when TraceabilityService, DecisionTrace, correlation IDs, lineage reconstruction, trace telemetry, DI, unit/integration/lineage/correlation tests, and this status update are delivered — stop before shadow soak (A6).**  
**Directive 008 (A6 Shadow Soak) complete when ShadowSoakOrchestrator, comparison / determinism / drift monitors, health metrics, rollback verification, ops dashboard hooks, unit/integration/drift/rollback/long-running replay tests, architecture status update, and Adaptive Engine Readiness Report are delivered — stop before Internal Alpha Ready gate (A7).**  
**Do not begin Internal Alpha Ready declaration (A7) under Directive 008.**  
**Do not modify Runtime A write paths, RecommendationService algorithms, Planning, schemas, or UI under A0–A6.**  
**Await architecture review before declaring MS-003 complete / enabling Authority in production.**
