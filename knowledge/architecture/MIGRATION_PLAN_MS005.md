# MS-005 — Migration Plan (Learning Strategy & Intervention Engine)

**Milestone:** MS-005 — Learning Strategy & Intervention Engine  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_STRATEGY_ENGINE_ARCHITECTURE.md`  
**Risks:** `RISK_ANALYSIS_MS005.md`  
**Depends on:** MS-001 Runtime Bridge; MS-003 Adaptive contracts (recommended A0–A3+); MS-004 Twin contracts (recommended T0–T4+ for fatigue/confidence)

---

## Principles

1. **Incremental** — each phase independently releasable.  
2. **Reversible** — feature-flag rollback per phase.  
3. **No big-bang** — never flip Strategy Authority + Adaptive Authority + Twin Authority together.  
4. **No schema changes** for Strategy Ready.  
5. **No UI redesign.**  
6. **No educational writes** inside Strategy.  
7. **No Runtime A / Twin / Adaptive redesign** in Strategy phases.  
8. **Shadow before serve** — orchestrate before Experience cutover.  
9. **Empty authentic / bridged fallback over demo** when Strategy flags are on.  
10. **Runtime A wins** fact conflicts; **Adaptive wins** recommendation ranking; **Strategy orchestrates only**.  
11. **Architecture first** — this directive stops at docs; S0 begins only after architecture review PASS.

---

## Phase overview

| Phase | Name | Releasable? | Educational write? | Changes Adaptive/Twin? |
|---|---|---|---|---|
| — | Architecture docs (this directive) | Yes (docs) | No | No |
| S0 | Contracts, fixtures, ADRs | Yes (docs/tests) | No | No |
| S1 | Strategy Input Assembler / Core Strategy Engine | Yes | No | No (consume only) |
| S2 | Strategy Executor + intervention builders | Yes | No | No |
| S3 | Strategy Explainability Gate | Yes | No | No |
| S4 | Shadow execution | Yes | No | No |
| S5 | Observational Strategy traceability | Yes | No | No |
| S6 | Shadow soak + monitors | Yes (ops) | No | No |
| S7 | Experience cutover (flagged Authority) | Yes | No | No |
| — | **Learning Strategy Engine Ready** | — | S0–S7 | — |

---

## Architecture review gate (before S0)

### Scope

- Accept MS-005 architecture docs (this set).  
- Accept ADR-MS005-001 Strategy Authority Boundaries.  
- Confirm dependency law: Runtime A → Twin → Adaptive → Strategy → Experience.  
- Confirm no implementation artefacts introduced by this directive.

### Exit criteria

- Architecture review **PASS**.  
- Acceptance criteria in parent §11 satisfied.

### Rollback

N/A (docs only).

---

## S0 — Contracts, fixtures, ADRs

### Scope

- Inert logical contracts / DTOs / port interfaces behind `ENABLE_STRATEGY_ENGINE` (default OFF).  
- Golden learners: empty plan, sparse evidence, mid-plan learning, revision stage, abandoned mission, high fatigue fixture, confidence divergence fixture.  
- Draft ADR-MS005-002 (trace retention) / ADR-MS005-003 (Experience sole-director policy) as needed.  
- **No** orchestration execution; **no** Experience cutover.

### Status

**Implemented** (Engineering Directive 002) — `app/infrastructure/adapters/strategy_engine/` (`LearningStrategyContract`, `LearningIntervention`, `InterventionStep`, `StrategyContext`, `StrategyAdapter`, DI, flag default OFF, contract tests).

### Exit criteria

- Contract serialization / immutability tests.  
- Dependency boundary tests (Strategy must not import Experience internals; must not write Runtime A).  
- Flag defaults OFF.

### Rollback

Disable Strategy Engine flag / leave unused.

---

## S1 — Strategy Input Assembler / Core Strategy Engine

### Scope

- Read-only assembler producing `StrategyContext` from Runtime A + Twin consume + Adaptive consume.
- Deterministic `StrategyEngine` coordinating Study / Session / Revision / Recovery / Fatigue / Confidence / Intervention planners into one `LearningIntervention`.
- Field provenance + unavailable honesty.
- **No** Experience cutover; **no** explainability gate.

### Status

**Implemented** (Engineering Directive 003) — `StrategyContextAssembler`, planners, `StrategyEngine`, validation, DI, unit / integration / determinism tests. Flag default OFF.

### Exit criteria

- Identical Runtime A + Twin + Adaptive inputs + `as_of` → identical intervention serialize.
- All planners contribute to one intervention; Adaptive topic order preserved (no re-rank).
- Missing Twin/Adaptive → explicit unavailable; never estimate.
- No write APIs in assembler / engine call graph.

### Rollback

Disable Engine flag.

---

## S2 — Strategy Executor + intervention builders

### Scope

- Deterministic `StrategyExecutor` → `StrategyDecisionRecord` + `InterventionPlan`.  
- Builders: Session, Revision, Recovery, Fatigue, Confidence, Study (as designed).  
- Populate StrategyExplanationBundle.  
- Shadow-friendly; **no** Authority cutover.

### Exit criteria

- Composition rules respected (fatigue/recovery precedence; mission alignment).  
- Adaptive primary preserved (no re-rank).  
- Deterministic decision ids.  
- Flag defaults OFF.

### Rollback

Disable Engine / Shadow flags.

---

## S3 — Strategy Explainability Gate

### Scope

- Enforce five mandatory explanation questions.  
- Emit `STRATEGY_GATE_*` telemetry.  
- Failed interventions remain shadow-only / ineligible.

### Exit criteria

- Complete bundles PASS; incomplete FAIL with `STRATEGY_EXPLAINABILITY_INCOMPLETE`.  
- No Runtime A / Twin / Adaptive / UI mutation.

### Rollback

Gate stays observational; Authority remains OFF.

---

## S4 — Shadow execution

### Scope

- `ENABLE_STRATEGY_SHADOW`: assemble → execute → gate → discard for UX.  
- Shadow telemetry; optional compare vs prior Experience baseline.  
- **No** Authority.

### Exit criteria

- Shadow never changes Home / Start / Recommendation UX.  
- Determinism replay on frozen input bundles.  
- Flags default OFF.

### Rollback

Disable Shadow / Engine.

---

## S5 — Observational Strategy traceability

### Scope

- `StrategyTrace` + lineage reconstruction; correlation ids (prefer Adaptive correlation continuity).  
- Trace telemetry only; no educational SoT writes.

### Exit criteria

- ST-1…ST-6 checks (`STRATEGY_TRACEABILITY.md`).  
- Reconstruct identical lineage serialize on repeat.

### Rollback

Disable Engine / Shadow; traces observational only.

---

## S6 — Shadow soak + monitors

### Scope

- Production-like observational soak: latency, determinism, gate pass rate, topic-identity agreement vs Adaptive/Recommendation, drift signals, rollback verifier.  
- Ops dashboard hook (design parallel to Adaptive soak).  
- **No** Authority by default.

### Exit criteria

- Soak health criteria documented and met for Internal Alpha.  
- Rollback verifier: Authority/Engine OFF restores prior Experience path.  
- Readiness report (future) before S7.

### Rollback

Disable Shadow / Engine.

---

## S7 — Experience cutover (Authority)

### Scope

- `ENABLE_STRATEGY_AUTHORITY` routes `StrategyInterventionPort` on Gate PASS.  
- Automatic fallback on FAIL / exception.  
- Demo intervention theatre forbidden under Authority.  
- Planning/Mission Start authority unchanged.

### Exit criteria

- Golden users: session primary topic mission-aligned; Adaptive advisory preserved when differing.  
- Explanation five questions present on served interventions.  
- Authority default OFF until explicit go-live decision.  
- No schema changes; no UI redesign required (consume existing surfaces).

### Rollback

Disable Authority (or Engine/Shadow) → prior Experience path immediately.

---

## Learning Strategy Engine Ready

Declare Ready only when:

1. Architecture review PASS (this directive).  
2. S0–S6 complete with soak evidence.  
3. S7 implemented but Authority OFF by default (or ON only under documented Alpha protocol).  
4. Acceptance criteria hold: distinct responsibilities; Runtime A authoritative; Twin interpretive; Adaptive recommendation-only; Strategy orchestration-only.  
5. No educational writes from Strategy path.  
6. Curriculum V1/V2 traversal unaffected.

---

## Explicit non-phases (out of scope for MS-005 Ready)

| Item | Why deferred |
|---|---|
| Alembic StrategyTrace store | Optional ADR-MS005-002 |
| Strategy as sole next-action authority replacing Adaptive port | Requires ADR-MS005-003 + product decision |
| Content generation / tutoring scripts | Product boundary |
| Replacing Planning mission generation | MS-001 dual-next policy |
| AI/LLM intervention selection | Forbidden in educational core |

---

## Suggested flag rollout order

```
1. ENABLE_STRATEGY_ENGINE = ON          # DI / contracts
2. ENABLE_STRATEGY_SHADOW = ON          # observe
3. Soak + readiness review
4. ENABLE_STRATEGY_AUTHORITY = ON       # Alpha cohort only
5. Expand cohort / keep kill switch
```

Never enable step 4 without steps 1–3 evidence.
