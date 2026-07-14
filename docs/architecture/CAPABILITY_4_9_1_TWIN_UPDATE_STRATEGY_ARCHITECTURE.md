# Capability 4.9.1 — Twin Update Strategy Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 4 — Educational Intelligence Evolution (Internal Alpha active)  
**Capability:** 4.9.1 Twin Update Strategy Architecture (sole architectural authority permitted to evolve a Digital Twin from Educational Evidence)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Upstream Educational Evidence:** [`CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md)  
**Upstream Evidence → Twin mapping:** [`CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md`](CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md)  
**Upstream Student Calibration:** [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md)  
**Upstream Twin Persistence:** [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md)  
**Upstream Twin retrieval:** [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md)  
**Scope:** Structural architecture for Twin Update Strategies as educational-state authors of immutable successor Twins — **no code, algorithms, Flask, ORM, persistence schemas, product flows, UI, Educational Intelligence reasoning, or tests**

---

## Document purpose

Capability 4.8 completed Educational Evidence as a first-class capability:

- Architecture  
- Analysis  
- Product Flow  
- Contract  
- Twin Mapping  

Educational Evidence is now fully specified as **immutable educational observation**. Educational Evidence never updates the Digital Twin.

The next architectural capability defines **how immutable successor Twins are authored**.

That authorship has a hard educational law:

> **Educational Evidence records observations. Observations are not educational state. Digital Twins represent educational state. Twin Update Strategies transform observations into successor educational state.**

**Governing principle (binding):**

> **Twin Update Strategies are the sole architectural authority permitted to evolve a Digital Twin from Educational Evidence. They interpret. They never mutate existing Twins. They never recommend.**

**Architectural restatement:**

> **Strategies consume Current Twin + Educational Evidence and produce a complete immutable Successor Twin. Twin Repository stores. Twin Provider retrieves. Educational Intelligence consumes. Educational Intelligence never authors Twins. Twin Update Strategies never produce recommendations.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Twin Update Strategy** | Lawful interpreter of Educational Evidence that authors a complete immutable successor Twin (or declines change while preserving honesty) |
| **Twin Update Pipeline** | Coordinator that invokes registered Strategies; does not embed educational interpretation algorithms |
| **Educational Evidence** | Immutable educational observation (Capability 4.8) — sole lawful evolution input after birth |
| **Current Twin** | Latest lawful immutable Digital Twin snapshot for the student / sitting scope |
| **Successor Twin** | New complete immutable Twin snapshot authored by Strategies — never an in-place edit |
| **Candidate observation** | Evidence → Twin mapping affinity (Capability 4.8.5) — not a belief write |
| **Educational Intelligence** | Read path: Readiness → Decision → Recommendation → Mission — consumes Twins; never authors them from Evidence |
| **Student Calibration** | Birth Twin prior construction — not Evidence-driven succession |

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Belief-update algorithms, scoring formulas, BKT, forgetting curves, or numeric engines  
- Flask routes, forms, templates, or product UX flows  
- Database schemas, Alembic migrations, ORM models, or Strategy persistence technology  
- Twin Update Pipeline implementation or Strategy registration code  
- Redesign of Educational Evidence, Calibration, Twin Persistence, TwinProvider, or Educational Intelligence domains  
- Recommendation, readiness, decision, mission, or dashboard logic  

---

# 1. Purpose

## 1.1 Why Twin Update Strategies exist

Without Twin Update Strategies as a first-class architectural authority:

- Educational Evidence would be pressured to “apply itself” to Twin fields — collapsing observation into mutation.  
- Educational Intelligence would be pressured to rewrite Twin state while judging preparedness or selecting next actions — collapsing write and read.  
- Product surfaces would invent partial patches, mastery grants from mission ticks, or dashboard-driven belief edits.  
- Twin immutability would become theatre: “snapshots” that are secretly mutable bags of fields.  
- Educational honesty would fail — observations would masquerade as conclusions inside the Twin without an accountable interpreter.

**Twin Update Strategies** exist to:

1. **Separate observation from interpretation** — Evidence observes; Strategies interpret.  
2. **Separate interpretation from recommendation** — Strategies author educational *state*; Educational Intelligence judges and recommends from that state.  
3. **Preserve Digital Twin immutability** — evolution is succession of complete snapshots, never in-place mutation.  
4. **Make Twin evolution educationally traceable** — successor Twins are attributable to Evidence interpreted under named Strategies.  
5. **Protect Educational Intelligence honesty** — Intelligence consumes Twins; it never owns Evidence → belief authorship.

It is the lawful answer to:

> “Given what we *observed* and what we currently *believe*, what successor educational state is honestly warranted?”

It is **not** the answer to:

> “What educational observation was recorded?”  
> “What should the student do next?”  
> “How ready are they for the exam?”  
> “What mission should we package?”

```
Educational Evidence records observations.
              ↓
Observations are not educational state.
              ↓
Digital Twins represent educational state.
              ↓
Twin Update Strategies transform observations
into successor educational state.              ← this document
              ↓
Educational Intelligence never authors Twins.
Twin Update Strategies never produce recommendations.
```

## 1.2 Relationship with completed companions

| Concern | Owner |
|---|---|
| Birth Twin from self-declared history | **Student Calibration** (Capability 3.6) |
| Immutable educational observations after birth | **Educational Evidence** (Capability 4.8) |
| Candidate observation domain affinities | **Evidence → Twin Mapping** (Capability 4.8.5) |
| Interpretation of Evidence into successor Twins | **Twin Update Strategies** (this document) |
| Durable storage of Twin snapshots | **Twin Persistence / Twin Repository** (Capability 3.7) |
| Retrieval of current Twin or honest absence | **Twin Provider** (Capability 3.3) |
| Educational judgement from Twin state | **Educational Intelligence** |

**Rules:**

1. **Calibration births; Evidence observes; Strategies evolve.**  
2. **Evidence never edits a Twin.** Strategies author successors.  
3. **Intelligence never updates educational state.** Strategies never recommend.  
4. **Mapping places candidates; Strategies decide influence.** Not every candidate densifies belief.  
5. **Repository stores; Provider retrieves; Intelligence consumes.** Only Strategies author successor Twins from Evidence.

Governing restatement:

> **Evidence observes. Strategies interpret. Twins remember educational state. Intelligence judges. Those verbs do not commute.**

---

# 2. Educational philosophy

These principles bind Twin Update Strategies for Version 1.0. They extend ADR-002’s write/read separation, Twin immutability law, Educational Evidence observation law, and Calibration honesty into Evidence-driven succession.

### Strategies interpret

Twin Update Strategies are the educational interpreters of Evidence. They decide whether candidate observations warrant successor belief change — and how much honesty requires leaving state unchanged.

### Evidence observes

Educational Evidence remains observational only. Strategies must not rewrite Evidence history, invent missing Evidence, or treat Evidence payloads as already-concluded mastery, readiness, or recommendations.

### Twins remember educational state

The Digital Twin is authoritative learner-state memory. Strategies author what the platform *believes* educationally after interpretation. Observation history remains Evidence’s spine; state memory remains the Twin’s.

### Strategies author new immutable Twins

Evolution means producing a **new** complete Twin snapshot. The prior Twin remains historically true as what the product believed before.

### Strategies never mutate existing Twins

In-place field edits, partial patches, and silent domain overwrites are forbidden. Mutation of a stored snapshot is architectural failure — not “efficient update.”

### Unknown educational state remains unknown

Sparse Evidence does not authorise Mid beliefs, invented coverage, or false density. Empty domains that remain unwarranted stay empty. Unknown is honesty; false certainty is pathology.

### Strategies should be conservative

Prefer under-claiming educational change over over-claiming. A single mission completion, short session, or thin reflection must not become aggressive mastery or readiness theatre inside Strategy authorship.

### Educational honesty is preferred over false certainty

When Evidence is weak, conflicting, self-declared (thin warrant), or insufficient for a domain, Strategies leave beliefs honest rather than “completing” the Twin for product comfort.

Governing restatement:

> **Interpret conservatively. Author wholly. Never mutate. Prefer unknown over invented certainty.**

---

# 3. Ownership

## 3.1 Ownership chain (binding)

```
Educational Evidence
        ↓
Twin Update Strategy
        ↓
Successor Twin
        ↓
Twin Repository
        ↓
Twin Provider
        ↓
Educational Intelligence
```

| Stage | Owns | Does not own |
|---|---|---|
| **Educational Evidence** | Immutable educational observations | Twin snapshots; Strategy interpretation; recommendations |
| **Twin Update Strategy** | Interpretation of Current Twin + Evidence into successor Twin authorship | Evidence content; Persistence technology; Educational Intelligence selection |
| **Successor Twin** | Authoritative learner-state snapshot after interpretation | Evidence log ownership; next-action authority |
| **Twin Repository** | Durable store / load of immutable Twin snapshots | Twin authorship; educational interpretation |
| **Twin Provider** | Retrieval of current Twin or honest absence for product read paths | Twin fabrication; Evidence consumption as Twin substitute |
| **Educational Intelligence** | Judgement from Twin (Readiness → Decision → Recommendation → Mission) | Twin authorship from Evidence; Evidence ownership |

## 3.2 Clarifications (binding)

| Role | Verb |
|---|---|
| **Repository** | **Stores** |
| **Provider** | **Retrieves** |
| **Educational Intelligence** | **Consumes** |
| **Twin Update Strategies** | **Author** successor Twins |

Only Twin Update Strategies author successor Twins from Educational Evidence.

Student Calibration remains the sole lawful author of Birth Twins (priors). Re-calibration and Calibration corrections remain Calibration events — not Evidence→Strategy disguised birth.

## 3.3 Twin Update Strategies own

| Responsibility | Meaning |
|---|---|
| **Educational interpretation** | Decide what Current Twin + Evidence warrant as successor educational state. |
| **Whole Twin authorship** | Emit a complete immutable Successor Twin (or an explicit no-change successor equivalent that preserves immutability discipline). |
| **Domain-scoped interpretation** | Each Strategy owns its domain’s interpretive responsibility (Knowledge, Performance, Behaviour, Memory, Goals, …) without owning neighbouring domains’ meaning. |
| **Traceability posture** | Successor Twin lineage must remain attributable to the Evidence that justified succession. |
| **Conservative honesty** | Refuse false certainty; preserve unknown / thin-warrant posture when Evidence does not warrant densification. |
| **Immutability discipline** | Never mutate Current Twin; always succeed by succession. |

## 3.4 Twin Update Strategies never own

| Forbidden ownership | Why |
|---|---|
| **Educational Evidence content** | Evidence remains independent observational memory. |
| **Twin Persistence policy** | Repository stores what Strategies author; Strategies do not become storage adapters. |
| **Twin retrieval honesty** | Provider retrieve-or-absent remains Application read-path law. |
| **Readiness / Decision / Recommendation / Mission** | Educational Intelligence judgements remain downstream of Twin. |
| **Dashboard / UI decisions** | Product surfaces display consequences; they do not author educational state. |
| **Curriculum invention** | Syllabus truth remains Curriculum Engine / `CurriculumService`. |
| **Calibration prior fabrication** | Birth priors remain Calibration; Strategies must not silently rebrand priors as Evidence-backed by Evidence arrival alone without explicit warrant change. |

### Owner map (no duplication)

| Concept | Layer | Relation to Twin Update Strategies |
|---|---|---|
| **Educational Evidence** | Domain / educational memory | Sole post-birth Twin-evolution *input* |
| **Evidence → Twin Mapping** | Architecture | Candidate affinities only; stops before Strategy interpretation |
| **Twin Update Strategies** | Domain | Sole Evidence interpreters → successor Twin authors (this document) |
| **Twin Update Pipeline** | Domain | Coordinates Strategy invocation; does not embed interpretation math |
| **Twin Repository** | Application | Stores successor snapshots — never authors them |
| **Twin Provider** | Application | Retrieves Twin; never invents successors from Evidence |
| **Student Calibration** | Application | Birth Twin only; not Evidence-driven succession |
| **Educational Orchestrator** | Application | Composes Intelligence from Twin; never runs Strategy authorship on dashboard read path |
| **Educational Intelligence Domains** | Domain | Consume Twins; never write Twin beliefs from activity or Evidence bypass |

### Ownership invariants

1. **Only Twin Update Strategies author successor Twins from Educational Evidence.**  
2. **Repository stores. Provider retrieves. Educational Intelligence consumes.**  
3. **Educational Intelligence never owns Twin authorship.**  
4. **Strategies never own recommendation or readiness.**  
5. **Evidence never owns Twin mutation.**  
6. **Calibration never becomes a second Evidence→Strategy path by seeding fake Evidence.**

Governing restatement:

> **Strategies answer only: “What successor educational state is warranted?” They never answer what was observed, where the Twin is stored, or what the student should do next.**

---

# 4. Inputs

## 4.1 Closed input set (binding)

Twin Update Strategies consume:

| Input | Meaning |
|---|---|
| **Current Twin** | The latest lawful immutable Digital Twin snapshot for the authorised student / sitting scope. |
| **Educational Evidence** | Immutable educational observation(s) entering through the Evidence boundary only. |

**Nothing else.**

## 4.2 Forbidden inputs (must not be Strategy authority)

| Forbidden input | Why |
|---|---|
| **Dashboard state / analytics aggregates** | Product mirrors; not educational-state authorship authority |
| **Routes / HTTP / session globals** | Framework coupling; Presentation is not educational truth |
| **Recommendation history as Twin-write authority** | Recommendation artefacts are Intelligence outputs; accept/dismiss may become Evidence later — Strategies then consume *Evidence*, not Recommendation stores |
| **Missions directly** | Missions are operational consequences; mission outcomes become Evidence observations first |
| **Raw student activity streams** | Activity is transient; Evidence is the sole Twin-evolution input after birth |
| **Readiness / Decision / Mission payloads as belief writers** | Read path must not silently reopen write path |
| **Calibration declarations as Evidence substitutes** | Calibration remains priors; not Evidence densification |

## 4.3 Evidence boundary law

Evidence enters Strategy authorship **only through the Educational Evidence boundary**.

```
Student activity / mission events / sessions
              ↓
   Educational Evidence boundary
              ↓
   Educational Evidence (immutable observation)
              ↓
   Twin Update Strategy   (+ Current Twin)
```

Strategies must not:

- read mission tables as silent Twin writers;  
- treat UI clicks as Evidence;  
- invent Evidence from dashboard pressure;  
- consume Orchestrator Experience payloads as Twin-evolution authority.

### Input invariant

> **Current Twin + Educational Evidence. Nothing else. Evidence enters through the Evidence boundary only.**

---

# 5. Outputs

## 5.1 Primary output (binding)

| Output | Meaning |
|---|---|
| **Complete immutable successor Digital Twin** | A whole Twin aggregate representing post-interpretation educational state for the scope. |

## 5.2 What Strategies produce

- A **complete** Twin — all domains present as lawful Twin structure (including domains intentionally left empty / unchanged).  
- An **immutable** Twin — not a mutable working object intended for later patching.  
- A **successor** Twin — new snapshot identity / succession posture relative to Current Twin.  
- Traceable lineage posture — successor beliefs remain attributable to interpreted Evidence (architecturally, not as a schema mandate here).

## 5.3 What Strategies must never produce

| Forbidden output | Why |
|---|---|
| **Partial updates** | Breaks snapshot integrity; invites hybrid Twins |
| **Patches / field edits** | In-place mutation path; destroys immutability |
| **Domain slices without whole Twin** | Encourages Repository merges Strategies must not author |
| **Recommendations** | Belongs to Recommendation Engine / Decision packaging |
| **Mission decisions** | Belongs to Mission Intelligence |
| **Readiness bands / overall preparedness %** | Belongs to Readiness Aggregation |
| **Pass probability / predicted marks** | Belongs to Predictions / later forecasting consumers |
| **Evidence rewrite** | Evidence remains append-only observational memory |

## 5.4 Prior Twin remains unchanged

| Rule | Meaning |
|---|---|
| **No mutation of Current Twin** | Strategies read Current Twin; they do not edit it. |
| **History retained** | Prior Twin remains valid history of past educational belief. |
| **Repository receives successor** | Persistence stores the new snapshot as current under replace-by-snapshot law (Capability 3.7.1). |
| **No-change is still succession discipline** | If Evidence warrants no domain change, the architecture still forbids partial mutation theatre — honesty may yield an unchanged educational meaning expressed without mutating the prior snapshot’s identity in place. |

### Output invariant

> **Strategies produce a complete immutable successor Digital Twin. Not patches. Not recommendations. The previous Twin remains unchanged.**

---

# 6. Strategy independence

## 6.1 Why multiple strategies may exist

Educational state is multi-dimensional. Knowledge, Performance, Behaviour, Memory, and Goals answer different educational questions. Collapsing them into one god-strategy:

- couples unrelated interpretation math;  
- encourages cross-domain smuggling (e.g. Behaviour grant of mastery);  
- makes conservative Version 1.0 impossible without freezing everything;  
- blocks independent deepening of belief engines later.

Multiple Twin Update Strategies exist so each domain can evolve **independently in educational responsibility** while still contributing to one successor Twin under Pipeline coordination.

## 6.2 Named independent strategies (architectural catalogue)

| Strategy | Educational question it may interpret toward | Must not absorb |
|---|---|---|
| **Knowledge Update Strategy** | What can the student do now (belief)? | Memory retention curves as mastery; Behaviour completion as mastery |
| **Performance Update Strategy** | How does the student perform when assessed / under practice conditions? | Second Knowledge mastery store; pass-probability engine |
| **Behaviour Update Strategy** | How does the student actually study? | Learning / mastery grants; readiness composites |
| **Memory Update Strategy** | What educational history / retention posture is warranted? | Knowledge mastery fill; forecast-as-Memory-truth |
| **Goal Update Strategy** | How do declared / warranted Goals evolve when Evidence and Twin require explicit goal succession? | Decision selection; readiness theatre; Identity rewrite from session noise |

Additional separable strategies (e.g. Confidence when separable) remain future domain ownership — not required ownership of Version 1.0 Strategy catalogue completeness.

## 6.3 Version 1.0 subset posture

Version 1.0 may implement **only a subset** of the catalogue.

Architecture requires:

1. **Independent evolution** — deepening Knowledge later must not force Behaviour redesign.  
2. **Single responsibility** — each Strategy owns one educational interpretation concern.  
3. **Composable succession** — Pipeline coordination may compose Strategy contributions into one successor Twin without Strategies calling each other’s belief engines.  
4. **No god-strategy** — Version 1.0 must not “temporarily” put all interpretation in one module that later cannot be split without Twin redesign.

## 6.4 Independence invariants

1. **Strategies do not own each other’s domains.**  
2. **Strategies do not recommend.**  
3. **Strategies do not persist.**  
4. **Strategies do not consume raw activity.**  
5. **Absence of a Strategy for a domain does not license Intelligence or Persistence to invent that domain’s beliefs.**

Governing restatement:

> **Many Strategies. One successor Twin. Independent educational responsibilities. Shared immutability law.**

---

# 7. Relationship with Educational Intelligence

## 7.1 Consumption chain (binding)

```
Twin Update Strategies
        ↓
produce successor Twin
        ↓
Twin Repository stores
        ↓
Twin Provider retrieves
        ↓
Educational Intelligence consumes successor Twin
```

## 7.2 Firewall (binding)

| Layer | May | Must never |
|---|---|---|
| **Twin Update Strategies** | Interpret Evidence; author successor Twin | Recommend; select missions; compute readiness bands as product authority; mutate Current Twin |
| **Educational Intelligence** | Consume Twin; aggregate readiness; select next action; package recommendations; compose missions | Update educational state from Evidence or activity; bypass Twin via Evidence shortcuts; author successor Twins |

## 7.3 Write path vs read path (preserved from ADR-002)

```
WRITE path (evolution):
  Educational Evidence → Twin Update Strategies → Successor Twin → Twin Repository

READ path (guidance):
  Twin Repository → Twin Provider → Educational Intelligence
  (Readiness → Decision → Recommendation → Mission)
```

**Rules:**

1. **Educational Intelligence never updates educational state.**  
2. **Twin Update Strategies never recommend.**  
3. **Read-side accept/dismiss and mission completion become Evidence** (when recorded) — then Strategies may interpret; Intelligence must not write Twin beliefs as a side effect of selection.  
4. **Strategies write. Intelligence reads.** Crossing the firewall recreates planner pathology.

### Relationship invariant

> **Strategies produce successor Twin. Educational Intelligence consumes successor Twin. Intelligence never updates educational state. Strategies never recommend.**

---

# 8. Educational boundaries

Twin Update Strategies remain **educational state authors only**. Version 1.0 architecture forbids the following inside Strategy ownership:

| Boundary | Forbidden inside Twin Update Strategies |
|---|---|
| **No recommendation generation** | Strategies must not select next actions or package Recommendation artefacts |
| **No mission generation** | Missions remain Mission Intelligence consequences |
| **No dashboard decisions** | Analytics / dashboard composition must not drive Strategy outputs or act as Strategy inputs |
| **No readiness engine** | Preparedness bands and overall readiness % remain Readiness Aggregation |
| **No prediction engine** | Pass probability, predicted marks, and forecast snapshots remain Predictions / later forecasting |
| **No pass probability** | Strategies may update Performance / Knowledge *state*; they must not emit exam-pass forecasts as Strategy authority |
| **No UI** | Forms, templates, routes, and engagement theatre are not Strategy concerns |
| **No Evidence authorship** | Strategies interpret Evidence; they do not invent observational history |
| **No Calibration substitution** | Strategies do not birth Twins from declarations or re-seed priors as Evidence |

### Boundary invariant

> **Twin Update Strategies remain educational state authors only. Observation stays in Evidence. Judgement stays in Intelligence. Presentation stays in product surfaces.**

---

# 9. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **Evidence interpreted twice** | Intelligence and Strategies both “interpret” the same Evidence into competing truths | Write/read firewall: Strategies interpret → Twin; Intelligence consumes Twin only |
| **Educational Intelligence updating Twins** | Readiness/Decision/Mission paths silently rewrite Twin domains | Hard ban: Intelligence never authors Twins; only Strategies (and Calibration at birth) author |
| **Strategies mutating Twins** | In-place field patches; Repository upsert of domain slices | Whole immutable successor Twins only; replace-by-snapshot Persistence law |
| **Strategy coupling** | Knowledge Strategy invents Behaviour; Behaviour Strategy grants mastery | Single-responsibility Strategies; Pipeline composition without cross-domain god logic |
| **Over-aggressive interpretation** | Mission completed ⇒ Mid mastery / High readiness theatre | Conservative Version 1.0 philosophy; thin warrant; unknown remains unknown |
| **Premature certainty** | Sparse Evidence densified to look “product complete” | Honesty over completeness; empty domains remain lawful |
| **Strategy ownership leakage** | Strategies emit recommendations, readiness %, or mission choices “for convenience” | Closed output law: successor Twin only |
| **Activity bypass** | Strategies read missions/sessions directly without Evidence | Evidence boundary only; activity → Evidence → Strategies |
| **Partial Twin authorship** | Strategies emit Knowledge-only fragments; Persistence merges hybrids | Complete successor Twin required; no field merges across authors |
| **Mapping confused with Strategies** | Candidate observation placement treated as belief write | Capability 4.8.5 stops before interpretation; this document begins interpretation authority without implementing algorithms |

### Risk restatement

The primary danger is not missing Strategy algorithms. It is **Strategies that start recommending**, **Intelligence that starts updating Twins**, or **Evidence that is interpreted on both write and read paths** — recreating study-planner pathology inside Educational Intelligence Evolution.

---

# 10. Version 1.0 recommendations

## 10.1 Binding Version 1.0 recommendations

| Recommendation | Meaning |
|---|---|
| **Small strategies** | Prefer focused domain Strategies over a single interpreter god-module |
| **Single responsibility** | Each Strategy owns one educational interpretation concern |
| **Immutable successor Twins** | Evolution is succession only — never in-place mutation |
| **Whole Twin authoring** | Strategies (via Pipeline coordination) produce complete Twin snapshots |
| **Traceability** | Successor Twin changes remain attributable to interpreted Evidence |
| **Future composability** | Version 1.0 Strategy subset must not require Twin redesign when additional Strategies or richer update mathematics arrive |

## 10.2 Future mathematics without redesign

Future update mathematics (richer Knowledge beliefs, retention models, Performance scoring, Confidence separability) must:

1. **Live inside Strategy ownership boundaries** already named here.  
2. **Continue to consume only Current Twin + Educational Evidence.**  
3. **Continue to emit complete immutable successor Twins.**  
4. **Leave Educational Intelligence as Twin consumer only.**  
5. **Leave Evidence observational** — deeper math must not move conclusions into Evidence payloads.

Version 1.0 architecture succeeds when later belief engines plug into Strategies **without** redesigning Evidence, Twin immutability, Persistence replace-by-snapshot law, Provider honesty, or Intelligence read-path ownership.

## 10.3 Version 1.0 success criteria (architectural)

Version 1.0 succeeds when:

1. Twin Update Strategies are recognised as the sole Evidence → Twin evolution authors.  
2. Current Twin + Educational Evidence are the only Strategy inputs.  
3. Complete immutable successor Twins are the only Strategy outputs.  
4. Educational Intelligence never updates educational state.  
5. Strategies never recommend, generate missions, or run readiness/prediction engines.  
6. Multiple Strategies may evolve independently; Version 1.0 may ship a subset.  
7. Future update mathematics requires no architectural redesign of this ownership model.

Governing restatement:

> **Small. Responsible. Immutable. Whole. Traceable. Composable. Future math should deepen Strategies — not redesign Twin law.**

---

# 11. Architecture Compliance Summary

| Invariant | Status under this architecture |
|---|---|
| Twin evolves from Educational Evidence only (after birth) | Required — Strategies are sole interpreters |
| Twin snapshots remain immutable; succession only | Required |
| Strategies consume Current Twin + Evidence only | Required |
| Strategies produce complete successor Twin only | Required |
| Educational Intelligence consumes Twins; never authors from Evidence | Preserved |
| Strategies never recommend / ready / predict / missionise | Required |
| Repository stores; Provider retrieves; Intelligence consumes | Preserved |
| Calibration ≠ Evidence-driven succession | Preserved |
| Evidence → Twin Mapping stops before Strategy interpretation | Preserved |
| Curriculum V1/V2 identity safety for topic-scoped succession | Required |
| No Flask / ORM / algorithms / persistence / Intelligence redesign in this milestone | Honoured — architecture only |

---

# 12. STOP

This document defines **Twin Update Strategy architecture only**.

It does **not** authorise:

- Implementation  
- Algorithms or belief-update mathematics  
- Flask routes or services  
- ORM models, schemas, or migrations  
- Twin Update Pipeline code  
- Persistence of Strategies or Twins  
- Product flows, dashboards, or UI  
- Educational Intelligence redesign  
- Educational Evidence redesign  

**STOP.**

---

# References

| Artefact | Role |
|---|---|
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Governing ADR; write/read separation; Evidence → Twin → Intelligence |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Platform educational chain; Update Strategy ownership |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Canonical Twin domain law; immutable snapshots |
| [`CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md) | Evidence observes; never updates Twin |
| [`CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md`](CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md) | Candidate observations; stops before Strategy interpretation |
| [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md) | Birth Twin priors; not Evidence-driven succession |
| [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md) | Repository stores immutable Twin snapshots |
| [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md) | Provider retrieves Twin or honest absence |
| [`CAPABILITY_2_5_BEHAVIOUR_UPDATE_STRATEGY.md`](CAPABILITY_2_5_BEHAVIOUR_UPDATE_STRATEGY.md) | Domain Strategy precedent (Behaviour) |
| [`CAPABILITY_2_6_PERFORMANCE_UPDATE_STRATEGY.md`](CAPABILITY_2_6_PERFORMANCE_UPDATE_STRATEGY.md) | Domain Strategy precedent (Performance) |
| [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md) | Epic 0 Evidence catalogue companion |
| [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md) | Shared educational vocabulary |
