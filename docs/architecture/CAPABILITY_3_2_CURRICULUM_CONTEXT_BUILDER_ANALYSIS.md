# Capability 3.2.4 — CurriculumContextBuilder Analysis

**Status:** Architecture analysis — analysis only  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.2 Integration (CurriculumContextBuilder analysis preceding architecture and implementation)  
**Governing ADR:** [`ADR-001-Curriculum-Hierarchy.md`](ADR-001-Curriculum-Hierarchy.md), [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream orchestration:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md), [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
**Downstream experience:** [`CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md`](CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md)  
**Product law:** [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Scope:** How the application layer should construct immutable CurriculumContext for Educational Orchestration — **no implementation, services, code, schemas, migrations, or UI**

---

## Document purpose

Educational Intelligence domains (Readiness, Decision, Recommendation, Mission) already consume a framework-free **CurriculumContext**: syllabus identity, V1/V2 format tag, ordered topic refs, and section identities when applicable.

That context is a **domain contract**. It is not yet produced by a named product Integration component. Epic 2 completion reviews and orchestration architecture both name the missing piece: a thin **CurriculumContextBuilder** that loads official syllabus truth through canonical Curriculum helpers and emits an immutable CurriculumContext for the orchestrated read path.

This milestone answers **what** CurriculumContextBuilder is for Epic 3 Capability 3.2: an application-layer Integration component — not an Educational Intelligence domain, and not a second syllabus engine.

**Governing principle (binding):**

> **The builder constructs CurriculumContext. It never interprets curriculum as educational reasoning.**

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Database schemas, Alembic migrations, or ORM adapters beyond naming ownership  
- Redesign of Curriculum Engine, `CurriculumService`, or CurriculumContext domain contracts  
- Redesign of Readiness, Decision, Recommendation, Mission, or Twin  
- Caching strategy implementation, UI, or Stage B/C cutover mechanics beyond builder boundaries  

---

# 1. Executive Summary

## Why the builder exists

Educational Orchestration must assemble CurriculumContext before Readiness and Decision can run. Domains must remain framework-free: they must not load ORM curricula, open JSON files, or invent syllabus trees.

Without a builder:

- Routes or orchestrator methods would each invent ad-hoc topic lists and weight maps.  
- V1 flat and V2 hierarchical curricula would diverge across call sites.  
- Plan rows or UI order could be mistaken for official syllabus truth.  
- Domain packages would be pressured to import Flask / SQLAlchemy “just to get topics.”

**CurriculumContextBuilder** exists to:

1. **Load** the student’s target curriculum through canonical Curriculum Engine / `CurriculumService` paths.  
2. **Traverse** syllabus structure only via canonical helpers (`get_topics_flat`, `get_all_topics_ordered`, section helpers — ADR-001).  
3. **Preserve V1 and V2** as first-class formats without Section-global assumptions.  
4. **Construct** one immutable CurriculumContext that domains already contract for.  
5. **Validate** that the result is lawful (identity present, format coherent, traversal complete enough to be a denominator) — or fail honestly.

It does **not**:

- Select next actions, score readiness, package recommendations, or compose missions.  
- Mutate Twin beliefs or write Learning Evidence.  
- Invent topics, reorder syllabus privately, or treat study-plan rows as curriculum truth.  
- Become a parallel Curriculum Engine.

```
Curriculum Engine / CurriculumService   ← syllabus authority
              ↓
   CurriculumContextBuilder             ← application Integration (this analysis)
              ↓
   Immutable CurriculumContext          ← domain contract consumed by EI
              ↓
   Educational Orchestration → Readiness → Decision → …
```

Epic 3 Integration ships the builder so orchestration can wire Twin-first guidance without leaking syllabus loading into domains or inventing educational meaning at the application boundary.

---

# 2. Layer Ownership

Kwalitec Product Integration uses a clear stack:

```
Presentation
     ↓
Application
     ↓
Educational Intelligence Domains
     ↓
Infrastructure
```

| Layer | Responsibility | Curriculum-related role |
|---|---|---|
| **Presentation** | HTTP, auth, templates, forms, client chrome | May request a study day; never builds CurriculumContext or invents topic order |
| **Application** | Product use-cases, orchestration, persistence bridges, Integration adapters | **Owns CurriculumContextBuilder** — load, traverse via helpers, construct, validate |
| **Educational Intelligence Domains** | Evidence, Twin, Readiness, Decision, Recommendation, Mission — framework-independent | **Consume** CurriculumContext; never load ORM/JSON curricula |
| **Infrastructure** | DB, filesystem curriculum JSON, config, runtime | Store and serve raw syllabus artefacts; do not define educational order policy |

## Why CurriculumContextBuilder belongs to the Application Layer

1. **Domains stay framework-free (ADR-002).** CurriculumContext is a frozen domain contract. Building it requires Curriculum Engine / `CurriculumService` / repository access that sit outside `app/domain/`. Application is the lawful place for that bridge.  
2. **Syllabus authority already lives outside EI.** Official structure and weights belong to Curriculum Engine / `CurriculumService` (ADR-001). The builder is Integration wiring to that authority — not a new domain reasoner.  
3. **Orchestration composes; the builder supplies one input.** Educational Orchestration owns lifecycle and ordering. CurriculumContextBuilder owns the specialised construction of CurriculumContext so the orchestrator does not become a god syllabus parser.  
4. **Presentation must not own traversal.** Putting V1/V2 branching in routes recreates the drift ADR-001 forbids.  
5. **Infrastructure must not own meaning.** Loaders and tables hold bytes and rows; the builder maps them into the domain CurriculumContext contract using canonical helpers only.

### Layering consequences

- Blueprints call Application / Orchestration; they do not call CurriculumContextBuilder with invented topic arrays.  
- Domains receive CurriculumContext as an argument; they do not import the builder.  
- Duplicate “quick” context construction in Readiness tests or Decision helpers must not become a second production builder.  
- Plan / mission / progress tables remain learner artefacts — never substitute syllabus truth inside the builder.

Governing restatement:

> **Application builds CurriculumContext from Curriculum authority. Domains reason with it. Presentation only displays results.**

---

# 3. Responsibilities

## 3.1 Own

| Responsibility | Meaning |
|---|---|
| **Curriculum loading** | Resolve and load the target curriculum (engine and/or persisted syllabus) for the requested identity / sitting through canonical load paths — never invent a curriculum. |
| **Canonical traversal** | Obtain ordered topics, sections (when V2), and weights only via Curriculum Engine / `CurriculumService` helpers. No private DFS, no UI sort, no plan-row order. |
| **V1/V2 compatibility** | Emit a format-aware CurriculumContext: V1 flat (no Section hard-requirement); V2 sectioned (section ids and section-aware weights as Curriculum helpers define). Both remain first-class. |
| **CurriculumContext construction** | Map loaded + traversed syllabus truth into the immutable domain CurriculumContext contract (curriculum id, format tag, ordered topic refs, section ids when applicable). |
| **Validation** | Refuse to emit a context that is empty of identity, format-incoherent, or otherwise unlawful for domain consumption; fail closed rather than guessing. |

The builder is a **translator** from Curriculum infrastructure into a domain input. Curriculum Engine remains the musician for syllabus structure; the builder only hands the score to Educational Intelligence.

## 3.2 Never own

| Forbidden ownership | Why |
|---|---|
| **Educational reasoning** | Twin strategies, Readiness Aggregation, and Decision Engine own educational judgement. A builder that “helps” by scoring topics or preferring high-weight actions becomes a parallel intelligence. |
| **Readiness** | Preparedness factors and warrant belong to Readiness Aggregation. The builder supplies syllabus denominator context; it does not compute readiness. |
| **Decision** | Next-action selection belongs solely to Decision Engine. Topic order in CurriculumContext is syllabus order — not a ranked study queue. |
| **Recommendation** | Packaging and narration belong to Recommendation Engine. The builder must not invent titles or student-facing claims. |
| **Mission** | Task composition belongs to Mission Intelligence. The builder must not invent tasks or day plans from syllabus lists. |
| **Twin mutation** | Belief updates belong to Evidence → Twin Update Pipeline (Capability 3.3). The builder is read-path Integration only. |

### Binding vocabulary

| Concept | Owns | Relation to builder |
|---|---|---|
| **Curriculum Engine / `CurriculumService`** | Syllabus structure, order, weights, V1/V2 traversal | Called by builder; never bypassed |
| **CurriculumContextBuilder** | Load → traverse → construct → validate → immutable CurriculumContext | Application Integration |
| **CurriculumContext** | Domain contract for syllabus denominator | Output only; not owned as a mutable store |
| **Educational Orchestration** | Requests context; wires into read path | Caller; does not reimplement builder |
| **Readiness / Decision / Recommendation / Mission** | Educational judgements and projections | Consumers of context; never builders of syllabus truth |
| **Twin** | Learner educational state | Independent input on the read path; builder does not write it |

Governing restatement:

> **The builder answers only: “What is the official syllabus context for this request?” It never answers educational questions about the student.**

---

# 4. Inputs

The builder assembles CurriculumContext from syllabus and product identity inputs. It does not invent educational content for them.

| Input | Role | Boundary |
|---|---|---|
| **Curriculum** | Official syllabus artefact (engine definition and/or persisted curriculum row) for the target sitting. | Loaded via canonical Curriculum paths only. Never synthesised from plan rows, mission history, or Twin topic bags. |
| **Curriculum version** | Format / revision identity needed to load the correct syllabus and tag CurriculumContext as V1 or V2. | Automatic format detection remains centralised in canonical loaders (ADR-001). The builder must not fork a second detect-V1-vs-V2 algorithm. |
| **Student goal (if required)** | Sitting target / curriculum identity linkage when the product request names a goal or sitting that selects which curriculum applies. | Used only to **resolve which curriculum** to load. Goals that encode capacity, pass targets, or remaining time are forwarded by orchestration to domains — not reinterpreted by the builder as syllabus structure. |
| **Configuration** | Environment or product configuration that names default curricula paths, allowed sittings, or load sources. | Configuration selects sources; it must not override official topic order or invent weights. |

### Input assembly principle

```
Curriculum identity (from sitting / goal / request)
      + Curriculum version / format (via canonical load)
      + Configuration (source resolution only)
            ↓
   CurriculumContextBuilder
            ↓
   Immutable CurriculumContext
```

Missing or ambiguous inputs produce honest failure (§6) — not a guessed topic list.

---

# 5. Outputs

The builder returns a **closed output set**.

| Output | Meaning |
|---|---|
| **Immutable CurriculumContext** | Syllabus denominator and weight context for one orchestration / domain derivation: curriculum identity, V1/V2 format tag, ordered topic refs (with weights when known), section ids when format is V2. |

### Explicit non-outputs

The builder must **not** produce as part of its contract:

- ReadinessState, Decision, Recommendation, or Mission  
- Twin snapshots or belief patches  
- Ranked “study priority” lists derived from weights  
- Dashboard view models or Educational Experience components  
- Legacy readiness percentages or hybrid truth  
- Mutable shared curriculum caches presented as domain authority  

> **Nothing else.** If a caller needs educational judgement, that is a domain question — not a builder extension.

Immutability is binding: once emitted, CurriculumContext is a snapshot for the composition pass. Callers must not mutate topic order or weights in place to “fix” UX.

---

# 6. Failure Behaviour

**Product rule (binding):**

> **Fail closed on syllabus truth. Never invent a curriculum so orchestration can continue with false denominators.**

Orchestration depends on this honesty: missing curriculum stops the Twin-first educational chain (Capability 3.2.2 / 3.2.3).

## 6.1 Missing curriculum

| Condition | Builder behaviour |
|---|---|
| Target curriculum cannot be resolved or loaded (unknown sitting, missing file/row, empty identity) | Do not invent topics. Do not emit a partial fake CurriculumContext. |
| Truthful outcome | Explicit failure / absence signal to orchestration so Warnings and Empty-State Guidance can surface blocked guidance. |
| Forbidden | Defaulting to an unrelated curriculum; using another student’s syllabus; fabricating placeholder topic ids. |

## 6.2 Invalid curriculum

| Condition | Builder behaviour |
|---|---|
| Loaded artefact fails validation (corrupt structure, incoherent weights, traversal helpers cannot produce a lawful ordered denominator) | Refuse construction. |
| Truthful outcome | Explicit invalid-curriculum failure; orchestration stops Twin-first chain. |
| Forbidden | Silently dropping broken sections; inventing equal weights to paper over corruption; treating plan coverage as syllabus repair. |

## 6.3 Unsupported version

| Condition | Builder behaviour |
|---|---|
| Curriculum format or revision is not one of the supported V1/V2 contracts the helpers understand | Do not coerce into a guessed format. |
| Truthful outcome | Explicit unsupported-version failure. |
| Forbidden | Private “best effort” parsers; treating unknown hierarchy as flat V1 without canonical detection. |

## 6.4 Graceful failure

Graceful failure means **clear classification for orchestration**, not **soft educational substitutes**.

| Allowed | Forbidden |
|---|---|
| Propagate typed failure classes: missing, invalid, unsupported | Emit empty topic tuples presented as a valid full syllabus |
| Let orchestration compose a valid Educational Experience with Warnings / Empty-State Guidance | Invent Mid readiness or a confident next action despite builder failure |
| Retry after infrastructure recovery with identical input contracts | Bypass canonical helpers “just this once” |

### Failure propagation principle

```
Missing / invalid / unsupported curriculum
        ↓
CurriculumContextBuilder fails closed
        ↓
Orchestrator classifies (missing curriculum)
        ↓
Educational Experience remains truthful (blocked / empty-state)
```

---

# 7. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **Duplicate builders** | Readiness tests, Decision helpers, routes, and orchestration each construct CurriculumContext differently; denominators diverge. | One Application CurriculumContextBuilder for production composition; test fixtures may synthesise contexts but must not become a second product path. |
| **Business logic leakage** | Builder starts ranking topics by “importance,” filtering “too hard” topics, or encoding Decision heuristics into topic lists. | Own construction only; refuse educational algorithms in builder milestones. Topic order is syllabus order. |
| **Curriculum interpretation drift** | Private traversal or weight rules diverge from `CurriculumService` / engine helpers; V1 breaks or V2 section weights are misapplied. | Canonical helpers only (ADR-001); no Section-global assumptions; format tag from lawful detection. |
| **Caching mistakes** | Stale or cross-student CurriculumContext reused; mutated “immutable” contexts shared across requests; cache key ignores version/sitting. | Treat emitted context as immutable snapshots; cache only with explicit identity+version keys if caching is later authorised; never cache across ownership scopes. |

### Risk restatement

The primary danger is not missing a helper method. It is **a builder that starts reasoning** — or **many builders that disagree about what the syllabus is**. Either failure corrupts every downstream Educational Intelligence result that trusts CurriculumContext as denominator.

---

# 8. Recommendations

How CurriculumContextBuilder should proceed after this analysis:

1. **Treat this document as analysis law for Capability 3.2.4** — the builder is Application Integration; it constructs immutable CurriculumContext and introduces no educational authority.  
2. **Proceed Analysis → Architecture → Implementation → Review** (Engineering Charter). Next artefact is a builder *architecture* note: contracts with orchestration, canonical helper boundaries, failure classes — still without domain redesign.  
3. **Keep the builder outside `app/domain/`** — domains continue to consume CurriculumContext; they never load curricula.  
4. **Mandate canonical Curriculum Engine / `CurriculumService` helpers only** for load and traversal; prove V1 and V2 with the same builder entry.  
5. **Emit immutable CurriculumContext and nothing else** — no readiness, decision, recommendation, mission, or Twin side effects.  
6. **Design fail-closed behaviour first** — missing, invalid, and unsupported version must stop Twin-first composition honestly.  
7. **Forbid duplicate production builders** — single Integration entry for orchestration; reject route-local syllabus assembly.  
8. **Separate goal resolution from Goals semantics** — use student goal only to select which curriculum applies; do not reinterpret capacity or pass targets as syllabus structure.  
9. **Defer caching until architecture names keys and invalidation** — prefer correctness over premature shared caches.  
10. **Wire builder before live Twin-first consumers** that need syllabus beyond Decision-carried identities (orchestration architecture recommendation).  
11. **STOP.** This milestone is analysis only. No services. No code. No implementation until an explicit architecture / implementation milestone authorises them.

---

# References

- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md)  
- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
- [`CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md`](CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md)  
- [`ADR-001-Curriculum-Hierarchy.md`](ADR-001-Curriculum-Hierarchy.md)  
- [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
- [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
- [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
- [`CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md`](CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md)  
- [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md)  
- [`ARCHITECTURE.md`](../../ARCHITECTURE.md)

---

**STOP.** Capability 3.2.4 complete as analysis only.
