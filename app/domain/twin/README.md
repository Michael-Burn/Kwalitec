# Student Digital Twin Domain

Pure domain vocabulary for the **Student Digital Twin** in Kwalitec, plus the
**Twin Update Pipeline** orchestration framework and concrete update strategies
for **Knowledge**, **Memory**, **Behaviour**, and **Performance** structural
evolution.

**Readiness** is a separate read-side package (`app/domain/readiness/`), not a
Twin write domain and not an Update Strategy. Live readiness is derived on
read from Twin + CurriculumContext + Goals; it is not a required field on
`DigitalTwin`.

**Decision Engine** is a separate read-side package (`app/domain/decision/`),
not a Twin write domain and not an Update Strategy. It selects the next
learning action from Twin + ReadinessState + CurriculumContext + Goals +
Constraints; live `Decision` is not a required field on `DigitalTwin`.
Decision State materialisation is an in-memory audit artefact only in this
capability (no ORM). Readiness remains preparedness context — Decision never
asks readiness to choose actions.

**Recommendation Engine** is a separate read-side package
(`app/domain/recommendation/`), not a Twin write domain, not an Update
Strategy, and not a second Decision Engine. It packages a `Decision` into an
attributable `Recommendation` (suggestion surface, reason narration, warrant
honesty, journal affordances). It never re-selects actions, invents ranking,
mutates Twin beliefs, recomputes readiness, or generates missions. Live
`Recommendation` is not a required field on `DigitalTwin`. Callers that need
a Recommendation must obtain a Decision via `DecisionEngine.evaluate(...)`
first, then call `RecommendationEngine.package(decision, ...)`.

**Mission Intelligence** is a separate execution / projection package
(`app/domain/mission/`), not a Twin write domain, not an Update Strategy, not
a second Decision Engine, and not Recommendation packaging. It operationalises
`Decision`(s) into session/day domain `Mission` / `MissionTask` structure
with Decision attribution, warrant honesty, feasibility acknowledgements, and
Behaviour evidence hooks. It never re-selects actions, invents filler or
ranking, mutates Twin beliefs, recomputes readiness, owns WeekPlan policy, or
runs scheduling optimisation. Live domain `Mission` is not a required field
on `DigitalTwin`. Domain `Mission` / `MissionTask` are distinct from ORM
`app.models.mission.Mission` / `MissionTask` (Stage A coexistence — named
dual truth). Callers that need a Decision-first Mission must obtain
`Decision`(s) via `DecisionEngine.evaluate(...)` (and optionally Recommendation
language via `RecommendationEngine.package(...)`), then call
`MissionIntelligence.compose(decision_or_batch, execution_context, ...)`.
Composition must not call Decision Engine as a hidden re-selection path.

This package is **not** persistence, HTTP, UI, mastery/readiness scoring,
recommendation packaging logic, mission composition, or service-layer
orchestration. It defines:

1. Immutable *state objects* that represent a learner’s current exam-preparation
   condition.
2. A registry-backed *update pipeline* that coordinates update strategies.
3. Concrete *update strategies* that evolve domain states from Learning Evidence
   (Knowledge, Memory, Behaviour, and Performance — intentionally simple
   structural rules only).

Canonical architecture: [`STUDENT_DIGITAL_TWIN.md`](../../../STUDENT_DIGITAL_TWIN.md).  
Ubiquitous language: [`UBIQUITOUS_LANGUAGE.md`](../../../UBIQUITOUS_LANGUAGE.md).

## Purpose

Establish a framework-independent representation of *who the student is
relative to a syllabus and a sitting* — Knowledge, Memory, Behaviour,
Performance, Goals, Identity, and Prediction snapshots — as one aggregate.

Provide the orchestration mechanism that applies Learning Evidence to that
aggregate via registered **Update Strategies**, producing a new immutable Twin
snapshot.

The Twin is Kwalitec’s **single authoritative learner-state model**. Study
plans, missions, readiness scores, and recommendations are *consequences* of
Twin state; they must not become competing learner-state stores.

| Capability | Delivered |
|---|---|
| 2.1 | Immutable Twin **state objects** |
| 2.2 | Twin Update Pipeline **orchestration framework** |
| 2.3 | **Knowledge Update Strategy** (structural Knowledge evolution) |
| 2.4 | **Memory Update Strategy** (structural Memory evolution) |
| 2.5 | **Behaviour Update Strategy** (structural Behaviour evolution) |
| 2.6 | **Performance Update Strategy** (structural Performance evolution) |
| 2.7 | **Readiness Aggregation** (read-side; see `app/domain/readiness/`) |
| 2.8 | **Decision Engine** (read-side; see `app/domain/decision/`) |
| 2.9 | **Recommendation Engine** (read-side packaging; see `app/domain/recommendation/`) |
| 2.10 | **Mission Intelligence** (execution / projection; see `app/domain/mission/`) |

## Responsibilities

| Module | Responsibility |
|---|---|
| `identity_state.py` | Who the learner is (student, curriculum, exam, sitting) |
| `goal_state.py` | Pass ambition, completion date, planned weekly hours |
| `knowledge_state.py` | Structural topic-mastery slots and evidence references |
| `memory_state.py` | Structural retention slots and revision references |
| `behaviour_state.py` | Consistency metrics and session / pattern / evidence references |
| `performance_state.py` | Assessment references and performance summaries |
| `prediction_state.py` | Stored readiness / pass-probability snapshots |
| `digital_twin.py` | Immutable aggregate composing the domains above |
| `update_context.py` | Immutable context (Twin + evidence + metadata) |
| `update_result.py` | Pipeline outcome (original / updated Twin, messages) |
| `update_strategy.py` | Public strategy contract alias |
| `strategies/base_strategy.py` | Abstract update strategy interface |
| `strategies/knowledge_update_strategy.py` | Structural KnowledgeState evolution from evidence |
| `strategies/memory_update_strategy.py` | Structural MemoryState evolution from evidence |
| `strategies/behaviour_update_strategy.py` | Structural BehaviourState evolution from evidence |
| `strategies/performance_update_strategy.py` | Structural PerformanceState evolution from evidence |
| `update_pipeline.py` | Registry coordinator that invokes applicable strategies |

This package **must not**:

- Import Flask, blueprints, SQLAlchemy, or request/session globals
- Define repositories, database models, or Alembic migrations
- Persist Twin state or Learning Evidence
- Compute mastery, confidence, readiness, pass probability, or forgetting curves
- Produce recommendations, plans, or missions
- Expose routes, templates, or HTTP APIs

## Knowledge Update Strategy

`KnowledgeUpdateStrategy` is the first concrete `BaseUpdateStrategy`.

### Purpose

Evolve the Twin’s **KnowledgeState** when Knowledge-related Learning Evidence
arrives. Capability 2.3 keeps educational behaviour intentionally simple so the
pipeline can evolve Knowledge structure without committing to a mastery model.

### Behaviour (intentionally simple)

1. **Applicability** — runs when the context contains at least one
   Knowledge-related evidence record with a non-empty `topic_id`
   (see `KNOWLEDGE_EVIDENCE_TYPES`).
2. **New topic** — creates a `TopicMasteryRecord` when a topic is first seen.
3. **Evidence count** — appends the evidence id to the topic’s `evidence_ids`
   (count = `len(evidence_ids)`). Does not invent a separate counter field.
4. **State references** — appends the evidence id to `KnowledgeState.evidence_ids`.
5. **Timestamp** — sets `KnowledgeState.last_updated` to the latest processed
   evidence timestamp.
6. **Immutability** — returns a **new** `DigitalTwin`; the original Twin is
   never mutated. `mastery_belief` is preserved as-is and never computed here.

### What it does *not* do

- Mastery / Bayesian Knowledge Tracing / IRT
- Confidence, readiness, or pass-probability scoring
- Forgetting curves or spaced-repetition scheduling
- Persistence, recommendations, planning, or insight generation

## Memory Update Strategy

`MemoryUpdateStrategy` is the second concrete `BaseUpdateStrategy`.

### Purpose

Evolve the Twin’s **MemoryState** when Memory-related Learning Evidence
arrives. Capability 2.4 keeps educational behaviour intentionally simple so the
pipeline can evolve Memory structure without committing to a retention,
forgetting, or spaced-repetition model.

### Behaviour (intentionally simple)

1. **Applicability** — runs when the context contains at least one
   Memory-related evidence record with a non-empty `topic_id`
   (see `MEMORY_EVIDENCE_TYPES`: revision sessions, flashcard reviews).
2. **New retention entry** — creates a `RetentionRecord` when a topic is first
   seen, setting `last_reinforced` to the evidence timestamp.
3. **Existing entry** — updates `last_reinforced` when newer evidence arrives;
   never regresses the clock on older evidence.
4. **Evidence references** — appends the evidence id to
   `MemoryState.revision_ids` (deduped).
5. **Timestamp** — sets `MemoryState.last_updated` to the latest processed
   evidence timestamp.
6. **Immutability** — returns a **new** `DigitalTwin`; the original Twin is
   never mutated. `retention_belief` is preserved as-is and never computed here.

### What it does *not* do

- Retention / forgetting-curve / memory-strength scoring
- Spaced repetition, FSRS, SM-2, Leitner, or revision scheduling
- Confidence or readiness scoring
- Persistence, recommendations, planning, or insight generation

### KnowledgeState vs MemoryState

| | **KnowledgeState** | **MemoryState** |
|---|---|---|
| Question | “What do they know *now*?” | “Will they still know it?” |
| Structural slot | `TopicMasteryRecord` | `RetentionRecord` |
| Belief field (stored, not computed here) | `mastery_belief` | `retention_belief` |
| Evidence references | `evidence_ids` (state + per topic) | `revision_ids` (state) |
| Typical evidence | Attempts, quizzes, diagnostics | Revision sessions, flashcard reviews |
| Strategy | `KnowledgeUpdateStrategy` | `MemoryUpdateStrategy` |

Knowledge must not encode forgetting curves. Memory must not become a second
mastery store. Keep the domains complementary
([`STUDENT_DIGITAL_TWIN.md`](../../../STUDENT_DIGITAL_TWIN.md) Knowledge vs Memory).

## Behaviour Update Strategy

`BehaviourUpdateStrategy` is the third concrete `BaseUpdateStrategy`.

### Purpose

Evolve the Twin’s **BehaviourState** when Behaviour-primary Learning Evidence
arrives. Capability 2.5 keeps educational behaviour intentionally simple so the
pipeline can evolve Behaviour structure without committing to consistency,
adherence, burnout, or velocity models.

**Hard educational rule:** Behaviour never grants or revokes mastery by itself.
Behaviour is not learning; activity is not readiness.

### Behaviour (intentionally simple)

1. **Applicability** — runs when the context contains at least one
   Behaviour-primary evidence record (see `BEHAVIOUR_EVIDENCE_TYPES`:
   mission completed/missed, skipped/abandoned session, study session,
   time on task, study break). Does **not** require `topic_id`.
2. **Session lineage** — appends a practice-unit / session id to
   `session_history_ids` (deduped). Identity priority: payload
   `session_id` / `mission_id` / `practice_unit_id`, else
   `originating_event_id`, else `evidence_id`.
3. **Pattern lineage** — appends `study_pattern_ids` only when evidence
   payload/metadata already supplies them; never invents clusters.
4. **Evidence references** — appends the evidence id to
   `BehaviourState.evidence_ids` (deduped).
5. **Metric bag** — preserves `consistency_metrics` unchanged; never invents
   scores.
6. **Timestamp** — sets `BehaviourState.last_updated` to the latest processed
   evidence timestamp.
7. **Immutability** — returns a **new** `DigitalTwin`; the original Twin is
   never mutated.

### What it does *not* do

- Consistency / adherence / streak scoring
- Burnout, velocity, or preferred-window models
- Knowledge or Memory belief changes
- Readiness, recommendations, planning, or mission generation
- Persistence or nested `BehaviourRecord` scoring

### Ownership vs Knowledge / Memory

| | **Knowledge** | **Memory** | **Behaviour** |
|---|---|---|---|
| Question | “What do they know *now*?” | “Will they still know it?” | “How do they actually study?” |
| Primary evidence | Attempts, quizzes, diagnostics | Revision, flashcards | Missions, skips, sessions, time |
| Requires `topic_id`? | Yes | Yes | No |
| Strategy | `KnowledgeUpdateStrategy` | `MemoryUpdateStrategy` | `BehaviourUpdateStrategy` |

Mission completion must not overwrite quiz-driven Knowledge updates. Revision
evidence remains Memory-primary; Behaviour does not absorb those types.

## Performance Update Strategy

`PerformanceUpdateStrategy` is the fourth concrete `BaseUpdateStrategy`.

### Purpose

Evolve the Twin’s **PerformanceState** when Performance-primary Learning
Evidence arrives. Capability 2.6 keeps educational behaviour intentionally
simple so the pipeline can evolve Performance structure without committing to
accuracy, strength, IRT, or pass-probability models.

**Hard educational rules:**

1. Performance never becomes a second Knowledge mastery store.
2. High mission adherence never invents strong Performance.
3. A single mock never becomes the whole readiness or pass-probability story.
4. Self-reported confidence never overrides dense contrary Performance evidence
   in educational narrative.

### Behaviour (intentionally simple)

1. **Applicability** — runs when the context contains at least one
   Performance-primary evidence record (see `PERFORMANCE_EVIDENCE_TYPES`:
   quiz completed, mock exam, past-paper attempt, diagnostic assessment,
   post-exam outcome). Does **not** require `topic_id` for all primary types
   (assessment-instance / post-exam scopes may apply without topic mapping).
2. **Assessment lineage** — appends an assessment / attempt id to
   `assessment_ids` (deduped). Identity priority: payload/metadata
   `assessment_id` / `quiz_id` / `mock_id` / `past_paper_id` /
   `diagnostic_id`, else `evidence_id`.
3. **Scoped summaries** — creates or merges a `PerformanceSummary` when a
   usable `scope_id` is resolved. Scope priority: explicit `scope_id` /
   assessment-instance keys, else non-empty `topic_id`, else non-empty
   `originating_event_id`. If no usable scope exists, append assessment /
   evidence references only — never fabricate a topic summary from free text.
4. **Fact bag** — overlays only summary facts / condition tags already
   supplied on evidence; preserves unknown keys; never invents accuracy or
   strength scores. Formative condition tags are stored as supplied — never
   upgraded to exam-condition strength.
5. **Evidence references** — appends the evidence id to
   `PerformanceState.evidence_ids` (deduped).
6. **Timestamp** — sets `PerformanceState.last_updated` to the latest
   processed evidence timestamp.
7. **Immutability** — returns a **new** `DigitalTwin`; the original Twin is
   never mutated.

### What it does *not* do

- Accuracy / strength / IRT / partial-credit scoring
- Pass probability or readiness composites
- Knowledge mastery or Memory retention belief changes
- Behaviour adherence absorption into “study quality” Performance
- Recommendations, planning, or mission generation
- Persistence

### Ownership vs Knowledge / Memory / Behaviour

| | **Knowledge** | **Memory** | **Behaviour** | **Performance** |
|---|---|---|---|---|
| Question | “What do they know *now*?” | “Will they still know it?” | “How do they actually study?” | “How do they perform when assessed?” |
| Primary evidence | Attempts, quizzes, diagnostics | Revision, flashcards | Missions, skips, sessions, time | Quiz / mock / past paper / diagnostic / post-exam |
| Requires `topic_id`? | Yes | Yes | No | No (topic optional for supports) |
| Strategy | `KnowledgeUpdateStrategy` | `MemoryUpdateStrategy` | `BehaviourUpdateStrategy` | `PerformanceUpdateStrategy` |

Mission completion alone must not invent Performance. Question attempts remain
Knowledge-primary (Choice A: Performance ignores them). Revision remains
Memory-primary. Post-exam is Performance-primary.

### Relationship to the Twin Update Pipeline

```
Learning Evidence
      │
      ▼
UpdateContext
      │
      ▼
TwinUpdatePipeline
      │  register(KnowledgeUpdateStrategy())
      │  register(MemoryUpdateStrategy())
      │  register(BehaviourUpdateStrategy())
      │  register(PerformanceUpdateStrategy())
      │  supports(context)? → apply(context) → new Twin
      ▼
UpdateResult (original_twin, updated_twin, applied_strategies, …)
```

Recommended registration order (structural phase): Knowledge → Memory →
Behaviour → Performance. The pipeline remains an orchestration shell and does
not hard-code these strategies.

The same Learning Evidence batch may drive multiple strategies when mixed
types are present (e.g. a quiz updates Knowledge and Performance; a mission
completed updates Behaviour). They must not share mutable state: each returns
a new Twin snapshot; the pipeline chains them via `context.with_twin(...)`.

### Relationship to the future Memory Engine

The **Memory Engine** (Revision Engine / spaced-repetition scheduling) will
later:

- **Read** `MemoryState` retention structure and `last_reinforced` clocks
- **Compute** retention beliefs, due dates, and decay using educational
  algorithms (forgetting curves, FSRS, etc.)
- **Emit** revision / flashcard Learning Evidence that Memory strategy already
  knows how to apply structurally

Capability 2.4 only establishes the *structural write path*. Educational
memory algorithms remain deferred. When those algorithms land, they should
update beliefs via evidence + strategy extension — not by mutating Twin
state from services or bypassing the pipeline.

## Update lifecycle

```
Learning Evidence (one or more)
      │
      ▼
UpdateContext  (current Twin + evidence + metadata)  — immutable
      │
      ▼
TwinUpdatePipeline
      │  discover registered strategies (registration order)
      │  for each strategy where supports(context):
      │       updated Twin ← strategy.apply(context)
      │       context ← context.with_twin(updated Twin)
      ▼
UpdateResult
      ├── original_twin
      ├── updated_twin          (new snapshot; may equal original)
      ├── applied_strategies
      ├── processing_messages
      └── success
```

1. Receive a `DigitalTwin` and one or more `LearningEvidence` records.
2. Build an immutable `UpdateContext`.
3. If **no strategies are registered**, return an `UpdateResult` whose
   `updated_twin` is the original Twin, with processing messages explaining
   the no-op (`success=True`).
4. Otherwise, invoke every registered strategy that reports
   `supports(context)`, in registration order.
5. Each strategy returns a **new** Twin; the pipeline never mutates the
   original aggregate in place.
6. Return `UpdateResult` describing what ran.

## Relationship to Learning Evidence

Learning Evidence ([`LEARNING_EVIDENCE_MODEL.md`](../../../LEARNING_EVIDENCE_MODEL.md),
[`app/domain/evidence/`](../evidence/)) is the immutable, attributable *history*
of what the student did. The Twin is the authoritative *state* derived from
that history.

```
Learning Event
      → Evidence Candidate → Learning Evidence (canonical, append-only)
            → Twin Update Pipeline (this package)
                  → Knowledge / Memory / Behaviour / Performance Update Strategies
                        → DigitalTwin domain states (new snapshot)
```

Rules:

1. Evidence is the only legitimate input that may change Twin beliefs.
2. Twin domains reference curriculum identity and evidence ids — they do not
   invent syllabus structure.
3. The pipeline coordinates strategy application; specialised strategies own
   domain evolution.

## Relationship to the Student Digital Twin

`DigitalTwin` remains a frozen aggregate of domain states. It exposes **no**
in-place update methods. Evolution happens only by constructing a new Twin
through the Update Pipeline (or by explicit `DigitalTwin.create` composition
in tests / bootstrap).

## Readiness Aggregation (read-side)

Capability 2.7 lives in [`app/domain/readiness/`](../readiness/), **outside**
this Twin write package.

| Concern | Owner |
|---|---|
| Producing `ReadinessState` | `ReadinessAggregation.derive(twin, curriculum, …)` |
| Twin belief domains used as inputs | Knowledge / Memory / Behaviour / Performance strategies |
| Syllabus denominator / weights | `CurriculumContext` built **outside** aggregation (via CurriculumService helpers in future orchestration) |
| Optional historical copy | Prediction snapshot path (deferred) |

Binding rules:

1. Aggregation **reads** Twin domains; it never mutates them.
2. Aggregation never writes Learning Evidence.
3. Aggregation never selects next actions or generates missions.
4. Cold start / empty domains yield **not yet knowable** overall posture — never Mid/High fabrication.
5. Confidence self-report is **omitted** from readiness v1 inputs.
6. Future services that need Curriculum weights must build `CurriculumContext` outside the domain aggregator so aggregation stays framework-free.

```
DigitalTwin snapshot + CurriculumContext + Goals
        ↓
ReadinessAggregation.derive(...)
        ↓
ReadinessState (factors + Evidence Warrant)
```

Do **not** register Readiness as a `BaseUpdateStrategy`. Do **not** add a
required `readiness` field on `DigitalTwin` in this capability.

## Future Update Strategies

Registered later; **not** implemented in this capability:

| Strategy | Intended concern |
|---|---|
| `PredictionSnapshotStrategy` | Store readiness / pass-probability snapshots |

Each inherits `BaseUpdateStrategy`, implements `supports` / `apply`, and is
registered with `TwinUpdatePipeline` without modifying the pipeline class.
Readiness Aggregation remains a read-side consumer — not a write strategy.

## Relationship to the future Insight Engine

The Insight Engine (and related Prediction / Recommendation consumers) will
**read** Twin state to produce explainable insights, forecasts, and next
actions. Insights must cite Twin factors and evidence lineage; they must not
silently mutate Knowledge, Memory, Behaviour, or Performance or bypass Twin
inputs.

The Update Pipeline **writes** new Twin snapshots from evidence. The Insight
Engine **reads** those snapshots. They must not be conflated.

## Extension guidelines

1. **New structural fields** — add optional fields to the relevant `*State`
   dataclass when the concept is stable across producers. Prefer tuples for
   collections and defensive copies for dict bags.
2. **New nested records** — keep them frozen dataclasses in the owning state
   module (e.g. `TopicMasteryRecord` beside `KnowledgeState`,
   `RetentionRecord` beside `MemoryState`).
3. **New update strategies** — subclass `BaseUpdateStrategy` under
   `strategies/`, register with the pipeline; do not put educational math in
   `update_pipeline.py`.
4. **Richer Knowledge algorithms** — extend `KnowledgeUpdateStrategy` (or
   introduce a successor strategy) when mastery / confidence models are ready;
   keep the pipeline unaware of scoring details.
5. **Richer Memory algorithms** — extend `MemoryUpdateStrategy` (or introduce
   a successor / Memory Engine consumer) when retention, decay, or spaced-
   repetition models are ready; keep scheduling and belief math out of the
   pipeline shell. Prefer emitting Learning Evidence that this strategy (or
   an extended version) applies structurally.
6. **Expand `MEMORY_EVIDENCE_TYPES`** carefully when new revision-like
   evidence types are added — do not absorb Knowledge attempt types into
   Memory.
7. **Richer Behaviour algorithms** — extend `BehaviourUpdateStrategy` (or
   introduce a successor) when consistency / adherence models are ready; fill
   `consistency_metrics` via approved extension; never invent pattern clusters
   without evidence lineage. Prefer emitting Learning Evidence that this
   strategy (or an extended version) applies structurally.
8. **Expand `BEHAVIOUR_EVIDENCE_TYPES`** carefully for documented secondary
   weak updates — do not absorb Knowledge attempt or Memory revision primary
   types into Behaviour.
9. **Planning / Readiness / Motivation domains** — introduce as additional
   immutable state modules when a later capability requires them.
10. **Do not** introduce Flask, ORM, HTTP, or service types into this package.
11. **Do not** mutate Twin aggregates in place — always return a new frozen
    snapshot from `apply`.
12. **Do not** let Memory, Knowledge, Behaviour, and Performance share mutable
    bags or diverge into competing mastery / assessment stores.
13. **Richer Performance algorithms** — extend `PerformanceUpdateStrategy` (or
    introduce a successor) when accuracy / strength / condition-delta models
    are ready; fill summary bags via approved extension; never invent High
    Performance from Goals, Behaviour, or empty cold start. Prefer emitting
    Learning Evidence that this strategy (or an extended version) applies
    structurally.
14. **Expand `PERFORMANCE_EVIDENCE_TYPES`** carefully for documented secondary
    weak updates — do not absorb Behaviour mission or Memory revision primary
    types into Performance; question attempts remain Knowledge-primary unless
    secondary weak lineage is explicitly approved.

## Package layout

```
app/domain/twin/
  __init__.py
  digital_twin.py
  identity_state.py
  goal_state.py
  knowledge_state.py
  memory_state.py
  behaviour_state.py
  performance_state.py
  prediction_state.py
  update_context.py
  update_result.py
  update_strategy.py
  update_pipeline.py
  strategies/
    __init__.py
    base_strategy.py
    knowledge_update_strategy.py
    memory_update_strategy.py
    behaviour_update_strategy.py
    performance_update_strategy.py
  README.md
```
