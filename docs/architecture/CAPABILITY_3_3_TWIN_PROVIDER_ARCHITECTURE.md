# Capability 3.3.4 — Twin Provider Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.3.4 Twin Provider (Application Layer Twin retrieval contract preceding implementation)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Upstream orchestration:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
**Upstream dashboard assembly:** [`CAPABILITY_3_3_DASHBOARD_ASSEMBLY_ARCHITECTURE.md`](CAPABILITY_3_3_DASHBOARD_ASSEMBLY_ARCHITECTURE.md)  
**Product law:** [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Scope:** Structural architecture for TwinProvider — the Application adapter that supplies an existing Digital Twin (or honest absence) to Educational Orchestrator — **no code, services, schemas, migrations, or tests**

---

## Document purpose

Capability 3.2 defined Educational Orchestration and the Application Layer. Capability 3.3.1–3.3.3 introduced feature flags, Recommendation Card presentation, and Dashboard Assembly.

This milestone defines **TwinProvider**: the Application Layer contract that **retrieves** an existing Student Digital Twin for the Twin-first product read path — or signals that no Twin is available — without becoming Educational Intelligence, persistence ownership, or infrastructure.

**Governing principle (binding):**

> **TwinProvider retrieves. It never fabricates. It never reasons.**

**Architectural restatement:**

> **TwinProvider is an Application adapter. Domains own Twin belief. Twin Update Pipeline owns Twin mutation. Future TwinRepository owns durable persistence. TwinProvider owns only retrieval and honest absence for Educational Orchestrator.**

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Database schemas, Alembic migrations, or ORM adapters beyond naming ownership  
- Redesign of Evidence, Twin, Readiness, Decision, Recommendation, or Mission  
- Twin Update Pipeline wiring or write-path Evidence → Twin mutation  
- Implementation of TwinRepository (named as future; not delivered here)  
- UI templates, copy systems, or premium experience design  

---

# 1. Executive Summary

## Why TwinProvider exists

Educational Orchestration must obtain a Twin snapshot before Readiness Aggregation and Decision Engine can run on the Twin-first product read path. Domains must remain framework-free: they must not load ORM Twin rows, invent Mid preparedness when empty, or import Flask.

Without a named Twin retrieval adapter:

- Routes or the orchestrator would each invent ad-hoc Twin loads (or silent defaults).  
- Missing Twin would collapse into fabricated Mid/High theatre.  
- Domain packages would be pressured to import SQLAlchemy “just to get the Twin.”  
- Parallel Twin stores (legacy mastery fields, plan rows, in-memory fixtures) would become de facto product authority by convenience.

**TwinProvider** exists to:

1. **Accept** authorised student identity and product context from Educational Orchestrator.  
2. **Retrieve** the existing Digital Twin snapshot the student already has — if one exists.  
3. **Signal absence honestly** when no Twin is available (`TwinAbsent`).  
4. **Never fabricate** Twin beliefs, Mid preparedness, or a “starter Twin” for UX completeness.  
5. **Keep Domains free of persistence frameworks** by owning the Application-side retrieval contract.

It is **not** Educational Intelligence. It does not score, select, package, or compose educational meaning.

It is **not** persistence. It does not own durable Twin storage schema, write APIs, or snapshot lifecycle policy.

It is **not** infrastructure. Databases and loaders hold bytes and rows; TwinProvider interprets only the retrieval contract: Twin present or Twin absent.

```
Educational Orchestrator
              ↓
        TwinProvider              ← Application retrieval adapter (this document)
              ↓
   DigitalTwin  |  TwinAbsent
              ↓
   Readiness → Decision → Recommendation → Mission
```

Epic 3 Integration ships TwinProvider so orchestration can wire Twin-first guidance without leaking Twin loading into domains or inventing educational certainty at the Application boundary.

Governing restatement:

> **Supply what exists. Signal what does not. Never invent a Twin.**

---

# 2. Ownership

## 2.1 TwinProvider owns

| Responsibility | Meaning |
|---|---|
| **Twin retrieval** | Obtain the existing Digital Twin snapshot for the authorised student / sitting scope Educational Orchestrator requests — when storage (or interim source) can supply one. |
| **Absence signalling** | Emit an explicit `TwinAbsent` (or equivalent honest absence signal) when no Twin exists for that scope. Absence is a first-class outcome, not an error to paper over. |
| **Retrieval contract** | Define what Orchestrator may ask for and what TwinProvider may return: student identity + context in; DigitalTwin or TwinAbsent out. No Mid default. No silent empty Twin dressed as Mid preparedness. |

TwinProvider is a **retrieval adapter**. Educational Orchestrator remains the composition conductor. Twin domain remains learner-state authority. Domains remain the musicians.

## 2.2 TwinProvider never owns

| Forbidden ownership | Why |
|---|---|
| **Twin mutation** | Belief evolution belongs to Learning Evidence → Twin Update Pipeline → Update Strategies (ADR-002 write path). Dashboard / Orchestrator read path must never mutate Twin via TwinProvider. |
| **Twin persistence** | Durable snapshot store, schema, and write bridges belong to future **TwinRepository** (and Infrastructure underneath). TwinProvider may *call* a repository later; it does not *become* the persistence owner. |
| **Learning Evidence** | Append-only evidence history and EvidenceRecorder (write path) are separate Application / domain concerns. TwinProvider does not record study outcomes. |
| **Readiness** | Preparedness judgement belongs to Readiness Aggregation. TwinProvider never derives readiness, coerces unknown → Mid/High, or averages legacy %. |
| **Decision** | Next-action selection belongs solely to Decision Engine. TwinProvider never selects, re-ranks, or invents next actions from absence. |
| **Recommendation** | Packaging belongs to Recommendation Engine. TwinProvider never invents student-facing educational claims. |
| **Mission** | Task composition belongs to Mission Intelligence. TwinProvider never invents filler tasks or a day plan from missing Twin. |

### Owner map (no duplication)

| Concept | Layer | Relation to TwinProvider |
|---|---|---|
| **EducationalOrchestrator** | Application | Consumer: requests Twin for composition; does not invent Twin |
| **TwinProvider** | Application | Retrieval adapter; Twin or TwinAbsent only |
| **TwinRepository** (future) | Application | Durable persistence adapter; TwinProvider migrates to use it for load |
| **EvidenceRecorder** | Application | Write-path Evidence bridge — separate from TwinProvider |
| **Student Digital Twin** | Domain | Authoritative educational state; loaded, never authored by TwinProvider |
| **Twin Update Pipeline** | Domain | Sole lawful mutation path; TwinProvider has no write edge |
| **Readiness / Decision / Recommendation / Mission** | Domains | Downstream of Twin load; never implemented inside TwinProvider |
| **Infrastructure** | Infrastructure | Stores rows/bytes; does not define Twin retrieval honesty policy |

### Ownership invariants

1. **TwinProvider does not reason about the student.** Retrieval and absence only.  
2. **TwinProvider does not mutate Twin.** No write methods on the Orchestrator read path.  
3. **TwinProvider does not invent Twin.** Fabrication is a contract violation.  
4. **Presentation never bypasses TwinProvider** (via Orchestrator) to invent Twin-first readiness locally.  
5. **Domains never import TwinProvider.** They receive Twin snapshots as arguments.

Governing restatement:

> **TwinProvider answers only: “Does an existing Twin exist for this student scope, and can I return it?” It never answers educational questions about the student.**

---

# 3. Inputs

TwinProvider accepts only what retrieval requires. It does not accept educational goals as scoring inputs, and it does not accept product pressure to invent a Twin.

## 3.1 Student identity

| Input | Meaning |
|---|---|
| **Authorised student identity** | The student whose Twin is requested. Scope must already be ownership-validated by Presentation / Application before TwinProvider is invoked. TwinProvider never loads another user’s Twin because a route guessed an id. |
| **Sitting / plan scope (when required)** | Exam sitting or curriculum-bound scope that identifies *which* Twin snapshot applies when Twin is sitting-scoped. TwinProvider does not invent sittings. |

## 3.2 Context

| Input | Meaning |
|---|---|
| **Product / session context** | Surface intent and request facts Orchestrator already carries (e.g. dashboard composition pass, cutover mode naming) — used only to scope retrieval and classify failures, never to invent beliefs. |
| **Retrieval hints (optional, non-authoritative)** | Non-educational operational hints (e.g. preferred snapshot id if Orchestrator already knows one). Hints never override absence with fabrication. |

### Input rules

1. **Identity is mandatory.** Without authorised student identity, TwinProvider must not guess.  
2. **Context is wiring, not policy.** Context does not author Mid Twin or coerce warrant.  
3. **Goals, Constraints, and CurriculumContext are not TwinProvider inputs for invention.** Orchestrator assembles those separately (CurriculumContextBuilder, Goals packaging). TwinProvider does not build CurriculumContext or score readiness from Goals.  
4. **No legacy mastery / readiness % as Twin substitute inputs.** Passing legacy TopicProgress composites into TwinProvider as “the Twin” is forbidden.

```
Educational Orchestrator supplies
  ├─ Student identity (authorised)
  └─ Context (product / sitting scope)
        ↓
   TwinProvider
```

---

# 4. Outputs

TwinProvider returns exactly one of two lawful outcomes. There is no third “fake Twin for UX” outcome.

## 4.1 DigitalTwin

| Output | Meaning |
|---|---|
| **DigitalTwin** | The existing Student Digital Twin snapshot retrieved for the requested scope — the domain aggregate Educational Intelligence already contracts for (Knowledge, Memory, Behaviour, Performance, and related Twin structure). |

**Rules when Twin is returned:**

1. Return the Twin **as stored / as already authored by the Twin Update Pipeline** — do not patch beliefs for dashboard completeness.  
2. Preserve immutability expectations of the domain Twin contract (snapshot semantics).  
3. Do not upgrade sparse Twin content into Mid/High preparedness theatre inside the provider.  
4. Orchestrator forwards the Twin to Readiness / Decision intact.

## 4.2 TwinAbsent

| Output | Meaning |
|---|---|
| **TwinAbsent** | Explicit signal that no Twin exists (or none can be lawfully returned) for the requested student / sitting scope. |

**Rules when Twin is absent:**

1. **Never fabricate.** Do not emit an empty Twin dressed as Mid preparedness. Do not invent Knowledge / Memory / Behaviour / Performance defaults that imply known educational state.  
2. **Absence is truthful cargo.** Orchestrator classifies Missing Twin and reduces product claims (honest empty / cold-start posture per orchestration failure law).  
3. **Absence is not Decision.** TwinProvider does not select diagnostic actions; Decision Engine may do so later only under domain-defined empty-state contracts when Orchestration proceeds that far.  
4. **Absence is not Readiness Mid.** Unknown / not-yet-knowable remains the honest posture.

### Closed output law

```
TwinProvider
   ├─→ DigitalTwin     (existing Twin retrieved)
   └─→ TwinAbsent      (honest absence)
```

**Forbidden outputs:**

- Fabricated Twin beliefs  
- Hybrid “legacy % as Twin” objects  
- Silent `null` that Presentation interprets as Mid readiness  
- Partial invented domains “so Readiness can run”  

Governing restatement:

> **DigitalTwin or TwinAbsent. Never fabricate.**

---

# 5. Failure Behaviour

**Product rule (binding):**

> **The student should always receive the best truthful experience available. Never fabricate educational certainty.**

TwinProvider prefers honest absence / classified failure over a complete false Twin.

## 5.1 Missing Twin

| Condition | TwinProvider behaviour |
|---|---|
| No Twin snapshot exists for the authorised student / sitting | Return **TwinAbsent**. |
| Truthful downstream effect | Orchestrator surfaces Missing Twin / cold-start empty posture; no Mid/High readiness theatre; no confident Decision invented by Application. |
| Forbidden | Starter Twin; default Mid Knowledge; motivational “you’re ready” packaging sourced from absence. |

## 5.2 Corrupt Twin

| Condition | TwinProvider behaviour |
|---|---|
| Stored Twin cannot be mapped to a lawful domain DigitalTwin (corrupt payload, contract violation, unreadable snapshot) | Do **not** repair by inventing beliefs. Classify as retrieval failure / treat as **TwinAbsent** (or an equivalent explicit corrupt-load failure signal Orchestrator can forward). |
| Truthful downstream effect | Orchestrator reduces claims; Warnings may name degraded composition; student sees honesty, not a patched Twin. |
| Forbidden | Best-effort “fix enough to score”; dropping warrant while retaining bold readiness; silently substituting legacy mastery rows as Twin. |

## 5.3 Unavailable storage

| Condition | TwinProvider behaviour |
|---|---|
| Persistence / interim store is unavailable (timeout, connection failure, infrastructure outage) | Do **not** invent an in-memory Twin to keep the dashboard full. Signal retrieval failure / **TwinAbsent**-equivalent unavailability so Orchestrator can degrade. |
| Truthful downstream effect | Product reduces surface; retry / reload may re-run identical retrieval contracts after recovery. |
| Forbidden | Fake Twin for availability theatre; skipping Twin and inventing Decision “just this once”; treating storage failure as Mid preparedness. |

### Failure propagation principle

```
Missing / Corrupt / Unavailable
        ↓
TwinProvider → TwinAbsent (or explicit retrieval failure)
        ↓
Educational Orchestrator classifies Missing Twin / degraded composition
        ↓
Experience + Dashboard Assembler reduce claims
        ↓
Student sees best truthful experience available
```

---

# 6. Relationship to future TwinRepository

APPLICATION_LAYER_ARCHITECTURE and Educational Orchestration Architecture name **TwinRepository** as the Application persistence adapter for durable Twin snapshot load (and, on separate write paths, persistence bridges).

**TwinProvider** and **TwinRepository** are related but not identical roles.

| Role | Owns | Horizon |
|---|---|---|
| **TwinProvider** | Retrieval contract for Educational Orchestrator: DigitalTwin or TwinAbsent; honesty policy for missing / corrupt / unavailable | Capability 3.3.4 architecture (this document); thin Implementation later |
| **TwinRepository** | Durable Twin persistence: map storage ↔ Twin snapshot domains; load and (on write paths) persist bridges; keep Domains free of ORM | Future Integration / Learning Evidence stream milestone (Epic 3 Stream B — Twin persistence) |

## 6.1 Why separate TwinProvider now

1. **Orchestrator needs a retrieval contract before durable schema lands.** TwinProvider can be defined (and later stubbed / adapted) without pretending TwinRepository persistence is complete.  
2. **Persistence debt must not become fabrication debt.** Naming TwinProvider prevents “temporary Mid Twin” while E2-PE-01 Twin persistence remains open.  
3. **Write/read firewall stays clear.** TwinRepository will eventually own persistence including write bridges; TwinProvider on the dashboard path remains **load-only** forever.  
4. **Application stays thin.** TwinProvider answers one question (retrieve or absent). TwinRepository answers storage mapping. Collapsing both prematurely recreates a god Integration service.

## 6.2 Migration path

```
Stage now (architecture / interim)
  EducationalOrchestrator → TwinProvider → (interim source or explicit TwinAbsent)

Stage after TwinRepository exists
  EducationalOrchestrator → TwinProvider → TwinRepository.load → DigitalTwin | TwinAbsent
```

| Migration step | Rule |
|---|---|
| **1. Contract first** | TwinProvider’s outputs remain DigitalTwin or TwinAbsent regardless of storage maturity. |
| **2. Repository behind provider** | When TwinRepository ships, TwinProvider delegates load to it — Orchestrator still talks to TwinProvider (or to a single Application retrieval façade that preserves the same contract). |
| **3. No dual Twin stores as authority** | Repository load becomes the durable source for Twin-first paths. Legacy mastery / readiness % tables must not remain parallel Twin authorities. |
| **4. Write path stays separate** | TwinRepository persistence writes (if any) belong to Evidence → Pipeline → persist — never to TwinProvider on dashboard composition. |
| **5. Honesty preserved** | Migration must not “improve UX” by fabricating Twins when the repository returns empty. |

### Migration invariant

> **TwinRepository changes *where* TwinProvider loads from. It does not change *that* TwinProvider may only return DigitalTwin or TwinAbsent.**

---

# 7. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **Parallel Twin stores** | Legacy TopicProgress / readiness % / plan rows / in-memory fixtures compete with Digital Twin as “the learner.” Orchestrator or TwinProvider silently prefers whichever is convenient. | Single Twin-first retrieval contract. Legacy peers remain Stage A/B named dual truth — never substituted as DigitalTwin. Stage C retires them as educational-state authority. |
| **Fake Twins** | Missing / corrupt / unavailable cases emit empty or Mid-default Twins “so Readiness can run” or “so the dashboard looks complete.” | Closed output law: DigitalTwin or TwinAbsent only. Architecture review rejects Mid defaults and starter Twins on the read path. |
| **Application reasoning** | TwinProvider (or Orchestrator via the provider) starts scoring readiness, selecting diagnostics, inventing Knowledge domains, or averaging legacy % into a synthetic Twin. | TwinProvider owns retrieval and absence only. Educational math stays in Domains. Review gate: if a method selects, scores, or invents beliefs, it is out of TwinProvider scope. |

### Risk restatement

The primary danger is not a missing repository. It is **a retrieval adapter that starts fabricating or reasoning** — recreating parallel learner truth and reintroducing the study-planner pathology Epic 2 was built to end.

---

# 8. Recommendations

## Implementation sequence

How TwinProvider work should proceed after this architecture:

1. **Treat this document as architecture law for Capability 3.3.4** — TwinProvider retrieves; it never fabricates or reasons. Do not reopen ADR-002’s educational chain.  
2. **Proceed Architecture → Implementation → Review** (Engineering Charter). This note authorises none of the code.  
3. **Keep TwinProvider as a thin Application adapter** called by EducationalOrchestrator — not by Presentation routes inventing Twin loads.  
4. **Prove TwinAbsent honesty first** — Missing Twin, Corrupt Twin, and Unavailable storage must yield truthful orchestration / dashboard degradation before “happy path” polish.  
5. **Forbid Fake Twins in every review** — no Mid defaults, no starter Twin, no legacy % as DigitalTwin.  
6. **Do not implement TwinRepository in this capability** — name it as future persistence; migrate TwinProvider to delegate load when Stream B Twin persistence lands.  
7. **Preserve write/read firewall** — TwinProvider has no mutation API on the dashboard path; EvidenceRecorder + Twin Update Pipeline own belief evolution.  
8. **Keep Domains framework-free** — TwinProvider (and later TwinRepository) absorb ORM / storage concerns; domains receive Twin snapshots as arguments only.  
9. **Align with CurriculumContextBuilder discipline** — Twin and CurriculumContext are both Orchestrator inputs; load either order, but never invent either.  
10. **Guard against Parallel Twin stores and Application reasoning** in Integration reviews.  
11. **Keep Application code untouched until an explicit implementation milestone** authorises TwinProvider types and tests.  
12. **STOP.** This milestone is architecture only. No services. No code. No tests. No implementation until an explicit implementation milestone authorises them.

---

# References

- [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
- [`CAPABILITY_3_3_DASHBOARD_ASSEMBLY_ARCHITECTURE.md`](CAPABILITY_3_3_DASHBOARD_ASSEMBLY_ARCHITECTURE.md)  
- [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
- [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
- [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
- [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md)  
- [`ARCHITECTURE.md`](../../ARCHITECTURE.md)

---

**STOP.** Capability 3.3.4 complete as architecture only.
