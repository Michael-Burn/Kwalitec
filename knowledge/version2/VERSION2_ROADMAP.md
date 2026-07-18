# Version 2 Roadmap

**Document ID:** V2-001-ROADMAP  
**Milestone:** V2-001 — Learning Journey Domain Architecture  
**Status:** Implementation sequencing reference  
**Nature:** Milestone definitions — not a sprint backlog  

**Strategy context:** [`VERSION2_PRODUCT_STRATEGY.md`](../product/roadmap/VERSION2_PRODUCT_STRATEGY.md)  
**Architecture parent:** [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md)

Version 2 is delivered as independently valuable milestones. Each milestone must improve educational decision quality even if work stopped afterwards. Evidence — not novelty — justifies scope expansion (Product Strategy).

---

## Milestone Sequence

```
V2-001 Architecture
    ↓
V2-002 Learning Journey Domain Foundation
    ↓
V2-003 Learning Journey Engine
    ↓
V2-004 Curriculum Graph / early Mission Engine parallel
    ↓
V2-005 Learning Session Engine
    ↓
V2-006 Mission Adapter
    ↓
V2-007 Mission Engine 2.0 (authoritative)
    ↓
V2-008 Educational Analytics
    ↓
V2-009 Founder Intelligence
    ↓
V2-010 Internal Alpha
```

**Note:** Curriculum Graph foundation shipped as a **parallel stream** under milestone id **V2-004 — Curriculum Graph Foundation** (`app/domain/curriculum/`, [`CURRICULUM_GRAPH.md`](CURRICULUM_GRAPH.md)). An early Mission Engine parallel package also exists at `app/application/mission_engine/`. Authoritative Mission Engine 2.0 is **V2-007** (`app/application/mission_engine_v2/`, [`MISSION_ENGINE_2.md`](MISSION_ENGINE_2.md)). Revision Engine (formerly listed as V2-007) is deferred to a subsequent stream after Twin signals land. Prefer document titles over bare ids when sequencing work.

---

## V2-001 — Architecture

**Status:** Complete (documentation)

**Delivers**

- Authoritative Version 2 educational architecture under `knowledge/version2/`
- Learning Journey domain vocabulary and state machines
- Educational principles, curriculum model, migration map, roadmap

**Does not deliver**

- Runtime behaviour, migrations, UI, APIs, feature flags

**Exit criteria**

- Future milestones can implement without redefining Journey, Session, Evidence, Reflection, or Topic Complete

---

## V2-002 — Learning Journey Domain Foundation

**Status:** Complete (domain code)

**Purpose**

Introduce the pure Version 2 Learning Journey domain package that future engines build upon — without changing Version 1 behaviour.

**Depends on**

- V2-001 domain + state machine documentation
- Existing Learning Evidence Model types (`app.domain.evidence`)

**Delivers**

- `app/domain/learning_journey/` entities, value objects, progress/validation services
- `LearningJourneyRepository` contract (no implementation)
- Pure domain unit tests
- [`DOMAIN_IMPLEMENTATION.md`](DOMAIN_IMPLEMENTATION.md) code ↔ architecture map

**Does not deliver**

- Journey Engine runtime, persistence, migrations, UI, feature flags
- Version 1 route / Mission / Recommendation / Dashboard changes
- Curriculum Graph persistence

**Exit criteria**

- Domain objects map to V2-001 vocabulary
- Session complete cannot complete a journey
- Progress never invents mastery scores
- Existing Version 1 suite remains green

---

## V2-003 — Learning Journey Engine

**Purpose**

Operate Learning Journey aggregates: JourneyState transitions, JourneyProgress evaluation, completion criteria, and history spine — using the V2-002 domain package.

**Depends on**

- V2-001 domain + state machine
- V2-002 domain foundation
- Curriculum topic/objective identity (Curriculum Engine; graph enhancements optional)

**Expected outcomes**

- Create/activate/pause/resume/defer/abandon/complete journeys
- JourneyHistory spine usage in runtime flows
- Dual-run reconciliation design with Version 1 Study Progress

**Must not**

- Auto-complete from mastery thresholds
- Replace Twin belief stores
- Bypass `app.domain.learning_journey` vocabulary

---

## V2-004 — Mission Engine 2.0 (early parallel package)

**Status:** Complete (early application orchestration — `app/application/mission_engine/`)

**Purpose**

Replace isolated daily mission generation architecture with a Version 2 orchestration layer that schedules one executable learning session per mission — without educational decision-making.

**Depends on**

- V2-003 Learning Journey Engine
- V2-005 Learning Session Runtime (session phase for resume / continue delivery)
- Curriculum Navigation Service (structural topic confirmation)
- Explainability Standard / Learning Mode authority (cutover still deferred)

**Delivered**

- `app/application/mission_engine/` — early Mission Engine 2.0 parallel package
- Deterministic scheduling (today / tomorrow / deferred / missed / revision)
- Lifecycle: schedule → activate → start → complete → archive (+ defer / skip / miss)
- Dashboard-ready DTOs + delivery payloads (no UI)
- `V1MissionAdapter` for parallel-only Version 1 coexistence
- Framework-independent unit suite (`tests/application/mission_engine/`)

**Note:** Authoritative Mission Engine 2.0 for adapter-compatible orchestration is delivered under **V2-007** as `app/application/mission_engine_v2/` — see [`MISSION_ENGINE_2.md`](MISSION_ENGINE_2.md).

**Must not**

- Contain educational reasoning (progression, Topic Complete, mastery)
- Silently override Learning Mode focus
- Treat mission complete as Topic Complete
- Replace Version 1 `MissionService` behaviour in this milestone

---

## V2-005 — Learning Session Engine

**Status:** Complete (application runtime — session execution layer)

**Purpose**

Run Learning Sessions as journey-scoped work with pause/resume, required reflection, and evidence emission.

**Depends on**

- V2-003, V2-004 (or interim recommendation adapter)
- LXP-002 patterns as UX ancestry

**Expected outcomes**

- SessionState machine implementation
- JourneyReflection capture
- JourneyEvidence attribution on session close
- Clear separation of session complete vs journey complete

**Delivered**

- `app/application/learning_session/` — Learning Session Runtime
- Runtime phases PLANNED → READY → ACTIVE → PAUSED → COMPLETED → ARCHIVED
- Framework-independent unit suite (`tests/application/learning_session/`)
- [`LEARNING_SESSION_RUNTIME.md`](LEARNING_SESSION_RUNTIME.md)

**Must not**

- Skip reflection without explicit deferred policy
- Write Estimated Mastery from bare completion
- Complete journeys / mutate Version 1 / add persistence or UI

---

## V2-006 — Student Digital Twin 2.0 (roadmap intent)

**Purpose**

Evolve Twin consumption and belief updates to prefer journey-attributed evidence and journey-aware planning inputs — without changing Twin constitutional authority.

**Depends on**

- Evidence Model + Twin specs
- V2-003–005 evidence flows

**Expected outcomes**

- Stronger linkage from journey evidence → Knowledge / Memory / Behaviour / Readiness
- Journey-aware explanations
- No competing learner-state store

**Must not**

- Let generative AI own Twin mutations
- Collapse coverage into mastery in Twin narratives

**Implementation note**

The Version 2 bounded-context delivery for Twin philosophy responsibilities is **V2-013** (`app/domain/student_twin/`, `app/application/student_twin/`). V2-006 remains the product-integration intent for journey-attributed evidence into Twin authority.

---

## V2-013 — Student Digital Twin 2.0 (domain + application)

**Status:** Complete (framework-independent domain + application)

**Purpose**

Implement a deterministic, evidence-driven Student Digital Twin that models the evolving educational state of a learner. Consumes evidence only — never curriculum, PDFs, or AI responses as Twin truth.

**Depends on**

- [`DIGITAL_TWIN_PHILOSOPHY.md`](DIGITAL_TWIN_PHILOSOPHY.md)
- Version 2 educational principles

**Expected outcomes**

- `app/domain/student_twin/` — immutable aggregate, evidence events, state value objects
- `app/application/student_twin/` — `StudentTwinEngine` + calculators / estimators / policies / DTOs
- Deterministic mastery, confidence, retention, readiness, velocity, weaknesses, recommendations
- Immutable snapshots, timeline evolution, explainable recommendations
- Framework-independent test suite (`tests/domain/student_twin/`, `tests/application/student_twin/`)
- Docs: [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md), [`DIGITAL_TWIN_PHILOSOPHY.md`](DIGITAL_TWIN_PHILOSOPHY.md)

**Must not**

- Teach or generate educational content
- Store curriculum / PDFs
- Add Flask routes, persistence, UI, or migrations
- Let AI determine learner state
- Silently replace Epic Twin production paths (`app/domain/twin/`) without explicit cutover

---

## V2-007 — Mission Engine 2.0

**Status:** Complete (application orchestration — parallel with Version 1)

**Purpose**

Implement Mission Engine 2.0 as a pure orchestration layer that composes a Daily Mission from Version 2 educational services — without educational decision-making.

**Depends on**

- Mission Adapter contracts (`MissionEnginePort`)
- Learning Journey Engine (injected port)
- Learning Session Runtime (injected port)
- Curriculum Navigation Service (injected port)

**Delivered**

- `app/application/mission_engine_v2/` — authoritative Mission Engine 2.0
- Mission factory: Journey Snapshot → Topic → Session Plan → Recommendation → Mission DTO
- Deterministic scheduling (today / deferred / revision / missed / future)
- Lifecycle: PLANNED → READY → ACTIVE → PAUSED → COMPLETED → ARCHIVED
- Workload balancer (structural signals only — never mastery)
- Dashboard-ready DTOs (`DailyMission`, `MissionCard`, `MissionDashboard`, `MissionTimeline`, `MissionExecution`)
- Adapter-compatible `MissionEnginePort` implementation
- Framework-independent unit suite (`tests/application/mission_engine_v2/`, ~220–280 tests)
- [`MISSION_ENGINE_2.md`](MISSION_ENGINE_2.md)

**Must not**

- Contain educational reasoning (progression, Topic Complete, mastery)
- Modify Mission Adapter / Journey Engine / Session Runtime / Curriculum Graph / Version 1
- Add persistence, Flask, SQLAlchemy, AI, or generated study content
- Treat mission complete as Topic Complete

**Deferred:** Revision Engine (previously listed under this id) awaits Twin memory signals in a later stream.

---

## V2-008 — Educational Analytics

**Purpose**

Measure journey health, session patterns, reflection quality signals, recommendation continuity, and coverage vs understanding separately.

**Depends on**

- Stable journey/session evidence from prior milestones

**Expected outcomes**

- Analytics that respect claim hierarchy (facts vs estimates)
- Cohort and individual views that support product learning

**Must not**

- Optimise vanity engagement over educational outcomes
- Mix unlabeled mastery into coverage KPIs

---

## V2-009 — Founder Intelligence

**Purpose**

Extend founder operational insight with journey-level educational signals (inactive journeys, stalled READY_FOR_COMPLETION, reflection gaps, recommendation thrash) while keeping Founder systems non-authoritative over student Learning Mode.

**Depends on**

- V2-008 analytics feeds / operational snapshots
- Existing Founder OS patterns (advisory only)

**Must not**

- Allow founder tools to mutate student journeys directly as a side channel

---

## V2-010 — Internal Alpha

**Purpose**

Validate Version 2 educational behaviour with invite-only learners under research and operational observation discipline.

**Depends on**

- Sufficient vertical slice of V2-003–007 for a coherent student experience
- Product Strategy evidence gates

**Expected outcomes**

- Observed journey behaviour, recommendation continuity, reflection adherence, educational trust signals
- Evidence that feeds the next iteration cycle

**Must not**

- Ship Version 2 Internal Alpha without explainability and continuity invariants
- Treat alpha novelty as proof of educational value without measurement

---

## Cross-Milestone Constraints

| Constraint | Applies to |
|------------|------------|
| No Constitution contradiction | All |
| V1 runtime safe until explicit cutover | All implementation milestones |
| Deterministic core paths | V2-003–007 |
| Evidence before opinion | V2-004–008 |
| Documentation in `knowledge/version2/` remains concept authority | All |

---

## Suggested Dependency Graph

```
V2-001
  └── V2-002
        └── V2-003
              ├── V2-004
              │     └── V2-005
              │           ├── V2-006
              │           │     └── V2-007
              │           └── V2-008
              │                 └── V2-009
              └── V2-010 (requires coherent slice; not only V2-009)
```

V2-010 may begin on a vertical slice before V2-009 completes, but must not precede a minimal Journey + Recommendation + Session path.

---

## Closing

This roadmap is the implementation sequence for Version 2. New milestones may be inserted only if they refine — not redefine — the Learning Journey architecture established in V2-001.
