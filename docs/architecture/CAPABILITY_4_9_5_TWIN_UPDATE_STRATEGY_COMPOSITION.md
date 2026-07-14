# Capability 4.9.5 — Twin Update Strategy Composition

**Status:** Architecture only — no implementation  
**Epic:** Epic 4 — Educational Intelligence Evolution (Internal Alpha active)  
**Capability:** 4.9.5 Twin Update Strategy Composition (architectural model for assembling independently authored domain Strategy outputs into one immutable Successor Digital Twin)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Upstream Strategy architecture:** [`CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md`](CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md)  
**Upstream educational analysis:** [`CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md`](CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md)  
**Upstream product flow:** [`CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md`](../product/CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md)  
**Upstream Strategy contract:** [`CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md`](CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md)  
**Upstream Twin Persistence:** [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md)  
**Upstream Educational Evidence:** [`CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md)  
**Upstream Evidence → Twin mapping:** [`CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md`](CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Scope:** Structural composition architecture for multiple Twin Update Strategies — **no code, algorithms, orchestration engine implementation, persistence, Flask, ORM, or Educational Intelligence redesign**

---

## Document purpose

Capabilities 4.9.1–4.9.4 established:

- **Architecture** — Twin Update Strategies are the sole authority permitted to evolve a Digital Twin from Educational Evidence; they interpret; they never mutate; they never recommend.  
- **Educational analysis** — observations are not educational state; Educational Sufficiency may warrant preservation rather than densification.  
- **Product flow** — Twin evolution is invisible continuity after valid Evidence; students never operate Strategies.  
- **Contract** — Version 1.0 freezes one Strategy invocation: Current Twin + Educational Evidence → one complete immutable Successor Twin.

This capability defines **how multiple independent Twin Update Strategies cooperate to produce one immutable Successor Digital Twin**.

It answers:

> How do independently authored educational domain contributions become one complete immutable Successor Twin — without any Strategy owning the whole Twin, and without Composition performing educational reasoning?

**Governing principle (binding):**

> **Each Strategy owns one educational concern. No Strategy owns the complete Digital Twin. Composition assembles one complete immutable Successor Twin.**

**Architectural restatement:**

> **Strategies interpret. Composition assembles. Repository stores. Provider retrieves. Educational Intelligence consumes. Composition never performs educational reasoning.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Strategy Composition** | Architectural model that assembles Domain Strategy Outputs into one complete immutable Successor Twin (this document) |
| **Twin Update Strategy** | Named educational interpreter of one educational concern (Knowledge, Performance, Behaviour, Memory, Goals, …) |
| **Domain Strategy Output** | Lawful interpretive contribution for the Strategy’s owned Twin domain state — not a partial Twin offered to Repository, not a recommendation |
| **Twin Composer** | Assembly authority that receives Current Twin + Domain Strategy Outputs and authors one immutable Successor Twin — assembles only; never interprets |
| **Twin Update Coordinator** | Future coordination authority that invokes registered Strategies for a composition cycle (also historically named Twin Update Pipeline in Capability 4.9.1) — does not embed educational interpretation |
| **Twin Update Strategy Contract** | Closed Application boundary for one Strategy invocation (Capability 4.9.4) — remains lawful under and beneath composition |
| **Current Twin** | Latest lawful immutable Digital Twin snapshot for the authorised student / sitting scope |
| **Successor Twin** | New complete immutable Twin snapshot authored by Composition via Twin Composer — never an in-place edit or Repository merge of patches |
| **Educational Intelligence** | Read path: Readiness → Decision → Recommendation → Mission — consumes Twins; never authors them from Evidence |

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Belief-update algorithms, scoring formulas, BKT, forgetting curves, or numeric engines  
- Twin Update Coordinator / Pipeline orchestration engine implementation or Strategy registration code  
- Twin Composer implementation, merge algorithms, or conflict-resolution mathematics  
- Flask routes, forms, templates, or product UX flows  
- Database schemas, Alembic migrations, ORM models, or persistence technology  
- Redesign of Educational Evidence, Calibration, Twin Persistence, TwinProvider, Strategy Contract Version 1.0, or Educational Intelligence domains  

---

# 1. Purpose

## 1.1 Why Strategy Composition exists

Educational state is multi-dimensional. Knowledge, Performance, Behaviour, Memory, and Goals answer different educational questions and may deepen on independent schedules.

Without Strategy Composition as a first-class architectural model:

- Independent Strategies would be pressured to own “the whole Twin,” recreating a god-strategy under many names.  
- Repository would be tempted to merge domain patches into hybrid Twins — Persistence authorship by convenience.  
- Educational Intelligence would be tempted to stitch domain fragments while judging readiness.  
- Partial successor theatre would appear: Knowledge advances while Behaviour is silently dropped mid-write.  
- Cross-Strategy coupling would grow — Strategies calling each other, sharing ownership, or smuggling neighbouring-domain meaning.

**Strategy Composition** exists to:

1. **Allow multiple educational domains to evolve independently** — domain Strategies deepen without freezing the rest of Twin law.  
2. **Still deliver one coherent Digital Twin** — students and Educational Intelligence consume a whole successor, not a bag of domain slices.  
3. **Combine independently authored educational state** — Domain Strategy Outputs assemble under one composition law.  
4. **Refuse educational reasoning at the assembly boundary** — Composition never interprets Evidence, densifies mastery, or recommends next actions.  
5. **Preserve Twin Update Strategy Contract Version 1.0** — one-Strategy invocation remains lawful; composition sits *above* that contract, never replaces its closed inputs/outputs with patch theatre.

It is the lawful answer to:

> “Given several lawful domain interpretations of the same Evidence against the same Current Twin, how does the platform author exactly one immutable Successor Twin?”

It is **not** the answer to:

> “What does this Evidence mean for Knowledge?”  
> “Should Behaviour densify or preserve?”  
> “What should the student do next?”  
> “Which table stores the Twin?”

```
Multiple educational domains evolve independently.
              ↓
Students still require one coherent Digital Twin.
              ↓
Composition combines independently authored educational state.
              ↓
Composition never performs educational reasoning.   ← this document
```

## 1.2 Relationship with completed companions

| Concern | Owner |
|---|---|
| Immutable educational observations | **Educational Evidence** (Capability 4.8) |
| Candidate observation domain affinities | **Evidence → Twin Mapping** (Capability 4.8.5) |
| Strategy purpose, independence, and whole-Twin immutability law | **Twin Update Strategy Architecture** (Capability 4.9.1) |
| Educational Sufficiency; preservation vs densification | **Twin Update Strategy Analysis** (Capability 4.9.2) |
| Invisible product timing of Twin evolution | **Twin Update Strategy Product Flow** (Capability 4.9.3) |
| One Strategy consume / produce closed boundary | **Twin Update Strategy Contract** (Capability 4.9.4) |
| Assembly of many Strategies into one Successor Twin | **Strategy Composition** (this document) |
| Durable storage of Twin snapshots | **Twin Persistence / Twin Repository** (Capability 3.7) |
| Retrieval of current Twin or honest absence | **Twin Provider** (Capability 3.3) |
| Educational judgement from Twin state | **Educational Intelligence** |

**Rules:**

1. **Strategies interpret. Composition assembles.**  
2. **Composition never interprets Evidence and never densifies belief.**  
3. **Repository stores. Provider retrieves. Educational Intelligence consumes.**  
4. **Capability 4.9.4 remains valid** for single-Strategy invocation even after composition exists.  
5. **Composition must not bypass whole-Twin law** by forwarding domain patches to Repository.

Governing restatement:

> **Composition exists so independence and coherence can coexist — without collapsing interpretation into Persistence, Intelligence, or a god-strategy.**

---

# 2. Composition Philosophy

These principles bind Strategy Composition for Version 1.0. They extend Capability 4.9.1 Strategy independence, Capability 4.9.4 one-Strategy contract law, Twin Persistence replace-by-snapshot law, ADR-002 write/read separation, and Application Layer “compose; never reason” discipline onto the multi-Strategy write path.

### Strategies remain independent

Each Twin Update Strategy evolves its educational responsibility without depending on sibling Strategy internals, schedules, or registration details.

### Strategies never invoke one another

Knowledge must not call Behaviour. Behaviour must not call Performance. Cross-domain meaning is smuggling, not composition. Only Coordinator / Composition may sequence Strategy invocations.

### Strategies never share ownership

One educational concern has one Strategy owner. Overlapping authorship of the same Twin domain state is architectural failure.

### Strategies never persist Twins

Twin Repository stores immutable snapshots. Strategies author educational meaning for their domain; they are not storage adapters.

### Strategies never retrieve Twins

Twin Provider retrieves Current Twin (or honest absence) on product read paths. Composition / Coordinator may receive an already-retrieved Current Twin as input; Strategies do not own retrieve-or-absent policy.

### Composition assembles

Twin Composer combines Current Twin + Domain Strategy Outputs into one complete immutable Successor Twin. Assembly is structural succession discipline — not interpretation.

### Strategies interpret

Educational meaning of Evidence against Current Twin remains Strategy-owned for each domain concern.

### Repository stores

Twin Repository persists the composed Successor Twin under replace-by-snapshot law. It never merges domain patches as authorship.

### Provider retrieves

Twin Provider returns the current Twin or honest absence for Educational Intelligence and product read paths.

### Educational Intelligence consumes

Readiness → Decision → Recommendation → Mission consume Twin state. Intelligence never invokes Composition as a side effect of judgement, and never authors successors from Evidence.

### Verb map (binding)

| Actor | Verb |
|---|---|
| **Educational Evidence** | Observes |
| **Twin Update Strategies** | Interpret |
| **Twin Composer / Composition** | Assembles |
| **Twin Repository** | Stores |
| **Twin Provider** | Retrieves |
| **Educational Intelligence** | Consumes |

Governing restatement:

> **Independent Strategies. No cross-calls. No shared ownership. No Strategy persistence or retrieval. Composition assembles. Strategies interpret. Repository stores. Provider retrieves. Intelligence consumes.**

---

# 3. Domain Ownership

## 3.1 Educational ownership map (binding)

Each Strategy owns exactly one educational concern and the Twin domain state that concern authors under succession.

| Strategy | Owns |
|---|---|
| **Knowledge Strategy** | **KnowledgeState** |
| **Performance Strategy** | **PerformanceState** |
| **Behaviour Strategy** | **BehaviourState** |
| **Memory Strategy** | **MemoryState** |
| **Goal Strategy** | **GoalState** |

```
One Strategy
      ↓
One educational concern
```

Additional separable Strategies (e.g. Confidence when split from neighbouring domains) remain future catalogue extensions — they must still obey single-domain ownership.

## 3.2 Ownership meaning

| Rule | Meaning |
|---|---|
| **Single-domain ownership** | A Strategy authors only its owned domain state’s educational succession contribution |
| **No overlapping ownership** | Two Strategies must not both claim authorship of the same domain state in one composition cycle |
| **No whole-Twin ownership by a domain Strategy** | Under composition, no named domain Strategy is the sole owner of the complete Digital Twin aggregate |
| **Preservation remains domain-local honesty** | A Strategy may return preserved domain state when Educational Sufficiency does not warrant densification (Capability 4.9.2 / 4.9.4) — that still counts as a lawful Domain Strategy Output |
| **Identity / Calibration anchors** | Birth Identity and Calibration priors remain Calibration-owned at birth; Strategies must not silently rebrand priors as Evidence-backed density without warrant, and Composition must not invent Identity theatre |

## 3.3 What domain ownership is not

| Forbidden pattern | Why |
|---|---|
| Knowledge Strategy grants Behaviour completion credit | Ownership leakage; Behaviour owns BehaviourState |
| Behaviour Strategy raises Knowledge mastery | Cross-domain smuggling |
| Performance Strategy emits pass probability as Twin truth | Prediction / forecasting ownership — not Strategy composition cargo |
| Goal Strategy rewrites Identity from session noise | Identity / Calibration boundary breach |
| Composition “fills” an unowned domain with Mid beliefs | Fabrication; unknown remains lawful |

### Domain ownership invariant

> **One Strategy → one educational concern → one owned domain state. No overlapping ownership. No Strategy owns the complete Digital Twin under Composition.**

---

# 4. Twin Composer

## 4.1 Role

The **Twin Composer** is the assembly authority of Strategy Composition.

It exists so Domain Strategy Outputs become one complete immutable Successor Twin without Repository patch merges and without Educational Intelligence stitching fragments on the read path.

## 4.2 Responsibilities (binding)

| Responsibility | Meaning |
|---|---|
| **Receive Current Twin** | Accept the lawful immutable Current Twin for the authorised scope as the succession base |
| **Receive Domain Strategy Outputs** | Accept interpretive contributions for owned domains from the Strategies invoked in the composition cycle |
| **Author one immutable Successor Twin** | Emit exactly one complete Twin aggregate representing post-composition educational state |

```
Current Twin
      +
Domain Strategy Outputs
      ↓
Twin Composer
      ↓
One immutable Successor Twin
```

## 4.3 Twin Composer does NOT

| Forbidden | Why |
|---|---|
| **Interpret** | Educational meaning belongs to Strategies |
| **Reason** | No Educational Sufficiency judgement, mastery densification, or belief algebra inside Composer |
| **Recommend** | Next-action ownership belongs to Educational Intelligence |
| **Persist** | Twin Repository stores; Composer does not become a storage adapter |
| **Retrieve** | Twin Provider retrieves; Composer does not own absence honesty policy |

## 4.4 Assembly law (binding)

1. **Composer assembles only.** It combines Current Twin structure with Domain Strategy Outputs under ownership placement — it does not invent missing educational meaning.  
2. **Domains without a Strategy output in the cycle** remain as carried forward from Current Twin (or remain empty / unknown where Current Twin already places honesty) — Composer does not Mid-fill unowned domains for completeness theatre.  
3. **Composer never asks Repository to merge patches.** The Successor Twin handed downstream is already a complete immutable whole.  
4. **Composer never collapses Strategies into one interpreter.** Assembly is not a second Knowledge Strategy.  
5. **Provenance posture remains mandatory.** The Successor Twin must remain attributable to Current Twin + Evidence + participating Strategies (Capability 4.9.4 provenance spirit extended to composition).

### Composer invariant

> **Twin Composer receives Current Twin + Domain Strategy Outputs and authors one immutable Successor Twin. It assembles only. It never interprets, reasons, recommends, persists, or retrieves.**

---

# 5. Composition Flow

## 5.1 Complete Version 1.0 composition flow

```
Educational Evidence
        ↓
Twin Update Coordinator (future)
        ↓
Knowledge Strategy
Behaviour Strategy
Performance Strategy
Memory Strategy
        ↓
Twin Composer
        ↓
Successor Twin
        ↓
Twin Repository
```

Goal Strategy may participate in the same catalogue when Goals require Evidence-driven succession; Version 1.0 may invoke a **subset** of Strategies without redesigning composition law (Capability 4.9.1 subset posture preserved).

## 5.2 Stage meanings

| Stage | Owns | Does not own |
|---|---|---|
| **Educational Evidence** | Immutable observation memory already created | Twin authorship; Strategy interpretation |
| **Twin Update Coordinator (future)** | Invoking registered Strategies for a composition cycle; supplying Current Twin + Evidence into Strategy boundaries | Educational interpretation algorithms; Repository merge authorship; Intelligence judgement |
| **Domain Strategies** | Interpreting Current Twin + Evidence for their owned domain | Sibling Strategy domains; Persistence; Recommendations |
| **Twin Composer** | Assembling Domain Strategy Outputs + Current Twin into one Successor Twin | Interpretation; Persistence; Retrieval; Recommendation |
| **Successor Twin** | Authoritative whole learner-state snapshot after composition | Evidence log ownership; next-action authority |
| **Twin Repository** | Durable store of the Successor Twin | Authorship; domain patch merges; educational reasoning |

## 5.3 Relationship to Twin Update Strategy Contract (4.9.4)

Composition sits **above** the one-Strategy contract:

```
Strategy Composition
        ↓
invokes Twin Update Strategy Contract per Strategy
  (or receives Domain Strategy Outputs under composition law)
        ↓
Twin Composer
        ↓
one durable complete Successor Twin → Twin Repository
```

Rules:

1. **Capability 4.9.4 remains lawful** for single-Strategy evolution when composition is not required.  
2. **Composition must not redefine Version 1.0 Required inputs** as Presentation cargo or Intelligence payloads.  
3. **Composition must not legitimise patch outputs** — even if intermediate Domain Strategy Outputs are domain-scoped, only Twin Composer may author the whole Successor Twin that Repository stores.  
4. **Coordinator is future** — this document names its architectural place; it does not authorise orchestration engine implementation.

## 5.4 Student experience

Students **never** experience this flow directly (Capability 4.9.3).

They study. Evidence may be created. Composition may assemble a Successor Twin afterward. On a later visit, Twin Provider retrieves; Educational Intelligence consumes. The Twin write machinery remains invisible continuity.

### Composition flow invariant

> **Evidence → Coordinator (future) → independent Strategies → Twin Composer → Successor Twin → Repository. Students never operate Composition.**

---

# 6. Failure Behaviour

Product-level composition behaviour only — no queues, retries, or persistence mechanics.

**Binding rule:**

> **No fabricated educational state. No partial Successor Twin.**

## 6.1 Knowledge Strategy unavailable

```
Knowledge Strategy unavailable
        ↓
Composition fails honestly
        ↓
No partial Successor Twin
```

| Condition | Composition behaviour |
|---|---|
| A required / invited Strategy for the composition cycle cannot lawfully run | **Composition fails honestly** — do not emit a Successor Twin that silently omits the Strategy’s owned domain as if succession completed |
| Forbidden | Forwarding “everything except Knowledge” as a durable successor; Mid-filling Knowledge to keep the Twin moving |

Version 1.0 may define which Strategies are required for a given cycle architecturally; absence of a required Strategy is failure, not soft omission.

## 6.2 Behaviour Strategy returns preserved state

```
Behaviour Strategy returns preserved state
        ↓
Composition continues
```

| Condition | Composition behaviour |
|---|---|
| Behaviour Strategy lawfully returns preserved BehaviourState because Educational Sufficiency does not warrant densification | **Composition continues** — preservation is educational honesty (Capability 4.9.2 / 4.9.4), not composition failure |
| Twin Composer | Assembles preserved BehaviourState with other Domain Strategy Outputs into one Successor Twin |

Preservation ≠ unavailability. Preserved domain output is a lawful Domain Strategy Output.

## 6.3 Composer unavailable

```
Composer unavailable
        ↓
No Successor Twin
```

| Condition | Composition behaviour |
|---|---|
| Twin Composer cannot assemble | **No Successor Twin** — do not ask Repository to invent completeness; do not let Intelligence assemble fragments |
| Forbidden | Persisting Domain Strategy Outputs as “current Twin”; patch-merging in Persistence |

## 6.4 Repository unavailable

```
Repository unavailable
        ↓
Successor Twin not persisted
```

| Condition | Composition behaviour |
|---|---|
| Composer authored a Successor Twin but Twin Repository cannot durably accept it | **Successor Twin not persisted** — signal honesty; Educational Intelligence continues on last durable Current Twin when retrieve succeeds (Capability 4.9.4 / 3.7 posture) |
| Forbidden | Claiming persist success without store; Mid substitute Twin for availability theatre |

## 6.5 Additional failure postures

| Condition | Composition behaviour |
|---|---|
| Missing Current Twin | Fail — do not invent Birth Twin inside Composition; Calibration remains birth author |
| Invalid Educational Evidence | Fail — do not invent Evidence; do not update from raw activity |
| Domain ownership conflict (two Strategies claim same domain) | Fail — overlapping ownership is unlawful |
| Strategy returns recommendation / readiness / mission cargo | Reject that output — Composition must not forward Intelligence theatre into Twin assembly |
| Strategy returns a Repository-bound patch without composition authorship | Reject — patches are not successors |

## 6.6 Failure summary

| Failure | Composition posture |
|---|---|
| Required Strategy unavailable | Composition fails honestly — no partial Successor Twin |
| Strategy returns preserved state | Composition continues |
| Composer unavailable | No Successor Twin |
| Repository unavailable | Successor Twin not persisted |
| Overlapping ownership / fabricated outputs | Reject — never invent |

Governing restatement:

> **Unavailability fails closed. Preservation continues. Composer failure yields no successor. Persistence failure refuses durability theatre. Never fabricate educational state.**

---

# 7. Educational Boundaries

## 7.1 Composition owns

| Ownership | Meaning |
|---|---|
| **Assembly** | Combining Current Twin + Domain Strategy Outputs into one complete Successor Twin |
| **Immutability discipline** | Ensuring succession produces a new whole Twin — never in-place mutation or Repository patch merges |
| **Traceability posture** | Keeping Successor Twin attributable to Current Twin + Evidence + participating Strategies |

## 7.2 Composition does NOT own

| Forbidden ownership | Why |
|---|---|
| **Educational interpretation** | Belongs to Twin Update Strategies |
| **Recommendation** | Belongs to Recommendation Engine / Decision packaging |
| **Mission generation** | Belongs to Mission Intelligence |
| **Dashboard decisions** | Belongs to product surfaces / Application read composition |
| **Prediction** | Belongs to Predictions / later forecasting consumers |

## 7.3 Educational meaning always belongs to Strategies

```
Educational meaning
        ↓
Strategies interpret
        ↓
Domain Strategy Outputs
        ↓
Composition assembles structure
        ↓
Successor Twin remembers state
```

Composition may place owned domain contributions into Twin structure. It must not decide whether Evidence warranted densification, whether Confidence should rise, or whether Goals should change.

### Boundary invariant

> **Composition owns assembly, immutability, and traceability. Educational meaning always belongs to Strategies. Judgement stays in Educational Intelligence. Observation stays in Evidence.**

---

# 8. Future Evolution

Version 1.0 Composition is intentionally small: independent Strategies, single-domain ownership, Twin Composer assembly, whole immutable successors, honest failure.

Future architecture may deepen **without redesigning Version 1.0 composition law**:

| Future capability | Evolutionary posture |
|---|---|
| **Additional domain Strategies** | Register new single-concern Strategies; Composer places new owned domains without inventing Version 1.0 ownership conflicts |
| **Parallel execution** | Coordinator may invoke Strategies concurrently; composition law remains “assemble after lawful outputs,” not “race Repository patches” |
| **Distributed orchestration** | Split Coordinator across workers / services; Strategy Contract + Composer assembly remain educational/write truth |
| **Strategy discovery** | Dynamic registration / discovery of Strategies; ownership map remains closed and non-overlapping |
| **Plugin Strategies** | Plugin contributors under the same interpret / never-recommend / never-persist rules |
| **Incremental composition** | Richer cycle selection of which Strategies run; still no partial durable Twin — Composer emits wholes or composition fails closed |

### Evolution rules

1. **Version 1.0 remains lawful history** — single-Strategy contract and subset Strategy catalogues stay valid.  
2. **Whole-Twin succession remains mandatory** — future speed must not resurrect domain patch persistence.  
3. **Strategies still never invoke each other** — orchestration advances; educational independence remains.  
4. **Composer still never interprets** — richer coordination must not densify belief inside assembly.  
5. **Educational Intelligence remains Twin consumer only.**

Governing restatement:

> **Future composition may grow coordination power. It must not redesign Version 1.0 independence, whole-Twin assembly, or educational ownership firewalls.**

---

# 9. Architectural Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **Strategies overlapping ownership** | Two Strategies densify the same domain; Twin becomes contested | Single-domain ownership map; ownership conflict fails closed |
| **Strategies invoking each other** | Hidden cascade of Interpretation across domains; Coupling recreates god-strategy | Hard ban: Strategies never invoke one another; only Coordinator sequences |
| **Composer interpreting educational state** | Assembly becomes a second Strategy; Mid fills appear for “completeness” | Composer assembles only; Educational Sufficiency stays Strategy-owned |
| **Partial Successor Twins** | Knowledge advances while Behaviour dropped mid-cycle; Repository stores hybrid | No partial Successor Twin; required Strategy unavailability fails composition |
| **Domain conflicts** | Competing Domain Strategy Outputs for one domain; silent last-write-wins theatre | Reject overlapping ownership; no silent conflict “resolution math” in Version 1.0 Composer |
| **Hidden coupling** | Shared mutable working Twin passed among Strategies; in-place edits | Current Twin immutable; Strategies emit Domain Strategy Outputs; Composer authors succession |
| **Duplicated educational reasoning** | Intelligence re-interprets Evidence; Repository merges meaning; Mapping treated as authorship | ADR-002 firewall: Strategies interpret → Composer assembles → Repository stores → Provider retrieves → Intelligence consumes |
| **Contract bypass** | Composition invents raw inputs outside Capability 4.9.4 | Composition sits above the contract; never reopens Presentation / Intelligence as Strategy authority |
| **Persistence authorship** | TwinRepository merges domain slices as “composition” | Only Composer authors the whole Successor Twin handed to Repository |
| **Preservation misclassified as failure** | Honest preserved BehaviourState aborts the cycle | Preservation continues composition; unavailability fails |

### Risk restatement

The primary danger is not missing Composer algorithms. It is **Strategies that share ownership or call each other**, **a Composer that starts interpreting**, or **partial successors that Persistence quietly merges** — recreating planner pathology as “adaptive composition.”

---

# 10. Version 1.0 Recommendations

## 10.1 Binding Version 1.0 recommendations

| Recommendation | Meaning |
|---|---|
| **Independent Strategies** | Domain Strategies evolve without cross-calls or shared ownership |
| **Single-domain ownership** | KnowledgeState / PerformanceState / BehaviourState / MemoryState / GoalState each have one Strategy owner |
| **Whole Twin composition** | Twin Composer authors one complete immutable Successor Twin per successful cycle |
| **Immutable Successor Twins** | Evolution is succession only — never in-place mutation |
| **Traceable composition** | Successor Twin remains attributable to Current Twin + Evidence + participating Strategies |
| **Future orchestration compatibility** | Version 1.0 names Coordinator place without requiring engine implementation now; later parallel / distributed / plugin execution must not rewrite ownership law |

## 10.2 Version 1.0 should remain intentionally small

Version 1.0 Composition succeeds when it ships (architecturally) the smallest coherent model:

1. Independent Strategies with single-domain ownership.  
2. Domain Strategy Outputs + Current Twin → Twin Composer → one Successor Twin.  
3. Honest failure when required Strategies or Composer are unavailable — no partial Twins.  
4. Preservation as lawful domain output that allows composition to continue.  
5. Repository persistence only of composed wholes.  
6. Compatibility with Capability 4.9.4 one-Strategy contract underneath.  
7. No Educational Intelligence, Persistence, or Presentation authorship of successors.

It deliberately defers:

- Orchestration engine implementation  
- Parallel execution machinery  
- Plugin discovery systems  
- Conflict-resolution mathematics between overlapping claims (because overlapping claims are unlawful, not solved)  
- Incremental durable partial Twins  

## 10.3 Version 1.0 success criteria (architectural)

Version 1.0 succeeds when:

1. Strategy Composition is recognised as assembly above Strategies — not a second interpreter.  
2. No Strategy owns the complete Digital Twin under the composition path.  
3. Twin Composer receives Current Twin + Domain Strategy Outputs and authors one immutable Successor Twin.  
4. Strategies never invoke one another, never persist, and never retrieve.  
5. Composition failures never fabricate educational state or partial successors.  
6. Educational Intelligence continues to consume Twins only.  
7. Future Coordinator / parallel / plugin evolution requires no redesign of Version 1.0 ownership and assembly law.

Governing restatement:

> **Independent. Single-domain. Whole. Immutable. Traceable. Orchestration-ready later. Version 1.0 remains intentionally small.**

---

# 11. Architecture Compliance Summary

| Invariant | Status under this architecture |
|---|---|
| Strategies interpret; Composition assembles | Required |
| No Strategy owns the complete Twin under composition | Required |
| Single-domain ownership; no overlap | Required |
| Twin Composer authors one immutable Successor Twin | Required |
| Composer never interprets / recommends / persists / retrieves | Required |
| Strategies never invoke one another | Required |
| Repository stores wholes only; no domain patch merges as authorship | Required |
| Provider retrieves; Educational Intelligence consumes | Preserved |
| Capability 4.9.4 one-Strategy contract remains lawful beneath composition | Preserved |
| Educational Evidence observes; never updates Twin directly | Preserved |
| No partial Successor Twin; no fabricated educational state | Required |
| Curriculum V1/V2 topic-scoped succession identity safety | Required |
| Consistent with Twin Persistence, Evidence Architecture, ADR-002, Application Layer | Affirmed |
| No Flask / ORM / algorithms / orchestration engine / persistence / Intelligence redesign | Honoured — architecture only |

---

# 12. STOP

This document defines **Twin Update Strategy Composition architecture only**.

It does **not** authorise:

- Implementation  
- Algorithms or belief-update / merge mathematics  
- Twin Update Coordinator / Pipeline orchestration engine implementation  
- Twin Composer service code  
- Flask routes or workers  
- ORM models, schemas, or migrations  
- Persistence of Strategies or Twins  
- Product flows, dashboards, or UI  
- Educational Intelligence redesign  
- Educational Evidence redesign  
- Bypass or replacement of Twin Update Strategy Contract Version 1.0  

**STOP.**

---

# References

| Artefact | Role |
|---|---|
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Governing ADR; write/read separation; Evidence → Twin → Intelligence |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Platform educational chain; Update Strategy ownership |
| [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md) | Application Layer “compose; never reason” law |
| [`CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md`](CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md) | Strategy architecture; independence; Pipeline coordinator naming |
| [`CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md`](CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md) | Educational Sufficiency; preservation vs densification |
| [`CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md`](../product/CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md) | Invisible Twin evolution; students never operate Strategies |
| [`CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md`](CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md) | One-Strategy contract; composition sits above |
| [`CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md) | Evidence observes; never updates Twin |
| [`CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md`](CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md) | Candidate observations; stops before Strategy interpretation |
| [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md) | Repository stores immutable Twin snapshots |
| [`CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md`](CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md) | Persist whole Twins; no hybrid authorship |
| [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md) | Provider retrieves Twin or honest absence |
| [`CAPABILITY_2_5_BEHAVIOUR_UPDATE_STRATEGY.md`](CAPABILITY_2_5_BEHAVIOUR_UPDATE_STRATEGY.md) | Domain Strategy precedent (Behaviour) |
| [`CAPABILITY_2_6_PERFORMANCE_UPDATE_STRATEGY.md`](CAPABILITY_2_6_PERFORMANCE_UPDATE_STRATEGY.md) | Domain Strategy precedent (Performance) |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Canonical Twin domain law; immutable snapshots |
| [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md) | Shared educational vocabulary |
