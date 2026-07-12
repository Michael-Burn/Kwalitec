# Capability 2.10.2 — Mission Intelligence Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.10 Mission Generation Intelligence (architecture preceding structural contracts and implementation)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Educational charter:** [`CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md)  
**Upstream gate:** Capability 2.10.1 Educational Analysis — APPROVED  
**Companions:** [`CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md), [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_ARCHITECTURE.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md)  
**Scope:** Structural architecture for Decision → Mission / MissionTask execution — **no code, algorithms, scheduling optimisation, services, tests, schemas, or migrations**

---

## Document purpose

This milestone answers **how** Mission Intelligence is structured as architecture after Capability 2.10.1 approved **what** it is educationally.

Decision Engine supplies authoritative next-action selection (or an ordered Decision batch for a session window). Recommendation Engine optionally packages Decisions as attributable suggestions. Mission Intelligence is Epic 2’s **execution / projection layer**: it operationalises Decision(s) into today’s (or this session’s) Mission / MissionTask structure — without selecting actions, inventing ranking, mutating Twin beliefs, recomputing readiness, owning Recommendation packaging, or owning WeekPlan regeneration policy.

This note locks structural contracts so later milestones can add execution artefacts without inventing syllabus, coercing unknown readiness, filling empty slots with unauthored educational need, or forking a parallel next-action authority inside mission rows.

**Governing principle (binding):**

> **Mission Intelligence is an execution layer. It operationalises Decisions. It does not decide.**

**Non-goals of this document**

- Code, pseudocode algorithms, package layouts, or dataclass definitions  
- Database schemas, Alembic migrations, or ORM layouts  
- Scheduling optimisation, packing solvers, load-balancing formulas, or session packing math  
- Ranking formulas, selection math, priority scores, or optimization objectives  
- UI redesign, gamification, dashboards, notifications, or social features  
- Decision Engine or Recommendation Engine redesign beyond interaction boundaries  
- Replacement of Curriculum Engine, Evidence Model, Twin aggregate, Readiness Aggregation, Decision Engine, or Recommendation Engine contracts  
- Deepening legacy mission-generation heuristics as Twin-first / Decision-first authority  

**Hard architectural rules (binding):**

1. Mission Intelligence never selects or re-selects next actions.  
2. Mission Intelligence never invents ranking that disagrees with Decision reason codes.  
3. Mission Intelligence never mutates Twin belief domains.  
4. Mission Intelligence never recomputes readiness or coerces unknown / low-warrant / `not_yet_knowable` into Mid or High preparedness.  
5. Mission Intelligence never invents curriculum identities, evidence ids, or Twin beliefs.  
6. Every core educational MissionTask must be attributable to a Decision and preserve the explainability chain.  
7. Completing a Mission does not grant mastery; completion / assessment evidence does.  
8. Empty capacity is not educational authority to invent tasks Decision did not author.  
9. Scheduling optimisation solvers are forbidden in this architecture charter.  
10. Curriculum V1 and V2 remain loadable; task identities come only from Decision / Curriculum lineage.

---

# 1. Mission model

## 1.1 Position

A **Mission** is the day’s (or session’s) executable projection of one Decision or an ordered Decision batch: a concrete, attributable task set the student can attempt within Goals capacity and Constraints.

```
CurriculumContext + Goals + Constraints
        +
Digital Twin domains
        +
ReadinessState
        ↓
Decision Engine                 (read-side next-action selection)
        ↓
Decision / Decision batch
   (selected action(s) + candidates + reason codes + lineage + warrant posture)
        ↓
Explainable Recommendation Engine   (optional sibling packaging / projection)
        ↓
Mission Intelligence            (execution-layer operationalisation)
        ↓
Mission / MissionTask artefacts
        ↓
Mission Completion / Failure → Learning Evidence → Behaviour (via Update Pipeline)
```

## 1.2 Architectural classification

| Kind | Role |
|---|---|
| **Mission** | Live execution result for one session/day window — Mission Intelligence’s primary output |
| **Mission operationalisation** | Mapping authorised Decision action(s) into Mission / MissionTask structure without re-selecting educational value |
| **Not a write-path Twin belief domain** | No Update Strategy evolves Mission from evidence as mastery/retention |
| **Not educational-state authority** | Twin domains remain sole authority for beliefs; Mission is a product consequence |
| **Not selection authority** | Decision Engine alone selects; Mission never re-ranks |
| **Sibling to Recommendation projection** | Capability 2.9 packages Decisions as suggestions; packaging ≠ day composition |
| **Not WeekPlan policy** | Planning owns multi-day / multi-week structure; Mission owns executable now |

## 1.3 Architectural properties

| Property | Requirement |
|---|---|
| **Execution-layer** | Produced by operationalising Decision(s) + execution context |
| **Decision-bound** | Every MissionTask cites Decision authority (single Decision or Decision-batched action) |
| **Deterministic core attribution** | Same Decision batch + same execution context in → same attributable Mission projection out |
| **Explainable by construction** | Preserves Decision reason codes + lineage into MissionTask attribution |
| **Curriculum-bound** | Curriculum-scoped tasks use official syllabus identities only |
| **Warrant-honest** | Evidence Warrant / cold-start posture survives into mission composition |
| **Feasibility-respecting** | Goals capacity, Constraints, and Behaviour sustainability shape load volume — not educational priority |
| **Regenerable** | When Decisions / Twin / Goals / Constraints change, missions may be recomposed; stale rows are not Twin truth |
| **Non-authoritative for beliefs** | Mission Completion does not grant mastery; Behaviour / planning evidence paths do |

## 1.4 Conceptual shape — Mission (contract, not schema)

| Slot | Architectural role |
|---|---|
| **Scope identity** | Student / curriculum / sitting (Goal) / session or day window the Mission applies to |
| **MissionTask set** | Ordered or prioritised executable tasks projected from Decision(s) |
| **Decision / batch references** | Identity of Decision(s) being operationalised (selection authority) |
| **Attribution / reason citations** | Decision reason codes + lineage hooks preserved on tasks |
| **Warrant / cold-start posture** | Evidence-density honesty inherited from Decision(s) |
| **Feasibility acknowledgements** | How Goals / Constraints / execution context shaped load volume |
| **Regeneration identity** | Enough Decision / Twin snapshot reference that recomposition can replace stale missions |
| **Evaluation context** | Curriculum format awareness (V1/V2), Mission Intelligence / Decision version tags for audit |

## 1.5 What Mission is not

- A Decision or re-ranked candidate list  
- A readiness score or factor recomputation  
- A Knowledge / Memory / Behaviour / Performance belief store  
- A Recommendation packaging artefact (titles / explanation ownership remain 2.9)  
- A WeekPlan or multi-week planning policy  
- A parallel mastery map inside mission rows  
- A private ranking score as educational authority  
- A black-box coach utterance without Decision reason codes  
- A scheduling optimisation result that invents educational need  

## 1.6 Ownership

| Concern | Owner |
|---|---|
| Producing Decision (selection) | Decision Engine (Capability 2.8) |
| Packaging Decision into Recommendation | Explainable Recommendation Engine (Capability 2.9) |
| Operationalising Decision(s) into Mission / MissionTask | **Mission Intelligence (Capability 2.10)** |
| Twin belief domains | Update Strategies via Twin Update Pipeline |
| Preparedness context | Readiness Aggregation (Capability 2.7) |
| Syllabus identities and weights | Curriculum Engine / CurriculumService helpers |
| WeekPlan regeneration policy | Planning ownership |
| Recording Mission Completion / Failure | Product recording paths → Learning Evidence |
| Selecting next action | **Decision Engine only** |

---

# 2. MissionTask model

## 2.1 Position

A **MissionTask** is a single executable unit within a Mission. It is the atomic projection of an authorised Decision action (or one action from a Decision-authored batch) into session/day structure.

## 2.2 Architectural properties

| Property | Requirement |
|---|---|
| **Decision-attributable** | Every core educational MissionTask cites Decision selected action + reason codes + lineage |
| **Action-family faithful** | Study / revise / assess / diagnostic / rest-protect preserved from Decision — not collapsed |
| **Curriculum-scoped when applicable** | Canonical syllabus identity from Decision / CurriculumContext lineage only |
| **Non-authoritative for beliefs** | Completing a MissionTask is Behaviour / planning evidence candidate — not mastery |
| **Explainable** | “Why this task?” answers via Decision reason codes, not a private mission priority score |
| **Feasibility-shaped, not re-selected** | Load / intensity may be demoted under Constraints; educational action identity may not be swapped for packing convenience |

## 2.3 Conceptual shape — MissionTask (contract, not schema)

| Slot | Architectural role |
|---|---|
| **Task identity** | Stable id within Mission for execution / completion recording |
| **Action family** | Preserved from Decision selected action (study / revise / assess / diagnostic / rest-protect) |
| **Curriculum scope** | Official syllabus identity when Decision was curriculum-scoped |
| **Decision reference** | Decision (and candidate contrast hooks when useful) that authorised this task |
| **Reason-code citations** | Machine-readable Decision factors preserved for attribution |
| **Lineage citations** | Twin / evidence / curriculum / readiness hooks carried from Decision — never fabricated |
| **Warrant posture** | Inherited honesty when Decision warrant / cold-start is thin |
| **Feasibility acknowledgement** | How session capacity / sustainability shaped inclusion or intensity |
| **Optional Recommendation language hook** | May surface 2.9 packaging already narrated from Decision — never as competing selection |
| **Completion / failure linkage** | Hooks for Behaviour / planning evidence recording — not mastery grants |

## 2.4 What MissionTask is not

- A second Decision among candidates  
- A Recommendation title ownership contract  
- A private mastery / readiness / priority score store  
- A filler slot inventing educational need Decision did not author  
- A collapsed “generic study block” that erases Decision action-family tension  

## 2.5 Mission ↔ MissionTask relationship (binding)

1. A Mission contains zero or more MissionTasks for one session/day window.  
2. Every core educational MissionTask must be attributable to Decision authority.  
3. Mission order / priority presentation must not invent ranking that disagrees with Decision reason codes or Decision-authored batch order.  
4. Empty Mission capacity (few or no tasks) is a **feasibility remainder**, not a defect requiring invented tasks.  
5. MissionTasks are regenerable projections; they must not ossify into Twin forks.

---

# 3. Inputs

## 3.1 Input principle

Mission Intelligence **consumes** Decision authority and supporting execution context. It **never modifies** Twin domains, readiness beliefs, or Decision selection. Same Decision batch + same execution context in → same attributable Mission projection out.

## 3.2 Primary input: Decision / Decision batch

| Decision element | Architectural role for Mission Intelligence |
|---|---|
| **Selected action** | The educational action(s) to operationalise — action type + curriculum scope when present |
| **Ordered Decision batch (when present)** | Decision-authored multi-action set for a session window; Mission shapes fit, not educational priority |
| **Candidate set** | Supports “why this task, not that?” attribution; Mission must not promote rejected candidates as equal authority |
| **Reason codes** | Stable factors MissionTasks must preserve for explainability |
| **Value rationale hooks** | Educational “why now” substance carried into task attribution — not marketing slogans |
| **Lineage references** | Twin / evidence / curriculum / readiness hooks already present on the Decision |
| **Constraint acknowledgements** | Feasibility / intensity demotion already decided upstream — Mission must not erase or over-claim |
| **Warrant posture** | Inherited honesty when readiness or Twin evidence density is low |
| **Evaluation context** | Curriculum format awareness (V1/V2), Decision version tags for audit |

**Binding:** Mission operationalises the Decision’s selected action(s). It does not re-select among candidates.

## 3.3 Supporting input: Recommendation (optional)

| Input | Architectural role | Authority |
|---|---|---|
| **Recommendation packaging** | Optional sibling projection that may supply student-facing language already narrated from Decision | Communication only |
| **Recommendation Reasons / warrant posture** | May be surfaced on MissionTasks when present | Never competing selection |

**Binding:** Recommendation is not required for Mission validity. Mission may project Decision(s) directly. When Recommendation language is used, it must remain Decision-faithful. Recommendation Priority must never become a private mission ranking engine.

## 3.4 Supporting inputs (execution context)

| Input | Architectural role | Authority |
|---|---|---|
| **CurriculumContext** | Confirm task scopes remain canonical; support V1/V2 fidelity via Decision / Curriculum lineage | Curriculum Engine via canonical helpers |
| **Goals** | Active paper / sitting, deadline context, committed capacity bound how much work a day/session may carry | Destination and capacity bound |
| **Constraints** | Available time now / session length, sustainable intensity, Behaviour burnout flags, other operational limits | Feasibility bound — demotes load; does not invent educational need |
| **Current session window** | Temporal container for today’s / this session’s Mission | Fit container |
| **Already-committed work** | Avoid double-booking capacity beyond Goals / Constraints honesty | Capacity honesty |
| **Decision Journal history (when available)** | Avoid thrashing composition that ignores recent dismiss without treating dismiss as mastery | Preference history — not mastery |
| **Prior Mission Completion / Failure patterns (as Behaviour evidence context)** | Inform feasibility honesty | Never treat adherence as exam readiness or mastery |
| **Self-report Confidence (when Decision framed it)** | May appear only as risk-framing if Decision already framed it that way | Decision-cited framing only |

## 3.5 Input contract (binding)

1. **Decision is the sole selection authority input** — Mission never re-ranks.  
2. **Recommendation is optional packaging, not authority** — Mission may use it for language; never for competing selection.  
3. **CurriculumContext is canonical** — V1/V2 via Decision / Curriculum lineage only; built via canonical Curriculum helpers outside Mission ownership.  
4. **Goals define destination and capacity** — not Twin beliefs.  
5. **Constraints bound ambition** — they do not invent need or erase high-weight Decision by silent substitution.  
6. **Student execution context shapes fit, not authority** — time and sustainability inform composition volume.  
7. **Evidence Warrant is non-optional honesty** — cold start and low warrant survive into mission posture.  
8. **No legacy hybrid truth** — do not average TopicProgress / readiness % with Twin/Decision factors as temporary mission authority.  
9. **No filler authority** — empty capacity is not permission to invent educational tasks Decision did not author.

## 3.6 What is not an input authority

- UI streak counters as educational value justification  
- Mission Completion counts as mastery proof or readiness proof  
- Opaque “fill the day” product defaults without Decision  
- Coach/LLM free-text topic invention  
- Legacy mission heuristics / private priority scores as Twin-first authority  
- Legacy `ReadinessService` overall % as Decision substitute  
- Recommendation packaging scores as a secret second Decision Engine  
- Raw readiness scores as direct mission scheduling authority  

---

# 4. Execution pipeline

## 4.1 Position

The execution pipeline is the **architectural sequence** of read-side / projection stages that turn Decision(s) into a Mission. It is a structural contract — not an algorithm, ranking function, or scheduling optimisation solver.

## 4.2 Pipeline stages (architectural)

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
8. Emit Mission container + regeneration identity
        ↓
Mission / MissionTask artefacts
```

## 4.3 Stage obligations

| Stage | Obligation | Forbidden |
|---|---|---|
| **Bind Decision / batch** | Decision(s) are the sole selection authority for this Mission | Mission without Decision; inventing a Decision |
| **Validate preconditions** | Require selected action(s) + reason codes on the core path | Opaque tasks without codes |
| **Bind execution context** | Consume Goals / Constraints / session window as fit bounds | Treat context as a second selector |
| **Operationalise actions** | Map Decision selected action(s) to MissionTasks | Re-select among candidates; invent topics; promote rejected candidates |
| **Shape feasible load** | Fit authorised work into capacity; prefer learning-value tasks already authorised | Scheduling solvers that invent educational need; empty-slot filler |
| **Preserve attribution / warrant** | Carry Decision reason codes, lineage, cold-start honesty | Mid/High preparedness theatre; stripped warrant |
| **Optional Recommendation language** | Surface 2.9 packaging when present and Decision-faithful | Recommendation Priority as mission ranker |
| **Emit Mission** | Produce regenerable Mission container | Store private mastery / readiness / competing priority as educational truth |

## 4.4 Pipeline principles (binding)

1. **Execution only** — no selection enrichment inside operationalisation.  
2. **Decision-first always** — no readiness-first scheduling, no streak-first scheduling.  
3. **Deterministic attribution** — composition templates may vary presentation; they may not vary educational authority.  
4. **Write/read firewall** — no Twin Update Pipeline bypass; no readiness recomputation.  
5. **No ranking stage** — there is no mission score that can change which educational actions are authorised.  
6. **No scheduling optimisation stage** — packing math that effectively re-selects educational value is forbidden in this charter.  
7. **Learning value over activity theatre** — prefer authorised learning-value tasks; do not invent filler to make the day look complete.  
8. **Empty capacity is honest** — leftover time is a feasibility remainder, not authority to invent tasks.

## 4.5 Explicitly deferred

- Exact Mission / MissionTask artefact schema  
- Exact regeneration timing / triggers  
- Exact UI for mission boards  
- Numeric packing / scheduling formulas (if ever approved later, still subordinate to Decision)  
- WeekPlan regeneration algorithms (planning ownership)  
- Coach phrasing models  

---

# 5. Decision interaction

## 5.1 Separation of concerns

| Concern | Owner |
|---|---|
| Highest-value next action + reason codes + candidates + lineage + warrant inheritance in selection | **Decision Engine (2.8)** |
| Session/day operationalisation of authorised Decision(s) into Mission / MissionTask structure | **Mission Intelligence (2.10)** |

## 5.2 Dependency direction

```
Decision Engine
        ↓
Decision (selected action + candidates + reason codes + lineage + warrant posture)
   (optionally a Decision batch for a session window)
        ↓
Mission Intelligence
        ↓
Mission / MissionTask artefacts
```

**One-way authority:** Decision → Mission. Mission never feeds a competing selection back into Decision within the same reasoning turn.

Educational Intelligence Architecture rule preserved:

> **Mission Generation depends on the Decision Engine rather than on Readiness directly.**

## 5.3 Binding rules

1. Decision Engine remains **selection authority**.  
2. Mission Intelligence **must not invent ranking** that disagrees with Decision reason codes.  
3. Mission Intelligence **may compose** authorised Decision(s) into a feasible session/day set; it may not invent evidence, syllabus topics, Twin beliefs, or substitute rejected candidates as equal authority.  
4. Multi-action session batches remain **Decision-authored** (or Decision-batched); Mission shapes fit, not educational priority.  
5. Accept/dismiss and Mission Completion are preference / Behaviour evidence — never mastery.  
6. Execution must not introduce scheduling optimisation formulas that effectively re-select educational value “for packing convenience.”  
7. If Decision and Mission disagree about what the student should learn next, **Decision is correct and Mission composition is wrong**.

## 5.4 What Mission never does in this relationship

- Re-select among Decision candidates  
- Drop or rewrite reason codes to soften educational tension  
- Present supportive Knowledge Strength as exam readiness when Decision did not claim readiness  
- Bypass Decision by writing missions from undocumented private ranks  
- Claim calibrated Confidence while Confidence domain ownership remains incomplete  
- Treat Mission Completion as proof the Decision “worked” for learning  
- Shortcut from raw ReadinessState to Mission without Decision  

---

# 6. Recommendation interaction

## 6.1 Separation of concerns

| Concern | Owner |
|---|---|
| Attributable next-action suggestion packaging | **Recommendation Engine (2.9)** |
| Session/day task-set operationalisation | **Mission Intelligence (2.10)** |

Recommendation packaging and Mission composition are **sibling projections**, not the same capability.

## 6.2 Dependency chain

```
Decision Engine
        ↓
Explainable Recommendation Engine   (optional product surface)
        ↓
Mission Intelligence                (session/day projection from Decision / Decision batches)
        ↓
Mission / MissionTask artefacts
```

Mission may:

- project Decision(s) directly; or  
- surface Recommendation language already narrated from Decision.

Mission must not:

- require Recommendation to exist before a Mission is valid;  
- treat Recommendation Priority as a competing selection score;  
- become the Recommendation Engine;  
- output Recommendation packaging artefacts as its primary contract.

## 6.3 Binding rules

1. **Keep 2.9 and 2.10 separate** — packaging a Decision is not composing today’s mission.  
2. Missions remain **consequences** of intelligence, not the learner model.  
3. Mission rows must **never** store private mastery, readiness, or competing recommendation ranks.  
4. Mission Completion ≠ mastery; Mission Completion ≠ exam readiness; Mission Completion ≠ proof the Recommendation “worked” for learning.  
5. A Mission may include a recommended action; it must not become a second Decision Engine or a second Recommendation Engine.  
6. If Recommendation copy and Mission task attribution disagree with Decision reason codes, **Decision wins**; packaging/composition must be corrected.

## 6.4 Firewall

Recommendation outputs Recommendations. Mission Intelligence outputs Missions. Neither mutates Twin beliefs. Neither invents syllabus. Neither treats recommendation or mission rows as educational-state authority. Neither selects next actions.

---

# 7. Planning interaction

## 7.1 Separation of concerns

| Concern | Owner |
|---|---|
| Multi-day / multi-week plan structure and regeneration policy (WeekPlan and related planning artefacts) | **Planning ownership** |
| Daily / session Mission operationalisation of Decision(s) | **Mission Intelligence (2.10)** |

Educational Intelligence Architecture treats Planning artefacts (WeekPlan, Mission) as *consequences* of intelligence — not as Twin domains or learner-model authority. Mission Intelligence executes Decisions into daily structure; it does not own WeekPlan strategy.

## 7.2 Architectural dependency shape

```
Goals + CurriculumContext + Twin + Constraints
        ↓
Decision Engine (authoritative next-action / batch)
        ↓
Mission Intelligence  →  Mission / MissionTask (today / session)
        ↓
Planning consumers may regenerate WeekPlan from Goals + Twin + Curriculum + time constraints
        (without treating WeekPlan or Mission as Twin truth)
```

## 7.3 Binding rules

1. **Plans and missions are consequences of intelligence, not the learner model.**  
2. WeekPlan regeneration must not silently become a second Decision Engine via private topic ranks.  
3. Mission Intelligence must not absorb WeekPlan policy and invent multi-week educational strategy under a “mission” label.  
4. Planning may consume Decisions / Missions as consequences; it must not store private mastery inside plan or mission rows.  
5. Capacity honesty flows Goals → Constraints → Decision acknowledgements → Mission load shaping → Planning capacity views — without hybrid legacy % truth.  
6. When Twin state changes, missions remain regenerable projections; planning must prefer recomposition over stale private mission-as-mastery stores.  
7. Explainability requires Decision reason codes between preparedness context and daily tasks; planning must not skip Decision.

## 7.4 Why Mission ≠ Planning ownership collapse

- Planning answers longer-horizon structure and capacity.  
- Mission answers executable now.  
- Collapsing them reintroduces activity theatre (“fill the week with tasks”) and dual authority.  
- Mission Intelligence must remain Decision-first execution, not a hidden WeekPlan strategy engine.

---

# 8. Constraint handling

## 8.1 Definition

**Constraint handling** is the architectural obligation that Goals capacity, Constraints, and Behaviour sustainability shape *how much* and *how intensely* authorised Decision actions fit into the current session/day — without inventing educational need or silently erasing Decision authority.

## 8.2 Constraint catalogue (architectural)

| Constraint class | Mission Intelligence use | Forbidden use |
|---|---|---|
| **Available time now / session length** | Bound how many authorised tasks fit | Invent filler to consume leftover minutes as if educationally authorised |
| **Goals committed capacity** | Bound day/session ambition within weekly/sitting honesty | Treat capacity remainder as permission to invent high-value claims |
| **Sustainable intensity / Behaviour burnout flags** | Demote volume or intensity; preserve rest-protect when Decision selected it | Ignore sustainability; or prefer rest always despite high-weight exam-risk Decision |
| **Decision-carried constraint acknowledgements** | Honour upstream feasibility demotions | Restore demoted polish; erase high-weight need under “too busy” theatre |
| **Already-committed work** | Avoid double-booking beyond honesty | Drop Decision-authorised learning value without acknowledgement |

## 8.3 Constraint principles (binding)

1. **Constraints bound ambition; they do not invent educational need.**  
2. **Constraints do not delete high-weight Decision authority by silent substitution.**  
3. **Feasibility demotion is educational fidelity** — unsustainable cram missions are fidelity failures.  
4. **Feasibility acknowledgements are mandatory** — Mission must record how load was shaped.  
5. **Empty capacity is a remainder, not a selector** — leftover time does not author tasks.  
6. **Rest/protect fidelity** — when Decision selected rest-protect for sustainability, Mission must not reframe it as failure or avoidance.  
7. **No scheduling optimisation solvers** in this charter — constraint handling is structural load shaping subordinate to Decision order/reason codes.

## 8.4 Constraint ↔ Decision relationship

Decision may already acknowledge constraints in selection. Mission Intelligence:

- **honours** those acknowledgements;  
- **may further demote volume/intensity** for the current session window;  
- **must not** invent a different educational priority list under constraint pressure;  
- **must not** promote rejected Decision candidates because they “fit better.”

---

# 9. Execution sequencing

## 9.1 Definition

**Execution sequencing** is the architectural concern of ordering MissionTasks within a Mission window when one or more Decisions (or a Decision batch) are operationalised.

## 9.2 Sequencing authority (binding)

| Source | Sequencing role |
|---|---|
| **Decision-authored batch order** | Primary educational order when Decision emits an ordered batch |
| **Decision reason codes / action families** | Preserve educational tension and action-family meaning in presented order |
| **Constraints / session fit** | May omit trailing authorised work that does not fit — with feasibility acknowledgement — without re-ranking educational value |
| **Recommendation Priority** | Never a sequencing authority |
| **Legacy mission heuristics / private scores** | Never a sequencing authority |
| **Raw readiness %** | Never a sequencing authority |
| **Packing / optimisation solvers** | Forbidden as educational sequencing authority in this charter |

## 9.3 Sequencing principles (binding)

1. **Educational order comes from Decision**, not from engagement or packing heuristics.  
2. **Omission under capacity ≠ re-selection** — leaving an authorised task out of *this* window because it does not fit is load shaping; substituting a rejected candidate is forbidden.  
3. **Preserve action families in sequence** — revise ≠ study ≠ assess ≠ diagnostic ≠ rest-protect.  
4. **Preserve educational tension** — do not collapse Knowledge vs Memory (or Behaviour vs Performance) into bland generic blocks for sequencing convenience.  
5. **No engagement-theatre urgency packing** — urgency/order reflects Decision-derived educational need and constraints, not notification dark patterns.  
6. **Deterministic attribution** — same Decision batch + same execution context → same attributable sequence meaning.  
7. **Future packing helpers (if ever approved)** remain subordinate to Decision order and reason codes — never become a secret selector.

## 9.4 Explicitly deferred

- Numeric session-packing formulas  
- Multi-day sequencing across WeekPlan horizons (planning ownership)  
- Exact UI reorder gestures and their educational meaning  

---

# 10. Explainability chain

## 10.1 Mandatory chain

Every core educational MissionTask must be able to answer **Why this task?** via:

```
Curriculum factor
    → Learning Evidence (or evidence aggregate)
        → Twin domain state factor(s)
            → Readiness factor (when relevant) + Evidence Warrant
                → Decision Engine reason code(s)
                    → MissionTask attribution
                       (optional Recommendation explanation narration)
```

Students must never be asked to trust a black-box daily task pack for core educational work.

## 10.2 Layer obligations for execution

| Layer | Mission Intelligence obligation |
|---|---|
| **Curriculum** | Present official identity / weight context from Decision lineage — never invented topics |
| **Evidence** | Carry evidence ids or honest aggregates when Decision carries them; absence under cold start is honesty |
| **Twin** | Carry domain factors Decision cited — preserve disagreements |
| **Readiness** | Carry factor posture + warrant only when Decision cites readiness; never schedule from raw readiness |
| **Decision** | Carry reason codes, selected vs considered candidates, constraint acknowledgements |
| **Recommendation (optional)** | May surface chain-supported packaging language — never invent disagreeing ranking |
| **Mission** | Complete the chain as executable structure — never invent private priority as educational authority |

## 10.3 Attribution requirements

1. MissionTask reason citations map to Decision reason codes.  
2. Candidate contrast uses Decision candidate set only.  
3. Warrant honesty appears whenever readiness or Twin evidence density is low.  
4. Attributions must not invent evidence, syllabus topics, or Twin beliefs.  
5. LLM / coach narration may only restate chain-supported attributions; it must not invent tasks.  
6. Post-hoc stories that disagree with Decision reason codes are forbidden.  
7. Completing a MissionTask records Behaviour / planning evidence only — not mastery.  
8. Feasibility acknowledgements remain visible when load was demoted.

## 10.4 Forbidden explanation patterns

- Opaque “today’s tasks” without Decision reason codes  
- Explanations that cite UI labels but not Twin/evidence/Decision codes  
- LLM-generated rationales that invent evidence, topics, or tasks  
- Narrating supportive Knowledge Strength as “you are exam ready”  
- Averaging away High Knowledge + Low Memory tension into a bland Mid pack  
- Treating Mission Completion as proof learning occurred or readiness rose  
- Presenting Performance string-tag heuristics as scored accuracy certainty  
- Stripping warrant / cold-start honesty for friendlier busywork packs  
- Hybrid stories that mix legacy readiness % with Twin factors as temporary “truth”  
- Private mission “priority %” as educational authority  
- Empty-slot filler framed as adaptive intelligence  

## 10.5 Audit artefacts

| Artefact | Role |
|---|---|
| Learning Evidence log | Immutable history |
| Twin snapshot / domain evidence ids | State lineage |
| ReadinessState attributions + warrant | Preparedness context lineage (when cited) |
| Decision / Decision State | Candidates + selected action + reason codes |
| Recommendation (optional) | Packaging consequence — not authority |
| Decision Journal | User response to recommendations |
| Mission / MissionTask | Daily structure consequence — not authority |
| Mission Completion / Failure evidence | Behaviour / planning signal — not mastery |

---

# 11. Cold-start behaviour

## 11.1 Definition

Cold-start behaviour is the execution posture when Goals may exist, Twin domains are thin, Readiness overall is `not_yet_knowable` / low Evidence Warrant, and Decision prefers **evidence-creating** actions (diagnostics, early assessments, structured first coverage of high-weight areas).

## 11.2 Execution posture (binding)

| Do | Do not |
|---|---|
| Compose MissionTasks that operationalise diagnostic / evidence-creating Decisions | Invent polish, advanced rehearsal, or “you’re nearly ready” task packs |
| Preserve low warrant / `not_yet_knowable` honesty in mission attribution | Claim Mid or High readiness to “motivate” a fuller day |
| Prefer a small honest diagnostic-shaped mission over a busy false-personalised mission | Fill empty slots with unauthored topics to look adaptive |
| Keep Mission Completion expectations proportionate to thin history | Shame the student for lacking history via overloaded missions |
| Regenerate as warrant grows and Decisions change | Ossify cold-start filler as if it were a mastery map |
| Keep curriculum weight honesty when Decision scopes high-weight first coverage | Invent a fake personalised priority tree inside mission rows |

## 11.3 Cold-start principles

1. **Unknown is a first-class execution state** — not an error to hide with busywork.  
2. **Diagnostics are high-value missions** — evidence-creating tasks are not “filler until real missions arrive.”  
3. **Warrant inheritance is mandatory** — Decision’s cold-start honesty must survive composition.  
4. **No coercion** — never rewrite `not_yet_knowable` into Mid preparedness mission narratives.  
5. **No legacy percentage theatre** — do not fill empty Twin warrant with TopicProgress composites as if Twin-first truth.  
6. **No second reasoner under cold start** — thin evidence is not permission for Mission Intelligence to invent ranking.  
7. **No Mid/High theatre packing** — composition that hides diagnostic intent, over-packs the day, or over-promises preparedness fails educational fidelity even if the underlying Decision was correct.

## 11.4 Relationship to Decision and Recommendation cold-start postures

| Layer | Cold-start job |
|---|---|
| **Decision** | Selects evidence-creating actions under low warrant |
| **Recommendation** | Says so clearly in packaging |
| **Mission Intelligence** | Composes executable structure that still says so |

---

# 12. Legacy convergence

## 12.1 Current legacy posture

Product-facing ancestors (heuristic mission / plan generators, TopicProgress-based readiness composites, related planning consumers, and any private mission priority scores) currently provide daily-task and readiness-like signals without Twin-first Decision authority.

## 12.2 Convergence principle (binding)

Epic 2 requires Decision Engine to become the **authoritative next-action reasoner**, with Mission Intelligence operationalising Decision — not inventing a second ranker or a private mastery store inside mission rows. Migration is **additive**: preserve behaviour where needed, redirect authority, retire divergent selection truth. Do **not** deepen legacy mission ranking / filler generation while Decision-first execution contracts land. Do **not** hybrid-average legacy % with Twin factors as temporary authority.

## 12.3 Convergence path (architectural stages)

| Stage | Meaning |
|---|---|
| **A — Coexistence** | Legacy mission / plan generators continue for product surfaces; Decision-first Mission contracts land without claiming cutover |
| **B — Adapter** | Adapters expose Decision-operationalised Missions beside legacy task packs; dual truth is explicit and temporary |
| **C — Twin-first Decision execution authority** | New Educational Intelligence paths consume Decision → Mission; legacy private priority scores cease to be execution authority |
| **D — Retire divergent math** | Remove or quarantine legacy mission heuristics that disagree with Twin-first Decision |

## 12.4 Adapter rules during coexistence

1. Adapters must not silently rewrite Twin beliefs.  
2. Adapters must not present legacy overall % as Twin-first readiness or Decision authority.  
3. Dual truth must be **named** in architecture/docs during coexistence — not papered over as one score.  
4. Mission Intelligence must operationalise Decision, not invent a third ranker.  
5. Recommendation packaging (2.9) and Mission execution (2.10) must remain separate during cutover.  
6. Planning / WeekPlan consumers must not treat legacy mission rows as Twin truth.  
7. Freeze deepening of legacy mission ranking / filler generation as Twin-first truth.

## 12.5 Explicit non-goals of this milestone

- Implementing adapters  
- Cutting over UI  
- Deleting legacy mission / plan services  
- Deepening TopicProgress / heuristic mission math  
- Schema for Mission / MissionTask persistence  
- Scheduling optimisation during coexistence  

---

# 13. Risks

| Risk | Architectural impact | Mitigation |
|---|---|---|
| **Mission becomes a second Decision Engine** | Twin-first / Decision-first authority fractures; unexplained task invention | Operationalise Decision only; never author competing selection/priority lists |
| **Readiness → Mission shortcut** | Activity theatre (“schedule filler to raise readiness”); missing Decision explainability | Mission depends on Decision, not raw readiness |
| **Recommendation Priority used as secret ranker** | Packaging becomes selection; 2.9/2.10 collapse | Treat Recommendation as optional language; Decision remains authority |
| **Scheduling optimisation creep** | Packing solvers invent educational need or re-order value | Forbid optimisation-as-selection in this charter; Decision owns educational order |
| **Filler / empty-slot invention** | Low-value busywork presented as adaptive intelligence | Empty capacity ≠ authority to invent tasks |
| **Mission rows as mastery / readiness store** | Stale private state; broken audit; parallel learner model | Missions are projections only; regenerate from Decisions |
| **Mission Completion treated as mastery or exam readiness** | Silent educational falsehood; Behaviour contaminated into Knowledge/Performance | Completion/failure → Behaviour / planning evidence only |
| **Warrant stripped at composition** | False preparedness; dishonest cold start | Carry warrant / cold-start honesty into MissionTask attribution |
| **Write/read firewall breach** | Mission path mutates Twin or recomputes readiness | Execution is projection-only; no Update Pipeline bypass |
| **Planning / Mission ownership collapse** | WeekPlan policy hidden inside mission generation; dual strategy | Keep Planning vs Mission boundaries explicit |
| **Legacy dual mission authority** | Heuristic mission generators disagree with Decision | Freeze heuristic deepening; Decision-first cutover; no hybrid average truth |
| **Confidence contamination in scheduling** | Self-report upgrades task aggressiveness as if mastery | Risk-framing only when Decision already framed it |
| **Domain / action-family collapse** | Revise packed as study; Performance packed as Knowledge busywork | Preserve Decision action families in MissionTasks |
| **LLM ownership creep** | Non-determinism; invented syllabus/evidence/tasks | Coach narrates; Decision selects; Mission operationalises |
| **Thrashing / preference blindness** | Recompose dismissed work without lineage honesty | Consume Decision Journal / Behaviour context; dismiss ≠ mastery |
| **Ignoring constraints** | Unsustainable missions; burnout; dismiss thrashing | Constraints demote load; record feasibility acknowledgements |
| **Ignoring constraints’ opposite** | Feasibility used to erase high-weight educational need | Constraints bound ambition; they do not delete Decision authority by silent substitution |
| **Curriculum invention / V1 breakage** | Parallel topic trees; broken plans | Canonical identities only; CurriculumContext via canonical helpers |
| **Opaque mission packs** | Students cannot answer Why?; Epic 2 thesis fails | Mandatory Decision attribution; no “today’s tasks” without codes |
| **Premature packing formulas** | Unmaintainable “UX packing scores” become de facto rankers | No scheduling optimisation / selection formulas inside 2.10.2 |

---

# 14. Extensibility

## 14.1 Extension points

| Future capability | How it extends without breaking architecture |
|---|---|
| **Decision batches for a session window** | Decision Engine may emit ordered batches; Mission still only operationalises; selection ownership unchanged |
| **Richer MissionTask templates** | Add execution forms over the same Decision actions/lineage; never add private ranking |
| **Feasibility-aware volume banding** | Shape how many authorised tasks fit; still never invent unauthored educational actions |
| **Regeneration policies** | Recompose when Twin/Decision/Goals change; missions remain disposable projections |
| **Decision Journal personalisation** | Accept/dismiss inform Behaviour and future Decision candidate preference via Evidence → Strategies — not silent Mission-side Twin writes |
| **Insight / AI Coach surfaces** | Read Mission + Decision attribution; never silent Twin writes; never own selection |
| **Analytics on reason codes in missions** | Compare MissionTasks via Decision codes without opaque mission scores as authority |
| **Legacy mission cutover** | Redirect product surfaces from heuristic mission generation to Decision-first execution without hybrid formulas |
| **Confidence calibration domain** | May enrich risk-framing once owned; still never upgrades mastery/readiness via mission packing |
| **Institutional overlays** | Observe Missions; do not fork student-owned Twin or invent syllabus |
| **Later approved packing helpers** | If ever approved, remain subordinate to Decision order and reason codes — never become a secret selector |

## 14.2 Compatibility guarantees to preserve

1. Decision Engine remains the only next-action selector.  
2. Recommendation Engine remains packaging / projection only.  
3. Mission Intelligence remains execution / projection only — **it does not decide**.  
4. Readiness remains preparedness judgement only.  
5. Twin remains sole educational-state authority.  
6. Curriculum V1 and V2 remain loadable; identities via canonical helpers.  
7. Evidence append-only semantics remain permanent.  
8. Deterministic cores remain free of required network LLM calls.  
9. Missions remain projections of Decisions, not of readiness scores or packaging scores.  
10. Mission Completion / Failure remains Behaviour / planning evidence, not mastery.  
11. Plans and missions remain consequences of intelligence, not the learner model.  
12. Scheduling optimisation never becomes a secret Decision Engine inside Mission Intelligence.

## 14.3 Deliberately unlocked

Not locked by this architecture beyond ownership:

- Exact Mission / MissionTask artefact schema  
- Exact regeneration timing / triggers  
- Exact UI for mission boards  
- Exact coexistence mechanics with legacy mission services  
- Numeric packing / scheduling formulas (if ever approved later, still subordinate to Decision)  
- WeekPlan regeneration algorithms (planning ownership)  
- Numeric Decision enrichment (remains Decision-owned if ever approved)  
- Coach phrasing models  

---

# 15. Recommendations

## 15.1 Implementation sequence (separate milestones)

1. **Structural execution contracts** — Mission / MissionTask / attribution / warrant posture / feasibility acknowledgement / regeneration identity shapes (still no scheduling optimisation).  
2. **CurriculumContext builder** — thin orchestration using canonical Curriculum helpers before any live Mission consumer that needs syllabus lineage beyond Decision-carried identities.  
3. **Execution skeleton** — Decision / Decision batch in → attributable Mission out; cold-start honesty first; empty capacity remains honest.  
4. **Completion / failure evidence path** — Mission Completion / Failure as Behaviour / planning evidence only (no mastery writes).  
5. **Legacy convergence stages** — adapters → Twin-first Decision execution authority → retire divergent math.  
6. **Planning consumers** — WeekPlan regeneration continues under planning ownership; consume Missions as consequences, never as Twin truth.  
7. **Optional coach narration** — only as chain-supported rephrase after attribution contracts are proven.

## 15.2 Binding design recommendations

1. Treat composition as **operationalisation of Decision**, not negotiation with engagement or packing heuristics.  
2. Preserve educational **tensions** and **action families** in MissionTasks.  
3. Prefer **diagnostic honesty** under cold start over busy false-personalised days.  
4. Keep **Mission Completion** explicitly Behaviour-tied and vocabulary-disambiguated from mastery / readiness.  
5. Require **Decision attribution** on every core educational MissionTask early — “why this task?” is educationally load-bearing.  
6. Do not deepen legacy mission ranking / filler generation while Decision-first execution contracts land.  
7. Keep Recommendation packaging (2.9) and Mission execution (2.10) separate — package and compose as siblings, not one god layer.  
8. Keep Planning / WeekPlan ownership distinct — Mission Intelligence must not absorb multi-week strategy.  
9. Encode Educational Reasoning / Decision / Recommendation conditions as execution invariants before any production consumer.  
10. Plan cutover so new Educational Intelligence surfaces never treat legacy mission heuristics or `ReadinessService.get_overall_readiness` as Twin-first / Decision-first authority.  
11. Ship / reuse thin `CurriculumContext` building (orchestration layer) before any live Mission consumer that needs syllabus lineage beyond Decision-carried identities.  
12. Treat leftover capacity as a **feasibility remainder**, not as permission to invent educational value.  
13. Never let Mission invent ranking that disagrees with Decision reason codes.  
14. Never grant mastery on Mission Completion.  
15. Never introduce scheduling optimisation solvers inside Capability 2.10 as educational authority.

## 15.3 Architecture compliance checklist

| Invariant | Status for this architecture |
|---|---|
| Twin is sole educational-state authority | Mission consumes lineage; does not fork beliefs |
| Evidence is only legitimate belief input | Completion/failure becomes evidence via recording paths; Mission does not mutate beliefs |
| Strategies own domain evolution | Mission is not a write strategy |
| Decision ≠ Recommendation packaging ≠ Mission execution; Readiness ≠ next action | Binding |
| Activity ≠ learning value; Confidence ≠ mastery; Behaviour ≠ learning; Mission Completion ≠ mastery | Binding |
| Curriculum V1/V2 compatibility | Required; canonical identities only |
| No LLM ownership of core selection or invented tasks | Binding |
| Mission remains an execution projection of Decision | Binding |
| Mission does not decide | Binding |
| No implementation / algorithms / scheduling optimisation in this milestone | Satisfied |

## 15.4 Explicit stop line

This milestone delivers **architecture only**.

**Do not proceed in this milestone to:** code, algorithms, scheduling optimisation, scoring, dataclasses, services, tests, database changes, Decision/Recommendation redesign, or UI.

**Next engineering step (separate milestone):** structural execution contracts and/or implementation plan for Capability 2.10 — then implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot lineage may be cited; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains Decision consumed; Mission operationalises without modification; Completion/Failure may feed Behaviour via evidence |
| 2.7 | Readiness Aggregation | May appear in attribution when Decision cites readiness; never schedules missions directly |
| 2.8 | Decision Engine | Supplies Decision authority that Mission operationalises |
| 2.9 | Explainable Recommendation Engine | Sibling packaging projection; optional language source; not selection |
| **2.10.1** | **Mission Intelligence Educational Analysis** | Approved educational charter this architecture implements structurally |
| **2.10.2** | **Mission Intelligence Architecture** | **This document** |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.10.2 — Mission Intelligence Architecture |
| Nature | Architecture only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required; no traversal changes introduced |
| Application code intentionally untouched | Yes |
| Upstream gate | Capability 2.10.1 — Mission Intelligence Educational Analysis — APPROVED |
| Prior | Capability 2.10.1 — Mission Intelligence Educational Analysis (approved) |
| Next | Structural execution contracts / implementation plan (separate milestone) — not started here |
| Governing principle | Mission Intelligence is an execution layer; it operationalises Decisions; it does not decide |

---

*End of Capability 2.10.2 Mission Intelligence Architecture. STOP.*
