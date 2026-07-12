# Capability 2.9.2 — Recommendation Engine Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.9 Explainable Recommendation Engine (architecture preceding structural contracts and implementation)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Educational charter:** [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md)  
**Upstream gate:** Educational Reasoning Review — APPROVED WITH CONDITIONS ([`docs/reviews/EDUCATIONAL_REASONING_REVIEW.md`](../reviews/EDUCATIONAL_REASONING_REVIEW.md))  
**Companions:** [`CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md), [`CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md)  
**Scope:** Structural architecture for Decision → Recommendation projection — **no code, algorithms, ranking, scoring, services, tests, schemas, or migrations**

---

## Document purpose

This milestone answers **how** the Explainable Recommendation Engine is structured as architecture after Capability 2.9.1 approved **what** it is educationally.

Decision Engine supplies the authoritative next-action selection. Recommendation Engine is Epic 2’s **read-side packaging / projection layer**: it turns a Decision into an attributable, student-facing suggestion — without selecting actions, inventing ranking, mutating Twin beliefs, recomputing readiness, or composing missions.

This note locks structural contracts so later milestones can add packaging artefacts and narration surfaces without inventing syllabus, coercing unknown readiness, or forking a parallel next-action authority.

**Governing principle (binding):**

> **Recommendation remains a projection of Decision.**

**Non-goals of this document**

- Code, pseudocode algorithms, package layouts, or dataclass definitions  
- Database schemas, Alembic migrations, or ORM layouts  
- Ranking formulas, selection math, priority scores, or optimization objectives  
- UI redesign, gamification, dashboards, notifications, or social features  
- Mission Generation Intelligence design beyond projection boundaries  
- Replacement of Curriculum Engine, Evidence Model, Twin aggregate, Readiness Aggregation, or Decision Engine contracts  

**Hard architectural rules (binding):**

1. Recommendation Engine never selects or re-selects next actions.  
2. Recommendation Engine never invents ranking that disagrees with Decision reason codes.  
3. Recommendation Engine never mutates Twin belief domains.  
4. Recommendation Engine never recomputes readiness or coerces unknown / low-warrant / `not_yet_knowable` into Mid or High preparedness.  
5. Recommendation Engine never invents curriculum identities, evidence ids, or Twin beliefs.  
6. Every Recommendation must be attributable to a Decision and walk the mandatory explainability chain.  
7. Accepting a Recommendation does not grant mastery; completion / assessment evidence does.  
8. Curriculum V1 and V2 remain loadable; presented identities come only from Decision / Curriculum lineage.

---

# 1. Recommendation model

## 1.1 Position

A **Recommendation** is the product projection of a Decision Engine output: a concrete, attributable suggestion the student can accept, dismiss, defer, or act on.

```
CurriculumContext + Goals + Constraints
        +
Digital Twin domains
        +
ReadinessState
        ↓
Decision Engine              (read-side next-action selection)
        ↓
Decision (selected action + candidates + reason codes + lineage + warrant posture)
        ↓
Explainable Recommendation Engine   (read-side packaging / projection)
        ↓
Recommendation (attributable suggestion)
        ↓
Decision Journal (accept / dismiss / defer) → Learning Evidence
        ↓
Optional Mission projection (Capability 2.10)
```

## 1.2 Architectural classification

| Kind | Role |
|---|---|
| **Recommendation** | Live packaging result for one Decision — the Recommendation Engine’s primary output |
| **Recommendation packaging** | Mapping Decision → action surface, explanation presentation, urgency/duration presentation, citations, journal affordances |
| **Not a write-path Twin belief domain** | No Update Strategy evolves Recommendation from evidence as mastery/retention |
| **Not educational-state authority** | Twin domains remain sole authority for beliefs; Recommendation is a product consequence |
| **Not selection authority** | Decision Engine alone selects; Recommendation never re-ranks |
| **Sibling to Mission projection** | Capability 2.10 projects Decisions into daily structure; packaging ≠ mission composition |

## 1.3 Architectural properties

| Property | Requirement |
|---|---|
| **Read-side** | Produced by projecting a Decision (+ communication context) |
| **Decision-bound** | Every Recommendation cites exactly one Decision as selection authority |
| **Deterministic core attribution** | Same Decision (and bound context) in → same attributable packaging out |
| **Explainable by construction** | Completes the mandatory explainability chain; narrates Decision reason codes |
| **Curriculum-bound** | Curriculum-scoped suggestions use official syllabus identities only |
| **Warrant-honest** | Evidence Warrant / cold-start posture survives into Recommendation Confidence and tone |
| **Immutable per packaging evaluation** | One Decision packaging yields one Recommendation for that input set |
| **Non-authoritative for beliefs** | Accept does not grant mastery; journal outcomes become preference / intent evidence |

## 1.4 Conceptual shape — Recommendation (contract, not schema)

| Slot | Architectural role |
|---|---|
| **Decision reference** | Identity of the Decision being projected (selection authority) |
| **Actionable suggestion** | Student-facing action projected from Decision selected action (study / revise / assess / diagnostic / rest-protect), curriculum-scoped when applicable |
| **Recommendation Reasons** | Narration of Decision reason codes + explainability-chain layers |
| **Explanation chain presentation** | Student-facing Why? across Curriculum / Evidence / Twin / Readiness (when cited) / Decision |
| **Lineage citations** | Twin / evidence / curriculum / readiness hooks carried from Decision — never fabricated |
| **Warrant / Recommendation Confidence posture** | Evidence-density honesty for the suggestion — distinct from self-report Confidence and Mastery |
| **Urgency / duration presentation** | Communication of Decision-derived feasibility and timing — not an independent priority optimizer |
| **Candidate contrast (when useful)** | “Why not Y?” drawn from Decision candidate set only |
| **Response affordances** | Accept / dismiss / defer as journalable outcomes |
| **Evaluation context** | Packaging version / Decision engine version tags for audit |

## 1.5 What Recommendation is not

- A Decision or re-ranked candidate list  
- A readiness score or factor recomputation  
- A Knowledge / Memory / Behaviour / Performance belief store  
- A Mission / MissionTask list or WeekPlan  
- A parallel mastery map inside suggestion rows  
- A black-box coach utterance without Decision reason codes  
- A private ranking score as educational authority  

## 1.6 Ownership

| Concern | Owner |
|---|---|
| Producing Decision (selection) | Decision Engine (Capability 2.8) |
| Packaging Decision into Recommendation | **Explainable Recommendation Engine (Capability 2.9)** |
| Twin belief domains | Update Strategies via Twin Update Pipeline |
| Preparedness context | Readiness Aggregation (Capability 2.7) |
| Syllabus identities and weights | Curriculum Engine / CurriculumService helpers |
| Session/day task projection | Mission Generation Intelligence (2.10) |
| Journal recording of accept/dismiss/defer | Product recording paths → Decision Journal → Learning Evidence |
| Selecting next action | **Decision Engine only** |

---

# 2. Inputs

## 2.1 Input principle

Recommendation Engine **consumes** Decision authority and supporting communication context. It **never modifies** Twin domains, readiness beliefs, or Decision selection. Same Decision (and bound context) in → same attributable Recommendation packaging out.

## 2.2 Primary input: Decision

| Decision element | Architectural role for Recommendation |
|---|---|
| **Selected action** | The only next-action authority to package — action type + curriculum scope when present |
| **Candidate set** | Enables “why this, not that?” without inventing rejected alternatives |
| **Reason codes** | Stable machine-readable factors that Recommendation Reasons must narrate faithfully |
| **Value rationale hooks** | Educational “why now” substance for narration — not marketing slogans |
| **Lineage references** | Twin / evidence / curriculum / readiness hooks already present on the Decision |
| **Constraint acknowledgements** | Feasibility / intensity demotion that packaging must not erase or over-claim |
| **Warrant posture** | Inherited honesty when readiness or Twin evidence density is low |
| **Evaluation context** | Curriculum format awareness (V1/V2), Decision version tags for audit |

**Binding:** Recommendation packages the Decision’s selected action. It does not re-select among candidates.

## 2.3 Supporting inputs (communication only)

| Input | Architectural role | Authority |
|---|---|---|
| **Goals** | Scope language about sitting destination and capacity-honest duration/urgency presentation | Goals — communication bound only |
| **Constraints already acknowledged on Decision** | Present feasible ambition; do not upgrade into unsustainable cram theatre | Decision-carried feasibility |
| **Decision Journal history (when available)** | Avoid thrashing narration; respect prior dismiss without treating dismiss as mastery | Preference history — not mastery |
| **Self-report Confidence (when Decision framed it)** | May appear only as risk-framing narration — never as mastery or readiness upgrade | Decision-cited framing only |

Student context shapes **communication appropriateness**, not a second selection authority.

## 2.4 Input contract (binding)

1. **Decision is the sole selection authority input** — packaging never re-ranks.  
2. **Reason codes are authored upstream** — packaging narrates; it does not redefine educational factors.  
3. **Lineage is citation, not invention** — no fabricated evidence ids or Twin beliefs.  
4. **Evidence Warrant is non-optional honesty** — cold start and low warrant survive into copy.  
5. **Student context shapes communication, not authority** — Goals/Constraints/Journal inform phrasing and response handling, not a private Decision Engine.  
6. **No legacy hybrid truth** — do not average `ReadinessService` percentages with Twin/Decision factors as temporary packaging authority.  
7. **Curriculum identities remain canonical** — V1/V2 via Decision / CurriculumContext lineage only.

## 2.5 What is not an input authority

- UI streak counters as educational value justification  
- Mission completion counts as mastery proof  
- Opaque “recommended for you” product defaults without Decision  
- Coach/LLM free-text topic invention  
- Legacy `RecommendationService.generate_recommendations` heuristics as Twin-first authority  
- Legacy `ReadinessService` overall % as Decision substitute  
- Private packaging scores that override Decision selection  

---

# 3. Projection pipeline

## 3.1 Position

The projection pipeline is the **architectural sequence** of read-side stages that turn a Decision into a Recommendation. It is a structural contract — not an algorithm, ranking function, or optimization solver.

## 3.2 Pipeline stages (architectural)

```
1. Bind Decision
        ↓
2. Validate projection preconditions
   (selected action present; reason codes present; lineage hooks; warrant posture)
        ↓
3. Project actionable suggestion
   (action family + curriculum identity from Decision — no re-selection)
        ↓
4. Package explanation chain
   (Curriculum → Evidence → Twin → Readiness when cited → Decision reason codes)
        ↓
5. Propagate warrant / Recommendation Confidence posture
        ↓
6. Present urgency / duration from Decision-derived feasibility
        ↓
7. Attach candidate contrast (from Decision candidate set)
        ↓
8. Attach response affordances (accept / dismiss / defer)
        ↓
Recommendation
```

## 3.3 Stage obligations

| Stage | Obligation | Forbidden |
|---|---|---|
| **Bind Decision** | One Decision is the sole selection authority for this Recommendation | Packaging without Decision; inventing a Decision |
| **Validate preconditions** | Require selected action + reason codes on the core path | Opaque suggestions without codes |
| **Project suggestion** | Map Decision selected action to actionable surface | Re-select among candidates; invent topics |
| **Package explanation** | Narrate Decision reason codes + chain layers | Invent evidence, syllabus, Twin beliefs, or disagreeing codes |
| **Propagate warrant** | Carry Decision warrant / cold-start honesty into Recommendation Confidence | Mid/High preparedness theatre under thin warrant |
| **Urgency / duration** | Present Decision-derived feasibility | Independent priority optimizer; engagement urgency theatre |
| **Candidate contrast** | Use Decision candidate set only | Invent “why not” alternatives Decision never considered |
| **Response affordances** | Expose journalable outcomes as preference / intent | Treat accept as mastery grant |

## 3.4 Pipeline principles (binding)

1. **Projection only** — no selection enrichment inside packaging.  
2. **One Decision → one Recommendation** on the core educational path (batches are ordered Decision packaging later; ordering authority remains Decision).  
3. **Deterministic attribution** — packaging may vary presentation templates; it may not vary educational authority.  
4. **Write/read firewall** — no Twin Update Pipeline bypass; no readiness recomputation.  
5. **No ranking stage** — there is no packaging score that can change which action is suggested.

## 3.5 Explicitly deferred

- Exact copy templates / UX components  
- Exact Recommendation artefact schema  
- Numeric packaging “match %” scores  
- Coach phrasing models  
- Mission batching algorithms (2.10)  

---

# 4. Decision explanation contract

## 4.1 Definition

The **Decision explanation contract** is the structural obligation that Recommendation packaging narrates Decision authority faithfully: selected action, reason codes, candidate contrast, constraint acknowledgements, and lineage — without inventing or contradicting them.

## 4.2 Contract slots (binding)

| Slot | Packaging obligation |
|---|---|
| **Selected action fidelity** | Presented action family and curriculum scope match Decision selected action |
| **Reason-code narration** | Every core Recommendation Reason maps to one or more Decision reason codes |
| **Candidate contrast** | “Why not Y?” uses Decision candidate set statuses only |
| **Constraint honesty** | Feasibility demotions remain visible; packaging does not restore demoted ambition |
| **Lineage citation** | Twin / evidence / curriculum / readiness citations come from Decision lineage |
| **Warrant inheritance** | Readiness-adjacent language inherits Decision warrant posture |
| **Version attribution** | Packaging can name Decision evaluation / reason-code vocabulary version for audit |

## 4.3 Authorship rules

1. **Decision Engine alone authors** reason codes and selected action.  
2. **Recommendation Engine narrates**; it does not invent ranking codes that contradict the Decision.  
3. **LLM / coach may restate** chain-supported attributions; they must not author selection or fabricate lineage.  
4. **Post-hoc stories that disagree with reason codes are forbidden.**  
5. **Factor disagreement remains visible** — High Knowledge + Low Memory (and similar tensions) must not collapse into bland Mid copy.

## 4.4 Forbidden explanation contract breaches

- Softening reason codes to remove educational tension  
- Presenting supportive Knowledge Strength as exam readiness when Decision did not claim readiness  
- Dropping cold-start / low-warrant codes for friendlier engagement copy  
- Adding unofficial reason codes as if they were Decision authority  
- Narrating a different action family than Decision selected (e.g. revise → study collapse)

---

# 5. Warrant propagation

## 5.1 Definition

**Warrant propagation** is the architectural requirement that Evidence Warrant / cold-start / `not_yet_knowable` posture on the Decision flows end-to-end into Recommendation Confidence and student-facing tone.

## 5.2 Propagation path

```
ReadinessState Evidence Warrant / cold-start posture
        ↓
Decision warrant posture (inherited in selection)
        ↓
Recommendation Confidence + explanation tone
```

## 5.3 Propagation rules (binding)

1. **Warrant is non-optional** — packaging may not strip warrant for polish.  
2. **Low warrant → low Recommendation Confidence honesty** — never inflate for engagement.  
3. **`not_yet_knowable` remains first-class** — never rewritten into Mid or High preparedness narratives.  
4. **Readiness language only when Decision cites readiness** — packaging does not introduce preparedness claims Decision did not authorize.  
5. **Performance tag honesty** — string-tag heuristics must not be narrated as scored accuracy certainty.  
6. **No legacy percentage fill** — do not substitute TopicProgress / `ReadinessService` % for missing Twin warrant.

## 5.4 Recommendation Confidence (architectural meaning)

| Term | Meaning | Distinct from |
|---|---|---|
| **Recommendation Confidence** | Appropriateness / evidence-density honesty of the packaged suggestion | Self-report Confidence; Mastery; Readiness overall |

Recommendation Confidence is a **communication honesty posture**, not a selection score and not calibrated student Confidence.

---

# 6. Educational narration

## 6.1 Definition

**Educational narration** is the packaging concern of turning Decision reason codes and explainability-chain layers into student-facing language that preserves educational meaning.

## 6.2 Narration principles (binding)

1. **Truth before polish** — prefer accurate warrant-limited language over confident Mid/High readiness claims.  
2. **Learning value over activity theatre** — do not praise streaks as if they justify harder content when assessed evidence is thin.  
3. **One Decision, one honest suggestion** — packaging clarifies; it does not negotiate a different educational action.  
4. **Name the educational tension** — when Decision preserves Knowledge vs Memory (or Behaviour vs Performance) tension, copy must not collapse it.  
5. **Action families stay separable** — revise ≠ study ≠ assess ≠ diagnostic ≠ rest-protect in language as in Decision.  
6. **Feasibility is educational** — sustainability demotion is a legitimate recommendation story, not failure of ambition.  
7. **Confidence language is dangerous** — disambiguate Recommendation Confidence from self-report Confidence; never imply calibrated Confidence before that domain exists.  
8. **Accept is commitment, not competence** — language around accept/dismiss must not imply mastery change.  
9. **Curriculum-first wording** — name official syllabus identities; never invent “Module X*” labels.  
10. **No engagement theatre urgency** — urgency presentation reflects Decision-derived educational need and constraints, not notification dark patterns.  
11. **Coach may help phrase; coach may not decide** — generative assistance is narration only.  
12. **Comparable reasons beat opaque scores** — prefer factorable Recommendation Reasons over a single composite “match %.”  

## 6.3 Narration ownership

| Concern | Owner |
|---|---|
| Educational factors (reason codes) | Decision Engine |
| Student-facing phrasing of those factors | Recommendation Engine |
| Optional coach rephrase of chain-supported text | Future Insight / Coach surfaces — narration only |

---

# 7. Student context adaptation

## 7.1 Definition

**Student context adaptation** is communication-layer adaptation using Goals, Decision-carried Constraints, Decision Journal history, and Decision-cited Confidence framing — **without** authorizing a second selection path.

## 7.2 Adaptation catalogue

| Context | Allowed packaging use | Forbidden use |
|---|---|---|
| **Goals (sitting, capacity, deadline)** | Scope “toward the sitting” language; capacity-honest duration presentation | Change selected action; invent topics |
| **Constraints on Decision** | Present feasible ambition; explain intensity demotion | Restore demoted polish; erase high-weight need |
| **Decision Journal history** | Avoid thrashing copy; acknowledge prior dismiss respectfully | Treat dismiss as mastery; invent preference Twin writes |
| **Self-report Confidence (Decision-cited)** | Risk-framing narration only | Upgrade mastery/readiness; skip foundations |
| **Behaviour feasibility (Decision-cited)** | Sustainability language when intensity was demoted | Treat streaks as learning-value justification |

## 7.3 Adaptation principles (binding)

1. Context adapts **phrasing and affordances**, not educational authority.  
2. Adaptation must remain **deterministic for attribution** — same Decision + same bound context → same attributable meaning.  
3. Journal-aware packaging respects preference without silent Twin mutation.  
4. Capacity honesty is educational fidelity, not reduced ambition theatre.

---

# 8. Cold-start communication

## 8.1 Definition

Cold-start communication is the packaging posture when Goals may exist, Twin domains are thin, Readiness overall is `not_yet_knowable` / low Evidence Warrant, and Decision prefers **evidence-creating** actions.

## 8.2 Communication posture (binding)

| Do | Do not |
|---|---|
| Say that evidence is still thin / not yet enough to judge preparedness | Claim Mid or High readiness to “motivate” |
| Frame the suggestion as diagnostic / evidence-creating | Frame polish, advanced rehearsal, or “you’re nearly ready” |
| Keep Recommendation Confidence low/honest | Inflate Recommendation Confidence for engagement |
| Cite Decision cold-start / low-warrant reason codes | Invent Mid readiness as packaging convenience |
| Prefer curiosity and clarity (“help us learn where you stand”) | Shame the student for lacking history |
| Preserve curriculum weight honesty when Decision scopes high-weight first coverage | Invent a fake personalised mastery map |

## 8.3 Cold-start principles

1. **Unknown is a first-class message** — not an error state to hide.  
2. **Diagnostics are high-value communication** — evidence-creating actions are not “filler until real recommendations arrive.”  
3. **Warrant inheritance is mandatory** — Decision’s cold-start honesty must survive packaging.  
4. **No coercion** — never rewrite `not_yet_knowable` into Mid preparedness narratives.  
5. **No legacy percentage theatre** — do not fill empty Twin warrant with TopicProgress composites as if Twin-first truth.

## 8.4 Relationship to Decision cold-start

Decision selects evidence-creating actions under low warrant. Recommendation’s job is to **say so clearly**. Packaging that hides diagnostic intent or over-promises preparedness fails educational fidelity even if the underlying Decision was correct.

---

# 9. Explainability preservation

## 9.1 Mandatory chain

Every educational Recommendation must be able to answer **Why?** via:

```
Curriculum factor
    → Learning Evidence (or evidence aggregate)
        → Twin domain state factor(s)
            → Readiness factor (when relevant) + Evidence Warrant
                → Decision Engine reason code(s)
                    → Recommendation explanation
```

Students must never be asked to trust a black box for core next-action advice.

## 9.2 Layer obligations for packaging

| Layer | Packaging obligation |
|---|---|
| **Curriculum** | Present official identity / weight context from Decision lineage — never invented topics |
| **Evidence** | Present evidence ids or honest aggregates when Decision carries them; absence under cold start is honesty |
| **Twin** | Present domain factors Decision cited — preserve disagreements |
| **Readiness** | Present factor posture + warrant only when Decision cites readiness |
| **Decision** | Present reason codes, selected vs considered candidates, constraint acknowledgements |
| **Recommendation** | Complete the chain as actionable suggestion — never invent disagreeing ranking |

## 9.3 Attribution requirements

1. Recommendation Reasons map to Decision reason codes.  
2. Candidate contrast uses Decision candidate set only.  
3. Warrant honesty appears whenever readiness or Twin evidence density is low.  
4. Explanations must not invent evidence, syllabus topics, or Twin beliefs.  
5. LLM / coach narration may only restate chain-supported attributions.  
6. Post-hoc stories that disagree with Decision reason codes are forbidden.  
7. Accepting a Recommendation records preference / intent only — not mastery.

## 9.4 Forbidden explanation patterns

- Single opaque “recommended for you” without factors  
- Explanations that cite UI labels but not Twin/evidence/Decision codes  
- LLM-generated rationales that invent evidence or topics  
- Narrating supportive Knowledge Strength as “you are exam ready”  
- Averaging away High Knowledge + Low Memory tension into a bland Mid story  
- Treating dismissals as proof the topic is mastered  
- Presenting Performance string-tag heuristics as scored accuracy certainty  
- Stripping warrant / cold-start honesty for friendlier engagement copy  
- Hybrid stories that mix legacy readiness % with Twin factors as temporary “truth”  
- Private packaging “match %” as educational authority  

## 9.5 Audit artefacts

| Artefact | Role |
|---|---|
| Learning Evidence log | Immutable history |
| Twin snapshot / domain evidence ids | State lineage |
| ReadinessState attributions + warrant | Preparedness context lineage (when cited) |
| Decision / Decision State | Candidates + selected action + reason codes |
| Recommendation | Product packaging consequence — not authority |
| Decision Journal | User response to recommendations |
| Mission projections (2.10) | Daily structure consequences — not authority |

---

# 10. Mission boundary

## 10.1 Separation of concerns

| Concern | Owner |
|---|---|
| Attributable next-action suggestion packaging | **Recommendation Engine (2.9)** |
| Session/day task-set projection | **Mission Generation Intelligence (2.10)** |

## 10.2 Dependency chain

```
Decision Engine
        ↓
Explainable Recommendation Engine   (optional product surface)
        ↓
Mission Generation Intelligence     (session/day projection from Decision / Decision batches)
        ↓
Mission / MissionTask artefacts
```

Educational Intelligence Architecture allows Mission projection from Decision Engine outputs (or a batch thereof). Recommendation packaging and Mission composition are **sibling projections**, not the same capability.

## 10.3 Boundary rules (binding)

1. **Keep 2.9 and 2.10 separate** — packaging a Decision is not composing today’s mission.  
2. Missions remain **consequences** of intelligence, not the learner model.  
3. Mission rows must **never** store private mastery, readiness, or competing recommendation ranks.  
4. Mission Completion ≠ mastery; Mission Completion ≠ exam readiness; Mission Completion ≠ proof the Recommendation “worked” for learning.  
5. A Mission may surface a recommended action; it must not become a second Decision Engine.  
6. Recommendation Engine outputs Recommendations only — not Mission / MissionTask artefacts.

## 10.4 Firewall

Recommendation outputs Recommendations. Mission Intelligence projects Decisions (and may surface Recommendation language). Neither mutates Twin beliefs. Neither invents syllabus. Neither treats mission or recommendation rows as educational-state authority.

---

# 11. Legacy convergence

## 11.1 Current legacy posture

Product-facing ancestors (`RecommendationService`, TopicProgress-based readiness composites, related planning consumers) currently provide next-action and readiness-like signals without Twin-first Decision authority.

## 11.2 Convergence principle (binding)

Epic 2 requires Decision Engine to become the **authoritative next-action reasoner**, with Recommendation Engine packaging Decision — not inventing a third ranker. Migration is **additive**: preserve behaviour where needed, redirect authority, retire divergent selection truth. Do **not** deepen legacy ranking formulas while Decision-first packaging contracts land. Do **not** hybrid-average legacy % with Twin factors as temporary authority.

## 11.3 Convergence path (architectural stages)

| Stage | Meaning |
|---|---|
| **A — Coexistence** | Legacy recommenders continue for product surfaces; Decision-first Recommendation packaging contracts land without claiming cutover |
| **B — Adapter** | Adapters expose Decision-packaged Recommendations beside legacy ranks; dual truth is explicit and temporary |
| **C — Twin-first Decision packaging authority** | New Educational Intelligence paths consume Decision → Recommendation; legacy ranks cease to be selection/packaging authority |
| **D — Retire divergent math** | Remove or quarantine legacy selection formulas that disagree with Twin-first Decision |

## 11.4 Adapter rules during coexistence

1. Adapters must not silently rewrite Twin beliefs.  
2. Adapters must not present legacy overall % as Twin-first readiness or Decision authority.  
3. Dual truth must be **named** in architecture/docs during coexistence — not papered over as one score.  
4. Recommendation packaging must package Decision, not invent a third ranker.  
5. Mission generation (2.10) must eventually project Decision, not legacy private priority scores as mastery.  
6. Freeze deepening of `RecommendationService.generate_recommendations` heuristics as Twin-first truth.

## 11.5 Explicit non-goals of this milestone

- Implementing adapters  
- Cutting over UI  
- Deleting `RecommendationService`  
- Deepening TopicProgress recommendation math  
- Schema for Recommendation / Decision Journal persistence  

---

# 12. Risks

| Risk | Architectural impact | Mitigation |
|---|---|---|
| **Recommendation invents ranking** | Packaging becomes a secret Decision Engine; Twin-first authority fractures | Package Decision only; never author competing selection/priority lists |
| **Opaque product copy** | Students cannot answer Why?; Epic 2 thesis fails | Mandatory chain packaging; no “recommended for you” without codes |
| **Warrant stripped at presentation** | False preparedness; dishonest cold start | Carry warrant / cold-start honesty into Recommendation Confidence and copy |
| **Post-hoc stories disagree with reason codes** | Broken audit and trust | Narrate Decision codes; forbid contradictory coach/LLM stories |
| **Legacy dual next-action authority** | `RecommendationService` heuristics disagree with Decision | Freeze heuristic deepening; Stage B Decision-first cutover; no hybrid average truth |
| **Accept treated as mastery** | Silent Knowledge/Memory corruption; broken evidence lineage | Accept/dismiss → Decision Journal / Behaviour/Decision history only |
| **Write/read firewall breach** | Recommendation path mutates Twin or recomputes readiness | Packaging is read-side only; no Update Pipeline bypass |
| **Confidence collapse into mastery / readiness** | Optimistic false claims | Separability: Recommendation Confidence ≠ self-report ≠ Mastery ≠ readiness |
| **Domain collapse in copy** | Revise narrated as study; Performance narrated as Knowledge | Preserve action-family and domain separations in packaging |
| **Mission conflation** | Recommendation Engine secretly becomes day planner | Keep 2.10 separate; missions never store private mastery |
| **LLM ownership creep** | Non-determinism; invented syllabus/evidence | Coach narrates chain; Decision selects; Recommendation packages |
| **Premature scoring in packaging** | Unmaintainable “UX scores” become de facto rankers | No numeric selection/ranking formulas inside 2.9 |
| **Curriculum invention / V1 breakage** | Parallel topic trees; broken plans | Canonical identities only; CurriculumContext via canonical helpers before production consumers |
| **Performance tag overclaim** | String-tag heuristics narrated as scored accuracy | Honest, limited assessment language until richer fact schema |
| **Thrashing / preference blindness** | Re-recommend dismissed actions without lineage | Consume Decision Journal context; dismiss ≠ mastery |
| **Parallel learner-state stores** | Divergent “next topic” truths | Twin + Decision as authority; Recommendation projects only |

---

# 13. Extensibility

## 13.1 Extension points

| Future capability | How it extends without breaking architecture |
|---|---|
| **Richer explanation templates** | Add presentation forms over the same Decision codes/lineage; never add private ranking |
| **Multi-language / coach phrasing** | Narrate chain-supported attributions; never invent evidence or selection |
| **Recommendation Confidence bands** | Reflect warrant/evidence-density more finely; still distinct from Mastery and self-report Confidence |
| **Decision Journal personalisation** | Accept/dismiss inform Behaviour and future Decision candidate preference via Evidence → Strategies — not silent Recommendation-side Twin writes |
| **Batch packaging for a session window** | Package an ordered Decision batch; ordering authority remains Decision; Mission Intelligence still owns day structure |
| **Insight / AI Coach surfaces** | Read Recommendation + explanation chain; never silent Twin writes; never own selection |
| **Analytics on reason codes** | Compare Recommendations via codes without opaque scores |
| **Stage B legacy cutover** | Redirect product surfaces from `RecommendationService` heuristics to Decision-first packaging without hybrid formulas |
| **Confidence calibration domain** | May enrich risk-framing narration once owned; still never upgrades mastery/readiness in packaging |
| **Institutional overlays** | Observe Recommendations; do not fork student-owned Twin or invent syllabus |

## 13.2 Compatibility guarantees to preserve

1. Decision Engine remains the only next-action selector.  
2. Recommendation Engine remains packaging / projection only.  
3. Readiness remains preparedness judgement only.  
4. Twin remains sole educational-state authority.  
5. Curriculum V1 and V2 remain loadable; identities via canonical helpers.  
6. Evidence append-only semantics remain permanent.  
7. Deterministic cores remain free of required network LLM calls.  
8. Missions remain projections of Decisions, not of packaging scores.  
9. Accept/dismiss remains preference evidence, not mastery.  

## 13.3 Deliberately unlocked

Not locked by this architecture beyond ownership:

- Exact copy templates / UX components  
- Exact Recommendation artefact schema  
- Exact Decision Journal persistence design  
- Coach phrasing models  
- Mission batching algorithms (2.10)  
- Numeric Decision enrichment (remains Decision-owned if ever approved)  

---

# 14. Educational Fidelity Review

Educational fidelity: prefer honest learning-state representation and learning-value communication over engagement theatre.

## 14.1 Confirmations (binding)

| Commitment | Status |
|---|---|
| **Recommendation is a projection of Decision** | Confirmed — packaging does not re-select |
| **Recommendation never invents ranking** | Confirmed — no competing priority authority |
| **Recommendation never updates Twin domains** | Confirmed — write/read firewall |
| **Recommendation never invents Twin beliefs or syllabus** | Confirmed — cites Decision lineage / Curriculum identities only |
| **Recommendation never coerces unknown readiness** | Confirmed — inherits warrant; cold-start honesty mandatory |
| **Recommendation always remains explainable** | Confirmed — completes mandatory chain; narrates Decision reason codes |
| **Accept ≠ mastery** | Confirmed — journal/evidence preference path only |
| **Recommendation prefers fidelity over engagement theatre** | Confirmed — no Mid/High fabrication, no streak-as-readiness copy |

## 14.2 Fidelity commitments in product language

1. Do not package polish because streaks look good while mocks are missing.  
2. Do not narrate self-report Confidence as permission to skip foundations.  
3. Do not treat accept or mission completion as proof learning occurred.  
4. Do not hide High Knowledge + Low Memory tension behind a single bland suggestion story.  
5. Do not present “study anything” filler when Decision identified high-weight risks.  
6. Do not let coach/LLM invent “do Topic Z” without Decision + Curriculum support.  
7. Do not strip diagnostic intent under cold start to sound more “personalised.”  
8. Do not average legacy readiness percentages into Twin-first recommendation stories.  
9. Do not present rest/protect as failure, or as avoidance when Decision selected it for sustainability.

## 14.3 Anti-fidelity patterns to reject

| Pattern | Why it fails fidelity |
|---|---|
| “Recommended for you” with no reason codes | Opaque; breaks Epic 2 thesis |
| Packaging re-ranks Decision candidates by engagement heuristics | Secret second Decision Engine |
| Cold-start Mid readiness used to sell advanced rehearsal | Fabricates preparedness |
| Confidence slider upgrades recommendation aggressiveness as if mastery | Confidence contamination |
| Recommendation copy that disagrees with Decision reason codes | Broken explainability |
| Accept writes Knowledge/Memory directly | Evidence/Twin bypass |
| Mission generator writing private “priority scores” as mastery | Parallel authority |
| Legacy hybrid % + Twin factors as temporary truth | Dual authority; untrustable |
| LLM invents evidence ids for nicer stories | Audit fraud |
| Inflated Recommendation Confidence under thin warrant | Engagement theatre |

## 14.4 Upstream conditions acknowledged

This architecture accepts and encodes the Educational Reasoning Review conditions relevant to 2.9:

1. Decision Engine remains selection authority.  
2. Explainability chain preserved end-to-end.  
3. No legacy hybrid truth.  
4. Write/read firewall.  
5. Warrant and cold-start honesty.  
6. Confidence separability.  
7. Curriculum V1/V2 invariants; CurriculumContext via canonical helpers before production consumers.  
8. Accept/dismiss is preference, not mastery.  
9. Documentation hygiene remains a follow-up at kickoff (Epic 2 status tables).  
10. No numeric selection/ranking formulas inside Recommendation packaging.  

Also retains Decision / Readiness / Midpoint conditions still in force: Twin sole educational-state authority, no parallel learner-state forks, Missions as consequences, deterministic cores free of LLM ownership.

---

# 15. Recommendations

## 15.1 Implementation sequence (separate milestones)

1. **Structural packaging contracts** — Recommendation / reason narration / warrant posture / journal affordance shapes (still no ranking).  
2. **CurriculumContext builder** — thin orchestration using canonical Curriculum helpers before any live Recommendation consumer.  
3. **Projection skeleton** — Decision in → attributable Recommendation out; cold-start honesty first.  
4. **Decision Journal linkage** — accept/dismiss/defer as preference evidence path (no mastery writes).  
5. **Legacy convergence stages** — adapters → Twin-first Decision packaging authority → retire divergent math.  
6. **Mission Generation Intelligence (2.10)** — only after Recommendation packaging boundaries are locked.  
7. **Optional coach narration** — only as chain-supported rephrase after attribution contracts are proven.

## 15.2 Binding design recommendations

1. Treat packaging as **narration of Decision**, not negotiation with engagement heuristics.  
2. Preserve educational **tensions** (Knowledge vs Memory, Behaviour vs Performance) in Recommendation Reasons.  
3. Prefer **diagnostic honesty** under cold start over personalised Mid theatre.  
4. Keep **Recommendation Confidence** explicitly warrant-tied and vocabulary-disambiguated.  
5. Require **candidate contrast** support early — “why not the other topic?” is educationally load-bearing.  
6. Do not deepen legacy recommendation ranking while Decision-first packaging contracts land.  
7. Keep Mission Generation (2.10) out of 2.9 scope — package first, compose sessions later.  
8. Encode Educational Reasoning Review conditions as packaging invariants before any production consumer.  
9. Plan Stage B cutover so new Educational Intelligence surfaces never treat `RecommendationService.generate_recommendations` / `ReadinessService.get_overall_readiness` as Twin-first authority.  
10. Ship a thin `CurriculumContext` builder (orchestration layer) before any live Recommendation consumer that needs syllabus lineage beyond Decision-carried identities.  
11. Never let packaging invent ranking that disagrees with Decision reason codes.  
12. Never grant mastery on accept.

## 15.3 Architecture compliance checklist

| Invariant | Status for this architecture |
|---|---|
| Twin is sole educational-state authority | Recommendation consumes lineage; does not fork beliefs |
| Evidence is only legitimate belief input | Accept/dismiss becomes evidence via recording paths; packaging does not mutate beliefs |
| Strategies own domain evolution | Recommendation is not a write strategy |
| Decision ≠ Recommendation packaging; Recommendation ≠ Missions; Readiness ≠ next action | Binding |
| Activity ≠ learning value; Confidence ≠ mastery; Behaviour ≠ learning | Binding in communication |
| Curriculum V1/V2 compatibility | Required; canonical identities only |
| No LLM ownership of core selection or fabricated reasons | Binding |
| Recommendation remains a projection of Decision | Binding |
| No implementation / algorithms / ranking in this milestone | Satisfied |

## 15.4 Explicit stop line

This milestone delivers **architecture only**.

**Do not proceed in this milestone to:** code, algorithms, ranking, scoring, optimization, dataclasses, services, tests, database changes, Mission generation design detail, or UI.

**Next engineering step (separate milestone):** structural packaging contracts and/or implementation plan for Capability 2.9 — then implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot lineage may be cited; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains Decision consumed; Recommendation narrates without modification |
| 2.7 | Readiness Aggregation | May appear in explanation when Decision cites readiness; firewall preserved |
| 2.8 | Decision Engine | Supplies Decision authority that Recommendation projects |
| **2.9.1** | **Recommendation Engine Educational Analysis** | Approved educational charter this architecture implements structurally |
| **2.9.2** | **Recommendation Engine Architecture** | **This document** |
| 2.10 | Mission Generation Intelligence | Separate projection into daily structure; not owned here |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.9.2 — Recommendation Engine Architecture |
| Nature | Architecture only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required; no traversal changes introduced |
| Application code intentionally untouched | Yes |
| Upstream gate | Educational Reasoning Review — APPROVED WITH CONDITIONS — conditions encoded herein |
| Prior | Capability 2.9.1 — Recommendation Engine Educational Analysis (approved) |
| Next | Structural packaging contracts / implementation plan (separate milestone) — not started here |

---

*End of Capability 2.9.2 Recommendation Engine Architecture. STOP.*
