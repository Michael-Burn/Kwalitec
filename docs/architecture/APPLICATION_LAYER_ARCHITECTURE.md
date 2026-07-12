# Capability 3.2.5 — Application Layer Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.2 Integration (Application Layer architecture preceding implementation)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream orchestration:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md), [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
**Upstream experience contract:** [`CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md`](CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md)  
**Upstream builder analysis:** [`CAPABILITY_3_2_CURRICULUM_CONTEXT_BUILDER_ANALYSIS.md`](CAPABILITY_3_2_CURRICULUM_CONTEXT_BUILDER_ANALYSIS.md)  
**Product law:** [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Scope:** Responsibilities of the Application Layer that composes Educational Intelligence into product experiences — **no code, services, algorithms, schemas, migrations, or tests**

---

## Document purpose

Capability 3.2.1–3.2.4 defined orchestration purpose, orchestration structure, the Educational Experience Contract, and CurriculumContextBuilder analysis.

This milestone defines the **Application Layer** as a whole: the Integration tier that owns coordination between Presentation and Educational Intelligence Domains — without owning educational reasoning.

**Governing principle (binding):**

> **The Application Layer composes. It never reasons.**

**Architectural restatement:**

> **Application owns coordination. Educational Intelligence owns judgement. Presentation owns display. Infrastructure owns persistence and runtime.**

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Database schemas, Alembic migrations, or ORM adapters beyond naming ownership  
- Redesign of Evidence, Twin, Readiness, Decision, Recommendation, or Mission  
- UI templates, copy systems, or premium experience design  
- Implementation of Stage B/C adapters beyond layer boundaries  

---

# 1. Executive Summary

## Purpose of the Application Layer

Educational Intelligence (Epic 2 / v0.5.0) is a complete **platform**: Evidence → Twin → Readiness → Decision → Recommendation → Mission. Domains answer educational questions. They do not present a study day, load ORM Twin rows, or speak Flask.

Presentation (blueprints, templates, future clients) must not invent ordering, syllabus context, or educational meaning.

The **Application Layer** is the Epic 3 Integration tier between those worlds. It:

1. Accepts authorised product requests from Presentation.  
2. Assembles lawful inputs domains already contract for.  
3. Invokes Educational Intelligence in the only lawful order.  
4. Bridges persistence and curriculum loading without leaking frameworks into domains.  
5. Composes domain outputs into the Educational Experience Contract / view models.  
6. Propagates failures and thin-warrant postures honestly.

It owns **coordination**. It never owns **educational reasoning**.

```
Presentation (Web · Mobile · Desktop · API)
              ↓
        Application Layer     ← composes; does not author
              ↓
 Educational Intelligence Domains
              ↓
        Infrastructure
```

Without Application:

- Routes would wire Twin → Decision inconsistently.  
- Domains would be pressured to import Flask / SQLAlchemy.  
- Each client would invent its own experience shape.  
- Stage A legacy peers would remain de facto product authority by convenience.

With Application, Version 1.0 gains one Integration spine whose educational meaning is entirely inherited from completed domains. Epic 3 replaces **product authority** through wiring and cutover. It does not redesign Educational Intelligence (ADR-002).

---

# 2. Layer Hierarchy

Kwalitec Product Integration uses a strict four-layer stack:

```
Presentation
     ↓
Application
     ↓
Educational Intelligence Domains
     ↓
Infrastructure
```

| Layer | Responsibility | Must not |
|---|---|---|
| **Presentation** | Auth, HTTP / client chrome, templates or native UI, forms, progressive disclosure of the Experience Contract | Call domains directly; build CurriculumContext; score, select, or invent educational claims |
| **Application** | Product use-cases, orchestration, builders, repositories, assemblers, write-path recording bridges, workflow coordination | Own educational math; become a second Decision / Readiness / Mission engine |
| **Educational Intelligence Domains** | Evidence, Twin, Readiness, Decision, Recommendation, Mission — framework-independent educational judgement and projection | Import Flask / ORM / presentation; load syllabus privately; depend on Application |
| **Infrastructure** | Database, filesystem curriculum JSON, config, runtime hosting | Contain educational scoring, selection, recommendation, or mission logic |

### Hierarchy invariants

1. **Calls flow downward only** for educational composition: Presentation → Application → Domains → Infrastructure.  
2. **Domains never depend on Application** — Application depends on Domains.  
3. **Presentation never bypasses Application** for Twin-first educational surfaces.  
4. **Infrastructure never contains educational logic** — it stores and serves artefacts; Application and Domains interpret contracts.

Governing restatement:

> **Presentation displays. Application coordinates. Domains reason. Infrastructure stores.**

---

# 3. Application Components

Components are architectural roles. This section does **not** define classes, modules, or APIs.

## 3.1 EducationalOrchestrator

**Role:** Sole composition entry for the Twin-first educational product read path.

**Owns:** Request lifecycle, lawful invocation order, shared context assembly requests, error classification / propagation, forwarding of domain outputs into the Experience Contract.

**Does not own:** Scoring, selection, packaging invention, mission invention, Twin mutation on the read path.

**Relation:** Conductor. Calls builders, repositories, and Educational Intelligence domains; returns composed experience to Presentation via assemblers.

Binding law (Capability 3.2.2): *The orchestrator coordinates. It never reasons.*

## 3.2 CurriculumContextBuilder

**Role:** Application / Curriculum boundary that produces immutable CurriculumContext for orchestration.

**Owns:** Load → traverse (canonical Curriculum helpers only) → construct → validate → emit CurriculumContext (V1 and V2 first-class).

**Does not own:** Syllabus authority (Curriculum Engine / `CurriculumService`), educational ranking of topics, readiness denominators beyond supplying official structure.

**Relation:** Called by EducationalOrchestrator before Readiness / Decision. Never bypassed by Presentation. Domains consume CurriculumContext as an argument; they never import the builder.

## 3.3 TwinRepository

**Role:** Application persistence adapter for durable Twin snapshot load (and, on separate write paths, persistence bridges — not dashboard side effects).

**Owns:** Mapping between storage and the Twin snapshot domains already contract for; explicit absence signalling when no Twin exists.

**Does not own:** Twin belief strategies, K→M→B→P update math, fabricated Mid preparedness when empty.

**Relation:** Outside domain packages so Domains stay framework-free. Read path is load-only; belief mutation belongs to Evidence → Twin Update Pipeline (Capability 3.3), not dashboard composition.

## 3.4 EvidenceRecorder

**Role:** Application write-path bridge that records Learning Evidence from product actions (accept, dismiss, complete, diagnostics, session outcomes).

**Owns:** Translating authorised product events into Evidence artefacts domains contract for; ensuring writes do not invent Twin beliefs or next-action selection.

**Does not own:** Twin update strategies, readiness recomputation as a side effect of UI clicks, Decision selection.

**Relation:** Complements the read-path orchestrator. Presentation reports actions; EvidenceRecorder records; Twin Update Pipeline (domain + later Integration) updates beliefs. Dashboard orchestration must not mutate Twin.

## 3.5 DashboardAssembler

**Role:** Maps composed domain outputs into the closed Educational Experience Contract / dashboard view model Presentation may render.

**Owns:** Placement of Today's Recommendation, Today's Mission, Readiness Summary, Progress Snapshot, Explainability, Warnings, Empty-State Guidance, Metadata — without adding educational meaning.

**Does not own:** Re-ranking Decision, inventing filler missions, averaging legacy % with Twin factors, stripping warrant for polish.

**Relation:** Downstream of EducationalOrchestrator composition. Surfaces consume the assembled Experience; they do not reassemble educational truth.

## 3.6 Future Builders

**Role:** Additional thin Application constructors that emit immutable domain-ready inputs when new Integration needs appear (e.g. Goals / Constraints packaging from product sitting facts, Decision Journal load adapters, communication-channel context).

**Owns:** Specialised construction and validation of one input contract.

**Does not own:** Educational judgement about that input.

**Discipline:** Prefer few builders with clear contracts over many ad-hoc constructors. Each builder answers one construction question. Duplicate “quick” builders must not become parallel product paths.

## 3.7 Future Assemblers

**Role:** Additional thin Application mappers from composed domain outputs to surface-specific projections that still honour the Educational Experience Contract (e.g. mission-detail assembler, explainability-detail assembler, API serialisation projection).

**Owns:** Shape and progressive-disclosure packaging for a named surface family.

**Does not own:** New educational claims, alternate next-action stories, or client-local Decision overrides.

**Discipline:** Assemblers may differ by platform presentation needs; they must not diverge in educational meaning. One Decision-backed day remains one story across Web, Mobile, Desktop, and API.

### Component map

```
Presentation
     ↓
EducationalOrchestrator
     ├─ CurriculumContextBuilder  → CurriculumContext
     ├─ TwinRepository            → Twin snapshot (read)
     ├─ (Future Builders)         → Goals / Constraints / journal context …
     ├─ Educational Intelligence Domains (Readiness → Decision → Recommendation → Mission)
     ├─ DashboardAssembler        → Educational Experience Contract
     └─ (Future Assemblers)       → surface projections
EvidenceRecorder                  → Learning Evidence (write path; separate from dashboard read)
```

---

# 4. Responsibilities

## 4.1 Own

| Responsibility | Meaning |
|---|---|
| **Composition** | Wire completed Educational Intelligence into one product path; produce the Experience Contract from domain answers intact. |
| **Ordering** | Enforce lawful invocation order so later domains never run without earlier inputs; never invent alternate educational order for UX convenience. |
| **Context creation** | Build and pass CurriculumContext, Twin load, Goals, Constraints, and product/session facts domains already require — wiring, not inventing syllabus, beliefs, or capacity policy. |
| **Repository access** | Own persistence adapters (TwinRepository and later journal / evidence stores) so Domains remain free of Flask / ORM. |
| **View model assembly** | Map domain outputs into Experience Contract / dashboard projections via assemblers without adding educational meaning. |
| **Workflow coordination** | Own product-request lifecycle for Twin-first read paths and authorised write recording (EvidenceRecorder) without collapsing read/write firewalls. |

Application is a **conductor and bridge**. Domains remain the musicians.

## 4.2 Never own

| Forbidden ownership | Why |
|---|---|
| **Educational reasoning** | Twin strategies, Readiness Aggregation, and Decision Engine own educational judgement. Application that “helps” by scoring or choosing becomes a parallel intelligence. |
| **Scoring** | No readiness composites, priority scores, engagement heuristics, or legacy % averages inside Application. |
| **Decision logic** | Next-action selection, candidate sets, and reason codes belong solely to Decision Engine. |
| **Recommendation logic** | Packaging, titles, and warrant-bound narration belong to Recommendation Engine. |
| **Mission logic** | Task composition, Decision-binding, and feasibility-shaped execution belong to Mission Intelligence. |
| **Curriculum ownership** | Syllabus identities, order, and weights belong to Curriculum Engine / `CurriculumService`. Application builds CurriculumContext through those helpers only. |
| **Twin ownership** | Learner educational state and update strategies belong to Twin / Twin Update Pipeline. Application loads and persists; it does not author beliefs. |

### Binding vocabulary

| Concept | Layer | Relation to Application |
|---|---|---|
| **EducationalOrchestrator** | Application | Composition entry; no educational math |
| **CurriculumContextBuilder** | Application | Syllabus context construction via Curriculum authority |
| **TwinRepository** | Application | Persistence adapter; read-path load |
| **EvidenceRecorder** | Application | Write-path Evidence bridge |
| **DashboardAssembler** | Application | Experience / view-model placement |
| **Readiness / Decision / Recommendation / Mission** | Domains | Called; results forwarded |
| **Curriculum Engine** | Curriculum authority (outside EI domains) | Called by builder; never reimplemented |
| **Twin** | Domain educational state | Loaded / persisted; never reasoned about in Application |

Governing restatement:

> **Application answers only: “How do we ask the right educational owners, in order, and deliver their answers intact?” It never answers educational questions about the student.**

---

# 5. Dependency Rules

These rules are binding for Epic 3 Integration.

### Application may depend on Domains

Application invokes Readiness, Decision, Recommendation, Mission (and related domain contracts) with inputs those architectures already define. Application may also depend on Curriculum Engine / `CurriculumService` helpers for CurriculumContext construction.

### Domains never depend on Application

Domain packages remain framework-independent. They must not import orchestrators, repositories, assemblers, Flask, or ORM. They receive CurriculumContext, Twin snapshots, Goals, and Constraints as arguments.

### Presentation never bypasses Application

Blueprints, templates, and future clients request composed experience (or write recording) through Application. They must not call Decision, Recommendation, or Mission engines with ad-hoc arguments that skip orchestration, and must not invent CurriculumContext or Twin-first readiness locally.

### Infrastructure never contains educational logic

Databases, JSON loaders, and config hold rows, bytes, and settings. They do not score readiness, select next actions, package recommendations, compose missions, or interpret Twin beliefs as product authority.

```
Presentation ──depends on──► Application ──depends on──► Domains
                                   │
                                   └──depends on──► Infrastructure
                                        (adapters only)

Domains ──✗──► Application
Presentation ──✗──► Domains (Twin-first educational path)
Infrastructure ──✗──► educational reasoning
```

### Additional firewalls

1. **Read / write firewall** — Dashboard composition does not mutate Twin; product actions become Evidence via EvidenceRecorder.  
2. **No hybrid averages** — Application must not average legacy readiness % with Twin / Decision factors.  
3. **No parallel product authority** — Legacy Stage A peers are not nodes inside the Twin-first Application graph; Stage B adapters sit beside it, named honestly.

---

# 6. Product Integration

## How Application enables multiple product surfaces

Educational Intelligence is platform-neutral. Application is the Integration spine that lets many clients share one educational truth.

| Surface | Application role | What stays unchanged |
|---|---|---|
| **Web** | Flask blueprints call EducationalOrchestrator / assemblers; templates render the Experience Contract | Domains, Decision authority, warrant honesty |
| **Mobile** | Client consumes the same Experience Contract via Application/API boundary; progressive disclosure may differ | Educational meaning and Decision-backed day |
| **Desktop** | Same contract; chrome and offline concerns stay Presentation / client | No second readiness or next-action engine |
| **API** | Serialises Experience Contract and write events through Application; does not expose domain internals as a second reasoner | Domains remain selection / scoring authority |

### Integration principle

```
One Educational Intelligence
        ↓
One Application composition path
        ↓
Many Presentation surfaces
```

Surfaces may differ in layout, progressive disclosure, and chrome. They must not differ in educational story: one Decision, one Recommendation packaging, one Mission operationalisation, one honesty posture.

### Why Educational Intelligence does not change

- Domains already answer educational questions without knowing Flask, React Native, or desktop shells.  
- Application absorbs framework and product-workflow concerns.  
- New clients add Presentation + thin Application adapters / assemblers — not new Twin strategies or Decision formulas.  
- Epic 3 Integration and cutover (Stage A → B → C) change **which product authority students receive**, not ADR-002 domain design.

Governing restatement:

> **Add surfaces by consuming Application. Never by forking Educational Intelligence.**

---

# 7. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **God Services** | EducationalOrchestrator (or a single “IntegrationService”) accumulates scoring, selection, packaging, mission packing, persistence, and UI policy until it recreates the monolithic Recommendation Service ADR-002 rejected. | Keep Application thin: lifecycle, order, context, repository bridges, assembly, errors only. Refuse new educational algorithms in Integration milestones. |
| **Builder explosion** | Every call site invents a CurriculumContext / Goals / Twin “helper”; denominators and honesty diverge; V1/V2 drift returns. | Few named builders with closed contracts; production composition uses one CurriculumContextBuilder; test fixtures must not become a second product path. |
| **Domain leakage** | Domains import Flask/ORM, or Application reimplements readiness / decision / mission math “temporarily.” | Preserve ADR-002: domains framework-free; persistence and curriculum loading in Application; educational math only in domain owners. |
| **Hidden educational logic** | “Temporary” Mid defaults, re-ranking, copy-driven overrides, or legacy substitution land in Application or routes “for UX.” | Architecture review gate: if a method selects, scores, invents tasks, or coerces warrant, it is out of Application scope. Product copy consumes domain outputs — it does not override them. |

### Risk restatement

The primary danger is not missing a surface. It is **Application that starts reasoning** — or Presentation that bypasses Application and recreates parallel truth. Either failure reintroduces the study-planner pathology Epic 2 was built to end.

---

# 8. Recommendations

## Implementation philosophy

How Application Layer work should proceed after this architecture:

1. **Treat this document as architecture law for Capability 3.2.5** — Application composes; it introduces no educational authority. Do not reopen ADR-002’s educational chain.  
2. **Proceed Architecture → Implementation → Review** (Engineering Charter). This note authorises none of the code.  
3. **Keep Application thin by design** — prefer orchestrator + few builders + few assemblers + repository/recorder bridges over a god Integration service.  
4. **Implement a single Twin-first product read-path entry** (EducationalOrchestrator) before Twin-first UI claims.  
5. **Ship CurriculumContextBuilder via canonical Curriculum helpers first** so V1/V2 safety is proven at the Application boundary.  
6. **Wire TwinRepository as a read-only Application adapter** on the dashboard path; prove missing-Twin honesty before inventing fallbacks.  
7. **Compose only the closed Experience Contract set** via DashboardAssembler; reject “just one more” educational side channel.  
8. **Separate EvidenceRecorder (write) from orchestrated dashboard (read)** — preserve the write/read firewall; Twin mutation stays on the Evidence → Twin Update path (Capability 3.3).  
9. **Add Future Builders and Assemblers only when a new contract is proven necessary** — not as speculative framework code; each must answer one construction or projection question.  
10. **Bind Web, Mobile, Desktop, and API to the same Experience Contract** — platforms differ in presentation, not in educational meaning.  
11. **Cut over Stage A → Stage B → Stage C** with named dual-truth adapters; no hybrid averages; Stage C before Version 1.0 Twin-first marketing.  
12. **Guard against God Services, builder explosion, domain leakage, and hidden educational logic** in every Integration review.  
13. **STOP.** This milestone is architecture only. No services. No code. No tests. No implementation until an explicit implementation milestone authorises them.

---

# References

- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md)  
- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
- [`CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md`](CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md)  
- [`CAPABILITY_3_2_CURRICULUM_CONTEXT_BUILDER_ANALYSIS.md`](CAPABILITY_3_2_CURRICULUM_CONTEXT_BUILDER_ANALYSIS.md)  
- [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
- [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
- [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
- [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md)  
- [`ARCHITECTURE.md`](../../ARCHITECTURE.md)

---

**STOP.** Capability 3.2.5 complete as architecture only.
