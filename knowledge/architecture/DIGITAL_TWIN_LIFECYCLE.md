# MS-004 — Digital Twin Lifecycle

**Milestone:** MS-004 — Student Digital Twin  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`  
**Companions:** `DIGITAL_TWIN_DATA_MODEL.md`, `DIGITAL_TWIN_INTERFACE_SPECIFICATION.md`

---

## 1. Purpose

Define how a Student Digital Twin is **created, updated, freshened, frozen, and recomputed** — and which Runtime A events trigger Twin synthesis — without Twin writing educational state.

---

## 2. Lifecycle states

```
Absent
  ↓ initialise (PlanActivated / first Twin read under flags)
Initialised
  ↓ first evidence-backed update
Active
  ⇄ Stale (freshness window exceeded)
  ↓ freeze (audit / Adaptive as_of)
Frozen (immutable historical snapshot)
  ↓ recompute from Runtime A
Active (new snapshot; Frozen retained if policy requires)
```

| State | Meaning | Student-visible? |
|---|---|---|
| **Absent** | No Twin synthesis yet; flags off or never assembled | Prior Experience path / empty |
| **Initialised** | Identity + Goals projected; structural domains empty | Honest empty insights allowed |
| **Active** | Snapshot within freshness window | Twin Authority may serve |
| **Stale** | Newer Runtime A evidence exists beyond window | Serve only with `stale` limitations, or recompute first |
| **Frozen** | Point-in-time immutable snapshot | Audit / Adaptive replay only (not live Home unless explicitly requested `as_of`) |

---

## 3. Lifecycle operations

| Operation | Input | Output | Writes Runtime A? |
|---|---|---|---|
| `initialise` | student_id, as_of | Initialised snapshot | No |
| `update` | prior snapshot + evidence delta / full re-read | New Active snapshot | No |
| `mark_stale` | freshness check | Stale flag on projection | No |
| `recompute` | student_id, as_of, twin_version | New Active snapshot from Runtime A | No |
| `freeze` | Active/Stale snapshot | Frozen copy (immutable) | No |
| `project` | snapshot | Experience opaque DTO | No |

**Preferred update mode for Twin Ready:** full deterministic recompute from Runtime A at `as_of` (simpler; no incremental store). Incremental delta strategies may appear later behind ADR without changing external contracts.

---

## 4. Update triggers

Twin synthesis reacts to **authoritative Runtime A educational events** (observed after they are committed). Twin never emits these events.

### 4.1 Primary triggers

| Trigger | Runtime A source | Twin effect |
|---|---|---|
| **PlanActivated** | StudyPlan create / activate | Initialise or refresh Identity + Goals |
| **SessionCompleted** | Mission → Completed (Evidence Before Completion); EP-003.4 may also emit observational `plan_completed` feedback (not Twin write authority) | Refresh Behaviour + Performance + Knowledge refs |
| **EvidenceCommitted** | StudyAttempt accepted | Refresh Knowledge evidence refs (+ Memory structure if revision-linked) |
| **ProgressChanged** | TopicProgress gated update | Refresh Knowledge factual slots |
| **LifecycleStageChanged** | LearningLifecycleService | Refresh Identity lifecycle + Memory revision posture |
| **GoalsChanged** | StudyPlan edit (goals/hours/date) | Refresh Goals; ContinuityService rules for progress continuity remain Runtime A |
| **RecommendationResponse** (optional) | Accept/dismiss if captured (EP-003.4 Learning Feedback preference-journal events; flag-gated) | Behaviour preference refs only — never mastery |

### 4.2 Secondary / explicit triggers

| Trigger | Meaning |
|---|---|
| **TwinReadRequested** | Experience TwinPort read under Shadow/Authority — assemble if missing/stale |
| **AdaptiveAsOfRequested** | Adaptive Assembler needs Twin attachment at `as_of` — freeze/recompute for that clock |
| **ManualRecompute** | Ops / test / Alpha tooling — observational |
| **TwinVersionBump** | Rule/schema version change — force recompute |

### 4.3 Non-triggers (forbidden)

| Non-trigger | Why |
|---|---|
| Adaptive decision emitted | Advice must not mutate learner profile as if evidence |
| UI page view alone (without Shadow/Authority assemble policy) | Avoid write-amplified “views update Twin” confusion — reads may assemble ephemeral projections only |
| Demo seed generation | Forbidden under Twin flags |
| Twin estimate thresholds | Estimates do not write TopicProgress |

---

## 5. Freshness policy

| Parameter | Design default (architecture) |
|---|---|
| Freshness window | Snapshot `as_of` must be ≥ latest material evidence timestamp considered, or within a small skew budget documented in implementation |
| Stale if | New SessionCompleted / EvidenceCommitted / ProgressChanged occurred after snapshot `as_of` |
| On stale read (Authority ON) | Recompute synchronously **or** return prior with `limitations.codes += stale_snapshot` and reduced confidence — product chooses per surface; Alpha preference = recompute for Home readiness |
| Shadow | May tolerate stale for observational cost; telemetry must mark stale |

---

## 6. Sequencing with Runtime A and Bridges

```
Student completes session
  → Runtime A: Evidence Before Completion (MS-001)
  → Runtime A: Mission Completed + Attempt + Progress
  → Journey/History may project new events (MS-002)
  → Twin: update/recompute (MS-004) — after evidence commit
  → Adaptive: later decide using Runtime A (+ optional Twin) (MS-003)
```

**Ordering invariant:** Twin update **after** Evidence Before Completion succeeds. Twin must not race ahead of Evidence Authority.

---

## 7. Continuity across plan changes

| Concern | Owner | Twin behaviour |
|---|---|---|
| TopicProgress continuity | EducationalContinuityService (Runtime A) | Twin recomputes from surviving Runtime A state; does not invent wiped history |
| Goals change | StudyPlan | Twin GoalsFacet refreshes; Knowledge refs remain evidence-backed |
| Curriculum V1/V2 switch | Curriculum binding on plan | Twin IdentityFacet updates; topic slots remapped via CurriculumService — never private taxonomy |

---

## 8. Failure and empty authentic behaviour

| Condition | Twin lifecycle response |
|---|---|
| No active StudyPlan | Initialised-empty or Absent; `NO_ACTIVE_PLAN`; no demo |
| Sparse evidence | Active with empty Knowledge/Behaviour payloads; `sparse_evidence` limitation |
| Runtime A unavailable | `UNAVAILABLE`; do not serve demo; Experience fallback per flag policy |
| Explainability incomplete | Do not ship claim as Twin Authority insight |
| Partial facet failure | Facet `unavailable`; other facets may remain if provenance honest |

---

## 9. Telemetry (observational design)

| Event | When |
|---|---|
| `TWIN_ASSEMBLE_REQUESTED` | Assemble/recompute starts |
| `TWIN_ASSEMBLE_SUCCESS` | Snapshot produced |
| `TWIN_ASSEMBLE_FAILURE` | Assemble failed |
| `TWIN_ASSEMBLE_LATENCY` | Observational latency |
| `TWIN_MARKED_STALE` | Freshness check failed |
| `TWIN_SHADOW_*` | Shadow pipeline (parallel to Adaptive shadow naming) |
| `TWIN_AUTHORITY_*` | Experience cutover serve / fallback |

Telemetry must not include secrets or full evidence payloads.

---

## 10. Lifecycle vs Adaptive / Experience flags

| Flags | Lifecycle behaviour |
|---|---|
| All Twin flags OFF | Absent for synthesis; Experience prior path |
| Engine Twin ON, Shadow ON | Assemble Active snapshots; discard for UX |
| Authority ON | Project Active (or recomputed) via StudentTwinPort |
| Adaptive Twin-input ON | Freeze/recompute at Adaptive `as_of` for attachment |

Twin lifecycle never enables Adaptive Authority or Runtime A writes.
