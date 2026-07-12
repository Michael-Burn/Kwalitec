# Capability 2.6 — Performance Domain Analysis

**Status:** Educational / architecture analysis — analysis only  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.6 Performance Update Strategy (analysis milestone preceding implementation)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Companions:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md), [`CAPABILITY_2_5_BEHAVIOUR_DOMAIN_ANALYSIS.md`](CAPABILITY_2_5_BEHAVIOUR_DOMAIN_ANALYSIS.md)  
**Scope:** Domain definition, boundaries, evidence ownership, beliefs, and relationships — **no implementation, code, tests, schema, or services**

---

## Document purpose

This milestone answers what **Performance** is inside the Student Digital Twin, what it may and must not own, how assessed evidence updates it, what beliefs it may hold, and how it relates to Knowledge, Memory, Behaviour, and Readiness.

It prepares Capability 2.6 implementation (`PerformanceUpdateStrategy`) the same way Knowledge (2.3), Memory (2.4), and Behaviour (2.5) were prepared: **architecture and educational clarity first**, structural write path later, scoring algorithms deferred.

Knowledge, Memory, and Behaviour are complete as prior domains. Performance is the next Digital Twin educational domain under the approved Educational Intelligence Architecture.

**Non-goals of this document**

- Code, pseudocode algorithms, or service refactors  
- Database schemas, Alembic migrations, or ORM layouts  
- Concrete accuracy / IRT / partial-credit / pass-probability formulas  
- UI redesign, analytics dashboards as a second intelligence layer, gamification, or notifications  
- Replacement of Curriculum Engine, Evidence Model, or Twin aggregate contracts  

---

# 1. Definition of Performance

## 1.1 Canonical question

> **How does the student perform when assessed?**

Not: what they know as a durable mastery belief store (Knowledge).  
Not: whether they will still know it when it matters (Memory).  
Not: how they actually study day to day (Behaviour).  
Not: how certain they *feel* (Confidence).  
Not: whether they are on track to pass (Readiness).  
Not: what they should do next (Decision Engine).

## 1.2 Educational meaning

**Performance** is the Twin domain that represents the student’s **measured outcomes under assessment conditions**: scored attempts, quizzes, mocks, past papers, diagnostics, and related assessment trends — scoped to curriculum identities where evidence is topic- or objective-mapped.

In Epic 2 language:

| Concept | Relation to Performance |
|---|---|
| **Study** | May create conditions for assessment; study alone is not Performance |
| **Activity** | Engagement presence — Behaviour’s concern; weak as Performance without scored outcomes |
| **Motivation** | Willingness — may affect whether assessments are attempted; not Performance ownership |
| **Learning** | Durable Knowledge/Memory change — Performance is often the *strongest assessed signal into* learning beliefs, but it remains a distinct domain so assessment trends are not collapsed into mastery or session activity |

Governing principle (Educational Intelligence Architecture §13):

> **Confidence is not mastery; Behaviour is not learning; Activity is not readiness.**

Extended for this domain:

> **Assessment trends are not session activity; Performance is not a second mastery store; a single mock is not the whole readiness story.**

## 1.3 Product purpose

Performance exists so Kwalitec can:

1. Keep **assessment trends visible** as a first-class Twin factor — accuracy, scoped summaries, exam-condition rehearsal — without folding them into Behaviour “study quality.”  
2. Supply the **strongest assessed signal** into Knowledge belief evolution and Readiness Aggregation.  
3. Provide **weak-area and assessment-strength inputs** to the Decision Engine (what to practise under assessment-shaped actions).  
4. Enable later **Confidence calibration** (self-report vs measured accuracy) without collapsing Confidence into mastery.  
5. Support Predictions (pass probability, readiness snapshots) with exam-condition and syllabus-mapped assessment facts — without inventing those forecasts inside Performance itself.

## 1.4 Ubiquitous language anchors

| Term | Meaning |
|---|---|
| **Performance** | Twin domain of how the student performs when assessed |
| **Assessment** | Scored or judged practice against curriculum entities (questions, quizzes, mocks, past papers, diagnostics) |
| **Exam-condition rehearsal** | Timed / mock-style assessment approximating sitting conditions; high reliability for Performance and Readiness narratives |
| **Diagnostic Assessment** | Baseline positioning assessment; evidence, not a permanent label |
| **Performance vs Knowledge** | Measured assessment outcomes / trends vs durable mastery belief structure — complementary, not interchangeable |
| **Calibration** | Alignment of Confidence (self-report) with observed Performance accuracy — Confidence owns the calibration *question*; Performance supplies the measured pole |

---

# 2. Responsibilities

Performance **owns** the educational concern of **assessment outcome structure and assessed-performance facts** inside the Twin.

## 2.1 Owns

| Responsibility | Notes |
|---|---|
| **Assessment references** | Lineage to assessment / attempt evidence ids (append-only references) |
| **Scoped performance summaries** | Structural summaries keyed by scope (topic, quiz, mock, diagnostic, sitting slice, or similar) — facts stored when supplied; computation deferred |
| **Structural performance facts** | Accuracy trends, mistake aggregates, timed-rehearsal metadata *as referenced or stored structure* — not as private scoring engines inside unrelated services |
| **Assessment-condition context (structural)** | Exam-condition vs formative vs diagnostic distinction when evidence carries it |
| **Update ownership** | Future `PerformanceUpdateStrategy` evolves `PerformanceState` from Learning Evidence via the Twin Update Pipeline |

## 2.2 Typical primary evidence (from ownership matrix)

- Quiz / mock / past-paper / diagnostic outcomes (**Primary**, shared with Knowledge as **Primary**)  
- Post-exam outcome (**Primary** for Performance; Knowledge secondary)  
- Question attempt / correct / incorrect (**Secondary** for Performance; Knowledge **Primary**)

## 2.3 Downstream consumers (read-only of Performance)

| Consumer | Uses Performance for |
|---|---|
| **KnowledgeUpdateStrategy** | Assessed outcomes strongly inform mastery beliefs (same evidence batch; separate domain ownership) |
| **Readiness Aggregation** | Assessment strength / weakness factors |
| **Decision Engine** | Assessment weakness signals; prefer assessment-shaped actions when evidence is thin or weak |
| **Confidence path** | Measured pole for over/under-confidence calibration |
| **Mission Generation Intelligence** | Weak-area practice targets without treating missions as score stores |
| **Predictions (later)** | Mock / exam-condition features for pass-probability and readiness snapshots |
| **Analytics / Insight / Coach (later)** | Narrate assessment trends with Twin+evidence lineage — never fork Performance formulas |

## 2.4 Write-path responsibility

Performance beliefs and structural slots change **only** through:

```
Learning Evidence → Twin Update Pipeline → PerformanceUpdateStrategy → new PerformanceState in new Twin snapshot
```

No quiz service, mock scorer, analytics dashboard, or recommendation packager may write Performance “truth” outside that path. Graders and assessment producers emit **Learning Evidence**; they do not mutate Twin domains directly.

---

# 3. Non-responsibilities

Performance must **not** own or silently become:

| Non-responsibility | Why |
|---|---|
| **Daily mission scheduling** | Missions are Decision / Mission Intelligence consequences |
| **Syllabus structure or exam weights** | Curriculum Engine remains syllabus truth |
| **Mastery belief store as Knowledge replacement** | Knowledge owns mastery structure; Performance informs it via evidence, does not absorb it |
| **Retention clocks / Memory beliefs** | Memory owns retention; assessment may reinforce Memory only through Memory’s strategy when evidence warrants |
| **Behaviour adherence / consistency metrics** | Completing assessments is not the same as study cadence ownership |
| **Exam pass probability or readiness composite** | Readiness Aggregation / Predictions derive these; Performance is one input |
| **Next-action selection** | Decision Engine owns selection; Performance supplies assessment weakness |
| **Confidence self-report channel** | Confidence remains separable; Performance is the measured calibration pole, not the feeling store |
| **Mistake taxonomy product UI** | Aggregates may live as structural Performance facts later; UI is a projection |
| **Item bank / question content** | Assessment content lives outside Twin; Performance references outcomes and scopes |
| **Analytics as authority** | Dashboards must share metric definitions with Twin — Analytics never forks readiness/Performance formulas |
| **Persistence, HTTP, Flask, ORM** | Domain strategies stay framework-free |
| **Inventing syllabus topics** | Topic-scoped Performance requires curriculum identity on evidence |

**Hard educational rules**

1. Performance never becomes a second Knowledge mastery store.  
2. High mission adherence never invents strong Performance.  
3. A single mock never becomes the whole readiness or pass-probability story.  
4. Self-reported confidence never overrides dense contrary Performance evidence in educational narrative — Confidence is down-weighted relative to assessed Performance.

---

# 4. Performance beliefs

## 4.1 What “belief” means here

In Educational Intelligence, core Twin domains hold **beliefs** where the system’s claim about the learner is uncertain and evidence-weighted — not binary badges.

For Performance, beliefs are claims such as:

- “Under quiz/mock conditions scoped to *S*, observed accuracy / strength is …”  
- “Assessment evidence for topic *T* is dense / sparse / contradictory …”  
- “Exam-condition rehearsal suggests strength or weakness relative to formative practice …”  

These are **assessment-conditioned** beliefs. They are related to Knowledge mastery beliefs but answer a different question: *measured when assessed*, not *durable know-now structure*.

## 4.2 Belief classes (conceptual — not formulas)

| Belief class | Educational meaning | Locked now? |
|---|---|---|
| **Scoped outcome belief** | Strength/accuracy for a scope (topic, quiz, mock, section slice) | Structure yes; numeric model no |
| **Assessment density / confidence** | How much warrant Performance summaries carry (sparse vs repeated independent outcomes) | Principles yes; weights no |
| **Condition belief** | Formative vs exam-condition vs diagnostic interpretation | Structural tagging yes; scoring no |
| **Trend / trajectory belief** | Improving, flat, or declining assessed outcomes over time | Deferred derived |
| **Mistake-pattern belief** | Recurring error families (conceptual taxonomy) | Deferred; structural aggregates later |
| **Calibration gap (shared)** | Self-report vs measured accuracy | Confidence primary for the gap *concept*; Performance supplies measured facts |

## 4.3 Relationship to Knowledge beliefs

| | Performance belief | Knowledge belief |
|---|---|---|
| **Question** | How do they perform when assessed (scoped)? | What do they know *now* (mastery structure)? |
| **Typical warrant** | Scored outcomes, mocks, quizzes | Same assessments *plus* other evidence channels at domain-appropriate weights |
| **May diverge** | Strong untimed quiz, weak timed mock | Mastery belief may lag or lead Performance depending on evidence mix and decay |

Architecture explicitly allows **mixed batches**: one quiz updates Knowledge *and* Performance. Belief enrichment ordering (e.g. Performance before Knowledge once both compute beliefs) must be intentional at implementation — not decided as math in this analysis.

## 4.4 What Performance beliefs are *not*

- Not a vanity accuracy percentage detached from curriculum scope  
- Not a substitute for Memory retention beliefs  
- Not automatic “mastered” badges from one lucky mock  
- Not Motivation or Confidence feelings  
- Not Decision Engine priority scores  

## 4.5 Cold start and uncertainty

With little assessment evidence, PerformanceState remains sparsely populated. Downstream consumers must treat missing Performance as **explicit low assessment confidence**, not as “assumed weak forever” or “assumed exam-ready.” Cold-start diagnostics raise Performance (and Knowledge) warrant when present; skipping diagnostic must keep assessment confidence low — never fabricate High Performance.

---

# 5. Performance evidence

## 5.1 Ownership relative to Learning Evidence

Learning Evidence is the immutable history. PerformanceState is derived Twin state.

From the Educational Intelligence **Evidence Ownership Matrix**:

| Evidence type (illustrative) | Performance role |
|---|---|
| Quiz / mock / past paper / diagnostic | **Primary** (with Knowledge **Primary**) |
| Post-exam outcome | **Primary** |
| Question attempt / correct / incorrect | **Secondary** (Knowledge **Primary**) |
| Revision session / flashcard review | **—** (Memory primary; not Performance-owned) |
| Mission completed / missed | **—** (Behaviour primary) |
| Skipped / abandoned session | **—** unless the session *was* an assessment abandon — then Behaviour primary for abandon; incomplete assessment may leave a weak/incomplete Performance signal without stealing Behaviour ownership |
| Time on task / study break | **—** |
| Confidence rating / readiness self-review | **—** (Confidence primary; may later calibrate *against* Performance) |
| Plan reschedule / goal change | **—** (does not rewrite historical Performance) |
| Recommendation accept / dismiss | **—** |

## 5.2 Evidence quality principles for Performance

1. **Exam-condition outweighs formative (for Readiness narratives)** — mocks and timed past papers generally dominate short micro-quizzes for assessment-strength stories (Evidence Model principle; no numeric formula here).  
2. **Curriculum attribution mandatory for topic slots** — unmapped free-text “practice” is weak/Unknown for scoped Performance.  
3. **Independence matters** — unaided attempts outrank hinted or heavily scaffolded successes.  
4. **Repetition and diversity raise aggregate warrant** — one correct item ≠ scoped strength; patterns across items/conditions do.  
5. **Contradiction lowers conclusion confidence** — conflicting High-reliability outcomes must remain visible, not silently averaged into false certainty.  
6. **Secondary never steals primary** — a single question attempt may append a weak Performance reference; Knowledge remains primary owner of attempt-type evolution.  
7. **Append-only evidence ids** — Performance references evidence; it never rewrites the log.  
8. **Completion of an assessment session ≠ Behaviour mastery grant** — scored outcomes update Performance/Knowledge; mission wrapper completion remains Behaviour.

## 5.3 Categories feeding Performance

| Category | Performance relevance |
|---|---|
| **Assessment** | Core: questions, quizzes, mocks, past papers, diagnostics |
| **Learning Activity** | Not Performance unless nested scored outcomes arrive |
| **Behaviour** | Abandon mid-assessment may pair Behaviour + incomplete Performance signal |
| **Revision** | Not Performance-primary; Memory owns revision |
| **Confidence** | Calibration consumer of Performance; not a Performance writer |
| **Planning** | Goal/date changes do not erase Performance history |
| **System Events** | Graded system assessments are legitimate Performance producers when typed as Assessment evidence |

## 5.4 Mixed batches (architectural)

A daily mission that embeds a scored quiz is a canonical mixed batch:

- Behaviour **Primary** for mission completed  
- Knowledge **Primary** + Performance **Primary** for quiz outcomes  
- Dual (or triple) strategy application is valid  

Mission completion must not overwrite or replace quiz-driven Performance/Knowledge updates.

---

# 6. Structural vs derived state

Epic 2 repeats the Knowledge / Memory / Behaviour pattern: **structure first, beliefs later**.

## 6.1 Structural Performance (Capability 2.6 target)

The Twin already exposes a structural `PerformanceState` contract conceptually aligned with:

| Structural field | Educational role |
|---|---|
| **assessment_ids** | Lineage to assessment / attempt evidence |
| **performance_summaries** | Scoped structural summaries (`scope_id` + stored facts bag) — **not computed by domain analysis** |
| **last_updated** | Materialisation timestamp for the Performance snapshot |

Structural Performance answers: *What assessment evidence has been observed and linked, and what scoped summary facts have been stored?*

It intentionally does **not** answer: *What is this student’s pass probability?* or *Which IRT ability estimate should we use?*

## 6.2 Derived Performance (deferred)

Derived Performance is computed later by enriched strategies or dedicated consumers:

| Derived concept | Likely future owner | Notes |
|---|---|---|
| **Accuracy / strength trends** | Performance enrichment | Per topic/objective/scope windows |
| **Mistake taxonomy aggregates** | Performance enrichment | Conceptual taxonomies may evolve |
| **Exam-condition vs formative delta** | Performance / Predictions | Timed mock may diverge from untimed mastery |
| **Item / objective grain models** | Performance + richer banks | Partial credit, multi-part items |
| **Cross-sitting baselines** | Predictions / Analytics (read Twin) | Privacy-preserving; no peer exposure requirement in Epic 2 |
| **Pass-probability features** | Predictions consuming Performance | Performance supplies inputs; does not own the composite |
| **Learning velocity (assessment-adjusted)** | Cross-domain derivation | Must not redefine mastery or Behaviour consistency |

## 6.3 Boundary rules

1. Structural strategy must **preserve unknown summary fields** when not computing them (same discipline as `mastery_belief` / `retention_belief` / Behaviour metric bags).  
2. Derived metrics must remain **factorable and explainable** when shown to students or used in decisions.  
3. Derived Performance must **not** become a second readiness composite or a second Knowledge mastery store.  
4. Analytics projections of Performance must **share definitions** with Twin — never fork.  
5. Summaries store facts; they must not become opaque blobs without evidence lineage.

## 6.4 Implementation implication (analysis only)

Capability 2.6 implementation should ship a **structural `PerformanceUpdateStrategy`**, analogous to Knowledge / Memory / Behaviour:

- `supports` on Performance-primary (and carefully documented secondary) evidence types  
- append/update `assessment_ids`, scoped `performance_summaries`, and `last_updated`  
- no accuracy engines, IRT, partial-credit math, or pass-probability  

Numeric Performance engines remain deliberately unlocked (Educational Intelligence Architecture §11.3).

## 6.5 Pipeline ordering note

Architecture requires intentional registration order when strategies interact (e.g. Performance before Knowledge belief enrichment once both compute beliefs). Structural phase may register Performance adjacent to Behaviour/Knowledge once Capability 2.5–2.6 architecture notes fix order for mixed assessment batches. This analysis does not hard-code a final order — it requires that order be **documented before coding**.

---

# 7. Relationship with Knowledge

## 7.1 Complementary questions

| Domain | Question |
|---|---|
| **Knowledge** | What does the student know *now*? |
| **Performance** | How does the student perform when assessed? |

## 7.2 Allowed interactions

- Assessed outcomes **strongly inform** mastery beliefs — shared primary evidence on quizzes/mocks/diagnostics is intentional.  
- Performance summaries supply Decision Engine “assessment weakness” while Knowledge supplies “mastery gap” — often correlated, sometimes divergent (e.g. untimed vs timed).  
- Cold-start diagnostics feed both domains; both must mark low confidence when diagnostic is skipped.  
- Post-exam outcomes: Performance primary; Knowledge may take a secondary update without Performance absorbing mastery ownership.

## 7.3 Forbidden interactions

| Anti-pattern | Why forbidden |
|---|---|
| Performance stores `mastery_belief` as its only truth | Domain collapse |
| Knowledge strategy absorbs all Performance summary ownership | Hides assessment trends as a distinct factor |
| One strong mock → permanent High mastery with no decay/context | Overclaim; ignores Memory/time and evidence quality |
| Treating Performance accuracy % as syllabus coverage | Coverage is Knowledge/Curriculum-weighted; accuracy ≠ coverage |

## 7.4 Educational takeaway

Strong Performance with thin Knowledge structure means assessed signals exist but mastery slots may still be incomplete or low-confidence.  
Strong Knowledge claims with thin Performance mean the Twin may be over-trusting non-assessed or sparse channels — Decision Engine should favour assessment-shaped actions. Keep both visible so explanations stay honest (“mock weakness on Topic T” vs “mastery belief still low on Topic T”).

---

# 8. Relationship with Memory

## 8.1 Complementary questions

| Domain | Question |
|---|---|
| **Memory** | Will the student still know it when it matters? |
| **Performance** | How does the student perform when assessed (now / under conditions)? |

## 8.2 Allowed interactions

- Correct assessed outcomes may update Memory’s `last_reinforced` / retention structure **via MemoryUpdateStrategy** when evidence is topic-scoped — Performance does not store retention clocks.  
- A strong past mock can coexist with high Memory risk if reinforcement is stale — Readiness must see both factors.  
- Revision evidence remains Memory-primary; it must not be reclassified as Performance merely because it feels “test-like.”

## 8.3 Forbidden interactions

| Anti-pattern | Why forbidden |
|---|---|
| Performance stores `retention_belief` | Domain collapse |
| Flashcard correctness treated as full exam-condition Performance | Wrong reliability class; Memory primary |
| Old high mock freezes retention forever | High past scores do not freeze Retention |
| Skipping Memory update because a Performance summary exists | Complementary domains; both may need evolution |

## 8.4 Educational takeaway

Performance describes assessed competence under observed conditions; Memory describes durability toward the sitting. A student can mock well in March and still face retention risk in June. Explain both — do not merge into one “they’re fine” score.

---

# 9. Relationship with Behaviour

## 9.1 Distinct questions

| Domain | Question |
|---|---|
| **Performance** | How does the student perform when assessed? |
| **Behaviour** | How does the student actually study day to day? |

## 9.2 Allowed interactions

- Quizzes/mocks: Performance (+ Knowledge) primary; Behaviour may record secondary session engagement.  
- Abandoned assessments: Behaviour (abandon) + incomplete Performance signal — dual update is valid; ownership remains split.  
- Decision Engine uses Performance weakness for *what* to practise and Behaviour for *how hard / how soon* is feasible.  
- Architecture principle: learning over activity — prefer actions that move Knowledge/Memory/**Performance**, not empty completion.

## 9.3 Forbidden interactions

| Anti-pattern | Why forbidden |
|---|---|
| High mission adherence → “strong Performance” | Adherence ≠ assessed accuracy |
| Collapsing Performance into Behaviour “study quality” | Hides assessment trends — the reason Performance is a distinct domain |
| Behaviour owns mock score summaries | Performance domain exists precisely to prevent that collapse |
| Treating time-on-task as Performance accuracy | Time ≠ assessed outcome |

## 9.4 Educational takeaway

A student can complete every mission and still fail mocks (activity without assessed learning).  
A student can score well on sparse assessments and still show fragile Behaviour (unsustainable practice). Both must remain visible as separate Twin factors — Behaviour Domain Analysis §10 and this charter agree.

---

# 10. Relationship with Readiness

## 10.1 Readiness is derived

Readiness answers: *Are we on track to pass?*  
Performance answers: *How does the student perform when assessed?*

Readiness Aggregation (Capability 2.7) consumes Performance as **one factor class** among:

```
Curriculum weights + Knowledge + Memory + Performance
+ Behaviour consistency / pace
+ Confidence calibration (optional)
+ Goals (exam date, capacity)
```

## 10.2 Performance’s contribution to Readiness

Architectural factor roles (names illustrative):

| Factor family | Performance contribution |
|---|---|
| **Assessment strength** | Scoped summaries, mock/exam-condition signals |
| **Assessment weakness / risk concentration** | High-weight topics with weak Performance slices |
| **Evidence warrant** | Sparse vs dense assessment history affects confidence in readiness claims |
| **Condition gap** | Timed mock weakness vs untimed practice — readiness must not ignore exam-condition risk |

## 10.3 What Performance must not do to Readiness

- Emit the overall readiness composite inside `PerformanceUpdateStrategy`  
- Treat a single mock score as pass probability  
- Treat Performance as equivalent to weighted syllabus coverage  
- Bypass factorability with an opaque “performance score” that cannot be explained  
- Require Sections globally (breaks V1) when contributing scoped facts  

## 10.4 Decision Engine vs Readiness

| Concern | Owner | Performance’s role |
|---|---|---|
| On track for sitting? | Readiness Aggregation | Assessment strength/weakness factor |
| What to do in the next session? | Decision Engine | Assessment weakness → assessment-shaped or remediation actions |

Same PerformanceState; different read-side questions. Do not conflate them.

---

# 11. Example educational scenarios

## 11.1 Steady adherent, thin assessment

**Situation:** Student completes missions five days/week for three weeks; almost no quizzes.

**Twin reading:** Behaviour structural adherence lineage is rich; Performance (and often Knowledge warrant) remain sparse.

**Correct intelligence:** Do not declare readiness from Behaviour. Decision Engine should favour assessment-shaped actions that create Performance/Knowledge evidence, within Behaviour feasibility.

## 11.2 Strong mocks, irregular practice

**Situation:** Strong Performance on mocks; irregular mission adherence.

**Twin reading:** Performance/Knowledge optimistic relative to Behaviour pace risk vs remaining calendar.

**Correct intelligence:** Readiness may still flag time/pace risk. Decision Engine balances retention/coverage needs against feasibility — Behaviour constrains ambition without erasing Performance evidence.

## 11.3 Untimed quiz strong, timed mock weak

**Situation:** High formative quiz accuracy on Topic T; timed mock section on T is weak.

**Twin reading:** Performance summaries diverge by condition; Knowledge may sit between signals depending on strategy weighting (deferred math).

**Correct intelligence:** Keep condition visible in explanations. Readiness/Decision should not treat formative strength as exam-condition readiness. Prefer exam-condition rehearsal for high-weight weak slices.

## 11.4 Mission complete with embedded quiz

**Situation:** Daily mission includes a scored quiz on Topic T; student completes the mission.

**Twin reading:** Mixed batch — Behaviour primary for mission completed; Knowledge + Performance primary for quiz outcomes.

**Correct intelligence:** Dual/triple strategy application is valid. Mission completion must not overwrite quiz-driven Performance updates.

## 11.5 Abandoned mid-mock

**Situation:** Student starts a timed mock, abandons halfway.

**Twin reading:** Behaviour records abandon; Performance may hold incomplete assessment reference / partial summary with reduced warrant.

**Correct intelligence:** Do not invent full-mock Performance strength from a partial attempt. Do not treat abandon as mastery loss by itself. Decision may recommend shorter assessment-shaped tasks if abandon patterns recur.

## 11.6 Overconfident self-report vs weak quizzes

**Situation:** Student rates Confidence high on Topic T; quiz/mock Performance on T is repeatedly weak.

**Twin reading:** Confidence primary for ratings; Performance primary for assessed outcomes; calibration gap is first-class.

**Correct intelligence:** Decision Engine risk-framing may demote self-report; never let Confidence override dense Performance. Explain both poles — do not silently average into false mastery.

## 11.7 Cold-start without diagnostic

**Situation:** New Twin; Goals set; no assessments yet.

**Twin reading:** Empty Performance references; unknown assessment strength.

**Correct intelligence:** Explicit low assessment confidence; prefer diagnostic or early assessment-shaped actions. Never fabricate High Performance or High readiness from Goals alone.

## 11.8 Post-exam outcome after sitting

**Situation:** Official sitting result arrives as post-exam evidence.

**Twin reading:** Performance primary; Knowledge secondary; Goals/Decision State may take secondary updates.

**Correct intelligence:** Historical Performance remains audit lineage for future Predictions calibration. Do not delete prior evidence. Re-sit Goals may reset Planning while preserving Performance history (Twin lifecycle).

## 11.9 High-weight weakness concentration

**Situation:** Performance weak on a small set of high exam-weight topics; strong on low-weight topics.

**Twin reading:** Performance summaries show concentrated risk; Curriculum weights amplify readiness concern.

**Correct intelligence:** Readiness risk concentration and Decision Engine curriculum-weighted value must prefer high-weight weak areas over low-weight polish when time is scarce — Performance supplies the weakness signal; Curriculum supplies weight; Decision Engine selects.

---

# 12. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| **Domain collapse into Knowledge** | Unexplainable dual mastery; lost assessment-condition nuance | Complementary questions; ownership matrix; separate `PerformanceState` |
| **Domain collapse into Behaviour** | Assessment trends hidden as “study quality” | Distinct domain; Behaviour never owns mock summaries |
| **Single-mock overclaim** | False readiness / pass narratives | Factorable Readiness; evidence quality principles; mocks outweigh quizzes but do not alone equal pass probability |
| **Mission completion as Performance** | Activity theatre replaces assessed learning | Ownership matrix; mixed-batch rules |
| **Analytics formula fork** | Divergent dashboards vs Twin | Analytics reads Twin; shared metric definitions |
| **Confidence overrides Performance** | Optimistic false readiness | Confidence separable; down-weighted vs assessed Performance |
| **Hinted success as exam strength** | Inflated Performance warrant | Independence / scaffolding metadata on evidence |
| **Unmapped practice as topic Performance** | Invented syllabus signal | Curriculum identity mandatory for topic slots |
| **Strategy order hazards** | Non-reproducible updates on mixed batches | Document registration order in Capability 2.6 architecture notes before coding |
| **Premature scoring complexity** | Unmaintainable IRT/accuracy math before structure settles | Structural strategy first; derived metrics later |
| **Partial attempts treated as full mocks** | Misleading exam-condition beliefs | Incomplete-assessment warrant rules |
| **LLM-invented scores / weak areas** | Fabricated Performance | Coach narrates Twin+evidence only |
| **V1/V2 breakage** | Section-required Performance logic | Nullable sections; canonical traversal; never invent topics |
| **Parallel Performance stores in quiz services** | Divergent learner state | Evidence → strategy → Twin only |
| **Post-exam erasure of history** | Broken calibration / audit | Append-only evidence; preserve Performance lineage across re-sits |

---

# 13. Future extensibility

## 13.1 Safe extension points

| Extension | How to extend safely |
|---|---|
| **`PerformanceUpdateStrategy`** | Register with Twin Update Pipeline; framework-free; immutable snapshots |
| **Richer scoped summaries** | Fill `performance_summaries` facts via later engines; keep structural slots stable |
| **New Assessment evidence types** | Add to Evidence catalogue; assign primary/secondary in ownership matrix |
| **Objective / item grain** | Additive scopes referencing Learning Objectives / items; Curriculum remains authority |
| **Partial-credit / multi-part items** | Derived enrichment; structural summaries remain additive |
| **Exam-style item types** | Evidence metadata + Performance interpretation; no Twin syllabus invention |
| **Mistake taxonomy** | Structural aggregates with lineage; taxonomies may evolve without breaking snapshots |
| **Cross-sitting baselines** | Prediction/Analytics features reading Performance; privacy-preserving aggregates only |
| **Confidence calibration engines** | Consume Performance as measured pole; Confidence remains separable |
| **Prediction features** | Pass probability / readiness snapshots read Performance; write via Prediction path only |

## 13.2 Compatibility guarantees to preserve

1. Curriculum V1 and V2 remain loadable; Performance must not require Sections globally.  
2. Structural Twin fields prefer additive optional fields over breaking renames.  
3. Evidence append-only semantics remain permanent.  
4. Deterministic cores remain free of required network LLM calls.  
5. Knowledge and Memory remain complementary mastery/retention stores — Performance must not become a third mastery store.  
6. Behaviour remains the study-practice domain — Performance must not absorb adherence.

## 13.3 Deliberately unlocked

Not locked by this analysis beyond ownership:

- Exact accuracy / strength formulas  
- IRT / BKT / heuristic mastery bridges from Performance → Knowledge  
- Mistake taxonomy schemes  
- Partial-credit models  
- Numeric readiness weights on assessment factors  
- Pass-probability models  
- Cohort benchmarking bands  

---

# 14. Educational fidelity considerations

Educational fidelity is a binding Epic 2 principle: **prefer honest learning-state representation over engagement theatre**.

## 14.1 Fidelity commitments for Performance

1. **Assessed outcomes remain visible** — do not hide weak mocks behind streak or completion narratives.  
2. **Condition honesty** — formative success must not be narrated as exam-condition readiness.  
3. **Uncertainty honesty** — sparse Performance is “we don’t know yet,” not “you’re behind” theatre or “you’re fine” marketing.  
4. **No vanity accuracy** — percentages without curriculum scope, evidence lineage, or condition context fail fidelity.  
5. **No gamified score chasing as Twin authority** — leaderboards or badge accuracy, if ever productised outside Epic 2, remain projections — never Performance truth.  
6. **Calibration humility** — overconfidence and underconfidence are educational signals, not shame metrics; still, self-report does not outrank assessed Performance.  
7. **Learning over activity** — Decision Engine should prefer actions that create genuine Performance/Knowledge/Memory movement when assessment evidence is thin.  
8. **Explainability** — every student-facing Performance claim should be traceable: evidence → PerformanceState → factor → recommendation/readiness narrative.

## 14.2 Anti-fidelity patterns to reject

| Pattern | Why it fails fidelity |
|---|---|
| “100% mission week” banner implying exam readiness | Activity ≠ Performance ≠ Readiness |
| Inflating mastery from easy hinted quizzes | Independence and difficulty ignored |
| Erasing a bad mock because it demotivates | Evidence honesty over comfort theatre |
| Coach inventing “you’re strong on Section C” without Twin support | LLM ownership creep |
| Dashboard “performance score” that disagrees with Twin | Parallel intelligence layer |

## 14.3 Fidelity relative to sibling domains

Performance protects fidelity **between** domains: it prevents Behaviour from pretending to be assessed competence, prevents Knowledge from losing assessment-condition nuance, and prevents Readiness from being a single opaque mock number. Keeping Performance distinct is itself an educational fidelity mechanism.

---

# 15. Recommendations

## 15.1 For Capability 2.6 next milestones

1. **Treat this analysis as the domain charter** for Performance before writing `PerformanceUpdateStrategy`.  
2. **Implement structural-only strategy first** — mirror Knowledge / Memory / Behaviour discipline: `assessment_ids`, scoped summaries, timestamps, preserve unknown summary fields, no scoring.  
3. **Fix evidence `supports` types explicitly** — primary: quiz / mock / past paper / diagnostic / post-exam outcome; secondary: question attempts only with documented weak updates.  
4. **Document pipeline registration order** relative to Knowledge / Memory / Behaviour before coding (mixed assessment batches must stay reproducible).  
5. **Do not expand Performance into Knowledge or Readiness** — inform them; do not absorb them.  
6. **Keep Confidence separable** — Performance supplies measured calibration facts; Confidence owns self-report.  
7. **Keep missions as projections** — Mission Generation consumes Performance weakness; it does not own Performance truth.  
8. **Align Analytics early** — any dashboard assessment metrics must read Twin Performance definitions, not fork formulas.

## 15.2 Educational design recommendations

1. Prefer **condition-aware explanations** (“timed mock” vs “practice quiz”) over a single accuracy number.  
2. Always separate “you showed up” (Behaviour), “you demonstrated assessed competence” (Performance), and “you likely still know it” (Memory).  
3. Use Performance to **reveal assessment risk**, not to inflate readiness from one good day.  
4. When Behaviour is strong and Performance is thin, recommend **assessment-shaped** next actions — fidelity over completion theatre.  
5. When Performance is strong and Behaviour is fragile, protect the assessment signal while constraining intensity — do not erase mocks because adherence slipped.

## 15.3 Architecture compliance checklist

| Invariant | Status for Performance |
|---|---|
| Twin is sole educational state authority | PerformanceState lives only in Twin |
| Evidence is only legitimate belief input | Required |
| Strategies own domain evolution | `PerformanceUpdateStrategy` planned |
| Performance ≠ Behaviour; Performance ≠ Knowledge store; Activity ≠ readiness | Binding |
| V1/V2 curriculum compatibility | Performance must not invent syllabus or require V2-only structure |
| No implementation in this milestone | Satisfied by analysis-only deliverable |

## 15.4 Explicit stop line

This milestone delivers **analysis only**.

**Do not proceed in this milestone to:** code, tests, database changes, services, scoring formulas, or UI.

Next engineering step (separate milestone): Capability 2.6 architecture notes for `PerformanceUpdateStrategy` → structural implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Performance in the capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | PerformanceState already part of Twin vocabulary; pipeline will register Performance strategy later |
| 2.3–2.4 | Knowledge / Memory strategies | Structural precedents Performance must follow; complementary domain interactions |
| 2.5 | Behaviour Update Strategy | Complete prior domain; secondary session signals only for assessments |
| **2.6** | **Performance Update Strategy** | **This analysis precedes implementation** |
| 2.7 | Readiness | Consumes Performance as assessment strength/weakness factor |
| 2.8–2.10 | Decision / Recommendation / Missions | Read Performance for assessment weakness; write back via evidence |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.6 — Performance Domain Analysis |
| Nature | Architecture / educational analysis only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required going forward; Performance analysis introduces no traversal changes |
| Application code intentionally untouched | Yes |
| Next | Performance Update Strategy architecture → structural implementation (separate milestone) |

---

*End of Capability 2.6 Performance Domain Analysis.*
