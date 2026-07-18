# Learning Journey Domain

**Document ID:** V2-001-DOMAIN  
**Milestone:** V2-001 — Learning Journey Domain Architecture  
**Status:** Authoritative domain specification  
**Nature:** Conceptual educational domain — not a database schema  

**Parent:** [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md)  
**State transitions:** [`STATE_MACHINE.md`](STATE_MACHINE.md)  
**Educational rules:** [`EDUCATIONAL_PRINCIPLES.md`](EDUCATIONAL_PRINCIPLES.md)

This document defines the Version 2 educational domain entities. It evolves — and does not duplicate — the Student Digital Twin, Learning Evidence Model, Educational State Lifecycle, and Educational Constitution.

---

## 1. Domain Overview

The Learning Journey domain answers:

> For this student and this curriculum topic, what multi-session educational path is underway, what evidence has it produced, and what should happen next until the topic is educationally complete?

```
LearningJourney
├── LearningObjective[]          (references curriculum objectives)
├── LearningSession[]
│   ├── SessionState
│   ├── JourneyEvidence[]        (session-scoped contributions)
│   └── JourneyReflection
├── JourneyRecommendation[]      (derived commitments / advice)
├── JourneyEvidence[]            (journey-scoped accumulation)
├── JourneyHistory               (immutable transition & event log)
├── JourneyProgress              (derived educational measures)
└── JourneyState                 (lifecycle posture)
```

**Ownership principle:** Journey artefacts belong to the **learner** for the syllabus topic identity. Planning containers (Study Plan, daily mission rows) may contextualise journeys; they do not ontologically own them ([`EDUCATIONAL_CONTINUITY_STANDARD.md`](../educational/EDUCATIONAL_CONTINUITY_STANDARD.md)).

---

## 2. LearningJourney

### Purpose

Represent the complete educational path a student takes through a single curriculum **Topic**, from first meaningful engagement to lawful **Topic Complete** (or lawful abandonment / deferral).

### Responsibilities

- Anchor all sessions, evidence, reflections, and recommendations for one topic
- Hold journey lifecycle state (`JourneyState`)
- Expose progress measures (`JourneyProgress`) without inventing mastery
- Enforce that Topic Complete requires journey completion criteria — not a single session
- Preserve history across days, plan changes, and pauses

### Relationships

| Relates to | Cardinality | Meaning |
|------------|-------------|---------|
| Topic (curriculum) | N : 1 | Journey is always about one official topic |
| Student / Twin Identity | N : 1 | Owned by one learner |
| LearningObjective | 1 : N | Objectives the journey intends to satisfy |
| LearningSession | 1 : N | Bounded work blocks inside the journey |
| JourneyEvidence | 1 : N | Accumulated attributable observations |
| JourneyReflection | 1 : N | Via sessions (one reflection per completed session) |
| JourneyRecommendation | 1 : N | Advice / daily commitments that continue the journey |
| JourneyHistory | 1 : 1 | Append-only log of material events |
| JourneyProgress | 1 : 1 | Current derived progress posture |
| Study Plan (V1) | N : 0..1 | Optional planning context; not owner |

### Ownership

- **Educational owner:** Learner + topic identity
- **Mutators (future):** Learning Journey Engine (V2-003); lawful session and evidence writers
- **Non-owners:** Recommendation engines (advice only); Founder systems; UI caches

### Lifecycle

```
Created (NOT_STARTED)
  → activated on first meaningful start (ACTIVE)
  → may PAUSE / RESUME
  → may reach READY_FOR_COMPLETION
  → COMPLETED (Topic Complete outcome)
  or ABANDONED / DEFERRED under explicit rules
```

Full transitions: [`STATE_MACHINE.md`](STATE_MACHINE.md).

### State transitions

Delegated to `JourneyState`. The journey aggregate must never jump to `COMPLETED` from a single session finish without meeting completion criteria.

### Educational reasoning

Professional topics require spaced engagement. The journey is the honest educational container for that work. Without it, the product collapses multi-day learning into mission theatre.

---

## 3. LearningSession

### Purpose

Represent one bounded period of intentional study work that advances an active Learning Journey.

### Responsibilities

- Capture session intent (learn, practice, revise, reflect-heavy review)
- Track session lifecycle (`SessionState`)
- Produce session-scoped evidence and a required reflection on completion
- Contribute to journey progress without claiming Topic Complete
- Record planned vs actual effort for capacity realism

### Relationships

| Relates to | Cardinality | Meaning |
|------------|-------------|---------|
| LearningJourney | N : 1 | Session always belongs to one journey |
| JourneyRecommendation | 0..1 : 1 | May realise a specific recommendation |
| JourneyEvidence | 1 : N | Evidence generated during the session |
| JourneyReflection | 1 : 1 | Required after session completion |
| V1 Study Session / Mission | 0..1 | Migration ancestry (see Migration Strategy) |

### Ownership

- **Educational owner:** Learner (as part of journey history)
- **Mutators (future):** Learning Session Engine (V2-005)
- **Non-owners:** Advisory copy; analytics projections

### Lifecycle

```
NOT_STARTED → ACTIVE → (PAUSED ↔ ACTIVE) → COMPLETED
                                    ↘ ABANDONED
```

A completed session updates journey history and may move journey progress; it does **not** alone complete the journey.

### State transitions

See SessionState in [`STATE_MACHINE.md`](STATE_MACHINE.md).

### Educational reasoning

Sessions create the rhythm of study. Version 2 keeps sessions concrete and finishable while refusing to treat “session finished” as “topic finished.”

---

## 4. LearningObjective

### Purpose

Represent an educational objective the journey aims to satisfy, referenced from the official curriculum (learning outcomes / learning objectives), not invented by the journey engine.

### Responsibilities

- Bind journey intent to syllabus language
- Support completion criteria (“which objectives need evidence?”)
- Enable explainability (“you are working on objective X”)
- Remain stable under curriculum identity rules

### Relationships

| Relates to | Cardinality | Meaning |
|------------|-------------|---------|
| Curriculum Learning Objective / Outcome | N : 1 | Canonical syllabus reference |
| LearningJourney | N : 1 | Objectives scoped to a journey |
| JourneyEvidence | 0..N | Evidence may cite objectives |
| JourneyProgress | derived | Objective coverage / evidence density |

### Ownership

- **Syllabus meaning:** Curriculum Engine
- **Journey binding:** Learning Journey aggregate
- Journeys must not create orphan objectives unknown to the curriculum

### Lifecycle

Objectives are attached when a journey is created or when curriculum remapping lawfully updates bindings. They are not “completed” by checkbox alone; objective satisfaction is evidenced and/or declared under completion criteria ([`CURRICULUM_MODEL.md`](CURRICULUM_MODEL.md)).

### State transitions

Objectives do not have an independent student-facing state machine in V2-001. Progress toward them is reflected in `JourneyProgress` and evidence density.

### Educational reasoning

Without objectives, a journey is only “time on a topic title.” Objectives keep work curriculum-honest and explainable.

---

## 5. JourneyRecommendation

### Purpose

Represent an explainable educational recommendation that **continues, adjusts, or prepares** a Learning Journey — including the daily commitment the student is asked to take next.

### Responsibilities

- Propose the next learning session intent, duration, and focus
- Cite journey state, progress, evidence, and constraints
- Distinguish Learning Mode authority from optional advice (Constitution; Explainability Standard)
- Prefer continuing the active journey over unexplained topic switching
- Record accept / dismiss / expire as behavioural evidence (via Evidence Model categories)

### Relationships

| Relates to | Cardinality | Meaning |
|------------|-------------|---------|
| LearningJourney | N : 1 | Recommendation is journey-scoped |
| LearningSession | 0..1 | May be realised as a session |
| JourneyEvidence / Twin | inputs | Must be evidence-traceable |
| V1 Daily Mission | conceptual successor | See Migration Strategy |

### Ownership

- **Producer (future):** Mission Engine 2.0 / Decision paths (V2-004), consuming Journey Engine + Twin
- **Authority:** Under Learning Mode, recommendations must not silently replace the authorised journey focus
- **Student:** Retains agency for optional advice

### Lifecycle

```
PROPOSED → ACCEPTED → REALISED (session started)
        → DISMISSED
        → EXPIRED
        → SUPERSEDED (newer recommendation)
```

Recommendations are guidance artefacts. They are never Educational Evidence of understanding.

### State transitions

Recommendation artefact states are advisory-lifecycle states, not journey completion states. Invalid: treating `ACCEPTED` as Topic Complete.

### Educational reasoning

Version 1 missions reduce decision load. Version 2 recommendations must do the same **without** fragmenting learning into disconnected daily topics. Continuation is the default educational stance.

---

## 6. JourneyEvidence

### Purpose

Represent learning evidence **attributed to a Learning Journey** (and usually to a Learning Session), specialising the global Learning Evidence Model rather than forking it.

### Responsibilities

- Attach Evidence Model records to journey and session identity
- Accumulate across sessions for the same topic journey
- Support quality, confidence, and category semantics already defined in [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md)
- Feed Twin updates only through lawful evidence authority gates
- Remain append-only

### Relationships

| Relates to | Cardinality | Meaning |
|------------|-------------|---------|
| Learning Evidence Model types | specialisation | Same catalogue; added journey attribution |
| LearningJourney | N : 1 | Journey-scoped accumulation |
| LearningSession | N : 0..1 | Usually session-scoped |
| LearningObjective | N : 0..1 | Optional objective citation |
| Student Digital Twin | many : 1 | Evidence updates Twin beliefs |

### Ownership

- **Record owner:** Learner educational history
- **Catalogue owner:** Learning Evidence Model
- **Gate owner:** Educational Evidence Authority (understanding claims)
- JourneyEvidence must not invent new mastery maths

### Lifecycle

Created when a qualifying activity/observation occurs during journey work. Never edited in place; corrections are compensating evidence.

### State transitions

Evidence has quality/authority posture (observation vs authorised understanding evidence) per existing EIP documents — not a journey state machine of its own.

### Educational reasoning

Journeys make evidence *about a topic arc* first-class. The Twin still interprets beliefs; the journey still does not mint mastery from completion.

---

## 7. JourneyReflection

### Purpose

Capture the student’s structured reflection after every learning session — what was attempted, what felt clear or unclear, and what should happen next in the journey.

### Responsibilities

- Close the session educationally (required step after session completion)
- Produce soft-signal evidence (Confidence / Engagement categories) without over-claiming mastery
- Inform the next JourneyRecommendation
- Preserve student voice in journey history

### Relationships

| Relates to | Cardinality | Meaning |
|------------|-------------|---------|
| LearningSession | 1 : 1 | One reflection per completed session |
| LearningJourney | N : 1 | Accumulates on the journey |
| JourneyEvidence | 1 : 0..N | Reflection may emit soft evidence records |
| JourneyRecommendation | influences | Next-step advice may cite reflection themes |

### Ownership

- **Author:** Student
- **Recorder (future):** Learning Session Engine
- System must not invent reflection content

### Lifecycle

```
Session COMPLETED → Reflection REQUIRED → Reflection CAPTURED → Session educationally closed
```

Skipping reflection is an invalid educational close in Version 2 principles (implementation may allow deferred capture only under explicit rules — see Open Questions in the completion report).

### State transitions

`PENDING` → `CAPTURED` → (optional) `AMENDED` via compensating note, not silent overwrite.

### Educational reasoning

Reflection converts finished time into educational memory. Without it, multi-session journeys lose the signal that should shape the next session.

---

## 8. JourneyHistory

### Purpose

Provide an immutable, attributable log of material journey events and state transitions for audit, explainability, and Twin/decision replay.

### Responsibilities

- Record journey and session state transitions
- Record recommendation accept/dismiss and completion decisions
- Support “why did the journey move?” narratives
- Enable deterministic recomputation of derived progress where required

### Relationships

| Relates to | Cardinality | Meaning |
|------------|-------------|---------|
| LearningJourney | 1 : 1 | History belongs to one journey |
| All journey entities | references | Events cite sessions, evidence ids, recommendations |

### Ownership

- Append-only system log owned as learner educational history
- Not a student-editable diary (reflections are separate)

### Lifecycle

Begins at journey creation; grows until journey terminal state; retained under continuity rules after plan deletion.

### State transitions

History itself does not transition; it records transitions of other entities.

### Educational reasoning

Explainability and governance require a spine. JourneyHistory is that spine for journey-scoped decisions, complementary to the Twin Evidence Log.

---

## 9. JourneyProgress

### Purpose

Represent **educational progress of the journey** as evidence-aware measures and lawful coverage posture — never as unsupported mastery theatre.

### Responsibilities

- Summarise sessions completed, objectives addressed, evidence density, and time invested
- Distinguish coverage progress from understanding estimates (Twin-owned)
- Support READY_FOR_COMPLETION detection inputs
- Remain recomputable from history + evidence where possible

### Relationships

| Relates to | Cardinality | Meaning |
|------------|-------------|---------|
| LearningJourney | 1 : 1 | Progress posture of the journey |
| JourneyEvidence | derived from | Density and quality feed progress |
| Study Progress (Constitution) | related | Coverage completion remains constitutionally owned |
| Estimated Knowledge / Mastery | distinct | Twin estimates; not renamed JourneyProgress |

### Ownership

- **Derived measures:** Journey Engine
- **Coverage declarations:** Still subject to Study Progress / Constitution rules
- Progress must not silently write Estimated Mastery

### Lifecycle

Updates after session close, evidence arrival, reflection capture, and lawful coverage actions.

### State transitions

Progress is a posture (metrics + flags), not a finite state enum. Flags such as `meets_completion_criteria` may become true and enable `READY_FOR_COMPLETION` on `JourneyState`.

### Educational reasoning

Version 1 risk was narrating coverage or scores as mastery. JourneyProgress exists to make “how far through this topic’s learning path am I?” answerable without lying about competence.

---

## 10. JourneyState

### Purpose

Hold the lifecycle posture of a Learning Journey.

### Responsibilities

- Encode where the journey sits educationally
- Gate lawful transitions (see State Machine)
- Drive recommendation and UI meaning in future milestones
- Separate pause/deferral from completion

### Canonical states

| State | Meaning |
|-------|---------|
| `NOT_STARTED` | Journey exists or is authorised but no meaningful session has begun |
| `ACTIVE` | Student is in an ongoing journey; sessions may run |
| `PAUSED` | Journey intentionally suspended; not abandoned |
| `RESUMED` | Transitional acknowledgement after pause (may collapse to ACTIVE in implementation) |
| `READY_FOR_COMPLETION` | Completion criteria satisfied; awaiting lawful Topic Complete confirmation |
| `COMPLETED` | Topic Complete outcome recorded for this journey |
| `DEFERRED` | Journey postponed with intent to return (distinct from pause of short duration) |
| `ABANDONED` | Explicit end without Topic Complete |

### Ownership

Journey Engine owns transitions; students may request pause/defer/abandon; systems must not auto-complete.

### Lifecycle / transitions

Authoritative detail: [`STATE_MACHINE.md`](STATE_MACHINE.md).

### Educational reasoning

Named states prevent the product from treating “no mission today” as “topic done” or “paused” as “failed.”

---

## 11. SessionState

### Purpose

Hold the lifecycle posture of a Learning Session.

### Responsibilities

- Track start, pause, resume, finish, abandon
- Gate reflection requirement
- Prevent double-completion and silent time inflation

### Canonical states

| State | Meaning |
|-------|---------|
| `NOT_STARTED` | Session planned or recommended but not begun |
| `ACTIVE` | Student is in the session |
| `PAUSED` | Timer/work suspended |
| `COMPLETED` | Session finished; reflection pending or captured |
| `ABANDONED` | Session ended without completion |

`RESUMED` may appear as an event that returns the session to `ACTIVE`.

### Ownership

Learning Session Engine (future); student actions drive transitions.

### Lifecycle / transitions

Authoritative detail: [`STATE_MACHINE.md`](STATE_MACHINE.md).

### Educational reasoning

Session state keeps daily work honest (including pause semantics already explored in LXP-002) while subordinating sessions to journeys.

---

## 12. Topic Complete (Outcome)

Topic Complete is **not** a separate persisted entity in V2-001; it is the educational **outcome** of a journey reaching `COMPLETED` under completion criteria.

### Meaning

- Lawful declaration that the journey’s coverage/completion criteria for the topic are satisfied
- Does **not** mean Estimated Mastery, Exam Ready, or certified knowledge
- May update Study Progress / coverage spine when constitutionally warranted
- Understanding estimates remain Twin-owned and evidence-gated

### Relationship to Version 1 Study Progress

Study Progress answers “have I completed studying this unit?” Journey `COMPLETED` is the Version 2 path that should eventually author that coverage outcome for journey-managed topics — without inventing mastery ([`CURRICULUM_MODEL.md`](CURRICULUM_MODEL.md) completion criteria).

---

## 13. Domain Boundaries (Non-Duplication)

| Existing authority | Journey domain role |
|--------------------|---------------------|
| Curriculum Engine | Topic / objective identity |
| Student Digital Twin | Learner beliefs, readiness, predictions |
| Learning Evidence Model | Evidence catalogue and immutability law |
| Educational State Authority Matrix | Who may mutate which educational states |
| Educational Explainability Standard | How recommendations are narrated |
| Study Plan | Disposable planning constraints and capacity |
| Founder Recommendation Engine | Operational founder advice — not student journeys |

---

## 14. Implementation (V2-002)

The conceptual entities in this document are implemented as a pure domain package:

| Concept | Module |
|---------|--------|
| Package root | `app/domain/learning_journey/` |
| Aggregate | `entities/learning_journey.py` |
| Sessions / objectives / progress / recommendations / reflections / evidence / history | `entities/` |
| JourneyState / SessionState / EffortEstimate / CompletionStatus | `value_objects/` |
| Progress + validation | `services/` |
| Persistence port | `interfaces/learning_journey_repository.py` (contract only) |

Full mapping, non-goals, and test location: [`DOMAIN_IMPLEMENTATION.md`](DOMAIN_IMPLEMENTATION.md).

V2-002 does **not** activate journey runtime behaviour. Engines begin at V2-003.

---

## 15. Closing

These entities are the vocabulary for all Version 2 educational implementation. Engines may add technical fields; they must not invent parallel meanings for Journey, Session, Evidence, Reflection, or Topic Complete.
