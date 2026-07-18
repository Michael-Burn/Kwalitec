# Learning Session Runtime

**Document ID:** V2-005-RUNTIME  
**Milestone:** V2-005 — Learning Session Runtime  
**Status:** Authoritative application-layer specification  
**Nature:** Framework-independent educational session execution  

**Domain foundation:** [`LEARNING_JOURNEY_DOMAIN.md`](LEARNING_JOURNEY_DOMAIN.md) · [`STATE_MACHINE.md`](STATE_MACHINE.md)  
**Journey orchestration:** [`LEARNING_JOURNEY_ENGINE.md`](LEARNING_JOURNEY_ENGINE.md)  
**Curriculum structure:** [`CURRICULUM_GRAPH.md`](CURRICULUM_GRAPH.md)  
**Package:** `app/application/learning_session/`

---

## 1. Purpose

The Learning Session Runtime is the **execution layer** for a student's interaction with an individual Learning Session.

It bridges:

```
Curriculum Graph
      ↓
Learning Journey Engine
      ↓
Student Learning Session
      ↓
Evidence
      ↓
Reflection
      ↓
Recommendation (consumers)
```

The runtime owns session-local lifecycle, evidence attribution, reflection capture, session completion evaluation, and deterministic next-action scheduling.

It does **not** own Journey / Topic Complete, Twin belief writes, persistence, UI, or study content generation.

---

## 2. Responsibilities

| Component | Responsibility |
|-----------|----------------|
| `LearningSessionRuntime` | Public facade — create/start/resume/pause/complete, snapshot, evidence, reflection, completion, next action |
| `LearningSessionPlanner` | Deterministic `LearningSessionPlan` from journey / topic / objectives / effort / prior evidence |
| `LifecycleManager` | Lawful runtime phase transitions |
| `EvidenceCollector` | Session-scoped JourneyEvidence attribution (Learning Evidence Model) |
| `ReflectionManager` | Pending / captured / deferred structured reflection |
| `CompletionEvaluator` | Whether the **session** is educationally complete |
| `ActivityScheduler` | Deterministic next actions (break / reflect / continue / revise / next session) |
| Policies | Stateless planning, reflection, completion, scheduling rules |
| DTOs | Immutable plans / snapshots / summaries / results |

### Explicit non-responsibilities

- No Flask routes or request/session access
- No SQLAlchemy / ORM / migrations / persistence writes
- No UI rendering
- No AI / randomness / study content generation
- No Twin belief mutations
- No Journey / Topic Complete confirmation (Learning Journey Engine only)
- No Version 1 Study Progress mutation

---

## 3. Package structure

```
app/application/learning_session/
    __init__.py
    runtime.py
    planner.py
    lifecycle_manager.py
    evidence_collector.py
    reflection_manager.py
    completion_evaluator.py
    activity_scheduler.py
    runtime_phase.py
    exceptions.py
    dto/
        learning_session_plan.py
        runtime_snapshot.py
        evidence_summary.py
        reflection_summary.py
        completion_result.py
    policies/
        planning_policy.py
        reflection_policy.py
        completion_policy.py
        scheduling_policy.py
```

---

## 4. Lifecycle and state machine

### 4.1 Runtime phases

```
PLANNED
   ↓ prepare
READY
   ↓ start
ACTIVE
   ↓ pause
PAUSED
   ↓ resume
ACTIVE
   ↓ complete
COMPLETED
   ↓ archive
ARCHIVED
```

`start` is also lawful directly from `PLANNED` (prepare is optional).  
`complete` is lawful from `ACTIVE` or `PAUSED`.

### 4.2 Mapping to domain SessionState

| RuntimePhase | Domain SessionState |
|--------------|---------------------|
| PLANNED | `NOT_STARTED` |
| READY | `NOT_STARTED` (prepared flag) |
| ACTIVE | `ACTIVE` |
| PAUSED | `PAUSED` |
| COMPLETED | `COMPLETED` |
| ARCHIVED | `COMPLETED` (archived flag) |

Domain terminals `ABANDONED` / `SKIPPED` remain domain vocabulary; the runtime surfaces them as closed (`ARCHIVED`-equivalent) and does not invent parallel educational meanings.

### 4.3 SessionHandle

Because `READY` and `ARCHIVED` are runtime overlays on domain state, callers receive an immutable `SessionHandle`:

- `session` — domain `LearningSession`
- `phase` — `RuntimePhase`
- `plan` — optional `LearningSessionPlan`

The runtime never persists handles. Callers (future adapters) remain responsible for storage.

---

## 5. Relationship to the Learning Journey Engine

| Concern | Authority |
|---------|-----------|
| Journey lifecycle / Topic Complete | Learning Journey Engine |
| Session selection within a journey | Journey Engine `SessionSelector` |
| Session execution (start/pause/finish/reflect/evidence) | **Learning Session Runtime** |
| Progress recalculation after session close | Journey Engine (consumer of completed session) |

Typical integration sequence:

1. Journey Engine selects / plans the next session structurally.
2. Session Runtime creates and executes the session.
3. Caller returns the completed session (+ reflection / evidence) to the Journey Engine (`apply_session_completed` / `apply_reflection_captured`).

The Session Runtime **never** calls Journey completion APIs and always sets `CompletionResult.journey_complete = False`.

---

## 6. Relationship to the Curriculum Graph

The Curriculum Graph is the structural sequencing source for topics, prerequisites, and learning paths.

The Session Runtime:

- accepts `topic_id` and objective identities as **inputs**
- does not traverse the graph
- does not invent curriculum ordering
- does not generate syllabus content

Future Mission / Recommendation adapters may use Curriculum Graph readiness to decide *which* topic/objective to hand to the Session Runtime; the runtime itself remains graph-agnostic.

---

## 7. Relationship to Mission Engine 2.0

Mission Engine 2.0 (roadmap V2-004 product milestone) produces `JourneyRecommendation` artefacts that continue active journeys.

When a recommendation is accepted and realised as session work:

1. Mission / Journey layers resolve the recommendation to topic + objective + effort.
2. Session Runtime executes the session.
3. Evidence and reflection from the session feed subsequent recommendation inputs.

Accepting a recommendation never completes a topic. Finishing a session never completes a journey.

---

## 8. Evidence

`EvidenceCollector` attributes observations as `JourneyEvidence` using Learning Evidence Model catalogue types (`EvidenceType`) and qualitative confidence only.

Rules:

- Collect only while phase is `ACTIVE`, `PAUSED`, or `COMPLETED` (not archived)
- Append-only on the session
- Never estimate mastery
- May wrap an existing `LearningEvidence` record for attribution

---

## 9. Reflection

Structured student reflection supports:

| Runtime field | Domain mapping |
|---------------|----------------|
| summary | `what_was_learned` |
| challenges | `uncertainty` |
| questions_remaining | `questions_remaining` |
| confidence | `confidence` |
| next_intention | encoded into questions; surfaced in `ReflectionSummary` |

On `complete_session`, a `PENDING` reflection is attached by default. Capture is required for session educational closure under `ReflectionPolicy` / `CompletionPolicy`. Explicit deferral (`DEFERRED_CAPTURE`) is allowed but does not satisfy final closure.

---

## 10. Session completion vs journey completion

`CompletionEvaluator` answers only: “Is **this Learning Session** educationally closed?”

Required by default:

- Domain state `COMPLETED`
- Reflection satisfied (`CAPTURED` or `NOT_REQUIRED`)

Optional (policy flag, default off):

- At least one evidence item

Hard invariant: `journey_complete` is always `False` in runtime results.

---

## 11. Activity scheduling

`ActivityScheduler` / `SchedulingPolicy` produce deterministic `NextAction` tags:

| Action | Typical trigger |
|--------|-----------------|
| `prepare` | PLANNED |
| `start` | READY |
| `continue` | ACTIVE / PAUSED |
| `break` | ACTIVE with long duration / high effort |
| `reflect` | COMPLETED with reflection owed |
| `revise` | COMPLETED + closed reflection + thin evidence |
| `next_session` | COMPLETED + educationally complete |
| `archive` / `none` | closed / archived postures |

No AI. No content generation. Tags are structural advice only.

---

## 12. Determinism

Same inputs → same plan, phase transitions, evidence attribution shape, reflection validation, completion result, and next action.

Injectable `clock` and `id_factory` keep unit tests reproducible without wall-clock coupling.

---

## 13. Consumer contract

Future HTTP adapters, Mission Engine 2.0, Twin 2.0, Revision, and Analytics **must**:

- call `LearningSessionRuntime` for session execution
- not re-implement session lifecycle rules in controllers
- treat session complete as progress input to the Journey Engine — never as Topic Complete
- preserve explainability tags from plans and snapshots

---

## 14. Closing

If an implementation allows `finish_session` to set JourneyState `COMPLETED`, or writes Estimated Mastery from session completion alone, it violates Version 2 architecture regardless of UI convenience.
