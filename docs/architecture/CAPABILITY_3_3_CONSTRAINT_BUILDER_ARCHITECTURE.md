# Capability 3.3.5 — Constraint Builder Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.3.5 Constraint Builder (Application Layer Constraints construction preceding implementation)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Upstream orchestration:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
**Upstream dashboard assembly:** [`CAPABILITY_3_3_DASHBOARD_ASSEMBLY_ARCHITECTURE.md`](CAPABILITY_3_3_DASHBOARD_ASSEMBLY_ARCHITECTURE.md)  
**Upstream Twin retrieval:** [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md)  
**Product law:** [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Domain Constraints law:** [`CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md) (Constraint handling), [`CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md) (feasibility-shaped load)  
**Scope:** Structural architecture for ConstraintBuilder — the Application component that converts product context into immutable Educational Constraints for Educational Orchestrator — **no code, services, schemas, migrations, or tests**

---

## Document purpose

Capability 3.2 defined Educational Orchestration and the Application Layer. Capability 3.3.1–3.3.4 introduced feature flags, Recommendation Card presentation, Dashboard Assembly, and TwinProvider.

Educational Intelligence domains already consume **Constraints** as feasibility limits on ambition: available time now, session length, sustainable intensity, Behaviour sustainability / burnout flags, and related operational bounds. Domains answer educational questions under those bounds. They must not invent session duration, calendar free time, or preference defaults from Flask routes.

This milestone defines **ConstraintBuilder**: the Application Layer component that **prepares** immutable Constraints from known product context — or marks values unknown — without performing educational reasoning.

**Governing principle (binding):**

> **ConstraintBuilder prepares context. It never reasons educationally.**

**Architectural restatement:**

> **ConstraintBuilder is an Application constructor. Domains consume Constraints as ambition bounds. Decision and Mission honour feasibility. ConstraintBuilder owns only collection, construction, default honesty, validation, and immutable emission for Educational Orchestrator.**

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Database schemas, Alembic migrations, or ORM adapters beyond naming ownership  
- Redesign of Evidence, Twin, Readiness, Decision, Recommendation, or Mission  
- Redesign of domain Constraints value objects beyond naming the Application construction role  
- Implementation of PlanningService, Calendar, Offline sync, or Scheduling  
- UI templates, copy systems, or premium experience design  

---

# 1. Executive Summary

## Why ConstraintBuilder exists

Educational Orchestration must supply **Constraints** before Decision Engine and Mission Intelligence can lawfully shape ambition and session load. Domains already contract for Constraints as *feasibility* — not as educational need, Twin beliefs, or next-action selection.

Without a named ConstraintBuilder:

- Routes or the orchestrator would each invent ad-hoc session minutes, intensity defaults, or “assume 60 minutes” theatre.  
- Missing duration / preferences would collapse into fabricated Mid ambition or padded missions.  
- Planning, calendar, and offline clients would each invent private constraint shapes.  
- Domain packages would be pressured to read Flask session, clocks, or user preference stores “just to get Constraints.”  
- Parallel “quick” constraint helpers would diverge honesty and break determinism of the Twin-first path.

**ConstraintBuilder** exists to:

1. **Collect** authorised product context Educational Orchestrator already has or can request (identity, clock, duration, preferences, session type, product configuration, offline posture when relevant).  
2. **Construct** one immutable Constraints artefact domains already contract for.  
3. **Handle defaults honestly** — only when a product-configured, non-educational default is lawful; never invent educational certainty or fake study capacity.  
4. **Validate** that the constructed Constraints are structurally lawful (or fail / degrade honestly).  
5. **Emit** immutable Constraints where **unknown values remain unknown**.

It is **not** Educational Intelligence. It does not score readiness, select next actions, package recommendations, compose missions, load Twin, or interpret curriculum.

It is **not** presentation. It does not own dashboard cards, copy, or ViewModels.

It belongs to the **Application Layer** because APPLICATION_LAYER_ARCHITECTURE already names Future Builders that package Goals / Constraints from product sitting facts as thin constructors — wiring, not judgement. ConstraintBuilder is that specialised constructor for Constraints.

```
Product context (known facts + explicit unknowns)
              ↓
      ConstraintBuilder           ← Application preparation (this document)
              ↓
   Immutable Constraints
              ↓
Educational Orchestrator → Decision / Mission (feasibility bounds only)
```

Epic 3 Integration ships ConstraintBuilder so orchestration can wire Twin-first guidance without leaking product-clock / preference assembly into domains or inventing educational meaning at the Application boundary.

Governing restatement:

> **Prepare what is known. Leave unknown unknown. Never fabricate feasibility theatre.**

---

# 2. Ownership

## 2.1 ConstraintBuilder owns

| Responsibility | Meaning |
|---|---|
| **Context collection** | Gather authorised product / session facts needed to build Constraints for one composition pass: student identity scope, current date/time, available study duration (when known), user preferences (when known), session type, product configuration, offline state when relevant. Collection is assembly of *sitting facts*, not educational interpretation. |
| **Constraint construction** | Map collected facts into the immutable Constraints shape Decision and Mission already consume as feasibility bounds. Construction packages; it does not decide educational value. |
| **Default handling** | Apply only lawful, non-educational product defaults when architecture explicitly allows them (e.g. a configured product default session type label). Prefer **unknown** over invented study minutes, inventively “comfortable” intensity, or Mid-ambition theatre. |
| **Validation** | Ensure constructed Constraints are structurally coherent for domain consumption (required identity/scope present when mandated; known fields typed/bounded; unknown fields marked unknown — not silently filled). Fail or degrade honestly when validation cannot pass. |
| **Immutable output** | Emit a snapshot Constraints artefact for the composition pass. Downstream must not mutate it into a second educational story. |

ConstraintBuilder is a **context constructor**. Educational Orchestrator remains the composition conductor. Domains remain the musicians. Constraints remain ambition bounds — never educational need.

## 2.2 ConstraintBuilder never owns

| Forbidden ownership | Why |
|---|---|
| **Educational reasoning** | Twin strategies, Readiness Aggregation, and Decision Engine own educational judgement. ConstraintBuilder that “helps” by choosing gentler topics, inventing rest as educational need, or scoring sustainability as learning value becomes a parallel intelligence. |
| **Readiness** | Preparedness judgement and warrant belong to Readiness Aggregation. Constraints do not recompute readiness or coerce unknown → Mid/High. |
| **Decision** | Next-action selection, candidate sets, and reason codes belong solely to Decision Engine. ConstraintBuilder never selects, re-ranks, or invents next actions from duration or preferences. |
| **Recommendation** | Packaging belongs to Recommendation Engine. ConstraintBuilder never invents student-facing educational claims. |
| **Mission** | Task composition and Decision-binding belong to Mission Intelligence. ConstraintBuilder never invents filler tasks or pads load to fill leftover capacity. |
| **Curriculum** | Syllabus identities, order, and weights belong to Curriculum Engine / `CurriculumService` (via CurriculumContextBuilder). ConstraintBuilder never invents topics or treats plan rows as curriculum truth. |
| **Digital Twin** | Authoritative learner state belongs to Twin / Twin Update Pipeline. ConstraintBuilder never loads, mutates, or fabricates Twin beliefs — including inventing Behaviour burnout flags as Twin truth when product context has none. Behaviour sustainability signals that domains already expose may be *forwarded* when Orchestrator supplies them as known domain facts; ConstraintBuilder does not author Twin Behaviour. |

### Owner map (no duplication)

| Concept | Layer | Relation to ConstraintBuilder |
|---|---|---|
| **EducationalOrchestrator** | Application | Consumer: requests Constraints for composition; does not invent Constraints ad hoc |
| **ConstraintBuilder** | Application | Context constructor; immutable Constraints out |
| **CurriculumContextBuilder** | Application | Sibling builder for syllabus context — separate contract |
| **TwinProvider** | Application | Sibling retrieval adapter for Twin — separate contract |
| **DashboardAssembler** | Application | Downstream presentation composition — never builds Constraints |
| **PlanningService / Calendar / Offline / Scheduling** (future) | Application / product peers | May supply richer *product facts* into ConstraintBuilder inputs; do not become parallel Constraint builders |
| **Decision / Mission** | Domains | Consume Constraints as feasibility bounds; perform constraint acknowledgements |
| **Readiness / Recommendation / Twin / Curriculum** | Domains / Curriculum authority | Never implemented inside ConstraintBuilder |

### Ownership invariants

1. **ConstraintBuilder does not reason about the student educationally.** Preparation and honesty only.  
2. **ConstraintBuilder does not invent educational need.** Missing duration ≠ invent a study plan; unknown intensity ≠ Mid ambition.  
3. **Constraints bound ambition; they do not erase high-weight educational risk** — Decision / Mission preserve that law; ConstraintBuilder must not pre-erase need by fabricating “rest forever” constraints.  
4. **Presentation never bypasses ConstraintBuilder** (via Orchestrator) to invent session feasibility locally.  
5. **Domains never import ConstraintBuilder.** They receive Constraints as arguments.  
6. **One builder for Constraints on the Twin-first path.** Parallel “quick” builders are forbidden as product authority.

Governing restatement:

> **ConstraintBuilder answers only: “What feasibility facts are known for this request, and can I emit lawful immutable Constraints?” It never answers educational questions about the student.**

---

# 3. Inputs

ConstraintBuilder accepts product context required to construct Constraints. It does not accept educational pressure to invent feasibility, and it does not accept Twin / Decision outputs as construction inputs for authorship.

## 3.1 Input catalogue (examples)

| Input | Meaning |
|---|---|
| **Student identity** | Authorised student (and sitting / plan scope when required). Ownership must already be validated before invocation. ConstraintBuilder never builds Constraints for another user because a route guessed an id. |
| **Current date/time** | Clock / request time used only to situate “available time now” and session window facts — not to invent curriculum urgency as Twin belief. |
| **Available study duration** | Minutes (or equivalent) the student / product declares available for this session — when known. |
| **User preferences** | Non-educational preference facts that shape feasibility packaging (e.g. preferred session length band, sustainability protect preference) — when known. Preferences never become Decision selection. |
| **Session type** | Product session intent (e.g. short focus, standard study, review window) as a labelled product fact — not an educational action family. |
| **Product configuration** | Named product / cutover / feature configuration that may lawfully affect which optional fields are collected — never educational scorers. |
| **Offline state (when relevant)** | Whether the client is offline / sync-limited, affecting which sources of duration / calendar facts are trustworthy — not inventing Twin or Decision. |

Orchestrator may also forward **already-known domain feasibility signals** (e.g. Behaviour sustainability flags already present on an loaded Twin) as *known facts* for packaging into Constraints. Forwarding is not Twin authorship; inventing burnout when TwinAbsent is forbidden.

## 3.2 Known facts vs unknown values

ConstraintBuilder must separate:

| Class | Meaning | Rule |
|---|---|---|
| **Known facts** | Values supplied by authorised product context, validated configuration, or forwarded domain signals that already exist | May appear in Constraints as concrete fields |
| **Unknown values** | Duration, preferences, calendar free time, offline-enriched facts, or sustainability signals not available for this request | Must remain **unknown** in the output — never fabricated |

### Never fabricate

Forbidden fabrications include:

- Inventing “60 minutes” when duration is missing “so Mission can pack.”  
- Inventing Mid / High sustainable intensity when preferences or Behaviour signals are absent.  
- Inventing calendar free blocks from hope.  
- Treating Stage A planning rows or legacy readiness % as Constraints truth.  
- Coercing offline absence of sync into “full online capacity.”  
- Filling unknown fields with motivational defaults for UX completeness.

```
Educational Orchestrator supplies product context
  ├─ Known facts (identity, clock, duration?, preferences?, …)
  └─ Explicit unknowns (what was not available)
        ↓
   ConstraintBuilder
```

### Input rules

1. **Identity is mandatory** for an authorised composition pass. Without it, ConstraintBuilder must not guess.  
2. **Optional context is optional.** Missing optional fields yield unknown — not invention.  
3. **Goals are not ConstraintBuilder’s educational destination authority.** Goals packaging (destination / capacity intent) remains a separate Application concern when needed; ConstraintBuilder may accept capacity-related *facts* already authorised as Goals/session inputs, but does not become Goals ownership or invent Twin Goals.  
4. **CurriculumContext and Twin are not ConstraintBuilder construction sources for invention.** Sibling builders / providers supply those; ConstraintBuilder does not load syllabus or Twin to “infer” minutes.  
5. **No legacy mastery / readiness % as constraint substitute inputs.**

---

# 4. Outputs

ConstraintBuilder returns **immutable Constraints**.

## 4.1 Immutable Constraints

| Output | Meaning |
|---|---|
| **Constraints** | Framework-free, immutable feasibility artefact Decision Engine and Mission Intelligence already contract for: session bounds and sustainability limits that shape ambition — not educational priority. |

**Rules when Constraints are returned:**

1. **Immutable snapshot** for the composition pass — no post-hoc mutation by Presentation or assemblers.  
2. **Unknown values remain unknown.** Fields without known facts stay explicitly unknown / unset in the contract sense — domains honour unknown feasibility honestly (e.g. constrained ambition acknowledgements when domains can proceed; reduced claims when they cannot).  
3. **No educational authorship.** Output must not embed selected actions, readiness scores, recommendation titles, mission task lists, curriculum topic lists, or Twin beliefs.  
4. **Orchestrator forwards Constraints intact** to Decision / Mission (and any other domain that already contracts for them).  
5. **Constraint acknowledgements remain domain-owned.** Decision / Mission record how Constraints shaped ambition; ConstraintBuilder does not invent acknowledgements as educational stories.

### Closed output law

```
ConstraintBuilder
   └─→ Immutable Constraints
         ├─ known feasibility fields (from known facts)
         └─ unknown fields remain unknown
```

**Forbidden outputs:**

- Fabricated study duration  
- Fake intensity / sustainability defaults presented as known  
- Hybrid “legacy plan row as Constraints” objects  
- Silent null that Presentation interprets as “plenty of time”  
- Partial invented educational need “so Decision can run confidently”  

Governing restatement:

> **Immutable Constraints. Unknown remains unknown. Never fabricate.**

---

# 5. Failure Behaviour

**Product rule (binding):**

> **The student should always receive the best truthful experience available. Never fabricate educational certainty — including fabricated feasibility.**

ConstraintBuilder prefers honest unknown / classified failure over complete false Constraints.

## 5.1 Missing duration

| Condition | ConstraintBuilder behaviour |
|---|---|
| Available study duration is not provided | Do **not** invent minutes. Mark duration **unknown**. |
| Truthful downstream effect | Orchestrator still may proceed with Twin / Curriculum / Goals / Readiness when those exist; Decision / Mission apply domain-defined behaviour under unknown session length (feasibility honesty, not padded missions). Product may prompt for duration later — Application does not invent it here. |
| Forbidden | Default “60 minutes for UX”; Mission filler under assumed leftover capacity; treating missing duration as unlimited time. |

## 5.2 Missing preferences

| Condition | ConstraintBuilder behaviour |
|---|---|
| User preferences are absent or incomplete | Do **not** invent preferred intensity, preferred length, or protect-mode theatre. Mark preference-derived fields **unknown** (or omit optional preference packaging). |
| Truthful downstream effect | Domains rely on Twin Behaviour / Goals / explicit Constraints fields that are known; product copy does not claim personalised pacing from absent preferences. |
| Forbidden | Silent Mid intensity; “everyone prefers long sessions” defaults marketed as student preference. |

## 5.3 Offline operation

| Condition | ConstraintBuilder behaviour |
|---|---|
| Client / product reports offline (or sync unavailable) and richer context sources (calendar, remote preference store) cannot be trusted | Build Constraints only from **locally known facts**. Mark calendar-enriched or remote-only fields **unknown**. Signal offline posture as a known operational fact when the Constraints contract allows an offline flag — without inventing Twin or Decision. |
| Truthful downstream effect | Orchestrator / Experience may warn about reduced context; Dashboard reduces claims; retry after sync may rebuild Constraints with richer known facts under the **same public contract**. |
| Forbidden | Inventing online calendar free time while offline; fabricating full-capacity Constraints to keep the dashboard looking complete. |

## 5.4 Missing optional context

| Condition | ConstraintBuilder behaviour |
|---|---|
| Optional inputs absent (session type detail, product-specific optional flags, non-mandatory preference keys) | Proceed with Constraints containing what is known; leave optional fields unknown / absent. |
| Truthful downstream effect | Composition continues when mandatory identity/scope and domain inputs allow; Experience Warnings may note thin product context when Orchestrator classifies it. |
| Forbidden | Rejecting the entire Twin-first path solely because optional preference chrome is missing; inventing optional fields for completeness. |

## 5.5 Validation failures

| Condition | ConstraintBuilder behaviour |
|---|---|
| Inputs contradict (e.g. impossible negative duration), fail structural bounds, or cannot be mapped to a lawful Constraints artefact | Do **not** “fix” by inventing corrected educational capacity. Classify validation failure; return explicit construction failure (or refuse emission) so Orchestrator can degrade. |
| Truthful downstream effect | Orchestrator classifies degraded composition; Experience + Dashboard Assembler reduce claims; student sees honesty, not a patched feasibility envelope. |
| Forbidden | Clamping invalid inputs into confident Mid defaults; stripping unknown markers to force Decision; substituting Stage A planning heuristics as Constraints while claiming Twin-first composition. |

### Failure propagation principle

```
Missing duration / preferences / offline / optional / validation failure
        ↓
ConstraintBuilder → unknown fields and/or explicit construction failure
        ↓
Educational Orchestrator classifies and forwards honesty
        ↓
Decision / Mission honour feasibility without fabricated ambition
        ↓
Experience + Dashboard Assembler reduce claims as needed
        ↓
Student sees best truthful experience available
```

Graceful handling means **reducing fabricated certainty**, not **replacing missing facts with theatre**.

---

# 6. Relationship to future services

ConstraintBuilder’s **public contract** is stable: product context in → immutable Constraints out (unknown remains unknown). Richer Integration peers may improve *what is known* without changing that contract.

## 6.1 PlanningService

| Future role | Relation to ConstraintBuilder |
|---|---|
| **PlanningService** remains multi-day WeekPlan / exam-date planning owner where appropriate (Epic 3 product law). It loses dual claim on Twin-first daily next-action selection. | May supply **known capacity facts** (e.g. already-committed study blocks, remaining weekly hours as product facts) into ConstraintBuilder inputs. |
| **Must not** | Become a second ConstraintBuilder; select daily next actions; average legacy planning heuristics into Constraints as educational truth; erase Decision authority. |

## 6.2 Calendar integration

| Future role | Relation to ConstraintBuilder |
|---|---|
| Calendar adapters may observe free/busy windows and propose **available study duration** or session window facts. | ConstraintBuilder consumes calendar-derived facts when authorised and trustworthy; marks duration unknown when calendar is unavailable. |
| **Must not** | Invent educational need from empty calendar; become Decision; invent Twin Memory spacing from calendar alone. |

## 6.3 Offline sync

| Future role | Relation to ConstraintBuilder |
|---|---|
| Offline sync may later deliver remote preferences, committed capacity, or clock-aligned session facts after reconnect. | On rebuild, ConstraintBuilder accepts newly known facts under the **same** Constraints output contract. Offline path already marks remote-only fields unknown (Section 5.3). |
| **Must not** | Cache fabricated Constraints as if they were synced truth; mutate Twin on sync via ConstraintBuilder. |

## 6.4 Scheduling

| Future role | Relation to ConstraintBuilder |
|---|---|
| Scheduling peers may propose session start/end or intensity windows as product operational facts. | Those facts feed ConstraintBuilder inputs; Domains still own selection and feasibility acknowledgements. |
| **Must not** | Schedule become a parallel Recommendation / Mission authority; ConstraintBuilder must not absorb scheduling optimization math that invents educational priority. |

### Migration / extension invariant

```
Today
  Orchestrator → ConstraintBuilder(product context) → Constraints

Later (richer sources)
  Planning / Calendar / Offline sync / Scheduling
        ↓ (known facts only)
  ConstraintBuilder (same public contract)
        ↓
  Immutable Constraints (unknown still unknown)
        ↓
  Educational Orchestrator → Domains
```

> **Future services change *which facts are known*. They do not change *that* ConstraintBuilder may only emit honest immutable Constraints — never educational reasoning.**

---

# 7. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **Business logic leakage** | ConstraintBuilder accumulates planning math, scheduling optimization, burnout coaching policy, and “smart” duration inference until it becomes a god Integration service. | Keep builder thin: collect → construct → validate → emit. Refuse educational algorithms and planner-first selection in ConstraintBuilder milestones. |
| **Hidden educational reasoning** | “Temporary” helpers choose rest vs study, demote high-weight topics, or invent protect-intensity as educational need inside the builder “for UX.” | Review gate: if a method selects, scores, ranks, or invents educational need, it is out of ConstraintBuilder scope. Domains own constraint *acknowledgements* after consuming Constraints. |
| **Fake defaults** | Missing duration / preferences become Mid minutes, Mid intensity, or unlimited time so Mission looks full. | Unknown remains unknown. Architecture review rejects starter durations and preference theatre. Align with TwinProvider / Orchestration honesty law. |
| **Presentation ownership** | Dashboard Assembler, blueprints, or card builders start inventing Constraints (or mutating them) to fill cards. | Constraints are built only via ConstraintBuilder for Orchestrator. Assemblers place Experience; they never author feasibility. |
| **Parallel constraint builders** | PlanningService, calendar adapter, offline client, and routes each invent private Constraints shapes; honesty and determinism diverge. | One ConstraintBuilder on the Twin-first path. Peers supply facts; they do not emit competing Constraints authorities. Test fixtures must not become a second product path. |

### Risk restatement

The primary danger is not missing calendar integration. It is **a context builder that starts fabricating feasibility or reasoning educationally** — recreating planner-first pathology and unsustainable ambition theatre Epic 2 was built to end.

---

# 8. Recommendations

## Implementation sequence

How ConstraintBuilder work should proceed after this architecture:

1. **Treat this document as architecture law for Capability 3.3.5** — ConstraintBuilder prepares context; it never reasons educationally. Do not reopen ADR-002’s educational chain.  
2. **Proceed Architecture → Implementation → Review** (Engineering Charter). This note authorises none of the code.  
3. **Keep ConstraintBuilder as a thin Application constructor** called by EducationalOrchestrator — not by Presentation routes inventing session minutes.  
4. **Align with CurriculumContextBuilder and TwinProvider discipline** — sibling Application roles; Constraints, CurriculumContext, and Twin are Orchestrator inputs; invent none.  
5. **Prove unknown-duration / missing-preferences honesty first** — Missing duration, missing preferences, offline, and validation failure must yield truthful orchestration / domain behaviour before “happy path” polish.  
6. **Forbid fake defaults in every review** — no invented study minutes, Mid intensity theatre, or unlimited-time assumptions.  
7. **Preserve Constraints as ambition bounds only** — Decision / Mission remain owners of how Constraints reshape candidates and load; ConstraintBuilder does not pre-erase educational need.  
8. **Do not implement Planning / Calendar / Offline sync / Scheduling in this capability** — name them as future fact sources; extend inputs without changing the public Constraints contract.  
9. **Guard against business logic leakage, hidden reasoning, fake defaults, presentation ownership, and parallel builders** in Integration reviews.  
10. **Keep Application code untouched until an explicit implementation milestone** authorises ConstraintBuilder types and tests.  
11. **STOP.** This milestone is architecture only. No services. No code. No tests. No implementation until an explicit implementation milestone authorises them.

## Testing philosophy (when implementation is authorised)

Architecture guidance only — not an authorisation to write tests now:

- Prefer contract tests: same known facts → same immutable Constraints; unknowns stay unknown.  
- Cover missing duration, missing preferences, offline, optional absence, and validation failure as first-class cases.  
- Prove ConstraintBuilder emits no educational selection / readiness / Twin / curriculum authorship.  
- Reject fixture builders that become a second product Constraints path.

## Migration path

1. **Contract first** — Orchestrator consumes ConstraintBuilder outputs as Constraints regardless of how thin product context is today.  
2. **Facts enrich later** — PlanningService, Calendar, Offline sync, and Scheduling add known facts behind the same builder.  
3. **No dual Constraints authorities** — Stage A planning peers may coexist as named dual truth for other concerns; they must not silently replace Twin-first Constraints on the orchestrated path.  
4. **Stage C** — Twin-first student path uses one ConstraintBuilder-backed Constraints feed into Decision → Recommendation → Mission.

---

# References

- [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
- [`CAPABILITY_3_3_DASHBOARD_ASSEMBLY_ARCHITECTURE.md`](CAPABILITY_3_3_DASHBOARD_ASSEMBLY_ARCHITECTURE.md)  
- [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md)  
- [`CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md)  
- [`CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md)  
- [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
- [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
- [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
- [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md)  
- [`ARCHITECTURE.md`](../../ARCHITECTURE.md)

---

**STOP.** Capability 3.3.5 complete as architecture only.
