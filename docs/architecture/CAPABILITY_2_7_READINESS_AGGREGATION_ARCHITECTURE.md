# Capability 2.7.2 — Readiness Aggregation Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.7 Readiness Aggregation (architecture preceding structural contracts and implementation)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Educational charter:** [`CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md)  
**Gate:** Epic 2 Midpoint Architecture Review — APPROVED WITH CONDITIONS ([`docs/reviews/EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md`](../reviews/EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md))  
**Companions:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md), Capability 2.5 / 2.6 update-strategy architectures, [`knowledge/subsystems/readiness.md`](../../knowledge/subsystems/readiness.md)  
**Scope:** Read-side aggregation architecture for sitting preparedness — **no code, dataclasses, services, tests, schemas, migrations, or scoring formulas**

---

## Document purpose

This milestone answers **how** Readiness Aggregation is structured as architecture after Capability 2.7.1 approved **what** Readiness is educationally.

Knowledge, Memory, Behaviour, and Performance exist as Twin write-path domains. Readiness is the first Epic 2 **reasoning** capability: a derived, factorable preparedness judgement computed on read from Twin + Curriculum + Goals. This note locks contracts so a later implementation can build aggregation without inventing beliefs, mutating Twin domains, selecting next actions, or forking a third readiness formula beside the Twin and legacy analytics.

**Non-goals of this document**

- Code, pseudocode algorithms, package layouts, or dataclass definitions  
- Database schemas, Alembic migrations, or ORM layouts  
- Concrete readiness weights, averages, composites, pass-probability formulas, or Bayesian math  
- UI redesign, analytics dashboards as a second intelligence layer, gamification, or notifications  
- Decision Engine, Recommendation Engine, or Mission Generation design beyond consumption boundaries  
- Replacement of Curriculum Engine, Evidence Model, Twin aggregate, or Twin Update Pipeline contracts  

**Hard architectural rules (binding):**

1. Readiness Aggregation never writes Learning Evidence.  
2. Readiness Aggregation never mutates Twin belief domains.  
3. Readiness Aggregation never invents preparedness from absence.  
4. Readiness Aggregation never selects next actions or generates missions.  
5. Every overall readiness claim must decompose into named factors with explicit Evidence Warrant.  
6. Curriculum V1 and V2 remain loadable; weights and order come only from canonical Curriculum helpers.

**Governing principle:** Readiness is derived, factorable, and honest under uncertainty — not a write-side belief store and not a next-action engine.

---

# 1. ReadinessState

## 1.1 Position

`ReadinessState` is the **derived educational judgement** produced by Readiness Aggregation.

It answers:

> **How prepared is the student for the target sitting, given syllabus weight, Twin educational state, and remaining time?**

It sits on the **read path**, not beside Knowledge / Memory / Behaviour / Performance as a write-path domain evolved by Update Strategies.

```
Curriculum + Goals
        +
Digital Twin domains (Knowledge · Memory · Behaviour · Performance · …)
        ↓
Readiness Aggregation
        ↓
ReadinessState          (derived judgement — this capability’s output)
        ↓
Decision Engine / Analytics / optional Prediction snapshot
```

## 1.2 Architectural classification

| Kind | Role of ReadinessState |
|---|---|
| **Derived (read-side)** | Primary nature — computed from a Twin snapshot plus Curriculum and Goals |
| **Not a write-path Twin domain** | No Update Strategy owns ReadinessState evolution from evidence |
| **Optionally snapshotable** | A copy may be persisted via the Prediction path after derivation (§11) |
| **Not educational-state authority** | Twin domains remain sole authority for beliefs; ReadinessState is a lens |

Naming note: Educational Intelligence Architecture diagrams may show Readiness near Twin domains. Architecturally, that means readiness *outputs* may appear in Twin-adjacent Prediction slots — not that Readiness is a primary evidence-backed write domain.

## 1.3 Architectural properties

| Property | Requirement |
|---|---|
| **Derived** | Exists only as the result of aggregation over Twin + Curriculum + Goals |
| **Factorable** | Always carries named factors; never an opaque composite alone |
| **Deterministic core** | Same Twin snapshot + same Curriculum + same Goals → same factor attributions and overall judgement posture |
| **Warrant-aware** | Carries explicit Evidence Warrant / Uncertainty as a first-class dimension |
| **Curriculum-relative** | Preparedness is always against official syllabus weight and sitting Goals |
| **Immutable per derivation** | A derivation yields a judgement for that input snapshot; later Twin updates require a new derivation |
| **Explainable** | Every claim supports the Curriculum → Evidence → Twin → Factor → Overall chain |
| **Non-authoritative for decisions** | Supplies preparedness context; does not select actions |

## 1.4 Conceptual shape (contract, not schema)

`ReadinessState` is defined by educational slots, not by storage layout.

| Slot | Architectural role |
|---|---|
| **Scope identity** | Student / curriculum / sitting (Goal) the judgement applies to |
| **Overall readiness posture** | Synthesised preparedness judgement — always accompanied by factors and warrant |
| **Named factors** | Ordered or keyed set of factor judgements (§2) |
| **Factor attributions** | Per-factor citations to Twin domains, Curriculum weight context, and evidence lineage where available |
| **Evidence Warrant** | Meta judgement of how much evidence supports the other factors (§4) |
| **Unknown / sparse flags** | Explicit markers when domains or factors are unknowable (§5–§6) |
| **Derivation context** | Curriculum format awareness (V1/V2), Goal constraints used, derivation identity for audit |
| **Optional snapshot metadata** | Only when persisted — model/version tags belong with Prediction, not as a second readiness truth |

Structural ReadinessState answers: *What is the factorable preparedness picture for this sitting, and how warranted is it?*

It intentionally does **not** answer: *What should the student do next?* or *What mastery belief should we write?*

## 1.5 What ReadinessState is not

- A primary Twin write domain fed by its own evidence stream  
- A second Knowledge mastery store or Memory retention engine  
- A Behaviour streak or mission-completion cache  
- A Confidence self-report channel  
- A Decision State or recommendation package  
- A mission plan or daily task list  
- A parallel learner-state store that analytics may update independently  
- A marketing claim of “ready” without warrant  

## 1.6 Ownership

| Concern | Owner |
|---|---|
| Producing ReadinessState | Readiness Aggregation (Capability 2.7) |
| Twin belief domains used as inputs | Knowledge / Memory / Behaviour / Performance Update Strategies (write path) |
| Syllabus denominator and weights | Curriculum Engine / CurriculumService |
| Optional persistence of a copy | Prediction snapshot path (§11) |
| Consuming readiness as context | Decision Engine, Recommendation packaging, Analytics/Dashboard (read-only) |
| Selecting next action | Decision Engine (Capability 2.8) — never Readiness |

---

# 2. Factor contracts

## 2.1 Purpose

Factor contracts define the **named structural dimensions** of preparedness that every ReadinessState must be able to express. Factors are educational meanings and attribution obligations — not scoring formulas.

## 2.2 Canonical factor catalogue

| Factor | Educational question | Primary Twin / context inputs | Must not absorb |
|---|---|---|---|
| **Curriculum Coverage** | How much of the official syllabus (weighted) has meaningful Twin presence? | Knowledge structural slots / topic presence; Curriculum denominator and weights | Proof of mastery; inventing syllabus topics |
| **Knowledge Strength** | How strong is current mastery (or honest structural proxy) on weighted identities? | Knowledge mastery beliefs or named structural proxies | Filling empty mastery bags; treating Confidence ratings as mastery |
| **Memory Stability** | Will demonstrated knowledge remain available at the sitting? | Memory retention structure, reinforcement clocks, retention beliefs when present; sitting date from Goals | Updating reinforcement; collapsing into Knowledge Strength |
| **Behaviour Reliability** | Is study practice consistent and feasible enough to close remaining gaps in time? | Behaviour consistency / adherence structure; Goals capacity | Granting exam readiness from streaks or mission counts |
| **Assessment Performance** | How does the student fare under assessed conditions? | Performance assessment lineage and scoped summaries | Emitting pass probability; equating one mock with overall readiness |
| **Time / Goal Pressure** *(supporting)* | How does remaining calendar and capacity reframe the other factors? | Goals sitting date, weekly hours, ambition | Inventing Knowledge or Performance |
| **Evidence Warrant / Uncertainty** *(meta-factor)* | How much evidence supports the other factors? | Density and quality of Twin lineage across domains | Silent omission when sparse |

Factor names may be refined in implementation naming, but the **meanings and separations** are binding. Collapsing Assessment Performance into Behaviour Reliability, or Memory Stability into Knowledge Strength, is forbidden.

## 2.3 Per-factor contract requirements

Every factor judgement in ReadinessState must expose, conceptually:

| Contract element | Requirement |
|---|---|
| **Identity** | Stable factor name from the catalogue |
| **Posture** | Educational posture for that dimension (supportive / risk-elevating / unknown / low-warrant / not-applicable) — exact vocab deferred; opacity forbidden |
| **Attribution** | Citations to Twin domain inputs and Curriculum weight context used |
| **Lineage hooks** | Evidence ids or Twin slot references when available |
| **Warrant contribution** | How this factor participates in overall Evidence Warrant (§4) |
| **Disagreement eligibility** | Factors may disagree with each other; disagreement must remain visible |

## 2.4 Factor principles (binding)

1. **Every overall readiness claim must decompose** into named factors.  
2. **Factors may disagree** — disagreement is educational information, not a bug to average away.  
3. **No opaque composite** without attributions.  
4. **No formulas in this milestone** — numeric weights and composites are deferred.  
5. **Supporting vs primary** — Time / Goal Pressure reframes; it does not replace Assessment Performance or Knowledge Strength.  
6. **Meta vs content** — Evidence Warrant is honesty about support for other factors; it is not a sixth content belief about the syllabus.  
7. **V1/V2 safe** — any factor that uses weights obtains them via canonical Curriculum helpers (§9–§10).

## 2.5 What is not a readiness factor

- Motivation score as preparedness  
- Streak length as exam readiness  
- Self-report Confidence as Assessment Performance  
- Mission completion count as Knowledge Strength  
- Dashboard vanity percentage without Twin lineage  
- Decision reason codes (those belong to Decision Engine)  
- Mission task lists  

---

# 3. Aggregation boundaries

## 3.1 Aggregation owns

| Responsibility | Boundary meaning |
|---|---|
| **Read Twin snapshot** | Observational consumption of Knowledge, Memory, Behaviour, Performance (and optional Confidence stance per §7) |
| **Read Curriculum context** | Denominator, order, exam weights via canonical helpers |
| **Read Goals context** | Sitting date, capacity, ambition constraints |
| **Synthesise factors** | Produce named factor judgements and attributions |
| **Synthesise overall posture** | Compose overall readiness judgement from factors without hiding disagreement or warrant |
| **Propagate Evidence Warrant** | Carry uncertainty honestly through factors and overall judgement |
| **Emit explanation inputs** | Provide chain-ready attributions for consumers |
| **Optionally request snapshot** | Hand a derived ReadinessState to the Prediction path after derivation |

## 3.2 Aggregation must not own

| Non-responsibility | Why |
|---|---|
| Learning Evidence authorship | Evidence remains append-only history |
| Twin domain mutation | Only Update Strategies via the Twin Update Pipeline |
| Mastery / retention / behaviour / performance belief engines | Domain strategies own enrichment |
| Syllabus structure | Curriculum Engine remains truth |
| Next-action selection | Decision Engine |
| Recommendation packaging | Capability 2.9 |
| Mission generation | Capability 2.10 via Decision Engine |
| Parallel learner-state stores | Twin remains educational-state authority |
| Orphan evidence absorption | Types without Twin strategy ownership must not be ingested ad hoc |
| Secondary evidence smuggling (Choice B) | Not via readiness without a deliberate architecture note |

## 3.3 Write / read firewall

```
WRITE PATH                              READ PATH
─────────                              ────────
Evidence → Update Pipeline             Twin + Curriculum + Goals
         → Domain Strategies                    ↓
         → Twin snapshot               Readiness Aggregation
                                                ↓
                                       ReadinessState
                                                ↓
                                       Decision / Analytics / Prediction snapshot
```

Binding firewall rules:

1. Aggregation receives a Twin snapshot and returns ReadinessState.  
2. No Twin domain field is written by aggregation.  
3. Aggregation must not bypass the Update Pipeline to “fix” readiness.  
4. Aggregation must not call Decision Engine or Mission Generation.  
5. If a design needs “readiness said do X,” the design is wrong.

## 3.4 Determinism and purity

- Core aggregation is a pure function of declared inputs.  
- No required network LLM calls in the core path.  
- Coach/LLM may narrate chain-supported attributions later — never author factors.  
- Randomness and engagement theatre defaults are forbidden in the core path.

## 3.5 Relationship to downstream consumers

| Consumer | May use ReadinessState for | Must not treat Readiness as |
|---|---|---|
| Decision Engine | Preparedness context, urgency, warrant, factor tensions | Action selector |
| Recommendation Engine | Explanation chain citations when Decision cited readiness | Action ranker |
| Mission Generation | Indirect lineage via Decision reason codes only | Direct mission author |
| Analytics / Dashboard | Presentation of factors and warrant | Parallel formula authority |
| Prediction path | Optional historical copy | Derivation substitute |

---

# 4. Evidence Warrant propagation

## 4.1 Definition

**Evidence Warrant** (Uncertainty) is the meta-factor that answers:

> **How much Twin-backed evidence supports the preparedness picture we are presenting?**

It is first-class educational honesty, not a UI inconvenience or an error code.

## 4.2 Propagation rules

1. **Per-factor warrant** — each content factor carries a warrant posture derived from the density and applicability of its Twin inputs.  
2. **Overall warrant** — overall readiness warrant is never stronger than the weakest critical sitting-relevant factors allow; sparse assessment evidence must keep exam-preparedness warrant low even if Behaviour looks strong.  
3. **Absence lowers warrant** — missing domain state lowers warrant; it does not invent Mid content postures.  
4. **Warrant is not content** — low warrant is not the same as “student is weak”; high Behaviour Reliability with empty Performance yields informative pace signal and **low exam-preparedness warrant**.  
5. **Warrant travels with explanations** — every overall claim presented to students or auditors must be able to surface warrant.  
6. **Downstream inheritance** — Decision Engine and recommendations that cite readiness must preserve warrant honesty (e.g. “diagnostic preferred because warrant is low”), not strip it for confidence theatre.

## 4.3 Propagation diagram (conceptual)

```
Twin domain density / lineage quality
        ↓
Per-factor Evidence Warrant
        ↓
Overall Evidence Warrant  ───► constrains how strongly Overall Readiness may be asserted
        ↓
Explanation chain + Decision context
```

## 4.4 Forbidden warrant behaviours

- Hiding uncertainty to encourage engagement  
- Averaging missing factors as neutral Mid to “fill” warrant  
- Letting self-report Confidence inflate Assessment Performance warrant  
- Presenting a single strong mock as high overall warrant across the syllabus  
- Storing a Prediction snapshot that drops warrant metadata while keeping a bold overall claim  

---

# 5. Cold-start semantics

## 5.1 Definition

A Twin is in **cold start** (or sparse start) for readiness when one or more hold:

- No or few Knowledge topic slots / empty mastery beliefs  
- No or few Memory reinforcements / empty retention beliefs  
- Thin or empty Behaviour lineage  
- No or sparse Performance assessments / empty summaries  
- Goals may exist while educational evidence does not  

**Goals alone never create preparedness.**

## 5.2 Cold-start output contract

When cold start applies, ReadinessState must:

1. Mark overall readiness as **not yet knowable** / **unknown** / **low-warrant** — not Mid, not High.  
2. Emit factors with explicit unknown or low-warrant postures where inputs are absent.  
3. Allow partial factors when structural presence exists (e.g. coverage started) **without** upgrading exam preparedness.  
4. Keep Evidence Warrant elevated in uncertainty (low support).  
5. Preserve explainability: “insufficient evidence to judge sitting preparedness” is a valid overall narrative.

## 5.3 Forbidden cold-start behaviours

- Inventing High readiness to encourage engagement  
- Defaulting overall readiness to Mid  
- Treating mission adherence as exam readiness  
- Filling empty belief bags inside the aggregator  
- Narrating “you’re on track” without Twin warrant  
- Using Confidence self-report to invent Assessment Performance  
- Writing synthetic Twin beliefs so aggregation has something to score  

## 5.4 Cold-start vs Decision Engine

Decision Engine (later) may prefer diagnostic or evidence-creating actions under cold start. That is **decision**, not readiness inventing Performance. Readiness only makes the unknown visible.

---

# 6. Unknown-state handling

## 6.1 Distinction: unknown vs weak vs supportive

| Posture | Meaning | Architectural rule |
|---|---|---|
| **Unknown** | Insufficient Twin evidence to judge this factor | Must remain explicit; must not be coerced to Mid |
| **Low warrant** | Some signal exists but support is thin | Assert softly; do not overclaim |
| **Risk-elevating / weak** | Enough evidence to judge the factor as concerning | Distinct from unknown |
| **Supportive** | Enough evidence to judge the factor as supportive of preparedness | Distinct from unknown |
| **Not applicable** | Factor structurally does not apply in this context (rare; must be justified) | Must not be used to hide cold start |

## 6.2 Domain-empty mapping (binding)

| Input condition | Factor handling |
|---|---|
| Empty / missing Performance | Assessment Performance = unknown / low warrant — never assumed strong or assumed permanently weak |
| Empty mastery beliefs | Knowledge Strength = unknown, or structural-coverage-only if slots exist — never fabricated High mastery |
| Empty Memory | Memory Stability = unknown — never assume durable retention |
| Thin Behaviour | Behaviour Reliability = unknown / low warrant |
| Goals only | Overall readiness = not yet knowable; all exam-preparedness claims low-warrant |
| Strong Behaviour, empty Performance | Behaviour may be informative for pace; overall exam readiness remains low-warrant |

## 6.3 Aggregation rules for unknowns

1. **Unknowns do not average into Mid.**  
2. **Unknowns do not disappear** from the factor set — omit-from-UI is a presentation choice; architecture retains them.  
3. **Partial knowledge is named** — e.g. coverage structural presence without mastery beliefs must be labelled as coverage/proxy, not Knowledge Strength High.  
4. **Disagreement with unknown** — a supportive factor beside an unknown critical factor keeps overall assertiveness constrained by warrant.  
5. **Orphan / unmapped inputs** — do not invent factor content from evidence types lacking Twin ownership.

## 6.4 Product language for unknown

Honest posture:

> We do not yet know if you are prepared.  
> Here is what little we have.  
> Uncertainty is high.

Forbidden posture: silent Mid scores, fake completeness bars, or “looking good” without warrant.

---

# 7. Confidence interaction

## 7.1 Separability (midpoint condition)

**Confidence** (how certain the student *feels*, and later how well that is calibrated) is **not** readiness and **not** mastery.

Estimate-warrant confidence (“how sure are we of this judgement?”) belongs to **Evidence Warrant** and must be named distinctly from self-report Confidence.

## 7.2 Readiness v1 stance (binding decision)

For Readiness Aggregation **v1**:

| Decision | Rule |
|---|---|
| **Self-report Confidence** | **Omit** from readiness factor synthesis |
| **Knowledge-held `CONFIDENCE_RATING` lineage** | Must **not** be treated as calibrated Confidence or as Assessment Performance |
| **Evidence Warrant** | Remains the honesty channel for judgement certainty |
| **Future Confidence domain** | May later supply an explicit provisional factor with clear lower warrant than Performance — additive, not required for v1 |

## 7.3 Provisional path (future, non-blocking)

If a later milestone introduces Confidence as a readiness factor:

1. It must be an **explicit named factor**, not a silent booster of Assessment Performance or Knowledge Strength.  
2. It must be marked **lower warrant** than Performance and Knowledge for preparedness claims.  
3. Overconfidence / underconfidence may inform Decision Engine risk framing — not upgrade overall readiness in contradiction to Performance.  
4. Aggregation still never mutates Confidence state.

## 7.4 Forbidden Confidence behaviours

- Equating “I feel ready” with overall readiness High  
- Using Confidence to fill cold-start unknowns  
- Letting Confidence override dense contrary Performance evidence in narrative  
- Treating Confidence contamination as a temporary product shortcut  

---

# 8. Context inputs

## 8.1 Input classes

| Input class | Source | Role for aggregation |
|---|---|---|
| **Knowledge** | Twin KnowledgeState | Coverage and Knowledge Strength inputs |
| **Memory** | Twin MemoryState | Memory Stability / retention-risk inputs |
| **Behaviour** | Twin BehaviourState | Behaviour Reliability / pace feasibility inputs |
| **Performance** | Twin PerformanceState | Assessment Performance inputs |
| **Goals** | Twin Goals (or Goal context bound to sitting) | Sitting date, capacity, ambition — Time / Goal Pressure and scope |
| **Curriculum** | Curriculum Engine via canonical helpers | Denominator, order, exam weights |
| **Identity** | Twin / user / curriculum scope | Bound the judgement to the correct student and syllabus |
| **Confidence** | Omit in v1 (§7) | Not a v1 aggregation input |
| **Decision State** | Not an aggregation input | Downstream consumer, not readiness fuel |
| **Missions / plans** | Not belief inputs | Must not grant preparedness; Behaviour may already reflect adherence lineage |

## 8.2 Input contract (binding)

1. Aggregation is defined over a **single coherent Twin snapshot** plus Curriculum + Goals for that scope.  
2. Mixed snapshots from different times must not be silently blended.  
3. Secondary evidence columns must not be read behind Twin’s back.  
4. Legacy TopicProgress / attempt tables are **not** authoritative Twin substitutes for Epic 2 readiness (§13).  
5. Same inputs → same ReadinessState in the deterministic core.

## 8.3 Supporting vs belief inputs

| Kind | Examples | Rule |
|---|---|---|
| **Belief / structural Twin inputs** | Knowledge, Memory, Behaviour, Performance | Observational only; never mutated |
| **Constraint / context inputs** | Goals, Curriculum weights, Identity | Shape relativity and pressure; do not invent beliefs |
| **Forbidden shortcuts** | Raw mission rows, Confidence self-report (v1), orphan evidence | Do not bypass Twin ownership |

---

# 9. Curriculum weighting

## 9.1 Principle

Preparedness is always **curriculum-relative**. A readiness claim without syllabus weight context is incomplete for exam products.

## 9.2 Weighting responsibilities

| Concern | Owner |
|---|---|
| Official syllabus structure, order, weights | Curriculum Engine / CurriculumService |
| Applying weights to factor narratives and risk concentration | Readiness Aggregation (consumer) |
| Inventing parallel topic trees or weight tables | **Forbidden** |

## 9.3 Weighting rules (architectural, not formulas)

1. High-weight syllabus areas contribute more strongly to sitting-risk narratives than low-weight areas — as **attribution emphasis**, not as a coded formula in this note.  
2. Coverage and strength factors must be interpretable against the **canonical denominator** for the Goal’s curriculum.  
3. Risk concentration on high-weight weak/unknown areas must remain visible in attributions.  
4. Time / Goal Pressure interacts with weighted remaining work as context — it does not replace weight truth.  
5. Aggregation must not recompute unofficial “effective weights” that disagree with Curriculum helpers.

## 9.4 Weighting and warrant

- Dense evidence on low-weight topics must not inflate overall warrant for the sitting.  
- Sparse evidence on high-weight topics must keep overall exam-preparedness warrant constrained.  
- A single strong mock on a narrow slice does not warrant “ready across the paper.”

---

# 10. V1/V2 compatibility

## 10.1 Invariant

**V1 (flat) and V2 (sectioned) curricula must both remain loadable and traversable.** Readiness Aggregation must not require Sections globally.

## 10.2 Compatibility rules

| Rule | Requirement |
|---|---|
| **Canonical traversal** | Topic order and coverage denominator via CurriculumService helpers only |
| **Weight branching** | V1 topic weights vs V2 section (and topic) weights handled as Curriculum-format awareness — not as forked readiness products |
| **No Section hard-requirement** | Factor logic that assumes Section rows exist breaks V1 — forbidden |
| **No parallel ordering** | Aggregation must not invent a second syllabus order for “coverage %” |
| **Identity stability** | Curriculum entity ids used in attributions must match Twin and Curriculum identities |
| **Feature parity of honesty** | Cold-start and unknown semantics apply equally to V1 and V2 |

## 10.3 What V2 enables without changing ownership

- Section-level risk concentration narratives when sections exist  
- Section-weighted emphasis in attributions  

These are additive explanation richness. They must degrade safely on V1 to topic-weighted narratives.

## 10.4 Compatibility checklist

| Check | Status required |
|---|---|
| Flat curriculum readiness deriveable | Yes |
| Sectioned curriculum readiness deriveable | Yes |
| Same factor catalogue both formats | Yes |
| Same cold-start / unknown contracts | Yes |
| Weights only from canonical helpers | Yes |

---

# 11. Prediction snapshots

## 11.1 Purpose

A **Prediction snapshot** is an optional historical copy of a derived readiness (or later pass-probability) judgement for audit, trend, and analytics.

Storage ≠ derivation authority.

## 11.2 Derive-first rule (binding)

```
Read Twin + Curriculum + Goals
        ↓
Derive ReadinessState (aggregation)
        ↓
Optionally persist snapshot (Prediction path)
```

Forbidden: writing PredictionState readiness fields that skip aggregation, or treating a stored snapshot as live Twin belief that other writers may patch.

## 11.3 Snapshot contract

| Element | Requirement |
|---|---|
| **Source** | Must reference a derived ReadinessState (or equivalent factor set + warrant) |
| **Timing** | After derivation only |
| **Metadata** | Model/version or derivation identity tags for audit when persisted |
| **Warrant** | Snapshot must not drop Evidence Warrant while retaining a bold overall claim |
| **Authority** | Live readiness for decisions should re-derive from current Twin unless an explicitly versioned historical read is requested |
| **Owner** | Prediction snapshot path (adjacent to Capability 2.7); aggregation remains derivation owner |

## 11.4 What snapshots must not become

- A write-side readiness domain updated from missions or UI toggles  
- A third formula store diverging from Twin-first aggregation  
- A cache that Decision Engine mutates in place  
- A substitute for empty Twin beliefs  

## 11.5 Pass probability (future)

Pass probability, if introduced later, is a sibling derived / Prediction output reading the same Twin + Curriculum + Goals — still read-side, still factorable or warrant-aware, still snapshot-after-derive. It does not move into Performance or Behaviour write strategies.

---

# 12. Explainability

## 12.1 Mandatory chain

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
Overall Readiness (ReadinessState)
```

Extended when consumed downstream:

```
… → ReadinessState
        ↓
Decision Engine reason codes
        ↓
Recommendation / Mission explanation (lineage only)
```

## 12.2 Attribution requirements

1. Each presented factor cites Twin domain inputs and Curriculum weight context.  
2. Overall readiness cites contributing factors — including disagreement.  
3. Evidence Warrant appears whenever evidence density is low or critical factors are unknown.  
4. Explanations must not invent evidence, syllabus topics, or Twin beliefs.  
5. LLM / coach narration may only restate chain-supported attributions.  
6. Snapshots used in historical explanations must declare they are historical copies.

## 12.3 Layer examples (educational, not formulas)

| Layer | Example content |
|---|---|
| **Curriculum** | “This area carries substantial exam weight.” |
| **Evidence** | “Recent assessment evidence on topic T showed repeated incorrect attempts.” |
| **Twin Domain** | “Performance summaries weak on T; Memory reinforcement stale; Knowledge slot present with thin warrant.” |
| **Readiness Factor** | “Assessment Performance and Memory Stability elevate sitting risk on a high-weight slice.” |
| **Overall Readiness** | “Preparedness is fragile: coverage partial, assessment warrant thin on weighted areas, uncertainty explicit.” |

## 12.4 Forbidden explanation patterns

- Single opaque composite without factors  
- Explanations that cite UI labels but not Twin/evidence  
- Post-hoc stories that disagree with Twin lineage  
- Collapsing all factors into Motivation or streak language  
- Treating Confidence self-report as Assessment Performance  
- “Readiness chose this mission” narratives  

---

# 13. Legacy Readiness convergence

## 13.1 Current legacy posture

Legacy readiness analytics (`ReadinessService` and related dashboard/analytics summaries) estimate preparedness from progress, attempts, and curriculum weights. They predate Twin-first Educational Intelligence and must not remain a permanent parallel authority.

## 13.2 Convergence principle (binding)

| Rule | Meaning |
|---|---|
| **Twin-first authority** | Epic 2 readiness truth is ReadinessState derived from Twin + Curriculum + Goals |
| **No third formula** | Do not maintain a long-lived third readiness definition beside Twin aggregation and legacy service |
| **Snapshots after derive** | Prediction copies do not create a third live formula |
| **Presentation convergence** | UI/analytics should migrate to Twin-first factors and warrant |
| **No deepening of legacy TopicProgress formulas** | Avoid expanding legacy scoring while Twin-first aggregation lands |

## 13.3 Convergence path (architectural stages)

```
Stage A — Coexistence (documented)
  Legacy ReadinessService continues for existing surfaces.
  Twin-first aggregation designed; not yet required of all UI.

Stage B — Twin-first read for new intelligence
  Decision Engine and new readiness narratives consume ReadinessState.
  Legacy summaries may still exist but are marked transitional.

Stage C — Presentation cutover
  Dashboard/analytics readiness cards read Twin-first factors + warrant.
  Legacy composite retained only if it can share definitions or is retired.

Stage D — Legacy retirement / thin adapter
  Legacy entry points become adapters over ReadinessState or are removed.
  No divergent learner-state math remains.
```

Exact timing of stages is an implementation/program concern. This architecture locks **direction and non-negotiables**, not calendar.

## 13.4 Adapter rules during coexistence

1. Adapters may translate ReadinessState into legacy-shaped summaries for UI continuity.  
2. Adapters must not reintroduce belief invention or Mid defaults for cold start.  
3. Adapters must not write Twin domains.  
4. If legacy and Twin-first disagree, Twin-first wins for Educational Intelligence paths; divergence must be treated as transitional debt, not dual truth.

## 13.5 Explicit non-goals of this milestone

- Refactoring or deleting `ReadinessService` now  
- Migrating all analytics widgets in this note  
- Replacing RecommendationService decision logic  
- Inventing interim hybrid scores that average legacy % with Twin factors  

---

# 14. Risks

| Risk | Architectural impact | Mitigation |
|---|---|---|
| **Treating ReadinessState as a write domain** | Circular Twin updates; broken evidence lineage | Strict read-side classification; no Update Strategy for readiness beliefs |
| **Averaging unrelated factors** | Hides educational tension; false Mid readiness | Keep factors separable; surface disagreement; defer numeric discipline |
| **Hiding uncertainty** | False preparedness; broken trust | Evidence Warrant mandatory; cold-start and unknown contracts |
| **Unknown coerced to Mid** | Cold-start fabrication | Explicit unknown posture; forbidden Mid defaults |
| **Duplicated readiness stores** | Divergent % vs Twin factors; dual authority | Twin-first convergence; no third formula; snapshots after derive only |
| **Legacy formula deepening** | Permanent dual truth | Freeze legacy expansion; adapter-only coexistence |
| **Confidence contamination** | Self-report as readiness | Omit Confidence from v1; warrant ≠ Confidence |
| **Activity-as-readiness** | Mission completion narrated as exam preparedness | Behaviour Reliability ≠ Assessment Performance ≠ Overall |
| **Single-mock overclaim** | Narrow evidence becomes whole-paper readiness | Assessment Performance is one factor; warrant + Curriculum weight constrain overall |
| **Readiness conflated with Decision** | Wrong owner; opaque product behaviour | Firewall vs Decision Engine |
| **Direct readiness → missions** | Activity theatre; circular incentives | Missions only via Decision Engine |
| **Opaque composites** | Product thesis failure | Mandatory factorability + explanation chain |
| **V1 breakage** | Section-required logic fails flat curricula | Canonical helpers; no global Section assumption |
| **Belief engines inside aggregation** | Invented mastery; unmaintainable math | Aggregation consumes beliefs; strategies enrich them |
| **LLM ownership creep** | Invented preparedness stories | Coach narrates chain-supported factors only |
| **Orphan evidence absorption** | Ad hoc readiness without Twin ownership | Do not absorb orphan types into 2.7 |
| **Choice B smuggling** | Secondary evidence updates via readiness | Keep Choice A until deliberate architecture note |
| **Snapshot-as-truth** | Stale Prediction overrides live Twin | Live paths re-derive; snapshots are historical |
| **Warrant stripped at presentation** | Honest derivation, dishonest UI | Warrant travels with ReadinessState and explanations |

---

# 15. Recommendations

## 15.1 Implementation sequence (separate milestones)

1. **Structural read-side contracts** — factor identity set, unknown/warrant postures, input boundary checklist (still no scoring formulas if beliefs remain sparse).  
2. **Aggregation skeleton** — derive ReadinessState from Twin + Curriculum + Goals with attributions; cold-start honesty first.  
3. **Consumer wiring** — Decision Engine context inputs; analytics adapters as needed.  
4. **Prediction snapshot path** — optional, derive-first, warrant-preserving.  
5. **Legacy convergence stages** — adapters → Twin-first UI → retire divergent math.  
6. **Numeric / pass-probability enrichment** — only after structural honesty and factorability are proven.

## 15.2 Binding design recommendations

1. Keep **ReadinessState** named and documented as **derived**, never as a write-path Twin peer to Knowledge.  
2. Preserve factor **disagreement** as a feature.  
3. Prefer **unknown / low warrant** over fake Mid.  
4. Keep Assessment Performance distinct from Behaviour Reliability in every readiness narrative.  
5. **Omit Confidence** from readiness v1.  
6. Obtain all weights/order via **canonical Curriculum helpers**.  
7. Do not deepen TopicProgress-based readiness formulas while Twin-first aggregation lands.  
8. Never generate missions from readiness directly.  
9. Never let Prediction snapshots skip or replace derivation.  
10. Treat Evidence Warrant as non-optional in ReadinessState.

## 15.3 Midpoint conditions acknowledged

This architecture encodes the Epic 2 Midpoint Review conditions relevant to Readiness:

- Cold-start / empty-belief / unknown contract  
- No parallel authority / third formula  
- Confidence separability  
- Write/read firewall  
- Curriculum V1/V2 invariants  
- Snapshot path: derive first, store second  
- Registration-order stability for Twin writes remains upstream (K→M→B→P)

## 15.4 Architecture compliance checklist

| Invariant | Status for this architecture |
|---|---|
| Twin is sole educational-state authority | Readiness consumes Twin; does not fork beliefs |
| Evidence is only legitimate belief input | Readiness never owns evidence |
| Strategies own domain evolution | Readiness is not a write strategy |
| Activity ≠ readiness; Confidence ≠ mastery; Behaviour ≠ learning | Binding |
| Readiness ≠ Decision; Readiness ≠ Missions | Binding |
| V1/V2 curriculum compatibility | Required; no traversal redesign in this milestone |
| No implementation in this milestone | Satisfied |

## 15.5 Explicit stop line

This milestone delivers **architecture only**.

**Do not proceed in this milestone to:** code, dataclasses, services, tests, database changes, scoring formulas, Decision Engine implementation, or UI.

**Next engineering step (separate milestone):** structural read-side contracts and/or implementation plan for Capability 2.7 — then implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot is the read input; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains consumed without modification |
| **2.7.1** | **Readiness Educational Analysis** | Approved educational charter this architecture implements structurally |
| **2.7.2** | **Readiness Aggregation Architecture** | **This document** |
| 2.8 | Decision Engine | Consumes ReadinessState as context |
| 2.9 | Explainable Recommendation Engine | May cite readiness factors in explanation packaging |
| 2.10 | Mission Generation Intelligence | Depends on Decision Engine, not Readiness directly |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.7.2 — Readiness Aggregation Architecture |
| Nature | Architecture only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required; no traversal changes introduced |
| Application code intentionally untouched | Yes |
| Midpoint gate | APPROVED WITH CONDITIONS — conditions encoded herein |
| Prior | Capability 2.7.1 — Readiness Educational Analysis (approved) |
| Next | Structural contracts / implementation plan (separate milestone) — not started here |

---

*End of Capability 2.7.2 Readiness Aggregation Architecture.*
