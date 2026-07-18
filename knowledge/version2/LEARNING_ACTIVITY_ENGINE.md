# Learning Activity Engine

**Document ID:** V2-008-ACTIVITY  
**Milestone:** V2-008 — Learning Activity Engine  
**Status:** Authoritative application-layer specification  
**Nature:** Framework-independent educational activity execution  

**Session runtime:** [`LEARNING_SESSION_RUNTIME.md`](LEARNING_SESSION_RUNTIME.md)  
**Journey orchestration:** [`LEARNING_JOURNEY_ENGINE.md`](LEARNING_JOURNEY_ENGINE.md)  
**Domain foundation:** [`LEARNING_JOURNEY_DOMAIN.md`](LEARNING_JOURNEY_DOMAIN.md)  
**Package:** `app/application/learning_activity/` · `app/domain/learning_activity/`

---

## 1. Purpose

The Learning Activity Engine owns the **execution structure inside a Learning Session**.

It bridges:

```
Learning Session Runtime
        ↓
Learning Activity Engine
        ↓
Activity Sequence
        ↓
Activity transitions / evidence / reflection hooks
        ↓
ready_for_session_completion  →  Session Runtime
```

It does **not** own:

| Concern | Owner |
|---------|-------|
| Session lifecycle (start / pause / complete session) | Learning Session Runtime |
| Journey progression / Topic Complete | Learning Journey Engine |
| Mission scheduling / dispatch | Mission Engine 2.0 / Mission Adapter |
| Curriculum structure | Curriculum Graph |
| Persistence / Flask / UI | Out of scope |

---

## 2. Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `LearningActivityEngine` | Public facade — create sequence, advance / skip / pause / resume / complete, snapshot, evidence, reflection |
| `ActivityPlanner` | Deterministic `ActivityPlan` from types / tags / items |
| `SequenceBuilder` | Ordered `ActivitySequence` from plan (no AI, no content generation) |
| `ProgressionManager` | Current / completed / remaining / progress percentage |
| `TransitionManager` | Lawful activity state transitions only |
| `CompletionManager` | Activity / sequence completion + `ready_for_session_completion` |
| `EvidenceRouter` | Route evidence ids to activities (no persistence, no scoring) |
| `ReflectionRouter` | Associate reflection ids with activities (not sessions) |
| `ActivityValidator` | Single active, no duplicate ids, sequence integrity, lawful transitions |
| Policies | Stateless sequencing, progression, transition, completion rules |
| DTOs | Immutable plans / sequences / transitions / snapshots / results |

### Explicit non-responsibilities

- No Flask routes or request/session access
- No SQLAlchemy / ORM / migrations / persistence writes
- No UI rendering
- No AI / randomness / study content generation
- No Learning Session completion (signal only)
- No Journey / Topic Complete
- No Mission generation

---

## 3. Package structure

```
app/domain/learning_activity/
    entities/
        learning_activity.py
        activity_progress.py
    value_objects/
        activity_type.py
        activity_state.py

app/application/learning_activity/
    __init__.py
    engine.py
    planner.py
    sequence_builder.py
    progression_manager.py
    transition_manager.py
    validator.py
    completion_manager.py
    evidence_router.py
    reflection_router.py
    exceptions.py
    dto/
        activity_plan.py
        activity_snapshot.py
        activity_result.py
        activity_transition.py
        activity_sequence.py
    policies/
        sequencing_policy.py
        progression_policy.py
        transition_policy.py
        completion_policy.py
```

---

## 4. Domain model

### 4.1 LearningActivity

Bounded educational step inside a session sequence.

| Field | Role |
|-------|------|
| `activity_id` | Stable identity |
| `session_id` | Parent Learning Session |
| `activity_type` | Structural kind (`ActivityType`) |
| `sequence_index` | 0-based order |
| `state` | Lifecycle posture |
| `evidence_ids` | Append-only evidence attribution |
| `reflection_ids` | Append-only reflection attribution |

### 4.2 ActivityType (extensible)

```
INTRODUCTION
CONCEPT_LEARNING
WORKED_EXAMPLE
GUIDED_PRACTICE
INDEPENDENT_PRACTICE
KNOWLEDGE_CHECK
REFLECTION
SUMMARY
SPACED_RECALL
NEXT_INTENTION
REVIEW
CUSTOM
```

**Extensibility rule:** `ActivityType.resolve` maps unknown future tokens to `CUSTOM`. Orchestration dispatches on structural type tags only — adding catalogue members does not require rewriting engine control flow.

### 4.3 ActivityProgress

Summary: totals, completed / skipped / remaining counts, current id/index, progress percentage (terminal ÷ total).

---

## 5. Activity lifecycle

```
NOT_STARTED
    │ start
    ▼
  ACTIVE ◄──── resume ────┐
    │                      │
    │ pause                │
    ▼                      │
  PAUSED ──────────────────┘
    │
    │ complete          skip (from NOT_STARTED | ACTIVE | PAUSED)
    ▼                              │
COMPLETED                          ▼
                                SKIPPED
```

Terminal states: `COMPLETED`, `SKIPPED`.

Invalid transitions raise `TransitionError` / domain `ValueError`. The validator enforces **at most one ACTIVE** activity by default.

---

## 6. Sequence diagrams

### 6.1 Create and advance

```
Caller                  LearningActivityEngine
  │                              │
  │ create_sequence(...)         │
  │─────────────────────────────►│ plan → build → validate
  │◄─────────────────────────────│ ActivityHandle
  │                              │
  │ advance_activity(handle)     │
  │─────────────────────────────►│ start first OR complete+start next
  │◄─────────────────────────────│ updated handle
```

### 6.2 Completion readiness (session signal only)

```
Caller                  Activity Engine              Session Runtime
  │                           │                            │
  │ complete activities…      │                            │
  │──────────────────────────►│                            │
  │ ready_for_session_        │                            │
  │   completion?             │                            │
  │──────────────────────────►│                            │
  │◄──── true / false ────────│                            │
  │                           │                            │
  │ if true: complete_session │                            │
  │───────────────────────────────────────────────────────►│
```

The Activity Engine **never** calls session completion.

### 6.3 Evidence and reflection hooks

```
Caller                  EvidenceRouter / ReflectionRouter
  │                              │
  │ route_evidence(id)           │ → attach to ACTIVE (or named) activity
  │ associate_reflection(id)     │ → prefer REFLECTION type, else ACTIVE
  │                              │
  │  No persistence. No scoring. Not session-scoped.
```

---

## 7. Relationship to Session Runtime

| Layer | Owns |
|-------|------|
| Session Runtime | Session phases (PLANNED→ARCHIVED), session evidence/reflection artefacts, session completion evaluation, next-action scheduling |
| Activity Engine | Ordered activities *inside* an active session, activity transitions, activity-scoped evidence/reflection ids, sequence readiness signal |

Typical composition (caller-owned; not wired in this milestone):

```
SessionHandle (runtime)
    └── ActivityHandle (activity engine)  # optional in-memory companion
```

`LearningSessionPlan.recommended_activities` tags may be mapped via `SequencingPolicy.type_from_tag` into an `ActivityPlan`. The Activity Engine does not import or mutate Session Runtime modules.

---

## 8. Completion policy

| Check | Meaning |
|-------|---------|
| `activity_complete` | Named activity is `COMPLETED` |
| `sequence_complete` | All activities are terminal |
| `ready_for_session_completion` | Sequence complete **and** at least one `COMPLETED` (all-skipped ≠ ready) |

**Hard rule:** never complete a Learning Session, Journey, or Mission from this engine.

---

## 9. DTOs (immutable)

| DTO | Role |
|-----|------|
| `ActivityPlan` / `ActivityPlanItem` | Planner output |
| `ActivitySequence` | Ordered materialised activities |
| `ActivityTransition` | Lawful transition record |
| `ActivitySnapshot` | Consumer-facing posture |
| `ActivityResult` | Completion / readiness evaluation |

---

## 10. Future extensibility

1. **New activity types** — add `ActivityType` members; unknown strings already resolve to `CUSTOM`.
2. **Custom sequencing** — supply `items=` or `activity_types=` to the planner; priority sort remains optional.
3. **Policy injection** — engine collaborators are constructor-injectable (`planner`, `transitions`, `completion`, …).
4. **Session integration** — a future milestone may attach `ActivityHandle` to `SessionHandle` without changing Activity Engine contracts.
5. **Persistence** — callers own save/load; `rehydrate(sequence)` rebuilds handles.

---

## 11. Invariants

1. Deterministic sequencing from the same plan inputs.
2. At most one ACTIVE activity (default validation).
3. No duplicate activity identities; contiguous 0-based indices.
4. No invalid state transitions.
5. Evidence / reflection attribution is activity-scoped.
6. Framework-independent (no Flask / SQLAlchemy).
7. Session Runtime, Journey Engine, Mission Engine, Mission Adapter, and Curriculum Graph remain unmodified by this milestone.
