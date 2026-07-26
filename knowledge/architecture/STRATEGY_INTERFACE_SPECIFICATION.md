# MS-005 — Strategy Interface Specification

**Milestone:** MS-005 — Learning Strategy & Intervention Engine  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design — **no implementation**  
**Parent:** `LEARNING_STRATEGY_ENGINE_ARCHITECTURE.md`  
**Extends:** MS-003 Adaptive contracts; MS-004 Twin consume patterns; MS-001 BridgeResult / TraceRef patterns  
**Companions:** `INTERVENTION_MODEL.md`, `STRATEGY_EXPLAINABILITY.md`, `STRATEGY_PIPELINE.md`

---

## 0. Conventions

### Layers

| Layer | Responsibility |
|---|---|
| Experience Port / Facade | `StrategyInterventionPort`, HomeService, EducationalStateService |
| Strategy Engine Adapter | Assembles inputs; invokes Executor; projects DTOs; telemetry; flags |
| Learning Strategy Engine | Pure orchestration + StrategyExplanationBundle |
| Adaptive Engine | Recommendation artefacts (consume) |
| Digital Twin | Interpretation artefacts (consume) |
| Educational Services | Authoritative Runtime A **read** APIs |
| Database / Curriculum | Existing SQLAlchemy models / Curriculum JSON |

### Shared types (logical)

| Type | Meaning |
|---|---|
| `StudentId` | Authenticated user id |
| `TopicCode` | Curriculum topic identifier |
| `StrategyDecisionId` | Stable id for StrategyDecisionRecord |
| `AdaptiveDecisionId` | Adaptive decision id consumed |
| `MissionId` | SQL Mission.id (stringified) |
| `AttemptId` | StudyAttempt.id (stringified) |
| `OpaqueDict` | Projection document safe for Experience |
| `BridgeResult[T]` | `{ ok, value?, error_code?, message?, fallback_used }` |
| `StrategyExplanationBundle` | See `STRATEGY_EXPLAINABILITY.md` |
| `StrategyInputBundle` | See §3 |
| `StrategyDecisionRecord` | See §2 |
| `InterventionPlan` | See `INTERVENTION_MODEL.md` |

### Shared failure codes

Reuse MS-001 / MS-002 / MS-003 codes where applicable:

| Code | Meaning |
|---|---|
| `UNAVAILABLE` | Downstream service or DB unreachable |
| `NO_ACTIVE_PLAN` | No active StudyPlan |
| `NOT_FOUND` | Insufficient context for intervention kind |
| `FORBIDDEN` | Ownership failure |
| `INVALID_STATE` | Malformed request / illegal as_of |
| `STRATEGY_EXPLAINABILITY_INCOMPLETE` | Orchestration computed but explanation incomplete — **must not ship as guidance** |
| `STRATEGY_INPUT_UNAVAILABLE` | Critical Adaptive/Runtime A input missing for safe orchestration |
| `BEHAVIOUR_MISMATCH` | Parity / golden check (tests only) |

### Shared read-only rule

Strategy Engine Adapter / Engine **must not**:

- Call Planning ensure/generate / mission create  
- Start / resume / complete sessions  
- Write TopicProgress or StudyAttempt  
- Accept evidence  
- Mutate StudyPlan  
- Mutate Twin snapshots  
- Mutate / re-rank AdaptiveDecisionRecord  
- Emit demo seeds when Strategy Engine flags are on  
- Change RecommendationService or Adaptive algorithm bodies  

---

## 1. `StrategyEngineBridge` (adapter)

**Purpose:** Experience StrategyInterventionPort backed by Learning Strategy Engine.  
**Ownership:** Infrastructure adapter (future package design: `app/infrastructure/adapters/strategy_engine/`).  
**Educational owners (read):** Runtime A read APIs; Twin consume; Adaptive consume.

### 1.1 `orchestrate`

**Inputs**

| Name | Type | Required | Notes |
|---|---|---|---|
| `student_id` | StudentId | Yes | Current user |
| `as_of` | datetime | No | Defaults to server now (decision clock when provided) |
| `intervention_kinds` | list[str] | No | Default composite selection per composition rules |
| `include_explanation` | bool | No | Default **true** (required true for UX guidance) |
| `shadow` | bool | No | Force shadow semantics for this call |
| `adaptive_decision_id` | AdaptiveDecisionId | No | Pin consumption to a known Adaptive decision |
| `twin_snapshot_ref` | str | No | Pin consumption to a known Twin snapshot |

**Outputs** (`BridgeResult[StrategyDecisionRecord]`)

Success value: §2 record.  
On `STRATEGY_EXPLAINABILITY_INCOMPLETE`: `ok=false` (or ok with `fallback_used` to prior Experience path — product policy: **prefer fallback over unexplained guidance**).

### 1.2 `get_tonights_intervention` (Experience-shaped)

Projects StrategyDecisionRecord into OpaqueDict compatible with Home / session shell:

```
{
  primary_intervention_kind,
  topic_title,
  topic_code,
  session_plan,              # phases / minutes / close_ritual (nullable)
  revision_plan,             # nullable
  recovery_plan,             # nullable
  fatigue,                   # nullable
  confidence_intervention,   # nullable
  explanation_summary,       # from StrategyExplanationBundle.why.summary
  educational_principle_ids,
  adaptive_decision_id,
  twin_snapshot_ref,
  confidence_band,
  mission_aligned,
  strategy_decision_id,
  authority: "strategy_engine",
  explanation,               # full or compact StrategyExplanationBundle
  fallback_used,
  limitations
}
```

**Mission alignment:** If today’s Mission exists, `topic_title` / `topic_code` **equal** mission topic; `mission_aligned=true`. Adaptive differing topic appears under advisory fields / supporting interventions — never as contradictory primary.

### 1.3 `compare_shadow` (ops / dual-run)

**Inputs:** `student_id`, `as_of`  
**Outputs:** Strategy record + prior Experience baseline snapshot + diff summary (primary kind, topic, fatigue/recovery presence).  
**No UX mutation.**

---

## 2. `StrategyDecisionRecord`

```
StrategyDecisionRecord {
  decision_id,
  student_id,
  as_of,
  engine_version,
  intervention_plan,           # InterventionPlan
  explanation,                 # StrategyExplanationBundle
  confidence: { score?, band, rationale },
  input_fingerprint,
  runtime_a_snapshot_id,
  twin_snapshot_ref?,
  adaptive_decision_id?,
  authority_status,
  feature_flag_state,
  serialize()
}
```

**Immutability:** Records are immutable value objects.  
**Determinism:** identical material inputs → identical `serialize()` / `decision_id`.

---

## 3. `StrategyInputBundle`

```
StrategyInputBundle {
  student_id,
  as_of,
  runtime_a: {
    evidence_summary,
    topic_progress[],
    study_attempts[],
    mission_history[],
    readiness?,
    curriculum_context,
    student_goals,
    lifecycle_stage,
    active_mission?
  },
  twin: {
    availability,              # available | unavailable
    snapshot?,                 # TwinSnapshot material or ref
    unavailable_reason?
  },
  adaptive: {
    availability,
    decision?,                 # AdaptiveDecisionRecord material or ref
    unavailable_reason?
  },
  field_provenance{},
  serialize()
}
```

### Provenance keys (per field / block)

| Key | Meaning |
|---|---|
| `source_service` | Authority that supplied the field |
| `source_entity` | Entity / aggregate name |
| `collected_at` | Equals assembler `as_of` |
| `availability` | `available` or `unavailable` |
| `unavailable_reason` | Required when unavailable |

**Assembler MUST NOT:** estimate missing values, rank topics, or mutate upstream systems.

---

## 4. `StrategyInterventionPort` (Experience)

| Method | Meaning |
|---|---|
| `get_tonights_intervention(student_id, as_of?)` | Primary Home / director structure |
| `get_revision_intervention(student_id, as_of?)` | Revision surface structure |
| `get_recovery_intervention(student_id, trigger?, as_of?)` | Recovery structure when triggered |
| `explain(strategy_decision_id)` | Fetch StrategyExplanationBundle |

Port returns OpaqueDict / BridgeResult shapes — **never** Strategy executor internals, Twin builders, or Adaptive executor objects.

---

## 5. Dependency injection (design)

```
composition root
  → build_strategy_engine_adapter(flags)
       → StrategyInputAssembler(runtime_a_readers, twin_consumer, adaptive_consumer)
       → StrategyExecutor
       → StrategyExplainabilityGate
       → StrategyTraceabilityService (optional)
       → StrategyExperiencePortRouter
  → Experience StrategyInterventionPort
```

| Flag | Effect |
|---|---|
| Engine OFF | No Strategy DI / inert |
| Engine ON + Shadow ON | Observational orchestration |
| Authority ON (+ Engine + Shadow) | Router may serve Strategy projections on Gate PASS |

Defaults: all **OFF**.

---

## 6. Fallback contract

| Condition | Behaviour |
|---|---|
| Authority OFF | Prior Experience path (Adaptive / Recommendation / checklist) |
| Gate FAIL | Prior Experience path + `STRATEGY_GATE_FAILED` |
| Strategy exception | Prior Experience path + `STRATEGY_FALLBACK` |
| Adaptive unavailable under Strategy | Document limitation **or** fallback — never invent Adaptive ranking |
| Twin unavailable | Strategy may continue with Twin unavailable markers |

**Student-visible rule:** No degradation theatre; empty authentic preferred over demo seeds when Strategy flags on.

---

## 7. Compatibility with Adaptive / Twin ports

| Port | Strategy interaction |
|---|---|
| `AdaptiveDecisionPort` | Strategy **consumes** Adaptive outputs; does not replace Adaptive port unless a later ADR explicitly routes Experience through Strategy-only |
| `StudentTwinPort` | Strategy **consumes** Twin snapshots / projections; does not own Twin UX authority |
| `RecommendationBridge` | Fallback / baseline for shadow compare |

**Design intent for MS-005 Authority:** Experience may consume Strategy for **intervention structure** while Adaptive remains recommendation authority upstream. Product may later choose Strategy as the sole student-facing director DTO — only via ADR, after soak.

---

## 8. Test contracts (future implementation)

| Suite | Asserts |
|---|---|
| Unit | Executor determinism; composition rules; explanation completeness |
| Integration | Assembler provenance; mission alignment; fallback |
| Boundary | No Runtime A / Twin / Adaptive writes; no reverse imports |
| Golden | Fixture learners → stable InterventionPlan serialize |
| Gate | Incomplete explanations never Authority-delivered |

---

## 9. Non-goals (this specification)

- Concrete Python modules or feature-flag wiring in application code  
- Alembic tables for StrategyTrace persistence  
- UI template changes  
- Changes to Adaptive / Twin interface specs  

This document is the contract target for a future S0+ implementation milestone after architecture review.
