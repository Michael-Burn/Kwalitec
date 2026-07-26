# MS-005 — Strategy Pipeline

**Milestone:** MS-005 — Learning Strategy & Intervention Engine  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_STRATEGY_ENGINE_ARCHITECTURE.md`  
**Related:** `INTERVENTION_MODEL.md`, `STRATEGY_INTERFACE_SPECIFICATION.md`, `ADAPTIVE_DECISION_PIPELINE.md`

---

## 1. Purpose

Define the end-to-end orchestration flow from authoritative Runtime A state through Twin interpretation and Adaptive recommendations to Experience, with an explicit **no educational writes** boundary inside the Strategy Engine.

---

## 2. End-to-end pipeline

```
Runtime A
   ↓  (authoritative educational facts)
Student Digital Twin
   ↓  (interpretation — TwinSnapshot)
Adaptive Engine
   ↓  (recommendation — AdaptiveDecisionRecord)
Learning Strategy Engine
   ↓  (orchestration — StrategyDecisionRecord + InterventionPlan)
Experience
   ↓  (presentation — existing UI surfaces)
(Student action → Runtime A write paths only — outside Strategy)
```

### Pipeline invariant

| Stage | May read educational state? | May write educational state? |
|---|---|---|
| Runtime A services (authorised workflows) | Yes | Yes |
| Twin assembly | Yes (Runtime A) | **No** educational SoT; Twin artefacts only |
| Adaptive Engine | Yes (Runtime A + Twin) | **No** |
| Strategy Engine | Yes (Runtime A + Twin + Adaptive) | **No** |
| Experience presentation | Yes (DTOs) | **No** educational writes |
| Student Start / Complete / Plan edit | — | Yes, via Runtime A only |

---

## 3. Stages (detailed)

### Stage 0 — Trigger

| Trigger | Example | Notes |
|---|---|---|
| Home load | Tonight’s intervention / session shell | Primary Experience path |
| Revision load | Revision plan structure | Lifecycle Revision |
| Post-failure / abandon signal | Recovery plan request | Observational or flagged |
| Shadow cron / dual-run | Compare vs prior Experience path | No UX change |
| Explicit refresh | Strategy port refresh | Optional |

Triggers **request orchestration**; they do not authorise educational mutation.

### Stage 1 — Runtime A authority check

1. Resolve `student_id` ownership.  
2. Confirm active StudyPlan (or document `NO_ACTIVE_PLAN`).  
3. Load lifecycle stage (`LearningLifecycleService`).  
4. Load today’s Mission if any — required for session alignment.  
5. Collect bounded evidence / attempt / progress / goals / curriculum context.

**Failure:** `FORBIDDEN` / `NO_ACTIVE_PLAN` / `UNAVAILABLE` → empty authentic or prior Experience path per flag policy.

### Stage 2 — Twin consumption

1. Obtain immutable `TwinSnapshot` (or unavailable attachment).  
2. Record Twin facet availability for fatigue / confidence / rhythm factors.  
3. **Must not** call Twin builders if Adaptive/Twin already supplied a snapshot — consume only.

**Missing Twin:** continue with `twin_unavailable` limitation; never estimate facets.

### Stage 3 — Adaptive consumption

1. Obtain `AdaptiveDecisionRecord` / AdaptiveOutputBundle (or RecommendationService fallback snapshot when Adaptive Authority off).  
2. Preserve Adaptive primary + alternatives order.  
3. Capture Adaptive ExplanationBundle refs for Strategy explanation lineage.

**Missing Adaptive:** `adaptive_unavailable`; do not invent next-topic ranking.

**Forbidden in Stage 3:** Re-scoring Adaptive candidates; mutating AdaptiveDecisionRecord.

### Stage 4 — Strategy input assembly

Assemble `StrategyInputBundle`:

```
StrategyInputBundle {
  student_id,
  as_of,
  runtime_a_snapshot,           # evidence, progress, missions, goals, curriculum, readiness
  twin_attachment,              # TwinSnapshot ref + availability
  adaptive_attachment,          # AdaptiveDecisionRecord ref + availability
  mission_context,              # mission_id?, topic, aligned policy
  field_provenance{},           # per-block availability / source
  serialize()
}
```

**Assembler MAY:** collect, normalize, validate, annotate provenance.  
**Assembler MUST NOT:** estimate missing values, rank topics, mutate Runtime A / Twin / Adaptive.

**Determinism:** identical inputs + identical `as_of` → identical `StrategyInputBundle.serialize()`.

### Stage 5 — Strategy execution (orchestration)

Logical steps (design — not implementation):

1. **Detect constraints** — mission alignment, lifecycle stage, sparse evidence.  
2. **Evaluate fatigue** — Twin load + Runtime A activity → optional FatigueIntervention.  
3. **Evaluate recovery triggers** — abandoned / failed / gap signals.  
4. **Evaluate confidence divergence** — Twin confidence vs Runtime A performance.  
5. **Select primary intervention kind** — composition rules (`INTERVENTION_MODEL.md` §11).  
6. **Build plan structures** — Session / Revision / Study / Recovery as applicable.  
7. **Attach Adaptive topic identity** — primary or advisory; never invent competing primary.  
8. **Compute Strategy confidence** — reflects input completeness, not Adaptive score copy.  
9. **Build StrategyExplanationBundle** (mandatory).  
10. Emit **StrategyDecisionRecord** + **InterventionPlan**.

**Forbidden in Stage 5:**

- `generate_today_mission` / mission create / Planning writes  
- TopicProgress / StudyAttempt / Evidence writes  
- Twin snapshot mutation  
- Adaptive re-ranking  
- LLM / opaque generative reasoning  

### Stage 6 — Explainability Gate

Validate StrategyExplanationBundle completeness (see `STRATEGY_EXPLAINABILITY.md`).

| Outcome | Meaning |
|---|---|
| **PASS** | Eligible for Experience when Authority ON |
| **FAIL** | Shadow-only / ineligible; no mutation of plan; emit gate telemetry |

### Stage 7 — Routing / delivery

```
Default (any Strategy flag OFF / Authority OFF)
  → Prior Experience path (Adaptive/Recommendation/checklist)

When ENGINE + SHADOW + AUTHORITY ON:
  Gate PASS → StrategyInterventionPort (authority=strategy_engine)
  Gate FAIL / exception → Fallback prior Experience path
```

Shadow-only: emit telemetry; discard for UX.

### Stage 8 — Student action (outside Strategy)

Start / Resume / Complete / Plan edit remain Runtime A. Strategy may later **observe** outcome linkage for traceability — never write outcomes.

---

## 4. Shadow pipeline

```
Prior Experience baseline
Strategy Engine (shadow) → StrategyDecisionRecord
Compare → Measure → Record
Never influence the student
```

Soak monitors (design): agreement on primary topic identity vs Adaptive/Recommendation; determinism replay; explainability pass rate; drift telemetry. Details: `MIGRATION_PLAN_MS005.md` phase S6.

---

## 5. Mission alignment policy

| Situation | Session primary topic | Adaptive primary |
|---|---|---|
| SQL Mission exists | **Mission topic** | If equal → aligned; if differs → advisory / supporting only |
| No mission | Adaptive primary (when available) | Primary topic identity |
| Adaptive unavailable | Mission topic or empty authentic | N/A |

This preserves MS-001 dual-“next” policy: Planning/Mission owns Start; Strategy structures the night around that authority.

---

## 6. Failure and degradation matrix

| Failure | Strategy behaviour |
|---|---|
| Runtime A unavailable | `UNAVAILABLE`; fallback Experience |
| No active plan | `NO_ACTIVE_PLAN`; empty authentic |
| Twin unavailable | Proceed; mark Twin factors unavailable |
| Adaptive unavailable | Proceed only with honest limitations **or** fail open to prior path — never invent ranking |
| Explainability incomplete | Gate FAIL; no Authority delivery |
| Executor exception | Fallback; `STRATEGY_FAILED` telemetry |

---

## 7. Telemetry events (design)

| Event | When |
|---|---|
| `STRATEGY_REQUESTED` | Orchestration begins |
| `STRATEGY_ASSEMBLED` | Input bundle ready |
| `STRATEGY_COMPLETED` | Decision record emitted |
| `STRATEGY_FAILED` | Exception / hard failure |
| `STRATEGY_GATE_PASSED` / `FAILED` | Explainability Gate |
| `STRATEGY_SHADOW_*` | Shadow observation |
| `STRATEGY_FALLBACK` | Authority path fell back |
| `STRATEGY_LATENCY` | Observational latency |

Telemetry must not include raw answers, secrets, or cross-student data.

---

## 8. Sequence (Load Home — Authority ON)

```
Experience Home
  → StrategyInterventionPort.get_tonights_intervention(student_id)
    → StrategyInputAssembler
         → Runtime A reads
         → Twin consume
         → Adaptive consume
    → StrategyExecutor.orchestrate(bundle)
    → StrategyExplainabilityGate
         PASS → project OpaqueDict to Home
         FAIL → Recommendation/Adaptive/checklist fallback
```

Student Start Session remains Mission/Planning Runtime A path — Strategy session plan is advice structure, not mission create.
