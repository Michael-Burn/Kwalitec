# Version 2 Architecture

**Document ID:** V2-001-ARCH  
**Milestone:** V2-001 — Learning Journey Domain Architecture  
**Status:** Authoritative architecture reference  
**Nature:** Documentation only — no runtime behaviour  
**Audience:** Product, engineering, educational governance, AI agents  

**Authority relationships**

| Document | Relationship |
|----------|--------------|
| [`PRODUCT_BLUEPRINT.md`](../../PRODUCT_BLUEPRINT.md) | Product vision; Version 2 evolves the educational model within that vision |
| [`KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) | Highest educational law; Version 2 must not contradict it |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Learner-state authority; journeys feed the Twin — they do not replace it |
| [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md) | Evidence spine; journey evidence specialises it, does not fork it |
| [`VERSION2_PRODUCT_STRATEGY.md`](../product/roadmap/VERSION2_PRODUCT_STRATEGY.md) | Strategic decision framework; this folder is educational architecture |

Companion documents in this folder: [`LEARNING_JOURNEY_DOMAIN.md`](LEARNING_JOURNEY_DOMAIN.md), [`STATE_MACHINE.md`](STATE_MACHINE.md), [`EDUCATIONAL_PRINCIPLES.md`](EDUCATIONAL_PRINCIPLES.md), [`CURRICULUM_MODEL.md`](CURRICULUM_MODEL.md), [`MIGRATION_STRATEGY.md`](MIGRATION_STRATEGY.md), [`VERSION2_ROADMAP.md`](VERSION2_ROADMAP.md).

---

## 1. Purpose

This document defines the high-level educational architecture for Kwalitec Version 2.

Version 2 reframes exam preparation around the **Learning Journey**: a multi-session, evidence-accumulating path through a curriculum topic that ends only when educational completion criteria are met — not when a single daily mission finishes.

This architecture is the blueprint every future Version 2 implementation milestone must follow. It does not change Version 1 production behaviour.

---

## 2. Educational Philosophy

Kwalitec exists to maximise a student’s probability of passing professional examinations in the shortest sustainable time ([`PRODUCT_BLUEPRINT.md`](../../PRODUCT_BLUEPRINT.md)).

Version 1 shipped a trustworthy **structured study platform**: official curriculum, study plan, daily mission, study session, and continuity of coverage history. That spine correctly answered “what should I study next under Learning Mode?”

Version 2 advances the same philosophy into a **journey-native educational model**:

1. **Learning is continuous.** A topic is rarely finished in one sitting. Professional syllabuses demand repeated exposure, practice, reflection, and revision.
2. **Evidence accumulates.** Understanding claims require authorised evidence over time ([`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md); Constitution Article V).
3. **Coverage and understanding remain separate spines.** Completing study coverage is not mastery ([`EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md`](../educational/EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md)).
4. **Recommendations continue work already in progress.** They do not thrash the student onto a new topic without educational justification.
5. **Explainability is mandatory.** Every journey recommendation must answer the four-question framework ([`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md)).
6. **The Digital Twin remains learner-state authority.** Journeys produce evidence and progress; the Twin interprets learner state ([`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)).

The product thesis is unchanged: **reduce decisions, increase learning.** Version 2 changes *what* is being decided — from “which isolated session today?” to “how does today’s session advance the active journey?”

---

## 3. Why Learning Journeys Replace Isolated Study Sessions

### 3.1 Version 1 model (as shipped)

```
Study Plan
    ↓
Daily Mission
    ↓
Study Session
```

This model assumes that educational progress can be adequately represented as a sequence of bounded daily work items. It is correct for **coverage sequencing** under Learning Mode. It is incomplete for **topic competence**, because:

- one session rarely saturates a professional topic;
- revision is treated as a parallel concern rather than journey continuation;
- mission completion can be misread (by students or systems) as topic completion;
- evidence density across days is not first-class in the planning object model.

### 3.2 Version 2 model

```
Curriculum
    ↓
Subject
    ↓
Chapter
    ↓
Topic
    ↓
Learning Journey
    ↓
Learning Sessions
    ↓
Evidence
    ↓
Reflection
    ↓
Recommendation
    ↓
Topic Complete
```

A **Learning Journey** is the educational unit of work for a topic. It may span multiple learning sessions over multiple days. **Topic Complete** is an outcome of the journey under explicit completion criteria — never an automatic side-effect of finishing one session.

Study sessions remain real and valuable. They become **steps inside a journey**, not the container of topic meaning.

### 3.3 What is gained

| Concern | Version 1 limitation | Version 2 improvement |
|---------|----------------------|------------------------|
| Topic duration | Implicitly session-sized | Explicit multi-session journey |
| Continuity | Plan/mission regenerate; topic story is thin | Journey state persists across days |
| Evidence | Exists globally; weakly bound to topic arc | Accumulates on the journey |
| Reflection | Optional / session-local | Required after every learning session |
| Revision | Separate workspace / future mode | Part of the same journey lifecycle |
| Recommendations | Can feel like topic replacement | Continue or adjust the active journey |
| Completion | Mission complete ≠ topic complete (law), but UX conflation risk | Topic Complete is a named journey outcome |

---

## 4. Relationship to Version 1

Version 2 **evolves** Version 1; it does not rewrite or invalidate it.

| Version 1 artefact | Version 2 evolution | Continuity rule |
|--------------------|---------------------|-----------------|
| Study Plan | Planning context + journey portfolio constraints | Remains disposable container; learner history survives ([`EDUCATIONAL_CONTINUITY_STANDARD.md`](../educational/EDUCATIONAL_CONTINUITY_STANDARD.md)) |
| Daily Mission | Journey Recommendation (daily commitment derived from journeys) | Learning Mode authority preserved until Mission Engine 2.0 lawfully supersedes it |
| Study Session | Learning Session | Same bounded work block; richer journey attribution |
| Study Progress | JourneyProgress + Topic Complete criteria | Coverage honesty preserved; completion criteria become explicit |
| Current Learning Topic | Active Learning Journey pointer | Still syllabus-order subordinate under Learning Mode |
| Student Digital Twin | Twin 2.0 consumes journey evidence | Twin remains sole learner-state authority |
| Learning Evidence Model | JourneyEvidence specialises attribution | Append-only evidence law unchanged |
| Curriculum V1 flat / V2 hierarchical (engine) | Subject / Chapter educational framing | ADR-003 coexistence preserved; no syllabus rewrite |

**Non-regression:** Until an implementation milestone explicitly activates Version 2 behaviour behind a governed cutover, Version 1 Learning Mode, missions, sessions, and continuity rules remain the live educational path. This documentation milestone changes nothing at runtime.

Detailed mapping: [`MIGRATION_STRATEGY.md`](MIGRATION_STRATEGY.md).

---

## 5. Architectural Goals

1. **Establish Learning Journey as the central educational concept** for Version 2 design and implementation.
2. **Make multi-session topic learning first-class** in domain language, state machines, and completion criteria.
3. **Bind evidence, reflection, and recommendation to journeys** so educational decisions are attributable.
4. **Preserve constitutional spines** — coverage vs understanding; observed facts vs estimates vs advice.
5. **Keep curriculum as syllabus truth** — journeys never invent topics ([ADR-003](../architecture/ADR-003-curriculum-v1-v2.md), [ADR-004](../architecture/ADR-004-canonical-topic-traversal.md)).
6. **Keep the Twin as learner-state truth** — journeys write evidence and progress; they do not become a competing Twin.
7. **Enable deterministic, explainable engines** — same journey state + same evidence → same core recommendations.
8. **Support sustainable intensity** — pause, resume, and effort estimation are educational controls, not engagement theatre.
9. **Provide a migration path** from Study Plan / Mission / Session without silent educational discontinuity.
10. **Sequence implementation** so each roadmap milestone can be derived from this folder without redefining concepts ([`VERSION2_ROADMAP.md`](VERSION2_ROADMAP.md)).

---

## 6. Non-Goals

This Version 2 architecture (and V2-001 specifically) does **not**:

- change production behaviour, UI, CSS, Flask routes, or feature flags;
- introduce SQLAlchemy models, migrations, services, repositories, or APIs;
- replace the Educational Constitution or amend it by stealth;
- replace the Student Digital Twin with journey state;
- replace the Learning Evidence Model with a parallel evidence store;
- invent black-box LLM ownership of recommendations or mastery;
- reproduce copyrighted syllabus text or proprietary exam materials;
- force a hard cutover that breaks Version 1 learners;
- treat Topic Complete as Estimated Mastery or Exam Ready;
- gamify journeys with streaks, badges, or engagement-first metrics;
- redefine Founder Operational State as educational authority.

---

## 7. System Context (Conceptual)

```
┌─────────────────────────────────────────────────────────────────┐
│                     Official Curriculum                          │
│              (Subject → Chapter → Topic → Objectives)            │
└───────────────────────────────┬─────────────────────────────────┘
                                │ references
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Learning Journey                            │
│   state · progress · objectives · history · completion criteria  │
└───────┬─────────────────┬──────────────────┬────────────────────┘
        │                 │                  │
        ▼                 ▼                  ▼
 Learning Session   JourneyEvidence   JourneyReflection
        │                 │                  │
        └────────┬────────┴────────┬─────────┘
                 ▼                 ▼
         JourneyRecommendation   Topic Complete?
                 │                 │
                 ▼                 ▼
         Daily commitment     Coverage / journey outcome
                 │
                 ▼
        Student Digital Twin (beliefs, readiness, predictions)
```

Layering for future implementation remains:

```
Templates/JS → Blueprints → Services → Models + Curriculum Engine → DB/JSON
```

Journey math belongs in services; curriculum identity belongs in the Curriculum Engine; HTTP remains thin ([`ARCHITECTURE.md`](../../ARCHITECTURE.md)).

---

## 8. Design Invariants

1. **One active learning journey focus under Learning Mode** — recommendations may advise other work; they must not silently replace the authorised focus (Constitution Article VI; Explainability Standard).
2. **A learning session never implies Topic Complete.**
3. **Evidence is append-only**; journey progress is derived or lawfully declared, not rewritten history.
4. **Reflection is part of the session lifecycle**, not an optional garnish.
5. **Revision sessions are journey sessions** with a revision intent — not a disconnected product island.
6. **V1 and V2 curriculum formats remain loadable** until an explicit retirement milestone.
7. **Determinism over theatre** for core journey transitions and recommendations.
8. **Documentation in `knowledge/version2/` is authoritative** for Version 2 educational concepts; implementation must cite it rather than invent synonyms.

---

## 9. Open Architecture Boundaries

Resolved in companion docs; deferred to later milestones:

| Boundary | Owning doc / milestone |
|----------|------------------------|
| Entity definitions | [`LEARNING_JOURNEY_DOMAIN.md`](LEARNING_JOURNEY_DOMAIN.md) |
| State transitions | [`STATE_MACHINE.md`](STATE_MACHINE.md) |
| Educational rules | [`EDUCATIONAL_PRINCIPLES.md`](EDUCATIONAL_PRINCIPLES.md) |
| Structural curriculum framing | [`CURRICULUM_MODEL.md`](CURRICULUM_MODEL.md) |
| V1 → V2 concept mapping | [`MIGRATION_STRATEGY.md`](MIGRATION_STRATEGY.md) |
| Learning Journey domain package | V2-002 ([`DOMAIN_IMPLEMENTATION.md`](DOMAIN_IMPLEMENTATION.md); `app/domain/learning_journey/`) |
| Curriculum graph persistence | Parallel / follow-on (topic ids via Curriculum Engine meanwhile) |
| Journey engine runtime | V2-003 ([LEARNING_JOURNEY_ENGINE.md](LEARNING_JOURNEY_ENGINE.md)) |
| Mission Engine 2.0 | V2-004 |
| Session engine | V2-005 |
| Twin 2.0 | V2-006 |

---

## 10. Closing

Version 2 architecture makes the Learning Journey the educational centre of gravity while preserving Version 1’s hard-won integrity: curriculum-first ordering, evidence before opinion, explainability, continuity, and Twin authority.

Future milestones implement this blueprint. They must not redefine what a Learning Journey is.
