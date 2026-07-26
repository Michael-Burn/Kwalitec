# MS-004 — Migration Plan (Student Digital Twin)

**Milestone:** MS-004 — Student Digital Twin  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`  
**Risks:** `RISK_ANALYSIS_MS004.md`  
**Depends on:** MS-001 Runtime Bridge (Mission / Evidence / Recommendation); MS-002 Journey/History (recommended for narrative consistency); MS-003 Adaptive contracts (optional for T6)

---

## Principles

1. **Incremental** — each phase independently releasable.  
2. **Reversible** — feature-flag rollback per phase.  
3. **No big-bang** — never flip Twin Authority + Adaptive Authority + Sole Runtime together.  
4. **No schema changes** for Twin Ready.  
5. **No UI redesign.**  
6. **No educational writes** inside Twin.  
7. **No Runtime A / Adaptive Engine redesign** in Twin phases.  
8. **Shadow before serve** — assemble before Experience cutover.  
9. **Empty authentic / bridged fallback over demo** when Twin flags are on.  
10. **Runtime A wins** fact conflicts.

---

## Phase overview

| Phase | Name | Releasable? | Educational write? | Changes Adaptive algorithms? |
|---|---|---|---|---|
| T0 | Contracts, fixtures, ADRs | Yes (docs/tests) | No | No |
| T1 | Twin Assembler + golden snapshots | Yes | No | No |
| T2 | Lifecycle triggers + freshness | Yes | No | No |
| T3 | Twin Explainability Gate | Yes | No | No |
| T4 | StudentTwinPort cutover (flagged) | Yes | No | No |
| T5 | Observational Twin traceability | Yes | No | No |
| T6 | Optional Adaptive Twin-input attach | Yes | No | No (consume only) |
| T7 | Shadow soak + Internal Alpha — Twin Ready | Yes (ops) | No | No |
| — | **Student Digital Twin Ready** | — | DT-1…DT-n | — |

---

## T0 — Contracts, fixtures, ADRs

### Scope

- Accept MS-004 architecture docs.  
- Accept ADR-MS004-001; draft ADR-MS004-002 / 003.  
- Capture golden learners: empty plan, new learner sparse evidence, mid-plan learning, revision stage, plan-edit continuity.  
- Document expected Twin facets vs Runtime A TopicProgress / Readiness / Mission lists.  
- Inert logical contracts only when implementation starts — **this directive stops at docs**.

### Exit criteria

- ADRs accepted for authority boundary.  
- Fixture table agreed.  
- Architecture review PASS.

### Rollback

N/A (docs only).

---

## T1 — Twin Assembler + golden snapshots

### Scope

- Read-only assembler producing `LearnerProfileSnapshot` behind `ENABLE_DIGITAL_TWIN`.  
- Field provenance + pass-through Knowledge / Readiness.  
- Structural Behaviour / Memory refs.  
- **No** Experience cutover; **no** estimate scoring without ADR-MS004-004.

### Exit criteria

- Snapshots match Runtime A for golden users (TopicProgress, missions, readiness pass-through).  
- No write APIs in assembler call graph.  
- Missing inputs → explicit unavailable; DTO determinism preserved; flag defaults OFF.

### Rollback

Disable Twin flag / leave unused.

---

## T2 — Lifecycle triggers + freshness

### Scope

- Implement trigger taxonomy (post Evidence Before Completion).  
- Freshness / stale marking / recompute policy.  
- Shadow-friendly assemble on read when Shadow ON.

### Exit criteria

- Completing a session then assembling includes new attempt refs or explicit stale limitation.  
- Twin never runs before evidence commit in completion path tests.  
- Flags default OFF.

### Rollback

Disable Shadow / Twin flags.

---

## T3 — Twin Explainability Gate

### Scope

- Enforce TwinExplanationBundle completeness on student-visible claims.  
- Emit `TWIN_GATE_*` telemetry.  
- Failed claims remain shadow-only.

### Exit criteria

- Complete bundles PASS; incomplete FAIL with `TWIN_EXPLAINABILITY_INCOMPLETE`.  
- No Runtime A / UI mutation.

### Rollback

Gate stays observational; Authority remains OFF.

---

## T4 — StudentTwinPort cutover (flagged)

### Scope

- `ENABLE_DIGITAL_TWIN_AUTHORITY` routes `StudentTwinPort` to Twin projections.  
- Demo Twin insights disabled when Authority ON.  
- Automatic fallback to prior Experience path on Twin failure.

### Exit criteria

- Golden users: learner/readiness/insights match Runtime-A-grounded fixtures.  
- No seeded demo readiness theatre under Authority.  
- Journey/History session ids remain consistent when Twin cites sessions.  
- Authority default OFF.

### Rollback

Disable Authority (or Twin) flag → prior Experience Twin path immediately.

---

## T5 — Observational Twin traceability

### Scope

- TwinTrace + reconstruction; correlation ids.  
- No student-facing history table; no educational writes.

### Exit criteria

- Evidence → Snapshot → Claim → Projection reconstructable on fixtures.  
- Telemetry `TWIN_TRACE_*` present.

### Rollback

Disable Twin/Shadow; traces observational only.

---

## T6 — Optional Adaptive Twin-input attach

### Scope

- `ENABLE_DIGITAL_TWIN_ADAPTIVE_INPUT` attaches Twin structural fields to Adaptive Assembler.  
- Fail-open when Twin unavailable.  
- Does not change Adaptive decision algorithms or Authority routing.

### Exit criteria

- Adaptive with Twin absent ≡ Adaptive with attach skipped (same Runtime A primary inputs).  
- Twin attach never required for Adaptive Gate PASS.  
- Adaptive still never writes Runtime A / Twin.

### Rollback

Disable Adaptive Twin-input flag.

---

## T7 — Shadow soak + Internal Alpha — Twin Ready

### Scope

- Dual-run: prior Experience Twin path vs Twin Authority (observational compare when safe).  
- Freshness, explainability pass rate, demo eradication checklist.  
- Rollback verification.  
- Ops dashboard hooks (observational).

### Exit criteria

- Soak metrics stable; rollback immediate; Runtime A read-only from Twin proven.  
- Architecture Twin Ready criteria (§ parent §16) met.  
- Await product/architecture sign-off before production Authority.

### Rollback

All Twin flags OFF.

---

## Twin Ready acceptance checklist (DT)

| ID | Criterion |
|---|---|
| DT-1 | Twin consumes Runtime A only; no educational writes |
| DT-2 | Runtime A remains fact SoT; conflicts Runtime A wins |
| DT-3 | Adaptive consumes Twin optionally; does not own Twin |
| DT-4 | Experience TwinPort Authority empty authentic over demo |
| DT-5 | Explainability gate enforced for Authority claims |
| DT-6 | Traceability chain reconstructable |
| DT-7 | Feature flags default OFF; rollback verified |
| DT-8 | No schema / UI / Runtime A / Adaptive algorithm changes for Ready |
| DT-9 | V1 and V2 curricula traversable via CurriculumService |
| DT-10 | Privacy: student-scoped; refs not raw payloads |

---

## Explicitly out of Twin Ready

- Durable Twin ORM / Alembic tables (ADR-MS004-002).  
- Probabilistic mastery / forgetting-curve Authority estimates (ADR-MS004-004).  
- Adaptive Authority ON.  
- Planning regenerated from Twin.  
- UI redesign.  
- Deleting V2 Twin packages.

---

## Stop condition (this directive)

Architecture documentation complete. **Do not begin T0 implementation coding** until architecture review accepts MS-004 Directive 001.
