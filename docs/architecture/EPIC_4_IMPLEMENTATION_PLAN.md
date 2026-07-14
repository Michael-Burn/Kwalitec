# Epic 4 — Implementation Plan

**Status:** Engineering roadmap only — no implementation in this milestone  
**Epic:** Epic 4 — Educational Intelligence Evolution (Internal Alpha active)  
**Scope:** Incremental implementation roadmap for Educational Evidence (4.8) and Twin Update (4.9) — **not architecture redesign, not product design, not educational analysis, not code**  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)

**Upstream (architecture complete — frozen for implementation):**

| Capability | Artefacts |
|---|---|
| **4.8 Educational Evidence** | [`CAPABILITY_4_8_1`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md) · [`4.8.2`](CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md) · [`4.8.3`](../product/CAPABILITY_4_8_3_EDUCATIONAL_EVIDENCE_PRODUCT_FLOW.md) · [`4.8.4`](CAPABILITY_4_8_4_EDUCATIONAL_EVIDENCE_CONTRACT.md) · [`4.8.5`](CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md) |
| **4.9 Twin Update** | [`CAPABILITY_4_9_1`](CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md) · [`4.9.2`](CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md) · [`4.9.3`](../product/CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md) · [`4.9.4`](CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md) · [`4.9.5`](CAPABILITY_4_9_5_TWIN_UPDATE_STRATEGY_COMPOSITION.md) |
| **Twin Persistence / Provider** | [`CAPABILITY_3_7_1`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md) · [`CAPABILITY_3_7_3`](CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md) · [`CAPABILITY_3_3`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md) |

---

## Document purpose

Capabilities 4.8 and 4.9 are architecturally complete. No further architectural redesign is planned before implementation.

This document converts that architecture into an **incremental engineering roadmap**. It answers:

1. What is frozen and must not be redesigned during implementation  
2. Which principles govern every implementation milestone  
3. In what order Components ship so each milestone is independently testable  
4. What Version 1.0 delivers vs what remains stubbed or deferred  
5. How testing and Internal Alpha validate the end-to-end path  

**Governing principle (binding):**

> **Implement the frozen architecture incrementally. Minimise risk. Preserve integrity. Ship one independently testable milestone at a time. Do not redesign contracts to excuse early convenience.**

**Architectural restatement:**

> **Evidence observes. Strategies interpret. Composer assembles. Repository stores. Provider retrieves. Educational Intelligence consumes. Implementation wires this chain — it does not invent a shorter one.**

**Non-goals of this document**

- Implementation code, package layouts, or service class designs beyond roadmap naming  
- Belief-update algorithms, sufficiency formulas, BKT, or numeric engines  
- Flask routes, templates, ORM schemas, or Alembic migrations  
- Architectural redesign of 4.8 / 4.9 / Twin Persistence / Educational Intelligence  
- Product UX redesign or Internal Alpha feature expansion beyond validation posture  

**STOP before implementation.** This document does not authorise starting Phase A work until a separate implementation milestone explicitly requests it.

---

# 1. Architecture Freeze

The following capabilities and contracts are **frozen**. Future implementation must implement them — not redesign them.

| Frozen surface | Bound by | Implementation posture |
|---|---|---|
| **Educational Evidence** | Capabilities 4.8.1–4.8.5 | Observe only; Presentation → Application contract; candidate mapping to Twin domains; never Twin authorship |
| **Twin Update Strategy** | Capabilities 4.9.1–4.9.4 | Sole interpreters of Evidence into educational state; Current Twin + Evidence → Successor Twin; never mutate in place; never recommend |
| **Twin Composer** | Capability 4.9.5 | Assembles Domain Strategy Outputs + Current Twin into one immutable Successor Twin; never interprets |
| **Twin Update Coordinator** | Capabilities 4.9.1 / 4.9.5 | Invokes registered Strategies for a composition cycle; does not embed educational interpretation |
| **Educational Intelligence interfaces** | ADR-002 + Epic 2 read path | Readiness → Decision → Recommendation → Mission; consume Twins only; never author Twins from Evidence |
| **Twin Repository contract** | Capability 3.7.3 | Persist whole immutable Twin snapshots; no domain-patch merge authorship |
| **Twin Provider contract** | Capability 3.3 | Retrieve Twin or honest absence; never invent educational state |

### Freeze rules (binding)

1. **Do not reopen Version 1.0 contracts** to “make wiring easier.”  
2. **Do not merge layers** (e.g. Evidence creating Masters, Intelligence writing Twins, Repository composing domains).  
3. **Do not collapse Strategies into Composer** or Composer into Coordinator.  
4. **Do not introduce partial Successor Twins** as temporary scaffolding that Product then relies on.  
5. **Additive deepening only** — richer Strategies, parallel coordination, and plugins must evolve *above* frozen Version 1.0 law.

If implementation discovers an ambiguity, resolve it by reading the frozen architecture — not by inventing a competing model.

---

# 2. Implementation Principles

Every Phase and milestone must obey these principles.

| Principle | Meaning |
|---|---|
| **Small increments** | Prefer a milestone that ships one boundary and proves it over a mega-PR that wires the whole chain untested. |
| **Always executable** | After each milestone, the tree builds/tests; shells and stubs are real callable types with honest no-op or fail-closed behaviour — not commented-out architecture. |
| **Framework-independent Application Layer** | Domain / Application educational logic must not import Flask, SQLAlchemy session globals, or request context. Adapters sit at the edges. |
| **Tests before wiring** | Prove Strategy / Composer / Evidence creation against fixtures *before* Presentation or ORM adapters. |
| **Composition before integration** | Coordinator → Strategies → Composer path exists in-process before Flask end-session wiring or persistence adapters. |
| **No educational shortcuts** | Mission complete ≠ Mid mastery. Thin warrant stays thin. Preservation is lawful. Unknown remains unknown. |
| **Architecture first** | When code and architecture disagree, change the code. Do not silently weaken frozen contracts. |
| **Independently testable** | Each milestone declares its own test surface and succeeds or fails without requiring later Phases. |
| **Stub honestly** | Deferred Strategies return explicit preserve / unavailable postures — never fabricated densification to “look adaptive.” |
| **Curriculum V1/V2 safe** | Twin succession and Evidence identities remain lawful for flat and hierarchical curricula. |

### Anti-patterns (forbidden)

- God coordinator that interprets Evidence  
- Composer that densifies mastery “for completeness”  
- Repository that merges Knowledge patches into live Twins  
- Educational Intelligence that calls Strategies as a side effect of recommendation  
- End-to-end demo that skips unit / composition tests  
- Parallel execution, queues, or retry engines before the synchronous Version 1.0 path is proven  

---

# 3. Implementation Order

Implementation proceeds in fixed Phase order. Do not start Phase N+1 until Phase N’s independent tests pass.

```
Phase A  Shared contracts · Shared types · Coordinator shell · Composer shell
    ↓
Phase B  Knowledge Update Strategy · Framework-free tests · Coordinator wiring · Composer wiring
    ↓
Phase C  Evidence → Coordinator → Knowledge Strategy → Composer → Repository  (end-to-end path)
    ↓
Phase D  Educational Intelligence automatically reads Successor Twin
    ↓
Phase E  Behaviour Strategy
    ↓
Phase F  Performance Strategy
    ↓
Phase G  Goal Strategy
```

---

## Phase A — Shared contracts, types, and shells

**Objective:** Make the frozen write-side spine exist as framework-free types and callable shells — without educational interpretation and without persistence.

| Deliverable | Intent | Independence test |
|---|---|---|
| Shared contract types | Educational Evidence Contract (4.8.4) and Twin Update Strategy Contract (4.9.4) as immutable Application shapes | Structural validation / round-trip fixtures; reject illegal payloads |
| Shared Twin / Evidence types | Current Twin, Successor Twin, Domain Strategy Output, composition cycle identity | Immutability and completeness checks; no Flask imports |
| Twin Update Coordinator shell | Invokes registered Strategies; sequences a composition cycle; does not interpret | With stub Strategies: invoke order + fail-closed when required Strategy missing |
| Twin Composer shell | Current Twin + Domain Strategy Outputs → one immutable Successor Twin or fail closed | Assembles stub outputs; rejects overlapping ownership; never invents domain densification |

**Out of Phase A:** Real Knowledge / Behaviour / Performance / Goal Strategies; Evidence pipeline; Repository persistence; Flask wiring; Intelligence cutover.

**Exit criteria:** Shells compile; unit tests prove contract validation, Composer assembly-from-stubs, and Coordinator fail-closed behaviour. Architecture unchanged.

---

## Phase B — Knowledge Strategy and composition wiring

**Objective:** Ship the first real educational interpreter and prove it composes — still framework-free.

| Deliverable | Intent | Independence test |
|---|---|---|
| Knowledge Update Strategy | Interprets Evidence candidates into Knowledge-owned Domain Strategy Output (or lawful preservation) under Educational Sufficiency honesty | Fixed fixtures: densify only when warranted; preserve otherwise; never recommend; never persist |
| Framework-free Strategy tests | Decision table over Current Twin × Evidence → Domain Strategy Output | Deterministic; no DB; curriculum V1/V2 scope ids safe |
| Coordinator wiring | Registers Knowledge Strategy; invokes it in a composition cycle | Coordinator → Knowledge → Domain Strategy Output |
| Composer wiring | Places Knowledge Domain Strategy Output into Successor Twin; preserves non-owned domains from Current Twin | Whole Successor Twin; non-Knowledge domains unchanged unless Strategy-owned later |

**Version 1.0 catalogue posture:** Knowledge Strategy is the first concrete Strategy. Behaviour / Performance / Goal remain stubs that preserve their domains when registered for composition completeness (or Coordinator/Composer treat unregistered domains as lawful carry-forward from Current Twin — per 4.9.5 ownership / completeness law already frozen).

**Out of Phase B:** Evidence Presentation capture; ORM; Educational Intelligence changes; Behaviour / Performance / Goal educational depth.

**Exit criteria:** Knowledge Strategy + Coordinator + Composer produce a complete immutable Successor Twin in memory for Knowledge-affecting fixtures.

---

## Phase C — Evidence through Repository (end-to-end write path)

**Objective:** Wire the first durable Evidence → Successor Twin path.

```
Educational Evidence
        ↓
Twin Update Coordinator
        ↓
Knowledge Update Strategy
        ↓
Twin Composer
        ↓
Twin Repository
        ↓
persisted Successor Twin
```

| Deliverable | Intent | Independence test |
|---|---|---|
| Evidence pipeline (Version 1.0) | Presentation handoff → structural validation → Educational Evidence creation (observational memory) | Contract acceptance / rejection; Evidence never authors Twin directly |
| Candidate mapping use | Evidence classes offered as candidates per 4.8.5 — Strategies interpret | Mapping does not write conclusions |
| Coordinator composition cycle | Loads Current Twin (Provider / Repository); runs Knowledge Strategy; Composer authors Successor | Fail closed on missing Current Twin or required Strategy |
| Successor Twin persistence | Repository stores whole immutable Successor Twin only | No partial Twin rows; replace-by-snapshot discipline |
| End-to-end write-path tests | Synthetic Evidence → durable Successor Twin → Provider retrieve | Identical inputs → identical Successor Twin (deterministic core) |

**Out of Phase C:** Automatic Intelligence behaviour changes beyond reading the new Twin; Behaviour / Performance / Goal Strategies; retry queues; parallel Strategies.

**Exit criteria:** One Evidence package can lawfully produce one persisted Successor Twin through Coordinator → Knowledge → Composer → Repository, with end-to-end tests green.

---

## Phase D — Educational Intelligence reads Successor Twin

**Objective:** Close the educational loop without giving Intelligence write authority.

```
persisted Successor Twin
        ↓
Twin Provider
        ↓
Educational Intelligence (Readiness → Decision → Recommendation → Mission)
```

| Deliverable | Intent | Independence test |
|---|---|---|
| Provider retrieve after succession | Intelligence / Application always consume latest lawful Twin | Honest absence vs retrieve Successor |
| Application composition update | Orchestration that previously read Twin now reads Successor after Evidence cycles | No Strategy calls inside Decision / Recommendation |
| Recommendation evolution posture | Same Intelligence path; different Twin → different lawful recommendations where warranted | Explainability chain still Attribution → Twin → Evidence lineage |

**Out of Phase D:** Twin Update inside Intelligence; recommendation ranking redesign; Behaviour / Performance / Goal Strategies.

**Exit criteria:** After Phase C succession, Educational Intelligence recommendations reflect the Successor Twin without educational jumps fabricated by wiring.

---

## Phase E — Behaviour Strategy

**Objective:** Add Behaviour as a real domain Strategy under frozen composition law.

| Deliverable | Intent |
|---|---|
| Behaviour Update Strategy | Interprets Behaviour-candidate Evidence; preserves or densifies BehaviourState only |
| Coordinator registration | Behaviour joins Knowledge without Strategies calling each other |
| Composer placement | Behaviour Domain Strategy Output assembled into Successor Twin |
| Framework-free + composition tests | Ownership isolation; no Knowledge densification from Behaviour Strategy |

**Stub remains:** Performance, Goal (and other catalogue entries not yet deepened).

---

## Phase F — Performance Strategy

**Objective:** Add Performance as a real domain Strategy.

| Deliverable | Intent |
|---|---|
| Performance Update Strategy | Interprets Performance-candidate Evidence under assessment / practice honesty |
| Coordinator + Composer wiring | Same composition cycle; single-domain ownership preserved |
| Tests | No second mastery store disguised as Performance; no pass-probability theatre as Strategy authority |

**Stub remains:** Goal (and any still-deferred catalogue entries).

---

## Phase G — Goal Strategy

**Objective:** Complete the Version 1.0 Strategy catalogue depth for Goals.

| Deliverable | Intent |
|---|---|
| Goal Update Strategy | Interprets Goal-candidate Evidence / declared goal posture into GoalState succession |
| Coordinator + Composer wiring | Full multi-Strategy composition under frozen 4.9.5 law |
| Tests | Goals never grant mastery; Goals never short-circuit Recommendation selection |

After Phase G, Version 1.0 Strategy *depth* is complete for Knowledge, Behaviour, Performance, and Goals. Further catalogue entries (e.g. Memory as independent Strategy if not already carried, Confidence separability) remain evolutionary extras unless already required for completeness under frozen ownership maps — implement only if architecture already mandates them; do not invent new owners during implementation.

---

# 4. Version 1.0 Deliverables

Version 1.0 **ships** exactly the following. Everything else remains stubbed or deferred.

| Ships in Version 1.0 | Meaning |
|---|---|
| **Twin Update Coordinator** | Synchronous composition-cycle coordination — not a distributed orchestrator |
| **Twin Composer** | Whole immutable Successor Twin assembly |
| **Knowledge Update Strategy** | First real educational interpreter |
| **Educational Evidence pipeline** | Contract → Evidence creation → candidate posture for Strategies |
| **Successor Twin persistence** | Twin Repository stores composed wholes |
| **Twin Provider read of Successor** | Honest retrieve after succession |
| **Educational Intelligence consumption** | Read path automatically uses Successor Twin (Phase D) |
| **End-to-end tests** | Evidence → Knowledge → Composer → Repository → Provider → Intelligence path |
| **Honest stubs** | Behaviour / Performance / Goal Strategies until Phases E–G; preserve / carry-forward only — no fake densification |

### Explicitly not part of the Version 1.0 *minimum* ship (Phase C/D gate)

Phases E–G deepen Strategies after the end-to-end Knowledge path works. The **Version 1.0 product gate** for Internal Alpha Twin evolution is the Phase C + D path with Knowledge Strategy live. Behaviour / Performance / Goal may follow in-order without redesigning Coordinator / Composer.

### Version 1.0 stack (success shape)

```
Presentation end-of-session observations
        ↓
Educational Evidence Contract → Educational Evidence
        ↓
Twin Update Coordinator
        ↓
Knowledge Update Strategy  (+ honest stubs / carry-forward for other domains)
        ↓
Twin Composer → one immutable Successor Twin
        ↓
Twin Repository (persist whole)
        ↓
Twin Provider (retrieve)
        ↓
Educational Intelligence → Recommendation
```

---

# 5. Deferred Work

The following remain **out of Version 1.0 minimum** and must not delay Phase C/D success.

| Deferred item | Why deferred |
|---|---|
| **Behaviour Strategy** (until Phase E) | Knowledge path proves composition law first |
| **Performance Strategy** (until Phase F) | Independent educational depth after Behaviour |
| **Goal Strategy** (until Phase G) | Completes catalogue after Performance |
| **Parallel Strategy execution** | Synchronous Version 1.0 Coordinator first |
| **Strategy plugins / dynamic discovery** | Closed registration for Version 1.0 |
| **Distributed orchestration** | Single-process composition cycle first |
| **Retry engine** | Fail closed honestly; operational retries later |
| **Background queues / workers** | Invisible Twin evolution may later async; Version 1.0 may be request- synchronous |
| **Conflict-resolution mathematics** | Overlapping ownership is unlawful — not solved by merge math |
| **Partial durable Twins** | Forbidden forever under frozen law — never “temporarily” deferred as a feature |
| **Belief engines (BKT, forgetting curves, rich scoring)** | Strategies interpret conservatively first; deepen mathematics later without contract redesign |
| **AI / tutor observation sprawl** | Version 1.0 Evidence catalogue stays small |
| **Presentation polish / coach phrasing** | Product later; observational honesty first |
| **Redesign of Educational Intelligence selection** | Intelligence already exists; Version 1.0 only feeds Successor Twins |

---

# 6. Testing Strategy

Testing order is fixed. Do not skip layers to force a demo.

```
Unit
  ↓
Composition
  ↓
Coordinator
  ↓
Repository
  ↓
End-to-end
  ↓
Internal Alpha
```

| Layer | What it proves | Typical fixtures |
|---|---|---|
| **Unit** | Contract validation; Strategy Educational Sufficiency / preservation; Composer placement rules; type immutability | Pure Python / domain fixtures; no Flask; no DB |
| **Composition** | Multiple Domain Strategy Outputs assemble into one Successor Twin; ownership isolation | Stub Strategies + real Knowledge; overlapping ownership fails closed |
| **Coordinator** | Registration, invoke order, fail-closed on missing required Strategy / missing Current Twin | In-memory twins; recorded call sequences |
| **Repository** | Whole Successor Twin persist / retrieve; no patch merges | Test DB or fakes implementing Repository contract |
| **End-to-end** | Evidence → … → Provider → Intelligence recommendation changes lawfully | Deterministic fixtures; V1 and V2 curriculum ids |
| **Internal Alpha** | Lived study: recommendations evolve; Twin machinery stays invisible; no educational jumps | Dogfood journal + manual session endings |

### Test discipline (binding)

1. Every Phase must exit with its Independence tests green.  
2. Deterministic educational cores: same Current Twin + same Evidence + same Strategy versions → same Successor Twin.  
3. Negative tests are first-class: illegal contracts, missing Strategy, Composer ownership conflict, partial Twin attempts rejected.  
4. No test may require Intelligence to write Twin state.  
5. Curriculum V1 and V2 both covered wherever topic / scope identities appear.

---

# 7. Internal Alpha Validation

Internal Alpha does **not** validate orchestration machinery. It validates **educational continuity** under Twin evolution.

| Validation focus | Pass signal | Fail signal |
|---|---|---|
| **Recommendations evolve naturally** | After honest study Evidence, next recommendations change when Twin succession warrants | Recommendations thrash without Evidence, or stay frozen despite clear assessment Evidence |
| **No educational jumps** | Thin warrant stays thin; completion alone does not invent Mid/High mastery theatre | Mission complete ⇒ sudden Mid mastery / High readiness |
| **Successor Twins remain explainable** | Lineage: Current Twin + Evidence + Strategy identities attributable | Opaque Twin state; no Evidence / Strategy trail |
| **Evidence captured honestly** | Observations and declared reflection stored as observations | Reflection rewritten as conclusions; session UI cargo stored as Twin belief |
| **Twin evolution invisible** | Student sees better guidance, not Twin Update UI, Strategy toggles, or “your Twin updated” theatre | Students operate Strategies or see internal densification jargon as product |
| **Preservation feels calm** | Thin or insufficient Evidence produces preserved successors without drama | System invents densification to appear adaptive |
| **Intelligence stays read-only on Twins** | Recommendation path never authors Twins | Decision / Mission side effects mutate Twin |

Internal Alpha uses the product journal (`docs/journal/`) for lived observations — not as an architecture change log.

---

# 8. Success Criteria

## 8.1 Version 1.0 implementation succeeds when

```
Educational Evidence
        ↓
Knowledge Update Strategy
        ↓
Successor Twin
        ↓
Twin Repository
        ↓
Educational Intelligence
        ↓
Recommendation
```

works **end-to-end**, with frozen architectural integrity preserved.

## 8.2 Binding checklist

| Criterion | Required |
|---|---|
| Architecture freeze held — no redesign of 4.8 / 4.9 / Repository / Provider / Intelligence write ownership | Yes |
| Evidence observes; Strategies interpret; Composer assembles; Repository stores wholes; Provider retrieves; Intelligence consumes | Yes |
| Knowledge Update Strategy is a real interpreter (not a stub densifier) | Yes |
| Coordinator and Composer exist and remain education-free / interpretation-free respectively | Yes |
| Successor Twin is complete, immutable, and persisted as a whole | Yes |
| Educational Intelligence automatically reads Successor Twin and produces Recommendation without writing Twins | Yes |
| Unit → Composition → Coordinator → Repository → End-to-end tests green | Yes |
| Deferred Strategies / parallelism / queues do not block Version 1.0 gate | Yes |
| No educational shortcuts; preservation lawful; unknown remains unknown | Yes |
| Curriculum V1/V2 succession identities remain lawful | Yes |

## 8.3 Failure modes that mean Version 1.0 did *not* succeed

- Evidence creates or patches Twin domains directly  
- Intelligence authors Twins while recommending  
- Repository merges domain patches as composition  
- Composer densifies educational state  
- End-to-end path only works through a demo script that bypasses contracts  
- “Working” recommendations that depend on fabricated Mid mastery  

---

# 9. Migration and layering notes

| Concern | Version 1.0 posture |
|---|---|
| **Alembic / schema** | Only if Twin Repository / Evidence persistence lack required tables — additive migrations only; documented per implementing milestone |
| **Flask / Presentation** | End-session Evidence capture adapters only at Presentation → Application boundary; no educational math in routes |
| **Application Layer** | Owns coordination of Evidence creation and composition cycle invocation; never owns Strategy interpretation |
| **Domain layer** | Strategies, Composer rules, contract types remain framework-free |
| **Legacy Stage A peers** | Must not become a third Twin truth; no hybrid averaging of legacy progress into Successor Twins |

---

# 10. STOP

This document defines the **Epic 4 implementation roadmap only**.

It does **not** authorise:

- Starting Phase A (or any Phase) code  
- Algorithms or belief-update mathematics  
- Flask / ORM / migration work  
- Architectural redesign of Educational Evidence, Twin Update, Composer, Coordinator, Repository, Provider, or Educational Intelligence  
- Shipping deferred Strategies, parallel execution, plugins, retry engines, or background queues as Version 1.0 blockers  

**Create this plan. Stop before implementation.**

**STOP.**

---

# References

| Artefact | Role |
|---|---|
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Write/read separation; Evidence → Twin → Intelligence |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Platform educational chain |
| [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md) | Application composes; never reasons |
| [`CAPABILITY_4_8_4_EDUCATIONAL_EVIDENCE_CONTRACT.md`](CAPABILITY_4_8_4_EDUCATIONAL_EVIDENCE_CONTRACT.md) | Frozen Evidence handoff |
| [`CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md`](CAPABILITY_4_8_5_EDUCATIONAL_EVIDENCE_TWIN_MAPPING.md) | Candidate observations only |
| [`CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md`](CAPABILITY_4_9_4_TWIN_UPDATE_STRATEGY_CONTRACT.md) | One-Strategy write-side contract |
| [`CAPABILITY_4_9_5_TWIN_UPDATE_STRATEGY_COMPOSITION.md`](CAPABILITY_4_9_5_TWIN_UPDATE_STRATEGY_COMPOSITION.md) | Composer + Coordinator composition law |
| [`CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md`](CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md) | Whole Twin persistence |
| [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md) | Honest Twin retrieve |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Twin immutability law |
| Epic 2 implementation plans (e.g. [`CAPABILITY_2_9_…`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_IMPLEMENTATION_PLAN.md)) | Precedent for incremental, independently testable engineering roadmaps |
