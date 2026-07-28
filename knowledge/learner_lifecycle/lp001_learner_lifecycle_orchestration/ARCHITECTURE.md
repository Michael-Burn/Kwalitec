# LP-001 — Learner Lifecycle Orchestration Architecture

**Programme:** LP-001 — Learner Lifecycle Orchestration  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/application/learner_lifecycle/` · `app/models/learner_lifecycle.py`  
**Depends on:** EI-004 · EI-005 · EI-006 · EI-007 · EX-001 · RI-001

---

## 1. Capability statement

> Kwalitec automatically maintains each learner's educational state throughout their learning journey.

A student entering or using Kwalitec is enrolled into the Educational Intelligence pipeline and kept current as Learning Evidence arrives — without manual twin/decision rebuilds and without new educational reasoning in the orchestrator.

---

## 2. Lifecycle flow

```
                    ┌─────────────────────────────────────┐
                    │   LearnerLifecycleOrchestrator      │
                    │   (coordination only — no reasoning)│
                    └─────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
   Onboard student            Process evidence              Recover / ensure
          │                           │                           │
          ▼                           ▼                           ▼
 EI-004 Bind SCI              EI-005 Record evidence      Initialise nodes
 EI-004 Init node state               │                   (idempotent)
          │                           ▼                           │
          ├──────────► EI-006 Twin belief rebuild ◄───────────────┤
          │                           │                           │
          ├──────────► EI-007 Decision rebuild    ◄───────────────┤
          │                           │                           │
          └──────────► EX-001 Experience portfolio◄───────────────┘
                                      │
                                      ▼
                     RI-001 Runtime Integration (read path)
                     Preferred Authority → student surfaces
```

Experience Models are regenerable presentation artefacts (not persisted). Runtime Integration remains the sole Preferred Authority **read** path for Dashboard / Mission / Coach / Revision / Session.

---

## 3. Orchestration responsibilities

| In scope | Out of scope |
|----------|--------------|
| Invoke EI-004 binding + node init | Educational decision ranking / rules |
| Invoke EI-005 evidence recording | Twin inference formulas |
| Invoke EI-006 belief rebuild | Experience presentation catalogues |
| Invoke EI-007 decision rebuild | Student UI / blueprint logic |
| Invoke EX-001 portfolio generation | Bypassing RI-001 for surface delivery |
| Technical retry + checkpointed recovery | Modifying CKG / curriculum engines |

The orchestrator passes clocks (`as_of`) for determinism and sets `ensure_beliefs=False` on decision rebuild so the twin stage remains an explicit coordinated step.

---

## 4. Event sequence

### 4.1 Onboarding

1. `bind_instance` — `StudentCurriculumBindingService.create_instance`
2. `initialise_node_state` — `initialise_node_states` (idempotent)
3. `twin_beliefs` — `BeliefInferenceService.rebuild_beliefs`
4. `educational_decisions` — `DecisionReasoningService.rebuild_decisions`
5. `experience_models` — `ExperienceTransformationService.portfolio_for_instance`

### 4.2 Evidence pipeline

1. `record_evidence` — `EvidenceRecordingService.record_evidence` (append-only)
2. `twin_beliefs` — full rebuild from evidence history
3. `educational_decisions` — full rebuild from beliefs + curriculum + SCI
4. `experience_models` — regenerate from persisted decisions

`refresh_after_evidence` skips step 1 when evidence was already appended by another caller.

### 4.3 Ensure / recover

- `ensure_complete` inspects SCI completeness and re-runs missing derived stages.
- `recover` always re-initialises node states (idempotent) then refreshes twin → decisions → experience so partial failures cannot leave beliefs and decisions misaligned.

---

## 5. Recovery strategy

| Mechanism | Behaviour |
|-----------|-----------|
| **Technical retry** | Per-stage retries (`LifecycleRetryPolicy`, default 3) for transient failures |
| **Checkpoints** | `llp_lifecycle_operations` records operation type, completed stages, failed stage, cause |
| **Idempotent EI stages** | Binding same edition returns existing SCI; twin/decision rebuilds replace derived rows; experience is ephemeral |
| **Aligned refresh** | Recovery never re-runs only decisions after a twin success without also ensuring twin currency — derived refresh is atomic as a logical unit |
| **Immutable evidence** | Failed refresh never deletes recorded evidence; recovery rebuilds derived state from history |

Partial failure after SCI bind leaves a recoverable incomplete state (e.g. beliefs without decisions). Callers invoke `recover(instance_id)` or `ensure_complete(instance_id)` to restore completeness. Runtime Integration falls back to Temporary Runtime A until decisions exist — it is never bypassed with invented recommendations.

---

## 6. Dependency graph

```
Published CKG Edition (EI-001/002/003)
        │
        ▼
Student Curriculum Instance + Node State (EI-004)
        │
        ▼
Learning Evidence events (EI-005)  ←── process_evidence
        │
        ▼
Twin Beliefs (EI-006)
        │
        ▼
Educational Decisions (EI-007)
        │
        ▼
Experience Models (EX-001) ──► Runtime Integration (RI-001) ──► Surfaces
        ▲
        │
LearnerLifecycleOrchestrator (LP-001)  [write-path coordination]
LlpLifecycleOperation checkpoints      [operational only]
```

---

## 7. Public API

| Method | Purpose |
|--------|---------|
| `onboard_student(student_id, edition_id, …)` | Full onboarding pipeline |
| `process_evidence(instance_id, node, type, source, …)` | Record + refresh |
| `refresh_after_evidence(instance_id, …)` | Refresh only |
| `ensure_complete(instance_id, …)` | Heal incomplete EI state |
| `recover(instance_id, …)` | Resume after failed checkpoint |
| `inspect_consistency(instance_id)` | Completeness report |

Version: `llp.v1`.

---

## 8. Invariants

1. Orchestrator contains **no** educational reasoning.
2. Stage order is fixed and deterministic for equal inputs + `as_of`.
3. Repeated onboarding for the same student+edition is idempotent.
4. Evidence appends remain immutable; derived state is fully rebuildable.
5. Student-facing delivery continues through RI-001 Preferred Authority — LP-001 does not introduce a parallel recommendation path.
