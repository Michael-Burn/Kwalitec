# Capability 2.10.3 — Mission Intelligence Implementation Plan

**Status:** Implementation plan only — no code in this milestone  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.10 Mission Generation Intelligence (structural execution-layer implementation planning)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Educational charter:** [`CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md)  
**Mission architecture:** [`CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream gate:** Capability 2.10.1 Educational Analysis — APPROVED; Capability 2.10.2 Architecture — APPROVED  
**Companions:** [`CAPABILITY_2_8_DECISION_ENGINE_IMPLEMENTATION_PLAN.md`](CAPABILITY_2_8_DECISION_ENGINE_IMPLEMENTATION_PLAN.md), [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_IMPLEMENTATION_PLAN.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_IMPLEMENTATION_PLAN.md), [`CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md), [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), Twin domain README (`app/domain/twin/README.md`), Decision package (`app/domain/decision/`), Recommendation package (`app/domain/recommendation/`), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md)  
**Scope:** Plan the first structural **execution / projection** ship of Mission Intelligence — **no code, tests, migrations, services, or scheduling optimisation in this document’s milestone**

---

## Document purpose

This plan translates the approved Mission Intelligence educational analysis and architecture into a concrete, executable implementation sequence for Capability 2.10.

It answers:

1. What is in / out of scope for the first Mission Intelligence ship  
2. Which files to create and modify  
3. How Mission and MissionTask must be represented as domain artefacts  
4. How the execution pipeline, Decision attribution, and Behaviour evidence hooks must work  
5. Public API, testing, migration, compatibility, fidelity, and acceptance gates  

**Governing principle (binding):**

> **Mission Intelligence is an execution layer. It operationalises Decisions. It does not decide.**

**Hard architectural rules (binding):**

1. Mission Intelligence never selects or re-selects next actions.  
2. Mission Intelligence never invents ranking that disagrees with Decision reason codes.  
3. Mission Intelligence never mutates Twin belief domains.  
4. Mission Intelligence never recomputes readiness or coerces unknown / low-warrant / `not_yet_knowable` into Mid or High preparedness.  
5. Mission Intelligence never invents curriculum identities, evidence ids, or Twin beliefs.  
6. Every core educational MissionTask must be attributable to a Decision and preserve the explainability chain.  
7. Completing a Mission does not grant mastery; completion / assessment evidence does.  
8. Empty capacity is not educational authority to invent tasks Decision did not author.  
9. Scheduling optimisation solvers are forbidden in this capability charter.  
10. Curriculum V1 and V2 remain loadable; task identities come only from Decision / Curriculum lineage.

**Structural discipline:** Structure, attribution, warrant honesty, feasibility acknowledgements, and regenerability first; packing formulas and product cutover later. No selection ever inside this layer.

**Non-goals of this document**

- Implementing execution or any production code  
- Creating tests, Alembic migrations, or service wiring  
- Scheduling optimisation, packing solvers, load-balancing formulas, or session packing math  
- Ranking formulas, selection math, priority scores, or optimization objectives  
- UI, analytics cutover, gamification, notifications, or coach/LLM phrasing models  
- Refactoring or deleting legacy `PlanningService` / ORM `Mission` / `MissionTask`  
- WeekPlan regeneration policy ownership  
- Decision Engine or Recommendation Engine redesign beyond consumption boundaries  
- Full Mission persistence schema or Behaviour evidence recording services  

---

# 1. Scope

## 1.1 In scope (Capability 2.10 structural ship)

| Item | Intent |
|---|---|
| **Domain `Mission` + supporting value types** | Immutable, framework-free execution result — not a Twin write-domain peer; not the ORM model |
| **Domain `MissionTask`** | Atomic Decision-attributable executable unit within a Mission |
| **Decision / Decision-batch operationalisation** | Map authorised selected action(s) into MissionTasks — no re-selection |
| **Decision attribution** | Reason-code citations + lineage hooks preserved on every core educational MissionTask |
| **Warrant / cold-start posture inheritance** | Decision honesty survives into mission composition |
| **Feasibility shaping of load** | Goals capacity / Constraints / sustainability demote volume or intensity — never invent filler |
| **Execution sequencing** | Preserve Decision-authored batch order / reason-code meaning; omit trailing work that does not fit with acknowledgement |
| **Optional Recommendation language hooks** | Surface 2.9 packaging when present and Decision-faithful — never as competing selection |
| **Regeneration identity** | Enough Decision / Twin snapshot reference that recomposition can replace stale missions |
| **Behaviour evidence hooks (structural)** | Mission Completion / Failure linkage slots for later Behaviour / planning evidence — not mastery writes |
| **`MissionIntelligence.compose(...)`** | Pure read-side / execution function/class: Decision(s) + execution context → domain `Mission` |
| **Execution pipeline skeleton** | Bind → validate → bind context → operationalise → shape load → preserve attribution → optional Recommendation language → emit |
| **Cold-start execution posture** | Diagnostic / evidence-creating honesty; never Mid/High preparedness theatre packing |
| **Package exports + domain docs** | Public domain surface; Twin / Decision / Recommendation READMEs note Mission as execution projection |
| **Focused unit tests** | Compose fidelity, attribution, warrant inheritance, empty capacity, cold start, V1/V2, immutability, purity, firewall |

## 1.2 Explicitly deferred

| Item | Why deferred |
|---|---|
| Scheduling optimisation / packing solvers | Forbidden as educational authority; Decision owns educational order |
| Numeric packing / load-balancing formulas | Premature; if ever approved later, remain subordinate to Decision |
| ORM Mission / MissionTask schema changes | Domain artefacts first; product persistence cutover later |
| Alembic migrations | Domain layer only for this capability |
| Flask services / blueprints / mission UI cutover | Orchestration and product surfaces after structural contracts |
| Legacy `PlanningService` deletion or rewrite | Convergence Stage A coexistence only (§12) |
| WeekPlan regeneration algorithms | Planning ownership — Mission ≠ multi-week strategy |
| Mission Completion / Failure evidence recording services | Structural hooks first; product recording path later |
| Decision Journal ORM / persistence | Consume history refs when available; do not own journal |
| Coach / LLM phrasing models | Narration assistance later; core attribution must not depend on LLM |
| CurriculumContext production builder | Orchestration follow-up before live consumers needing syllabus beyond Decision-carried ids |
| Adapters that hybrid-average legacy mission ranks with Twin Decision execution | Forbidden temporary third truth |
| Recommendation Engine redesign | Sibling packaging; optional language only |

## 1.3 Success shape

After implementation:

```
Decision / Decision batch
  - selected action(s)
  - candidate set
  - reason codes + lineage + warrant posture
  - constraint acknowledgements
        +
Execution context
  (Goals capacity, Constraints, session window,
   already-committed work, optional journal / Behaviour feasibility)
        +
Optional Recommendation language (Decision-faithful only)
        ↓
MissionIntelligence.compose(...)
        ↓
Mission (domain)
  - scope identity (student / curriculum / sitting / session window)
  - MissionTask set (Decision-attributable)
  - Decision / batch references
  - attribution + warrant posture
  - feasibility acknowledgements
  - regeneration identity
  - completion / failure evidence hooks
        ↓
(consumers later: product surfaces / Behaviour evidence recording / Planning)
```

Same Decision batch (+ same bound execution context) → same attributable domain `Mission`. No Twin mutation. No readiness recomputation. No re-selection. No scheduling optimisation. No Flask. No migrations. No private mastery in mission rows.

## 1.4 Package placement (locked recommendation)

Prefer a **sibling domain package**, not a Twin write-domain module, not a Decision submodule that blurs selection with execution, and **not** the Flask ORM models under `app/models/mission.py`:

| Path root | Rationale |
|---|---|
| **`app/domain/mission/`** | Makes execution-layer ownership obvious; mirrors `app/domain/decision/` and `app/domain/recommendation/`; avoids implying Mission is a belief domain, a second Decision Engine, or the legacy ORM row |

Do **not** add `mission: Mission` as a required field on `DigitalTwin` in this ship. Live execution is derived on read from Decision(s) + execution context.

Do **not** redefine or replace `app.models.mission.Mission` / `MissionTask` in this ship. Domain types and ORM types must remain **named dual truth** during coexistence (Stage A).

**Reuse:** Import `Decision`, `SelectedAction`, `CandidateAction`, `ReasonCodeRef`, `DecisionWarrantPosture`, `ActionFamily`, `Constraints`, and related types from `app.domain.decision`. Optionally consume Recommendation language hooks from `app.domain.recommendation` without treating Recommendation Priority as sequencing authority. Do not fork selection or packaging types.

---

# 2. Files to create

| Path | Role |
|---|---|
| `app/domain/mission/__init__.py` | Package exports: `Mission`, `MissionTask`, supporting types, `MissionIntelligence` |
| `app/domain/mission/mission.py` | Frozen domain `Mission` (+ scope, tasks, Decision refs, warrant, feasibility, regeneration identity) |
| `app/domain/mission/task.py` | Frozen domain `MissionTask` (+ action family, curriculum scope, Decision attribution, warrant, feasibility, evidence hooks) |
| `app/domain/mission/attribution.py` | Frozen Decision attribution / reason-code citation / lineage citation types |
| `app/domain/mission/feasibility.py` | Frozen feasibility acknowledgement types (capacity / constraint / sustainability load shaping) |
| `app/domain/mission/context.py` | Frozen execution-context VO (Goals capacity, Constraints, session window, committed work, optional journal / Behaviour refs) |
| `app/domain/mission/warrant.py` | Mission warrant / cold-start posture vocabulary (inherits Decision warrant honesty) |
| `app/domain/mission/evidence_hooks.py` | Structural Mission Completion / Failure → Behaviour / planning evidence linkage hooks (not mastery writes) |
| `app/domain/mission/engine.py` | `MissionIntelligence` (or `compose_mission`) — pure compose path |
| `tests/test_mission_intelligence.py` | Unit + fidelity + cold-start + V1/V2-context + firewall suite |

Optional (only if it keeps `engine.py` readable without inventing scheduling optimisation):

| Path | Role |
|---|---|
| `app/domain/mission/sequencing.py` | Pure helpers that preserve Decision-authored order and omit trailing unfit work with acknowledgement |
| `app/domain/mission/load_shaping.py` | Pure helpers that demote volume / intensity under Constraints — never invent filler tasks |

Do **not** create in this capability: services, blueprints, migrations, scoring modules, scheduling solvers, WeekPlan engines, adapters that rewrite `PlanningService`, or ORM replacements for `app.models.mission`.

---

# 3. Files to modify

| Path | Why it must change |
|---|---|
| `app/domain/twin/README.md` | Document Mission Intelligence as **execution / projection** of Decision; clarify it is not a write strategy, not a selector, not Recommendation packaging, and not WeekPlan policy; point to `app/domain/mission/` |
| `app/domain/decision/__init__.py` | Docstring clarification only if needed: Decision selects; Recommendation packages; Mission operationalises; Decision does not own day composition |
| `app/domain/recommendation/__init__.py` | Docstring clarification only if needed: Recommendation packages; Mission may surface language; packaging ≠ day composition |
| `app/domain/__init__.py` | Optional docstring note that mission is a domain package (only if the package already advertises subdomains) |

**Do not modify (this capability)**

- `app/domain/decision/engine.py` selection algorithms or reason-code authorship  
- `app/domain/recommendation/engine.py` packaging algorithms beyond optional consumption  
- `app/domain/twin/update_pipeline.py` algorithms or registration defaults  
- Knowledge / Memory / Behaviour / Performance strategies or frozensets  
- `DigitalTwin` aggregate shape (no required `mission` field)  
- `app/domain/readiness/aggregation.py` factor math or overall posture rules  
- `app/services/planning_service.py`, `app/services/mission_service.py`, mission blueprints, analytics/dashboard  
- `app/models/mission.py` ORM schema  
- Evidence catalogue, Curriculum JSON, Alembic, Flask app factory  

**Caller note (documentation only in README):** future services that need Decision-first Missions must obtain `Decision` / Decision batch first via `DecisionEngine.evaluate(...)` (and optionally Recommendation language via `RecommendationEngine.package(...)`), then call `MissionIntelligence.compose(...)`. Composition must not call Decision Engine as a hidden re-selection path, must not re-derive readiness, must not mutate Twin, and must not invent filler. Orchestration that needs syllabus beyond Decision-carried identities must build `CurriculumContext` via `CurriculumService` helpers **outside** the domain package before Decision evaluation — same pattern as Readiness / Decision / Recommendation.

---

# 4. Mission model

## 4.1 Classification (keep)

| Property | Requirement |
|---|---|
| **Execution-layer** | Produced by operationalising Decision(s) + execution context |
| **Decision-bound** | Every Mission cites Decision(s) as selection authority |
| **Immutable** | Frozen dataclasses; one composition evaluation per input set |
| **Explainable by construction** | Preserves Decision reason codes + lineage into MissionTask attribution |
| **Curriculum-bound** | Curriculum-scoped tasks use official syllabus identities from Decision only |
| **Warrant-honest** | Evidence Warrant / cold-start posture survives into mission composition |
| **Feasibility-respecting** | Goals / Constraints / Behaviour sustainability shape load volume — not educational priority |
| **Regenerable** | When Decisions / Twin / Goals / Constraints change, missions may be recomposed; stale rows are not Twin truth |
| **Non-authoritative for beliefs** | Mission Completion does not grant mastery; Behaviour / planning evidence paths do |
| **Not selection authority** | Decision Engine alone selects; Mission never re-ranks |
| **Not Recommendation packaging** | Outputs Mission only — packaging ownership remains 2.9 |
| **Not WeekPlan policy** | Outputs session/day execution only — planning owns multi-week structure |
| **Not the ORM model** | Domain `Mission` ≠ `app.models.mission.Mission` during coexistence |

## 4.2 Conceptual shape (contract → structural fields)

| Slot | Structural intent |
|---|---|
| **Scope identity** | Student / curriculum / sitting (Goal) / session or day window |
| **MissionTask set** | Ordered executable tasks projected from Decision(s) — may be empty |
| **Decision / batch references** | Identity of Decision(s) being operationalised |
| **Attribution / reason citations** | Aggregated or per-task Decision reason-code + lineage hooks |
| **Warrant / cold-start posture** | Inherited honesty from Decision(s) |
| **Feasibility acknowledgements** | How Goals / Constraints / execution context shaped load volume |
| **Regeneration identity** | Decision / Twin snapshot / compose-version tags enabling recomposition |
| **Evaluation context** | Curriculum format awareness (V1/V2), Mission Intelligence / Decision version tags |
| **Completion / failure linkage** | Structural hooks for Behaviour / planning evidence — not mastery |

## 4.3 What Mission must not store

- Private mastery / readiness / competing priority scores as educational truth  
- Re-ranked Decision candidate lists as equal authority  
- Recommendation Priority as sequencing authority  
- Invented syllabus topics or evidence ids  
- Mid/High preparedness claims when Decision warrant is thin  
- WeekPlan multi-week strategy fields  

## 4.4 Empty Mission capacity (binding)

A Mission with few or zero MissionTasks is a **valid feasibility remainder** when Decision-authorised work does not fit, or when Decision authored a sparse / diagnostic set. Empty capacity must **not** trigger filler generation.

---

# 5. MissionTask model

## 5.1 Classification (keep)

| Property | Requirement |
|---|---|
| **Decision-attributable** | Cites Decision selected action + reason codes + lineage |
| **Action-family faithful** | Study / revise / assess / diagnostic / rest-protect preserved from Decision — not collapsed |
| **Curriculum-scoped when applicable** | Canonical syllabus identity from Decision / Curriculum lineage only |
| **Immutable** | Frozen dataclass within Mission composition |
| **Explainable** | “Why this task?” answers via Decision reason codes, not a private mission priority score |
| **Feasibility-shaped, not re-selected** | Load / intensity may be demoted; educational action identity may not be swapped for packing convenience |
| **Non-authoritative for beliefs** | Completing a MissionTask is Behaviour / planning evidence candidate — not mastery |

## 5.2 Conceptual shape (contract → structural fields)

| Slot | Structural intent |
|---|---|
| **Task identity** | Stable id within Mission for execution / completion recording |
| **Action family** | Preserved from Decision selected action (`ActionFamily`) |
| **Curriculum scope** | Official syllabus identity when Decision was curriculum-scoped |
| **Decision reference** | Decision (and optional candidate-contrast hooks) that authorised this task |
| **Reason-code citations** | Machine-readable Decision factors preserved for attribution |
| **Lineage citations** | Twin / evidence / curriculum / readiness hooks from Decision — never fabricated |
| **Warrant posture** | Inherited honesty when Decision warrant / cold-start is thin |
| **Feasibility acknowledgement** | How session capacity / sustainability shaped inclusion or intensity |
| **Optional Recommendation language hook** | May surface 2.9 packaging already narrated from Decision |
| **Completion / failure linkage** | Hooks for Behaviour / planning evidence recording — not mastery grants |
| **Sequence position** | Presentation order subordinate to Decision-authored batch order |

## 5.3 Mission ↔ MissionTask relationship (binding)

1. A Mission contains zero or more MissionTasks for one session/day window.  
2. Every core educational MissionTask must be attributable to Decision authority.  
3. Mission order / priority presentation must not invent ranking that disagrees with Decision reason codes or Decision-authored batch order.  
4. Empty Mission capacity is a feasibility remainder, not a defect requiring invented tasks.  
5. MissionTasks are regenerable projections; they must not ossify into Twin forks.  
6. Omitting an authorised trailing task because it does not fit is load shaping; substituting a rejected Decision candidate is forbidden.

## 5.4 What MissionTask must not be

- A second Decision among candidates  
- A Recommendation title ownership contract  
- A private mastery / readiness / priority score store  
- A filler slot inventing educational need Decision did not author  
- A collapsed “generic study block” that erases Decision action-family tension  

---

# 6. Execution pipeline

## 6.1 Definition

The execution pipeline is the **structural sequence** of read-side / projection stages that turn Decision(s) into a domain Mission. It is a composition contract — not an algorithm, ranking function, or scheduling optimisation solver.

## 6.2 Pipeline stages (binding)

```
1. Bind Decision / Decision batch
        ↓
2. Validate execution preconditions
   (selected action(s) present; reason codes present; lineage hooks; warrant posture)
        ↓
3. Bind execution context
   (Goals capacity, Constraints, session window, already-committed work)
        ↓
4. Operationalise authorised actions into MissionTask candidates
   (action family + curriculum identity from Decision — no re-selection)
        ↓
5. Shape feasible load
   (reduce volume / intensity under Constraints / sustainability — never invent filler)
        ↓
6. Preserve attribution + warrant posture onto MissionTasks
        ↓
7. Optionally attach Recommendation language (Decision-faithful only)
        ↓
8. Emit Mission container + regeneration identity + evidence hooks
        ↓
Mission / MissionTask artefacts (domain)
```

## 6.3 Stage obligations

| Stage | Obligation | Forbidden |
|---|---|---|
| **Bind Decision / batch** | Decision(s) are the sole selection authority for this Mission | Mission without Decision; inventing a Decision |
| **Validate preconditions** | Require selected action(s) + reason codes on the core path | Opaque tasks without codes |
| **Bind execution context** | Consume Goals / Constraints / session window as fit bounds | Treat context as a second selector |
| **Operationalise actions** | Map Decision selected action(s) to MissionTasks | Re-select among candidates; invent topics; promote rejected candidates |
| **Shape feasible load** | Fit authorised work into capacity; prefer learning-value tasks already authorised | Scheduling solvers that invent educational need; empty-slot filler |
| **Preserve attribution / warrant** | Carry Decision reason codes, lineage, cold-start honesty | Mid/High preparedness theatre; stripped warrant |
| **Optional Recommendation language** | Surface 2.9 packaging when present and Decision-faithful | Recommendation Priority as mission ranker |
| **Emit Mission** | Produce regenerable Mission container + evidence hooks | Store private mastery / readiness / competing priority as educational truth |

## 6.4 Pipeline principles (binding)

1. **Execution only** — no selection enrichment inside operationalisation.  
2. **Decision-first always** — no readiness-first scheduling, no streak-first scheduling.  
3. **Deterministic attribution** — composition templates may vary presentation; they may not vary educational authority.  
4. **Write/read firewall** — no Twin Update Pipeline bypass; no readiness recomputation.  
5. **No ranking stage** — there is no mission score that can change which educational actions are authorised.  
6. **No scheduling optimisation stage** — packing math that effectively re-selects educational value is forbidden.  
7. **Learning value over activity theatre** — prefer authorised learning-value tasks; do not invent filler to make the day look complete.  
8. **Empty capacity is honest** — leftover time is a feasibility remainder, not authority to invent tasks.  
9. **Sequencing authority** — Decision-authored batch order and reason codes; Constraints may omit trailing unfit work with acknowledgement only.

## 6.5 Public compose API (illustrative)

```
MissionIntelligence.compose(
    decision_or_batch: Decision | Sequence[Decision],
    execution_context: MissionExecutionContext,
    recommendation_language: Recommendation | None = None,
) -> Mission
```

Same Decision batch + same execution context → same attributable Mission. Pure: no Flask, no ORM writes, no Twin mutation, no DecisionEngine re-entry for re-selection.

## 6.6 Explicitly deferred inside pipeline

- Exact numeric packing formulas  
- Exact regeneration timing / triggers  
- Exact UI for mission boards  
- WeekPlan regeneration (planning ownership)  
- Coach phrasing models  

---

# 7. Decision attribution

## 7.1 Definition

**Decision attribution** is the structural obligation that every core educational MissionTask remains explainable via Decision authority: selected action, reason codes, candidate contrast hooks, constraint acknowledgements, lineage, and warrant posture.

## 7.2 Mandatory explainability chain

Every core educational MissionTask must support **Why this task?** via:

```
Curriculum factor
    → Learning Evidence (or evidence aggregate)
        → Twin domain state factor(s)
            → Readiness factor (when relevant) + Evidence Warrant
                → Decision Engine reason code(s)
                    → MissionTask attribution
                       (optional Recommendation explanation narration)
```

## 7.3 Attribution slots (binding)

| Slot | Obligation |
|---|---|
| **Selected action fidelity** | MissionTask action family + curriculum scope match Decision selected action (or Decision-batched action) |
| **Reason-code citations** | Every core MissionTask maps to one or more Decision reason codes |
| **Candidate contrast** | “Why this task, not that?” uses Decision candidate set only — never promotes rejected candidates as equal authority |
| **Constraint honesty** | Upstream Decision constraint acknowledgements + Mission feasibility acknowledgements remain visible |
| **Lineage citation** | Twin / evidence / curriculum / readiness citations come from Decision lineage only |
| **Warrant inheritance** | Readiness-adjacent language inherits Decision warrant posture |
| **Version attribution** | Composition names Decision evaluation / reason-code vocabulary / Mission Intelligence version for audit |
| **Tension preservation** | High Knowledge + Low Memory (and similar) must not collapse into bland generic blocks |
| **Action-family preservation** | revise ≠ study ≠ assess ≠ diagnostic ≠ rest-protect |

## 7.4 Authorship rules (binding)

1. **Decision Engine alone authors** reason codes and selected action(s).  
2. **Mission Intelligence operationalises**; it does not invent ranking codes that contradict the Decision.  
3. **Recommendation may narrate** chain-supported packaging language when present; it does not author selection.  
4. **LLM / coach may restate** chain-supported attributions later; they must not invent tasks or fabricate lineage in this ship.  
5. **Post-hoc stories that disagree with reason codes are forbidden.**  
6. **If Decision and Mission disagree about what the student should learn next, Decision is correct and Mission composition is wrong.**

## 7.5 Forbidden attribution breaches (reject in review/tests)

- Opaque “today’s tasks” without Decision reason codes  
- Softening reason codes to remove educational tension  
- Presenting supportive Knowledge Strength as exam readiness when Decision did not claim readiness  
- Dropping cold-start / low-warrant codes for friendlier busywork packs  
- Re-selecting among Decision candidates or promoting rejected candidates  
- Narrating a different action family than Decision selected (e.g. revise → study collapse)  
- Private mission “priority %” as educational authority  
- Hybrid stories that mix legacy readiness % / heuristic mission ranks with Twin/Decision factors as temporary truth  
- Inventing evidence ids, syllabus topics, or Twin beliefs  
- Empty-slot filler framed as adaptive intelligence  
- Rest/protect reframed as failure or avoidance when Decision selected it for sustainability  

## 7.6 Audit artefacts (this ship)

| Artefact | Role in structural ship |
|---|---|
| `Decision` / Decision batch (input) | Selection authority + reason codes + lineage + warrant |
| Domain `Mission` / `MissionTask` (output) | Daily structure consequence — not authority |
| Optional `Recommendation` | Packaging language only — not selection |
| Twin / Readiness | Unchanged; cited only via Decision lineage |
| Behaviour evidence recording / ORM Mission | Deferred — structural hooks / boundary docs only |

---

# 8. Behaviour evidence hooks

## 8.1 Definition

**Behaviour evidence hooks** are structural linkage slots on Mission / MissionTask that allow later product recording paths to emit Mission Completion / Failure as Learning Evidence for Behaviour and planning progress — **without** granting mastery, exam readiness, or Knowledge/Memory/Performance belief writes inside Mission Intelligence.

## 8.2 Educational meaning (binding)

| Outcome | Educational meaning | Forbidden meaning |
|---|---|---|
| **Mission Completion** | Student finished required mission tasks — Behaviour / planning signal | Mastery grant; exam readiness proof; proof Decision “worked” for learning |
| **Mission Failure** | Mission missed, expired, abandoned, or failed criteria — Behaviour / planning signal | Mastery revocation of unrelated domains; readiness collapse theatre |
| **Task completion tick** | Execution adherence candidate | Knowledge/Memory Strength update |

## 8.3 Structural representation

Prefer thin frozen hooks, e.g.:

```
MissionEvidenceHooks
  completion_outcome_identities: ...   # completed / failed / abandoned / expired (structural)
  behaviour_evidence_category_hint: ... # Behaviour / planning — never Knowledge/Memory
  journal_or_recording_refs: ...       # optional linkage identities when available
  notes: ...                           # structural — never mastery writes
```

Mission Intelligence **defines** these hooks and documents that recording happens outside the domain package. It does **not** call `TwinUpdatePipeline`, Update Strategies, or invent Learning Evidence rows in this ship.

## 8.4 Hook principles (binding)

1. Completion / failure become evidence only via **product recording paths** → Learning Evidence → Behaviour Update Strategy.  
2. Mission Intelligence never writes Twin beliefs from completion ticks.  
3. Vocabulary must keep **Mission Completion ≠ mastery** and **Mission Completion ≠ exam readiness** explicit in types/docs.  
4. Accept/dismiss (Decision Journal) and Mission Completion are preference / Behaviour evidence — never mastery.  
5. Prior Completion / Failure patterns may appear in execution context as feasibility honesty only — never as readiness or mastery authority.  
6. Evidence hooks must not store private mastery scores.

## 8.5 Explicitly deferred

- Concrete Behaviour Update Strategy enrichment from mission outcomes  
- ORM persistence of completion events  
- HTTP endpoints that mark tasks complete  
- Analytics dashboards that treat completion % as readiness  

---

# 9. Public API

## 9.1 New exports (additive)

From `app.domain.mission` (names illustrative but should be stable once shipped):

| Symbol | Kind |
|---|---|
| `Mission` | Frozen dataclass (domain) |
| `MissionTask` | Frozen dataclass (domain) |
| `DecisionAttribution` / reason-citation types | Frozen dataclasses |
| `FeasibilityAcknowledgement` | Frozen dataclass |
| `MissionExecutionContext` | Frozen execution-context VO |
| `MissionWarrantPosture` | Enum / frozen posture (inherits Decision honesty) |
| `MissionEvidenceHooks` | Frozen structural hooks |
| `MissionIntelligence` (or `compose_mission`) | Pure compose API |
| Compose / Mission Intelligence version constant | Audit tag |

Prefer explicit `app.domain.mission` imports. Do not force Twin write-path packages to import mission. Do not alias domain `Mission` over `app.models.mission.Mission` in product imports without an explicit adapter layer in a later milestone.

## 9.2 Unchanged interfaces

| Contract | Impact |
|---|---|
| `DecisionEngine` / `Decision` | Unchanged — consumed as input |
| `RecommendationEngine` / `Recommendation` | Unchanged — optional language input only |
| `TwinUpdatePipeline` / Update Strategies | Unchanged — Mission is not registered as a strategy |
| `DigitalTwin` fields | Unchanged (no required mission domain field) |
| `ReadinessAggregation` / `ReadinessState` | Unchanged — not recomputed by composition |
| `CurriculumContext` | Unchanged — Decision already carries format / identities |
| `LearningEvidence` / `EvidenceType` | Unchanged — hooks only; no catalogue rewrite required in this ship |
| HTTP / Flask / `PlanningService` / `MissionService` | No product API change required in this capability |
| ORM `app.models.mission` / Alembic | None |

## 9.3 API compatibility rules

- Additive domain package only.  
- No breaking renames of Twin write domains, readiness types, Decision types, or Recommendation types.  
- Callers that never import domain mission continue to work.  
- Future product cutover and Planning consumers depend on this API; keep Decision-reference fields, reason citations, feasibility acknowledgements, and evidence-hook identities stable once published.  
- Mission Intelligence must not expose “re-rank Decision,” “fill empty slots,” or “select via packing score” shortcuts that bypass Decision authority.  
- Action families remain those authored by Decision (`ActionFamily`); composition must not introduce a competing family catalogue.  
- Domain Mission must remain distinguishable from ORM Mission during Stage A coexistence.

---

# 10. Testing strategy

Target module: `tests/test_mission_intelligence.py`.

## 10.1 Suites

| Suite | Assertions |
|---|---|
| **Contract** | `compose` returns domain `Mission` with Decision refs, ≥0 MissionTasks, attribution on every core educational task, frozen/immutable |
| **Purity** | Input Decision(s) unchanged after compose; no Twin / readiness / strategy side effects |
| **Determinism** | Same Decision batch (+ same execution context) → equal structural fields |
| **No re-selection** | MissionTask family + curriculum id equal Decision selected action(s); rejected candidates never promoted |
| **Attribution** | Every core MissionTask maps to ≥1 Decision reason code; lineage citations ⊆ Decision lineage; no invented evidence ids |
| **Sequencing** | Order preserves Decision-authored batch order meaning; trailing omission under capacity carries feasibility acknowledgement |
| **Load shaping** | Constraints demote volume/intensity without inventing filler; empty capacity remains valid |
| **No filler** | Leftover capacity does not create unauthored educational MissionTasks |
| **Warrant inheritance** | Cold-start / `not_yet_knowable` / low warrant Decision → honest mission warrant; never Mid/High preparedness coercion |
| **Cold-start execution** | Diagnostic / evidence-creating Decision remains diagnostic-shaped; cold-start codes survive attribution |
| **Recommendation optional** | Mission valid without Recommendation; when language attached, selection unchanged; Priority never sequences |
| **Tension preservation** | High Knowledge + Low Memory style Decision reasons remain visible on MissionTasks |
| **Action-family fidelity** | revise ≠ study ≠ assess ≠ diagnostic ≠ rest-protect preserved |
| **Completion ≠ mastery** | Evidence hooks expose Behaviour / planning outcomes only; no Twin write APIs |
| **Curriculum V1 context** | Flat topic-scoped Decision composes without Section ids |
| **Curriculum V2 context** | Section-aware Decision composes; same action-family catalogue |
| **No Twin mutation** | Compose path does not import/call Update Strategies for writes |
| **Framework purity** | AST/import ban for Flask/SQLAlchemy (same pattern as decision/recommendation tests) |
| **Non-optimisation** | No required packing solver / priority float / optimization objective fields |
| **Firewall** | Module does not call `DecisionEngine.evaluate` for re-selection; does not import Update Strategies for writes; does not average legacy `PlanningService` ranks; does not own WeekPlan policy |
| **ORM boundary** | Domain Mission types are not `app.models.mission.Mission`; no ORM persistence in compose path |

## 10.2 Fixture strategy

- Build minimal `Decision` objects via Decision domain constructors / fixtures already used in `tests/test_decision_engine.py`.  
- Prefer structural Decision fixtures (cold start, revise-over-study tension, constraint demotion, rest-protect, V1/V2, Decision batch) over mocking ORM.  
- Execution-context fixtures: ample capacity / tight capacity / burnout sustainability / already-committed work — assert selection unchanged and filler absent.  
- Optional Recommendation fixtures: none / Decision-faithful language — assert selection and sequencing unchanged.  
- Do **not** require equality with legacy `PlanningService` / ORM mission outputs.

## 10.3 Regression

- Existing Decision Engine + Recommendation Engine suites remain green.  
- Existing readiness aggregation + Twin strategy suites remain green.  
- No curriculum engine test changes expected.  
- Suggested command:  
  `python -m pytest tests/test_mission_intelligence.py tests/test_recommendation_engine.py tests/test_decision_engine.py tests/test_readiness_aggregation.py tests/test_knowledge_update_strategy.py tests/test_memory_update_strategy.py tests/test_behaviour_update_strategy.py tests/test_performance_update_strategy.py -v`  
  and `ruff check app/ tests/`

## 10.4 Out of test scope for this capability

- HTTP / mission UI integration  
- ORM Mission persistence round-trips  
- Numeric packing / scheduling optimisation correctness (forbidden)  
- WeekPlan regeneration behaviour  
- Legacy `PlanningService` parity goldens (document divergence as transitional debt; do not force equality)  
- Behaviour Update Strategy writes from completion  
- LLM narration  

---

# 11. Migration impact

| Concern | Impact |
|---|---|
| Database changes | **None** |
| Alembic migrations | **None** |
| ORM / model changes | **None** |
| Persistence changes | **None** |
| Evidence catalogue DB | **None** |
| Curriculum JSON | **None** |
| Data backfill | **None** |
| Legacy `missions` / `mission_tasks` tables | **None** — no cutover in this ship |

Mission domain remains in-memory / framework-free. If a later milestone persists Decision-first Missions, adapts ORM rows, or records Completion / Failure evidence, that is a separate schema / recording plan — not Capability 2.10 structural execution.

**Expected answer for this capability: None.**

---

# 12. Backwards compatibility

| Invariant | Confirmation |
|---|---|
| **Twin write path unaffected** | Pipeline and K→M→B→P strategies unchanged |
| **DigitalTwin shape compatible** | No required mission field added |
| **Decision Engine unaffected** | Consumed as input; selection algorithms not rewritten by composition |
| **Recommendation Engine unaffected** | Optional language only; packaging algorithms not rewritten |
| **Readiness Aggregation unaffected** | Not recomputed by composition |
| **Curriculum V1/V2 unaffected** | No traversal redesign; identities via Decision lineage only |
| **Legacy `PlanningService` / ORM Mission continue** | Coexistence Stage A — not deleted or secretly replaced |
| **No third live ranker forced into UI** | Domain Mission ships; presentation cutover deferred |
| **Evidence append-only** | Preserved |
| **Deterministic cores** | No required LLM/network in compose path |
| **Confidence separability** | Self-report framing only when Decision cited; never mastery/readiness via mission packing |
| **Planning boundary** | No WeekPlan policy absorbed |
| **Recommendation boundary** | Packaging ≠ day composition |

### Legacy convergence posture for this ship

Remain at **Stage A — Coexistence (documented)** per Mission architecture §12:

- Twin-first Decision → Mission execution exists in domain.  
- Legacy `PlanningService` / ORM `Mission` / `MissionTask` continue for existing surfaces.  
- Do not deepen TopicProgress / heuristic mission ranking / filler generation.  
- Do not invent hybrid averages of legacy ranks + Twin Decision execution as temporary authority.  
- Dual truth must remain **named** — domain Mission vs ORM Mission — not papered over as one artefact.  

Stages B–D (adapters, Twin-first product authority, retirement of divergent math) are **out of scope**.

---

# 13. Educational Fidelity Review

Verify the following remain true after structural implementation:

| Fidelity check | Required outcome |
|---|---|
| **Mission Intelligence is an execution layer** | Operationalises Decisions; does not decide |
| **Mission never invents ranking / selection** | No competing priority / packing-as-selection authority |
| **Mission never updates the Twin** | No Update Strategy calls; no belief writes |
| **Mission never invents beliefs or syllabus** | Lineage and curriculum ids only from Decision |
| **Mission never coerces unknown readiness** | Inherits warrant; cold-start honesty mandatory |
| **Mission always remains attributable** | Reason codes + lineage on every core educational MissionTask |
| **Mission Completion ≠ mastery / exam readiness** | Evidence hooks are Behaviour / planning only |
| **Empty capacity ≠ educational authority** | No filler invention |
| **Learning value over activity theatre** | No Mid/High fabrication; no streak-as-readiness packing |
| **Decision ≠ Recommendation ≠ Mission** | Selection / packaging / execution remain separate |
| **Mission ≠ Planning / WeekPlan ownership** | Session/day only |
| **Mission depends on Decision, not raw readiness** | No readiness→mission shortcut |
| **Factor disagreement preserved** | Knowledge vs Memory / Behaviour vs Performance tensions remain visible |
| **Constraints do not erase need** | Demotion visible; high-weight risk remains attributable; no silent substitution of rejected candidates |
| **Rest/protect fidelity** | Not reframed as failure when Decision selected it for sustainability |
| **Confidence ≠ mastery** | Self-report framing cannot unlock foundations-skipping packs as mastery upgrade |
| **V1/V2 honesty parity** | Same cold-start / warrant / attribution contracts on both formats |
| **Explainability spine** | Curriculum → Evidence → Twin → Readiness (when cited) → Decision → MissionTask chain supportable |
| **Fidelity over engagement / schedule aesthetics** | Prefer honest sparse / diagnostic missions over busy false-personalised days |

### Anti-fidelity patterns to reject in review

| Pattern | Reject because |
|---|---|
| Mission re-ranks Decision candidates by engagement or packing heuristics | Secret second Decision Engine |
| Readiness % directly schedules the day | Missing Decision authority and explainability |
| Cold-start Mid readiness used to sell advanced rehearsal packs | Fabricates preparedness |
| Empty-slot filler topics invented to complete a “full mission” | Activity theatre; invented educational need |
| Confidence slider upgrades mission aggressiveness as if mastery | Contamination |
| MissionTask attribution that disagrees with Decision reason codes | Broken explainability |
| Mission Completion writes Knowledge/Memory directly | Evidence/Twin bypass |
| Mission rows store private “priority scores” as mastery | Parallel authority |
| Legacy hybrid % + Twin factors as temporary mission truth | Dual authority; untrustable |
| LLM invents evidence ids or topics for nicer mission stories | Audit fraud |
| Unsustainable cram missions that Behaviour says will fail | Feasibility denial |
| “Rest never allowed” despite burnout flags | Collapses learning sustainability |
| “Rest always preferred” despite high-weight exam-risk Decision | Avoidance theatre; erases educational need |
| Recommendation Priority used as secret sequencer | 2.9/2.10 collapse |
| Scheduling optimisation solver invents educational need | Forbidden in this charter |
| Domain Mission silently aliased as ORM mastery store | Parallel learner model |

---

# 14. Acceptance criteria

Capability 2.10 structural implementation is accepted when all of the following hold:

1. **`app/domain/mission/` exists** as framework-free domain code with `compose` (or equivalent) producing domain `Mission`.  
2. **`Mission` / `MissionTask` are explainable by construction** — Decision references, action-family fidelity, ≥1 reason-code citation on every core educational MissionTask, lineage citations, warrant posture, feasibility acknowledgements, regeneration identity, evidence hooks.  
3. **Composition is execution-layer only** — Twin domains unchanged; Decision unchanged; no Update Strategy registration for Mission beliefs; no readiness recomputation; no re-selection.  
4. **No ranking / no scheduling optimisation** — no packing solver / priority score as educational authority; empty capacity does not invent tasks.  
5. **Cold-start contract** — low-warrant / `not_yet_knowable` / cold-start Decisions compose with honest warrant and diagnostic-shaped missions when Decision selected evidence-creating actions.  
6. **Attribution contract** — every core MissionTask maps to Decision reason codes; rejected candidates never promoted; constraint / feasibility demotions remain visible.  
7. **Recommendation optional** — Mission valid without Recommendation; language never becomes selection or sequencing authority.  
8. **Behaviour evidence hooks** — Completion / Failure linkage is Behaviour / planning only; no mastery writes.  
9. **Curriculum V1 and V2** Decision fixtures compose without requiring Sections globally.  
10. **No scheduling optimisation / scoring formulas / Flask services / migrations / ORM replacement / WeekPlan ownership** in the Capability 2.10 structural PR unless explicitly re-scoped.  
11. **Public exports** documented; Twin / Decision / Recommendation docs clarify Mission as execution projection of Decision.  
12. **Tests green** for mission suite + recommendation + decision + readiness + Twin strategy regressions; ruff clean on touched paths.  
13. **Hard educational rules** remain true: Mission operationalises Decisions and does not decide; Mission Completion ≠ mastery; Mission ≠ Recommendation packaging; Mission ≠ WeekPlan policy; Activity ≠ learning value.  
14. **Legacy coexistence** — `PlanningService` / ORM Mission not deleted; no hybrid averaging adapter shipped as “temporary truth”; dual truth named.

---

# 15. Definition of Done

A Capability 2.10 implementation milestone is **Done** when:

- [ ] Scope in §1 delivered; deferred items not sneakily included  
- [ ] Files in §2 created; files in §3 modified only as planned  
- [ ] Domain `Mission` model matches §4 (execution-layer, Decision-bound, immutable, explainable, regenerable, no required Twin field, not ORM)  
- [ ] Domain `MissionTask` model matches §5 (Decision-attributable, action-family faithful, no filler, no private mastery)  
- [ ] Execution pipeline matches §6 (pure compose; no re-selection; no ranking; no scheduling optimisation; no Twin writes)  
- [ ] Decision attribution matches §7 (reason-code citations; chain supportable; forbidden patterns rejected)  
- [ ] Behaviour evidence hooks match §8 (Completion / Failure → Behaviour / planning only; no mastery writes)  
- [ ] Public API impact is additive only (§9)  
- [ ] Testing strategy §10 executed and green  
- [ ] Migration impact is None (§11) and confirmed in the completion report  
- [ ] Backwards compatibility invariants §12 hold (Twin write path, Decision, Recommendation, readiness, V1/V2, legacy coexistence, Planning boundary)  
- [ ] Educational fidelity review §13 verified by tests and review  
- [ ] Acceptance criteria §14 all checked  
- [ ] Completion report produced per project reporting rules (Summary, Files Created/Modified, Tests Executed, Migration Impact, Architecture Compliance incl. V1/V2, Technical Debt, Known Limitations)  
- [ ] No scheduling optimisation, ORM Mission replacement, `PlanningService` deletion, WeekPlan ownership absorption, or mastery-on-completion shipped under this capability label  

**Stop after Capability 2.10 structural ship + review.** Do not start legacy cutover, packing solvers, or UI migration in the same change set unless separately requested.

---

# 16. Recommended Implementation Sequence

Execute in this order during the **separate implementation milestone** (not this planning milestone):

| Step | Work | Exit check |
|---|---|---|
| **0** | Re-read 2.10.1 analysis + 2.10.2 architecture + this plan; confirm Decision / Recommendation types to consume | Shared understanding; execution-only firewall confirmed |
| **1** | Lock Mission warrant / feasibility / evidence-hook / attribution vocabulary in PR description | Catalogues listed; Mid coercion forbidden; Completion ≠ mastery; no filler |
| **2** | Implement `attribution.py` + `feasibility.py` + `warrant.py` + `evidence_hooks.py` + `context.py` + `task.py` + `mission.py` | Types import cleanly; frozen; distinct from ORM |
| **3** | Implement `engine.py` cold-start + low-warrant + empty-capacity paths first | not-yet-knowable / cold_start → honest warrant; empty capacity valid; no filler |
| **4** | Implement operationalisation + Decision attribution preservation | Every core MissionTask cites Decision codes; action families preserved |
| **5** | Implement load shaping + sequencing (omit trailing unfit work with acknowledgement) | Volume/intensity demotion only; Decision order meaning preserved; no rejected-candidate promotion |
| **6** | Implement optional Recommendation language attachment | Valid without Recommendation; Priority never sequences |
| **7** | Export package + update Twin / Decision / Recommendation docs | Execution-layer ownership clear; dual truth vs ORM named |
| **8** | Write `tests/test_mission_intelligence.py` | Suite green |
| **9** | Run recommendation + decision + readiness + Twin strategy regressions + ruff | No regressions |
| **10** | Capability review against §14 + fidelity §13 | Checklist complete |
| **11** | Completion report + stop | Do not start packing solvers / ORM cutover / WeekPlan ownership |

### Suggested PR shape

- **Title:** `feat: structural Mission Intelligence (Decision execution, attributable)`  
- **Body:** link this plan + 2.10.1/2.10.2; state execution-only firewall; migration None; V1/V2 via Decision lineage; note deferred scheduling optimisation, ORM cutover, Behaviour recording services, WeekPlan ownership, coach phrasing, and legacy `PlanningService` coexistence  

### Explicit stop line (this planning milestone)

This document delivers **planning only**.

**Do not proceed in this milestone to:** code, tests, database changes, services, scheduling optimisation, scoring formulas, ORM Mission replacement, WeekPlan policy, or UI.

Next engineering step (separate milestone): execute §16 steps 1–11 → capability review → architecture review → acceptance.

---

# Appendix A — Capability map

| ID | Capability | Relation to this plan |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot lineage may be cited via Decision; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains Decision consumed; Mission operationalises without modification; Completion/Failure may feed Behaviour later via evidence |
| 2.7 | Readiness Aggregation | May appear in attribution when Decision cites readiness; never schedules missions directly |
| 2.8 | Decision Engine | Supplies Decision authority that Mission operationalises |
| 2.9 | Explainable Recommendation Engine | Sibling packaging; optional language source; not selection |
| **2.10.1** | Mission Intelligence Educational Analysis | Approved educational charter |
| **2.10.2** | Mission Intelligence Architecture | Approved structural contracts |
| **2.10.3** | **Mission Intelligence Implementation Plan** | **This document** |
| 2.10 impl | Structural execution | Separate milestone after this plan |
| Planning | WeekPlan / legacy mission services | Consume consequences later; coexistence Stage A only |

---

# Appendix B — Risks carried into implementation

| Risk | Mitigation in implementation |
|---|---|
| Treating Mission as write domain | Separate package; no Twin field; no Update Strategy |
| Mission invents ranking / becomes second Decision Engine | Operationalise Decision only; firewall tests; no packing-as-selection |
| Readiness → Mission shortcut | Compose requires Decision; never schedule from raw readiness |
| Recommendation Priority as secret ranker | Optional language only; Priority never sequences |
| Scheduling optimisation creep | Forbidden fields/solvers; non-optimisation tests |
| Filler / empty-slot invention | Explicit empty-capacity tests; no unauthored tasks |
| Mission rows as mastery / readiness store | Domain projections only; dual truth vs ORM named |
| Mission Completion treated as mastery | Evidence hooks Behaviour/planning only; no Twin writes |
| Warrant stripped at composition | Explicit cold-start / low-warrant tests; forbidden Mid coercion |
| Action-family / tension collapse | Preserve revise ≠ study ≠ assess ≠ diagnostic ≠ rest-protect |
| Planning / Mission ownership collapse | No WeekPlan types/policy in package; boundary docs |
| Legacy dual mission authority deepening | Stage A only; no hybrid adapters |
| Confidence contamination in packing | Risk-framing only when Decision cited |
| LLM ownership creep | Framework purity + no network compose authority |
| V1 Section hard-requirement | Compose Decision identities as-is; V1 fixture tests |
| Curriculum invention | Cite Decision lineage only |
| Thrashing / preference blindness | Optional journal context; dismiss ≠ mastery |
| Ignoring constraints or erasing need under constraints | Feasibility acknowledgements required; no rejected-candidate substitution |
| Opaque mission packs | Mandatory Decision attribution from first ship |
| Confusing domain Mission with ORM Mission | Distinct package; import/docs firewall; no silent alias |

---

# Appendix C — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.10.3 — Mission Intelligence Implementation Plan |
| Nature | Planning only |
| Code impact | None (this milestone) |
| Migration impact | None (planned implementation also expects None) |
| Curriculum V1/V2 | Compatibility required; Decision lineage reuse planned; no traversal redesign |
| Application code intentionally untouched | Yes (this milestone) |
| Upstream gate | Capability 2.10.1 — APPROVED; Capability 2.10.2 — APPROVED |
| Governing principle | Mission Intelligence is an execution layer; it operationalises Decisions; it does not decide |
| Next | Structural implementation milestone (separate) — not started here |

---

*End of Capability 2.10.3 Mission Intelligence Implementation Plan. STOP.*
