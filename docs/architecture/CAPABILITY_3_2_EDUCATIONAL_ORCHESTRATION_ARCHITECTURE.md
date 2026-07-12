# Capability 3.2.2 — Educational Orchestration Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.2 Integration (Educational Orchestration architecture preceding implementation)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream analysis:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md)  
**Product law:** [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Companions:** [`CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md`](CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md), [`CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md), [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md), [`CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md)  
**Scope:** Structural architecture for composing completed Educational Intelligence into a product experience — **no code, services, algorithms, schemas, migrations, or tests**

---

## Document purpose

Capability 3.2.1 defined **what** Educational Orchestration is: a thin coordination layer that sequences completed educational domains into product outputs without becoming a second reasoner.

This milestone answers **how** that layer is structured as architecture: responsibilities, dependency graph, contracts, dashboard composition, failure handling, Stage A/B/C product integration, risks, and implementation sequencing — still without redesigning Educational Intelligence (ADR-002).

**Governing principle (binding):**

> **The orchestrator coordinates. It never reasons.**

**Architectural restatement:**

> **Educational Orchestration is application composition.** It wires completed Educational Intelligence components into one product path. It introduces no educational authority.

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Database schemas, Alembic migrations, or ORM adapters  
- Redesign of Evidence, Twin, Readiness, Decision, Recommendation, or Mission  
- UI templates, copy systems, or premium experience design  
- Hybrid legacy + Twin educational formulas  
- Implementation of Stage B/C adapters beyond architectural boundaries  

**Hard architectural rules (binding):**

1. Orchestration never answers educational questions — domains do.  
2. Orchestration never selects, scores, ranks, or invents next actions.  
3. Orchestration never recomputes readiness or coerces unknown / low-warrant / `not_yet_knowable` into Mid or High.  
4. Orchestration never invents curriculum identities, Twin beliefs, or explanation stories.  
5. Orchestration never mutates Twin on the product read path.  
6. Recommendation and Mission remain projections of Decision — never selection authorities.  
7. Curriculum V1 and V2 remain loadable; CurriculumContext comes only from canonical Curriculum helpers.  
8. The student always receives the best **truthful** experience available — never fabricated educational certainty.

---

# 1. Executive Summary

## Orchestration as application composition

Educational Intelligence (v0.5.0) is a complete **platform**: Evidence → Twin → Readiness → Decision → Recommendation → Mission. That stack can answer *what the highest-value next action should be*. It does not yet answer *how the Flask application presents that answer as one calm study day*.

**Educational Orchestration** is the Product Integration composition layer that:

1. Accepts an authorised product request (student, session, surface intent).  
2. Assembles the inputs domains already contract for.  
3. Invokes Educational Intelligence domains in the only lawful order.  
4. Composes domain outputs into dashboard-ready product artefacts.  
5. Propagates failures and thin-warrant postures honestly.

It is **application composition**, not educational reasoning.

```
Completed Educational Intelligence (Epic 2)
              ↓
   Educational Orchestrator     ← composes; does not author
              ↓
   Product experience (Epic 3)
```

Without orchestration, blueprints would invent ordering, context assembly, and error policy; surfaces would wire Twin → Decision inconsistently; and Stage A legacy peers would remain de facto product authority by convenience.

With orchestration, Version 1.0 gains a single product read path whose educational meaning is entirely inherited from completed domains.

Epic 3 replaces **product authority** through wiring and cutover. It does not redesign Educational Intelligence.

---

# 2. Architectural Responsibilities

## 2.1 Own

| Responsibility | Meaning |
|---|---|
| **Lifecycle** | Own the product-request lifecycle for the Twin-first educational read path: start from authorised student context, end with a composed product result (or an honest failure / degraded posture). One request → one ordered composition pass unless an explicit partial refresh contract says otherwise. |
| **Dependency ordering** | Enforce the lawful invocation order so later domains never run without the inputs earlier domains own. Caching may reuse identical inputs; it must not invent alternate educational answers or skip Decision. |
| **Context assembly** | Build and pass shared context domains already require: CurriculumContext (via canonical Curriculum helpers), Twin snapshot load, Goals, Constraints, and product/session facts. Assembly is wiring — not inventing syllabus, beliefs, or capacity policy. |
| **Error propagation** | Surface missing Twin, cold start, missing curriculum, domain failures, and thin warrant upward without replacing them with fabricated confident substitutes. Partial success is allowed only when remaining outputs stay truthful. |
| **View model composition** | Map domain outputs into product-facing projections (Today’s Recommendation, Today’s Mission, Readiness summary, Explainability, Progress hooks) without adding educational meaning, re-ranking, or hybrid averages. |

Orchestration is a **conductor**. Domains remain the musicians.

## 2.2 Never own

| Forbidden ownership | Why |
|---|---|
| **Educational reasoning** | Twin strategies, Readiness Aggregation, and Decision Engine own educational judgement. Orchestration that “helps” by scoring or choosing becomes a parallel intelligence. |
| **Scoring** | No readiness composites, priority scores, engagement heuristics, or legacy % averages inside the orchestrator. |
| **Decision** | Next-action selection, candidate sets, and reason codes belong solely to Decision Engine. Orchestration must not re-rank, filter by UX preference, or substitute legacy recommendation lists. |
| **Recommendation** | Packaging, titles, explanation affordances, and warrant-bound narration belong to Recommendation Engine. Orchestration may request packaging; it must not invent student-facing educational claims. |
| **Mission logic** | Task composition, Decision-binding, and feasibility-shaped execution belong to Mission Intelligence. Orchestration must not invent filler tasks, private priority scores, or a second day plan. |
| **Curriculum interpretation** | Syllabus identities, order, and weights belong to Curriculum Engine / `CurriculumService`. Orchestration builds CurriculumContext through those helpers only — never invents topics or treats plan rows as curriculum truth. |

### Binding vocabulary

| Concept | Owns | Relation to orchestration |
|---|---|---|
| **Educational Orchestration** | Lifecycle, order, context assembly, composition, errors | Product Integration concern |
| **CurriculumContextBuilder** | Syllabus context via canonical helpers | Called by orchestration; never bypassed |
| **TwinRepository** | Durable Twin snapshot load (Application persistence adapter) | Called for read; never mutated on this path |
| **Readiness Aggregation** | Derived preparedness judgement | Called; results forwarded |
| **Decision Engine** | Highest-value next action | Called; sole selection authority |
| **Recommendation Engine** | Decision packaging | Called; projection only |
| **Mission Intelligence** | Decision operationalisation | Called; execution / projection only |
| **Legacy readiness / recommendation / mission services** | Stage A product peers | Must not be Twin-first authority inside the orchestrator |

Governing restatement:

> **Orchestration never answers educational questions. It only ensures the owners of those questions are asked in the right order, with the right inputs, and that their answers reach the product intact.**

---

# 3. Dependency Graph

The product read path dependency graph is:

```
Dashboard
   ↓
Educational Orchestrator
   ↓
CurriculumContextBuilder
TwinRepository
ReadinessAggregation
DecisionEngine
RecommendationEngine
MissionIntelligence
```

## 3.1 Graph meanings

| Node | Role in the graph |
|---|---|
| **Dashboard** | Product consumer. Requests a composed study-day projection. Must not call educational domains directly or invent ordering. |
| **Educational Orchestrator** | Sole composition entry for Twin-first educational surfaces on this path. Owns lifecycle and wiring; owns none of the educational math. |
| **CurriculumContextBuilder** | Application/curriculum boundary that produces CurriculumContext via canonical Curriculum helpers (V1 and V2 first-class). |
| **TwinRepository** | Application persistence adapter that loads the authoritative Twin snapshot for the student / sitting. Outside domain packages; domains stay framework-free. |
| **ReadinessAggregation** | Domain preparedness derivation from Twin + CurriculumContext + Goals. |
| **DecisionEngine** | Domain next-action selection — sole educational selection authority on this path. |
| **RecommendationEngine** | Domain packaging / projection of Decision. |
| **MissionIntelligence** | Domain execution / projection of Decision into today’s Mission / MissionTask set. |

## 3.2 Lawful invocation order

Dependency edges imply a **strict educational order**. Orchestration may load CurriculumContext and Twin in either sequence relative to each other (both are inputs), but must not invoke later reasoning without earlier results:

```
CurriculumContextBuilder  →  CurriculumContext
TwinRepository            →  Twin snapshot (read)
        ↓
ReadinessAggregation      →  ReadinessState
        ↓
DecisionEngine            →  Decision
        ↓
RecommendationEngine      →  Recommendation
MissionIntelligence       →  Mission
        ↓
Educational Orchestrator  →  composed Dashboard view model
        ↓
Dashboard
```

### Graph invariants

1. **Dashboard depends on Orchestrator**, not on individual engines.  
2. **Recommendation and Mission depend on Decision**, never the reverse.  
3. **Decision depends on Readiness** (as preparedness context), Twin, CurriculumContext, Goals, and Constraints.  
4. **No parallel educational authority** — legacy peers are not nodes inside this Twin-first graph.  
5. **No Twin write edges** on this graph — belief mutation belongs to Evidence → Twin Update Pipeline (Capability 3.3), not dashboard composition.  
6. **Progress** on the dashboard is a composition of forwarded educational state (Twin / readiness / evidence summaries) — not a sixth reasoner hanging off the orchestrator.

---

# 4. Contracts

Contracts are structural, not code. They define what each layer may ask for and what it may return.

```
Application
   ↓
Orchestrator
   ↓
Educational Domains
```

## 4.1 Application → Orchestrator

**Application** (product use-cases, blueprint-facing services, persistence bridges) may request a composed educational product result for an authorised student and sitting.

| Application provides | Meaning |
|---|---|
| **Authorised student scope** | Identity and ownership already validated; orchestration never loads other users’ state. |
| **Sitting / goal context** | Exam target, remaining time, capacity intent domains already consume as Goals. |
| **Constraints** | Session bounds and sustainability limits that shape feasibility — not educational priority. |
| **Product context** | Surface intent (dashboard vs mission path), locale/copy channel, and named cutover mode (Stage A/B/C) when relevant. |
| **Persistence bridges** | Ability for orchestration to ask TwinRepository / later journal adapters — Application owns adapters; domains stay free of Flask/ORM. |

| Orchestrator returns | Meaning |
|---|---|
| **Composed product result** | Closed set: Recommendation, Mission, Readiness projection, Explainability payload, Dashboard view model (and Progress hooks when requested). |
| **Honesty posture** | Explicit cold-start / thin-warrant / partial-failure signals so Application and UI do not invent Mid/High theatre. |
| **Failure classification** | Missing Twin, missing curriculum, domain failure, or degraded composition — never a silent confident fake. |

**Application must not:**

- Call Decision, Recommendation, or Mission engines with ad-hoc route arguments that skip orchestration.  
- Average legacy readiness % with Twin-first factors “for the dashboard.”  
- Mutate Twin, readiness, or mastery from accept / dismiss / complete handlers on this read path.  
- Treat Stage A legacy outputs as Twin-first truth while claiming Stage C behaviour.

## 4.2 Orchestrator → Educational Domains

Orchestrator invokes domains with the contracts those architectures already define. It does not invent new educational inputs.

| Downstream | Orchestrator supplies | Orchestrator accepts | Orchestrator must not |
|---|---|---|---|
| **CurriculumContextBuilder** | Student sitting / curriculum identity needed to build context | CurriculumContext (V1 or V2 safe) | Invent topics, reorder syllabus privately, or treat plan rows as curriculum truth |
| **TwinRepository** | Student / sitting identity for snapshot load | Twin snapshot or explicit absence | Fabricate a Twin; mutate beliefs; treat empty as Mid preparedness |
| **ReadinessAggregation** | Twin + CurriculumContext + Goals | ReadinessState with warrant / unknown honesty | Recompute factors; coerce unknown to Mid/High; select next actions |
| **DecisionEngine** | Twin + CurriculumContext + Goals + Constraints + ReadinessState (+ optional journal history context) | Decision (selected action, candidates, reason codes, lineage, warrant posture) | Re-rank candidates; substitute legacy lists; strip reason codes |
| **RecommendationEngine** | Decision (+ communication / packaging context) | Recommendation (attributable packaging) | Invent titles or claims that disagree with Decision; become selection authority |
| **MissionIntelligence** | Decision / Decision batch + Goals + Constraints (+ optional Recommendation language hooks) | Mission / MissionTask set | Invent filler under leftover capacity; re-select educational value |

### Contract firewall

```
Application asks for product composition
        ↓
Orchestrator asks domains educational questions
        ↓
Domains answer with warrant-honest educational artefacts
        ↓
Orchestrator forwards answers intact into product projections
```

Nothing in Application or Orchestrator may invent a second answer to an educational question a domain already owns.

---

# 5. Dashboard Composition

Dashboard surfaces are **projections of composed domain outputs**. Composition places artefacts; it does not create educational meaning.

## 5.1 From domain outputs to product artefacts

| Dashboard artefact | Source of educational truth | Orchestration role |
|---|---|---|
| **Today’s Recommendation** | Recommendation Engine packaging of Decision | Forward Recommendation; place as primary next-action suggestion; preserve Decision attribution and warrant tone |
| **Today’s Mission** | Mission Intelligence operationalisation of Decision | Forward Mission / MissionTask set; place as today’s executable work; preserve Decision binding |
| **Readiness summary** | Readiness Aggregation ReadinessState | Forward factorable posture and warrant; never recompute or average with legacy % |
| **Explainability** | Decision reason codes + lineage (+ readiness citations when Decision cites readiness); Recommendation narration hooks | Preserve and surface chain-supported *why*; never invent post-hoc stories |
| **Progress** | Twin / evidence / readiness projections already authorised as product summaries (not a new scorer) | Compose honest progress cues from forwarded state; never invent mastery theatre from absence |

## 5.2 Composition rules (no educational logic)

1. **Place, do not author.** If Decision selected revise-topic-X, Recommendation and Mission already carry that meaning; the dashboard shows them.  
2. **One next-action story.** Today’s Recommendation and Today’s Mission must not disagree with Decision. If they would, composition failed — do not “fix” by inventing a third story.  
3. **Warrant travels.** Cold-start and thin-warrant postures survive into visible honesty (language, confidence affordances, progressive disclosure) — not into fabricated Mid/High readiness.  
4. **Explainability is mandatory cargo.** Stripping reason codes to “simplify” the first viewport is an orchestration failure; progressive disclosure may hide detail, not delete lineage.  
5. **Progress is not selection.** Progress cues summarise what is known; they do not choose what to study next.  
6. **Closed set.** Version 1.0 educational authority on this path is the composed set above — not streak theatre, competing next-action panels, or opaque composites.

```
Decision
   ├─→ Recommendation  →  Today’s Recommendation
   ├─→ Mission         →  Today’s Mission
   ├─→ reason codes    →  Explainability
   └─→ (cites)
ReadinessState         →  Readiness summary
Twin / evidence hooks  →  Progress (honest, non-authoritative for selection)
        ↓
Dashboard View Model   ← composition only
```

---

# 6. Failure Handling

**Product rule (binding):**

> **The student should always receive the best truthful experience available. Never fabricate educational certainty.**

Orchestration prefers a smaller honest surface over a complete false one.

## 6.1 Missing Twin

| Condition | Orchestration behaviour |
|---|---|
| Twin snapshot cannot be loaded (no persistence yet, corrupt load, or explicit absence) | Do not invent a Twin. Do not invent Mid/High readiness or a confident next action. |
| Truthful experience | Surface an honest empty / cold-start product posture: diagnostic or evidence-creating guidance only if Decision Engine can produce it from domain-defined empty-state contracts; otherwise a clear “not yet knowable” product state. |
| Forbidden | Fabricated Twin beliefs; legacy % presented as Twin-first truth; motivational theatre pretending preparedness is known. |

## 6.2 Cold start

| Condition | Orchestration behaviour |
|---|---|
| Twin exists but evidence density is sparse / domains empty / warrant thin | Forward cold-start and low-warrant postures from Readiness and Decision intact. |
| Truthful experience | Allow Decision’s cold-start policy (e.g. diagnostic / evidence-creating actions) to reach Recommendation and Mission. Keep readiness summary unknown/honest. |
| Forbidden | Coercing unknown readiness to Mid; inventing High confidence packaging; filling Mission with unauthored educational tasks. |

## 6.3 Missing curriculum

| Condition | Orchestration behaviour |
|---|---|
| CurriculumContextBuilder cannot produce a lawful CurriculumContext (missing sitting, unloadable syllabus, V1/V2 helper failure) | Stop the Twin-first educational chain. Do not invent topics or treat plan rows as curriculum truth. |
| Truthful experience | Product-safe error / blocked posture: student sees that guidance cannot be built without official syllabus context. |
| Forbidden | Private topic lists, ad-hoc reorderings, or “best guess” curriculum identities inside orchestration. |

## 6.4 Partial failures

| Condition | Orchestration behaviour |
|---|---|
| Early stages succeed; a later stage fails (e.g. Readiness ok, Decision fails; Decision ok, Mission fails) | Propagate the failure class. Compose from what remains only when remaining artefacts stay educationally consistent. |
| Examples of truthful partial composition | Readiness summary alone when Decision cannot run; Recommendation without Mission when Mission Intelligence fails — provided the product does not imply a full study day that Decision did not author. |
| Forbidden | Substituting legacy recommendation lists for a failed Decision; inventing Mission filler to avoid an empty day; presenting Progress as if Decision succeeded. |

## 6.5 Graceful degradation

Graceful degradation means **reducing claims**, not **replacing truth**.

| Degradation mode | Allowed | Forbidden |
|---|---|---|
| **Reduce surface** | Show fewer panels; emphasise honesty and next evidence-creating step | Show complete dashboard with fabricated certainty |
| **Preserve warrant** | Keep unknown / low-warrant language visible | Quietly upgrade warrant for UX polish |
| **Named dual truth (Stage B only)** | Explicitly label legacy vs Twin-first when cutover mode requires it | Market Stage B as Twin-first Version 1.0; average legacy % with Twin factors |
| **Retry / reload** | Re-run composition with identical contracts after persistence recovery | Skip Decision “just this once” to unblock UI |

### Failure propagation principle

```
Domain failure or thin warrant
        ↓
Orchestrator classifies and forwards
        ↓
Application / Dashboard reduces claims
        ↓
Student sees best truthful experience available
```

---

# 7. Product Integration

Orchestration is the Integration spine for Stage A → B → C cutover. Cutover changes **which product authority students receive**, not Educational Intelligence domain design.

## 7.1 Stage A — Named dual truth (current platform reality)

| Property | Architecture posture |
|---|---|
| **Educational domains** | Exist in `app/domain/`; framework-independent; not yet product authority on live surfaces. |
| **Live product peers** | Legacy `ReadinessService`, `RecommendationService`, planning / ORM mission paths remain what students actually consume. |
| **Orchestrator role** | May exist as a non-authoritative composition path for engineering validation — must not be marketed as Twin-first Version 1.0. |
| **Rule** | Name Stage A honestly. Freeze deepening of legacy heuristics as Twin-first truth. |

## 7.2 Stage B — Named dual-truth adapters

| Property | Architecture posture |
|---|---|
| **Product path** | Orchestrator becomes the Twin-first composition entry; adapters may still expose legacy peers for comparison or fallback **explicitly named** as dual authority. |
| **Dashboard** | May show Twin-first composition behind feature flags / adapter modes; dual-authority debug views are engineering-only. |
| **Rule** | Never average legacy percentages with Twin / Decision factors. Never present hybrid scores as a single preparedness truth. |
| **Orchestrator duty** | Keep Twin-first graph pure. Legacy peers are not nodes inside the Orchestrator dependency graph; adapters sit beside it at the Application boundary. |

## 7.3 Stage C — Single product educational authority

| Property | Architecture posture |
|---|---|
| **Product path** | Dashboard and Version 1.0 educational surfaces consume Orchestrator composition only. |
| **Authority** | Readiness Aggregation, Decision, Recommendation packaging, and Mission Intelligence are product educational authority for daily guidance. |
| **Legacy** | Legacy readiness / recommendation / daily-mission selection peers retire as product educational authority (Planning may remain multi-day WeekPlan / exam-date owner without claiming daily next-action authority). |
| **Rule** | Version 1.0 Twin-first claims require Stage C on student paths. |

## 7.4 Legacy cutover

| Legacy product peer | Twin-first authority after cutover | Orchestration rule |
|---|---|---|
| `ReadinessService` (% / coverage composites as preparedness truth) | Readiness Aggregation projections | Forward domain readiness only on Twin-first path; no hybrid averages |
| `RecommendationService.generate_recommendations` | Decision → Recommendation packaging | Decision selects; packaging narrates; legacy ceases as next-action authority |
| Mission optimizer / legacy mission generation | Decision → Mission Intelligence | Mission executes Decision; no filler under leftover capacity |
| `PlanningService` as daily next-action / mission authority | Loses dual claim on Twin-first daily selection | Planning ≠ Decision; cutover targets daily authority, not deletion of exam-date planning |
| Direct UI mastery / readiness writes | Forbidden | Accept / dismiss / complete become Evidence on write path (Capability 3.3), not orchestrator side effects |

### Cutover invariants

1. Progressive cutover — not big-bang deletion before Stage B adapters exist.  
2. Orchestration before live Twin-first UI claims.  
3. Write/read firewall preserved at every stage.  
4. Communications honesty: do not market Stage A or partial Stage B as Twin-first Version 1.0.

---

# 8. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **God Service** | One orchestrator accumulates scoring, selection, packaging, mission packing, and persistence until it recreates the monolithic Recommendation Service ADR-002 rejected. | Keep orchestrator thin: lifecycle, order, context, composition, errors only. Refuse new educational algorithms in orchestration milestones. |
| **Hidden educational logic** | “Temporary” re-ranking, Mid defaults, or copy-driven overrides land in orchestration or routes “for UX.” | Architecture review gate: if a method selects, scores, or invents tasks, it is out of scope. Product copy consumes domain outputs — it does not override them. |
| **Performance bottlenecks** | Sequential over-fetching, repeated Twin loads, or full-pipeline work on every partial UI refresh makes the calm daily path feel heavy — a trust issue. | Compose once per product request; reuse snapshots for identical inputs; optimise wiring without collapsing domain boundaries or skipping Decision. |
| **Domain leakage** | Domains import Flask/ORM, or Application / Orchestrator reimplements readiness / decision math. | Preserve ADR-002 boundaries: domains framework-free; persistence adapters in Application; educational math only in domain owners. |
| **Parallel authority** | Dashboard uses Twin-first Decision while missions or progress still use Stage A planning / readiness %; students see conflicting “today” stories. | Bind all Version 1.0 educational surfaces to the same orchestrated chain; dual truth must be named (Stage B) and time-boxed; Stage C before Twin-first Version 1.0 claims. |

### Risk restatement

The primary danger is not missing a feature. It is **orchestration that starts reasoning** — or product surfaces that bypass orchestration and recreate parallel truth. Either failure reintroduces the study-planner pathology Epic 2 was built to end.

---

# 9. Recommendations

How Educational Orchestration implementation should proceed after this architecture:

1. **Treat this document as architecture law for Capability 3.2.2** — orchestration is application composition; it introduces no educational authority. Do not reopen ADR-002’s educational chain.  
2. **Proceed Architecture → Implementation → Review** (Engineering Charter). Next artefact is an explicit implementation milestone — this note authorises none of the code.  
3. **Implement a single product read-path entry** that realises Dashboard → Orchestrator → domain graph before any Twin-first UI claims.  
4. **Ship CurriculumContextBuilder via canonical Curriculum helpers first** so V1/V2 safety is proven at the orchestration boundary.  
5. **Wire TwinRepository load as a read-only Application adapter** outside domain packages; prove missing-Twin honesty before inventing fallbacks.  
6. **Wire Readiness → Decision → Recommendation → Mission as one composed path**; never expose Recommendation or Mission as selection authorities.  
7. **Compose the closed dashboard set only** (Today’s Recommendation, Today’s Mission, Readiness summary, Explainability, Progress hooks). Reject “just one more” educational side channel.  
8. **Design failure and cold-start propagation first** so thin warrant and missing inputs survive into product language — best truthful experience, never fabricated certainty.  
9. **Preserve write/read firewall** — dashboard orchestration must not mutate Twin; completion / accept / dismiss become Evidence in Capability 3.3 workstreams.  
10. **Cut over Stage A → Stage B → Stage C** with named dual-truth adapters; freeze legacy heuristic deepening; no hybrid averages; Stage C before Version 1.0 Twin-first marketing.  
11. **Guard against God Service and hidden educational logic** in architecture review: selection, scoring, and mission invention remain domain-owned.  
12. **Measure perceived latency on the daily path** as a trust concern once implementation begins — optimise composition, not by collapsing domains.  
13. **STOP.** This milestone is architecture only. No services. No code. No tests. No implementation until an explicit implementation milestone authorises them.

---

# References

- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md)  
- [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
- [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
- [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
- [`CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md`](CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md)  
- [`CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md)  
- [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md)  
- [`CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md)  
- [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md)  
- [`ARCHITECTURE.md`](../../ARCHITECTURE.md)

---

**STOP.** Capability 3.2.2 complete as architecture only.
