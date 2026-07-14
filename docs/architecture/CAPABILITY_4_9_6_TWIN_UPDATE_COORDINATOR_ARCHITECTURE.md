# Capability 4.9.6 — Twin Update Coordinator Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 4 — Educational Intelligence Evolution (Internal Alpha active)  
**Capability:** 4.9.6 Twin Update Coordinator Architecture (Application Layer orchestrator for the Twin write-side pipeline)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Read-path sibling:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
**Upstream Strategy architecture:** [`CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md`](CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md)  
**Upstream educational analysis:** [`CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md`](CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md)  
**Upstream product flow:** [`CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md`](../product/CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md)  
**Upstream Strategy contract:** [`CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md`](CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md)  
**Upstream Strategy Composition:** [`CAPABILITY_4_9_5_TWIN_UPDATE_STRATEGY_COMPOSITION.md`](CAPABILITY_4_9_5_TWIN_UPDATE_STRATEGY_COMPOSITION.md)  
**Upstream Twin Persistence:** [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md)  
**Upstream Twin Repository Contract:** [`CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md`](CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md)  
**Upstream Educational Evidence:** [`CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md)  
**Upstream Twin retrieval:** [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Scope:** Structural Application Layer architecture for sequencing Twin evolution after Educational Evidence — **no code, algorithms, orchestration engine implementation, persistence implementation, Flask, ORM, or Educational Intelligence redesign**

---

## Document purpose

Capabilities 4.9.1–4.9.5 established:

- **Architecture** — Twin Update Strategies are the sole authority permitted to evolve a Digital Twin from Educational Evidence; they interpret; they never mutate; they never recommend.  
- **Educational analysis** — observations are not educational state; Educational Sufficiency may warrant preservation rather than densification.  
- **Product flow** — Twin evolution is invisible continuity after valid Evidence; students never operate Strategies.  
- **Contract** — Version 1.0 freezes one Strategy invocation: Current Twin + Educational Evidence → one complete immutable Successor Twin (or Domain Strategy Output under composition).  
- **Composition** — independently authored Domain Strategy Outputs assemble via Twin Composer into one immutable Successor Twin.

This capability defines the **Twin Update Coordinator**: the Application Layer orchestrator that owns write-side sequencing for Twin evolution.

It answers:

> Who sequences Evidence-driven Twin succession so Strategies, Composer, and Repository each do their job — without any of them becoming a god coordinator or a second educational reasoner?

**Governing principle (binding):**

> **The Twin Update Coordinator orchestrates. It never interprets.**

**Architectural restatement:**

> **Coordinator orchestrates. Strategies interpret. Composer assembles. Repository persists. Provider retrieves. Educational Intelligence consumes.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Twin Update Coordinator** | Application Layer write-path orchestrator that sequences the Twin evolution pipeline (also historically named Twin Update Pipeline in Capability 4.9.1) |
| **Educational Orchestrator** | Application Layer *read*-path orchestrator (Capability 3.2) — sibling conductor; never mutates Twin |
| **Twin Update Strategy** | Named educational interpreter of one educational concern |
| **Domain Strategy Output** | Lawful interpretive contribution for a Strategy’s owned Twin domain state |
| **Twin Composer** | Assembly authority that authors one immutable Successor Twin from Current Twin + Domain Strategy Outputs |
| **Twin Repository** | Application persistence adapter that stores / loads immutable Twin snapshots |
| **Twin Provider** | Retrieval authority for current Twin or honest absence on product read paths |
| **Educational Evidence** | Immutable educational observation (Capability 4.8) — sole lawful evolution input after birth |
| **Current Twin** | Latest lawful immutable Digital Twin snapshot for the authorised student / sitting scope |
| **Successor Twin** | New complete immutable Twin snapshot authored by Composition via Twin Composer |
| **Educational Intelligence** | Read path: Readiness → Decision → Recommendation → Mission — consumes Twins; never authors them from Evidence |

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Belief-update algorithms, scoring formulas, BKT, forgetting curves, or numeric engines  
- Strategy registration mechanics, worker queues, or orchestration engine implementation  
- Twin Composer merge algorithms or conflict-resolution mathematics  
- Flask routes, forms, templates, or product UX flows  
- Database schemas, Alembic migrations, ORM models, or persistence technology  
- Redesign of Educational Evidence, Calibration, Twin Persistence, TwinProvider, Strategy Contract Version 1.0, Strategy Composition, or Educational Intelligence domains  

---

# 1. Purpose

## 1.1 Why the Twin Update Coordinator exists

Educational Evidence enters the write pipeline as immutable observation. Twin Update Strategies interpret. Twin Composer assembles. Twin Repository persists. Educational Intelligence later consumes.

Without a Twin Update Coordinator as a first-class Application Layer authority:

- Strategies would be pressured to coordinate each other — recreating a god-strategy under “pipeline helpers.”  
- Composer would be tempted to invent invocation order or recover missing domain meaning.  
- Repository would be tempted to orchestrate succession as a side effect of store.  
- Product write bridges would wire Evidence → Belief inconsistently across routes and workers.  
- Failure would become theatre — partial successors, Mid-filled domains, or silent stage skips to keep the pipeline “moving.”

**The Twin Update Coordinator** exists to:

1. **Own sequencing** — Current Twin + Educational Evidence traverse Strategies → Composer → Repository in one lawful order.  
2. **Own orchestration** — invoke Strategies, Composer, and Repository; classify and propagate failure honestly.  
3. **Refuse educational reasoning** — densification, preservation judgement, and Educational Sufficiency remain inside Strategies.  
4. **Keep Strategies independent** — Strategies never coordinate siblings; only the Coordinator sequences them.  
5. **Mirror Application Layer discipline on the write path** — the Educational Orchestrator coordinates the read path; the Twin Update Coordinator coordinates the write path; neither reasons.

It is the lawful answer to:

> “Given valid Educational Evidence and a Current Twin, in what order must the platform invoke interpreters, assembly, and persistence so succession remains honest?”

It is **not** the answer to:

> “What does this Evidence mean for Knowledge?”  
> “Should Behaviour densify or preserve?”  
> “What should the student do next?”  
> “Which table stores the Twin?”

```
Educational Evidence enters the write pipeline.
              ↓
Strategies must not coordinate each other.
              ↓
The Coordinator owns sequencing.
The Coordinator owns orchestration.
              ↓
Educational reasoning remains inside Strategies.   ← this document
```

## 1.2 Read / write orchestration symmetry

| Path | Application conductor | Owns | Never owns |
|---|---|---|---|
| **Read** | Educational Orchestrator | Lifecycle, lawful EI invocation order, experience composition | Scoring, Decision, Twin mutation |
| **Write** | Twin Update Coordinator | Lifecycle, Strategy / Composer / Repository sequencing, failure honesty | Interpretation, composition logic, persistence technology |

Governing restatement:

> **Educational Orchestrator coordinates the study-day read path. Twin Update Coordinator coordinates Twin succession on the write path. Both compose Application lifecycle. Neither becomes Educational Intelligence.**

## 1.3 Relationship with completed companions

| Concern | Owner |
|---|---|
| Immutable educational observations | **Educational Evidence** (Capability 4.8) |
| Candidate observation domain affinities | **Evidence → Twin Mapping** (Capability 4.8.5) |
| Strategy purpose, independence, and whole-Twin immutability law | **Twin Update Strategy Architecture** (Capability 4.9.1) |
| Educational Sufficiency; preservation vs densification | **Twin Update Strategy Analysis** (Capability 4.9.2) |
| Invisible product timing of Twin evolution | **Twin Update Strategy Product Flow** (Capability 4.9.3) |
| One Strategy consume / produce closed boundary | **Twin Update Strategy Contract** (Capability 4.9.4) |
| Assembly of Domain Strategy Outputs into one Successor Twin | **Strategy Composition / Twin Composer** (Capability 4.9.5) |
| Write-path sequencing of Strategies → Composer → Repository | **Twin Update Coordinator** (this document) |
| Durable storage of Twin snapshots | **Twin Persistence / Twin Repository** (Capability 3.7) |
| Retrieval of current Twin or honest absence | **Twin Provider** (Capability 3.3) |
| Product read-path composition | **Educational Orchestrator** (Capability 3.2) |
| Educational judgement from Twin state | **Educational Intelligence** |

**Rules:**

1. **Coordinator orchestrates. Strategies interpret.**  
2. **Composer assembles. Repository persists.**  
3. **Provider retrieves. Educational Intelligence consumes.**  
4. **Coordinator never bypasses Strategies, Composer, or Repository stages.**  
5. **Coordinator never interprets Evidence.**

Governing restatement:

> **Coordination exists so independence and honesty can coexist on the write path — without collapsing interpretation into Persistence, Intelligence, or a god pipeline.**

---

# 2. Ownership

## 2.1 Coordinator owns

| Responsibility | Meaning |
|---|---|
| **Strategy invocation** | Invoke the registered / invited Twin Update Strategies for the composition cycle with Current Twin + Educational Evidence under Capability 4.9.4 boundaries |
| **Flow sequencing** | Enforce the Version 1.0 pipeline order so later stages never run without lawful earlier outputs |
| **Failure handling** | Stop honestly when Strategy, Composer, Repository, or Evidence validity fails; never fabricate educational state or partial successors |
| **Composer invocation** | Supply Current Twin + Domain Strategy Outputs to Twin Composer after Strategies complete lawfully |
| **Repository invocation** | Submit the Composer-authored Successor Twin for persistence after assembly succeeds |

The Coordinator is a **conductor**. Strategies remain the interpreters. Composer remains the assembler. Repository remains the store.

## 2.2 Coordinator does NOT own

| Forbidden ownership | Why |
|---|---|
| **Educational interpretation** | Belongs exclusively to Twin Update Strategies |
| **Educational state** | Twin meaning is authored by Strategies / assembled by Composer — Coordinator does not densify, preserve, or invent belief |
| **Recommendation** | Next-action ownership belongs to Educational Intelligence |
| **Persistence implementation** | Twin Repository / Infrastructure decide storage mechanics; Coordinator only submits the Successor Twin |
| **Composition logic** | Twin Composer owns assembly of Domain Strategy Outputs into one Successor Twin |

## 2.3 Ownership map (binding)

| Actor | Owns | Does not own |
|---|---|---|
| **Twin Update Coordinator** | Invocation, sequencing, failure honesty, hand-offs | Interpretation, assembly math, storage technology, recommendations |
| **Twin Update Strategies** | Educational interpretation per domain | Sibling coordination; persistence; retrieval; recommendations |
| **Twin Composer** | Assembly of one immutable Successor Twin | Interpretation; orchestration; persistence |
| **Twin Repository** | Durable snapshot storage / load policy | Orchestration; authorship; educational reasoning |
| **Twin Provider** | Retrieval or honest absence | Write-path sequencing |
| **Educational Intelligence** | Judgement from Twin state | Twin authorship from Evidence |
| **Educational Evidence** | Observation memory | Twin succession authorship |

### Ownership invariant

> **Coordinator owns Strategy invocation, flow sequencing, failure handling, Composer invocation, and Repository invocation. It does not own educational interpretation, educational state, recommendation, persistence implementation, or composition logic.**

---

# 3. Pipeline

## 3.1 Version 1.0 write pipeline (binding)

```
Current Twin
      +
Educational Evidence
        ↓
Twin Update Coordinator
        ↓
Twin Update Strategies
        ↓
Twin Composer
        ↓
Successor Twin
        ↓
Twin Repository
        ↓
Result
```

## 3.2 Stage meanings

| Stage | Owns | Does not own |
|---|---|---|
| **Current Twin** | Lawful immutable base snapshot for authorised scope | Evidence observation; next-action packaging |
| **Educational Evidence** | Immutable observation already recorded | Twin authorship; Strategy interpretation |
| **Twin Update Coordinator** | Sequencing Strategies → Composer → Repository; honest failure | Educational interpretation; composition algorithms; storage technology |
| **Twin Update Strategies** | Interpreting Current Twin + Evidence for owned domains | Sibling Strategy domains; Persistence; Recommendations; Coordinator roles |
| **Twin Composer** | Assembling Domain Strategy Outputs + Current Twin into one Successor Twin | Interpretation; Persistence; Retrieval; Recommendation |
| **Successor Twin** | Authoritative whole learner-state snapshot after composition | Evidence log ownership; next-action authority |
| **Twin Repository** | Durable store of the Successor Twin | Authorship; domain patch merges; educational reasoning; orchestration |
| **Result** | Honest success (persisted succession) or honest failure signal | Fabricated Mid Twin; partial durable slices |

## 3.3 No bypass law (binding)

The Coordinator **never bypasses** any stage:

| Forbidden shortcut | Why |
|---|---|
| Evidence → Repository | Observation is not educational state; Persistence must not author belief |
| Evidence → Composer | Composer never interprets; Strategies must run first |
| Strategies → Repository (skip Composer) | Under composition, domain outputs are not whole successors; only Composer authors the durable whole |
| Coordinator → Repository with Mid Twin | Fabrication; availability theatre |
| Coordinator → TwinProvider mutates current | Provider retrieves; succession is replace-by-snapshot via Repository |
| Educational Intelligence → Strategies as a judgement side effect | Write/read firewall (ADR-002) |

Version 1.0 may invoke a **subset** of Strategies for a cycle without redesigning pipeline law (Capability 4.9.1 / 4.9.5 subset posture). Subset selection is orchestration policy; it is not Stage skip.

### Pipeline invariant

> **Current Twin + Educational Evidence → Coordinator → Strategies → Composer → Successor Twin → Repository → Result. The Coordinator never bypasses any stage.**

---

# 4. Relationship with Twin Update Strategies

## 4.1 Invocation direction (binding)

```
Twin Update Coordinator
        ↓
invokes Twin Update Strategies
```

| Rule | Meaning |
|---|---|
| **Coordinator invokes Strategies** | Only the Coordinator sequences Strategy participation for a cycle |
| **Strategies never invoke Coordinator** | Strategies are interpreters, not pipelines |
| **Strategies never invoke each other** | Knowledge must not call Behaviour; only Coordinator sequences peers |
| **Coordinator never interprets Evidence** | Evidence meaning remains Strategy-owned for each domain concern |

## 4.2 Contract posture

Coordinator supplies each Strategy with the closed Version 1.0 inputs (Current Twin + Educational Evidence) and accepts lawful Domain Strategy Outputs (under Composition) or whole Successor Twin posture where single-Strategy Contract Version 1.0 applies without multi-Strategy composition.

Coordinator must not:

- Open Presentation or Intelligence payloads as Strategy authority  
- Ask Strategies to recommend, ready, or missionise  
- Pass mutable working Twins for in-place edit  
- Treat Evidence → Twin Mapping affinities as already-authored belief  

## 4.3 Preservation vs failure

| Strategy outcome | Coordinator behaviour |
|---|---|
| Strategy returns preserved domain state (Educational Sufficiency) | Continue orchestration — preservation is honesty, not failure (Capability 4.9.2 / 4.9.5) |
| Required Strategy unavailable or fails | Stop honestly — no partial Successor Twin |
| Strategy returns recommendation / readiness cargo | Reject — do not forward Intelligence theatre into Composer |

### Strategy relationship invariant

> **Coordinator invokes Strategies. Strategies never invoke Coordinator. Strategies never invoke each other. Coordinator never interprets Evidence.**

---

# 5. Relationship with Twin Composer

## 5.1 Hand-off (binding)

```
Coordinator supplies
  Current Twin
  +
  Domain Strategy Outputs
        ↓
Twin Composer
        ↓
returns one immutable Successor Twin
```

| Responsibility | Owner |
|---|---|
| Collect lawful Domain Strategy Outputs | Coordinator |
| Supply Current Twin as succession base | Coordinator |
| Assemble one complete immutable Successor Twin | Twin Composer |
| Interpret Evidence or densify belief | Neither — Strategies only |

## 5.2 Coordinator never assembles Twins

| Forbidden | Why |
|---|---|
| Coordinator merges domain slices into a “successor” | Composition logic belongs to Twin Composer |
| Coordinator Mid-fills missing domains for completeness | Fabrication |
| Coordinator asks Repository to finish assembly | Persistence never authors Twins |
| Coordinator skips Composer when multiple Strategies ran | Under composition path, only Composer authors the durable whole |

### Composer relationship invariant

> **Coordinator supplies Current Twin + Domain Strategy Outputs. Composer returns one immutable Successor Twin. Coordinator never assembles Twins.**

---

# 6. Relationship with Repository

## 6.1 Persistence hand-off (binding)

```
Coordinator
        ↓
submits Successor Twin
        ↓
Twin Repository
        ↓
decides storage
```

| Responsibility | Owner |
|---|---|
| Submit Composer-authored Successor Twin after successful assembly | Coordinator |
| Accept / refuse durable store; map storage ↔ Twin snapshot contract | Twin Repository |
| Choose Infrastructure technology (tables, files, caches) | Repository / Infrastructure — not Coordinator educational law |
| Author Twin meaning | Never Repository; never Coordinator |

## 6.2 Separation rules

| Rule | Meaning |
|---|---|
| **Coordinator never performs persistence itself** | No ORM, SQL, or storage adapters inside coordination ownership |
| **Repository never performs orchestration** | Repository does not invoke Strategies or Composer |
| **Whole-snapshot only** | Coordinator submits complete Successor Twins — never domain patches (Capability 3.7 / 4.9.5) |
| **Failure remains honest** | If Repository cannot store, succession is not durable; last Current Twin remains retrieve truth |

### Repository relationship invariant

> **Coordinator submits the Successor Twin for persistence. Repository decides storage. Coordinator never persists. Repository never orchestrates.**

---

# 7. Failure Behaviour

Product-level coordination behaviour only — no queues, retries, or storage mechanics.

**Binding rule:**

> **No fabricated educational state. No partial Successor Twins.**

## 7.1 Strategy fails

```
Strategy fails
        ↓
Coordinator stops honestly
```

| Condition | Coordinator behaviour |
|---|---|
| A required / invited Strategy for the cycle cannot lawfully run or returns unlawful output | **Stop honestly** — do not advance to Composer with silent domain omission |
| Forbidden | Forwarding “everything except Knowledge” as a durable successor; Mid-filling the missing domain |

## 7.2 Composer unavailable

```
Composer unavailable
        ↓
No Successor Twin
```

| Condition | Coordinator behaviour |
|---|---|
| Twin Composer cannot assemble | **No Successor Twin** — do not ask Repository to invent completeness; do not let Intelligence assemble fragments |
| Forbidden | Persisting Domain Strategy Outputs as “current Twin”; Coordinator assembly shortcuts |

## 7.3 Repository unavailable

```
Repository unavailable
        ↓
Successor Twin not persisted
```

| Condition | Coordinator behaviour |
|---|---|
| Composer authored a Successor Twin but Twin Repository cannot durably accept it | **Successor Twin not persisted** — signal honesty; Educational Intelligence continues on last durable Current Twin when Provider retrieve succeeds |
| Forbidden | Claiming persist success without store; Mid substitute Twin for availability theatre |

## 7.4 Evidence invalid

```
Evidence invalid
        ↓
Pipeline terminates
```

| Condition | Coordinator behaviour |
|---|---|
| Educational Evidence is missing, invalid, or not a lawful observation artefact | **Pipeline terminates** — do not invent Evidence; do not evolve Twin from raw activity |
| Missing Current Twin | Fail — do not invent Birth Twin inside Coordinator; Calibration remains birth author |

## 7.5 Failure summary

| Failure | Coordinator posture |
|---|---|
| Strategy fails / unavailable (required) | Stop honestly — no Composer, no partial Successor Twin |
| Strategy returns preserved state | Continue — preservation is lawful |
| Composer unavailable | No Successor Twin |
| Repository unavailable | Successor Twin not persisted |
| Evidence invalid / Current Twin missing | Pipeline terminates |
| Overlapping ownership / fabricated Strategy outputs | Reject — never invent |

Governing restatement:

> **Unavailability fails closed. Preservation continues. Composer failure yields no successor. Persistence failure refuses durability theatre. Invalid Evidence never evolves Twin. Never fabricate educational state.**

---

# 8. Educational Boundaries

## 8.1 Coordinator owns orchestration only

```
Coordinator owns orchestration only.
```

| Ownership | Meaning |
|---|---|
| **Sequencing** | Lawful order of Strategy → Composer → Repository |
| **Invocation** | Calling Strategies, Composer, and Repository with closed contracts |
| **Honest failure** | Terminating or continuing under architectural failure law without inventing belief |

## 8.2 Coordinator never

| Forbidden | Why |
|---|---|
| **Interprets** | Educational meaning belongs to Strategies |
| **Scores** | No mastery composites, engagement heuristics, or readiness theatre inside coordination |
| **Predicts** | Pass probability / forecasts remain Predictions / later forecasting consumers |
| **Updates educational state** | Belief densification / preservation is Strategy-owned; assembly is Composer-owned |
| **Generates recommendations** | Recommendation Engine / Decision packaging own next-action packaging |
| **Creates missions** | Mission Intelligence owns operationalisation |

## 8.3 Educational reasoning belongs exclusively to Strategies

```
Educational reasoning
        ↓
Strategies interpret
        ↓
Domain Strategy Outputs
        ↓
Composer assembles
        ↓
Repository stores
        ↓
Provider retrieves
        ↓
Educational Intelligence consumes
```

Coordinator may sequence that chain. It must not decide whether Evidence warranted densification, whether Confidence should rise, or whether Goals should change.

### Boundary invariant

> **Coordinator owns orchestration only. Educational reasoning belongs exclusively to Strategies. Judgement stays in Educational Intelligence. Observation stays in Evidence. Assembly stays in Composer. Persistence stays in Repository.**

---

# 9. Future Evolution

Version 1.0 Coordinator is intentionally small: single pipeline, deterministic sequencing, Strategy → Composer → Repository hand-offs, honest failure.

Future architecture may deepen **without redesigning Version 1.0 coordination law**:

| Future capability | Evolutionary posture |
|---|---|
| **Multiple Evidence Packages** | Coordinator may sequence multiple lawful Evidence artefacts per cycle policy; Strategies still interpret; no Evidence-as-belief shortcut |
| **Parallel Strategy execution** | Coordinator may invoke independent Strategies concurrently; still assemble only after lawful outputs; still no race-to-Repository patches |
| **Retry policies** | Infrastructure / operational retries for transient Repository unavailability must not invent educational substitutes on failure |
| **Distributed orchestration** | Split Coordinator across workers / services; Strategy Contract + Composer assembly + no-bypass pipeline remain write truth |
| **Plugin Strategy discovery** | Dynamic registration of Strategies under the same interpret / never-recommend / never-persist / never-cross-call rules |

### Evolution rules

1. **Version 1.0 remains lawful history** — simple single pipeline and subset Strategy catalogues stay valid.  
2. **Whole-Twin succession remains mandatory** — future speed must not resurrect domain patch persistence.  
3. **Strategies still never invoke each other** — orchestration advances; educational independence remains.  
4. **Coordinator still never interprets** — richer coordination must not densify belief inside the pipeline shell.  
5. **Educational Intelligence remains Twin consumer only** — distributed write must not collapse into read judgement side effects.

Governing restatement:

> **Future coordination may grow operational power. It must not redesign Version 1.0 sequencing honesty, Strategy independence, Composer assembly, or educational ownership firewalls.**

---

# 10. Version 1.0 Recommendations

## 10.1 Binding Version 1.0 recommendations

| Recommendation | Meaning |
|---|---|
| **Simple orchestration** | Prefer a thin conductor over a smart pipeline engine |
| **Single pipeline** | One Version 1.0 Evidence → Strategies → Composer → Repository path — no parallel product write theatres |
| **Deterministic sequencing** | Same lawful inputs traverse the same stage order; parallelism is a future optimisation, not Version 1.0 requirement |
| **Traceable execution** | Cycle outcomes remain attributable to Current Twin + Evidence + participating Strategies + Composer / Repository results |
| **Framework independence** | Coordinator remains Application Layer architecture free of Flask/ORM ownership; Infrastructure stays behind Repository |
| **Application-layer ownership** | Twin Update Coordinator is an Application component — sibling to Educational Orchestrator, not a Domain EI engine |
| **Small Coordinator** | Own only invocation, sequencing, failure honesty, and hand-offs — refuse interpretation and assembly |

## 10.2 Version 1.0 should remain intentionally small

Version 1.0 Coordinator succeeds when it ships (architecturally) the smallest coherent model:

1. Application Layer ownership of write-path sequencing.  
2. Deterministic single pipeline with no stage bypass.  
3. Strategies interpret; Composer assembles; Repository persists — Coordinator only connects them.  
4. Honest failure — Strategy / Composer / Repository / Evidence failures never fabricate educational state.  
5. Preservation continues; unavailability stops.  
6. Write/read firewall preserved against Educational Orchestrator / Intelligence.  
7. Compatibility with Capabilities 4.9.1–4.9.5 and Twin Repository Architecture.

It deliberately defers:

- Orchestration engine implementation  
- Parallel Strategy machinery  
- Retry / outbox systems  
- Plugin discovery platforms  
- Multi-Evidence package schedulers  

## 10.3 Version 1.0 success criteria (architectural)

Version 1.0 succeeds when:

1. Twin Update Coordinator is recognised as Application Layer write orchestrator — not a Strategy, Composer, or Repository.  
2. Pipeline order Current Twin + Evidence → Strategies → Composer → Repository is mandatory.  
3. Strategies never invoke Coordinator or each other; Coordinator never interprets Evidence.  
4. Coordinator supplies Composer with Current Twin + Domain Strategy Outputs and never assembles Twins.  
5. Coordinator submits Successor Twin to Repository and never persists itself.  
6. Failures never fabricate educational state or partial successors.  
7. Future parallel / distributed / plugin evolution requires no redesign of Version 1.0 ownership and sequencing law.

Governing restatement:

> **Simple. Single pipeline. Deterministic. Traceable. Framework-independent. Application-owned. Small. Version 1.0 remains intentionally thin.**

---

# 11. Architecture Compliance Summary

| Invariant | Status under this architecture |
|---|---|
| Coordinator orchestrates; Strategies interpret | Required |
| Composer assembles; Repository persists | Required |
| Provider retrieves; Educational Intelligence consumes | Preserved |
| Coordinator owns invocation, sequencing, failure handling, Composer and Repository hand-offs | Required |
| Coordinator never interprets / scores / predicts / recommends / missions | Required |
| Coordinator never assembles Twins or performs persistence | Required |
| Strategies never invoke Coordinator or each other | Required |
| No stage bypass on Version 1.0 pipeline | Required |
| No partial Successor Twin; no fabricated educational state | Required |
| Write path sibling to Educational Orchestrator read path | Affirmed |
| Capability 4.9.4 / 4.9.5 Strategy and Composition law remains lawful | Preserved |
| Twin Persistence replace-by-snapshot law preserved | Preserved |
| Educational Evidence observes; never updates Twin directly | Preserved |
| Curriculum V1/V2 topic-scoped succession identity safety | Required |
| Consistent with Educational Orchestrator, Strategy Architecture, Composition, Twin Repository, Application Layer | Affirmed |
| No Flask / ORM / algorithms / orchestration engine / persistence / Intelligence redesign | Honoured — architecture only |

---

# 12. STOP

This document defines **Twin Update Coordinator architecture only**.

It does **not** authorise:

- Implementation  
- Algorithms or belief-update / merge mathematics  
- Twin Update Coordinator / Pipeline orchestration engine implementation  
- Twin Composer service code  
- Strategy registration code  
- Flask routes or workers  
- ORM models, schemas, or migrations  
- Persistence of Strategies or Twins  
- Product flows, dashboards, or UI  
- Educational Intelligence redesign  
- Educational Evidence redesign  
- Bypass or replacement of Twin Update Strategy Contract Version 1.0  
- Bypass or replacement of Twin Update Strategy Composition law  

**STOP.**

---

# References

| Artefact | Role |
|---|---|
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Governing ADR; write/read separation; Evidence → Twin → Intelligence |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Platform educational chain; Update Strategy ownership |
| [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md) | Application Layer “compose; never reason” law |
| [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md) | Read-path orchestrator sibling; coordinates never reasons |
| [`CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md`](CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md) | Strategy architecture; Pipeline coordinator naming |
| [`CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md`](CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md) | Educational Sufficiency; preservation vs densification |
| [`CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md`](../product/CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md) | Invisible Twin evolution; students never operate Strategies |
| [`CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md`](CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md) | One-Strategy contract; Coordinator invokes under closed inputs |
| [`CAPABILITY_4_9_5_TWIN_UPDATE_STRATEGY_COMPOSITION.md`](CAPABILITY_4_9_5_TWIN_UPDATE_STRATEGY_COMPOSITION.md) | Twin Composer; Domain Strategy Outputs; Coordinator place named |
| [`CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md) | Evidence observes; never updates Twin |
| [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md) | Repository stores immutable Twin snapshots |
| [`CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md`](CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md) | Persist whole Twins; no hybrid authorship |
| [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md) | Provider retrieves Twin or honest absence |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Canonical Twin domain law; immutable snapshots |
