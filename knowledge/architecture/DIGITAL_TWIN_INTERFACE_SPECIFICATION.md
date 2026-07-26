# MS-004 — Digital Twin Interface Specification

**Milestone:** MS-004 — Student Digital Twin  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`  
**Extends:** Experience `StudentTwinPort`; MS-001 BridgeResult patterns; MS-003 Adaptive input attachment (optional)

---

## 0. Conventions

### Layers

| Layer | Responsibility |
|---|---|
| Experience Port / Facade | `StudentTwinPort`, StudentExperienceService, History insights |
| Twin Projection Adapter | Flags, assemble/project, empty authentic, telemetry |
| Twin Assembler / Lifecycle | Deterministic snapshot synthesis |
| Educational Services | Authoritative Runtime A **read** APIs |
| Adaptive Assembler (optional) | Consume Twin snapshot attachment |
| Database / Curriculum | Existing SQL / Curriculum JSON |

### Shared types (logical)

| Type | Meaning |
|---|---|
| `StudentId` | Authenticated user id |
| `TwinSnapshotId` | Stable snapshot identity / fingerprint |
| `LearnerProfileSnapshot` | See `DIGITAL_TWIN_DATA_MODEL.md` |
| `OpaqueDict` | Projection document safe for Experience |
| `BridgeResult[T]` | `{ ok, value?, error_code?, message?, fallback_used }` |
| `TwinExplanationBundle` | See `DIGITAL_TWIN_EXPLAINABILITY.md` |
| `TwinTraceRef` | See `DIGITAL_TWIN_TRACEABILITY.md` |

### Shared failure codes

| Code | Meaning |
|---|---|
| `UNAVAILABLE` | Downstream service or DB unreachable |
| `NO_ACTIVE_PLAN` | No active StudyPlan |
| `NOT_FOUND` | No Twin context / empty authentic |
| `FORBIDDEN` | Ownership failure |
| `INVALID_STATE` | Malformed as_of / illegal request |
| `STALE_SNAPSHOT` | Snapshot behind newer evidence (may be soft) |
| `TWIN_EXPLAINABILITY_INCOMPLETE` | Claim computed but explanation incomplete — must not ship as Twin Authority insight |
| `BEHAVIOUR_MISMATCH` | Parity / golden check (tests only) |

### Shared read-only rule

Twin Adapter / Assembler **must not**:

- Call Planning ensure/generate  
- Start / resume / complete sessions  
- Write TopicProgress or StudyAttempt  
- Accept evidence  
- Mutate StudyPlan  
- Emit demo seeds when Twin flags are on  
- Own or mutate Adaptive decisions  
- Change RecommendationService / Adaptive Engine algorithm bodies  

---

## 1. `DigitalTwinBridge` (adapter — logical)

**Purpose:** Experience `StudentTwinPort` backed by Runtime-A-grounded Twin synthesis.  
**Ownership:** Infrastructure adapter (future package; not created in this directive).  
**Educational owners (read):** MissionService, StudyAttempt / Evidence reads, TopicProgress, ReadinessService, CurriculumService, StudyPlanService, LearningLifecycleService, Continuity reads.

### 1.1 `assemble_snapshot`

**Inputs**

| Name | Type | Required | Notes |
|---|---|---|---|
| `student_id` | StudentId | Yes | Current user |
| `as_of` | datetime | No | Defaults to server decision clock |
| `mode` | `shadow` \| `authority` \| `adaptive_attach` | Yes | Caller context |

**Outputs**

| Name | Type | Notes |
|---|---|---|
| `BridgeResult[LearnerProfileSnapshot]` | — | Deterministic material fields |

**Failures:** `FORBIDDEN`, `NO_ACTIVE_PLAN`, `UNAVAILABLE`, `INVALID_STATE`.

### 1.2 `project_learner_summary`

**Backs:** `StudentTwinPort.get_learner_summary`.

**Outputs:** `BridgeResult[OpaqueDict]` mapped from Identity + Goals + Knowledge coverage.

**Authority ON empty:** authentic empty / null — never demo.

### 1.3 `project_readiness_summary`

**Backs:** `StudentTwinPort.get_readiness_summary`.

**Rule:** Pass-through ReadinessService via PredictionFacet; Twin must not invent readiness maths.

**Explainability:** Student-visible readiness claims require TwinExplanationBundle PASS.

### 1.4 `project_learning_insights`

**Backs:** `StudentTwinPort.get_learning_insights`.

**Rule:** Insights cite Behaviour / Performance / Knowledge structural facts with TraceRef. No fabricated session cards (History Bridge remains narrative SoT for sessions).

---

## 2. Experience `StudentTwinPort` (existing contract)

Preserved methods:

| Method | Twin Bridge behaviour when Authority ON |
|---|---|
| `component_id` / `component_version` | Twin adapter identity |
| `is_available` | True when Twin DI constructed and healthy |
| `get_learner_summary` | §1.2 |
| `get_readiness_summary` | §1.3 |
| `get_learning_insights` | §1.4 |

**Invariant (unchanged):** Experience must never mutate Twin state or invent readiness scores.

---

## 3. Adaptive Twin input attachment (optional)

**Interface (logical):** `TwinAdaptiveInputAttachment`

| Field | Type | Notes |
|---|---|---|
| `twin_snapshot_ref` | string | Fingerprint |
| `as_of` | datetime | Must match Adaptive decision clock when attached |
| `behaviour` | opaque structural | Optional |
| `memory` | opaque structural | Optional |
| `predictions` | opaque | Prefer readiness pass-through consistency |
| `limitations` | codes | e.g. `twin_unavailable` |

**Rules:**

1. Adaptive Assembler remains able to run with Twin absent.  
2. Twin attachment is never required for Adaptive Gate PASS.  
3. Twin must not replace Runtime A collectors.  
4. Flag: bundled under `ENABLE_DIGITAL_TWIN` (default OFF). There is **no** separate `ENABLE_DIGITAL_TWIN_ADAPTIVE_INPUT` env flag in `v2_flags.py` (EP-001.5 TD-ARCH-06 / EP-002.1).

---

## 4. Explainability gate interface (logical)

**`TwinExplainabilityGate.validate(claim_bundle) → PASS | FAIL`**

- PASS → eligible for Twin Authority surfaces.  
- FAIL → `TWIN_EXPLAINABILITY_INCOMPLETE`; observational only / fallback.  
- Gate never mutates snapshot; never writes Runtime A.

See `DIGITAL_TWIN_EXPLAINABILITY.md`.

---

## 5. Feature-flag composition

Implemented flags are only **Twin** and **Authority**. Shadow Validation and Adaptive TwinInput are **bundled** when Twin is ON (no independent SHADOW / ADAPTIVE_INPUT env switches).

| ENABLE_DIGITAL_TWIN | AUTHORITY | Behaviour |
|---|---|---|
| OFF | * (forced OFF) | No Twin synthesis DI; prior Experience path; `build_*` return `None` |
| ON | OFF | Twin DI present (facets / snapshot / explainability / shadow / TwinInput / Foundation / `build_*`); UX TwinPort remains `ExperienceTwinAdapter` |
| ON | ON | Experience `StudentTwinPort` serves Foundation Authority (fallback ExperienceTwinAdapter) |

**Historical note:** Earlier drafts used a four-column SHADOW / ADAPTIVE_INPUT matrix. That matrix is **documentation debt** relative to code; treat the two-flag table above as authoritative.

**Recommended:** Authority requires Shadow path proven under Twin ON (same discipline as MS-003 A4).

---

## 6. Telemetry contracts

| Event | Payload (minimal) |
|---|---|
| `TWIN_ASSEMBLE_REQUESTED` | student_id hash/scope, mode, as_of |
| `TWIN_ASSEMBLE_SUCCESS` | twin_snapshot_ref, latency_ms |
| `TWIN_ASSEMBLE_FAILURE` | error_code |
| `TWIN_GATE_PASSED` / `FAILED` | claim_id, codes |
| `TWIN_AUTHORITY_SERVED` / `FALLBACK` | port method |
| `TWIN_ADAPTIVE_ATTACHED` / `SKIPPED` | reason |

---

## 7. Compatibility

| Consumer | Compatibility rule |
|---|---|
| Journey / History Bridges | Twin must not invent timeline events; may reference same Mission/Attempt ids |
| Recommendation Bridge | Twin does not calculate recommendations |
| Adaptive Engine | Consume-only attachment; MS-003 contracts unchanged |
| V1 / V2 curricula | CurriculumService traversal only (ADR-003 / ADR-004) |
