# MS-005 Engineering Directive 001 — Learning Strategy & Intervention Engine Architecture

**Milestone:** MS-005 — Learning Strategy & Intervention Engine  
**Directive:** Engineering Directive 001 (Architecture Design); Engineering Directive 002 (Learning Strategy Contracts S0); Engineering Directive 003 (Core Strategy Engine S1); Engineering Directive 004 (Explainability & Experience Projection S2); Engineering Directive 005 (Shadow Validation & Readiness S3)  
**Status:** Architecture Design — accepted for implementation; **S0 Contracts → Implemented**; **S1 Core Strategy Engine → Implemented**; **S2 Explainability & Projection → Implemented**; **S3 Shadow Validation → Implemented**  
**Companions:** `INTERVENTION_MODEL.md`, `STRATEGY_PIPELINE.md`, `STRATEGY_EXPLAINABILITY.md`, `STRATEGY_TRACEABILITY.md`, `STRATEGY_INTERFACE_SPECIFICATION.md`, `MIGRATION_PLAN_MS005.md`, `RISK_ANALYSIS_MS005.md`, `STRATEGY_ENGINE_READINESS_REPORT.md`  
**Prior foundation:** MS-001 Educational Runtime Bridge; MS-002 Journey / History Continuity; MS-003 Adaptive Learning Engine; MS-004 Student Digital Twin  
**Domain vocabulary (reference, not authority):** [`ADAPTIVE_DECISION_ENGINE.md`](../version2/ADAPTIVE_DECISION_ENGINE.md), [`LEARNING_ORCHESTRATOR.md`](../version2/LEARNING_ORCHESTRATOR.md), [`EDUCATIONAL_PRINCIPLES.md`](../version2/EDUCATIONAL_PRINCIPLES.md), EP-004 `EVIDENCE_TO_STRATEGY.md` §6

---

## S0 Contracts

| Item | Status |
|---|---|
| **S0 Contracts** | **Implemented** |
| Package | `app/infrastructure/adapters/strategy_engine/` |
| Flag | `KWALITEC_STRATEGY_ENGINE` → `ENABLE_STRATEGY_ENGINE` (default **OFF**) |
| Behaviour | Contracts / DTOs / StrategyAdapter DI only — **no** Experience cutover, Runtime A / Twin / Adaptive mutation, or UI |

**S0 deliverables:** `LearningStrategyContract`, `LearningIntervention`, `InterventionStep`, `StrategyContext`, explanation / provenance placeholders, `StrategyAdapter` interface, DI via `build_strategy_engine_adapter`, feature flag (default OFF), contract / unit / serialization / immutability tests.

---

## S1 Core Strategy Engine

| Item | Status |
|---|---|
| **S1 Core Strategy Engine** | **Implemented** |
| Package | `app/infrastructure/adapters/strategy_engine/` |
| Flag | `KWALITEC_STRATEGY_ENGINE` → `ENABLE_STRATEGY_ENGINE` (default **OFF**) |
| Behaviour | StrategyContextAssembler + planners + StrategyEngine orchestration → one immutable `LearningIntervention` — **no** Experience projection, authority cutover, persistence, or Runtime A / Twin / Adaptive mutation |

**S1 deliverables:** `StrategyEngine`, `StrategyContextAssembler`, `StudyPlanner`, `SessionPlanner`, `RevisionPlanner`, `RecoveryPlanner`, `FatigueManager`, `ConfidenceManager`, `InterventionPlanner`, strategy validation, DI, unit / integration / determinism / planner-consistency / missing-data tests.

**Stop condition (Directive 003):** Stop after Core Strategy Engine. Do not implement explainability gate or Experience projection. Await architecture review.

---

## S2 Explainability & Projection

| Item | Status |
|---|---|
| **S2 Explainability & Projection** | **Implemented** |
| Package | `app/infrastructure/adapters/strategy_engine/` |
| Flag | `KWALITEC_STRATEGY_ENGINE` → `ENABLE_STRATEGY_ENGINE` (default **OFF**) |
| Behaviour | Deterministic `StrategyExplanationBundle` + read-only `StrategyProjection` for Experience — **no** Experience authority cutover, Strategy Engine behavioural change, or Runtime A / Twin / Adaptive mutation |

**S2 deliverables:** `StrategyExplainabilityService`, `StrategyExplanationBundle` (+ nested explainability DTOs), `StrategyProjection`, `StrategyProjector`, `StrategyProjectionPort` (`StrategyExperienceProjectionPort`), projection provenance / summary DTOs, DI via `build_strategy_explainability_service` / `build_strategy_projector` / `build_strategy_projection_port`, unit / integration / explainability-consistency / projection-determinism / serialization tests.

**Stop condition (Directive 004):** Stop after Explainability & Projection. Do not implement Experience authority cutover. Await architecture review.

---

## S3 Shadow Validation

| Item | Status |
|---|---|
| **S3 Shadow Validation** | **Implemented** |
| Package | `app/infrastructure/adapters/strategy_engine/` |
| Flag | `KWALITEC_STRATEGY_ENGINE` → `ENABLE_STRATEGY_ENGINE` (default **OFF**) |
| Behaviour | End-to-end observational shadow pipeline (assemble → evaluate → explain → project → measure → discard) — **no** Experience authority, Runtime A changes, Twin / Adaptive mutation, persistence, or UI |

**S3 deliverables:** `StrategyShadowValidator`, `StrategyShadowMonitors` (`InterventionStabilityMonitor`, `ExplainabilityConsistencyMonitor`, `ProjectionConsistencyMonitor`, `PlannerConsistencyMonitor`, `StrategyDriftDetectionMonitor`), `StrategyShadowHealth`, `StrategyShadowRollback`, `StrategyShadowTelemetry` (`STRATEGY_SHADOW_*` events), DI via `build_strategy_shadow_validator`, composition `strategy_shadow`, unit / integration / determinism / rollback / feature-flag tests, `STRATEGY_ENGINE_READINESS_REPORT.md`.

**Shadow pipeline:**

```
Runtime A (+ Twin / Adaptive consumed inputs)
        │
        ▼
StrategyContextAssembler
        │
        ▼
Strategy Engine
        │
        ▼
LearningIntervention
        │
        ▼
Explainability
        │
        ▼
Projection
        │
        ▼
Telemetry
        │
        ▼
Discard
```

No learner-visible effects. Disabling `KWALITEC_STRATEGY_ENGINE` immediately removes Strategy Engine participation without affecting Runtime A, Twin, Adaptive Engine, or Experience.

**Stop condition (Directive 005):** Stop after Shadow Validation. Await final architecture review before declaring MS-005 complete.

---

## 0. Directive constraints (binding)

| Constraint | Meaning |
|---|---|
| **Architecture only** | This directive produces documentation only |
| **No Strategy Engine implementation** | Do not create Strategy Engine adapters, executors, or flags in application code |
| **No Runtime A modification** | Evidence, Mission, Progress, Planning write paths unchanged |
| **No Twin modification** | Twin synthesis / projection / flags unchanged |
| **No Adaptive Engine modification** | Adaptive contracts, executor, authority flags unchanged |
| **No Experience redesign** | Home / Revision / session UX surfaces unchanged |
| **No schema changes** | No Alembic / SQL DDL for Strategy Ready |

**Stop condition:** Stop after architecture documentation. Await architecture review before any implementation phase (S0+).

---

## 1. Purpose

Design the **Learning Strategy & Intervention Engine** as a **deterministic orchestration layer** that transforms:

1. **Authoritative educational evidence** (Runtime A),  
2. **Student Digital Twin interpretation** (longitudinal learner profile), and  
3. **Adaptive recommendations** (advice artefacts),

into **structured, explainable learning interventions** for Experience consumption.

MS-001 established authoritative educational **transactions**.  
MS-002 established authoritative educational **continuity**.  
MS-003 established adaptive educational **intelligence** (recommendation-only).  
MS-004 established longitudinal learner **interpretation** (Twin).  
MS-005 introduces educational **strategy orchestration** — turning advice + interpretation + evidence into actionable intervention structures (study / session / revision / recovery plans; fatigue and confidence interventions).

### 1.1 Problem statement

| Concern | Today | Problem |
|---|---|---|
| Intervention ownership | Split across RecommendationService narrative, Adaptive Decision Records, V2 `AdaptiveDecisionEngine` revision plans, Planning mission generation, Experience checklists | No single orchestration seam that is explainable, flag-gated, and dependency-lawful |
| Advice ≠ action structure | Adaptive answers *what should happen next*; Planning owns *tonight’s mission topic*; session structure is UI / checklist theatre | Students get topic direction without a coherent, inspectable intervention object |
| Fatigue / confidence | Twin facets and Adaptive confidence exist; recovery and load interventions are informal or absent | EP-004 secondary demand for recovery and anti-false-confidence without theatrical pep-talks |
| Authority polyphony | Multiple layers can appear to “decide” the night | Trust risk (ADR-005 Single Next-Action Authority spirit): Strategy must orchestrate, not invent facts or override Adaptive ranking |

### 1.2 Non-goals (this directive)

- Implementing Strategy Engine code or feature flags  
- Changing Runtime A, Twin, Adaptive Engine, or Experience behaviour  
- Replacing PlanningService mission authority for Start Session  
- Owning mastery, readiness maths, or content generation  
- Introducing AI / LLM reasoning into educational cores  
- Schema / Alembic changes  

---

## 2. Architectural decision (summary)

**Decision:** Introduce a **Learning Strategy & Intervention Engine** as a **read-only orchestration subsystem** that:

1. **Reads** Runtime A educational facts (evidence, progress, missions, goals, curriculum context).  
2. **Reads** Twin snapshots / facet interpretations (consume only).  
3. **Reads** Adaptive Decision Records / AdaptiveOutputBundle (consume only; does not re-rank Adaptive primary).  
4. **Orchestrates** structured **Intervention** artefacts (study plan, session plan, revision plan, recovery plan, fatigue management, confidence intervention).  
5. **Emits** explainable **StrategyDecisionRecord** + **InterventionPlan** consumed by Experience ports.  
6. **Never writes** educational history, evidence, mastery, missions, plans, Twin state, or Adaptive decisions.

**Binding authority split:**

| Layer | Authority |
|---|---|
| **Runtime A** | Sole educational **fact** authority |
| **Student Digital Twin** | Sole longitudinal **interpretation** authority (claims about the learner, not facts) |
| **Adaptive Engine** | Sole **recommendation** authority for next-topic / revision priority / adaptive advice |
| **Learning Strategy Engine** | Sole **intervention orchestration** authority (structure of how advice becomes actionable plans) |
| **PlanningService** | Remains sole authority for **what the student studies when they Start Session** (mission topic) — Strategy may advise structure around the mission; must not silently override mission topic |
| **Experience** | Presentation only; never invents interventions |

**ADR required (implementation gate):** ADR-MS005-001 Strategy Authority Boundaries (see §12).

---

## 3. Dependency direction (law)

```
Runtime A
    ↓
Student Digital Twin
    ↓
Adaptive Engine
    ↓
Learning Strategy Engine
    ↓
Experience
```

**No reverse dependencies.**

| From | May depend on | Must not depend on |
|---|---|---|
| Twin | Runtime A (read) | Adaptive, Strategy, Experience (as owners) |
| Adaptive | Runtime A (read), Twin (consume) | Strategy, Experience (as owners) |
| Strategy | Runtime A (read), Twin (consume), Adaptive (consume) | Experience internals; Twin/Adaptive write APIs |
| Experience | Strategy projections (when flagged) | Strategy internals; must not call Twin/Adaptive as write authorities |

### 3.1 Relationship to Version 2 packages

| V2 artefact | Relationship to MS-005 Strategy Engine |
|---|---|
| `AdaptiveDecisionEngine` (V2-014) | Candidate **Adaptive** recommendation vehicle; **not** the Strategy Engine. Intervention *selection ranking* remains Adaptive; Strategy *structures* selected advice into intervention plans |
| `LearningOrchestrator` (V2-015) | Event coordination across pipelines — **orthogonal**. Strategy Engine is decision/orchestration of interventions, not live event dispatch |
| Education Platform / Mission Engine | Mission educational execution remains Runtime A / Mission paths; Strategy may cite mission context in session plans |

---

## 4. Placement in the stack

```
Templates / JS (Home, Revision, session shell, explanation)
      ↓
Presentation (student blueprints / view models)
      ↓
Application facades (HomeService, EducationalStateService, StrategyInterventionPort)
      ↓
╔══════════════════════════════════════════════════════════════════╗
║  LEARNING STRATEGY & INTERVENTION ENGINE (MS-005 seam)           ║
║  StrategyInterventionPort ← StrategyEngineAdapter (read-only)    ║
║  Inputs: Runtime A + TwinSnapshot + AdaptiveDecisionRecord       ║
║  Outputs: StrategyDecisionRecord + InterventionPlan + Explanation║
║  FORBIDDEN: educational writes; Twin/Adaptive mutation           ║
╚══════════════════════════════════════════════════════════════════╝
      ↓ (consume only)
Adaptive Learning Engine (recommendations — advice only)
      ↓ (consume only)
Student Digital Twin (interpretation — claims only)
      ↓ (read only)
Runtime A educational services + SQL
  Evidence · TopicProgress · StudyAttempt · Mission · StudyPlan
  ReadinessService · CurriculumService · RecommendationService (read)
  Journey/History bridges (optional continuity context — read only)
```

---

## 5. Responsibilities

### 5.1 Strategy Engine owns

| Responsibility | Meaning |
|---|---|
| Intervention orchestration | Compose Adaptive primary (+ alternatives) with Twin factors and Runtime A constraints into InterventionPlan |
| Study planning model | Multi-session / multi-day study structure advice (not StudyPlan SQL ownership) |
| Session planning model | Tonight’s session shell: phases, minutes budget, close ritual — around mission-aligned topic |
| Revision planning model | Structured revision windows / topic sets from Adaptive revision_priority |
| Recovery planning model | Restart-after-failure / interruption recovery structure without pep-talk theatre |
| Fatigue management | Load / break / intensity interventions from Twin cognitive-load + Runtime A recent activity |
| Confidence intervention | Calibration interventions when Twin confidence trends diverge from Runtime A performance evidence |
| Explainability | Every intervention answers why / evidence / Twin / Adaptive / educational principle |
| Traceability | Reconstructable StrategyTrace from inputs → intervention → delivery → Runtime A outcome |
| Feature-flag rollout | Shadow before serve; Authority off by default |

### 5.2 Strategy Engine must not own

| Forbidden | Owner instead |
|---|---|
| Educational facts (attempts, progress, missions, evidence) | Runtime A |
| Learner longitudinal claims / facets | Twin |
| Next-topic / revision-priority **ranking** | Adaptive Engine |
| Mission creation / Start Session topic | PlanningService / Mission write paths |
| Content / questions / tutoring scripts | Curriculum / external materials (product boundary) |
| Mastery or readiness formula invention | Runtime A Readiness / TopicProgress |
| UI redesign | Experience (consume projections only) |
| Persistence of educational SoT | Existing SQL authorities |

### 5.3 Distinctness checklist (acceptance)

| Layer | Verb | Artefact |
|---|---|---|
| Runtime A | **records** | Evidence, Mission, Progress |
| Twin | **interprets** | TwinSnapshot facets |
| Adaptive | **recommends** | AdaptiveDecisionRecord |
| Strategy | **orchestrates** | InterventionPlan |
| Experience | **presents** | OpaqueDict / UI |

---

## 6. Inputs (consumed, never mutated)

| Input | Authoritative owner | What Strategy reads | Mutability from Strategy |
|---|---|---|---|
| **Evidence / Attempts / Missions / Progress** | Runtime A | Bounded snapshots at `as_of` | **Forbidden** |
| **Goals / plan constraints** | StudyPlan (Runtime A) | Exam window, minutes, stage | **Forbidden** |
| **Curriculum context** | CurriculumService | Ordered leaves, V1/V2 traversal | **Forbidden** |
| **TwinSnapshot (+ explanations)** | Digital Twin | Facets: rhythm, consistency, load, confidence trend, session habits, revision behaviour | **Forbidden** |
| **AdaptiveDecisionRecord** | Adaptive Engine | Primary recommendation, alternatives, confidence, revision_priority, workload advice, ExplanationBundle | **Forbidden** to re-rank primary |
| **Journey/History (optional)** | MS-002 bridges | Continuity context for recovery | **Forbidden** writes |

### 6.1 Consumption rules

1. Strategy **must not** synthesise Twin or Adaptive outputs.  
2. Missing Adaptive → fail open to RecommendationService-shaped advisory inputs **or** emit `STRATEGY_INPUT_UNAVAILABLE` with empty authentic intervention (product policy: prefer empty over invented ranking).  
3. Missing Twin → Strategy may proceed with Twin factors marked `unavailable` (never estimate facets).  
4. Missing Runtime A plan / ownership → `NO_ACTIVE_PLAN` / `FORBIDDEN`.  
5. Mission alignment: if SQL Mission exists, session intervention **primary topic equals mission topic**; Adaptive differing topic appears as advisory / alternative structure only.

---

## 7. Outputs (interventions only)

Outputs are **orchestration artefacts**, not educational facts and not Adaptive rankings.

| Output | Meaning |
|---|---|
| **StrategyDecisionRecord** | Identity, versions, input fingerprints, selected intervention kinds, confidence, explanation |
| **InterventionPlan** | Ordered set of Intervention objects (see `INTERVENTION_MODEL.md`) |
| **StudyPlanAdvice** | Multi-horizon study structure (logical; not StudyPlan ORM) |
| **SessionPlanAdvice** | Tonight’s session phases + minutes + close ritual |
| **RevisionPlanAdvice** | Revision windows / topic set structure |
| **RecoveryPlanAdvice** | Restart structure after failure / interruption |
| **FatigueIntervention** | Break / intensity / stop-for-tonight advice |
| **ConfidenceIntervention** | Calibration / honesty guardrail advice |
| **StrategyExplanationBundle** | Required explainability (see `STRATEGY_EXPLAINABILITY.md`) |

**Forbidden outputs:** SQL educational writes; fabricated Adaptive rankings; Twin mutations; silent mission topic override; demo-seeded theatre.

---

## 8. Determinism

| Guarantee | Meaning |
|---|---|
| Input→output stability | Identical `StrategyInputBundle.serialize()` → identical `StrategyDecisionRecord.serialize()` |
| No randomness | Decision ids are digests of material input serialization, not UUIDs |
| No wall-clock in material fields | Latency telemetry observational only |
| Snapshot consistency | Frozen `as_of` input bundle; concurrent Runtime A writes after assemble are outside boundary |
| No LLM in core | Registered educational principles + deterministic rules only |

---

## 9. Feature-flag rollout strategy (design)

| Flag (design name) | Default | Role |
|---|---|---|
| `KWALITEC_STRATEGY_ENGINE` → `ENABLE_STRATEGY_ENGINE` | **OFF** | Construct Strategy adapter / contracts DI |
| `KWALITEC_STRATEGY_SHADOW` → `ENABLE_STRATEGY_SHADOW` | **OFF** | Observational orchestration; discard for UX |
| `KWALITEC_STRATEGY_AUTHORITY` → `ENABLE_STRATEGY_AUTHORITY` | **OFF** | Experience consumes StrategyInterventionPort |

**Precedence (when Authority ON):**

```
StrategyInputAssembler → StrategyExecutor → StrategyExplainabilityGate
  PASS → Experience StrategyInterventionPort (authority=strategy_engine)
  FAIL / exception → Fallback to prior Experience path (Adaptive/Recommendation/checklist)
```

**Hard rules:**

1. Never enable Authority without Engine + Shadow soak evidence.  
2. Never flip Strategy Authority + Adaptive Authority + Twin Authority + Sole Runtime in one release.  
3. Rollback = disable Authority (or Engine) flag → prior Experience path immediately.  
4. Shadow never influences the student.

Detailed phases: `MIGRATION_PLAN_MS005.md`.

---

## 10. Educational principles applied (registry)

Every intervention cites ≥1 registered educational principle id (see `STRATEGY_EXPLAINABILITY.md`). Illustrative bindings:

| Principle id (design) | Intent |
|---|---|
| `ep.director.nightly_topic` | Defensible tonight direction (EP-004 Near Universal) |
| `ep.session.completable_shell` | Evening study structure reduces planning load |
| `ep.honesty.completion_neq_mastery` | Epistemic guardrail against coverage theatre |
| `ep.recovery.restart_that_counts` | Recovery without pep-talk theatre |
| `ep.fatigue.diminishing_returns` | Protect load when Twin/Runtime A show overload |
| `ep.confidence.calibrate_to_evidence` | Confidence interventions grounded in Runtime A performance |
| `ep.inspectability.why_tonight` | Student-verifiable rationale |

---

## 11. Acceptance criteria (architecture review)

| Criterion | Verdict target |
|---|---|
| Responsibilities remain distinct | Runtime A facts / Twin interpretation / Adaptive recommendation / Strategy orchestration / Experience presentation |
| Runtime A remains authoritative | Strategy read-only; no educational writes |
| Digital Twin remains interpretive | Strategy consumes Twin; never owns / mutates Twin |
| Adaptive remains recommendation-only | Strategy does not re-rank Adaptive primary |
| Strategy Engine performs orchestration only | Produces InterventionPlan structures, not facts or rankings |
| No implementation artefacts | Docs-only for this directive |

---

## 12. ADR-MS005-001 (draft) — Strategy Authority Boundaries

**Status:** Proposed (accept before S0 implementation)

**Context:** Adaptive recommendations and Twin interpretation exist; Experience needs structured interventions without authority polyphony.

**Decision:**

1. Strategy Engine is the sole owner of **intervention orchestration** DTOs served under Strategy Authority.  
2. Adaptive Engine remains sole owner of **recommendation ranking**.  
3. Twin remains sole owner of **learner interpretation**.  
4. Runtime A remains sole owner of **educational facts** and **Start Session mission topic**.  
5. Strategy may structure session plans **around** the mission; must not replace Planning mission generation.  
6. Unexplained interventions must not ship as guidance (`STRATEGY_EXPLAINABILITY_INCOMPLETE`).

**Consequences:** Clear dependency law; additional Experience port; feature-flag complexity; risk of over-orchestration if Strategy invents pedagogy — mitigated by principle registry + gate.

---

## 13. Final report (architecture complete)

| Deliverable | Path |
|---|---|
| Architecture | `LEARNING_STRATEGY_ENGINE_ARCHITECTURE.md` (this file) |
| Intervention model | `INTERVENTION_MODEL.md` |
| Pipeline | `STRATEGY_PIPELINE.md` |
| Explainability | `STRATEGY_EXPLAINABILITY.md` |
| Traceability | `STRATEGY_TRACEABILITY.md` |
| Interfaces | `STRATEGY_INTERFACE_SPECIFICATION.md` |
| Migration | `MIGRATION_PLAN_MS005.md` |
| Risks | `RISK_ANALYSIS_MS005.md` |

**Implementation status:** S0 Contracts Implemented; S1 Core Strategy Engine Implemented; S2 Explainability & Projection Implemented; S3 Shadow Validation Implemented (`app/infrastructure/adapters/strategy_engine/`). Experience authority cutover not started — await architecture review before declaring MS-005 complete.

---

## 14. Related documents

- MS-003: `ADAPTIVE_ENGINE_ARCHITECTURE.md`, `ADAPTIVE_INTERFACE_SPECIFICATION.md`  
- MS-004: `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`, `DIGITAL_TWIN_INTERFACE_SPECIFICATION.md`  
- MS-001: `EDUCATIONAL_RUNTIME_BRIDGE.md`  
- Product: `knowledge/product/ep004_private_beta/EVIDENCE_TO_STRATEGY.md` §6  
- Design principles: root `DESIGN_PRINCIPLES.md` (DP-005, DP-008, DP-009, DP-010, DP-012)
