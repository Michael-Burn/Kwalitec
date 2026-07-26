# MS-006 Engineering Directive 001 — Learning Evidence & Experimentation Platform Architecture

**Milestone:** MS-006 — Learning Evidence & Experimentation Platform  
**Directive:** Engineering Directive 001 (Architecture Design) + Engineering Directive 002 (E0 Contracts) + Engineering Directive 003 (E1 Evidence Collection) + Engineering Directive 004 (E2 Experiment Framework) + Engineering Directive 005 (E3 Policy Evaluation) + Engineering Directive 006 (E4 Analytics & Projection) + Engineering Directive 007 (E5 Shadow Validation & Operational Readiness)  
**Status:** Architecture Design delivered; **E0 Contracts — Implemented**; **E1 Evidence Collection — Implemented**; **E2 Experiment Framework — Implemented**; **E3 Policy Evaluation — Implemented**; **E4 Analytics & Projection — Implemented**; **E5 Shadow Validation & Operational Readiness — Implemented**  
**Companions:** `EVIDENCE_MODEL.md`, `EXPERIMENT_FRAMEWORK.md`, `POLICY_EVALUATION.md`, `OUTCOME_ANALYTICS.md`, `GOVERNANCE_MODEL.md`, `EVIDENCE_TRACEABILITY.md`, `MIGRATION_PLAN_MS006.md`, `RISK_ANALYSIS_MS006.md`, `EVIDENCE_PLATFORM_READINESS_REPORT.md`  
**Prior foundation:** MS-001 Educational Runtime Bridge; MS-002 Journey / History Continuity; MS-003 Adaptive Learning Engine; MS-004 Student Digital Twin; MS-005 Learning Strategy & Intervention Engine  
**Domain vocabulary (reference, not authority):** [`EDUCATIONAL_PRINCIPLES.md`](../version2/EDUCATIONAL_PRINCIPLES.md), EP-004 `EVIDENCE_TO_STRATEGY.md` (SP1–SP8), `EVIDENCE_BACKLOG.md` (capability outcomes)

---

## 0. Directive constraints (binding)

| Constraint | Meaning |
|---|---|
| **Architecture + E0–E5** | Documentation, contracts, observational intake, deterministic experiment assignment, deterministic policy evaluation, deterministic analytics aggregation / governance projection, and observational shadow validation / readiness |
| **No policy deployment** | Shadow / readiness never auto-promote or deploy policy |
| **No Runtime A modification** | Evidence, Mission, Progress, Planning write paths unchanged |
| **No Twin modification** | Twin synthesis / projection / flags unchanged |
| **No Adaptive Engine modification** | Adaptive contracts, executor, authority flags unchanged |
| **No Strategy Engine modification** | Strategy contracts, planners, shadow / authority flags unchanged |
| **No Experience redesign** | Home / Revision / session UX surfaces unchanged |
| **No schema changes** | No Alembic / SQL DDL for Evidence Platform Ready |
| **No policy promotion** | Policy evaluation and analytics emit governance artefacts only — never auto-promotes |

**Stop condition (Directive 007):** Stop after E5 Shadow Validation & Operational Readiness. Await architecture / implementation review before declaring Evidence Platform Ready / MS-006 complete.

---

## E0 Contracts (Implemented)

**Phase:** E0 — Contracts, fixtures, ADRs (contracts + DI subset)  
**Status:** **Implemented**  
**Package:** `app/infrastructure/adapters/evidence_platform/`  
**Feature flag:** `KWALITEC_EVIDENCE_PLATFORM` → `ENABLE_EVIDENCE_PLATFORM` (**default OFF**)

| Deliverable | Location |
|---|---|
| `LearningEvidenceContract` | `contracts.py` — Protocol (`observe`) |
| `EvidenceAdapter` | `contracts.py` — Protocol (`assemble_record`) |
| `EvidenceRecord` DTO | `contracts.py` — immutable, versioned (`e0.1` / `e1.0`) |
| `ExperimentDefinition` DTO | `contracts.py` — protocol structure only |
| `PolicyEvaluation` DTO | `contracts.py` — governance recommendation artefact |
| `OutcomeMetric` + `AnalyticsExport` DTOs | `contracts.py` — analytics contracts |
| DI helper | `adapter.py` — `build_evidence_platform_adapter(enabled=…)` |
| Composition wiring | `student_experience/composition.py` — construct when flag ON; unused for UX |

**E0 invariants (enforced by contract tests):**

- DTOs are `frozen` dataclasses with frozen nested mappings / tuples.  
- Deterministic `serialize()` / `to_canonical_dict()` (sorted keys).  
- Versioned via `evidence_version` / `definition_version` / `evaluation_version` / `metric_version`.  
- Claim boundaries encoded in types (`organisation` ≠ `learning_depth`).  
- No Runtime A write calls; no Experience / Flask imports in the package.  
- Flag OFF → adapter not constructed; no behavioural change to educational serving.

**Not implemented in E0:** evidence intake, experiment assignment, policy evaluation behaviour, analytics aggregation, persistence, schema.

---

## E1 Evidence Collection (Implemented)

**Phase:** E1 — Evidence intake & normalisation  
**Status:** **Implemented**  
**Package:** `app/infrastructure/adapters/evidence_platform/`  
**Feature flag:** `KWALITEC_EVIDENCE_PLATFORM` → `ENABLE_EVIDENCE_PLATFORM` (**default OFF**)

| Deliverable | Location |
|---|---|
| `ObservedEvent` | `contracts.py` — immutable intake event (observation + ingestion clocks) |
| `EvidenceCollector` | `collector.py` — freeze events / refs → `CollectedObservation` |
| `EvidenceAssembler` | `assembler.py` — project observation → `EvidenceRecord` + quality |
| `EvidenceValidator` | `validation.py` — structural / privacy / single-student gates |
| `EvidenceFactory` | `factory.py` — collect → assemble → validate → deterministic `evidence_id` |
| Collection telemetry | `collection_telemetry.py` — `EVIDENCE_COLLECTION_*` events |
| DI helpers | `build_evidence_collector` / `assembler` / `factory` / adapter |

**E1 behaviour:**

```
ObservedEvent / EvidenceContext / upstream refs
        │
        ▼
EvidenceCollector (freeze — never mutate inputs)
        │
        ▼
EvidenceAssembler (quality + provenance — no scoring)
        │
        ▼
EvidenceFactory (deterministic evidence_id + telemetry)
        │
        ▼
immutable EvidenceRecord
```

**E1 invariants:**

- Identical observed event material + engine version → identical `EvidenceRecord` every execution.  
- Observation (`observed_at`) and ingestion (`ingested_at`) timestamps preserved (no wall-clock invent).  
- Inputs never mutated; Runtime A / Twin / Adaptive / Strategy / Experience write APIs absent.  
- No experiment execution, policy evaluation, analytics aggregation, or persistence.  
- Flag OFF → no adapter; Experience educational behaviour unchanged.

**Stop condition (Directive 003):** Stop after Evidence Collection. Do **not** implement Experiment Framework (E2). Await architecture review.

---

## E2 Experiment Framework (Implemented)

**Phase:** E2 — Experiment Framework  
**Status:** **Implemented**  
**Package:** `app/infrastructure/adapters/evidence_platform/`  
**Feature flag:** `KWALITEC_EVIDENCE_PLATFORM` → `ENABLE_EVIDENCE_PLATFORM` (**default OFF**)

| Deliverable | Location |
|---|---|
| `ExperimentObservation` | `contracts.py` — immutable assignment observation (`e2.0`) |
| `ExperimentDefinitionRegistry` | `registry.py` — in-memory registered definitions |
| `ExperimentValidator` | `experiment_validator.py` — definition / eligibility / observation gates |
| `ExperimentAssigner` | `assigner.py` — deterministic hash / manual_allowlist assignment |
| `ExperimentFramework` | `framework.py` — registry → validate → assign → telemetry |
| Experiment telemetry | `experiment_telemetry.py` — `EXPERIMENT_ASSIGNMENT_*` events |
| DI helpers | `build_experiment_framework` / assigner / registry / validator; adapter wiring |

**E2 behaviour:**

```
Validated EvidenceRecord + Registered ExperimentDefinition
        │
        ▼
ExperimentValidator (structure + eligibility — never mutate evidence)
        │
        ▼
ExperimentAssigner (deterministic arm / cohort — no scoring)
        │
        ▼
ExperimentFramework (telemetry + observation_id)
        │
        ▼
immutable ExperimentObservation
```

**E2 invariants:**

- Identical EvidenceRecord + Identical ExperimentDefinition → identical `ExperimentObservation` every execution.  
- EvidenceRecord is referenced only (`evidence_id` / `evidence_ref`); never modified.  
- No statistical analysis, winner declaration, policy evaluation, analytics aggregation, or persistence.  
- No Runtime A / Twin / Adaptive / Strategy / Experience write APIs.  
- Flag OFF → no adapter / framework; Experience educational behaviour unchanged.

**Stop condition (Directive 004):** Stop after Experiment Framework. Do **not** implement Policy Evaluation (E3). Await architecture review.

---

## E3 Policy Evaluation (Implemented)

**Phase:** E3 — Policy Evaluation  
**Status:** **Implemented**  
**Package:** `app/infrastructure/adapters/evidence_platform/`  
**Feature flag:** `KWALITEC_EVIDENCE_PLATFORM` → `ENABLE_EVIDENCE_PLATFORM` (**default OFF**)

| Deliverable | Location |
|---|---|
| `PolicyDefinition` | `contracts.py` — immutable registered policy definition (`e3.0`) |
| `PolicyDefinitionRegistry` | `policy_registry.py` — in-memory registered definitions |
| `EvaluationValidator` | `evaluation_validator.py` — definition / observation / gate validation |
| `PolicyEvaluator` | `evaluator.py` — deterministic observational assessment |
| `EvaluationExplainability` | `evaluation_explainability.py` — five mandatory answers |
| `EvaluationAssembler` | `evaluation_assembler.py` — project assessment → `PolicyEvaluation` |
| `PolicyEvaluationFactory` | `evaluation_factory.py` — validate → assess → explain → assemble → telemetry |
| Evaluation telemetry | `evaluation_telemetry.py` — `EVIDENCE_EVAL_*` events |
| DI helpers | `build_policy_evaluation_factory` / evaluator / assembler / registry; adapter wiring |

**E3 behaviour:**

```
ExperimentObservation(s) + Registered PolicyDefinition
        │
        ▼
EvaluationValidator (structure + eligibility — never mutate observations)
        │
        ▼
PolicyEvaluator (assess outcomes / compare — no promotion)
        │
        ▼
EvaluationExplainability (five mandatory answers)
        │
        ▼
EvaluationAssembler (PolicyEvaluation + provenance + gate)
        │
        ▼
PolicyEvaluationFactory (deterministic evaluation_id + telemetry)
        │
        ▼
immutable PolicyEvaluation (governance recommendation only)
```

**E3 invariants:**

- Identical ExperimentObservations + Identical PolicyDefinition → identical `PolicyEvaluation` every execution.  
- Observations and evidence are referenced only; never modified.  
- No policy promotion, analytics aggregation, persistence, or educational behaviour change.  
- No Runtime A / Twin / Adaptive / Strategy / Experience write APIs.  
- Descriptive soak may recommend `expand_soak` / `inconclusive`; it must not alone justify `keep` of a learner-visible Authority flip.  
- Flag OFF → no adapter / factory; Experience educational behaviour unchanged.

**Stop condition (Directive 005):** Stop after Policy Evaluation. Do **not** implement Analytics & Projection (E4). Await architecture review.

---

## E4 Analytics & Projection (Implemented)

**Phase:** E4 — Analytics & Projection  
**Status:** **Implemented**  
**Package:** `app/infrastructure/adapters/evidence_platform/`  
**Feature flag:** `KWALITEC_EVIDENCE_PLATFORM` → `ENABLE_EVIDENCE_PLATFORM` (**default OFF**)

| Deliverable | Location |
|---|---|
| `AnalyticsSummary` + nested summary DTOs | `contracts.py` — immutable aggregate (`e4.0`) |
| `MetricSeries` / `MetricPoint` / `ScorecardSlice` | `contracts.py` — OUTCOME_ANALYTICS artefacts |
| `EvidenceProjection` + provenance | `contracts.py` — governance-facing projection |
| `EvidenceProjectionPort` | `contracts.py` — Protocol; `projector.py` — implementation |
| `AnalyticsAggregator` | `aggregator.py` — deterministic roll-ups |
| `AnalyticsEngine` | `analytics_engine.py` — aggregate → summary_id → export → telemetry |
| `EvidenceProjector` | `projector.py` — AnalyticsSummary → EvidenceProjection |
| Analytics telemetry | `analytics_telemetry.py` — `EVIDENCE_ANALYTICS_*` events |
| DI helpers | `build_analytics_engine` / aggregator / projector / projection port; adapter wiring |

**E4 behaviour:**

```
PolicyEvaluation(s) + ExperimentObservation(s) + EvidenceRecord(s)
        │
        ▼
AnalyticsAggregator (deterministic roll-ups — never mutate inputs)
        │
        ▼
AnalyticsEngine (summary_id + optional AnalyticsExport + telemetry)
        │
        ▼
EvidenceProjector (governance EvidenceProjection)
        │
        ▼
immutable AnalyticsSummary / EvidenceProjection
```

**E4 invariants:**

- Identical PolicyEvaluation / ExperimentObservation / EvidenceRecord inputs → identical analytics and projections every execution.  
- Inputs are referenced only; never modified.  
- Projections are immutable and governance-facing (forbidden audience: `student_coaching`).  
- Organisation vs learning-depth blocks remain separated (EP-004 SP8).  
- No policy promotion, persistence, or educational behaviour change.  
- No Runtime A / Twin / Adaptive / Strategy / Experience write APIs.  
- Flag OFF → no adapter / engine / projector; Experience educational behaviour unchanged.

**Stop condition (Directive 006):** Stop after Analytics & Projection. Do **not** implement Shadow Validation (E5). Await architecture review.

---

## E5 Shadow Validation & Operational Readiness (Implemented)

**Phase:** E5 — Shadow Validation & Operational Readiness  
**Status:** **Implemented**  
**Package:** `app/infrastructure/adapters/evidence_platform/`  
**Feature flag:** `KWALITEC_EVIDENCE_PLATFORM` → `ENABLE_EVIDENCE_PLATFORM` (**default OFF**)

| Deliverable | Location |
|---|---|
| `EvidenceShadowValidator` | `shadow.py` — orchestrate validate → measure → readiness → discard |
| `EvidencePlatformState` | `shadow.py` — frozen artefact bundle for one cycle |
| `DeterminismValidator` | `shadow_determinism.py` — serialize / pipeline replay determinism |
| `ReadinessEvaluator` + `ReadinessReport` | `shadow_readiness.py` — immutable readiness artefact |
| `OperationalHealthMonitor` | `shadow_health.py` — observational rates |
| `RollbackController` | `shadow_rollback.py` — flag-OFF isolation drill |
| Shadow telemetry | `shadow_telemetry.py` — `EVIDENCE_SHADOW_*` events |
| DI helpers | `build_evidence_shadow_validator` / readiness / health / rollback; composition `evidence_shadow` |

**E5 behaviour:**

```
EvidenceRecord / ExperimentObservation / PolicyEvaluation /
AnalyticsSummary / EvidenceProjection
        │
        ▼
DeterminismValidator (never mutate inputs)
        │
        ▼
OperationalHealthMonitor (rates only)
        │
        ▼
ReadinessEvaluator → immutable ReadinessReport
        │
        ▼
Telemetry (EVIDENCE_SHADOW_*)
        │
        ▼
Discard (no policy deployment; no educational authority)
```

**E5 invariants:**

- Identical platform state → identical `ReadinessReport` every execution.  
- All Evidence Platform artefacts remain immutable (inputs never mutated).  
- Shadow may validate determinism, measure health, and produce readiness reports — never deploy policy or change educational behaviour.  
- Disabling `KWALITEC_EVIDENCE_PLATFORM` immediately removes Evidence Platform + shadow DI without affecting Runtime A, Twin, Adaptive, Strategy, or Experience.  
- No persistence / schema / Experience UX authority.

**Stop condition (Directive 007):** Stop after Shadow Validation & Operational Readiness. Await architecture / implementation review before declaring Evidence Platform Ready / MS-006 complete. Do **not** begin a new milestone.

---

## 1. Purpose

Design the **Learning Evidence & Experimentation Platform** as an **observational measurement and policy-evaluation subsystem** that:

1. **Observes** educational outcomes from Runtime A facts (and, when present, Twin / Adaptive / Strategy / Experience delivery traces),  
2. **Evaluates** instructional strategies and educational policies against declared outcome definitions,  
3. **Supports** controlled, reversible experimentation (assignment, measurement, analysis — never silent authority mutation), and  
4. **Enables** evidence-based evolution of educational policies under explicit governance.

MS-001 established authoritative educational **transactions**.  
MS-002 established authoritative educational **continuity**.  
MS-003 established adaptive educational **intelligence** (recommendation-only).  
MS-004 established longitudinal learner **interpretation** (Twin).  
MS-005 established educational **strategy orchestration** (intervention structure).  
MS-006 introduces educational **measurement authority separation** — observing whether policies and interventions work, without becoming educational authority itself.

### 1.1 Problem statement

| Concern | Today | Problem |
|---|---|---|
| Outcome ownership | Outcome language mixed into Coach copy, Readiness composites, Adaptive confidence, and product narrative | EP-004: certainty without inspectable working breaks trust; measurement must not impersonate teaching authority |
| Policy change | Adaptive / Strategy / Experience behaviours evolve via flags and code without a closed evaluation loop | No governed path from “we changed a policy” → “what evidence supports keep / roll back / revise” |
| Experimentation | Shadow modes exist per engine (Adaptive / Twin / Strategy) but are engine-local, not cross-layer outcome experiments | Cannot answer “did intervention policy A improve recoverable study completion vs B?” without polluting Runtime A authority |
| Learning claims | Product may over-claim learning depth / exam transfer | EP-004 SP4 / SP8: separate organisation success from learning-depth claims; MS-006 must encode that separation |
| Feedback loops | If measurement writes missions, Twin, or Adaptive ranking, observation becomes self-fulfilling | Authority inversion risk across the entire stack |

### 1.2 Non-goals (this directive)

- Implementing Evidence Platform code, collectors, experiment runners, or feature flags  
- Changing Runtime A, Twin, Adaptive Engine, Strategy Engine, or Experience behaviour  
- Owning mastery maths, readiness scoring, content generation, or student-facing coaching  
- Declaring policies “proven” from thin Alpha / shadow agreement alone  
- Introducing AI / LLM reasoning into measurement or policy evaluation cores  
- Schema / Alembic changes  
- Production analytics pipelines or dashboards  

---

## 2. Architectural decision (summary)

**Decision:** Introduce a **Learning Evidence & Experimentation Platform** as a **read-only observational subsystem** that:

1. **Reads** Runtime A educational facts (attempts, missions, progress, goals, curriculum context).  
2. **Reads** Twin snapshots / Adaptive Decision Records / Strategy Interventions / Experience delivery traces (consume only; observational linkage).  
3. **Assembles** outcome observations and evidence artefacts under an explicit Evidence Model.  
4. **Defines** experiment protocols that assign variants **only** via controlled, flag-gated policy knobs owned upstream — never by writing educational history.  
5. **Evaluates** educational policies with mandatory explainability (evidence, statistical basis, educational rationale, policy version, confidence).  
6. **Emits** evaluation reports and governance recommendations (keep / revise / roll back / expand soak) — **never** student-facing educational decisions.  
7. **Never writes** educational history, evidence-as-SoT, mastery, missions, plans, Twin state, Adaptive decisions, Strategy interventions, or Experience authority.

**Binding authority split:**

| Layer | Authority |
|---|---|
| **Runtime A** | Sole educational **fact** authority |
| **Student Digital Twin** | Sole longitudinal **interpretation** authority |
| **Adaptive Engine** | Sole **recommendation** authority (advice only) |
| **Learning Strategy Engine** | Sole **intervention orchestration** authority |
| **Experience** | Presentation only |
| **Learning Evidence Platform** | Sole **observational measurement & policy-evaluation** authority — **not** educational decision authority |

**ADR required (implementation gate):** ADR-MS006-001 Evidence Platform Authority Boundaries (see §12).

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
    ↓
Learning Evidence Platform
```

**No reverse dependencies.**

| From | May depend on | Must not depend on |
|---|---|---|
| Twin | Runtime A (read) | Evidence Platform (as owner) |
| Adaptive | Runtime A (read), Twin (consume) | Evidence Platform (as owner) |
| Strategy | Runtime A (read), Twin / Adaptive (consume) | Evidence Platform (as owner) |
| Experience | Upstream projections (when flagged) | Evidence Platform internals as decision authority |
| Evidence Platform | Runtime A (read); Twin / Adaptive / Strategy / Experience traces (consume only) | Write APIs into any upstream layer; student-facing decision ports |

### 3.1 Measurement ≠ educational authority

| Allowed | Forbidden |
|---|---|
| Observe outcomes after Experience delivery | Change tonight’s mission because an experiment “needs” data |
| Recommend policy revision to governance | Auto-promote Adaptive / Strategy authority from evaluation PASS |
| Link observational traces across layers | Treat evaluation confidence as student-facing mastery |
| Shadow-compare policy variants via flags | Write Twin facets from experiment arms |
| Report organisation vs learning-depth outcomes separately | Collapse SP8 — claim “learning improved” from session completion alone |

### 3.2 Relationship to upstream shadow modes

| Upstream | Owns | Evidence Platform role |
|---|---|---|
| Adaptive Shadow (MS-003) | Engine-local shadow decide → discard | May **observe** shadow telemetry / DecisionTraces; does not own Adaptive shadow |
| Twin Shadow (MS-004) | Twin-local shadow synthesise → discard | May observe TwinShadow health; does not own Twin |
| Strategy Shadow (MS-005) | Strategy-local shadow orchestrate → discard | May observe StrategyTraces; does not own Strategy |
| Evidence Platform Shadow (MS-006) | Cross-layer outcome assembly → evaluate → discard UX effects | Owns **outcome / policy evaluation** shadow only |

Upstream shadows remain valid without MS-006. MS-006 must not require upstream Authority ON to observe Runtime A outcomes.

---

## 4. Platform responsibilities

### 4.1 In scope

| Responsibility | Description |
|---|---|
| **Evidence lifecycle** | Ingest observational refs → normalise → quality-gate → store observational artefacts → expire/retain per governance |
| **Outcome model** | Define measurable educational outcomes with claim boundaries (organisation vs learning-depth vs transfer) |
| **Experiment framework** | Protocol, assignment, measurement windows, analysis artefacts — flag-mediated variants only |
| **Policy evaluation** | Compare policy versions against outcomes with mandatory explainability |
| **Outcome analytics** | Aggregate observational metrics for governance / Alpha / research — not student coaching |
| **Governance** | Propose / review / decide / roll back educational policy changes |
| **Traceability** | Reconstruct Evidence → Delivery → Outcome → Evaluation chains |
| **Explainability** | Every evaluation answers five mandatory questions (§8) |

### 4.2 Out of scope (permanent boundary)

| Forbidden ownership | Remains with |
|---|---|
| Educational fact writes | Runtime A |
| Learner interpretation claims | Twin |
| Next-topic / revision ranking | Adaptive |
| Intervention structure | Strategy |
| Student-visible Home / Start / Recommendation authority | Experience + Planning (mission topic) |
| Exam-mark prediction as product claim | Explicitly deferred (EP-004) unless separate evidence programme |

---

## 5. Evidence lifecycle (overview)

Detailed model: `EVIDENCE_MODEL.md`.

```
Runtime A facts (+ optional upstream traces)
        │
        ▼
Observation Intake (read-only refs / fingerprints)
        │
        ▼
Normalisation & Claim Boundary tagging
        │
        ▼
Quality Gate (completeness, freshness, SP8 separation)
        │
        ▼
Observational Evidence Store (not educational SoT)
        │
        ▼
Outcome Assembly / Experiment Measurement / Policy Evaluation
        │
        ▼
Governance artefacts (reports, recommendations)
        │
        ▼
Retention / expiry per governance policy
```

**Invariant:** The Evidence Platform store is **observational**. Runtime A SQL remains the sole educational source of truth. Reconstructing “what happened educationally” always prefers Runtime A over Evidence Platform artefacts.

---

## 6. Experiment model (overview)

Detailed model: `EXPERIMENT_FRAMEWORK.md`.

| Principle | Binding |
|---|---|
| **Flag-mediated** | Variants change only via documented upstream feature flags / policy knobs — Evidence Platform never mutates engines |
| **Shadow-first** | Prefer observe-only arms before any learner-visible policy difference |
| **Reversible** | Every experiment arm maps to an immediate flag rollback |
| **Honest outcomes** | Primary metrics must not launder organisation success as learning depth |
| **No silent cutover** | Experiment PASS ≠ Adaptive/Strategy Authority ON |

---

## 7. Policy evaluation workflow (overview)

Detailed model: `POLICY_EVALUATION.md`.

```
Policy Version (declared)
    → Eligible Population / Window
    → Evidence Bundle (refs + quality)
    → Outcome Metrics (typed)
    → Statistical Summary (pre-registered)
    → Educational Rationale Review
    → EvaluationRecord + ExplanationBundle
    → Governance Decision (keep / revise / roll back / expand)
```

---

## 8. Explainability (binding)

Every **policy evaluation** must explain:

| # | Required answer | Field family |
|---|---|---|
| 1 | **Evidence considered** | `evidence_refs[]`, quality codes, claim boundaries |
| 2 | **Statistical basis** | design, sample, estimator, uncertainty, pre-registration id |
| 3 | **Educational rationale** | principle ids, outcome intent, SP mapping |
| 4 | **Policy version** | `policy_id`, `policy_version`, upstream flag snapshot |
| 5 | **Confidence level** | band + limitations + “what this does **not** prove” |

**No hidden reasoning.** Incomplete ExplanationBundle → evaluation is `gate_ineligible` / not actionable for governance promote. Details: `POLICY_EVALUATION.md`, `GOVERNANCE_MODEL.md`.

Student-facing Experience copy is **not** an Evidence Platform responsibility. Evaluations are operator / governance artefacts.

---

## 9. Feature-flag rollout (design + E0 master flag)

| Flag | Purpose | Default | Implementation |
|---|---|---|---|
| `ENABLE_EVIDENCE_PLATFORM` (`KWALITEC_EVIDENCE_PLATFORM`) | Master: allow Evidence Platform participation / DI | OFF | **E0–E5 Implemented** |
| `ENABLE_EVIDENCE_INTAKE` | Observational intake / normalisation (sub-flag) | OFF | Design only (E1 uses master flag) |
| `ENABLE_EVIDENCE_SHADOW` | Assemble outcomes → evaluate → discard learner effects | OFF | Design only (E5 shadow uses master flag) |
| `ENABLE_EXPERIMENT_ASSIGNMENT` | Allow reading assignment maps for controlled experiments | OFF | Design only (E2 assignment uses master flag) |
| `ENABLE_POLICY_EVALUATION` | Emit EvaluationRecords to governance sinks | OFF | Design only (E3 evaluation uses master flag) |
| `ENABLE_OUTCOME_ANALYTICS` | Aggregate analytics exports (non-student) | OFF | Design only (E4 analytics uses master flag) |

**Rollback:** Disabling `ENABLE_EVIDENCE_PLATFORM` / `KWALITEC_EVIDENCE_PLATFORM` immediately removes Evidence Platform participation without affecting Runtime A, Twin, Adaptive, Strategy, or Experience.

**Law:** Evidence Platform flags must never be required for educational serving. Upstream Authority flags remain independently controlled.

---

## 10. Shadow validation strategy (overview)

**Implementation status:** E5 Shadow Validation **Implemented** (`EvidenceShadowValidator` + monitors / health / rollback / readiness / telemetry). Detailed phases: `MIGRATION_PLAN_MS006.md`. Readiness artefact: `EVIDENCE_PLATFORM_READINESS_REPORT.md`.

```
EvidenceRecord / ExperimentObservation / PolicyEvaluation /
AnalyticsSummary / EvidenceProjection
        │
        ▼
DeterminismValidator
        │
        ▼
OperationalHealthMonitor
        │
        ▼
ReadinessEvaluator → ReadinessReport
        │
        ▼
Telemetry / Discard (no learner-visible effects; no policy deployment)
```

| Shadow rule | Binding |
|---|---|
| No learner UX change from Evidence Platform | Absolute during shadow |
| No auto-promotion of upstream Authority | Absolute |
| Deterministic reconstruction / readiness from frozen inputs | Required before Ready |
| Compare organisation metrics vs learning-depth metrics separately | Required (SP8) |
| Soak monitors for claim-boundary leakage | Required (observational drift signals) |

---

## 11. Acceptance criteria (architecture review)

PASS only if:

| # | Criterion |
|---|---|
| ✓ | Measurement remains separate from educational authority |
| ✓ | Runtime A remains authoritative for educational facts |
| ✓ | Twin remains interpretive |
| ✓ | Adaptive remains recommendation-only |
| ✓ | Strategy remains orchestration-only |
| ✓ | Experience remains presentation (for educational serving) |
| ✓ | Evidence Platform remains observational |
| ✓ | No reverse dependencies into Runtime A / Twin / Adaptive / Strategy / Experience as write owners |
| ✓ | Explainability five-answers mandatory for policy evaluation |
| ✓ | No production code introduced by this directive |
| ✓ | No schema changes introduced by this directive |

---

## 12. ADR-MS006-001 — Evidence Platform Authority Boundaries (draft)

**Status:** Proposed (architecture gate; ratify before E0)  
**Context:** MS-003–MS-005 introduce advice and orchestration layers. Without a measurement boundary, teams risk treating analytics, experiments, or evaluation “PASS” as educational truth or auto-cutover authority.

**Decision:**

1. Evidence Platform may **read** Runtime A and **consume** upstream observational traces.  
2. Evidence Platform must **not write** educational facts, Twin claims, Adaptive rankings, Strategy interventions, or Experience authority.  
3. Experiment variants may only be expressed through **documented upstream flags / policy knobs**, assigned and measured by Evidence Platform — not by inventing parallel educational write paths.  
4. Evaluation outcomes are **governance recommendations**, not student-facing decisions.  
5. Organisation outcomes and learning-depth outcomes must remain **separately typed** (EP-004 SP8).  
6. Declaring “Evidence Platform Ready” requires shadow soak + explainability gate proof + governance process rehearsal — not docs alone.

**Consequences:** Implementation phases (E0+) must include write-guard tests, claim-boundary tests, and flag-independence tests. Premature Ready is a Critical programme risk (`RISK_ANALYSIS_MS006.md`).

---

## 13. Companion index

| Document | Role |
|---|---|
| [EVIDENCE_MODEL.md](EVIDENCE_MODEL.md) | Evidence lifecycle, artefact types, claim boundaries, quality |
| [EXPERIMENT_FRAMEWORK.md](EXPERIMENT_FRAMEWORK.md) | Experiment protocol, assignment, measurement, analysis |
| [POLICY_EVALUATION.md](POLICY_EVALUATION.md) | Policy versions, evaluation workflow, explainability gate |
| [OUTCOME_ANALYTICS.md](OUTCOME_ANALYTICS.md) | Analytics responsibilities, metric families, anti-patterns |
| [GOVERNANCE_MODEL.md](GOVERNANCE_MODEL.md) | Propose → review → decide → roll back process |
| [EVIDENCE_TRACEABILITY.md](EVIDENCE_TRACEABILITY.md) | Full observational chain reconstruction |
| [MIGRATION_PLAN_MS006.md](MIGRATION_PLAN_MS006.md) | Phases E0–E7, flags, Ready checklist |
| [RISK_ANALYSIS_MS006.md](RISK_ANALYSIS_MS006.md) | Authority inversion, false causation, claim leakage, etc. |
| [EVIDENCE_PLATFORM_READINESS_REPORT.md](EVIDENCE_PLATFORM_READINESS_REPORT.md) | E5 operational readiness / architecture review gate |

---

## 14. Implementation readiness

| Item | Status |
|---|---|
| Architecture documentation set | **Delivered (Directive 001)** |
| ADR-MS006-001 ratified | Pending architecture review |
| E0 Contracts / DTOs / EvidenceAdapter / DI | **Implemented (Directive 002)** |
| E1 Evidence Collection (collector / assembler / validator / factory / telemetry) | **Implemented (Directive 003)** |
| E2 Experiment Framework (registry / assigner / framework / observation / telemetry) | **Implemented (Directive 004)** |
| E3 Policy Evaluation (evaluator / assembler / validator / explainability / factory / telemetry) | **Implemented (Directive 005)** |
| E4 Analytics & Projection (aggregator / engine / projector / projection port / telemetry) | **Implemented (Directive 006)** |
| E5 Shadow Validation & Operational Readiness | **Implemented (Directive 007)** |
| Master flag `KWALITEC_EVIDENCE_PLATFORM` | **Implemented** (default OFF) |
| Analytics behaviour | **Implemented (E4)** — governance-facing only |
| Shadow / readiness | **Implemented (E5)** — observational only; no policy deployment |
| Schema / Alembic | **None** |
| Evidence Platform Ready | **Not declared** — await architecture review |

**Next step:** Architecture / implementation review of E0–E5. Do **not** begin a new milestone. Do **not** declare Evidence Platform Ready without review.

---

## 15. Stop condition

**Stop after E5 Shadow Validation & Operational Readiness.**

Do **not** implement policy promotion / deployment.  
Do **not** modify Runtime A, Twin, Adaptive Engine, Strategy Engine, or Experience educational behaviour.  
Do **not** begin a new milestone.

Await architecture / implementation review before declaring Evidence Platform Ready / MS-006 complete.
