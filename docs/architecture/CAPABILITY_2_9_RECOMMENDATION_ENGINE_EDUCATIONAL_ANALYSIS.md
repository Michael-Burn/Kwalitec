# Capability 2.9.1 — Recommendation Engine Educational Analysis

**Status:** Educational / architecture analysis — analysis only  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.9 Explainable Recommendation Engine (educational analysis preceding architecture and implementation)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream gate:** Educational Reasoning Review — APPROVED WITH CONDITIONS ([`docs/reviews/EDUCATIONAL_REASONING_REVIEW.md`](../reviews/EDUCATIONAL_REASONING_REVIEW.md))  
**Companions:** [`CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md), [`CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md`](CAPABILITY_2_8_DECISION_ENGINE_ARCHITECTURE.md), [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md)  
**Scope:** Recommendation Engine definition, educational ownership, input/output boundaries, Decision/Mission relationships, explainability, communication principles, cold-start honesty, risks, fidelity, and ownership principles — **no implementation, algorithms, ranking, services, tests, schema, or migrations**

---

## Document purpose

This milestone answers what the **Explainable Recommendation Engine** is as Epic 2’s product projection of Decision: the educational capability that packages a Decision Engine output into an attributable, student-facing suggestion — without selecting next actions, inventing ranking, mutating Twin beliefs, or composing missions.

Student Digital Twin, Twin Update Pipeline, Knowledge, Memory, Behaviour, Performance, Readiness Aggregation, and Decision Engine are complete (or structurally approved). Educational Reasoning Review conditionally approved Capability 2.9. Recommendation Engine is the next capability. It prepares Capability 2.9 architecture the same way Decision Engine educational analysis prepared 2.8: **educational clarity first**, packaging contracts later, numeric ranking forever forbidden inside this layer.

**Governing principle (binding):**

> **Recommendation remains a projection of Decision.**

**Non-goals of this document**

- Code, pseudocode algorithms, dataclasses, or service refactors  
- Database schemas, Alembic migrations, or ORM layouts  
- Ranking formulas, selection math, priority scores, or optimization objectives  
- UI redesign, gamification, dashboards, notifications, or social features  
- Mission Generation Intelligence design beyond relationship boundaries  
- Replacement of Curriculum Engine, Evidence Model, Twin aggregate, Readiness Aggregation, or Decision Engine contracts  
- Deepening legacy `RecommendationService` heuristics as Twin-first authority  

---

# 1. Definition of Recommendation Engine

## 1.1 Canonical question

> **How is the selected next learning action presented as an attributable suggestion the student can understand, accept, dismiss, or act on?**

Not: what is the highest-value thing to do next (Decision Engine).  
Not: how prepared is the student for the sitting (Readiness).  
Not: what they know / retain / how they study / how they perform (Twin domains).  
Not: how today’s tasks become a mission (Mission Intelligence).  
Not: what ranking or score should override Decision (forbidden — no second reasoner).

Decision Engine answers: *What should we do next?*  
Recommendation Engine answers: *How do we present that Decision honestly and explainably?*

## 1.2 Educational meaning

A **Recommendation** is the **product projection** of a Decision Engine output: a concrete, attributable suggestion the student can accept, dismiss, defer, or act on.

The Recommendation Engine is:

- **read-side packaging only** — it projects a Decision; it does not mutate Knowledge, Memory, Behaviour, Performance, Readiness, or Decision selection;  
- **Decision-bound** — every Recommendation is grounded in a Decision (selected action, candidates, reason codes, lineage, warrant posture);  
- **curriculum-bound** — presented identities remain official syllabus identities from Decision / CurriculumContext lineage, never free-text invention;  
- **explainable by construction** — packaging completes the explainability chain; it never invents reasons that disagree with Decision reason codes;  
- **evidence-honest** — warrant, cold-start, and `not_yet_knowable` postures survive into student-facing communication;  
- **non-authoritative for educational state** — accepting a Recommendation does not grant mastery; completion and assessment evidence do;  
- **deterministic in the core path for attribution** — same Decision in → same attributable Recommendation packaging (no random theatre; no required LLM ownership of reasons).

It is **not**:

- a second next-action selector or ranker;  
- a readiness aggregator or preparedness claim engine;  
- a write-side Twin domain Update Strategy;  
- a mission / week-plan generator;  
- a motivation or engagement optimizer;  
- a black-box coach that invents syllabus, evidence, or Twin beliefs;  
- a permanent home for legacy heuristic recommendation lists that compete with Decision.

## 1.3 Distinctions (binding vocabulary)

| Concept | Educational question | Relation to Recommendation Engine |
|---|---|---|
| **Decision Engine** | What is the highest-value next learning action? | Owns selection; supplies the Decision that Recommendation projects |
| **Recommendation Engine** | How is that Decision packaged as an attributable suggestion? | Owns presentation-quality packaging of Decision outputs |
| **Readiness** | Are we on track for the sitting? | May appear in explanation chain when Decision cites readiness; never selects or ranks via Recommendation |
| **Mission** | What is today’s (or this session’s) task set? | Optional later projection (2.10); not owned by Recommendation packaging |
| **Decision State** | What was decided, among which candidates, with which reasons? | Audit / materialisation artefact of Decision; Recommendation may cite it |
| **Decision Journal** | Did the student accept, dismiss, or defer? | Outcome history; becomes Learning Evidence; Recommendation surfaces the choice, does not redefine mastery |
| **Recommendation Reason** | Why this suggestion? | Narration of Decision reason codes + chain layers — not a private ranking vocabulary that overrides Decision |
| **Recommendation Confidence** | How appropriate is this suggestion given evidence density / warrant? | Evidence-density honesty — distinct from self-report Confidence and from Mastery |
| **Recommendation Priority** | How urgent / ordered is this suggestion relative to others? | Presentation of Decision-derived urgency / ordering — **not** an independent ranking authority |

Governing principle (Educational Intelligence Architecture §13):

> **Every recommendation must be explainable via the evidence → Twin → decision chain.**

Extended for this capability:

> **Recommendation is not Decision; Recommendation is not Readiness; Recommendation is not Mission; Recommendation never invents ranking, syllabus, Twin beliefs, or Mid/High preparedness from thin warrant.**

## 1.4 Product purpose

Recommendation Engine exists so Kwalitec can:

1. Present Decision Engine authority as a **concrete, actionable student-facing suggestion**.  
2. Complete the **explainability chain** with human-readable layers grounded in Decision reason codes and lineage.  
3. Carry **warrant and cold-start honesty** into product language without coercing unknown into readiness theatre.  
4. Enable **accept / dismiss / defer** as preference and intent evidence — not as mastery grants.  
5. Converge legacy recommendation ancestors toward **Decision-first packaging** without inventing a parallel next-action store.

## 1.5 Ubiquitous language anchors

| Term | Meaning |
|---|---|
| **Recommendation** | Product projection of a Decision: attributable suggestion the student can respond to |
| **Recommendation packaging** | Mapping Decision → title/action surface, explanation chain presentation, urgency/duration presentation, citations |
| **Recommendation Reason** | Factorable justification narrated from Decision reason codes + explainability layers |
| **Recommendation Confidence** | Appropriateness / evidence-density honesty for the suggestion — not self-report Confidence, not Mastery |
| **Recommendation Priority** | Presented urgency/order derived from Decision — never a competing selection score invented in packaging |
| **Decision Journal** | Accept / dismiss / defer history for recommendations |
| **Projection** | Downstream packaging that must not change educational authority of the upstream Decision |

---

# 2. Educational Responsibilities

## 2.1 Owns

| Responsibility | Educational meaning |
|---|---|
| **Decision projection** | Package a Decision into a concrete, actionable Recommendation without changing selected action or inventing alternatives that Decision did not consider |
| **Explainability packaging** | Present the mandatory explanation chain (Curriculum → Evidence → Twin → Readiness when cited → Decision reason codes → Recommendation explanation) |
| **Reason narration (not authorship)** | Narrate Decision reason codes and lineage into Recommendation Reasons; never invent codes that contradict Decision |
| **Warrant honesty in communication** | Preserve Evidence Warrant / cold-start / `not_yet_knowable` posture in student-facing language |
| **Actionability** | Make the suggestion map to a clear student action (study / revise / assess / diagnostic / rest-protect) scoped to canonical curriculum identity when applicable |
| **Attribution surface** | Expose Twin / evidence / curriculum / readiness citations already present on the Decision — do not fabricate citations |
| **Response affordance (educational meaning)** | Support accept / dismiss / defer as Decision Journal outcomes that may become Learning Evidence later — without writing Knowledge/Memory beliefs |
| **Recommendation Confidence honesty** | Reflect evidence-density / warrant appropriateness of the packaged suggestion; never inflate confidence for engagement |
| **Legacy convergence posture** | Treat Twin-first Decision packaging as the educational authority path; do not deepen competing heuristic ranking as permanent truth |

## 2.2 Position in the intelligence stack

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

Write path (Evidence → Strategies → Twin) and read path (Twin → Readiness → Decision → Recommendation → Mission) must not be conflated. Recommendation Engine sits entirely on the **read** side for packaging; student responses become evidence later via recording paths.

---

# 3. Non-Responsibilities

| Non-responsibility | Why |
|---|---|
| **Next-action selection** | Decision Engine alone selects; Recommendation must not invent a competing rank, score, or topic priority list |
| **Readiness Aggregation / recomputation** | Preparedness judgement remains Capability 2.7; packaging may cite readiness only when Decision lineage does |
| **Twin domain mutation** | Only Update Strategies via the Twin Update Pipeline may evolve Knowledge, Memory, Behaviour, Performance (and future Confidence) |
| **Learning Evidence authorship (as belief authority)** | Evidence is append-only history; Recommendation does not rewrite the past. Journal outcomes may *become* evidence via product recording — Recommendation does not own Evidence Model |
| **Inventing Curriculum weights / order / topics** | Curriculum Engine / canonical helpers remain syllabus truth; packaging consumes Decision / Curriculum lineage |
| **Mission / plan generation** | Daily task sets and WeekPlan regeneration belong to Mission Intelligence / planning consumers (Capability 2.10 and plan services) |
| **Authoring Decision reason codes** | Reason-code vocabulary and authorship remain Decision Engine ownership; packaging narrates, does not redefine |
| **Scoring / ranking / optimization** | Forbidden in this capability’s educational charter; selection enrichment (if ever) stays inside Decision ownership |
| **LLM ownership of reasons or selection** | Generative assistance may rephrase chain-supported attributions; it must not invent evidence, topics, or a competing Decision |
| **Coercing unknown readiness into Mid/High** | Binding Educational Reasoning Review condition — packaging must inherit honesty |
| **Treating accept as mastery** | Accept/dismiss is preference / intent; Knowledge/Memory change only via evidence of learning |
| **Parallel learner-state stores** | Twin remains educational-state authority; Recommendation must not invent private mastery maps inside suggestion rows |
| **Deepening legacy `RecommendationService` heuristics as Twin-first truth** | Stage A coexistence may continue operationally; educational authority for new intelligence surfaces is Decision-first packaging |

**Hard rule:** If a design needs “recommendation ranked topics independently,” “copy invented why,” “accept wrote mastery,” or “mission stored private readiness,” that design is wrong.

---

# 4. Inputs

Recommendation Engine **consumes** Decision authority and supporting context. It **never modifies** Twin domains, readiness beliefs, or Decision selection. Consumption is observational: same Decision (and bound context) in → same attributable Recommendation packaging out.

## 4.1 Primary input: Decision

| Decision element | Educational role for Recommendation |
|---|---|
| **Selected action** | The only next-action authority to package — action type + curriculum scope when present |
| **Candidate set** | Enables “why this, not that?” explanation without packaging inventing rejected alternatives |
| **Value rationale hooks** | Educational “why now” substance for narration — not marketing slogans |
| **Constraint acknowledgements** | Feasibility / intensity demotion that packaging must not erase or over-claim |

**Binding:** Recommendation packages the Decision’s selected action. It does not re-select among candidates.

## 4.2 Reason Codes

| Input | Educational role |
|---|---|
| **Decision reason codes** | Stable machine-readable factors that Recommendation Reasons must narrate faithfully |
| **Reason-code vocabulary version** | Audit stability — packaging must not silently invent unofficial codes as authority |

**Binding:** Recommendation may clarify language around codes; it may not invent codes that disagree with Decision, nor drop warrant-bearing codes for “friendlier” Mid readiness stories.

## 4.3 Lineage

| Lineage hook | Educational role |
|---|---|
| **Twin snapshot / domain tags** | Ground Twin-layer explanation (“Knowledge weak,” “Memory stale,” “Performance concentrated weakness”) |
| **Curriculum identities** | Ground curriculum-layer explanation and actionable topic/section identity |
| **Evidence ids / aggregates (when present)** | Ground evidence-layer explanation without fabricating attempts |
| **Readiness factors (when Decision cites them)** | Ground readiness-layer explanation only when Decision lineage includes them |
| **Constraint acknowledgements** | Ground feasibility honesty (“smaller session because sustainability risk”) |

**Binding:** Packaging cites lineage that Decision already carries. Absence of evidence ids under cold start is honesty, not a defect to paper over.

## 4.4 Evidence Warrant

| Input | Educational role |
|---|---|
| **Evidence Warrant / warrant posture on Decision / Readiness context** | Determines how boldly packaging may claim preparedness-adjacent language |
| **Cold-start / `not_yet_knowable` posture** | Forces diagnostic / evidence-creating communication honesty |

**Binding:** Warrant must flow end-to-end into Recommendation Confidence and explanation tone. Low warrant never becomes Mid/High preparedness copy.

## 4.5 Student context

Student context informs **communication appropriateness**, not a second selection authority.

| Context | Educational use by Recommendation packaging |
|---|---|
| **Goals (sitting, capacity, deadline)** | Scope language about “toward the sitting” and capacity-honest duration/urgency presentation |
| **Constraints already acknowledged on Decision** | Present feasible ambition; do not upgrade into unsustainable cram theatre |
| **Behaviour feasibility signals (as Decision-cited)** | Support sustainability language when Decision demoted intensity |
| **Decision Journal history (when available)** | Avoid thrashing narration; respect prior dismiss without treating dismiss as mastery |
| **Self-report Confidence (when present)** | May appear only as risk-framing if Decision already framed it that way — never as mastery or readiness upgrade |

**Binding:** Student context does not authorize Recommendation to change selected action, invent topics, or average legacy readiness % into a hybrid story.

## 4.6 Input principles (binding)

1. **Decision is the sole selection authority input** — packaging never re-ranks.  
2. **Reason codes are authored upstream** — packaging narrates; it does not redefine educational factors.  
3. **Lineage is citation, not invention** — no fabricated evidence ids or Twin beliefs.  
4. **Evidence Warrant is non-optional honesty** — cold start and low warrant survive into copy.  
5. **Student context shapes communication, not authority** — Goals/Constraints/Journal inform phrasing and response handling, not a private Decision Engine.  
6. **No legacy hybrid truth** — do not average `ReadinessService` percentages with Twin/Decision factors as temporary packaging authority.  
7. **Curriculum identities remain canonical** — V1/V2 via Decision / CurriculumContext lineage only.

## 4.7 What is not an input authority

- UI streak counters as educational value justification  
- Mission completion counts as mastery proof  
- Opaque “recommended for you” product defaults without Decision  
- Coach/LLM free-text topic invention  
- Legacy `RecommendationService.generate_recommendations` heuristics as Twin-first authority  
- Legacy `ReadinessService` overall % as Decision substitute  

---

# 5. Outputs

## 5.1 Output principle

**The Recommendation Engine outputs a Recommendation only.**

It does not output Decisions, readiness judgements, Twin updates, or mission artefacts. Downstream Mission Intelligence (2.10) may project Recommendations / Decisions into daily structure later.

## 5.2 Recommendation contents (educational meaning — not a schema)

| Recommendation element | Educational meaning |
|---|---|
| **Actionable suggestion** | Concrete student action projected from Decision selected action (study / revise / assess / diagnostic / rest-protect), curriculum-scoped when applicable |
| **Recommendation Reasons** | Narration of Decision reason codes + explainability-chain layers |
| **Explanation chain presentation** | Student-facing answer to Why? across Curriculum / Evidence / Twin / Readiness (when cited) / Decision |
| **Lineage citations** | Twin / evidence / curriculum / readiness hooks carried from Decision |
| **Warrant / Recommendation Confidence posture** | Honest appropriateness given evidence density — never inflated for engagement |
| **Urgency / duration presentation** | Communication of Decision-derived feasibility and timing — not an independent priority optimizer |
| **Candidate contrast (when useful)** | “Why not Y?” drawn from Decision candidate set — never invented |
| **Response affordances** | Accept / dismiss / defer as journalable outcomes |

## 5.3 Explicit non-outputs

| Not an output of Recommendation Engine | Owner |
|---|---|
| Selected next action / re-ranked candidate list | Decision Engine |
| Overall readiness / factor recomputation | Readiness Aggregation |
| Twin belief updates | Update Strategies via Twin Update Pipeline |
| Mission / MissionTask rows | Mission Generation Intelligence (2.10) |
| WeekPlan regeneration | Planning services |
| New Decision reason codes that Decision did not emit | Decision Engine |
| Mastery grants on accept | Forbidden — Learning Evidence of learning only |

## 5.4 Output contract (binding)

1. Every Recommendation must be attributable to a Decision (selected action + reason codes + lineage).  
2. Every Recommendation explanation must be able to walk the mandatory explainability chain.  
3. Every Recommendation that touches readiness language must preserve warrant honesty.  
4. Every curriculum-scoped Recommendation must use canonical identities.  
5. Accepting a Recommendation does not grant mastery; completion / assessment evidence does.  
6. No opaque “do this” without reasons in the core educational path.  
7. No private ranking score as educational authority inside the Recommendation artefact.

---

# 6. Relationship with Decision

## 6.1 Separation of concerns

| Concern | Owner |
|---|---|
| Highest-value next action + reason codes + candidates + lineage + warrant inheritance in selection | **Decision Engine (2.8)** |
| Product packaging of that Decision (action surface, explanation presentation, urgency/duration presentation, journal affordances) | **Explainable Recommendation Engine (2.9)** |

## 6.2 Dependency direction

```
Decision Engine
        ↓
Decision (selected action + candidates + reason codes + lineage + warrant posture)
        ↓
Explainable Recommendation Engine
        ↓
Recommendation (packaged suggestion)
        ↓
Decision Journal (accept / dismiss / defer) → Learning Evidence
```

**One-way authority:** Decision → Recommendation. Recommendation never feeds a competing selection back into Decision within the same reasoning turn.

## 6.3 Binding rules (Educational Reasoning Review conditions encoded)

1. Decision Engine remains **selection authority**.  
2. Recommendation Engine **must not invent ranking** that disagrees with Decision reason codes.  
3. Recommendation Engine **may narrate** chain-supported reasons; it may not invent evidence, syllabus topics, or Twin beliefs.  
4. Recommendation Confidence is distinct from student self-report Confidence and from Mastery.  
5. Accepting a Recommendation does not grant mastery; it records preference / intent evidence only.  
6. Packaging must not introduce numeric selection/ranking formulas “for polish.”  
7. Legacy `RecommendationService` ancestors must converge toward Decision-first authority — additive migration, no permanent parallel selection truth, no hybrid average as temporary truth.

## 6.4 What Recommendation never does in this relationship

- Re-select among Decision candidates  
- Drop or rewrite reason codes to soften educational tension  
- Present supportive Knowledge Strength as exam readiness when Decision did not claim readiness  
- Bypass Decision by writing missions from undocumented private ranks  
- Claim calibrated Confidence while Confidence domain ownership remains incomplete  

## 6.5 Educational consequence

If Decision and Recommendation disagree, **Decision is correct and packaging is wrong**. Product trust depends on that firewall.

---

# 7. Relationship with Mission

## 7.1 Separation of concerns

| Concern | Owner |
|---|---|
| Attributable next-action suggestion packaging | **Recommendation Engine (2.9)** |
| Session/day task-set projection | **Mission Generation Intelligence (2.10)** |

## 7.2 Dependency chain

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

## 7.3 Educational rules

1. **Keep 2.9 and 2.10 separate** — packaging a Decision is not composing today’s mission.  
2. Missions remain **consequences** of intelligence, not the learner model.  
3. Mission rows must **never** store private mastery, readiness, or competing recommendation ranks.  
4. Mission Completion ≠ mastery; Mission Completion ≠ exam readiness; Mission Completion ≠ proof the Recommendation “worked” for learning.  
5. A Mission may include a recommended action; it must not become a second Decision Engine.

## 7.4 Firewall

Recommendation outputs Recommendations. Mission Intelligence projects Decisions (and may surface Recommendation language). Neither mutates Twin beliefs. Neither invents syllabus. Neither treats mission or recommendation rows as educational-state authority.

---

# 8. Explainability

## 8.1 Mandatory chain

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

## 8.2 Explanation layers (educational examples — not formulas)

| Layer | Example content |
|---|---|
| **Curriculum** | “This area carries substantial exam weight.” |
| **Evidence** | “Recent assessed attempts on Topic T were incorrect (evidence ids …).” |
| **Twin** | “Knowledge weak on T; Memory last reinforced long ago; Performance summaries concentrated weakness.” |
| **Readiness** | “Assessment Performance and Memory Stability elevate sitting risk on a high-weight slice; warrant remains limited.” |
| **Decision** | “Revise Topic T now: high weight × retention risk × feasible session length — preferred over new low-weight coverage.” |
| **Recommendation packaging** | Presents the above as an actionable suggestion with reasons — without adding “and you’re Mid ready” theatre |

## 8.3 Attribution requirements

1. Recommendation Reasons map to Decision reason codes.  
2. Candidate contrast uses Decision candidate set only.  
3. Warrant honesty appears whenever readiness or Twin evidence density is low.  
4. Explanations must not invent evidence, syllabus topics, or Twin beliefs.  
5. LLM / coach narration may only restate chain-supported attributions — never author the Decision or fabricate lineage.  
6. Post-hoc stories that disagree with Decision reason codes are forbidden.  
7. Factor disagreement (e.g. High Knowledge + Low Memory) must remain visible — not averaged into bland Mid copy.

## 8.4 Forbidden explanation patterns

- Single opaque “recommended for you” without factors  
- Explanations that cite UI labels but not Twin/evidence/Decision codes  
- LLM-generated rationales that invent evidence or topics  
- Narrating supportive Knowledge Strength as “you are exam ready”  
- Averaging away High Knowledge + Low Memory tension into a bland Mid story  
- Treating dismissals as proof the topic is mastered  
- Presenting Performance string-tag heuristics as scored accuracy certainty  
- Stripping warrant / cold-start honesty for friendlier engagement copy  
- Hybrid stories that mix legacy readiness % with Twin factors as temporary “truth”  

---

# 9. Educational communication principles

These principles bind how Recommendations speak to students — educational fidelity over engagement theatre.

1. **Truth before polish** — prefer accurate warrant-limited language over confident Mid/High readiness claims.  
2. **Learning value over activity theatre** — do not praise streaks as if they justify harder content when assessed evidence is thin.  
3. **One Decision, one honest suggestion** — packaging clarifies; it does not negotiate a different educational action.  
4. **Name the educational tension** — when Decision preserves Knowledge vs Memory (or Behaviour vs Performance) tension, copy must not collapse it.  
5. **Action families stay separable** — revise ≠ study ≠ assess ≠ diagnostic ≠ rest-protect in language as in Decision.  
6. **Feasibility is educational** — sustainability demotion is a legitimate recommendation story, not failure of ambition.  
7. **Confidence language is dangerous** — disambiguate Recommendation Confidence (evidence-density) from self-report Confidence; never imply calibrated Confidence before that domain exists.  
8. **Accept is commitment, not competence** — language around accept/dismiss must not imply mastery change.  
9. **Curriculum-first wording** — name official syllabus identities; never invent “Module X*” labels.  
10. **No engagement theater urgency** — urgency presentation reflects Decision-derived educational need and constraints, not notification dark patterns.  
11. **Coach may help phrase; coach may not decide** — generative assistance is narration only.  
12. **Comparable reasons beat opaque scores** — prefer factorable Recommendation Reasons over a single composite “match %.”  

---

# 10. Cold-start communication

## 10.1 Educational situation

Goals may be set while Twin domains are thin, Readiness overall is `not_yet_knowable` / low Evidence Warrant, and Decision prefers **evidence-creating** actions (diagnostics, early assessments, structured first coverage of high-weight areas).

## 10.2 Communication posture (binding)

| Do | Do not |
|---|---|
| Say that evidence is still thin / not yet enough to judge preparedness | Claim Mid or High readiness to “motivate” |
| Frame the suggestion as diagnostic / evidence-creating | Frame polish, advanced rehearsal, or “you’re nearly ready” |
| Keep Recommendation Confidence low/honest | Inflate Recommendation Confidence for engagement |
| Cite Decision cold-start / low-warrant reason codes | Invent Mid readiness as packaging convenience |
| Prefer curiosity and clarity (“help us learn where you stand”) | Shame the student for lacking history |
| Preserve curriculum weight honesty when Decision scopes high-weight first coverage | Invent a fake personalised mastery map |

## 10.3 Cold-start communication principles

1. **Unknown is a first-class message** — not an error state to hide.  
2. **Diagnostics are high-value communication** — evidence-creating actions are not “filler until real recommendations arrive.”  
3. **Warrant inheritance is mandatory** — Decision’s cold-start honesty must survive packaging.  
4. **No coercion** — never rewrite `not_yet_knowable` into Mid preparedness narratives.  
5. **No legacy percentage theatre** — do not fill empty Twin warrant with TopicProgress composites as if Twin-first truth.  

## 10.4 Relationship to Decision cold-start posture

Decision selects evidence-creating actions under low warrant. Recommendation’s job is to **say so clearly**. Packaging that hides diagnostic intent or over-promises preparedness fails educational fidelity even if the underlying Decision was correct.

---

# 11. Risks

| Risk | Educational / architectural impact | Mitigation |
|---|---|---|
| **Recommendation invents ranking** | Packaging becomes a secret Decision Engine; Twin-first authority fractures | Package Decision only; never author competing selection/priority lists |
| **Opaque product copy** | Students cannot answer Why?; Epic 2 thesis fails | Mandatory chain packaging; no “recommended for you” without codes |
| **Warrant stripped at presentation** | False preparedness; dishonest cold start | Carry warrant / cold-start honesty into Recommendation Confidence and copy |
| **Post-hoc stories disagree with reason codes** | Broken audit and trust | Narrate Decision codes; forbid contradictory coach/LLM stories |
| **Legacy dual next-action authority** | `RecommendationService` heuristics disagree with Decision | Freeze heuristic deepening; Stage B Decision-first cutover; no hybrid average truth |
| **Accept treated as mastery** | Silent Knowledge/Memory corruption; broken evidence lineage | Accept/dismiss → Decision Journal / Behaviour/Decision history only |
| **Write/read firewall breach** | Recommendation path mutates Twin or recomputes readiness | Packaging is read-side only; no Update Pipeline bypass |
| **Confidence collapse into mastery / readiness** | Optimistic false claims | Separability: no Knowledge-held confidence lineage as calibrated Confidence; no self-report upgrade |
| **Domain collapse in copy** | Revise narrated as study; Performance narrated as Knowledge | Preserve action-family and domain separations in packaging |
| **Mission conflation** | Recommendation Engine secretly becomes day planner | Keep 2.10 separate; missions never store private mastery |
| **LLM ownership creep** | Non-determinism; invented syllabus/evidence | Coach narrates chain; Decision selects; Recommendation packages |
| **Premature scoring in packaging** | Unmaintainable “UX scores” become de facto rankers | No numeric selection/ranking formulas inside 2.9 |
| **Curriculum invention / V1 breakage** | Parallel topic trees; broken plans | Canonical identities only; CurriculumContext via canonical helpers before production consumers |
| **Performance tag overclaim** | String-tag heuristics narrated as scored accuracy | Honest, limited assessment language until richer fact schema |
| **Thrashing / preference blindness** | Re-recommend dismissed actions without lineage | Consume Decision Journal context; dismiss ≠ mastery |
| **Parallel learner-state stores** | Divergent “next topic” truths | Twin + Decision as authority; Recommendation projects only |

---

# 12. Future Extensibility

The architecture must allow richer packaging **without changing ownership boundaries**.

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

## 12.1 Compatibility guarantees to preserve

1. Decision Engine remains the only next-action selector.  
2. Recommendation Engine remains packaging / projection only.  
3. Readiness remains preparedness judgement only.  
4. Twin remains sole educational-state authority.  
5. Curriculum V1 and V2 remain loadable; identities via canonical helpers.  
6. Evidence append-only semantics remain permanent.  
7. Deterministic cores remain free of required network LLM calls.  
8. Missions remain projections of Decisions, not of packaging scores.  
9. Accept/dismiss remains preference evidence, not mastery.  

## 12.2 Deliberately unlocked

Not locked by this analysis beyond ownership:

- Exact copy templates / UX components  
- Exact Recommendation artefact schema  
- Exact Decision Journal persistence design  
- Coach phrasing models  
- Mission batching algorithms (2.10)  
- Numeric Decision enrichment (remains Decision-owned if ever approved)  

---

# 13. Educational Fidelity Review

Educational fidelity: prefer honest learning-state representation and learning-value communication over engagement theatre.

## 13.1 Confirmations (binding)

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

## 13.2 Fidelity commitments in product language

1. Do not package polish because streaks look good while mocks are missing.  
2. Do not narrate self-report Confidence as permission to skip foundations.  
3. Do not treat accept or mission completion as proof learning occurred.  
4. Do not hide High Knowledge + Low Memory tension behind a single bland suggestion story.  
5. Do not present “study anything” filler when Decision identified high-weight risks.  
6. Do not let coach/LLM invent “do Topic Z” without Decision + Curriculum support.  
7. Do not strip diagnostic intent under cold start to sound more “personalised.”  
8. Do not average legacy readiness percentages into Twin-first recommendation stories.  
9. Do not present rest/protect as failure, or as avoidance when Decision selected it for sustainability.  

## 13.3 Anti-fidelity patterns to reject

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

## 13.4 Upstream conditions acknowledged

This analysis accepts and encodes the Educational Reasoning Review conditions relevant to 2.9:

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

# 14. Recommendation ownership principles

These principles bind Capability 2.9 educational design and all downstream consumers.

1. **Recommendation Engine packages Decisions; it never invents ranking.**  
2. **Decision Engine alone selects the highest-value next learning action.**  
3. **Readiness judges preparedness; it never selects actions and never becomes packaging authority.**  
4. **Mission Intelligence projects Decisions into daily structure; Recommendation packaging is not mission composition.**  
5. **Plans and missions are consequences of intelligence, not the learner model.**  
6. **Every Recommendation is a projection — authority flows Decision → Recommendation, never the reverse.**  
7. **Every Recommendation must be explainable via the Curriculum → Evidence → Twin → Readiness (when cited) → Decision → Recommendation chain.**  
8. **Recommendation Reasons narrate Decision reason codes; they do not author competing factors.**  
9. **Evidence Warrant and cold-start honesty must survive packaging.**  
10. **Accept / dismiss / defer is preference and intent evidence — never mastery.**  
11. **Recommendation Confidence is evidence-density honesty — not self-report Confidence, not Mastery, not readiness.**  
12. **Curriculum is the only syllabus authority; Recommendations use canonical identities only.**  
13. **Twin is the only educational-state authority; Recommendation consumes lineage, never forks beliefs.**  
14. **Learning Evidence is the only legitimate belief-changing input; journal outcomes enter via evidence recording, not silent Twin writes.**  
15. **No legacy hybrid truth — Decision-first packaging, not averaged TopicProgress theatre.**  
16. **Core packaging attribution is deterministic and free of black-box LLM ownership of reasons or selection.**  
17. **V1 and V2 curricula remain first-class through canonical traversal and identities.**  
18. **Educational fidelity over engagement theatre — always.**  

---

# 15. Recommendations

## 15.1 Architecture milestone that should follow

**Next milestone:** Capability 2.9 Explainable Recommendation Engine **architecture note** (short, binding) — then structural packaging contracts — then implementation in a later milestone.

The architecture note should lock, without algorithms or ranking:

1. Recommendation output contract (actionable suggestion, reasons, explanation chain presentation, warrant/confidence posture, lineage citations, journal affordances)  
2. Input contract: Decision (selected action, candidates, reason codes, lineage, warrant) + student context for communication only  
3. Firewall vs Decision (projection only; no re-selection; no private ranking)  
4. Firewall vs Readiness (cite only when Decision lineage cites; no recomputation; no Mid/High coercion)  
5. Firewall vs Mission Intelligence (2.10 separate; no private mastery in rows)  
6. Explainability packaging rules and forbidden patterns  
7. Cold-start / low-warrant communication posture  
8. Accept/dismiss → Decision Journal / Learning Evidence path (preference, not mastery)  
9. Relationship to legacy `RecommendationService` (convergence path; freeze heuristic deepening; no hybrid temporary truth)  
10. Explicit non-goals: no Twin writes, no readiness recomputation, no mission generation, no scoring/ranking/selection math in packaging  

## 15.2 Educational design recommendations

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

## 15.3 Architecture compliance checklist

| Invariant | Status for Recommendation Engine analysis |
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

This milestone delivers **analysis only**.

**Do not proceed in this milestone to:** code, algorithms, ranking, scoring, optimization, dataclasses, services, tests, database changes, Mission generation design detail, or UI.

**Next engineering step (separate milestone):** Capability 2.9 Recommendation Engine architecture note → structural packaging contracts → implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Recommendation Engine in the capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Twin snapshot lineage may be cited; pipeline remains write-only |
| 2.3–2.6 | Knowledge / Memory / Behaviour / Performance | Belief domains Decision consumed; Recommendation narrates without modification |
| 2.7 | Readiness Aggregation | May appear in explanation when Decision cites readiness; firewall preserved |
| 2.8 | Decision Engine | Supplies Decision authority that Recommendation projects |
| **2.9** | **Explainable Recommendation Engine** | **This analysis precedes architecture and implementation** |
| 2.10 | Mission Generation Intelligence | Separate projection into daily structure; not owned here |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.9.1 — Recommendation Engine Educational Analysis |
| Nature | Architecture / educational analysis only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required going forward; analysis introduces no traversal changes |
| Application code intentionally untouched | Yes |
| Upstream gate | Educational Reasoning Review — APPROVED WITH CONDITIONS |
| Governing principle | Recommendation remains a projection of Decision |
