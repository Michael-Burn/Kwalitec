# Capability 3.3.3 — Dashboard Assembly Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.3.3 Dashboard Assembly (Application Layer presentation composition preceding implementation)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Upstream experience contract:** [`CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md`](CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md)  
**Upstream orchestration:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
**Product law:** [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Upstream Application milestones:** Capability 3.3.1 (feature flags), Capability 3.3.2 (Recommendation Card presentation builder)  
**Scope:** Structural architecture for the Dashboard Assembler that converts the Educational Experience into one immutable DashboardViewModel — **no code, services, schemas, migrations, UI templates, or tests**

---

## Document purpose

Capability 3.2 defined orchestration, the Educational Experience Contract, and the Application Layer. Capability 3.3.1–3.3.2 introduced feature-flag-aware rollout and a single-widget presentation builder.

This milestone defines the **Dashboard Assembler**: the Application Layer component that owns **dashboard presentation composition** — converting one Educational Experience into one closed, immutable **DashboardViewModel** Presentation may render.

**Governing principle (binding):**

> **The Dashboard Assembler composes presentation. It never reasons educationally.**

**Architectural restatement:**

> **Educational Orchestrator composes educational truth. Dashboard Assembler shapes that truth for the dashboard. Presentation displays. Domains remain sole educational authority.**

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Database schemas, Alembic migrations, or ORM adapters  
- Redesign of Evidence, Twin, Readiness, Decision, Recommendation, or Mission  
- Premium visual design, copy systems, or template markup  
- New educational claims, alternate next-action stories, or client-local Decision overrides  
- Implementation of Stage B/C adapters beyond architectural boundaries for assembly  

---

# 1. Executive Summary

## Why Dashboard Assembly exists

Educational Orchestration produces the **Educational Experience Contract**: a platform-neutral, immutable snapshot of composed domain answers for one authorised product request. That contract is educational cargo — Recommendation packaging, Mission operationalisation, Readiness posture, Progress cues, Explainability, Warnings, Empty-State Guidance, Metadata.

The dashboard still needs a **single presentation artefact**: one ViewModel that places widgets, empty states, warnings, and navigation affordances for the calm Version 1.0 day — without re-opening educational questions.

Without a Dashboard Assembler:

- Blueprints would invent ad-hoc template dicts from domain objects.  
- Widget builders would diverge into competing “days.”  
- Feature-flag cutover would scatter across routes.  
- Domain objects would leak into templates and invite post-composition scoring.  
- Graceful degradation would become UI guesswork instead of closed ViewModel posture.

The **Dashboard Assembler** is the Application Layer owner of that presentation composition. It:

1. Accepts one Educational Experience (already composed; already honest).  
2. Applies feature-flag-aware inclusion of Twin-first widgets vs legacy coexistence posture.  
3. Assembles closed presentation cards / summaries into one immutable DashboardViewModel.  
4. Forwards Warnings, Empty-State Guidance, and navigation affordances without upgrading certainty.  
5. Emits **no domain objects** — only presentation fields Presentation may render safely.

```
Educational Intelligence Domains
              ↓
   Educational Orchestrator     ← composes educational truth
              ↓
   Educational Experience Contract
              ↓
   Dashboard Assembler          ← owns presentation composition (this document)
              ↓
   DashboardViewModel (immutable, closed)
              ↓
   Presentation (dashboard blueprint / templates)
```

Epic 3 replaces **product authority** through wiring and cutover. Dashboard Assembly replaces **template inventiveness** with one lawful presentation projection. It does not redesign Educational Intelligence (ADR-002).

Governing restatement:

> **One Experience. One Assembler. One DashboardViewModel. No educational authorship.**

---

# 2. Ownership

## 2.1 DashboardAssembler owns

| Responsibility | Meaning |
|---|---|
| **Dashboard composition** | Produce exactly one DashboardViewModel per authorised dashboard request from one Educational Experience (or from an honest empty / degraded Experience when domains could not complete). |
| **Widget assembly** | Place Version 1.0 dashboard widgets — Recommendation card, Mission card, Readiness summary, Progress summary — according to Experience contents and feature flags. Placement and inclusion only; never educational invention. |
| **Presentation shaping** | Map Experience components into presentation fields (titles, subtitles, action labels, duration display, reason summaries, visibility toggles, warning strings, empty-state copy hooks, navigation affordances). Shaping is display vocabulary, not selection or scoring. |
| **Feature-flag-aware composition** | Honour Educational Intelligence rollout flags (Capability 3.3.1) so Stage A legacy coexistence remains default until each Twin-first widget is explicitly enabled. Flags gate **inclusion**, not **truth rewriting**. |

Dashboard Assembler is a **presentation conductor**. Educational Orchestrator remains the educational conductor. Domains remain the musicians.

## 2.2 DashboardAssembler never owns

| Forbidden ownership | Why |
|---|---|
| **Readiness** | Preparedness judgement and warrant belong to Readiness Aggregation. Assembler forwards Readiness Summary presentation only — never recomputes, averages with legacy %, or coerces unknown → Mid/High. |
| **Decision** | Next-action selection, candidate sets, and reason codes belong solely to Decision Engine. Assembler never re-ranks, substitutes, or invents a next action for an empty card. |
| **Recommendation** | Packaging and warrant-bound narration belong to Recommendation Engine. Assembler (and Recommendation Card Builder) project packaging into card fields; they do not become a second packager that invents titles from Twin. |
| **Mission** | Task composition and Decision-binding belong to Mission Intelligence. Assembler places Mission card fields; it never invents filler tasks or a private day plan. |
| **Twin** | Authoritative learner state belongs to Twin / Twin Update Pipeline. Assembler never loads, mutates, or fabricates Twin beliefs to fill Progress. |
| **Curriculum** | Syllabus identities, order, and weights belong to Curriculum Engine / `CurriculumService`. Assembler never invents topics or treats plan rows as curriculum truth. |

### Owner map (no duplication)

| Concept | Layer | Relation to Dashboard Assembler |
|---|---|---|
| **EducationalOrchestrator** | Application | Upstream: composes Educational Experience; Assembler does not re-run domains |
| **Educational Experience Contract** | Application product artefact | Sole educational input to assembly |
| **DashboardAssembler** | Application | Presentation composition entry for the dashboard surface |
| **Widget builders** (e.g. Recommendation Card Builder) | Application | Optional thin helpers called by Assembler; same ownership firewall |
| **Feature flags** | Application config | Inclusion gates; never educational scorers |
| **Readiness / Decision / Recommendation / Mission / Twin / Curriculum** | Domains / Curriculum authority | Never called by Assembler for educational answers |

### Ownership invariants

1. **Assembler does not call Educational Intelligence domains.** It consumes Experience only.  
2. **Assembler does not bypass Orchestrator.** Presentation requests Experience via Orchestrator (when Twin-first path is enabled), then Assembler shapes the result.  
3. **Widget builders are not parallel assemblers of educational truth.** They may shape one card; they must not invent a second day story.  
4. **Flags never become Decision.** Disabling a widget hides or degrades presentation; it does not author a competing educational claim.  
5. **No domain objects in the ViewModel.** Templates receive presentation data only.

Governing restatement:

> **Dashboard Assembler answers only: “How do we place the Experience on the dashboard honestly?” It never answers educational questions about the student.**

---

# 3. DashboardViewModel

## 3.1 Closed ViewModel law

The **DashboardViewModel** is the closed, immutable presentation artefact for one dashboard composition pass.

**Binding rules:**

1. **Closed set.** Version 1.0 dashboard educational presentation on this path is the components below — nothing more as educational authority (no streak theatre widgets, competing next-action panels, opaque composite scores).  
2. **Immutable.** For a given assembly pass, the ViewModel is a snapshot. Presentation may progressive-disclose UI chrome; it must not mutate educational claims after assembly.  
3. **No domain objects.** The ViewModel must not carry Decision, Recommendation, Mission, ReadinessState, Twin, CurriculumContext, or other domain types. Only presentation scalars / closed presentation sub-models.  
4. **One next-action story.** Recommendation card and Mission card must not disagree with the Experience’s Decision-backed day. If they would, assembly failed.  
5. **Honest emptiness is valid.** A ViewModel with warnings and empty states is lawful; a ViewModel that fabricates Mid/High certainty is not.

Relation to the Educational Experience Contract:

| Experience component | DashboardViewModel role |
|---|---|
| Today's Recommendation | Recommendation card |
| Today's Mission | Mission card |
| Readiness Summary | Readiness summary |
| Progress Snapshot | Progress summary |
| Explainability | Progressive affordances on cards / navigation to explanation detail (not a second selector) |
| Warnings | Warnings |
| Empty-State Guidance | Empty states |
| Student Summary + Metadata | Situating / cutover / contract version facts for chrome and coexistence — never selection |
| (product navigation needs) | Navigation affordances |

```
Educational Experience Contract
        ↓
Dashboard Assembler (+ optional widget builders)
        ↓
DashboardViewModel
  ├─ Recommendation card
  ├─ Mission card
  ├─ Readiness summary
  ├─ Progress summary
  ├─ Warnings
  ├─ Empty states
  └─ Navigation affordances
```

## 3.2 Recommendation card

**Purpose:** Primary next-action presentation for the calm first viewport.

**Presentation cargo (conceptual):** title, optional subtitle, primary action label, estimated duration display, short reason summary, optional warning string, explanation visibility toggle, start / continue affordance visibility.

**Source:** Experience Today's Recommendation (Recommendation packaging of Decision), shaped via Assembler / Recommendation Card Builder.

**Must not:** Re-select action family; invent title from Twin; upgrade thin warrant to confident packaging; show a competing heuristic list.

**Feature flag:** `ENABLE_EI_RECOMMENDATIONS` (and orchestrator enablement) — when off, card is absent / legacy path remains; Assembler does not fabricate Twin-first recommendation presentation.

## 3.3 Mission card

**Purpose:** Today’s / this session’s attributable executable work path from the dashboard.

**Presentation cargo (conceptual):** mission title / summary, task count or short task headlines suitable for a card, duration / feasibility display already packaged, Decision-attribution hooks, primary “open mission” affordance, optional warning when Mission is partial or absent.

**Source:** Experience Today's Mission.

**Must not:** Invent filler tasks; re-order educational priority; imply a full Decision-authored day when Mission was not composed; conflate `domain.Mission` educational meaning with legacy ORM mission theatre without named cutover Metadata.

**Feature flag:** `ENABLE_EI_MISSIONS` — when off, Mission card Twin-first presentation is absent; legacy coexistence continues honestly.

## 3.4 Readiness summary

**Purpose:** Honest, factorable preparedness posture the student may see without cognitive overload.

**Presentation cargo (conceptual):** overall posture label, warrant posture / honesty cue, optional short factor highlights already authorised as summaries, link affordance to deeper readiness detail when progressive disclosure allows.

**Source:** Experience Readiness Summary.

**Must not:** Recompute readiness; average with legacy %; coerce unknown / not-yet-knowable to Mid/High; present legacy composites as Twin-first truth while claiming Stage C.

## 3.5 Progress summary

**Purpose:** Honest, non-selecting cues of what is known — evidence / Twin / readiness projections appropriate to Version 1.0 honesty.

**Presentation cargo (conceptual):** short progress cues, empty-or-known posture, optional navigation to progress / analytics surfaces that remain non-selecting.

**Source:** Experience Progress Snapshot.

**Must not:** Choose what to study next; invent mastery theatre from absence; let progress cues override Recommendation or Mission cards.

**Feature flag:** `ENABLE_EI_PROGRESS` — when off, Twin-first progress presentation is absent or reduced; never replaced with vanity streaks marketed as Twin truth.

## 3.6 Warnings

**Purpose:** Explicit honesty and degraded-composition signals on the dashboard.

**Presentation cargo (conceptual):** ordered warning messages / codes already classified by orchestration (thin warrant, missing Twin, missing curriculum, partial failure, named dual-truth Stage B, blocked guidance).

**Source:** Experience Warnings (Assembler may format for display; must not delete or soften educational honesty).

**Must not:** Strip warnings for polish; invent Mid/High reassurance; market Stage B dual truth as Twin-first Version 1.0.

## 3.7 Empty states

**Purpose:** Lawful guidance when the educational chain cannot yet produce a full study day.

**Presentation cargo (conceptual):** empty-state title / body hooks, optional diagnostic / evidence-creating CTA only when Experience Empty-State Guidance already authorises it, absence of fake recommendation / mission cards presented as complete.

**Source:** Experience Empty-State Guidance (+ Warnings / Metadata).

**Must not:** Motivational theatre pretending preparedness is known; fabricated Twin; legacy % as Twin-first Progress in the empty Twin-first path.

## 3.8 Navigation affordances

**Purpose:** Finished paths the student may take from the dashboard without dead buttons.

**Presentation cargo (conceptual):** which primary CTAs are live (start recommendation, open mission, view explanation, open readiness/progress detail), destinations that exist as completed Version 1.0 surfaces, and which affordances are hidden because flags / Experience say the educational cargo is absent.

**Source:** Experience contents + feature flags + Version 1.0 Included-surface discipline (Epic 3 product law).

**Must not:** Expose unfinished chrome; invent destinations that imply educational authority the Experience did not provide; use navigation to smuggle a second next-action selector.

### ViewModel composition rules

1. **Place, do not author.** Cards reflect Experience; Assembler does not invent educational meaning.  
2. **Omit rather than fake.** Missing Mission → no Mission card (or explicit empty), never filler.  
3. **Warrant travels.** Thin warrant appears as warning / card honesty, not as confident CTA copy.  
4. **Explainability is progressive, not deleted.** Default viewport may collapse detail; lineage hooks remain available when `ENABLE_EI_EXPLAINABILITY` and Experience allow.  
5. **Closed set.** No sixth educational widget as authority.

---

# 4. Failure handling

**Product rule (binding):**

> **The DashboardViewModel always remains valid. Validity means truthful — not necessarily complete.**

A valid ViewModel may be sparse. An invalid response is one that fabricates educational certainty for layout completeness.

## 4.1 Graceful degradation

Graceful degradation means **reducing presentation claims**, not **replacing educational truth**.

| Degradation mode | Allowed | Forbidden |
|---|---|---|
| **Reduce surface** | Omit cards; emphasise Warnings and Empty states; keep calm hierarchy | Fabricate full Twin-first dashboard with Mid/High theatre |
| **Preserve warrant** | Keep unknown / low-warrant language visible on cards and summaries | Quietly upgrade warrant for UX polish |
| **Partial Experience** | Assemble only widgets consistent with remaining Experience components | Imply a complete Decision-authored day when Decision / Recommendation / Mission did not complete |
| **Retry / reload** | Presentation re-requests Orchestrator → Assembler with identical contracts | Assembler invents a Decision “just this once” to unblock UI |

### Failure → ViewModel map

| Condition | Assembler behaviour |
|---|---|
| **Missing Twin** | No confident Recommendation / Mission / Mid readiness presentation. Warnings + Empty states from Experience. Navigation limited to lawful evidence-creating / diagnostic paths only if Experience already authorises them. |
| **Cold start / thin warrant** | Cards may exist if Experience carries Decision cold-start packaging; Warnings and warrant cues remain visible; never coerce readiness summary to Mid/High. |
| **Missing curriculum** | Twin-first educational cards absent / blocked empty state; Warning that guidance cannot be built without official syllabus context. |
| **Partial failures** | e.g. Readiness summary without Recommendation; Recommendation without Mission — only when Experience remains consistent; do not substitute legacy lists while claiming Twin-first composition. |
| **Orchestrator disabled / unavailable** | Feature-flag / Stage A coexistence path — do not pretend Assembler authored Twin-first truth from legacy peers. |

```
Domain / composition failure or thin warrant
        ↓
Experience carries Warnings / Empty-State Guidance
        ↓
Dashboard Assembler reduces widgets / claims
        ↓
DashboardViewModel remains truthful (possibly sparse)
        ↓
Presentation reduces chrome — never upgrades certainty
```

## 4.2 Legacy coexistence

Stage A dual truth is named reality until Stage C. Assembler must not erase that fact for convenience.

| Stage | Assembler posture |
|---|---|
| **Stage A** | Default flags off. Dashboard Assembler Twin-first ViewModel is not student product authority. Legacy dashboard peers remain what students consume. Assembler may exist for engineering validation only. |
| **Stage B** | Flags may enable Twin-first widgets behind named dual-truth adapters. Metadata / Warnings must name dual authority when both stories could appear. Engineering-only debug dual views stay out of student chrome. No hybrid averages of legacy % with Twin factors inside assembly. |
| **Stage C** | Student dashboard consumes Orchestrator → Assembler Twin-first ViewModel as single educational presentation authority on this path. Legacy peers retired from next-action / readiness / mission authority. |

**Binding:** Do not market Stage A or partial Stage B assembly as Twin-first Version 1.0.

## 4.3 Feature flags

Feature flags (Capability 3.3.1) are **inclusion gates** for presentation composition.

| Flag role | Assembler rule |
|---|---|
| `ENABLE_EDUCATIONAL_ORCHESTRATOR` | Without orchestrated Experience, Assembler has no Twin-first educational input; do not invent Experience from legacy services. |
| `ENABLE_EI_RECOMMENDATIONS` | Gates Recommendation card inclusion. |
| `ENABLE_EI_MISSIONS` | Gates Mission card inclusion. |
| `ENABLE_EI_EXPLAINABILITY` | Gates explanation affordances / progressive lineage chrome. |
| `ENABLE_EI_PROGRESS` | Gates Twin-first Progress summary inclusion. |

**Flag invariants:**

1. Flags default safe (off) so Stage A behaviour remains unchanged until cutover enables each experience.  
2. Flags never recompute readiness, select actions, or average legacy with Twin.  
3. Flag-off means **omit Twin-first widget** (legacy coexistence), not **fabricate alternate educational content** inside Assembler.  
4. Assembler reads flags; it does not become a policy engine that invents educational exceptions per user.

---

# 5. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **God assembler** | DashboardAssembler absorbs orchestration, domain calls, persistence, copy policy, and every surface projection until it recreates a monolithic Recommendation Service behind a new name. | Keep Assembler thin: Experience in → closed ViewModel out. Orchestrator owns educational composition; widget builders stay single-purpose; refuse domain invocation from assembly milestones. |
| **Domain leakage** | ViewModel carries Decision / Recommendation / Mission / Twin objects “temporarily,” or templates import domain packages and start scoring. | Closed ViewModel law: presentation scalars / sub-models only. Architecture review rejects domain types in dashboard render contracts. |
| **Widget reasoning** | Recommendation or Mission card builders re-rank, invent titles from Twin, coerce warrant, or invent filler tasks “so the card looks full.” | Widget builders are presentation shapers only (Capability 3.3.2 pattern). If a method selects, scores, or invents tasks, it is out of Application presentation scope. |
| **Hidden educational logic** | Routes or Assembler “help” by substituting legacy recommendation lists, Mid defaults, or hybrid averages when Experience is sparse. | Failure handling: reduce claims. Stage B naming required for dual truth. No hybrid averages (ADR-002 / Epic 2 binding conditions). Review gate: post-composition reasoning is a contract violation. |

### Risk restatement

The primary danger is not a missing widget. It is **presentation composition that starts reasoning** — or leaks domains into templates until the dashboard becomes a second Educational Intelligence. Either failure reintroduces the study-planner pathology Epic 2 was built to end.

---

# 6. Recommendations

## Implementation sequencing

How Dashboard Assembly work should proceed after this architecture:

1. **Treat this document as architecture law for Capability 3.3.3** — Dashboard Assembler owns presentation composition only. Do not reopen ADR-002’s educational chain.  
2. **Proceed Architecture → Implementation → Review** (Engineering Charter). This note authorises none of the code.  
3. **Keep Assembler downstream of EducationalOrchestrator** — never call Readiness / Decision / Recommendation / Mission / Twin / Curriculum from the Assembler.  
4. **Consume the closed Educational Experience Contract only** — assembly input is Experience (+ flags); not ad-hoc domain bundles from routes.  
5. **Define DashboardViewModel as a closed immutable presentation set** matching Section 3 — Recommendation card, Mission card, Readiness summary, Progress summary, Warnings, Empty states, Navigation affordances — with **no domain objects**.  
6. **Reuse thin widget builders** (e.g. Recommendation Card Builder from 3.3.2) as helpers inside assembly; do not let each builder become a parallel day composer.  
7. **Wire feature-flag-aware inclusion first** — prove Stage A unchanged defaults before enabling Twin-first widgets.  
8. **Design sparse / empty / partial ViewModels first** — Missing Twin, cold start, missing curriculum, and partial Experience must assemble as truthful dashboards before “happy path” polish.  
9. **Preserve legacy coexistence naming** through Stage B; forbid hybrid averages; require Stage C before Twin-first Version 1.0 marketing on the student dashboard.  
10. **Bind navigation affordances to finished surfaces only** — no dead buttons; unfinished capability stays Deferred / Hidden / Coming Soon (Epic 3 product law).  
11. **Guard every review against God assembler, domain leakage, widget reasoning, and hidden educational logic.**  
12. **Keep Application code untouched until an explicit implementation milestone** authorises Dashboard Assembler types and tests.  
13. **STOP.** This milestone is architecture only. No services. No code. No tests. No implementation until an explicit implementation milestone authorises them.

---

# References

- [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
- [`CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md`](CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md)  
- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md)  
- [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
- [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
- [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
- [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md)  
- [`ARCHITECTURE.md`](../../ARCHITECTURE.md)

---

**STOP.** Capability 3.3.3 complete as architecture only.
