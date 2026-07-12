# Capability 2.10.1 — Mission Intelligence Educational Analysis

**Status:** Educational / architecture analysis — analysis only  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.10 Mission Generation Intelligence (educational analysis preceding architecture and implementation)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream gate:** Educational Reasoning stack complete — Curriculum Intelligence, Student Digital Twin, Readiness Aggregation, Decision Engine, Recommendation Engine approved  
**Companions:** [`CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md), [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md)  
**Scope:** Mission Intelligence definition, educational ownership, input/output boundaries, Decision/Recommendation/Planning relationships, execution principles, cold-start execution, risks, fidelity, and ownership principles — **no implementation, algorithms, scheduling optimisation, services, tests, schema, or migrations**

---

## Document purpose

This milestone answers what **Mission Intelligence** is as Epic 2’s execution layer: the educational capability that **operationalises Decisions** into today’s (or this session’s) task set — without selecting next actions, inventing ranking, mutating Twin beliefs, recomputing readiness, or owning WeekPlan regeneration policy.

Curriculum Intelligence, Student Digital Twin, Readiness Aggregation, Decision Engine, and Recommendation Engine are approved. Mission Intelligence is the next capability. It prepares Capability 2.10 architecture the same way Recommendation educational analysis prepared 2.9: **educational clarity first**, structural contracts later, scheduling optimisation forever forbidden inside this analysis.

**Governing principle (binding):**

> **Mission Intelligence is an execution layer. It operationalises Decisions. It does not decide.**

**Non-goals of this document**

- Code, pseudocode algorithms, dataclasses, or service refactors  
- Database schemas, Alembic migrations, or ORM layouts  
- Scheduling optimisation, load-balancing solvers, or session packing formulas  
- UI redesign, gamification, dashboards, notifications, or social features  
- Decision Engine or Recommendation Engine redesign beyond relationship boundaries  
- Replacement of Curriculum Engine, Evidence Model, Twin aggregate, Readiness Aggregation, Decision Engine, or Recommendation Engine contracts  
- Deepening legacy mission-generation heuristics as Twin-first / Decision-first authority  

---

# 1. Definition of Mission Intelligence

## 1.1 Canonical question

> **How do we turn authorised educational Decisions into this session’s (or today’s) executable task set without inventing a second reasoner?**

Not: what is the highest-value thing to do next (Decision Engine).  
Not: how prepared is the student for the sitting (Readiness).  
Not: what they know / retain / how they study / how they perform (Twin domains).  
Not: how the selected action is packaged as an attributable suggestion (Recommendation Engine).  
Not: how the multi-week plan is regenerated as planning policy (Planning / WeekPlan ownership).  
Not: what ranking or score should override Decision (forbidden — no second reasoner).

Decision Engine answers: *What should we do next?*  
Recommendation Engine answers: *How do we present that Decision honestly?*  
Mission Intelligence answers: *How do we operationalise Decision(s) into executable mission structure?*

## 1.2 Educational meaning

A **Mission** is a day’s (or session’s) set of prioritised learning tasks for the student — a **projection** of one or more Decisions into executable structure. It is not a second syllabus, not a Twin store, and not a selection engine.

**Mission Intelligence** is:

- **execution-layer only** — it operationalises Decisions into Mission / MissionTask structure; it does not author educational next-action selection;  
- **Decision-bound** — every Mission task is grounded in a Decision (or an ordered Decision batch for a session window) with reason codes, lineage, and warrant posture intact;  
- **curriculum-bound** — task identities remain official syllabus identities from Decision / CurriculumContext lineage, never free-text invention;  
- **feasibility-respecting** — Goals capacity, Constraints, and Behaviour sustainability shape *how much* can be scheduled now; they do not invent *what* is educationally valuable;  
- **explainable by construction** — mission tasks remain attributable to Decision reason codes; execution never invents private priority scores as educational authority;  
- **evidence-honest** — warrant, cold-start, and `not_yet_knowable` postures survive into mission composition and regeneration posture;  
- **non-authoritative for educational state** — Mission Completion is Behaviour / planning progress evidence, not mastery, not exam readiness;  
- **regenerable** — when Twin state and Decisions change, missions may be recomposed; stale mission rows never become a private learner model;  
- **deterministic in the core path for attribution** — same Decision batch + same execution context in → same attributable mission projection (no random theatre; no required LLM ownership of composition).

It is **not**:

- a second next-action selector or ranker;  
- a readiness aggregator or preparedness claim engine;  
- a write-side Twin domain Update Strategy;  
- a Recommendation packaging layer (titles, explanation narrative ownership remain 2.9);  
- a WeekPlan policy owner that invents multi-week educational strategy;  
- a motivation or engagement optimizer;  
- a scheduling solver that invents educational need to fill empty slots;  
- a black-box coach that invents syllabus, evidence, or Twin beliefs;  
- a permanent home for legacy mission heuristics that compete with Decision.

## 1.3 Distinctions (binding vocabulary)

| Concept | Educational question | Relation to Mission Intelligence |
|---|---|---|
| **Decision Engine** | What is the highest-value next learning action? | Owns selection; supplies Decision(s) that Mission operationalises |
| **Recommendation Engine** | How is that Decision packaged as an attributable suggestion? | Sibling projection; packaging ≠ day composition |
| **Mission Intelligence** | How are Decision(s) turned into today’s executable task set? | Owns session/day operationalisation of Decision authority |
| **Readiness** | Are we on track for the sitting? | May appear in Decision lineage; never selects or schedules via Mission |
| **Planning / WeekPlan** | How is multi-day capacity and plan structure maintained? | Planning owns plan artefacts; Mission Intelligence projects Decisions into daily missions without becoming a competing Decision Engine |
| **Decision State** | What was decided, among which candidates, with which reasons? | Audit / materialisation of Decision; Mission may cite it |
| **Decision Journal** | Did the student accept, dismiss, or defer a recommendation? | Preference / intent evidence; Mission must not treat dismiss as mastery or erase educational need |
| **Mission** | What is today’s (or this session’s) task set? | Executable projection owned by Capability 2.10 |
| **Mission Completion / Failure** | Did the student finish / miss / abandon the mission? | Learning Evidence for Behaviour and planning progress — not mastery |

Governing principle (Educational Intelligence Architecture §9.4 / §13):

> **Missions become adaptive consequences of Decision Engine output — not of raw readiness scores, and not as a private mastery model.**

Extended for this capability:

> **Mission is not Decision; Mission is not Recommendation packaging; Mission is not Readiness; Mission is not Twin; Mission never invents ranking, syllabus, Twin beliefs, or Mid/High preparedness from thin warrant; Mission never decides.**

## 1.4 Product purpose

Mission Intelligence exists so Kwalitec can:

1. Turn Decision Engine authority into a **concrete, executable daily / session task set**.  
2. Keep adaptive missions **Decision-first** — not readiness-first filler, not streak theatre.  
3. Respect **Goals capacity, Constraints, and Behaviour feasibility** when composing how much work fits *now*.  
4. Preserve **explainability** from Decision reason codes into MissionTask attribution.  
5. Keep Mission Completion / Failure as **Behaviour and planning evidence**, never as mastery or exam readiness.  
6. Converge legacy mission / plan ancestors toward **Decision-first execution** without inventing a parallel learner-state store inside mission rows.

## 1.5 Ubiquitous language anchors

| Term | Meaning |
|---|---|
| **Mission** | Day’s / session’s set of prioritised learning tasks — projection of Decision(s), not a second syllabus |
| **MissionTask** | A single executable unit within a Mission, curriculum-scoped when applicable, attributable to Decision lineage |
| **Mission Intelligence** | Execution layer that operationalises Decision(s) into Mission / MissionTask structure |
| **Operationalisation** | Mapping authorised Decision action(s) into executable structure without re-selecting educational value |
| **Execution context** | Student-facing feasibility now: available time, session window, capacity already committed, sustainability signals |
| **Projection** | Downstream artefact that must not change educational authority of the upstream Decision |
| **Mission Completion** | Evidence that required mission tasks were finished — Behaviour / planning signal, not mastery |
| **Mission Failure** | Evidence that a mission was missed, expired, abandoned, or failed criteria — Behaviour / planning signal, not mastery revocation of unrelated domains |
| **Regeneration** | Recomposition of Mission from fresh Decision(s) when Twin / Goals / Constraints change — missions remain disposable projections |

---

# 2. Educational Responsibilities

## 2.1 Owns

| Responsibility | Educational meaning |
|---|---|
| **Decision operationalisation** | Turn one Decision or an ordered Decision batch into Mission / MissionTask structure without changing selected educational actions |
| **Session / day composition** | Fit authorised actions into the current session or day window under Goals capacity and Constraints |
| **Feasibility shaping of load** | Reduce volume / intensity when Behaviour sustainability or Constraints require it — without inventing a different educational priority list |
| **Attribution preservation** | Carry Decision reason codes, lineage hooks, and warrant posture onto MissionTasks so “why this task?” remains answerable |
| **Curriculum identity fidelity** | Keep task scopes on canonical syllabus identities from Decision / CurriculumContext lineage |
| **Learning-value preference in composition** | Prefer composing authorised learning-value tasks over inventing filler to “complete” a day aesthetic |
| **Regenerability posture** | Allow missions to be recomposed when Decisions change; refuse to treat stale mission rows as Twin truth |
| **Completion / failure as evidence signals (educational meaning)** | Treat Mission Completion / Failure as Behaviour and planning evidence candidates — never as Knowledge/Memory grants |
| **Cold-start honest execution** | When Decision prefers evidence-creating actions under low warrant, compose diagnostic / first-coverage shaped missions without Mid readiness theatre |

## 2.2 Position in the intelligence stack

```
CurriculumContext + Goals + Constraints
        +
Digital Twin domains
        +
ReadinessState
        ↓
Decision Engine                 (read-side next-action selection)
        ↓
Decision (selected action + candidates + reason codes + lineage + warrant posture)
        ↓
Explainable Recommendation Engine   (optional sibling packaging / projection)
        ↓
Mission Intelligence            (execution-layer operationalisation)
        ↓
Mission / MissionTask artefacts
        ↓
Mission Completion / Failure → Learning Evidence → Behaviour (via Update Pipeline)
```

Write path (Evidence → Strategies → Twin) and read/execution path (Twin → Readiness → Decision → Recommendation / Mission) must not be conflated. Mission Intelligence sits on the **execution / projection** side; it does not select and does not write Twin beliefs. Student mission outcomes become evidence later via recording paths.

---

# 3. Non-Responsibilities

| Non-responsibility | Why |
|---|---|
| **Next-action selection** | Decision Engine alone selects; Mission must not invent a competing rank, score, topic priority list, or “better task than Decision said” |
| **Readiness Aggregation / recomputation** | Preparedness judgement remains Capability 2.7; Mission may cite readiness only when Decision lineage does |
| **Twin domain mutation** | Only Update Strategies via the Twin Update Pipeline may evolve Knowledge, Memory, Behaviour, Performance (and future Confidence) |
| **Learning Evidence authorship (as belief authority)** | Evidence is append-only history; Mission does not rewrite the past. Completion/failure may *become* evidence via product recording — Mission Intelligence does not own Evidence Model |
| **Inventing Curriculum weights / order / topics** | Curriculum Engine / canonical helpers remain syllabus truth; execution consumes Decision / Curriculum lineage |
| **Recommendation packaging ownership** | Titles, explanation-chain presentation, Recommendation Confidence narration remain Capability 2.9; Mission may surface recommended language but does not own packaging |
| **Authoring Decision reason codes** | Reason-code vocabulary and authorship remain Decision Engine ownership; Mission preserves and cites, does not redefine |
| **Scheduling optimisation solvers** | Forbidden in this analysis charter; packing formulas and optimisers are deferred and must never become a secret Decision Engine |
| **WeekPlan regeneration policy** | Multi-week planning artefacts remain planning ownership; Mission Intelligence projects Decisions into daily missions without owning plan strategy |
| **LLM ownership of composition or selection** | Generative assistance may narrate chain-supported attributions; it must not invent tasks, evidence, topics, or a competing Decision |
| **Coercing unknown readiness into Mid/High** | Binding Educational Reasoning conditions — execution must inherit honesty |
| **Treating Mission Completion as mastery or exam readiness** | Completion is Behaviour / planning evidence; Knowledge/Memory/Performance change only via appropriate learning evidence |
| **Parallel learner-state stores** | Twin remains educational-state authority; Mission rows must never store private mastery, readiness, or competing priority scores as truth |
| **Filler generation as educational authority** | Empty capacity does not authorize inventing low-value tasks that Decision did not author |

**Hard rule:** If a design needs “mission ranked topics independently,” “mission wrote mastery,” “readiness scheduled the day,” “empty slot invented educational need,” or “completion proves readiness,” that design is wrong.

---

# 4. Inputs

Mission Intelligence **consumes** Decision authority and supporting execution context. It **never modifies** Twin domains, readiness beliefs, or Decision selection. Consumption is observational for educational authority: same Decision batch + same execution context in → same attributable Mission projection out.

## 4.1 Primary input: Decision

| Decision element | Educational role for Mission Intelligence |
|---|---|
| **Selected action** | The educational action(s) to operationalise — action type + curriculum scope when present |
| **Candidate set** | Supports “why this task, not that?” attribution; Mission must not promote rejected candidates as equal authority |
| **Reason codes** | Stable factors MissionTasks must preserve for explainability |
| **Value rationale hooks** | Educational “why now” substance carried into task attribution — not marketing slogans |
| **Lineage / warrant posture** | Twin / Curriculum / Evidence / Readiness hooks and cold-start honesty that must survive composition |
| **Constraint acknowledgements** | Feasibility / intensity demotion already decided upstream — Mission must not erase or over-claim |

**Binding:** Mission operationalises the Decision’s selected action(s). It does not re-select among candidates.

## 4.2 Supporting input: Recommendation (optional)

| Input | Educational role |
|---|---|
| **Recommendation packaging** | Optional sibling projection that may supply student-facing language already narrated from Decision |
| **Recommendation Reasons / warrant posture** | May be surfaced on MissionTasks when present — never as a competing selection authority |

**Binding:** Recommendation is not required for Mission validity. Mission may project Decision(s) directly. When Recommendation language is used, it must remain Decision-faithful. Recommendation Priority must never become a private mission ranking engine.

## 4.3 CurriculumContext

| Input | Educational role |
|---|---|
| **Official syllabus identities, order, weights** | Confirm task scopes remain canonical; support V1/V2 fidelity via Decision / Curriculum lineage |

**Binding:** CurriculumContext is built via canonical Curriculum helpers outside Mission ownership. Mission Intelligence must not invent parallel weights, order, or topic trees.

## 4.4 Goals

| Input | Educational role |
|---|---|
| **Active paper / sitting** | Scopes what “toward the Goal” means for mission framing |
| **Deadline / calendar pressure (as Goal context)** | Informs how aggressive composition may be *within Decision authorisation* — does not invent new actions |
| **Committed capacity (e.g. weekly hours)** | Bounds how much work a day/session may carry |

**Binding:** Goals bound destination and capacity. Goals alone never invent Twin beliefs or substitute for Decision selection.

## 4.5 Constraints

| Input | Educational role |
|---|---|
| **Available time now / session length** | Bounds how many authorised tasks fit in this execution window |
| **Sustainable intensity / Behaviour burnout flags** | Demote load volume or intensity when sustainability risk is present |
| **Other operational limits** | Protect feasible execution without erasing educational need already selected by Decision |

**Binding:** Constraints shape ambition of composition. Constraints do not invent educational need and do not delete high-weight Decision authority by silent substitution.

## 4.6 Student execution context

Student execution context informs **how Decisions are fitted into now**, not a second selection authority.

| Context | Educational use by Mission Intelligence |
|---|---|
| **Current session window** | Defines the temporal container for today’s / this session’s Mission |
| **Already-committed work** | Avoid double-booking capacity beyond Goals / Constraints honesty |
| **Behaviour feasibility signals (as Decision-cited or constraint-bound)** | Support sustainable load; do not treat streaks as permission to invent harder content |
| **Decision Journal history (when available)** | Avoid thrashing composition that ignores recent dismiss without treating dismiss as mastery |
| **Prior Mission Completion / Failure patterns (as Behaviour evidence context)** | Inform feasibility honesty; never treat adherence as exam readiness or mastery |
| **Self-report Confidence (when present)** | May appear only as risk-framing if Decision already framed it that way — never as mastery or readiness upgrade for scheduling |

**Binding:** Execution context does not authorize Mission Intelligence to change selected educational actions, invent topics, average legacy readiness % into hybrid truth, or fill empty slots with unauthorised educational claims.

## 4.7 Input principles (binding)

1. **Decision is the sole selection authority input** — Mission never re-ranks.  
2. **Recommendation is optional packaging, not authority** — Mission may use it for language; never for competing selection.  
3. **CurriculumContext is canonical** — V1/V2 via Decision / Curriculum lineage only.  
4. **Goals define destination and capacity** — not Twin beliefs.  
5. **Constraints bound ambition** — they do not invent need or erase high-weight Decision.  
6. **Student execution context shapes fit, not authority** — time and sustainability inform composition volume.  
7. **Evidence Warrant is non-optional honesty** — cold start and low warrant survive into mission posture.  
8. **No legacy hybrid truth** — do not average TopicProgress / readiness % with Twin/Decision factors as temporary mission authority.  
9. **No filler authority** — empty capacity is not permission to invent educational tasks Decision did not author.

## 4.8 What is not an input authority

- UI streak counters as educational value justification  
- Mission Completion counts as mastery proof or readiness proof  
- Opaque “fill the day” product defaults without Decision  
- Coach/LLM free-text topic invention  
- Legacy mission heuristics / private priority scores as Twin-first authority  
- Legacy `ReadinessService` overall % as Decision substitute  
- Recommendation packaging scores as a secret second Decision Engine  

---

# 5. Outputs

## 5.1 Output principle

**Mission Intelligence outputs a Mission only.**

It does not output Decisions, readiness judgements, Twin updates, Recommendation packaging ownership, or WeekPlan regeneration policy. Downstream product surfaces may present the Mission; completion/failure recording may create Learning Evidence later.

## 5.2 Mission contents (educational meaning — not a schema)

| Mission element | Educational meaning |
|---|---|
| **Mission container** | Session/day executable unit for the student |
| **MissionTask set** | Ordered or prioritised executable tasks projected from Decision(s) |
| **Task action family** | Study / revise / assess / diagnostic / rest-protect — preserved from Decision, not collapsed |
| **Curriculum scope** | Canonical identity when Decision was curriculum-scoped |
| **Attribution / reason citations** | Decision reason codes + lineage hooks preserved on tasks |
| **Warrant / cold-start posture** | Honest evidence-density posture inherited from Decision |
| **Feasibility acknowledgements** | How Goals/Constraints/execution context shaped load volume |
| **Regeneration identity** | Enough Decision / Twin snapshot reference that recomposition can replace stale missions |

## 5.3 Explicit non-outputs

| Not an output of Mission Intelligence | Owner |
|---|---|
| Selected next action / re-ranked candidate list | Decision Engine |
| Recommendation title / explanation packaging ownership | Explainable Recommendation Engine (2.9) |
| Overall readiness / factor recomputation | Readiness Aggregation |
| Twin belief updates | Update Strategies via Twin Update Pipeline |
| WeekPlan regeneration policy | Planning services / planning ownership |
| New Decision reason codes that Decision did not emit | Decision Engine |
| Mastery grants on Mission Completion | Forbidden — Learning Evidence of learning only |
| Private mastery / readiness / priority scores stored as educational truth in mission rows | Forbidden — projections only |

## 5.4 Output contract (binding)

1. Every MissionTask must be attributable to a Decision (selected action + reason codes + lineage).  
2. Every Mission that touches readiness language must preserve warrant honesty.  
3. Every curriculum-scoped MissionTask must use canonical identities.  
4. Completing a Mission does not grant mastery; completion / assessment evidence does.  
5. No opaque “do these tasks” without Decision attribution in the core educational path.  
6. No private ranking score as educational authority inside the Mission artefact.  
7. No Decisions invented inside Mission Intelligence — **Mission only; no decisions.**

---

# 6. Relationship with Decision

## 6.1 Separation of concerns

| Concern | Owner |
|---|---|
| Highest-value next action + reason codes + candidates + lineage + warrant inheritance in selection | **Decision Engine (2.8)** |
| Session/day operationalisation of authorised Decision(s) into Mission / MissionTask structure | **Mission Intelligence (2.10)** |

## 6.2 Dependency direction

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

## 6.3 Binding rules

1. Decision Engine remains **selection authority**.  
2. Mission Intelligence **must not invent ranking** that disagrees with Decision reason codes.  
3. Mission Intelligence **may compose** authorised Decision(s) into a feasible session/day set; it may not invent evidence, syllabus topics, Twin beliefs, or substitute rejected candidates as equal authority.  
4. Multi-action session batches remain **Decision-authored** (or Decision-batched); Mission shapes fit, not educational priority.  
5. Accept/dismiss and Mission Completion are preference / Behaviour evidence — never mastery.  
6. Execution must not introduce scheduling optimisation formulas that effectively re-select educational value “for packing convenience.”  
7. Legacy mission ancestors must converge toward Decision-first authority — additive migration, no permanent parallel selection truth, no hybrid average as temporary truth.

## 6.4 What Mission never does in this relationship

- Re-select among Decision candidates  
- Drop or rewrite reason codes to soften educational tension  
- Present supportive Knowledge Strength as exam readiness when Decision did not claim readiness  
- Bypass Decision by writing missions from undocumented private ranks  
- Claim calibrated Confidence while Confidence domain ownership remains incomplete  
- Treat Mission Completion as proof the Decision “worked” for learning  

## 6.5 Educational consequence

If Decision and Mission disagree about what the student should learn next, **Decision is correct and Mission composition is wrong**. Product trust depends on that firewall.

---

# 7. Relationship with Recommendation

## 7.1 Separation of concerns

| Concern | Owner |
|---|---|
| Attributable next-action suggestion packaging | **Recommendation Engine (2.9)** |
| Session/day task-set operationalisation | **Mission Intelligence (2.10)** |

Recommendation packaging and Mission composition are **sibling projections**, not the same capability.

## 7.2 Dependency chain

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
- become the Recommendation Engine.

## 7.3 Educational rules

1. **Keep 2.9 and 2.10 separate** — packaging a Decision is not composing today’s mission.  
2. Missions remain **consequences** of intelligence, not the learner model.  
3. Mission rows must **never** store private mastery, readiness, or competing recommendation ranks.  
4. Mission Completion ≠ mastery; Mission Completion ≠ exam readiness; Mission Completion ≠ proof the Recommendation “worked” for learning.  
5. A Mission may include a recommended action; it must not become a second Decision Engine or a second Recommendation Engine.  
6. If Recommendation copy and Mission task attribution disagree with Decision reason codes, **Decision wins**; packaging/composition must be corrected.

## 7.4 Firewall

Recommendation outputs Recommendations. Mission Intelligence outputs Missions. Neither mutates Twin beliefs. Neither invents syllabus. Neither treats recommendation or mission rows as educational-state authority. Neither selects next actions.

---

# 8. Relationship with Planning

## 8.1 Separation of concerns

| Concern | Owner |
|---|---|
| Multi-day / multi-week plan structure and regeneration policy (WeekPlan and related planning artefacts) | **Planning ownership** |
| Daily / session Mission operationalisation of Decision(s) | **Mission Intelligence (2.10)** |

Educational Intelligence Architecture treats Planning artefacts (WeekPlan, Mission) as *consequences* of intelligence — not as Twin domains or learner-model authority. This analysis sharpens the Mission side: Mission Intelligence executes Decisions into daily structure; it does not own WeekPlan strategy.

## 8.2 Educational dependency shape

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

## 8.3 Binding rules

1. **Plans and missions are consequences of intelligence, not the learner model.**  
2. WeekPlan regeneration must not silently become a second Decision Engine via private topic ranks.  
3. Mission Intelligence must not absorb WeekPlan policy and invent multi-week educational strategy under a “mission” label.  
4. Planning may consume Decisions / Missions as consequences; it must not store private mastery inside plan or mission rows.  
5. Capacity honesty flows Goals → Constraints → Decision acknowledgements → Mission load shaping → Planning capacity views — without hybrid legacy % truth.  
6. When Twin state changes, missions remain regenerable projections; planning must prefer recomposition over stale private mission-as-mastery stores.

## 8.4 Why Mission ≠ Planning ownership collapse

- Planning answers longer-horizon structure and capacity.  
- Mission answers executable now.  
- Collapsing them reintroduces activity theatre (“fill the week with tasks”) and dual authority.  
- Explainability requires Decision reason codes between preparedness context and daily tasks; planning must not skip Decision.

---

# 9. Educational execution principles

These principles bind how Missions operationalise Decisions — educational fidelity over engagement theatre and schedule aesthetics.

1. **Execution, not selection** — Mission Intelligence operationalises; Decision Engine decides.  
2. **Decision-first always** — no readiness-first scheduling, no streak-first scheduling, no empty-slot invention of educational need.  
3. **Learning value over activity theatre** — prefer authorised learning-value tasks; do not invent filler to make the day look complete.  
4. **Preserve action families** — revise ≠ study ≠ assess ≠ diagnostic ≠ rest-protect in MissionTasks as in Decision.  
5. **Preserve educational tension** — when Decision preserves Knowledge vs Memory (or Behaviour vs Performance) tension, mission composition must not collapse it into bland generic tasks.  
6. **Feasibility is educational** — demoting volume for sustainability is legitimate execution; denial of feasibility is fidelity failure; erasing high-weight need under “too busy” theatre is also fidelity failure.  
7. **Attribution is mandatory** — every core educational MissionTask answers Why? via Decision reason codes + lineage.  
8. **Warrant honesty survives composition** — cold-start / low-warrant Decisions become diagnostic-shaped missions, not Mid-ready polish packs.  
9. **Mission Completion is Behaviour signal, not competence** — language and downstream use must not imply mastery change from ticks alone.  
10. **Curriculum-first identities** — name official syllabus identities; never invent “Module X*” labels.  
11. **No engagement-theatre urgency packing** — urgency/order reflects Decision-derived educational need and constraints, not notification dark patterns.  
12. **Coach may help phrase; coach may not decide or invent tasks** — generative assistance is narration only.  
13. **Regenerate rather than ossify** — stale missions are replaced from fresh Decisions; they are not a Twin fork.  
14. **Empty capacity is not educational authority** — leftover time does not invent unauthorised high-value claims.  
15. **Comparable attribution beats opaque scores** — prefer Decision reason codes over a single composite “mission match %.”  

---

# 10. Cold-start execution

## 10.1 Educational situation

Goals may be set while Twin domains are thin, Readiness overall is `not_yet_knowable` / low Evidence Warrant, and Decision prefers **evidence-creating** actions (diagnostics, early assessments, structured first coverage of high-weight areas).

## 10.2 Execution posture (binding)

| Do | Do not |
|---|---|
| Compose MissionTasks that operationalise diagnostic / evidence-creating Decisions | Invent polish, advanced rehearsal, or “you’re nearly ready” task packs |
| Preserve low warrant / `not_yet_knowable` honesty in mission attribution | Claim Mid or High readiness to “motivate” a fuller day |
| Prefer a small honest diagnostic-shaped mission over a busy false-personalised mission | Fill empty slots with unauthored topics to look adaptive |
| Keep Mission Completion expectations proportionate to thin history | Shame the student for lacking history via overloaded missions |
| Regenerate as warrant grows and Decisions change | Ossify cold-start filler as if it were a mastery map |
| Keep curriculum weight honesty when Decision scopes high-weight first coverage | Invent a fake personalised priority tree inside mission rows |

## 10.3 Cold-start execution principles

1. **Unknown is a first-class execution state** — not an error to hide with busywork.  
2. **Diagnostics are high-value missions** — evidence-creating tasks are not “filler until real missions arrive.”  
3. **Warrant inheritance is mandatory** — Decision’s cold-start honesty must survive composition.  
4. **No coercion** — never rewrite `not_yet_knowable` into Mid preparedness mission narratives.  
5. **No legacy percentage theatre** — do not fill empty Twin warrant with TopicProgress composites as if Twin-first truth.  
6. **No second reasoner under cold start** — thin evidence is not permission for Mission Intelligence to invent ranking.

## 10.4 Relationship to Decision and Recommendation cold-start postures

Decision selects evidence-creating actions under low warrant. Recommendation’s job is to say so clearly. Mission Intelligence’s job is to **compose executable structure that still says so**. Composition that hides diagnostic intent, over-packs the day, or over-promises preparedness fails educational fidelity even if the underlying Decision was correct.

---

# 11. Risks

| Risk | Educational / architectural impact | Mitigation |
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

---

# 12. Future Extensibility

The architecture must allow richer execution **without changing ownership boundaries**.

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

## 12.1 Compatibility guarantees to preserve

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

## 12.2 Deliberately unlocked

Not locked by this analysis beyond ownership:

- Exact Mission / MissionTask artefact schema  
- Exact regeneration timing / triggers  
- Exact UI for mission boards  
- Exact coexistence mechanics with legacy mission services  
- Numeric packing / scheduling formulas (if ever approved later, still subordinate to Decision)  
- WeekPlan regeneration algorithms (planning ownership)  
- Numeric Decision enrichment (remains Decision-owned if ever approved)  

---

# 13. Educational Fidelity Review

Educational fidelity: prefer honest learning-state representation and learning-value execution over engagement theatre and schedule aesthetics.

## 13.1 Confirmations (binding)

| Commitment | Status |
|---|---|
| **Mission Intelligence is an execution layer** | Confirmed — operationalises Decisions; does not decide |
| **Mission never invents ranking / selection** | Confirmed — no competing priority authority |
| **Mission never updates Twin domains** | Confirmed — write/read firewall |
| **Mission never invents Twin beliefs or syllabus** | Confirmed — cites Decision lineage / Curriculum identities only |
| **Mission never coerces unknown readiness** | Confirmed — inherits warrant; cold-start honesty mandatory |
| **Mission always remains attributable** | Confirmed — Decision reason codes + lineage on MissionTasks |
| **Mission Completion ≠ mastery / exam readiness** | Confirmed — Behaviour / planning evidence path only |
| **Mission prefers fidelity over activity theatre** | Confirmed — no Mid/High fabrication, no filler-as-intelligence, no streak-as-readiness packing |

## 13.2 Fidelity commitments in product language and composition

1. Do not pack polish because streaks look good while mocks are missing.  
2. Do not narrate self-report Confidence as permission to schedule foundations-skipping work.  
3. Do not treat accept, dismiss, or Mission Completion as proof learning occurred.  
4. Do not hide High Knowledge + Low Memory tension behind a generic “study block” pack.  
5. Do not invent “study anything” filler when Decision identified high-weight risks — or when Decision identified diagnostics.  
6. Do not let coach/LLM invent “do Topic Z” without Decision + Curriculum support.  
7. Do not strip diagnostic intent under cold start to sound more “personalised” or fill the day.  
8. Do not average legacy readiness percentages into Twin-first mission stories.  
9. Do not present rest/protect as failure, or as avoidance when Decision selected it for sustainability.  
10. Do not use leftover capacity as permission to invent unauthorised educational claims.

## 13.3 Anti-fidelity patterns to reject

| Pattern | Why it fails fidelity |
|---|---|
| Mission re-ranks Decision candidates by engagement or packing heuristics | Secret second Decision Engine |
| Readiness % directly schedules the day | Missing Decision authority and explainability |
| Cold-start Mid readiness used to sell advanced rehearsal packs | Fabricates preparedness |
| Empty-slot filler topics invented to complete a “full mission” | Activity theatre; invented educational need |
| Confidence slider upgrades mission aggressiveness as if mastery | Confidence contamination |
| Mission task attribution that disagrees with Decision reason codes | Broken explainability |
| Mission Completion writes Knowledge/Memory directly | Evidence/Twin bypass |
| Mission rows store private “priority scores” as mastery | Parallel authority |
| Legacy hybrid % + Twin factors as temporary mission truth | Dual authority; untrustable |
| LLM invents evidence ids or topics for nicer mission stories | Audit fraud |
| Unsustainable cram missions that Behaviour says will fail | Feasibility denial |
| “Rest never allowed” despite burnout flags | Collapses learning sustainability |
| “Rest always preferred” despite high-weight exam risk Decision | Avoidance theatre; erases educational need |

## 13.4 Upstream conditions acknowledged

This analysis accepts and encodes Educational Reasoning / Decision / Recommendation conditions relevant to 2.10:

1. Decision Engine remains selection authority.  
2. Recommendation remains a projection of Decision; Mission remains a separate projection / execution layer.  
3. Explainability chain preserved end-to-end into MissionTask attribution.  
4. No legacy hybrid truth.  
5. Write/read firewall.  
6. Warrant and cold-start honesty.  
7. Confidence separability.  
8. Curriculum V1/V2 invariants; CurriculumContext via canonical helpers before production consumers.  
9. Accept/dismiss and Mission Completion are preference / Behaviour evidence, not mastery.  
10. No scheduling optimisation / selection math inside this educational analysis charter.  
11. Missions are consequences of intelligence, not the learner model.  
12. Mission Generation depends on Decision Engine rather than on Readiness directly.

Also retains Twin / Midpoint conditions still in force: Twin sole educational-state authority, no parallel learner-state forks, deterministic cores free of LLM ownership of selection.

---

# 14. Mission ownership principles

These principles bind Capability 2.10 educational design and all downstream consumers.

1. **Mission Intelligence is an execution layer; it operationalises Decisions; it does not decide.**  
2. **Decision Engine alone selects the highest-value next learning action (or Decision batch).**  
3. **Recommendation Engine packages Decisions; it never invents ranking and never composes missions.**  
4. **Readiness judges preparedness; it never selects actions and never becomes mission scheduling authority.**  
5. **Plans and missions are consequences of intelligence, not the learner model.**  
6. **Every Mission is a projection — authority flows Decision → Mission, never the reverse.**  
7. **Every core educational MissionTask must be attributable via Decision reason codes + lineage.**  
8. **Mission may surface Recommendation language; it must not treat Recommendation as selection authority.**  
9. **Evidence Warrant and cold-start honesty must survive mission composition.**  
10. **Mission Completion / Failure is Behaviour and planning evidence — never mastery, never exam readiness.**  
11. **Constraints and Goals shape feasible load; they do not invent educational need or silently erase Decision authority.**  
12. **Empty capacity is not educational authority to invent tasks.**  
13. **Curriculum is the only syllabus authority; MissionTasks use canonical identities only.**  
14. **Twin is the only educational-state authority; Mission consumes lineage, never forks beliefs.**  
15. **Learning Evidence is the only legitimate belief-changing input; mission outcomes enter via evidence recording, not silent Twin writes.**  
16. **No legacy hybrid truth — Decision-first execution, not averaged TopicProgress theatre.**  
17. **Core mission attribution is deterministic and free of black-box LLM ownership of selection or invented tasks.**  
18. **V1 and V2 curricula remain first-class through canonical traversal and identities.**  
19. **Mission depends on Decision, not on raw readiness scores.**  
20. **Educational fidelity over engagement theatre and schedule aesthetics — always.**  

---

# 15. Recommendations

## 15.1 Architecture milestone that should follow

**Next milestone:** Capability 2.10 Mission Intelligence **architecture note** (short, binding) — then structural execution contracts — then implementation in a later milestone.

The architecture note should lock, without algorithms or scheduling optimisation:

1. Mission output contract (Mission container, MissionTasks, attribution, warrant posture, feasibility acknowledgements, regeneration hooks)  
2. Input contract: Decision / Decision batch (selected action, candidates, reason codes, lineage, warrant) + Goals + Constraints + CurriculumContext + student execution context; Recommendation optional for language only  
3. Firewall vs Decision (execution only; no re-selection; no private ranking; **Mission only — no decisions**)  
4. Firewall vs Recommendation (sibling projection; no packaging ownership collapse; no Priority-as-ranker)  
5. Firewall vs Readiness (cite only when Decision lineage cites; no recomputation; no Mid/High coercion; no readiness→mission shortcut)  
6. Firewall vs Planning (Mission ≠ WeekPlan policy ownership; plans/missions remain consequences)  
7. Cold-start / low-warrant execution posture  
8. Mission Completion / Failure → Learning Evidence / Behaviour path (not mastery)  
9. Relationship to legacy mission / plan generators (convergence path; freeze heuristic deepening; no hybrid temporary truth)  
10. Explicit non-goals: no Twin writes, no readiness recomputation, no Decision selection, no Recommendation packaging ownership, no scheduling optimisation solvers, no scoring formulas in the first structural pass  

## 15.2 Educational design recommendations

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

## 15.3 Architecture compliance checklist

| Invariant | Status for Mission Intelligence analysis |
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

This milestone delivers **analysis only**.

**Do not proceed in this milestone to:** code, algorithms, scheduling optimisation, scoring, dataclasses, services, tests, database changes, Decision/Recommendation redesign, or UI.

**Next engineering step (separate milestone):** Capability 2.10 Mission Intelligence architecture note → structural execution contracts → implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Mission Intelligence in the capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot lineage may be cited; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains Decision consumed; Mission operationalises without modification; Completion/Failure may feed Behaviour via evidence |
| 2.7 | Readiness Aggregation | May appear in attribution when Decision cites readiness; never schedules missions directly |
| 2.8 | Decision Engine | Supplies Decision authority that Mission operationalises |
| 2.9 | Explainable Recommendation Engine | Sibling packaging projection; optional language source; not selection |
| **2.10** | **Mission Generation Intelligence** | **This analysis precedes architecture and implementation** |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.10.1 — Mission Intelligence Educational Analysis |
| Nature | Architecture / educational analysis only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required going forward; analysis introduces no traversal changes |
| Application code intentionally untouched | Yes |
| Upstream stack | Curriculum Intelligence, Twin, Readiness, Decision Engine, Recommendation Engine — approved |
| Governing principle | Mission Intelligence is an execution layer; it operationalises Decisions; it does not decide |

---

*End of Capability 2.10.1 Mission Intelligence Educational Analysis. STOP.*
