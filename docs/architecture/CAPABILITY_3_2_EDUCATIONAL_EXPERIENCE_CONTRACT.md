# Capability 3.2.3 — Educational Experience Contract

**Status:** Contract only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.2 Integration (Educational Experience Contract preceding product surface wiring)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream analysis:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md)  
**Upstream architecture:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
**Product law:** [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Scope:** Canonical product-facing Educational Experience produced by Educational Orchestration — **platform-neutral contract only; no code, services, schemas, migrations, or UI**

---

## Document purpose

Capability 3.2.1 defined **what** Educational Orchestration is.  
Capability 3.2.2 defined **how** orchestration is structured as architecture.

This milestone defines **what product surfaces receive**: the closed, platform-neutral **Educational Experience Contract** — everything a product surface needs to render a student's study experience without inventing educational meaning.

```
Educational Intelligence domains
              ↓
   Educational Orchestration     ← composes; does not author
              ↓
   Educational Experience Contract   ← this document
              ↓
   Product surfaces (Web · Mobile · Desktop · API)
```

**Governing principle (binding):**

> **The contract represents experience. It never becomes educational authority.**

**Non-goals of this document**

- Implementation types, dataclasses, JSON schemas, or API payloads  
- Service class designs, package layouts, or persistence adapters  
- Redesign of Evidence, Twin, Readiness, Decision, Recommendation, or Mission  
- UI templates, copy systems, or premium visual design  
- Platform-specific view models that diverge from this contract  

---

# 1. Executive Summary

## Why the Educational Experience Contract exists

Educational Orchestration composes completed Educational Intelligence into one product path. Product surfaces still need a **stable answer to what they may render**.

Without a contract:

- Web templates, future mobile clients, and API consumers would invent incompatible view models.  
- Surfaces would quietly re-rank, recompute, or strip warrant “for UX.”  
- Explainability and empty-state honesty would become optional decorations.  
- Ownership of Recommendation, Mission, and Readiness would blur into “whatever the dashboard needs today.”

The **Educational Experience Contract** is the canonical product-facing artefact produced by Educational Orchestration. It is the closed set of conceptual components that together represent a student's study experience for a given product request.

It exists so that:

1. **Every surface renders the same educational truth** — one Decision-backed day, not competing stories.  
2. **Composition stays honest** — missing Twin, cold start, and thin warrant remain first-class, not patched with Mid/High theatre.  
3. **Platforms stay interchangeable** — Web, Mobile, Desktop, and API consume the same conceptual contract.  
4. **Domains remain authoritative** — the contract carries domain answers; it does not invent new ones.

Epic 3 replaces **product authority** through wiring and cutover. This contract is the Integration boundary that makes that replacement consumable by every surface without redesigning Educational Intelligence (ADR-002).

---

# 2. Principles

These principles bind the contract. They extend orchestration architecture into the product-facing boundary.

### Platform-neutral

The contract is conceptual, not a Flask template model, React prop tree, or mobile DTO. Any client that can present the components may consume it. Platform rendering choices (layout, progressive disclosure, chrome) must not change educational meaning.

### Immutable

For a given composition pass, the Experience is a snapshot of composed domain outputs. Surfaces may filter presentation (e.g. hide deep lineage until requested). They must not mutate educational claims, re-order Decision meaning, or invent substitute Recommendation / Mission content after composition.

### Explainable

Every educational claim that students can act on must remain attributable. Explainability is mandatory cargo: reason codes, lineage hooks, and warrant posture travel with Recommendation and Mission. Progressive disclosure may hide detail; it must not delete lineage.

### Truthful

The contract prefers a smaller honest experience over a complete false one. Cold-start, unknown readiness, thin warrant, missing Twin, and blocked curriculum states are valid contract contents — not failures to paper over. Never fabricate Mid/High preparedness or a confident next action when domains did not author one.

### Complete

Within Version 1.0 scope, the contract is the **closed set** of components defined here. Surfaces must not invent a sixth educational authority channel (streak theatre, competing next-action panels, opaque composites, legacy % as Twin-first truth). If a surface needs a new educational claim, that is a domain or product-scope question — not a local view-model extension.

### No educational authority

The contract **carries** educational answers. It does **not** select next actions, aggregate readiness, package recommendations, compose missions, mutate Twin beliefs, or invent syllabus structure. Orchestration assembles the contract; domains author the meaning; surfaces render.

Governing restatement:

> **If a product surface needs to answer an educational question, it reads the contract. It does not reason.**

---

# 3. Core Components

Components are conceptual. This section does **not** define implementation types, field schemas, or serialisation formats.

Together they constitute the Educational Experience for one authorised product request.

| Component | Meaning |
|---|---|
| **Student Summary** | Who the experience is for: authorised student identity scope and sitting / goal context needed to situate the day — not a second Twin, and not other users’ state. |
| **Today's Recommendation** | The primary next-action suggestion for the student: attributable packaging of Decision (title / affordances / warrant-bound narration hooks). One next-action story — not a heuristic list that disagrees with Decision. |
| **Today's Mission** | Today’s / this session’s attributable executable work: Mission / MissionTask set operationalising Decision under Constraints. Tasks remain Decision-bound; no filler invented under leftover capacity. |
| **Readiness Summary** | Factorable preparedness posture and warrant as the product may display. Forwarded from Readiness Aggregation — never recomputed or averaged with legacy percentages inside the contract. |
| **Progress Snapshot** | Honest, non-authoritative cues of what is known from Twin / evidence / readiness projections appropriate to Version 1.0 honesty. Summarises state; never selects what to study next. |
| **Explainability** | Chain-supported *why*: Decision reason codes and lineage citations (and readiness citations when Decision cites readiness), plus Recommendation narration hooks. Mandatory cargo; progressive disclosure may defer detail, not erase it. |
| **Warnings** | Explicit honesty and degraded-composition signals: thin warrant, partial failure, named dual-truth (Stage B), blocked guidance, or other postures that reduce claims without fabricating certainty. |
| **Empty-State Guidance** | Lawful guidance when the educational chain cannot yet produce a full study day: cold-start / missing Twin / not-yet-knowable postures, and any domain-authored diagnostic or evidence-creating direction that Decision may produce — never motivational theatre pretending preparedness is known. |
| **Metadata** | Non-educational composition facts: when the experience was composed, product / surface intent, locale or copy channel, cutover mode (Stage A/B/C) when named, and contract version identity. Metadata must never become a back door for educational selection. |

### Component composition rules

1. **Place, do not author.** Components reflect domain outputs; the contract does not invent educational meaning.  
2. **One next-action story.** Today's Recommendation and Today's Mission must not disagree with Decision. If they would, composition failed.  
3. **Warrant travels.** Readiness Summary, Warnings, and Empty-State Guidance keep honesty visible.  
4. **Progress is not selection.** Progress Snapshot never overrides Recommendation or Mission.  
5. **Closed set.** Version 1.0 educational experience on this path is these components — nothing more as educational authority.

```
Student Summary
Today's Recommendation  ← Recommendation Engine (Decision packaging)
Today's Mission         ← Mission Intelligence (Decision operationalisation)
Readiness Summary       ← Readiness Aggregation
Progress Snapshot       ← Twin / evidence / readiness projections (honest, non-selecting)
Explainability          ← Decision lineage (+ readiness citations when cited)
Warnings                ← honesty / degradation signals
Empty-State Guidance    ← lawful empty / cold-start postures
Metadata                ← composition facts only
        ↓
Educational Experience Contract
```

---

# 4. Ownership

Every component maps to educational owners. Ownership is never duplicated. The contract **forwards**; it does not co-own.

| Component | Educational owner(s) | Contract role |
|---|---|---|
| **Student Summary** | Product identity / authorised scope (Application); sitting goals as Goals contracts domains already consume | Situate; never invent Twin or curriculum |
| **Today's Recommendation** | **Recommendation** (packaging) projecting **Decision** (selection) | Forward packaging; preserve Decision attribution and warrant |
| **Today's Mission** | **Mission** operationalising **Decision** | Forward Mission / tasks; preserve Decision binding; no filler |
| **Readiness Summary** | **Readiness** | Forward posture and warrant; never recompute |
| **Progress Snapshot** | **Twin** (authoritative learner state) + Readiness / evidence projections already authorised as summaries | Compose honest cues; never invent mastery theatre; never select |
| **Explainability** | **Decision** (reason codes, lineage) — with Readiness citations when Decision cites readiness; Recommendation narration hooks | Preserve and surface; never invent post-hoc stories |
| **Warnings** | Orchestration composition (classification only) from domain honesty postures | Classify and forward; never upgrade warrant for polish |
| **Empty-State Guidance** | **Decision** cold-start / empty-state policy when available; otherwise honest not-yet-knowable product posture | Forward domain-authored empty guidance only; never fabricate Twin or Mid readiness |
| **Metadata** | Orchestration / Application product context | Carry composition facts; never select educational value |

### Owner map (no duplication)

| Owner | Sole authority for | Must not appear as |
|---|---|---|
| **Decision** | Highest-value next action; candidate set; reason codes; lineage; cold-start selection policy | Something Recommendation, Mission, or Progress “fixes” |
| **Recommendation** | Packaging and warrant-bound narration of Decision | Selection authority or competing list |
| **Mission** | Operationalisation of Decision into today’s tasks under Constraints | Re-ranking educational value or inventing filler |
| **Readiness** | Derived preparedness judgement and warrant | Hybrid average with legacy %; Mid/High coercion of unknown |
| **Twin** | Authoritative learner educational state (read snapshot on this path) | Belief mutation during experience composition; fabricated Twin |
| **Curriculum** | Syllabus identities, order, weights via CurriculumContext | Private topic lists or plan rows treated as curriculum truth |

### Ownership invariants

1. **Decision selects once.** Recommendation and Mission never become parallel selectors inside the contract.  
2. **Readiness is not Progress.** Progress Snapshot may cite readiness; it does not own preparedness judgement.  
3. **Twin is not Decision.** Twin state informs domains; the contract does not let Progress or Student Summary choose the next action.  
4. **Curriculum is not optional colour.** Without lawful CurriculumContext, Twin-first guidance does not silently invent syllabus.  
5. **Orchestration owns composition, not answers.** Warnings and Metadata are composition concerns; educational meaning remains domain-owned.

Governing restatement:

> **Never duplicate ownership. If two components appear to answer the same educational question, the contract is broken.**

---

# 5. Product Independence

The Educational Experience Contract is the **same conceptual artefact** for every consumer. Platforms differ in presentation, not in educational truth.

| Consumer | How it consumes the contract |
|---|---|
| **Web** | Flask / templates / JS render components into the calm Version 1.0 day (dashboard → recommendation → mission). Layout and progressive disclosure are Web concerns; Decision attribution and warrant are not. |
| **Mobile** | Native or hybrid clients bind the same components to mobile navigation and session chrome. Mobile must not invent a second Recommendation list or offline-fabricated readiness. |
| **Desktop** | Desktop shells (if any) consume the same Experience; windowing and shortcuts are shell concerns, not educational re-authorship. |
| **API** | Machine consumers expose or transport the same components for authorised clients. API shape may serialise the contract; it must not redefine ownership or omit Explainability / Warnings as “payload optimisation.” |

### Independence rules

1. **One contract, many renderers.** Web, Mobile, Desktop, and API are adapters over the Experience — not authors of competing experiences.  
2. **No platform-private educational fields.** A platform may add presentation hints (e.g. collapsed-by-default) in its own UI layer; it must not add private educational scores or alternate next actions.  
3. **Same failure posture everywhere.** Missing Twin and cold start mean the same honesty on every surface.  
4. **Cutover mode is Metadata, not a fork.** Stage A/B/C naming travels in Metadata; Twin-first claims still require Stage C on student paths (Epic 3 product law).  
5. **Orchestration is the sole composer.** Surfaces request the Experience; they do not call Decision / Recommendation / Mission engines with ad-hoc arguments that skip orchestration.

```
                    Educational Experience Contract
                     /        |         |        \
                  Web      Mobile    Desktop      API
                     \        |         |        /
                      same educational truth
```

---

# 6. Failure Behaviour

**Product rule (binding):**

> **The contract always remains valid. Validity means truthful — not necessarily complete.**

A valid Experience may be sparse. An invalid response is one that fabricates educational certainty.

## 6.1 Missing Twin

| Condition | Contract behaviour |
|---|---|
| Twin snapshot cannot be loaded (absence, corrupt load, persistence not yet available) | Do not invent a Twin. Do not invent Mid/High Readiness Summary or a confident Today's Recommendation. |
| Valid Experience | Student Summary + Metadata + Warnings (missing Twin) + Empty-State Guidance (honest not-yet-knowable, or Decision-authored empty-state guidance only if domains can produce it without a fabricated Twin). |
| Forbidden | Fabricated Twin beliefs; legacy % as Twin-first Progress; motivational theatre. |

## 6.2 Cold start

| Condition | Contract behaviour |
|---|---|
| Twin exists but evidence is sparse / warrant thin | Forward cold-start and low-warrant postures intact. |
| Valid Experience | Readiness Summary remains unknown/honest; Today's Recommendation / Mission may carry Decision’s cold-start policy (e.g. diagnostic / evidence-creating actions); Warnings and Explainability preserve thin warrant. |
| Forbidden | Coercing unknown readiness to Mid; inventing High-confidence packaging; Mission filler. |

## 6.3 Missing curriculum

| Condition | Contract behaviour |
|---|---|
| Lawful CurriculumContext cannot be built | Stop the Twin-first educational chain. Do not invent topics. |
| Valid Experience | Student Summary + Metadata + Warnings (blocked: missing curriculum) + Empty-State Guidance that guidance cannot be built without official syllabus context. |
| Forbidden | Private topic lists; plan rows as curriculum truth; partial Recommendation pretending curriculum existed. |

## 6.4 Partial failures

| Condition | Contract behaviour |
|---|---|
| Early stages succeed; a later stage fails | Propagate failure class via Warnings. Include only remaining components that stay educationally consistent. |
| Examples of valid partial Experiences | Readiness Summary alone when Decision cannot run; Today's Recommendation without Today's Mission when Mission fails — provided the product does not imply a full Decision-authored day that did not complete. |
| Forbidden | Substituting legacy recommendation lists for failed Decision; inventing Mission filler; presenting Progress Snapshot as if Decision succeeded. |

### Validity invariant

```
Domain failure or thin warrant
        ↓
Orchestrator classifies into Warnings / Empty-State Guidance
        ↓
Contract remains valid (truthful, possibly reduced)
        ↓
Surfaces reduce claims — never upgrade certainty
```

The student always receives the best **truthful** experience available. Completeness is not required for contract validity; honesty is.

---

# 7. Versioning

The contract must evolve without breaking consumers that already render Version 1.0 components.

### Evolution rules

1. **Additive by default.** New optional components or optional conceptual fields may be introduced under a new contract version identity in Metadata. Existing consumers ignore what they do not understand.  
2. **Never silently redefine meaning.** Changing what Today's Recommendation *means* (e.g. from Decision packaging to a heuristic list) is a breaking change — not a patch.  
3. **Deprecate before remove.** Components leave the closed set only after a named deprecation window and a consumer migration path.  
4. **Ownership changes are architectural events.** Moving selection from Decision into Recommendation (or inventing a new selecting component) requires ADR / architecture revision — not a quiet contract bump.  
5. **Platform adapters version presentation, not truth.** Web/Mobile/API payload formats may version independently; they must map to the same conceptual contract version.  
6. **Metadata carries contract version.** Consumers may detect version and degrade presentation safely; they must not invent educational fallbacks when versions mismatch.

### Compatibility posture

| Change type | Allowed without breaking consumers? | Example |
|---|---|---|
| Add optional Warning class | Yes (additive) | New named dual-truth warning for Stage B |
| Add optional Progress cue | Yes if non-selecting and owner-clear | Additional Twin-backed honest summary cue |
| Remove Explainability | No | Breaks trust and Epic 3 product law |
| Reassign next-action ownership | No | Recommendation selecting without Decision |
| Change empty-state to Mid theatre | No | Violates Truthful principle |

Governing restatement:

> **Version the contract so surfaces stay interchangeable. Never version away honesty or Decision authority.**

---

# 8. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **View-model drift** | Web invents a dashboard model, Mobile invents another, API invents a third — educational stories diverge. | Treat this document as the sole conceptual Experience; platform models are projections of it, not peers. |
| **Duplicated contracts** | Parallel “Study Day DTO,” “Dashboard VM,” and “Mission payload” each claim to be the product experience. | One Educational Experience Contract; other payloads are transport or persistence concerns, not competing truth. |
| **Hidden educational logic** | Surfaces or adapters re-rank Decisions, coerce readiness, or invent Mission filler “for UX” after composition. | Contract principle: no educational authority; architecture review rejects post-composition reasoning. |
| **Platform divergence** | One platform ships Twin-first while another still markets legacy % as preparedness; students see conflicting days across devices. | Product Independence rules + Stage C before Twin-first Version 1.0 claims on all student paths. |

### Risk restatement

The primary danger is not an incomplete schema. It is **many product faces of one student day that no longer share one Decision**. Drift, duplication, hidden logic, and platform forks all reintroduce the study-planner pathology Epic 2 was built to end.

---

# 9. Recommendations

How implementation should follow this contract:

1. **Treat this document as contract law for Capability 3.2.3** — the Educational Experience is the closed, platform-neutral product artefact of orchestration. Do not reopen ADR-002’s educational chain.  
2. **Implement orchestration composition to emit this Experience** (conceptual components first; serialisation only in an explicit implementation milestone).  
3. **Bind all Version 1.0 educational surfaces to one Experience** — Web first, then any API / future Mobile / Desktop adapters — without platform-private educational fields.  
4. **Map components to owners exactly as Section 4** — Decision selects; Recommendation packages; Mission operationalises; Readiness judges preparedness; Twin / Curriculum never get duplicated.  
5. **Design failure and empty-state shapes first** so Missing Twin, Cold Start, Missing Curriculum, and Partial failures remain valid Experiences.  
6. **Preserve Explainability and Warnings as mandatory cargo** — progressive disclosure may hide detail; stripping lineage or warrant is a contract violation.  
7. **Keep Progress Snapshot non-selecting** — never let progress cues override Today's Recommendation or Today's Mission.  
8. **Version additively** and carry contract version in Metadata; forbid silent meaning changes.  
9. **Reject duplicated contracts** in review: if a second “day model” appears, fold it into this Experience or demote it to transport-only.  
10. **Guard against hidden educational logic** in surface adapters: if UI code selects, scores, or invents tasks, it is out of scope.  
11. **Proceed Contract → Implementation → Review** (Engineering Charter). This milestone authorises no services or code.  
12. **STOP.** This milestone is contract only. No services. No code. No implementation until an explicit implementation milestone authorises them.

---

# References

- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ANALYSIS.md)  
- [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
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

**STOP.** Capability 3.2.3 complete as contract only.
