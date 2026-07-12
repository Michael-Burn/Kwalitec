# Capability 2.8.2 — Decision Engine Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.8 Decision Engine (architecture preceding structural contracts and implementation)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Educational charter:** [`CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md)  
**Upstream gate:** Readiness Architecture Review — APPROVED WITH CONDITIONS ([`docs/reviews/READINESS_ARCHITECTURE_REVIEW.md`](../reviews/READINESS_ARCHITECTURE_REVIEW.md))  
**Companions:** [`CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md`](CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md)  
**Scope:** Structural architecture for next-action selection — **no code, algorithms, scoring, optimization formulas, services, tests, schemas, or migrations**

---

## Document purpose

This milestone answers **how** the Decision Engine is structured as architecture after Capability 2.8.1 approved **what** it is educationally.

Readiness Aggregation supplies factorable preparedness context. Decision Engine is Epic 2’s authoritative **next-action reasoner**: it selects the highest-value learning action from Twin-backed educational state, CurriculumContext, Goals, Constraints, and ReadinessState — without mutating Twin beliefs, recomputing readiness, packaging recommendations, or composing missions.

This note locks structural contracts so later milestones can add read-side artefacts and selection behaviour without inventing syllabus, coercing unknown readiness, or forking a parallel learner-state store.

**Non-goals of this document**

- Code, pseudocode algorithms, package layouts, or dataclass definitions  
- Database schemas, Alembic migrations, or ORM layouts  
- Scoring functions, ranking formulas, optimization objectives, or Bayesian selection math  
- UI redesign, gamification, dashboards, notifications, or social features  
- Explainable Recommendation Engine or Mission Generation design beyond consumption / projection boundaries  
- Replacement of Curriculum Engine, Evidence Model, Twin aggregate, Readiness Aggregation, or Twin Update Pipeline contracts  

**Hard architectural rules (binding):**

1. Decision Engine never writes Learning Evidence as belief authority.  
2. Decision Engine never mutates Twin belief domains.  
3. Decision Engine never invents curriculum identities, weights, or order.  
4. Decision Engine never recomputes a competing readiness truth.  
5. Decision Engine never coerces unknown / low-warrant / `not_yet_knowable` into Mid or High preparedness.  
6. Every Decision must carry reason codes, a candidate set, and lineage hooks.  
7. Curriculum V1 and V2 remain loadable; weights and order come only from canonical Curriculum helpers.

**Governing principle:** Readiness is derived and factorable; Decision Engine selects next action — explainably, deterministically in the core path, and without engagement theatre.

---

# 1. DecisionState / Decision model

## 1.1 Position

A **Decision** is the authoritative output of the Decision Engine for a given input snapshot.

**Decision State** is the materialised decision context / audit artefact produced from Decision outcomes (and later accept/dismiss lineage). Decision State closes the loop so future Behaviour and Decision Engine runs can respect history without inventing Twin beliefs.

```
CurriculumContext + Goals + Constraints
        +
Digital Twin domains (Knowledge · Memory · Behaviour · Performance · …)
        +
ReadinessState          (preparedness context)
        +
Prior Decision State / Decision Journal (optional history context)
        ↓
Decision Engine         (read-side next-action selection)
        ↓
Decision                (selected action + candidates + reason codes + lineage)
        ↓
Decision State          (materialised audit / journal linkage)
        ↓
Recommendation / Mission projections (Capabilities 2.9 / 2.10)
```

## 1.2 Architectural classification

| Kind | Role |
|---|---|
| **Decision** | Live selection result for one evaluation — the Decision Engine’s primary output |
| **Decision State** | Persisted or snapshotable decision context for audit, thrashing control, and lineage |
| **Not a write-path Twin belief domain** | No Update Strategy evolves Decision from evidence as mastery/retention |
| **Not educational-state authority** | Twin domains remain sole authority for beliefs; Decision is a read-side choice |
| **Consequence of intelligence** | Plans and missions consume Decisions; they do not replace them |

Naming note: Educational Intelligence Architecture lists Decision State among Twin-adjacent educational concerns. Architecturally, that means decision *outputs and history* may sit beside Twin snapshots for audit — not that Decision Engine is a write-path belief strategy.

## 1.3 Architectural properties

| Property | Requirement |
|---|---|
| **Read-side** | Produced by reasoning over Twin + Curriculum + Goals + Constraints + ReadinessState |
| **Action-selecting** | Chooses a next learning action; may surface ordered alternatives |
| **Deterministic core** | Same inputs → same Decision in the core educational path |
| **Explainable** | Reason codes + candidates + lineage are mandatory |
| **Curriculum-bound** | Curriculum-scoped actions use official syllabus identities only |
| **Warrant-honest** | Citations of readiness inherit Evidence Warrant; unknown stays unknown |
| **Immutable per evaluation** | One evaluation yields one Decision for that input set; Twin updates require a new evaluation |
| **Non-authoritative for beliefs** | Accepting a Decision does not grant mastery; completion / assessment evidence does |

## 1.4 Conceptual shape — Decision (contract, not schema)

| Slot | Architectural role |
|---|---|
| **Scope identity** | Student / curriculum / sitting (Goal) the Decision applies to |
| **Selected action** | Canonical next learning action (§3) |
| **Candidate set** | Alternatives considered — required for “why not Y?” |
| **Reason codes** | Stable machine-readable educational justifications (§9) |
| **Value rationale hooks** | Attributable narrative inputs for why this maximises educational value *now* — not marketing copy |
| **Lineage references** | Hooks to Twin snapshot / domain factors / ReadinessState factors / Curriculum identities / evidence ids |
| **Constraint acknowledgements** | Which feasibility limits shaped or demoted the selection |
| **Evaluation context** | Curriculum format awareness (V1/V2), input snapshot identity, engine/version tags for audit |
| **Warrant posture** | Inherited honesty when readiness or Twin evidence density is low |

## 1.5 Conceptual shape — Decision State (contract, not schema)

| Slot | Architectural role |
|---|---|
| **Decision payload** | Selected action, candidates, reason codes, lineage (as of evaluation) |
| **Twin / readiness references** | Snapshot or derivation identities used as inputs |
| **Journal linkage** | Accept / dismiss / defer outcomes when recorded |
| **Temporal identity** | When the Decision was produced; supersession relative to later Decisions |
| **Consumer projections** | Optional hooks to Recommendation / Mission artefacts that projected this Decision |

Decision State answers: *What was decided, among which candidates, with which reasons, and what happened next?*

It intentionally does **not** answer: *What does the student know?* or *How prepared are they overall?*

## 1.6 What Decision / Decision State are not

- A readiness score or factor recomputation  
- A Knowledge / Memory / Behaviour / Performance belief store  
- A Recommendation title or UI package  
- A Mission / MissionTask list  
- A WeekPlan  
- A parallel mastery map inside missions or journals  
- A black-box coach utterance without reason codes  

## 1.7 Ownership

| Concern | Owner |
|---|---|
| Producing Decision | Decision Engine (Capability 2.8) |
| Materialising Decision State from Decision + journal | Decision Engine outcomes + product recording paths (architecture ownership of selection remains 2.8) |
| Twin belief domains used as inputs | Knowledge / Memory / Behaviour / Performance Update Strategies (write path) |
| Preparedness context | Readiness Aggregation (Capability 2.7) |
| Syllabus identities and weights | Curriculum Engine / CurriculumService helpers |
| Packaging for product surfaces | Explainable Recommendation Engine (2.9) |
| Session/day task projection | Mission Generation Intelligence (2.10) |
| Selecting next action | **Decision Engine only** |

---

# 2. Decision inputs

## 2.1 Input principle

Decision Engine **consumes** educational context. It **never modifies** Twin domains or readiness beliefs. Same inputs in → same Decision out (deterministic core).

## 2.2 Primary input catalogue

| Input | Architectural role | Authority |
|---|---|---|
| **Twin snapshot** | Educational beliefs and structural slots for Knowledge, Memory, Behaviour, Performance (and Confidence when available) | Twin is sole educational-state authority |
| **ReadinessState** | Factorable preparedness context: factors, attributions, Evidence Warrant, cold-start / `not_yet_knowable`, disagreement | Readiness Aggregation — context only |
| **CurriculumContext** | Official syllabus identities, canonical order, exam weights (V1/V2) | Curriculum Engine via canonical helpers |
| **Goals** | Active paper/sitting, ambition, deadline, committed capacity | Goals — destination and capacity bound |
| **Constraints** | Session feasibility: available time now, sustainable intensity, Behaviour sustainability / burnout flags, operational limits | Feasibility bound — demotes ambition; does not invent educational need |
| **Decision history** | Prior Decision State / Decision Journal accept/dismiss lineage | Context against thrashing; dismiss ≠ mastery |

## 2.3 How Twin domains are consumed (read-only)

| Twin concern | Decision use |
|---|---|
| **Knowledge** | Gaps / weak mastery on weighted identities → study / coverage-shaped candidates |
| **Memory** | Stale high-value retention → revise-shaped candidates |
| **Performance** | Assessment weakness / thin warrant → diagnostic or exam-condition rehearsal candidates |
| **Behaviour** | Consistency and sustainability → feasibility constraints and intensity demotion |
| **Confidence (when available)** | Over/under-confidence vs Performance → risk framing only; never upgrades mastery or readiness |
| **Decision State history** | Prior selections and responses → avoid thrashing; respect revealed preference without treating dismiss as mastery |

## 2.4 Input contract (binding)

1. **ReadinessState is context only** — never an action selector, never a mission generator, never coerced from unknown to Mid/High.  
2. **CurriculumContext is built via canonical Curriculum helpers** — no parallel weights or order inside Decision Engine.  
3. **Goals define the educational destination** — sitting and capacity bound value; Goals alone never invent Twin beliefs.  
4. **Constraints bound ambition** — they do not erase high-weight educational risk.  
5. **Evidence Warrant must flow end-to-end** — reason codes that cite readiness inherit warrant honesty.  
6. **No legacy TopicProgress hybrid truth** — do not average legacy readiness percentages with Twin factors as temporary authority.  
7. **Sparse Twin → honest selection posture** — prefer evidence-creating actions; do not invent High-value polish on empty beliefs.  
8. **Prediction snapshots (when present)** are not live selection authority — Decision may consume them only as non-authoritative context after derive-first readiness/prediction rules.

## 2.5 What is not an input authority

- UI streak counters as educational value  
- Mission completion counts as mastery proof  
- Self-report Confidence as Assessment Performance  
- Coach/LLM free-text topic invention  
- Legacy `ReadinessService` overall % as Twin-first authority  
- Recommendation packaging layers inventing private ranks  

---

# 3. Candidate action representation

## 3.1 Purpose

A **candidate action** is a structured alternative the Decision Engine considers before selecting. The **candidate set** is mandatory for explainability: every core Decision must support “why this, not that?”

## 3.2 Conceptual shape (contract, not schema)

| Slot | Architectural role |
|---|---|
| **Action type** | Educational action family (study / revise / assess / diagnostic / rest-or-protect-intensity / other declared families) |
| **Curriculum scope** | Canonical topic / section / LO identity when applicable — never free-text syllabus invention |
| **Intent toward Goal** | Which educational tension the candidate addresses (coverage gap, retention risk, assessment warrant, feasibility protection, …) |
| **Feasibility envelope** | Session-length / intensity fit relative to Constraints |
| **Attribution hooks** | Twin / Readiness / Curriculum factors that nominated this candidate |
| **Status in set** | Selected / considered-not-selected / demoted-by-constraint / blocked (e.g. prerequisite context when available) |

## 3.3 Action-type families (architectural catalogue)

| Family | Educational meaning | Typical nominating signals |
|---|---|---|
| **Study / coverage** | Build Knowledge on underserved weighted identities | Knowledge gaps; Curriculum Coverage risk |
| **Revise / reinforce** | Restore Memory Stability on stale high-value identities | Memory staleness; High Knowledge + Low Memory disagreement |
| **Assess / exam-condition** | Create or strengthen Performance evidence under assessment conditions | Thin Assessment Performance warrant; Behaviour strong / Performance weak |
| **Diagnostic / evidence-creating** | Reduce uncertainty when warrant is low | Cold start; `not_yet_knowable`; sparse Twin |
| **Rest / protect intensity** | Protect learning sustainability when Behaviour / capacity flags risk | Burnout / feasibility constraints without erasing educational need |

Exact enums and naming may refine in implementation; the **separations** are binding. Collapsing revise into study, or rest into “do nothing without reason,” is forbidden.

## 3.4 Candidate set principles (binding)

1. **Candidate set is required** on the core educational path — opaque single-action output without alternatives is forbidden.  
2. **Candidates are curriculum-bound** when they name syllabus work.  
3. **Demotion is visible** — constraint demotion remains in the set with acknowledgement, not silent deletion of educational need.  
4. **Selection without nomination narrative is forbidden** — selected action must appear in (or be explicitly derived from) the considered set.  
5. **Batches (future)** may order multiple selected actions for a session window; Mission Intelligence still projects; ownership of selection unchanged.

## 3.5 What a candidate is not

- A Recommendation title or urgency badge  
- A MissionTask row  
- A mastery belief  
- A readiness factor  
- An LLM-invented topic  

---

# 4. Decision evaluation pipeline

## 4.1 Position

The evaluation pipeline is the **architectural sequence** of read-side stages that turn inputs into a Decision. It is a structural contract — not an algorithm, scoring function, or optimization solver.

## 4.2 Pipeline stages (architectural)

```
1. Assemble inputs
        ↓
2. Validate / scope (Goal sitting, CurriculumContext, Twin snapshot identity)
        ↓
3. Interpret readiness context (factors, warrant, cold-start, disagreement — context only)
        ↓
4. Nominate candidate actions (Twin + Curriculum value tensions + feasibility envelopes)
        ↓
5. Apply educational priority ordering (§8) and constraint handling (§6)
        ↓
6. Select action + retain candidate set
        ↓
7. Author reason codes + lineage hooks + constraint acknowledgements
        ↓
8. Emit Decision (→ optional Decision State materialisation)
```

## 4.3 Stage responsibilities

| Stage | Owns | Must not |
|---|---|---|
| **Assemble inputs** | Gather Twin, ReadinessState, CurriculumContext, Goals, Constraints, history | Mutate Twin; invent Curriculum |
| **Validate / scope** | Ensure sitting / curriculum identity coherence; V1/V2 format awareness | Invent Mid readiness when sparse |
| **Interpret readiness** | Use factors/warrant/disagreement as context | Select actions; coerce unknown → Mid/High |
| **Nominate candidates** | Produce curriculum-bound alternatives with attribution hooks | Invent topics; treat streaks as value |
| **Order / constrain** | Apply educational priority posture and feasibility demotion | Erase high-weight need via feasibility alone |
| **Select** | Choose highest-value feasible action | Opaque selection without candidates/reasons |
| **Author reasons** | Emit stable reason codes + lineage | Invent evidence or disagree with inputs |
| **Emit** | Decision (+ Decision State materialisation hooks) | Write Twin beliefs; generate missions |

## 4.4 Pipeline properties (binding)

1. **Read-only** with respect to Twin beliefs and Evidence-as-authority.  
2. **Deterministic** in the core path.  
3. **Explainable by construction** — reason codes and candidates are outputs of the pipeline, not post-hoc decoration.  
4. **Formula-deferred** — this architecture locks stage ownership, not numeric selection math.  
5. **No LLM ownership** of stages 4–6; generative assistance may narrate chain-supported reasons only after Decision emission.

## 4.5 Explicit non-pipeline concerns

- Twin Update Pipeline (write path)  
- Readiness Aggregation derivation (upstream producer of ReadinessState)  
- Recommendation packaging (2.9)  
- Mission composition (2.10)  
- Accept/dismiss UX  

---

# 5. Readiness interaction

## 5.1 Boundary

| Capability | Question | Ownership |
|---|---|---|
| **Readiness Aggregation** | Are we on track for the sitting? | Preparedness judgement |
| **Decision Engine** | What should we do next? | Next-action selection |

Same Twin snapshot; different questions; different owners.

## 5.2 How Decision Engine consumes ReadinessState

| Readiness signal | Architectural use |
|---|---|
| Time / goal pressure + weak Assessment Performance on high-weight areas | Prefer high-value remediation or exam-condition candidates |
| High uncertainty / cold start / `not_yet_knowable` | Prefer diagnostic / evidence-creating actions |
| Strong Knowledge / Performance with weak Memory Stability | Prefer revision-shaped actions on high-weight stale topics |
| Strong Behaviour Reliability with thin Performance warrant | Prefer assessment-shaped actions within feasible intensity |
| Fragile Behaviour Reliability near the sitting | Constrain intensity / protect sustainability — without erasing Performance evidence |
| Factor disagreement | Preserve tension in reason codes — do not average away |
| Evidence Warrant | Inherit honesty into any readiness-citing reason code |

## 5.3 Firewall (binding — Readiness Architecture Review)

1. Decision Engine consumes `ReadinessState` as **context only**.  
2. Decision Engine never asks readiness to select actions or generate missions.  
3. Decision Engine never coerces unknown / low-warrant / `not_yet_knowable` into Mid or High preparedness.  
4. Decision Engine never product-narrates structural “supportive” Knowledge Strength as exam readiness.  
5. If a design needs “readiness said do X,” that design is wrong.

## 5.4 What Readiness does not decide

- Topic selection  
- Action type  
- Session composition  
- Accept/dismiss handling  
- Plan or mission regeneration  

**Readiness informs decisions; it never chooses actions.**

---

# 6. Constraint handling

## 6.1 Definition

**Constraints** are feasibility limits on ambition: available time now, session length, sustainable intensity, Behaviour sustainability / burnout flags, and capacity implied by Goals.

Constraints answer: *What intensity and scope can this student sustainably attempt now?*  
They do **not** answer: *What educational risk exists?*

## 6.2 Architectural role

| Role | Meaning |
|---|---|
| **Ambition bound** | Demote or reshape candidates that exceed feasible intensity |
| **Visibility** | Demotions appear as constraint acknowledgements and candidate status — not silent erasure |
| **Non-erasure of need** | High-weight educational risk remains visible even when the selected action is gentler |
| **Rest legitimacy** | Rest / protect-intensity is a first-class action family when sustainability risk dominates |

## 6.3 Constraint principles (binding)

1. Constraints **bound ambition**; they do not invent educational need.  
2. Constraints **do not erase** high-weight curriculum risk — they change how aggressively the Decision pursues it.  
3. Behaviour sustainability is a **feasibility** signal, not a learning-value signal.  
4. Goals capacity and session time participate as constraints, not as Twin beliefs.  
5. Unsustainable cram selections that Behaviour says will fail are architectural failures even if curriculum need is real.  
6. “Rest always” despite known high-weight exam risk is equally a fidelity failure — avoidance theatre.

## 6.4 Constraint acknowledgements in Decision output

Every Decision shaped by constraints must expose, conceptually:

- which constraint class applied;  
- which candidates were demoted or reshaped;  
- that educational need (if any) remains attributable in reason codes.

---

# 7. Curriculum interaction

## 7.1 Principle

Curriculum is the **only syllabus authority**. Decision Engine consumes `CurriculumContext`; it never invents parallel topic trees, weights, or order.

## 7.2 CurriculumContext responsibilities

| Responsibility | Owner |
|---|---|
| Topic / section / LO identities | Curriculum Engine |
| Canonical traversal order | `CurriculumService` helpers (e.g. ordered topics) |
| Exam weights (V1 flat / V2 hierarchical) | Canonical weight helpers |
| Prerequisite structure (when used) | Curriculum declarations — Decision consumes, does not invent |
| Format awareness (V1 vs V2) | CurriculumContext derivation — Decision remains format-agnostic at ownership level |

## 7.3 Decision Engine curriculum rules (binding)

1. Every curriculum-scoped selected action and candidate must use **canonical identities**.  
2. Educational value of syllabus slices comes from **official weights and remaining coverage**, not from UI popularity.  
3. **V1 and V2** must both remain loadable and traversable; Decision must not assume sections always exist.  
4. Decision Engine must not embed a private “priority topic list” that disagrees with CurriculumContext.  
5. Prerequisite blocking, when represented, is curriculum structure — not Twin mastery invention.

## 7.4 V1/V2 compatibility checklist

| Check | Requirement |
|---|---|
| Flat (V1) curricula | Decisions remain valid without section hierarchy |
| Hierarchical (V2) curricula | Weights/order via V2-aware helpers; no invented hierarchy |
| Nullable sections | Consumers tolerate absence |
| No parallel syllabus | Forbidden |
| No traversal redesign in this milestone | Compatibility preserved; no Curriculum Engine rewrite |

---

# 8. Educational priority ordering

## 8.1 Purpose

Educational priority ordering is the **architectural posture** for resolving competing learning-value tensions among candidates. It is **not** a scoring formula, weight vector, or optimization objective.

## 8.2 Priority posture (binding principles)

1. **Curriculum-weighted value** — high-weight weak areas outrank low-weight polish when time is scarce.  
2. **Evidence over assumption** — low warrant prefers evidence-creating actions over refinement theatre.  
3. **Learning over activity** — prefer actions that move Knowledge / Memory / Performance over empty completion.  
4. **Retention awareness** — overdue high-value Memory risk can outrank new low-weight coverage.  
5. **Assessment honesty** — thin Performance warrant elevates diagnostic / assessment-shaped candidates.  
6. **Feasibility** — Behaviour and capacity constrain ambition; burnout demotes intensity.  
7. **Disagreement preservation** — High Knowledge + Low Memory (and similar tensions) remain explicit in ordering rationale.  
8. **Confidence as risk framing only** — self-report never upgrades priority as if it were mastery or assessment.

## 8.3 Tension classes (architectural, not scores)

| Competing tension | Architectural preference posture |
|---|---|
| High-weight gap vs low-weight polish | Prefer high-weight educational need |
| New coverage vs stale high-weight retention | Prefer retention risk when Memory flags staleness on high-weight identities |
| Activity streaks vs missing assessment | Prefer assessment / diagnostic over polish rewarded by streaks |
| Educational need vs burnout | Prefer smaller high-value or protect-intensity action; keep need visible |
| Overconfidence vs weak Knowledge/Performance | Prefer diagnostic / structured learning; Confidence does not skip foundations |
| Cold start vs advanced rehearsal | Prefer evidence-creating actions |

## 8.4 Explicitly deferred

- Numeric weights among tension classes  
- Exact ranking / selection functions  
- Multi-objective solvers  
- Bayesian decision policies  

Ownership of any future numeric selection remains inside Decision Engine; Twin and Curriculum authority remain unchanged.

---

# 9. Reason code architecture

## 9.1 Definition

**Reason codes** are stable, machine-readable educational justifications authored by the Decision Engine. Recommendation packaging may narrate them; it must not invent competing codes that disagree with the Decision.

## 9.2 Architectural properties

| Property | Requirement |
|---|---|
| **Stable identity** | Codes are versionable vocabulary entries, not free-text slogans |
| **Educational meaning** | Each code maps to a named tension (weight, retention, assessment warrant, feasibility, cold start, …) |
| **Attributable** | Codes cite lineage hooks to Twin / Readiness / Curriculum / Constraints inputs |
| **Warrant-aware** | Codes that cite readiness inherit Evidence Warrant honesty |
| **Comparable** | Analytics may aggregate codes without opaque scores |
| **Non-marketing** | Codes are educational factors, not urgency stickers |

## 9.3 Conceptual catalogue families (illustrative — not exhaustive enums)

| Family | Educational meaning |
|---|---|
| **Curriculum weight** | Selection driven by official exam weight / coverage value |
| **Knowledge gap** | Selection driven by weak or absent mastery on scoped identity |
| **Retention risk** | Selection driven by Memory staleness / stability risk |
| **Assessment warrant gap** | Selection driven by thin or weak Performance evidence |
| **Time / goal pressure** | Selection shaped by remaining calendar / capacity context |
| **Feasibility demotion** | Selection reshaped by Constraints / Behaviour sustainability |
| **Cold-start / low warrant** | Selection prefers evidence-creating actions under uncertainty |
| **Factor disagreement** | Selection preserves explicit Twin/Readiness tension (e.g. knows-now / may-not-retain) |
| **History / anti-thrash** | Selection respects prior dismiss/accept lineage without treating dismiss as mastery |
| **Confidence risk framing** | Over/under-confidence noted as risk — never as mastery upgrade |

Exact code strings and versioning live in a later structural vocabulary milestone. Meanings and authorship ownership are binding now.

## 9.4 Authorship rules (binding)

1. **Decision Engine alone authors** reason codes for a Decision.  
2. **Recommendation Engine narrates**; it does not invent ranking codes that contradict the Decision.  
3. **LLM / coach may restate** chain-supported codes; they must not author selection.  
4. **Version codes additively** — preserve audit of older Decisions.  
5. **No opaque “recommended for you”** without at least one educational reason code on the core path.  
6. **Post-hoc stories that disagree with reason codes are forbidden.**

## 9.5 What reason codes are not

- Readiness factors (those belong to ReadinessState; Decision may *cite* them)  
- Recommendation titles  
- Mission task labels  
- Mastery scores  
- Engagement badges  

---

# 10. Explainability chain

## 10.1 Mandatory chain

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

## 10.2 Layer obligations

| Layer | Obligation |
|---|---|
| **Curriculum** | Cite official identity / weight / order context — never invented topics |
| **Evidence** | Cite evidence ids or honest aggregates when available |
| **Twin** | Cite domain factors that nominated candidates |
| **Readiness** | Cite factor posture + warrant when used; never narrate supportive Knowledge Strength as exam readiness |
| **Decision** | Cite reason codes, selected vs considered candidates, constraint acknowledgements |
| **Recommendation (2.9)** | Package the chain; must not invent disagreeing ranking |

## 10.3 Attribution requirements

1. Selected action cites reason codes tied to Twin / Readiness / Curriculum / Constraints inputs.  
2. Candidate set supports “why not the alternative?” without post-hoc invention.  
3. Warrant honesty appears whenever readiness or Twin evidence density is low.  
4. Explanations must not invent evidence, syllabus topics, or Twin beliefs.  
5. Accepting a Decision records preference / intent only — not mastery.  
6. Decision State and Decision Journal participate as audit artefacts, not as rewrite of Twin beliefs.

## 10.4 Forbidden explanation patterns

- Single opaque “recommended for you” without factors  
- Explanations that cite UI labels but not Twin/evidence  
- LLM-generated rationales that invent evidence or topics  
- Narrating supportive Knowledge Strength as “you are exam ready”  
- Averaging away High Knowledge + Low Memory tension into a bland Mid story  
- Treating dismissals as proof the topic is mastered  
- Recommendation copy that disagrees with Decision reason codes  

## 10.5 Audit artefacts

| Artefact | Role |
|---|---|
| Learning Evidence log | Immutable history |
| Twin snapshot / domain evidence ids | State lineage |
| ReadinessState attributions + warrant | Preparedness context lineage |
| Decision / Decision State | Candidates + selected action + reason codes |
| Decision Journal | User response to recommendations |
| Recommendation / Mission projections | Product consequences — not authority |

---

# 11. Cold-start behaviour

## 11.1 Definition

Cold start is the educational situation where Goals (and possibly CurriculumContext) exist, but Twin domains are thin, Readiness overall is `not_yet_knowable` / low Evidence Warrant, and the system lacks honest support for refinement or exam-polish narratives.

## 11.2 Architectural posture (binding)

1. Prefer **evidence-creating** actions (diagnostics, early assessments, structured first coverage of high-weight areas).  
2. **Never coerce** unknown / low-warrant / `not_yet_knowable` into Mid or High preparedness to justify advanced polish.  
3. Reason codes must state **insufficient warrant** honestly.  
4. Candidate sets should still exist — including demoted polish candidates with visible “not yet warranted” status when useful for explainability.  
5. Cold-start Decisions remain **curriculum-bound** (high-weight first coverage) rather than random activity fillers.

## 11.3 Forbidden cold-start behaviours

- Inventing Mid readiness to unlock “exam rehearsal only”  
- Recommending polish because streaks or empty missions look tidy  
- Treating absence of Memory as “fully retained”  
- Treating absence of Performance as “exam ready”  
- Hybrid-averaging legacy TopicProgress % into a fake Twin-first warrant  

## 11.4 Relationship to Readiness cold-start

Readiness Aggregation owns honest `not_yet_knowable` / warrant postures. Decision Engine **inherits** those postures as context and translates them into selection posture — it does not redefine preparedness.

---

# 12. Legacy convergence

## 12.1 Current legacy posture

Product-facing ancestors (`RecommendationService`, TopicProgress-based readiness composites, related planning consumers) currently provide next-action and readiness-like signals without Twin-first Decision authority.

## 12.2 Convergence principle (binding)

Epic 2 requires Decision Engine to become the **authoritative next-action reasoner**, with Twin-first inputs. Migration is **additive**: preserve behaviour where needed, redirect authority, retire divergent selection truth. Do **not** deepen legacy ranking formulas while Twin-first Decision contracts land. Do **not** hybrid-average legacy % with Twin factors as temporary authority.

## 12.3 Convergence path (architectural stages)

| Stage | Meaning |
|---|---|
| **A — Coexistence** | Legacy recommenders continue for product surfaces; Decision Engine architecture and contracts land without claiming cutover |
| **B — Adapter** | Adapters expose Decision outputs beside legacy ranks; dual truth is explicit and temporary |
| **C — Twin-first Decision authority** | New Educational Intelligence paths consume Decision Engine; legacy ranks cease to be selection authority |
| **D — Retire divergent math** | Remove or quarantine legacy selection formulas that disagree with Twin-first Decision |

## 12.4 Adapter rules during coexistence

1. Adapters must not silently rewrite Twin beliefs.  
2. Adapters must not present legacy overall % as Twin-first readiness or Decision authority.  
3. Dual truth must be **named** in architecture/docs during coexistence — not papered over as one score.  
4. Recommendation packaging (2.9) must eventually package Decision, not invent a third ranker.  
5. Mission generation (2.10) must eventually project Decision, not legacy private priority scores as mastery.

## 12.5 Explicit non-goals of this milestone

- Implementing adapters  
- Cutting over UI  
- Deleting `RecommendationService`  
- Deepening TopicProgress recommendation math  
- Schema for Decision State persistence  

---

# 13. Risks

| Risk | Architectural impact | Mitigation |
|---|---|---|
| **Readiness → Decision conflation** | Wrong owner; readiness becomes hidden action selector | Strict firewall; consume `ReadinessState` as context only |
| **Opaque Decision Engine** | Product thesis failure; untrustable next-action advice | Mandatory reason codes + candidate set + explainability chain |
| **Coercing unknown readiness** | False preparedness; dishonest diagnostics avoidance | Inherit warrant; prefer evidence-creating actions under cold start |
| **Activity theatre in selection** | Missions/completions preferred over Knowledge/Memory/Performance movement | Learning-over-activity principle; Behaviour is feasibility, not value |
| **Confidence contamination** | Self-report drives action as if mastery/assessment | Confidence risk-framing only; no Knowledge-held confidence as calibrated Confidence |
| **Curriculum invention** | Parallel topic trees; V1/V2 breakage | `CurriculumContext` via canonical helpers only |
| **Legacy dual authority** | `RecommendationService` / TopicProgress ranks disagree with Twin-first Decision | Additive convergence; no hybrid average as temporary truth |
| **Recommendation invents ranking** | Packaging layer becomes secret Decision Engine | 2.9 packages only; must not contradict reason codes |
| **Mission rows as mastery** | Stale private state; broken audit | Missions are projections only |
| **LLM ownership creep** | Non-determinism; invented syllabus/evidence | Coach narrates; Decision Engine selects |
| **Premature scoring / optimization** | Unmaintainable math before educational contracts mature | Structural contracts first; defer formulas |
| **Ignoring constraints** | Unsustainable plans; burnout; dismiss thrashing | Constraints demote intensity; record feasibility in reasons |
| **Constraints erase need** | Feasibility used to delete high-weight risk | Constraints bound ambition; keep need visible in reason codes |
| **Thrashing / preference blindness** | Re-recommend dismissed actions without lineage | Consume Decision history; dismiss ≠ mastery |
| **Parallel learner-state stores** | Divergent “next topic” truths | Twin + Decision as authority; services consume |
| **Overall readiness ceiling misunderstanding** | Waiting for a green overall before deciding | Structural readiness may lack overall “ready”; Decision reasons from factors + warrant |

---

# 14. Extensibility

## 14.1 Extension points

| Future capability | How it extends without breaking architecture |
|---|---|
| **Numeric / structured selection functions** | Live inside Decision Engine ownership; remain deterministic and explainable; still consume Twin/Readiness/Curriculum/Goals/Constraints — never fork Twin beliefs |
| **Richer reason-code vocabulary** | Version codes additively; preserve audit of older Decisions |
| **Confidence calibration domain** | Supplies calibrated over/under-confidence as explicit Decision risk inputs; still never mutates Confidence from Decision |
| **Pass-probability / Prediction context** | Decision may consume Prediction snapshots as non-authoritative context after derive-first rules — not as a competing selector |
| **Multi-action session batches** | Decision Engine may emit an ordered batch for a window; Mission Intelligence still projects; ownership of selection unchanged |
| **Personalisation from Decision Journal** | Accept/dismiss evidence informs Behaviour and future candidate preference — via Evidence → Strategies, not silent Decision-side mutation |
| **Insight / AI Coach** | Reads Decision + explanation chain; never silent Twin writes; never owns selection |
| **Institutional overlays** | Observe Decisions; do not fork student-owned Twin or invent syllabus |
| **Prerequisite-aware nomination** | Consume Curriculum prerequisite structure; do not invent Twin mastery from blocking |

## 14.2 Compatibility guarantees to preserve

1. Decision Engine remains the only next-action selector.  
2. Readiness remains preparedness judgement only.  
3. Twin remains sole educational-state authority.  
4. Curriculum V1 and V2 remain loadable; weights/order via canonical helpers.  
5. Evidence append-only semantics remain permanent.  
6. Deterministic cores remain free of required network LLM calls.  
7. Missions remain projections of Decisions, not of raw readiness scores.  
8. Recommendations remain packaging of Decisions, not competing rankers.

## 14.3 Deliberately unlocked

Not locked by this architecture beyond ownership:

- Exact selection / ranking function  
- Numeric weights among reason factors / tension classes  
- Optimization formulations  
- Bayesian decision policies  
- Full Decision / Decision State persistence schema  
- Recommendation packaging schemas  
- Mission batching algorithms  
- Exact reason-code string vocabulary  

---

# 15. Recommendations

## 15.1 Implementation sequence (separate milestones)

1. **Structural read-side contracts** — Decision / candidate / reason-code / lineage shapes (still no scoring formulas).  
2. **CurriculumContext builder** — thin orchestration using canonical Curriculum helpers before production wiring.  
3. **Decision evaluation skeleton** — assemble inputs → nominate → constrain → select → author reasons; cold-start honesty first.  
4. **Consumer wiring** — Recommendation (2.9) packaging and Mission (2.10) projection boundaries.  
5. **Decision State materialisation** — audit / journal linkage without Twin mutation.  
6. **Legacy convergence stages** — adapters → Twin-first Decision authority → retire divergent math.  
7. **Numeric / structured selection enrichment** — only after structural honesty, candidate sets, and warrant handling are proven.

## 15.2 Binding design recommendations

1. Keep **Decision** named as read-side selection output; keep **Decision State** as audit materialisation — not a write-path Twin peer to Knowledge.  
2. Require **candidate sets** from the first structural pass.  
3. Treat factor **disagreement** as Decision information — preserve High Knowledge + Low Memory style tensions in reason codes.  
4. Prefer diagnostic / evidence-creating actions under low warrant over fake Mid confidence in selection.  
5. Keep Assessment-shaped needs distinct from Behaviour feasibility in every Decision narrative hook.  
6. Keep Constraints as ambition bounds, not as erasers of high-weight educational risk.  
7. Obtain all weights/order via **canonical Curriculum helpers**.  
8. Do not deepen legacy recommendation ranking while Twin-first Decision contracts land.  
9. Encode Readiness Architecture Review conditions as Decision input invariants before any production wiring.  
10. Omit calibrated Confidence domain as a blocker — risk-framing stance is enough to start.  
11. Never generate missions from readiness directly.  
12. Never let Recommendation packaging invent ranking that disagrees with Decision reason codes.

## 15.3 Upstream conditions acknowledged

This architecture accepts and encodes the Readiness Architecture Review conditions relevant to 2.8:

- `ReadinessState` as context only  
- Evidence Warrant end-to-end  
- No legacy TopicProgress hybrid truth  
- `CurriculumContext` via canonical helpers  
- No product narration of supportive Knowledge Strength as exam readiness  
- Confidence omitted from readiness; not reused as Decision mastery proxy  
- Prediction snapshots (when present) are not live selection authority  
- Documentation convergence for subsystem docs remains a follow-up outside this architecture charter  

Also retains Epic 2 Midpoint conditions still in force: write/read firewall, no parallel learner-state forks, Confidence separability before rich risk framing, V1/V2 invariants.

## 15.4 Architecture compliance checklist

| Invariant | Status for this architecture |
|---|---|
| Twin is sole educational-state authority | Decision consumes Twin; does not fork beliefs |
| Evidence is only legitimate belief input | Decision does not mutate beliefs; outcomes become evidence via recording paths |
| Strategies own domain evolution | Decision is not a write strategy |
| Readiness ≠ Decision; Decision ≠ Recommendation packaging; Decision ≠ Missions | Binding |
| Activity ≠ learning value; Confidence ≠ mastery; Behaviour ≠ learning | Binding |
| Curriculum V1/V2 compatibility | Required; CurriculumContext via canonical helpers |
| No LLM ownership of core selection | Binding |
| No implementation / algorithms / scoring in this milestone | Satisfied |

## 15.5 Explicit stop line

This milestone delivers **architecture only**.

**Do not proceed in this milestone to:** code, algorithms, scoring, optimization, dataclasses, services, tests, database changes, Recommendation packaging design detail, Mission generation design detail, or UI.

**Next engineering step (separate milestone):** structural read-side contracts and/or implementation plan for Capability 2.8 — then implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot is the read input; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains Decision consumes without modification |
| 2.7 | Readiness Aggregation | Supplies `ReadinessState` context; firewall preserved |
| **2.8.1** | **Decision Engine Educational Analysis** | Approved educational charter this architecture implements structurally |
| **2.8.2** | **Decision Engine Architecture** | **This document** |
| 2.9 | Explainable Recommendation Engine | Packages Decision output; must not invent ranking |
| 2.10 | Mission Generation Intelligence | Projects Decision output into daily structure |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.8.2 — Decision Engine Architecture |
| Nature | Architecture only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required; no traversal changes introduced |
| Application code intentionally untouched | Yes |
| Upstream gate | Readiness Architecture Review — APPROVED WITH CONDITIONS — conditions encoded herein |
| Prior | Capability 2.8.1 — Decision Engine Educational Analysis (approved) |
| Next | Structural contracts / implementation plan (separate milestone) — not started here |

---

*End of Capability 2.8.2 Decision Engine Architecture. STOP.*
