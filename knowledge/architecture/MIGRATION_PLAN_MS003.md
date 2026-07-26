# MS-003 — Migration Plan (Adaptive Learning Engine)

**Milestone:** MS-003 — Adaptive Learning Intelligence  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `ADAPTIVE_ENGINE_ARCHITECTURE.md`  
**Risks:** `RISK_ANALYSIS_MS003.md`  
**Depends on:** MS-001 Recommendation Read Bridge (implemented); MS-002 Journey/History (implemented, optional context)

---

## Principles

1. **Incremental** — each phase independently releasable.  
2. **Reversible** — feature-flag rollback per phase.  
3. **No big-bang** — never flip Engine + Planning consumption + sole-runtime together.  
4. **No schema changes** for Adaptive Engine Ready.  
5. **No UI redesign.**  
6. **No educational writes** inside Adaptive Engine.  
7. **Do not change recommendation algorithms** until an explicit later ADR.  
8. **Shadow before serve** — compare against Recommendation Bridge before UX cutover.  
9. **Empty authentic / bridged fallback over demo** when Engine flags are on.

---

## Phase overview

| Phase | Name | Releasable? | Educational write? | Changes recommendation algorithms? |
|---|---|---|---|---|
| A0 | Contracts, fixtures, ADRs | Yes — **Implemented** | No | No |
| A1 | Input assembler + golden snapshots | Yes | No | No |
| A2 | Shadow Adaptive Engine | Yes | No | No |
| A3 | ExplanationBundle completeness gate | Yes | No | No |
| A4 | AdaptiveDecisionPort cutover (flagged) | Yes | No | No (composition only) |
| A5 | Traceability / outcome linkage (observational) | Yes | No | No |
| A6 | Dual-run soak + monitors | Yes | No | No |
| A7 | Internal Alpha — Adaptive Engine Ready | Yes (ops) | No | No |
| — | **Adaptive Engine Ready** | — | AE-1…AE-10 | — |

Planning advisory consumption and Recommendation algorithm changes are **explicitly out of Ready** unless product expands via ADR-MS003-003 / separate directive.

---

## A0 — Contracts, fixtures, ADRs

### Scope

- Accept MS-003 architecture docs.  
- Accept ADR-MS003-001; draft ADR-MS003-002.  
- Capture golden learners: empty evidence, mid-plan learning, revision stage, mission-aligned day, sparse attempts.  
- Document expected decision kinds + ExplanationBundles.  
- **Implemented (Directive 002):** `AdaptiveDecisionContract`, `ExplanationBundle`, `AdaptiveInputBundle`, `AdaptiveOutputBundle`, `AdaptiveEngineBridge`, DI behind `ENABLE_ADAPTIVE_ENGINE` (default OFF), contract / serialization / determinism tests. No assembler; no Experience cutover.

### Exit criteria

- ADRs accepted for authority boundary.  
- Fixture table agreed.  
- **Contracts compile; DTOs immutable; serialization deterministic; flag defaults OFF.**

### Rollback

N/A (docs + inert contracts; flag OFF restores prior behaviour with no Adaptive Engine construction).

---

## A1 — Input assembler + golden snapshots

### Scope

- Read-only assembler producing `AdaptiveInputBundle` behind `ENABLE_ADAPTIVE_ENGINE`.  
- Authority tags + field provenance + bounds on history.  
- **No** Experience cutover; **no** Engine scoring required beyond pass-through tests.
- **Implemented (Directive 003):** `AdaptiveInputAssembler`, Runtime A collectors (evidence, topic progress, study attempts, missions, readiness, curriculum, student goals, lifecycle), validation, normalization, field provenance, DI, unit/integration/determinism/provenance/missing-data tests. No shadow (A2); no Experience cutover.

### Exit criteria

- Snapshots match Runtime A for golden users (TopicProgress, missions, readiness pass-through).  
- No write APIs in assembler call graph.
- **Every field exposes provenance; missing inputs return explicit unavailable contracts; DTO determinism preserved; flag defaults OFF.**

### Rollback

Disable assembler flag / leave unused.

---

## A2 — Shadow Adaptive Engine

### Scope

- Deterministic decision compute emitting `AdaptiveOutputBundle` via `AdaptiveEngineExecutor`.  
- `ENABLE_ADAPTIVE_ENGINE_SHADOW` (env: `KWALITEC_ADAPTIVE_SHADOW` or `KWALITEC_ADAPTIVE_ENGINE_SHADOW`) → `AdaptiveShadowOrchestrator` + telemetry `ADAPTIVE_SHADOW_*`.  
- Experience UX unchanged; outputs discarded for UX.
- **Implemented (Directive 004):** Executor, shadow orchestrator, ExplanationBundle population (`inputs_used` / `inputs_unavailable`), shadow telemetry, DI, unit/integration/determinism/explainability/isolation tests. No Experience cutover; no RecommendationService / Planning changes; no Explainability Gate (A3).

### Exit criteria

- Shadow produces AdaptiveOutputBundles with complete ExplanationBundles.  
- Determinism replay on fixtures (identical input → identical output).  
- Zero educational writes; Runtime A / Experience unchanged.  
- Feature flags default OFF.

### Rollback

Disable shadow flag.

---

## A3 — ExplanationBundle completeness gate

### Scope

- Enforce Explainability Gate quality rules on every AdaptiveOutputBundle (recommendation, confidence, evidence refs, inputs_used, inputs_unavailable, recommendation rationale, rule refs).  
- Emit `EXPLAINABILITY_GATE_*` observational telemetry.  
- Failed bundles remain shadow-only / observational — no correction, no Experience authority.  
- **Implemented (Directive 005):** `ExplainabilityGate`, quality rules, ExplanationBundle validator, gate telemetry, DI, unit/integration/failure-path tests. No Experience cutover (A4); no RecommendationService / Planning / schema / UI changes.

### Exit criteria

- Complete ExplanationBundles PASS; incomplete FAIL with `EXPLAINABILITY_INCOMPLETE`.  
- No mutation of AdaptiveOutputBundle; Runtime A / Experience unchanged.  
- Gate DI only when `KWALITEC_ADAPTIVE_ENGINE` **and** `KWALITEC_ADAPTIVE_SHADOW` are ON (default OFF).

### Rollback

Disable Engine and/or Shadow flags; gate is not constructed.

---

## A4 — AdaptiveDecisionPort cutover (flagged)

### Scope

- `ENABLE_ADAPTIVE_ENGINE` + `ENABLE_ADAPTIVE_ENGINE_SHADOW` + `ENABLE_ADAPTIVE_AUTHORITY` → AdaptiveExperiencePortRouter may serve Home recommendation via AdaptiveDecisionPort.  
- Preserve MS-001 mission alignment (executor / projection).  
- On failure / incomplete explanation (Gate FAIL) → fallback to Recommendation Bridge / RecommendationService.  
- **Do not** rewrite RecommendationService rule bodies.  
- **Implemented (Directive 006):** port router, eligibility consumption, Authority flag (default OFF), fallback, cutover telemetry, unit/integration tests. A5 Observational Traceability delivered under Directive 007. No Planning / UI / schema changes.

### Exit criteria

- AC-A1…AC-A8 architecture criteria held in tests.  
- No `seeded_demo_adaptive` authority when Recommendation Bridge / adaptive authority on.  
- Legacy dashboard RecommendationService path unchanged.  
- Adaptive authority disabled by default.

### Rollback

Disable `ENABLE_ADAPTIVE_AUTHORITY` (or Engine / Shadow) → Recommendation Bridge / prior path immediately.

---

## A5 — Traceability / outcome linkage (observational)

### Scope

- Persist or telemetric `decision_id` linkage per ADR-MS003-002 policy (DTO/telemetry; no educational mutation).  
- Golden chain Evidence → Decision → Recommendation → Outcome.  
- **Implemented (Directive 007):** `TraceabilityService`, `DecisionTrace`, correlation IDs, lineage reconstruction, `ADAPTIVE_TRACE_*` telemetry, DI behind Engine/Shadow flags, unit/integration tests. No schema / Planning / UI / recommendation algorithm changes. Outcome soak remains A6+.

### Exit criteria

- AT-1…AT-6 pass (architecture).  
- AT-A5-1…AT-A5-3 pass (DecisionTrace completeness, deterministic lineage, correlation consistency).  
- `unavailable` used honestly when linkage impossible.  
- Runtime A remains read-only; RecommendationService behaviour unchanged when Authority OFF.

### Rollback

Disable Engine / Shadow flags (traceability DI drops); or ignore emitters. Engine UX may remain under Authority independently.

---

## A6 — Dual-run soak + monitors

**Status → Implemented** (Directive 008)

### Scope

- `ShadowSoakOrchestrator`: RecommendationService baseline + Adaptive shadow → compare → measure → record (never UX).  
- Monitors: recommendation comparison, determinism replay, drift detection (telemetry only).  
- Health metrics: latency, agreement / divergence, explainability pass, trace creation, deterministic replay, fallback frequency.  
- Rollback verification: Engine OFF or Authority OFF → RecommendationService sole authority.  
- Ops hooks: `build_soak_ops_dashboard`, `DualRunStatus.adaptive_shadow_soak`.

### Exit criteria

- Soak window automation green (stable replay, measurable divergence, drift signals, rollback drill).  
- No Critical open Engine risks unmitigated for observational soak.  
- Rollback drill documented + automated.  
- Readiness report published; **await architecture review** before A7 Ready declaration.

### Rollback

Flags off (`KWALITEC_ADAPTIVE_ENGINE` / `KWALITEC_ADAPTIVE_AUTHORITY` / Shadow as needed).

---

## A7 — Internal Alpha — Adaptive Engine Ready

### Scope

- Gate review against § Adaptive Engine Ready definition.  
- Explicitly **do not** enable Planning consumption or sole-runtime as part of this gate.

### Exit criteria

- AE-1…AE-10 scorecard green.  
- Product accepts Ready.

### Rollback

Hold / disable Engine flag; Recommendation Bridge remains.

---

## Adaptive Engine Ready checklist (AE)

| ID | Criterion |
|---|---|
| AE-1 | Engine consumes Runtime A authoritative inputs only |
| AE-2 | History / educational facts immutable from Engine |
| AE-3 | ExplanationBundle complete on UX decisions |
| AE-4 | No educational writes in Engine/adapter call graph |
| AE-5 | Feature flags + verified rollback |
| AE-6 | Mission alignment preserved |
| AE-7 | Curriculum V1/V2 traversal preserved |
| AE-8 | Deterministic replay on golden snapshots |
| AE-9 | Shadow soak completed |
| AE-10 | Traceability chain documented for ≥1 golden learner |

---

## Explicit non-goals until later directives

- Changing RecommendationService algorithms  
- PlanningService consuming Adaptive advice to generate missions  
- Schema migrations for decision audit (optional ADR later)  
- UI redesign of recommendation / coach surfaces  
- LLM cores in educational decision centre  

---

## Dependency notes

| Dependency | Required for Ready? |
|---|---|
| MS-001 Recommendation Read Bridge | **Yes** (fallback + shadow baseline) |
| MS-001 Mission Read / Start | **Yes** (alignment + Start authority) |
| MS-002 Journey/History | **No** (optional context) |
| Evidence Before Completion | **Yes** for meaningful evidence inputs; Engine still safe with sparse evidence |
