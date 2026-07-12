# Capability 2.7.1 — Readiness Educational Analysis

**Status:** Educational / architecture analysis — analysis only  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.7 Readiness Aggregation (educational analysis preceding architecture and implementation)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Gate:** Epic 2 Midpoint Architecture Review — APPROVED WITH CONDITIONS ([`docs/reviews/EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md`](../reviews/EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md))  
**Companions:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md), Capability 2.5 / 2.6 domain analyses  
**Scope:** Readiness definition, boundaries, belief consumption, factors, cold start, explainability, and downstream relationships — **no implementation, code, dataclasses, services, tests, schema, migrations, or scoring formulas**

---

## Document purpose

This milestone answers what **Readiness** is as the first Epic 2 reasoning capability: an educational judgement derived from Twin domains that owns **no primary evidence** and must aggregate beliefs **without modifying them**.

Knowledge, Memory, Behaviour, and Performance now exist as Twin write-path domains. Readiness is the first **read-side** intelligence layer. It prepares Capability 2.7 architecture (factor contracts, cold-start semantics, Prediction snapshot rules, legacy convergence) the same way domain analyses prepared 2.5–2.6: **educational clarity first**, structural aggregation later, numeric scoring deferred.

**Non-goals of this document**

- Code, pseudocode algorithms, dataclasses, or service refactors  
- Database schemas, Alembic migrations, or ORM layouts  
- Concrete readiness weights, averages, pass-probability formulas, or Bayesian math  
- UI redesign, analytics dashboards as a second intelligence layer, gamification, or notifications  
- Decision Engine, Recommendation Engine, or Mission Generation design detail beyond relationship boundaries  
- Replacement of Curriculum Engine, Evidence Model, or Twin aggregate contracts  

---

# 1. Definition of Readiness

## 1.1 Canonical question

> **How prepared is the student for the target sitting, given syllabus weight, Twin educational state, and remaining time?**

Not: what they know *now* as durable mastery (Knowledge).  
Not: whether they will still know it when it matters (Memory).  
Not: how they actually study (Behaviour).  
Not: how they perform when assessed (Performance).  
Not: how certain they *feel* (Confidence).  
Not: what they should do in the next session (Decision Engine).

Readiness answers: *Are we on track for the sitting?*  
Decision Engine answers: *What is the highest-value thing to do next?*

## 1.2 Educational meaning

**Readiness** is an **educational judgement** — a derived, factorable estimate of exam preparedness — synthesised from multiple Twin domains plus Curriculum weights and Goals constraints.

It is:

- **derived** from educational beliefs and structural Twin facts;  
- **factorable** into named dimensions that can be explained separately;  
- **curriculum-relative** — preparedness is always against official syllabus weight and sitting Goals, never against an invented topic tree;  
- **uncertain when evidence is thin** — uncertainty is part of the judgement, not an error to hide;  
- **read-side only** — it does not write Learning Evidence and does not mutate Twin domains.

It is **not**:

- a primary Twin write domain fed by its own evidence stream;  
- a second mastery store;  
- a motivation or streak metric;  
- a next-action selector;  
- a mission generator;  
- a marketing claim of “you’re ready” without warrant.

## 1.3 Distinctions (binding vocabulary)

| Concept | Educational question | Relation to Readiness |
|---|---|---|
| **Readiness** | Are we on track to be prepared for the sitting? | Derived aggregate judgement; owns factor synthesis and explanation inputs for preparedness |
| **Confidence** | How certain does the student *feel*, and how well is that calibrated? | Separable Twin concern (and/or estimate warrant). Self-report must never be treated as readiness or mastery. Estimate-warrant confidence (“how sure are we of this judgement?”) belongs *with* readiness honesty — and must be named distinctly from self-report Confidence |
| **Performance** | How does the student perform when assessed? | Primary input domain for assessment strength/weakness; not readiness itself |
| **Mastery** | How well can the student perform a curriculum entity *now*? | Knowledge-domain belief; Readiness consumes it (or structural proxies) as Knowledge Strength / coverage inputs — does not own or update mastery |
| **Motivation** | Willingness and sustainability to keep studying | Context that Behaviour / Confidence may surface; never substitutes for preparedness. High motivation ≠ high readiness |

Governing principle (Educational Intelligence Architecture §13):

> **Confidence is not mastery; Behaviour is not learning; Activity is not readiness.**

Extended for this capability:

> **Readiness is not Performance; Readiness is not Confidence; Readiness is not Mastery; Readiness is not Motivation; Readiness never invents preparedness from absence.**

## 1.4 Product purpose

Readiness exists so Kwalitec can:

1. Present an **honest preparedness narrative** relative to the active Goal’s sitting and official syllabus weights.  
2. Supply **named preparedness factors** to the Decision Engine (urgency, risk concentration, time pressure, evidence warrant) without selecting actions.  
3. Anchor **explainable** “why this matters for the exam” stories in Twin + Curriculum lineage.  
4. Optionally **snapshot** derived judgements (PredictionState) for history — after derivation, never instead of it.  
5. Converge legacy readiness/analytics narratives toward Twin-first authority without creating a third formula.

## 1.5 Ubiquitous language anchors

| Term | Meaning |
|---|---|
| **Readiness** | Derived estimate of sitting preparedness; factorable; explainable |
| **Readiness factor** | Named structural dimension of preparedness (coverage, knowledge strength, memory stability, behaviour reliability, assessment performance, time pressure, warrant, …) |
| **Overall readiness** | Synthesised educational judgement across factors — never an opaque score without decomposition |
| **Uncertainty / warrant** | Explicit honesty about how much evidence supports the judgement |
| **Cold start** | Little or no Twin evidence; readiness must communicate unknown / low warrant, not fabricate High preparedness |
| **Prediction snapshot** | Optional stored copy of a derived readiness/pass estimate; storage ≠ derivation authority |

---

# 2. Responsibilities

## 2.1 Owns

| Responsibility | Educational meaning |
|---|---|
| **Aggregation of educational beliefs** | Read Twin Knowledge, Memory, Behaviour, Performance (and Goals / Curriculum context) as inputs — without changing them |
| **Factor synthesis** | Compose named readiness factors from those inputs into a factorable preparedness picture |
| **Examination preparedness assessment** | Answer the sitting-preparedness question relative to syllabus weight and remaining time |
| **Explanation inputs** | Produce factor attributions and lineage hooks so every readiness claim can be traced Curriculum → Evidence → Twin → Factor → Overall |

## 2.2 Must not own

| Non-responsibility | Why |
|---|---|
| **Evidence** | Learning Evidence is append-only history; Readiness never authors or rewrites it |
| **Mastery** | Knowledge owns mastery structure and beliefs |
| **Retention** | Memory owns retention structure and beliefs |
| **Behaviour** | Behaviour owns study-practice consistency and patterns |
| **Recommendations** | Explainable Recommendation Engine packages Decision Engine output |
| **Mission generation** | Mission Generation Intelligence projects Decision Engine output into daily structure |
| **Next-action selection** | Decision Engine owns “what next” |
| **Twin domain mutation** | Only Update Strategies via the Twin Update Pipeline may evolve Twin beliefs |
| **Syllabus structure / weights** | Curriculum Engine remains syllabus truth |
| **Parallel learner-state stores** | Twin remains educational-state authority; no third readiness truth |

## 2.3 Position in the intelligence stack

```
Curriculum + Goals
        +
Digital Twin domains (Knowledge · Memory · Behaviour · Performance · …)
        ↓
Readiness Aggregation  (read-side judgement)
        ↓
Decision Engine        (read-side next-action selection)
        ↓
Recommendation / Mission projections
```

Write path and read path must not be conflated. Readiness sits entirely on the **read** side.

---

# 3. Educational Beliefs Consumed

Readiness **consumes** Twin domains as educational beliefs and structural facts. It **never modifies** them. Consumption is observational: same Twin snapshot in → same factor attributions out (deterministic core).

## 3.1 Knowledge

| Aspect | How Readiness consumes it |
|---|---|
| **Educational question answered by Knowledge** | What does the student know *now*? |
| **What Readiness reads** | Topic mastery slots, evidence lineage, stored mastery beliefs when present; structural coverage of syllabus identities |
| **What Readiness does with it** | Informs Curriculum Coverage and Knowledge Strength factors |
| **What Readiness must not do** | Invent mastery; fill empty `mastery_belief` bags; treat Knowledge-held `CONFIDENCE_RATING` lineage as calibrated mastery (midpoint condition) |

## 3.2 Memory

| Aspect | How Readiness consumes it |
|---|---|
| **Educational question answered by Memory** | Will the student still know it when it matters? |
| **What Readiness reads** | Retention slots, `last_reinforced` clocks, revision lineage, retention beliefs when present |
| **What Readiness does with it** | Informs Memory Stability / retention-risk factors relative to sitting date |
| **What Readiness must not do** | Update reinforcement clocks; schedule revisions; collapse Memory into Knowledge Strength |

## 3.3 Behaviour

| Aspect | How Readiness consumes it |
|---|---|
| **Educational question answered by Behaviour** | How does the student actually study? |
| **What Readiness reads** | Consistency structure, session/pattern lineage, adherence-related structural facts, capacity realism vs Goals |
| **What Readiness does with it** | Informs Behaviour Reliability / pace feasibility / sustainability risk relative to remaining calendar |
| **What Readiness must not do** | Grant preparedness from streaks or mission completion alone; treat adherence as assessment strength |

## 3.4 Performance

| Aspect | How Readiness consumes it |
|---|---|
| **Educational question answered by Performance** | How does the student perform when assessed? |
| **What Readiness reads** | Assessment lineage, scoped summaries, exam-condition vs formative distinctions when present |
| **What Readiness does with it** | Informs Assessment Performance / assessment strength and weakness concentration factors |
| **What Readiness must not do** | Emit pass probability inside Performance; treat a single mock as overall readiness; invent scored accuracy from arbitrary summary keys without a defined fact vocabulary |

## 3.5 Supporting context (not Twin belief domains owned by Readiness)

| Input | Role for Readiness |
|---|---|
| **Curriculum** | Syllabus denominator, order, exam weights (V1/V2 via canonical helpers only) |
| **Goals** | Sitting date, ambition, weekly hours, capacity constraints |
| **Confidence (when available)** | Optional / provisional factor only; omit from readiness v1 or mark lower warrant than Performance; never equate self-report with preparedness |
| **Identity** | Scope Twin to student / curriculum / sitting |

## 3.6 Consumption contract (binding)

1. Readiness receives a Twin snapshot (plus Curriculum + Goals) and returns a factorable judgement.  
2. No Twin domain field is written by Readiness Aggregation.  
3. Sparse or empty domains produce **named low-warrant factors**, not silent defaults of “ready.”  
4. Orphan evidence types without Twin strategy ownership must not be absorbed ad hoc into readiness.  
5. Secondary evidence columns (Choice B) must not be smuggled into readiness without an architecture note.

---

# 4. Readiness Factors

Structural readiness dimensions are **educational meanings**, not formulas. Names are illustrative and may be refined in the architecture note; the requirement is factorability and explainability.

## 4.1 Factor catalogue (educational meaning only)

| Factor | Educational meaning |
|---|---|
| **Curriculum Coverage** | How much of the official syllabus (weighted) has meaningful Twin presence — topics/slots touched relative to the curriculum denominator for the Goal. Coverage is exposure structure, not proof of mastery. |
| **Knowledge Strength** | How strong current mastery beliefs (or structural mastery proxies) appear across weighted curriculum identities. Answers “do they know it *now*?” at preparedness grain — without owning mastery math. |
| **Memory Stability** | How likely demonstrated knowledge remains available at the sitting — retention risk, freshness of reinforcement, decay pressure vs exam date. |
| **Behaviour Reliability** | Whether study practice is consistent and feasible enough to close remaining gaps in time — pace realism, adherence lineage, sustainability — never “they completed missions so they are exam-ready.” |
| **Assessment Performance** | How the student fares under assessed conditions — scoped accuracy trends, mock/exam-condition rehearsal, concentrated weakness on high-weight areas. Strongest assessed signal into preparedness narratives. |
| **Time / Goal Pressure** *(supporting)* | Remaining calendar and capacity relative to Goals — amplifies or reframes other factors; does not invent Knowledge or Performance. |
| **Evidence Warrant / Uncertainty** *(meta-factor)* | How much evidence supports the other factors. Sparse Twin → high uncertainty. This factor exists so honesty is first-class, not an afterthought. |

## 4.2 Factor principles

1. **Every overall readiness claim must decompose** into named factors.  
2. **Factors may disagree** — that disagreement is educational information (see §11).  
3. **No opaque composite** without attributions.  
4. **No formulas in this milestone** — numeric weights, averages, and scoring functions are deferred.  
5. **V1/V2 safe** — factors that use weights must obtain them via canonical Curriculum helpers; no global Section requirement.

## 4.3 What is not a readiness factor

- Motivation score as preparedness  
- Streak length as exam readiness  
- Self-report Confidence as Assessment Performance  
- Mission completion count as Knowledge Strength  
- A single dashboard vanity percentage without Twin lineage  

---

# 5. Structural vs Derived

## 5.1 Classification

| Kind | What belongs here | Examples for Readiness |
|---|---|---|
| **Stored (Twin write path)** | Primary educational beliefs and structural slots evolved only from Learning Evidence via Update Strategies | Knowledge slots / mastery beliefs; Memory retention / `last_reinforced`; Behaviour consistency structure; Performance assessment summaries; Goals; optional PredictionState *snapshots of prior derived judgements* |
| **Derived (Readiness Aggregation)** | Educational judgements computed on read from Twin + Curriculum + Goals | Named readiness factors; overall preparedness judgement; factor attributions; uncertainty / warrant statements |
| **Computed (presentation / analytics)** | Product projections that must share definitions with derived factors — never fork authority | UI readiness narrative; dashboard cards reading Twin-first factors; coach narration of existing attributions |

## 5.2 Why Readiness remains read-side only

1. **Authority** — Twin domains remain the sole educational-state authority; readiness is a lens, not a competing store of beliefs.  
2. **Audit** — Evidence → Strategy → Twin lineage stays intact; readiness does not invent a side write.  
3. **Explainability** — Factors must cite Twin state that already exists; inventing readiness “beliefs” would break the chain.  
4. **Determinism** — Same Twin + Curriculum + Goals → same factor set in the core path.  
5. **Safety under cold start** — Absence stays absence; a write-side readiness domain would be tempted to invent “default High” or “default Mid” states.  
6. **Midpoint condition** — Write/read firewall is binding: aggregation must not mutate Twin domains, bypass the Update Pipeline, select next actions, or generate missions.

## 5.3 Optional Prediction snapshots

Storing a readiness or pass-probability snapshot in PredictionState is allowed **after** derivation:

```
Derive readiness factors (read)
        ↓
Optionally persist snapshot (Prediction path)
```

Storage must not skip aggregation. Snapshots are historical copies for audit and trend — not a parallel readiness truth that other services may update independently.

---

# 6. Cold Start Philosophy

## 6.1 Definition of cold start

A Twin is in **cold start** (or sparse start) when one or more of the following hold:

- No or few Knowledge topic slots / empty mastery beliefs  
- No or few Memory reinforcements / empty retention beliefs  
- Thin or empty Behaviour lineage / empty consistency metrics  
- No or sparse Performance assessments / empty summaries  
- Goals may exist (sitting date, hours) while educational evidence does not  

Goals alone never create preparedness.

## 6.2 Explicit uncertainty

Uncertainty is a **first-class educational output**, not a UI inconvenience.

| Situation | Honest readiness posture |
|---|---|
| No assessment evidence | Assessment Performance = unknown / low warrant — not “average,” not “assumed weak,” not “assumed strong” |
| Empty mastery beliefs | Knowledge Strength = unknown / structural-coverage-only if slots exist — never fabricated High mastery |
| Empty Memory | Memory Stability = unknown — never assume durable retention |
| Strong Behaviour, empty Performance | Behaviour Reliability may be informative for pace; overall readiness remains low-warrant for exam preparedness |
| New Twin with Goals only | Overall readiness = not yet knowable; communicate uncertainty explicitly |

## 6.3 Never fabricate preparedness

Forbidden cold-start behaviours:

- Inventing High readiness to encourage engagement  
- Treating mission adherence as exam readiness  
- Filling empty belief bags inside the aggregator “just to make a score”  
- Averaging missing factors as neutral Mid  
- Narrating “you’re on track” without Twin warrant  
- Using self-report Confidence to invent Assessment Performance  

Correct cold-start posture:

> **We do not yet know if you are prepared.**  
> Here is what little we have (coverage started / no mocks yet / study cadence beginning).  
> Uncertainty is high.

Decision Engine (later) may prefer diagnostic or assessment-shaped actions under cold start — that is **decision**, not readiness inventing Performance.

---

# 7. Explainability

## 7.1 Mandatory chain

Every readiness judgement must be traceable:

```
Curriculum
    ↓
Evidence
    ↓
Twin Domain
    ↓
Readiness Factor
    ↓
Overall Readiness
```

Extended when consumed downstream:

```
… → Overall Readiness / factors
        ↓
Decision Engine reason codes
        ↓
Recommendation explanation
```

Students and auditors must never be asked to trust an opaque “78% ready” without this chain.

## 7.2 Layer examples (educational, not formulas)

| Layer | Example content |
|---|---|
| **Curriculum** | “Section C carries substantial exam weight.” |
| **Evidence** | “Last mock on Topic T showed repeated incorrect attempts (evidence ids …).” |
| **Twin Domain** | “Performance summaries weak on T; Memory last reinforced long ago; Knowledge slot present with low warrant.” |
| **Readiness Factor** | “Assessment Performance and Memory Stability elevate sitting risk on a high-weight slice.” |
| **Overall Readiness** | “Preparedness is fragile for the sitting: coverage partial, assessment warrant thin on weighted areas, uncertainty explicit.” |

## 7.3 Attribution requirements

1. Each presented factor cites Twin domain inputs (and evidence ids where available).  
2. Overall readiness cites contributing factors — including disagreement between factors.  
3. Uncertainty / warrant appears whenever evidence density is low.  
4. Explanations must not invent evidence, syllabus topics, or Twin beliefs.  
5. LLM / coach narration may only restate chain-supported attributions — never author readiness.

## 7.4 Forbidden explanation patterns

- Single opaque composite without factors  
- Explanations that cite UI labels but not Twin/evidence  
- Post-hoc stories that disagree with Twin lineage  
- Collapsing all factors into Motivation or streak language  
- Treating Confidence self-report as Assessment Performance in the narrative  

---

# 8. Relationship with Recommendation Engine

## 8.1 Separation of concerns

| Concern | Owner |
|---|---|
| Sitting preparedness judgement | Readiness Aggregation |
| Highest-value next action | Decision Engine |
| Product packaging of that action (title, explanation chain, urgency presentation) | Explainable Recommendation Engine (Capability 2.9) |

## 8.2 How Readiness informs recommendations

Readiness supplies **context** that recommendations may surface:

- time pressure / sitting urgency narratives;  
- risk concentration on weighted syllabus areas;  
- evidence warrant honesty (“we recommend a diagnostic because readiness uncertainty is high”);  
- factor attributions that appear in the explanation chain when relevant.

## 8.3 What Readiness never does

- Choose the recommended action  
- Rank candidate actions  
- Package recommendation UI  
- Accept/dismiss recommendations  
- Mutate Twin because a recommendation was shown  

**Readiness informs recommendations; it never chooses actions.**

Accepting or dismissing a recommendation becomes Learning Evidence later (Behaviour / Decision State) — outside Readiness ownership.

---

# 9. Relationship with Decision Engine

## 9.1 Educational boundary

Readiness: *Are we on track?*  
Decision Engine: *What should we do next?*

Same Twin snapshot; different questions; different owners.

## 9.2 How Decision Engine consumes Readiness

Decision Engine may use readiness outputs as **context inputs**, for example:

| Readiness signal | Educational use by Decision Engine |
|---|---|
| High time pressure + weak Assessment Performance on high-weight topics | Prefer high-value remediation / exam-condition rehearsal |
| High uncertainty / cold start | Prefer diagnostic or evidence-creating actions |
| Strong Knowledge/Performance but weak Memory Stability | Prefer revision-shaped actions for high-weight stale topics |
| Strong Behaviour Reliability but thin Performance | Prefer assessment-shaped actions within feasible intensity |
| Fragile Behaviour Reliability near the sitting | Constrain intensity / protect sustainability — without erasing Performance evidence |

## 9.3 What Readiness does not decide

- Topic selection  
- Action type (study / revise / assess / rest)  
- Session length or mission composition  
- Accept/dismiss handling  
- Plan regeneration  

**Readiness does not make decisions.** It supplies factorable preparedness context so Decision Engine reason codes can cite sitting risk honestly.

## 9.4 Firewall

If a design ever needs “readiness said do X,” that design is wrong. Decision Engine owns selection; Readiness owns preparedness judgement only.

---

# 10. Relationship with Missions

## 10.1 Dependency chain

```
Twin + Curriculum + Goals
        ↓
Readiness Aggregation          (preparedness context — optional consumer)
        ↓
Decision Engine                (selected actions / reason codes)
        ↓
Mission Generation Intelligence (Capability 2.10)
        ↓
Mission / MissionTask artefacts
```

## 10.2 Educational rule

**Mission Generation depends on the Decision Engine rather than on Readiness directly.**

Missions are adaptive consequences of selected educational actions. They must:

1. Start from Decision Engine outputs (or a batch for a session window);  
2. Respect Behaviour feasibility and Goals capacity;  
3. Remain regenerable when Twin state changes;  
4. Never store a private mastery or readiness model inside mission rows.

## 10.3 Why not Readiness → Mission directly

- Readiness does not choose actions; missions need concrete actions.  
- Direct readiness→mission would reintroduce “activity theatre” (schedule filler to “raise readiness”).  
- Explainability requires Decision reason codes between preparedness context and daily tasks.  
- Midpoint non-goals: Capability 2.7 must not generate missions.

Readiness may appear in mission *explanations* when Decision Engine cited readiness factors — as lineage, not as the mission author.

---

# 11. Educational Scenarios

Educational interpretation only — no scoring.

## 11.1 High Knowledge + Low Memory

**Situation:** Mastery beliefs look strong on weighted topics; reinforcement is stale; sitting is approaching.

**Interpretation:** The student may be able to perform *now* in untimed conditions, but retention risk threatens sitting preparedness. Readiness should show Knowledge Strength relatively supportive while Memory Stability elevates risk. Overall preparedness is fragile despite “knows it now.” Decision Engine (later) may prefer revision over new coverage for high-weight stale topics — Readiness does not choose that action; it makes the tension visible.

## 11.2 High Behaviour + Low Performance

**Situation:** Consistent mission adherence and study cadence; few or weak assessed outcomes.

**Interpretation:** The student shows up (Behaviour Reliability), but exam preparedness warrant is thin (Assessment Performance unknown/weak). Activity is not readiness. Overall judgement must not declare preparedness from streaks. Honest narrative: practice habit is forming; assessed competence is not yet established. Decision Engine should favour assessment-shaped actions within feasible intensity.

## 11.3 Low Knowledge + High Confidence

**Situation:** Sparse or weak mastery structure; student self-reports high Confidence (or Knowledge holds `CONFIDENCE_RATING` lineage without a Confidence domain).

**Interpretation:** Feeling ready is not being ready. Readiness must keep Confidence separable and lower-warrant than Performance/Knowledge. Overall preparedness remains low or uncertain. Narrating “you feel ready” as “you are ready” is educationally dishonest and violates midpoint Confidence conditions. Calibration gap is a Decision risk-framing signal later — not a readiness upgrade now.

## 11.4 High Performance + Weak Behaviour

**Situation:** Strong mock/quiz outcomes; irregular adherence; capacity risk vs remaining calendar.

**Interpretation:** Assessment Performance supports preparedness *where assessed*; Behaviour Reliability questions whether remaining gaps can be closed sustainably. Readiness should preserve the assessment signal while flagging pace/feasibility risk — not erase mocks because missions were missed, and not ignore calendar risk because mocks were strong. Decision Engine balances value vs feasibility; Readiness surfaces both factors honestly.

## 11.5 Additional cold-start vignette

**Situation:** Goals set; Twin domains empty.

**Interpretation:** Overall readiness is unknown. Factors are low-warrant. Never fabricate Mid or High preparedness. Prefer honesty: insufficient evidence to judge sitting preparedness.

---

# 12. Risks

| Risk | Educational / architectural impact | Mitigation |
|---|---|---|
| **Averaging unrelated factors** | Hides educational tension (e.g. strong Behaviour + weak Performance averaged into false Mid readiness) | Keep factors separable; surface disagreement; defer numeric aggregation discipline to architecture — never silent equal averages as product truth |
| **Hiding uncertainty** | False preparedness; broken trust | Explicit Evidence Warrant / Uncertainty factor; cold-start contract |
| **Duplicated readiness stores** | Divergent “78%” vs Twin factors; dual authority with legacy `ReadinessService` / analytics | Twin-first convergence; no third formula; snapshots only after derivation |
| **Confidence contamination** | Self-report treated as mastery or assessment strength | Omit Confidence from readiness v1 or provisional low-warrant only; never equate Knowledge-held confidence ratings with calibrated Confidence |
| **Circular reasoning** | Readiness writes Twin → Twin feeds Readiness; or missions written to “improve readiness” without evidence | Strict read-side firewall; missions from Decision Engine only; beliefs only via Evidence → Strategies |
| **Activity-as-readiness** | Mission completion narrated as exam preparedness | Behaviour Reliability ≠ Assessment Performance ≠ Overall readiness |
| **Single-mock overclaim** | One strong mock becomes “ready to pass” | Assessment Performance is one factor; warrant and Curriculum weight still required |
| **Readiness conflated with next action** | Wrong owner; opaque product behaviour | Firewall vs Decision Engine (Capabilities 2.7 vs 2.8) |
| **Opaque composites** | Product thesis failure | Mandatory factorability + explainability chain |
| **V1 breakage** | Section-required readiness logic fails flat curricula | Canonical Curriculum helpers; no global Section assumption |
| **Smuggling belief engines into aggregation** | Premature scoring; unmaintainable math; inventing mastery inside readiness | Structural/factorable first; belief enrichment stays in domain strategies |
| **LLM ownership creep** | Invented preparedness stories | Coach narrates chain-supported factors only |
| **Absorbing orphan evidence** | Ad hoc readiness from types without Twin ownership | Midpoint rule: do not absorb orphan types into 2.7 |
| **Choice B smuggling** | Secondary evidence updates reintroduced via readiness | Keep Choice A until deliberate architecture note |

---

# 13. Future Extensibility

The architecture must allow richer reasoning **without changing ownership boundaries**.

| Future capability | How it extends without breaking architecture |
|---|---|
| **Pass probability** | New derived / Prediction output reading the same Twin + Curriculum + Goals; still read-side; still factorable; still optional snapshot — not a Performance or Behaviour write |
| **Confidence calibration** | Confidence domain or dedicated update path supplies calibrated signals; Readiness may consume as an explicit factor with clear warrant; still never mutates Confidence |
| **Adaptive weighting** | Factor synthesis may later weight dimensions by sitting proximity, evidence density, or curriculum format — still deterministic core; still explainable attributions; still no Twin mutation |
| **Bayesian reasoning** | Belief math belongs in Knowledge/Memory/Performance enrichment or a dedicated inference engine feeding Twin beliefs; Readiness continues to aggregate beliefs, not invent them |
| **Predictive modelling** | Prediction engines produce snapshots via Prediction path after reading Twin; Analytics/Coach consume; Decision Engine may use predictions as context — Readiness remains the preparedness judgement layer or shares a clear sibling Prediction contract without dual authority |

## 13.1 Compatibility guarantees to preserve

1. Readiness remains read-side and factorable.  
2. Twin remains sole educational-state authority.  
3. Curriculum V1 and V2 remain loadable; weights via canonical helpers.  
4. Evidence append-only semantics remain permanent.  
5. Deterministic cores remain free of required network LLM calls.  
6. Decision Engine remains the only next-action selector.  
7. Missions remain projections of decisions, not of raw readiness scores.

## 13.2 Deliberately unlocked

Not locked by this analysis beyond ownership:

- Numeric factor weights  
- Exact composite functions  
- Pass-probability model family  
- Bayesian priors / update equations  
- Adaptive weighting schedules  
- Confidence domain schema  

---

# 14. Educational Fidelity Review

Educational fidelity: prefer honest learning-state representation over engagement theatre.

## 14.1 Confirmations (binding)

| Commitment | Status |
|---|---|
| **Readiness never owns evidence** | Confirmed — Evidence remains append-only history; Readiness only cites lineage |
| **Readiness never updates the Twin** | Confirmed — write/read firewall; Update Strategies only |
| **Readiness never invents beliefs** | Confirmed — empty beliefs stay empty; structural proxies named honestly; no fabricated High preparedness |
| **Readiness always communicates uncertainty honestly** | Confirmed — Evidence Warrant / Uncertainty is first-class; cold start never marketed as ready |

## 14.2 Fidelity commitments in product language

1. Do not hide weak mocks behind streak narratives.  
2. Do not narrate self-report Confidence as exam readiness.  
3. Do not treat mission completion as sitting preparedness.  
4. Do not average away educational disagreement between factors.  
5. Do not present opaque percentages without factor attributions and warrant.  
6. Do not let coach/LLM invent “you’re ready on Section C” without Twin support.

## 14.3 Anti-fidelity patterns to reject

| Pattern | Why it fails fidelity |
|---|---|
| “100% mission week ⇒ exam ready” | Activity ≠ readiness |
| Cold-start Mid readiness by default | Fabricates preparedness |
| Confidence slider upgrades readiness composite | Confidence contamination |
| Dashboard readiness that disagrees with Twin factors | Parallel authority |
| Mission generator writing “readiness tasks” from a private score | Circular / wrong owner |

---

# 15. Recommendations

## 15.1 Architecture milestone that should follow

**Next milestone:** Capability 2.7 Readiness Aggregation **architecture note** (short, binding) — then structural/read-side design contracts — then implementation in a later milestone.

The architecture note should lock, without formulas:

1. Named factor list and attribution contract  
2. Cold-start / empty-belief / uncertainty semantics (binding midpoint condition)  
3. V1/V2 weight and ordering via canonical Curriculum helpers  
4. Confidence stance for readiness v1 (omit vs provisional low-warrant)  
5. PredictionState snapshot rules (derive first, store second)  
6. Relationship to legacy `ReadinessService` / analytics (convergence path; no third formula)  
7. Explicit non-goals: no Twin writes, no Decision selection, no mission generation, no scoring formulas in the first structural pass if beliefs remain empty  

## 15.2 Educational design recommendations

1. Treat factor **disagreement** as a feature — preserve High Knowledge + Low Memory style tensions.  
2. Prefer “unknown / low warrant” over fake Mid scores.  
3. Keep Assessment Performance distinct from Behaviour Reliability in every student-facing readiness narrative.  
4. Keep Confidence out of readiness v1 unless explicitly provisional and lower-warrant than Performance.  
5. Do not deepen TopicProgress-based readiness formulas while Twin-first aggregation lands.

## 15.3 Midpoint conditions acknowledged

This analysis accepts and encodes the Epic 2 Midpoint Review conditions:

- Cold-start / empty-belief contract  
- No parallel authority / third formula  
- Confidence separability  
- Write/read firewall  
- Curriculum V1/V2 invariants  
- Documentation hygiene remains a follow-up for kickoff/status tables (outside this analysis file’s educational charter, but required before or with 2.7 architecture kickoff)  
- Registration-order stability for Twin writes remains upstream of readiness (K→M→B→P)

## 15.4 Architecture compliance checklist

| Invariant | Status for Readiness analysis |
|---|---|
| Twin is sole educational-state authority | Readiness consumes Twin; does not fork beliefs |
| Evidence is only legitimate belief input | Readiness never owns evidence |
| Strategies own domain evolution | Readiness is not a write strategy |
| Activity ≠ readiness; Confidence ≠ mastery; Behaviour ≠ learning | Binding |
| Readiness ≠ Decision; Readiness ≠ Missions | Binding |
| V1/V2 curriculum compatibility | Required going forward; no traversal changes in this milestone |
| No implementation in this milestone | Satisfied |

## 15.5 Explicit stop line

This milestone delivers **analysis only**.

**Do not proceed in this milestone to:** code, dataclasses, services, tests, database changes, scoring formulas, Decision Engine design detail, or UI.

**Next engineering step (separate milestone):** Capability 2.7 Readiness Aggregation architecture note → structural read-side contracts → implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Readiness in the capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot is the read input; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains Readiness consumes without modification |
| **2.7** | **Readiness Aggregation** | **This analysis precedes architecture and implementation** |
| 2.8 | Decision Engine | Consumes readiness context; owns next-action selection |
| 2.9 | Explainable Recommendation Engine | Packages Decision output; may cite readiness factors |
| 2.10 | Mission Generation Intelligence | Depends on Decision Engine, not Readiness directly |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.7.1 — Readiness Educational Analysis |
| Nature | Architecture / educational analysis only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required going forward; analysis introduces no traversal changes |
| Application code intentionally untouched | Yes |
| Midpoint gate | APPROVED WITH CONDITIONS — conditions encoded herein |
| Next | Capability 2.7 Readiness Aggregation architecture note (separate milestone) |

---

*End of Capability 2.7.1 Readiness Educational Analysis.*
