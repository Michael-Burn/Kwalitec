# Capability 2.8.1 — Decision Engine Educational Analysis

**Status:** Educational / architecture analysis — analysis only  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.8 Decision Engine (educational analysis preceding architecture and implementation)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream gate:** Readiness Architecture Review — APPROVED WITH CONDITIONS ([`docs/reviews/READINESS_ARCHITECTURE_REVIEW.md`](../reviews/READINESS_ARCHITECTURE_REVIEW.md))  
**Companions:** [`CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md), [`CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md`](CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md)  
**Scope:** Decision Engine definition, educational ownership, input/output boundaries, relationships, explainability, scenarios, risks, and fidelity — **no implementation, algorithms, scoring, optimization, services, tests, schema, or migrations**

---

## Document purpose

This milestone answers what the **Decision Engine** is as Epic 2’s next-action reasoner: the educational capability that selects the **highest-value next learning action** from Twin-backed educational state, without owning preparedness judgement, product packaging, or mission composition.

Student Digital Twin, Twin Update Pipeline, Knowledge, Memory, Behaviour, Performance, and Readiness Aggregation are complete (or structurally approved). Decision Engine is the next capability. It prepares Capability 2.8 architecture the same way Readiness educational analysis prepared 2.7: **educational clarity first**, structural contracts later, numeric selection deferred.

**Non-goals of this document**

- Code, pseudocode algorithms, dataclasses, or service refactors  
- Database schemas, Alembic migrations, or ORM layouts  
- Scoring functions, ranking formulas, optimization objectives, or Bayesian selection math  
- UI redesign, gamification, dashboards, notifications, or social features  
- Explainable Recommendation Engine or Mission Generation Intelligence design beyond relationship boundaries  
- Replacement of Curriculum Engine, Evidence Model, Twin aggregate, or Readiness Aggregation contracts  

---

# 1. Definition of Decision Engine

## 1.1 Canonical question

> **What is the highest-value thing this student should do next?**

Not: how prepared they are for the sitting (Readiness).  
Not: what they know *now* (Knowledge).  
Not: whether they will still know it (Memory).  
Not: how they study (Behaviour).  
Not: how they perform when assessed (Performance).  
Not: how certain they *feel* (Confidence).  
Not: how the suggestion is titled or presented (Recommendation Engine).  
Not: how today’s tasks are packaged into a mission (Mission Intelligence).

Readiness answers: *Are we on track for the sitting?*  
Decision Engine answers: *What should we do next?*

## 1.2 Educational meaning

**“Highest-value”** means the action with the greatest expected educational contribution toward the active Goal (typically: pass the sitting), given Twin educational state, official syllabus weight and order, readiness context, and feasible constraints (available time, sustainable intensity, behavioural realism).

The Decision Engine is:

- **read-side only** — it reasons over Twin + Curriculum + Goals + ReadinessState; it does not mutate Knowledge, Memory, Behaviour, or Performance;  
- **action-selecting** — it chooses a next learning action (and may surface candidates considered);  
- **curriculum-bound** — actions reference official syllabus identities, never invented topics;  
- **evidence-honest** — cold start and low warrant favour diagnostics / evidence-creating actions, never fabricated certainty;  
- **deterministic in the core path** — same inputs → same decision (no random theatre; no required LLM ownership);  
- **explainable by construction** — every selection carries reason codes and lineage hooks for the explainability chain.

It is **not**:

- a preparedness score or readiness aggregator;  
- a write-side Twin domain Update Strategy;  
- a product packaging layer (titles, urgency copy, UI);  
- a mission / week-plan generator;  
- a motivation or engagement optimizer;  
- a black-box coach that invents syllabus or evidence.

## 1.3 Distinctions (binding vocabulary)

| Concept | Educational question | Relation to Decision Engine |
|---|---|---|
| **Decision Engine** | What is the highest-value next learning action? | Owns selection of the next action and decision rationale inputs |
| **Readiness** | Are we on track for the sitting? | Supplies factorable preparedness context; never selects actions |
| **Recommendation** | How is the selected action presented as an attributable suggestion? | Product projection of a Decision; owned by Capability 2.9 |
| **Mission** | What is today’s (or this session’s) task set? | Projection of one or more Decisions; owned by Capability 2.10 |
| **Decision State** | What was decided, among which candidates, with which reasons? | Materialised decision context / audit artefact produced from Decision Engine outcomes (and later accept/dismiss lineage) |
| **Decision Journal** | Did the student accept, dismiss, or defer? | Outcome history; becomes Learning Evidence; does not itself select the next action |

Governing principle (Educational Intelligence Architecture §13):

> **Readiness is derived and factorable; Decision Engine selects next action.**

Extended for this capability:

> **Decision is not Readiness; Decision is not Recommendation packaging; Decision is not Mission composition; Decision never invents syllabus or Twin beliefs; Decision never coerces unknown readiness into Mid or High preparedness.**

## 1.4 Product purpose

Decision Engine exists so Kwalitec can:

1. Answer Epic 2’s guiding question with an **authoritative next-action reasoner**.  
2. Prefer **learning-value actions** (Knowledge / Memory / Performance movement) over empty completion theatre.  
3. Respect **curriculum weight, retention risk, assessment weakness, and feasibility** as educational tensions — not as a single opaque score.  
4. Supply **reason codes and candidate context** so Recommendation and Mission layers remain explainable.  
5. Converge legacy recommendation ancestors toward Twin-first / Decision-first authority without inventing a parallel learner-state store.

## 1.5 Ubiquitous language anchors

| Term | Meaning |
|---|---|
| **Decision** | Selected next educational action plus attributable rationale (reason codes, candidates considered, value narrative hooks) |
| **Selected action** | Canonical next action (e.g. study topic X, revise topic Y, take diagnostic, rest / protect intensity) |
| **Candidate set** | Alternatives considered — required for “why this, not that?” explainability |
| **Reason codes** | Stable machine-readable factors justifying the selection |
| **Constraints** | Feasibility limits on ambition (available time, session length, Behaviour sustainability / burnout flags, capacity from Goals) |
| **CurriculumContext** | Syllabus order, identities, and exam weights obtained via canonical Curriculum helpers — never reinvented inside Decision Engine |
| **Decision ownership** | Only Decision Engine selects next actions; Readiness, Recommendation, and Mission layers must not silently assume that role |

---

# 2. Educational Responsibilities

## 2.1 Owns

| Responsibility | Educational meaning |
|---|---|
| **Next-action selection** | Choose the highest-value learning action *now* given Twin state, CurriculumContext, Goals, Constraints, and ReadinessState context |
| **Educational value framing** | Reason about expected contribution toward the Goal — coverage vs revision vs assessment vs rest — without collapsing into activity theatre |
| **Candidate consideration** | Hold a candidate set so alternatives remain auditable and explainable |
| **Reason-code authorship** | Emit stable educational reason codes that Recommendation packaging may narrate but must not invent |
| **Constraint-respecting ambition** | Honour feasible intensity and capacity; demote unsustainable load when Behaviour / Goals signal risk |
| **Cold-start honesty in selection** | Prefer evidence-creating / diagnostic-shaped actions when warrant is low — without inventing Mid readiness |
| **Decision context for Decision State** | Produce the decision context that later materialises as Decision State / journal lineage (architecture will name artefacts; this analysis locks ownership of selection) |

## 2.2 Position in the intelligence stack

```
CurriculumContext + Goals + Constraints
        +
Digital Twin domains (Knowledge · Memory · Behaviour · Performance · …)
        +
ReadinessState          (preparedness context — factors, warrant, cold start)
        ↓
Decision Engine         (read-side next-action selection)
        ↓
Decision (selected action + candidates + reason codes)
        ↓
Explainable Recommendation / Mission projections (later capabilities)
```

Write path (Evidence → Strategies → Twin) and read path (Twin → Readiness → Decision → projections) must not be conflated. Decision Engine sits entirely on the **read** side for selection; outcomes of student response become evidence later.

---

# 3. Non-Responsibilities

| Non-responsibility | Why |
|---|---|
| **Learning Evidence authorship (as belief input)** | Evidence is append-only history; Decision Engine does not rewrite the past. Accept/dismiss may *become* evidence via product recording paths — Decision Engine does not own Evidence Model |
| **Twin domain mutation** | Only Update Strategies via the Twin Update Pipeline may evolve Knowledge, Memory, Behaviour, Performance (and future Confidence) |
| **Mastery / retention / behaviour / performance beliefs** | Those domains own their questions; Decision Engine consumes them |
| **Readiness Aggregation** | Preparedness judgement remains Capability 2.7; Decision Engine consumes `ReadinessState`, never recomputes a competing readiness truth |
| **Inventing Curriculum weights / order** | Curriculum Engine / `CurriculumService` helpers remain syllabus truth; Decision Engine consumes `CurriculumContext` |
| **Recommendation packaging** | Titles, presentation, urgency copy, and explanation narrative packaging belong to Capability 2.9 |
| **Mission / plan generation** | Daily task sets and WeekPlan regeneration belong to Mission Intelligence / planning consumers (Capability 2.10 and plan services) |
| **Accept / dismiss UI and journal UX** | Product surfaces record outcomes; Decision Engine supplies the decision being responded to |
| **Scoring formulas / optimization solvers** | Deferred; this milestone forbids locking selection math |
| **LLM ownership of selection** | Generative assistance may narrate chain-supported reasons; it must not own the selection function |
| **Parallel learner-state stores** | Twin remains educational-state authority; Decision Engine must not invent a private mastery map inside decisions or missions |
| **Coercing unknown readiness into preparedness** | Binding Readiness Architecture Review condition — unknown / low-warrant / `not_yet_knowable` must not become Mid or High |

**Hard rule:** If a design needs “readiness said do X,” “recommendation invented the ranking,” or “mission wrote mastery,” that design is wrong.

---

# 4. Inputs

Decision Engine **consumes** educational context. It **never modifies** Twin domains or readiness beliefs. Consumption is observational: same inputs in → same Decision out (deterministic core).

## 4.1 Input catalogue (educational contracts)

| Input | Educational role |
|---|---|
| **ReadinessState** | Factorable preparedness context: named factors, attributions, evidence warrant, cold-start / `not_yet_knowable` posture, factor disagreement. Informs urgency, risk concentration, and honesty — **not** action selection by itself |
| **CurriculumContext** | Official syllabus identities, canonical order, exam weights (V1/V2 via canonical helpers). Supplies educational value of topics/sections relative to the sitting |
| **Goals** | Active paper/sitting, ambition, deadline, committed capacity (e.g. weekly hours). Scopes what “value toward the Goal” means |
| **Constraints** | Session feasibility: available time now, sustainable intensity, Behaviour sustainability / burnout flags, other operational limits that demote ambition without erasing educational need |

## 4.2 Supporting Twin context (consumed, not owned)

Decision Engine also reads Twin educational state that readiness may already have summarised — still Twin authority, still read-only:

| Twin concern | How Decision Engine uses it educationally |
|---|---|
| **Knowledge** | Gaps / weak mastery on weighted identities → study / coverage-shaped candidates |
| **Memory** | Stale high-value retention → revise-shaped candidates |
| **Performance** | Assessment weakness / thin warrant → diagnostic or exam-condition rehearsal candidates |
| **Behaviour** | Consistency and sustainability → feasibility constraints and intensity demotion |
| **Confidence (when available)** | Over/under-confidence vs Performance → risk framing only; never upgrades mastery or readiness; Knowledge-held confidence lineage is not calibrated Confidence |
| **Decision history / Decision State** | Prior selections and accept/dismiss lineage → avoid thrashing; respect revealed preferences without treating dismiss as mastery |

## 4.3 Input principles (binding)

1. **ReadinessState is context only** — never an action selector, never a mission generator, never coerced from unknown to Mid/High.  
2. **CurriculumContext is built via canonical Curriculum helpers** — Decision Engine must not invent parallel weights or order.  
3. **Goals define the educational destination** — sitting and capacity bound value; Goals alone never invent Twin beliefs.  
4. **Constraints bound ambition** — feasibility protects learning sustainability; constraints do not invent educational need.  
5. **Evidence Warrant must flow end-to-end** — reason codes that cite readiness must inherit warrant honesty (e.g. prefer diagnostics when warrant is low).  
6. **No legacy TopicProgress hybrid truth** — do not average legacy readiness percentages with Twin factors as temporary authority.  
7. **Sparse Twin → honest selection posture** — prefer evidence-creating actions; do not invent High-value polish narratives on empty beliefs.

## 4.4 What is not an input authority

- UI streak counters as educational value  
- Mission completion counts as mastery proof  
- Self-report Confidence as Assessment Performance  
- Coach/LLM free-text topic invention  
- Legacy `ReadinessService` overall % as Twin-first authority  

---

# 5. Outputs

## 5.1 Output principle

**The Decision Engine outputs a Decision only.**

It does not output readiness judgements, packaged recommendations, or mission artefacts. Downstream capabilities project the Decision into product surfaces.

## 5.2 Decision contents (educational meaning — not a schema)

| Decision element | Educational meaning |
|---|---|
| **Selected action** | The canonical next learning action (study / revise / assess / diagnostic / rest-or-protect-intensity, scoped to curriculum identity when applicable) |
| **Candidate set** | Alternatives considered — enables “why not Y?” explainability |
| **Reason codes** | Stable factors (e.g. high exam weight, retention risk, assessment warrant gap, time pressure, feasibility demotion, cold-start diagnostic preference) |
| **Value rationale hooks** | Why this action maximises expected educational value *now* — attributable, not marketing copy |
| **Lineage references** | Hooks to Twin snapshot / domain factors / ReadinessState factors / Curriculum identities / evidence ids where available |
| **Constraint acknowledgements** | Which feasibility limits shaped or demoted the selection |

Optional later materialisation (architecture milestone): Decision State snapshot for audit — still a consequence of Decision output, not a second selection engine.

## 5.3 Explicit non-outputs

| Not an output of Decision Engine | Owner |
|---|---|
| Overall readiness / factor recomputation | Readiness Aggregation |
| Recommendation title, UI copy, packaged explanation narrative | Explainable Recommendation Engine (2.9) |
| Mission / MissionTask rows | Mission Generation Intelligence (2.10) |
| WeekPlan regeneration | Planning services (consumers of decisions / goals) |
| Twin belief updates | Update Strategies via Twin Update Pipeline |
| Accept/dismiss evidence records | Product recording → Learning Evidence / Decision Journal |

## 5.4 Output contract (binding)

1. Every Decision must be attributable via reason codes + lineage hooks.  
2. Every Decision that cites readiness must preserve warrant honesty.  
3. Every curriculum-scoped action must use canonical identities from CurriculumContext.  
4. Accepting a Decision (later) does not grant mastery; completion / assessment evidence does.  
5. No opaque “do this” without candidates/reasons in the core educational path.

---

# 6. Relationship with Readiness

## 6.1 Educational boundary

| Capability | Question | Ownership |
|---|---|---|
| **Readiness Aggregation** | Are we on track for the sitting? | Preparedness judgement |
| **Decision Engine** | What should we do next? | Next-action selection |

Same Twin snapshot; different questions; different owners.

## 6.2 How Decision Engine consumes ReadinessState

| Readiness signal | Educational use by Decision Engine |
|---|---|
| High time / goal pressure + weak Assessment Performance on high-weight areas | Prefer high-value remediation or exam-condition rehearsal candidates |
| High uncertainty / cold start / `not_yet_knowable` | Prefer diagnostic or evidence-creating actions; never invent Mid preparedness to justify polish |
| Strong Knowledge / Performance with weak Memory Stability | Prefer revision-shaped actions for high-weight stale topics |
| Strong Behaviour Reliability with thin Performance warrant | Prefer assessment-shaped actions within feasible intensity |
| Fragile Behaviour Reliability near the sitting | Constrain intensity / protect sustainability — without erasing Performance evidence |
| Factor disagreement | Preserve educational tension in reason codes (e.g. “knows now / may not retain”) — do not average away |

## 6.3 Firewall (binding from Readiness Architecture Review)

1. Decision Engine consumes `ReadinessState` as **context only**.  
2. Decision Engine never asks readiness to select actions or generate missions.  
3. Decision Engine never coerces unknown / low-warrant / `not_yet_knowable` into Mid or High preparedness.  
4. Decision Engine never product-narrates structural “supportive” Knowledge Strength as exam readiness.  
5. If a design needs “readiness said do X,” that design is wrong — Decision Engine owns selection; Readiness owns preparedness judgement only.

## 6.4 What Readiness does not decide

- Topic selection  
- Action type  
- Session composition  
- Accept/dismiss handling  
- Plan or mission regeneration  

**Readiness informs decisions; it never chooses actions.**

---

# 7. Relationship with Recommendation Engine

## 7.1 Separation of concerns

| Concern | Owner |
|---|---|
| Highest-value next action + reason codes + candidates | **Decision Engine (2.8)** |
| Product packaging of that Decision (title, explanation chain presentation, urgency presentation, actionable suggestion surface) | **Explainable Recommendation Engine (2.9)** |

A **Recommendation** is the product projection of a Decision Engine output: a concrete, attributable suggestion the student can accept, dismiss, or act on.

## 7.2 Dependency direction

```
Decision Engine
        ↓
Decision (selected action + reason codes + candidates + lineage)
        ↓
Explainable Recommendation Engine
        ↓
Recommendation (packaged suggestion)
        ↓
Decision Journal (accept / dismiss / defer) → Learning Evidence
```

## 7.3 Binding rules

1. Recommendation Engine **must not invent ranking** that disagrees with Decision reason codes.  
2. Recommendation Engine **may narrate** chain-supported reasons; it may not invent evidence, syllabus topics, or Twin beliefs.  
3. Recommendation Confidence (evidence-density appropriateness) is distinct from student self-report Confidence and from Mastery.  
4. Accepting a Recommendation does not grant mastery; it records preference / intent evidence only.  
5. Legacy `RecommendationService` ancestors must converge toward Decision-first authority — additive migration, no permanent parallel selection truth.

## 7.4 What Decision Engine never does in this relationship

- Own UI copy or coach phrasing  
- Own accept/dismiss journaling UX  
- Bypass Recommendation packaging by writing missions directly from undocumented private ranks  

---

# 8. Relationship with Mission Intelligence

## 8.1 Dependency chain

```
Twin + CurriculumContext + Goals + Constraints + ReadinessState
        ↓
Decision Engine                         (selected actions / reason codes)
        ↓
Mission Generation Intelligence (2.10)  (session/day task projection)
        ↓
Mission / MissionTask artefacts
```

## 8.2 Educational rule

**Mission Generation depends on the Decision Engine rather than on Readiness directly.**

Missions become adaptive when they:

1. Start from Decision Engine outputs (or a batch thereof for a session window);  
2. Respect Behaviour feasibility and Goals capacity;  
3. Prefer learning-value tasks over filler;  
4. Remain regenerable when Twin state changes;  
5. Never store a private mastery or readiness model inside mission rows.

## 8.3 Why not Readiness → Mission or Decision → mastery

- Readiness does not choose actions; missions need concrete actions.  
- Direct readiness→mission reintroduces activity theatre (“schedule filler to raise readiness”).  
- Explainability requires Decision reason codes between preparedness context and daily tasks.  
- Missions are **consequences** of intelligence, not the learner model.  
- Mission Completion ≠ mastery; Mission Completion ≠ exam readiness.

## 8.4 Firewall

Decision Engine outputs Decisions. Mission Intelligence projects Decisions. Neither mutates Twin beliefs. Neither invents syllabus. Neither treats mission rows as educational-state authority.

---

# 9. Explainability

## 9.1 Mandatory chain

Every educational next-action Decision must be able to answer **Why?** via:

```
Curriculum factor
    → Learning Evidence (or evidence aggregate)
        → Twin domain state factor(s)
            → Readiness factor (when relevant) + Evidence Warrant
                → Decision Engine reason code(s)
                    → Recommendation explanation (Capability 2.9 packaging)
```

Students must never be asked to trust a black box for core next-action advice.

## 9.2 Explanation layers (educational examples — not formulas)

| Layer | Example content |
|---|---|
| **Curriculum** | “This area carries substantial exam weight.” |
| **Evidence** | “Recent assessed attempts on Topic T were incorrect (evidence ids …).” |
| **Twin** | “Knowledge weak on T; Memory last reinforced long ago; Performance summaries concentrated weakness.” |
| **Readiness** | “Assessment Performance and Memory Stability elevate sitting risk on a high-weight slice; warrant remains limited.” |
| **Decision** | “Revise Topic T now: high weight × retention risk × feasible session length — preferred over new low-weight coverage.” |

## 9.3 Attribution requirements

1. Selected action cites reason codes tied to Twin / Readiness / Curriculum / Constraints inputs.  
2. Candidate set supports “why not the alternative?” without post-hoc invention.  
3. Warrant honesty appears whenever readiness or Twin evidence density is low.  
4. Explanations must not invent evidence, syllabus topics, or Twin beliefs.  
5. LLM / coach narration may only restate chain-supported attributions — never author the Decision.  
6. Post-hoc stories that disagree with Decision reason codes are forbidden.

## 9.4 Forbidden explanation patterns

- Single opaque “recommended for you” without factors  
- Explanations that cite UI labels but not Twin/evidence  
- LLM-generated rationales that invent evidence or topics  
- Narrating supportive Knowledge Strength as “you are exam ready”  
- Averaging away High Knowledge + Low Memory tension into a bland Mid story  
- Treating dismissals as proof the topic is mastered  

---

# 10. Educational Decision Scenarios

Educational interpretation only — no scoring, ranking math, or optimization.

## 10.1 High Knowledge + Low Memory

**Situation:** Mastery beliefs look strong on weighted topics; reinforcement is stale; sitting approaches; Readiness shows Knowledge Strength supportive while Memory Stability elevates risk.

**Decision posture:** Prefer **revision-shaped** actions on high-weight stale topics over new low-weight coverage. Reason codes should make the tension explicit: knows-now vs may-not-retain. Do not narrate “ready because mastery looks high.”

## 10.2 High Behaviour + Low Performance

**Situation:** Consistent study cadence; thin or weak assessed outcomes; Readiness keeps Behaviour Reliability distinct from Assessment Performance; warrant for exam preparedness is thin.

**Decision posture:** Prefer **assessment-shaped or diagnostic** actions within feasible intensity. Do not reward streaks with “you’re ready” polish work. Activity is not learning proof; Decision must create assessed evidence.

## 10.3 Low Knowledge + High Confidence

**Situation:** Sparse/weak mastery; student self-reports high Confidence (or Knowledge holds confidence-rating lineage); Readiness omits Confidence as preparedness upgrade.

**Decision posture:** Prefer **diagnostic / structured learning** on high-weight gaps. Treat overconfidence as **risk framing**, not as authority to skip foundations. Never let self-report upgrade selected action into “exam rehearsal only.”

## 10.4 High Performance + Weak Behaviour

**Situation:** Strong mocks where assessed; irregular adherence; capacity risk vs remaining calendar; Readiness preserves assessment signal while flagging pace/feasibility.

**Decision posture:** Protect **high-value remediation continuity** while **demoting intensity** to sustainable load. Do not erase mock evidence because missions were missed; do not ignore calendar risk because mocks were strong. Constraints shape ambition; they do not invent educational need.

## 10.5 Cold start / low warrant

**Situation:** Goals set; Twin domains thin; Readiness overall `not_yet_knowable` / low Evidence Warrant.

**Decision posture:** Prefer **evidence-creating** actions (diagnostics, early assessments, structured first coverage of high-weight areas). Never coerce unknown readiness into Mid to justify advanced polish. Honest reason codes: insufficient warrant to prioritise refinement.

## 10.6 Time scarcity near sitting

**Situation:** Short remaining calendar; CurriculumContext shows unequal weights; Readiness time pressure elevated; several gaps compete.

**Decision posture:** Prefer **curriculum-weighted** weak areas over low-weight perfectionism. Retention risk on high-weight topics can outrank new coverage of low-weight topics. Feasibility still applies — unsustainable cram plans fail educational fidelity.

## 10.7 Feasibility / burnout signal

**Situation:** Educational need is high (weak high-weight Performance/Memory), but Behaviour flags unsustainable intensity.

**Decision posture:** Select a **smaller or gentler** high-value action (or explicit protect-intensity / rest-shaped decision) rather than an ambitious plan the Twin says will fail. Learning over theatre includes not prescribing collapse.

---

# 11. Risks

| Risk | Educational / architectural impact | Mitigation |
|---|---|---|
| **Readiness → Decision conflation** | Wrong owner; readiness becomes a hidden action selector | Strict firewall; consume `ReadinessState` as context only |
| **Opaque Decision Engine** | Product thesis failure; untrustable next-action advice | Mandatory reason codes + candidate set + explainability chain |
| **Coercing unknown readiness** | False preparedness; dishonest diagnostics avoidance | Inherit warrant; prefer evidence-creating actions under cold start |
| **Activity theatre in selection** | Missions/completions preferred over Knowledge/Memory/Performance movement | Learning-over-activity principle; Behaviour is feasibility, not value |
| **Confidence contamination** | Self-report drives action as if mastery/assessment | Confidence risk-framing only; omit as readiness upgrade; no Knowledge-held confidence as calibrated Confidence |
| **Curriculum invention** | Parallel topic trees; V1/V2 breakage | `CurriculumContext` via canonical helpers only |
| **Legacy dual authority** | `RecommendationService` / TopicProgress ranks disagree with Twin-first Decision | Additive convergence; no hybrid average as temporary truth |
| **Recommendation invents ranking** | Packaging layer becomes secret Decision Engine | 2.9 packages only; must not contradict reason codes |
| **Mission rows as mastery** | Stale private state; broken audit | Missions are projections only |
| **LLM ownership creep** | Non-determinism; invented syllabus/evidence | Coach narrates; Decision Engine selects |
| **Premature scoring / optimization** | Unmaintainable math before educational contracts mature | Structural/educational analysis first; defer formulas |
| **Ignoring constraints** | Unsustainable plans; burnout; dismiss thrashing | Constraints demote intensity; record feasibility in reasons |
| **Ignoring constraints’ opposite** | Feasibility used to erase educational need | Constraints bound ambition; they do not delete high-weight risk |
| **Thrashing / preference blindness** | Re-recommend dismissed actions without lineage | Consume Decision history as context; dismiss ≠ mastery |
| **Parallel learner-state stores** | Divergent “next topic” truths | Twin + Decision as authority; services consume |

---

# 12. Future Extensibility

The architecture must allow richer selection **without changing ownership boundaries**.

| Future capability | How it extends without breaking architecture |
|---|---|
| **Numeric / structured selection functions** | Live inside Decision Engine ownership; remain deterministic and explainable; still consume Twin/Readiness/Curriculum/Goals/Constraints — never fork Twin beliefs |
| **Richer reason-code vocabulary** | Version codes additively; preserve audit of older Decisions |
| **Confidence calibration domain** | Supplies calibrated over/under-confidence signals as explicit Decision risk inputs; still never mutates Confidence from Decision |
| **Pass-probability / Prediction context** | Decision may consume Prediction snapshots as context after derive-first/store-second readiness/prediction rules — not as a competing selector |
| **Multi-action session batches** | Decision Engine may emit an ordered batch for a window; Mission Intelligence still projects; ownership of selection unchanged |
| **Personalisation from Decision Journal** | Accept/dismiss evidence informs Behaviour and future candidate preference — via Evidence → Strategies, not silent Decision-side mutation |
| **Insight / AI Coach** | Reads Decision + explanation chain; never silent Twin writes; never owns selection |
| **Institutional overlays** | Observe Decisions; do not fork student-owned Twin or invent syllabus |

## 12.1 Compatibility guarantees to preserve

1. Decision Engine remains the only next-action selector.  
2. Readiness remains preparedness judgement only.  
3. Twin remains sole educational-state authority.  
4. Curriculum V1 and V2 remain loadable; weights/order via canonical helpers.  
5. Evidence append-only semantics remain permanent.  
6. Deterministic cores remain free of required network LLM calls.  
7. Missions remain projections of Decisions, not of raw readiness scores.  
8. Recommendations remain packaging of Decisions, not competing rankers.

## 12.2 Deliberately unlocked

Not locked by this analysis beyond ownership:

- Exact selection / ranking function  
- Numeric weights among reason factors  
- Optimization formulations  
- Bayesian decision policies  
- Full Decision State schema  
- Recommendation packaging schemas  
- Mission batching algorithms  

---

# 13. Educational Fidelity Review

Educational fidelity: prefer honest learning-state representation and learning-value action over engagement theatre.

## 13.1 Confirmations (binding)

| Commitment | Status |
|---|---|
| **Decision Engine never owns evidence as belief authority** | Confirmed — outcomes may become evidence via recording paths; Decision does not rewrite history or Twin beliefs |
| **Decision Engine never updates Twin domains** | Confirmed — write/read firewall; Update Strategies only |
| **Decision Engine never invents Twin beliefs or syllabus** | Confirmed — consumes Twin + CurriculumContext only |
| **Decision Engine never coerces unknown readiness** | Confirmed — inherits warrant; cold-start prefers diagnostics / evidence-creating actions |
| **Decision Engine always remains explainable** | Confirmed — reason codes + candidates + lineage mandatory in core path |
| **Decision Engine selects learning value over activity theatre** | Confirmed — Behaviour/constraints bound feasibility; streaks do not define value |

## 13.2 Fidelity commitments in product language

1. Do not recommend polish because streaks look good while mocks are missing.  
2. Do not narrate self-report Confidence as permission to skip foundations.  
3. Do not treat mission completion as proof a Decision “worked” for mastery.  
4. Do not hide High Knowledge + Low Memory tension behind a single bland suggestion story.  
5. Do not present “study anything” filler when high-weight risks are known.  
6. Do not let coach/LLM invent “do Topic Z” without Decision + Curriculum support.  
7. Do not schedule unsustainable cram plans that Behaviour says will fail, then blame the student.

## 13.3 Anti-fidelity patterns to reject

| Pattern | Why it fails fidelity |
|---|---|
| “100% mission week ⇒ recommend harder content” | Activity ≠ learning readiness for harder work |
| Cold-start Mid readiness used to justify advanced rehearsal | Fabricates preparedness |
| Confidence slider upgrades next-action aggressiveness as if mastery | Confidence contamination |
| Recommendation copy that disagrees with Decision reason codes | Broken explainability |
| Mission generator writing private “priority scores” as mastery | Parallel authority |
| Rest never allowed despite burnout flags | Feasibility denial; collapses learning sustainability |
| Rest always preferred despite high-weight exam risk | Avoidance theatre; erases educational need |

---

# 14. Recommendations

## 14.1 Architecture milestone that should follow

**Next milestone:** Capability 2.8 Decision Engine **architecture note** (short, binding) — then structural/read-side contracts — then implementation in a later milestone.

The architecture note should lock, without formulas:

1. Decision output contract (selected action, candidates, reason codes, lineage hooks)  
2. Input contracts: Twin snapshot + `ReadinessState` + Goals + Constraints + `CurriculumContext`  
3. Firewall vs Readiness (context only; warrant inheritance; no coercion of unknown → Mid/High)  
4. Firewall vs Recommendation (2.9 packages only) and Mission Intelligence (2.10 projects only)  
5. Cold-start / low-warrant decision posture (prefer evidence-creating actions)  
6. V1/V2 CurriculumContext via canonical helpers only  
7. Confidence stance for Decision v1 (risk framing only; no calibrated Confidence domain required to start)  
8. Relationship to legacy `RecommendationService` (convergence path; no hybrid temporary truth)  
9. Explicit non-goals: no Twin writes, no readiness recomputation, no mission generation, no scoring/optimization in the first structural pass  

## 14.2 Educational design recommendations

1. Treat factor **disagreement** as Decision information — preserve High Knowledge + Low Memory style tensions in reason codes.  
2. Prefer diagnostic / evidence-creating actions under low warrant over fake Mid confidence in selection.  
3. Keep Assessment-shaped needs distinct from Behaviour feasibility in every Decision narrative hook.  
4. Keep Constraints as ambition bounds, not as erasers of high-weight educational risk.  
5. Do not deepen legacy recommendation ranking while Twin-first Decision contracts land.  
6. Require candidate sets early — “why not the other topic?” is educationally load-bearing.  
7. Encode Readiness Architecture Review conditions as Decision input invariants before any production wiring.

## 14.3 Upstream conditions acknowledged

This analysis accepts and encodes the Readiness Architecture Review conditions relevant to 2.8:

- `ReadinessState` as context only  
- Evidence Warrant end-to-end  
- No legacy TopicProgress hybrid truth  
- `CurriculumContext` via canonical helpers  
- No product narration of supportive Knowledge Strength as exam readiness  
- Confidence omitted from readiness; not reused as Decision mastery proxy  
- Prediction snapshots (when present) are not live selection authority  
- Documentation convergence remains a follow-up for subsystem docs outside this analysis charter  

Also retains Epic 2 Midpoint conditions still in force: write/read firewall, no parallel learner-state forks, Confidence separability before rich risk framing, V1/V2 invariants.

## 14.4 Architecture compliance checklist

| Invariant | Status for Decision Engine analysis |
|---|---|
| Twin is sole educational-state authority | Decision consumes Twin; does not fork beliefs |
| Evidence is only legitimate belief input | Decision does not mutate beliefs; outcomes become evidence via recording paths |
| Strategies own domain evolution | Decision is not a write strategy |
| Readiness ≠ Decision; Decision ≠ Recommendation packaging; Decision ≠ Missions | Binding |
| Activity ≠ learning value; Confidence ≠ mastery; Behaviour ≠ learning | Binding |
| Curriculum V1/V2 compatibility | Required; CurriculumContext via canonical helpers |
| No LLM ownership of core selection | Binding |
| No implementation / algorithms / scoring in this milestone | Satisfied |

## 14.5 Explicit stop line

This milestone delivers **analysis only**.

**Do not proceed in this milestone to:** code, algorithms, scoring, optimization, dataclasses, services, tests, database changes, Recommendation packaging design detail, Mission generation design detail, or UI.

**Next engineering step (separate milestone):** Capability 2.8 Decision Engine architecture note → structural read-side contracts → implementation → tests → capability review — following Epic 2 engineering standards.

---

# 15. Decision Ownership Principles

These principles bind Capability 2.8 educational design and all downstream consumers.

1. **Decision Engine alone selects the highest-value next learning action.**  
2. **Readiness judges preparedness; it never selects actions.**  
3. **Recommendation Engine packages Decisions; it never invents ranking.**  
4. **Mission Intelligence projects Decisions; it never stores private mastery.**  
5. **Plans and missions are consequences of intelligence, not the learner model.**  
6. **Curriculum is the only syllabus authority; Decision Engine consumes `CurriculumContext`.**  
7. **Twin is the only educational-state authority; Decision Engine consumes Twin snapshots.**  
8. **Learning Evidence is the only legitimate belief-changing input; Decision outcomes enter via evidence recording, not silent Twin writes.**  
9. **Highest value means educational value toward the Goal — not engagement, streaks, or completion theatre.**  
10. **Constraints bound ambition; they do not erase educational need.**  
11. **Evidence Warrant flows into reason codes; unknown must not become Mid or High.**  
12. **Every Decision is explainable: reason codes, candidates, and lineage are mandatory.**  
13. **Core selection is deterministic and free of black-box LLM ownership.**  
14. **V1 and V2 curricula remain first-class through canonical traversal and weights.**  
15. **Educational fidelity over engagement theatre — always.**

---

# Appendix A — Decision Engine in the capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot is the read input; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains Decision consumes without modification |
| 2.7 | Readiness Aggregation | Supplies `ReadinessState` context; firewall preserved |
| **2.8** | **Decision Engine** | **This analysis precedes architecture and implementation** |
| 2.9 | Explainable Recommendation Engine | Packages Decision output; must not invent ranking |
| 2.10 | Mission Generation Intelligence | Projects Decision output into daily structure |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.8.1 — Decision Engine Educational Analysis |
| Nature | Architecture / educational analysis only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required going forward; analysis introduces no traversal changes |
| Application code intentionally untouched | Yes |
| Upstream gate | Readiness Architecture Review — APPROVED WITH CONDITIONS — conditions encoded herein |
| Next | Capability 2.8 Decision Engine architecture note (separate milestone) |

---

*End of Capability 2.8.1 Decision Engine Educational Analysis. STOP.*
