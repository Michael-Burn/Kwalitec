# Capability 2.6 — Performance Update Strategy Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.6 Performance Update Strategy  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Domain charter:** [`CAPABILITY_2_6_PERFORMANCE_DOMAIN_ANALYSIS.md`](CAPABILITY_2_6_PERFORMANCE_DOMAIN_ANALYSIS.md)  
**Companions:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md), Twin domain README (`app/domain/twin/README.md`), [`CAPABILITY_2_5_BEHAVIOUR_UPDATE_STRATEGY.md`](CAPABILITY_2_5_BEHAVIOUR_UPDATE_STRATEGY.md)  
**Scope:** Structural write-path architecture for `PerformanceUpdateStrategy` — **no code, services, tests, schemas, or scoring formulas**

---

## Document purpose

This milestone defines **how** Performance evolves inside the Student Digital Twin when Learning Evidence arrives.

It follows Capability 2.3 (Knowledge), 2.4 (Memory), and 2.5 (Behaviour): **structure first, beliefs later**. It translates the approved Performance Domain Analysis into update-strategy architecture that can be implemented in a later milestone without redesigning Twin, Evidence, or Curriculum contracts.

**Non-goals of this document**

- Code, pseudocode algorithms, or package layouts beyond conceptual names  
- Database schemas, Alembic migrations, or ORM layouts  
- Concrete accuracy / IRT / partial-credit / pass-probability formulas  
- UI, analytics dashboards as a second intelligence layer, gamification, or notifications  
- Replacement of Curriculum Engine, Evidence Model, Twin aggregate, or Twin Update Pipeline contracts  

**Hard educational rules (binding):**

1. Performance never becomes a second Knowledge mastery store.  
2. High mission adherence never invents strong Performance.  
3. A single mock never becomes the whole readiness or pass-probability story.  
4. Self-reported confidence never overrides dense contrary Performance evidence in educational narrative.

**Governing principle:** Assessment trends are not session activity; Performance is not a second mastery store; a single mock is not the whole readiness story.

---

# 1. PerformanceState

## 1.1 Position

`PerformanceState` is the Twin domain that answers:

> **How does the student perform when assessed?**

It sits beside Knowledge, Memory, Behaviour, Confidence (separable), Goals, Identity, and Prediction snapshots inside the immutable `DigitalTwin` aggregate.

## 1.2 Architectural properties

| Property | Requirement |
|---|---|
| **Evidence-backed** | Evolves only from Learning Evidence via `PerformanceUpdateStrategy` |
| **Immutable per snapshot** | Updates produce a new Twin snapshot; never mutate in place |
| **Structural-first** | Assessment references, scoped summaries, timestamps, and fact *slots* before scoring |
| **Curriculum-referenced when scoped** | Topic/objective scopes require curriculum identity on evidence; never invent syllabus trees |
| **Condition-aware** | Exam-condition vs formative vs diagnostic distinction is structural when evidence carries it |
| **Non-authoritative for readiness composites** | Supplies assessment strength/weakness factors; does not emit pass probability |

## 1.3 Structural shape (conceptual contract)

Prefer the existing Twin vocabulary. Capability 2.6 must not redesign Performance for scoring. Additive optional fields are allowed if lineage requires them (same discipline as Knowledge/Memory/Behaviour).

| Structural field | Educational role | Structural strategy duty |
|---|---|---|
| **assessment_ids** | Lineage to assessment / attempt evidence | Append (dedupe) when primary/secondary assessment evidence applies |
| **performance_summaries** | Scoped structural summaries (`scope_id` + stored facts bag) | Create/extend scopes when evidence supplies scope identity and stored facts; **do not** compute accuracy engines |
| **last_updated** | Materialisation timestamp for this Performance snapshot | Set from latest processed applicable evidence timestamp |
| **Optional additive lineage** (if required) | e.g. state-level `evidence_ids`, condition tags on summaries | Prefer additive optional fields over breaking renames |

Structural Performance answers: *What assessment evidence has been observed and linked, and what scoped summary facts have been stored?*

It intentionally does **not** answer: *What is this student’s pass probability?* or *Which IRT ability estimate should we use?*

## 1.4 What PerformanceState is not

- A second Knowledge mastery belief store  
- A Behaviour “study quality” aggregate or mission completion cache  
- A readiness composite or pass-probability engine  
- An item bank or question-content store  
- A mutable accuracy counter that bypasses evidence  
- A Confidence self-report channel  

## 1.5 Cold start

Empty `assessment_ids` and empty `performance_summaries` are valid. Downstream consumers (Decision Engine, Readiness, Planning) must treat missing Performance as **explicit low assessment confidence** — never as “assumed weak forever” or “assumed exam-ready.” Skipping diagnostic must keep assessment warrant low — never fabricate High Performance.

---

# 2. Performance evidence ownership

## 2.1 Ownership relative to Learning Evidence

Learning Evidence is the immutable history. `PerformanceState` is derived Twin state.

From the Educational Intelligence **Evidence Ownership Matrix**:

| Evidence type (illustrative) | Performance role | Structural effect (architecture) |
|---|---|---|
| Quiz / mock / past paper / diagnostic | **Primary** (with Knowledge **Primary**) | Assessment lineage; scoped summary materialisation; `last_updated` |
| Post-exam outcome | **Primary** | Assessment lineage; sitting-scoped summary facts when supplied |
| Question attempt / correct / incorrect | **Secondary** (Knowledge **Primary**) | Weak assessment reference only; must not steal Knowledge ownership |
| Revision session / flashcard review | **—** | Memory primary; not Performance-owned |
| Mission completed / missed | **—** | Behaviour primary |
| Skipped / abandoned session | **—** unless assessment abandon | Behaviour primary for abandon; incomplete Performance signal allowed without stealing Behaviour |
| Time on task / study break | **—** | Behaviour primary |
| Confidence rating / readiness self-review | **—** | Confidence primary; may later calibrate *against* Performance |
| Plan reschedule / goal change | **—** | Does not rewrite historical Performance |
| Recommendation accept / dismiss | **—** | Decision State primary |

## 2.2 Primary vs secondary rules

1. **Primary** evidence **must** evolve Performance when `supports` matches.  
2. **Secondary** evidence **may** append weak assessment references; it must **not** steal primary ownership from Knowledge (attempt types), Memory, Behaviour, Confidence, Goals, or Decision State.  
3. Mixed batches are valid (e.g. mission completed + embedded quiz).  
4. Domains reference evidence ids; they never rewrite the evidence log.  
5. Topic-scoped Performance requires curriculum identity on evidence — unmapped free-text “practice” is weak/Unknown for scoped summaries.

## 2.3 Evidence quality principles (update path)

1. **Exam-condition outweighs formative (for Readiness narratives)** — mocks and timed past papers dominate short micro-quizzes for assessment-strength stories (principle only; no numeric formula here).  
2. **Curriculum attribution mandatory for topic slots** — no invented syllabus identity.  
3. **Independence matters** — unaided attempts outrank hinted or heavily scaffolded successes when metadata is present.  
4. **Repetition and diversity raise aggregate warrant** — one correct item ≠ scoped strength; structural strategy may store facts but must not invent warrant scores.  
5. **Contradiction remains visible** — conflicting High-reliability outcomes must not be silently collapsed into false certainty by the structural strategy.  
6. **Secondary never steals primary.**  
7. **Append-only evidence ids** with dedupe.  
8. **Completion of an assessment session ≠ Behaviour mastery grant** — scored outcomes update Performance/Knowledge; mission wrapper completion remains Behaviour.  
9. **Partial attempts are incomplete lineage** — abandoned mid-mock may leave a weak/incomplete Performance signal with reduced warrant; never invent full-mock strength.

## 2.4 Categories feeding Performance

| Evidence category | Relevance to strategy |
|---|---|
| **Assessment** | Core primary set |
| **System Events** | Graded system assessments when typed as Assessment evidence |
| **Learning Activity** | Not Performance unless nested scored outcomes arrive |
| **Behaviour** | Assessment abandon may pair Behaviour + incomplete Performance |
| **Revision** | Not Performance-primary |
| **Confidence** | Calibration consumer of Performance; not a Performance writer |
| **Planning** | Goal/date changes do not erase Performance history |

## 2.5 Non-events (must not drive Performance ownership)

- Mission completion without scored assessment outcomes  
- Time-on-task or study-break evidence alone  
- Dashboard views or coach narration without assessment evidence  
- Confidence self-ratings as measured accuracy  
- Cosmetic accuracy badges or leaderboard projections  

---

# 3. Assessment lineage

## 3.1 Purpose

Assessment lineage is the **structural spine** of Performance — analogous to Knowledge’s topic mastery slots, Memory’s retention slots, and Behaviour’s session/pattern ids.

It answers structurally: *Which assessments have been observed, under what scopes, and which evidence ids support those scopes?*

It does **not** answer: *What is the student’s pass probability?* or *What IRT ability should we use?*

## 3.2 Two complementary lineage layers

| Layer | Structural home | Role |
|---|---|---|
| **Assessment references** | `assessment_ids` | Append-only ids of assessment / attempt evidence applied to Performance |
| **Scoped summaries** | `performance_summaries` | Per-scope structural units (`scope_id` + facts bag) |

Both remain architecture-compliant if lineage stays evidence-backed and immutable.

## 3.3 Scope identity

`scope_id` is the structural key for a summary slice. Illustrative scope kinds (classification only — not a scoring taxonomy):

| Scope kind | Example identity | Notes |
|---|---|---|
| **Topic / objective** | Curriculum topic or LO id | Requires curriculum identity on evidence |
| **Quiz / mock / past paper** | Assessment instance id | Exam-condition tags when present |
| **Diagnostic** | Diagnostic assessment id | Baseline positioning; not a permanent label |
| **Sitting / post-exam slice** | Sitting or outcome scope | Post-exam primary; preserve history across re-sits |
| **Section / paper slice** | Curriculum section or paper slice when V2 | Must remain nullable for V1 |

The structural strategy must **not** invent scopes from free text. If evidence lacks a usable scope identity, append assessment references only (weak lineage) — do not fabricate a topic summary.

## 3.4 Conceptual fields (scoped summary)

| Field | Role |
|---|---|
| **scope_id** | Stable identity for the assessment slice |
| **summary** | Structured facts bag describing observed performance (*stored*, not computed by the structural strategy) |
| **Optional condition tag** (additive) | Formative / exam-condition / diagnostic / incomplete — when evidence carries it |
| **Optional evidence_ids** (additive) | Append-only supporting evidence for this scope |
| **Optional curriculum refs** | Topic/section/LO references when present; never invent |
| **Optional last_observed** | Latest applicable evidence timestamp for this scope |

Belief/scoring fields (accuracy trend, strength score, mistake-pattern score, pass-probability contribution) remain **absent or preserved-unknown** in the structural strategy — same discipline as `mastery_belief` / `retention_belief` / Behaviour `consistency_metrics`.

## 3.5 Relationship to state-level assessment_ids

| State field | Summary relationship |
|---|---|
| `assessment_ids` | Deduped union of assessment/attempt evidence applied to Performance |
| `performance_summaries` | Scoped units that may reference overlapping evidence; must not diverge into a private gradebook |
| Optional state-level `evidence_ids` | If introduced additively, same append-only/dedupe rules |

Summaries must not become a competing store of quiz service rows. Graders emit Learning Evidence; Performance references evidence *about* outcomes.

## 3.6 Incomplete and contradictory lineage

| Situation | Structural rule |
|---|---|
| **Abandoned mid-assessment** | May append assessment id and/or incomplete-scoped summary with reduced warrant facts if supplied; never invent full-mock strength |
| **Hinted / scaffolded success** | Preserve independence metadata in facts when present; do not upgrade warrant in structural phase |
| **Contradictory High-reliability outcomes** | Keep separate scoped facts visible; do not silently average into one opaque score |
| **Post-exam after prior mocks** | Append new lineage; do not erase historical mock summaries |
| **Re-sit Goals** | Planning may reset; Performance history remains audit lineage |

---

# 4. Update responsibilities

## 4.1 Strategy charter

`PerformanceUpdateStrategy` owns **structural evolution of `PerformanceState`** from Learning Evidence inside the Twin Update Pipeline.

| Owns | Does not own |
|---|---|
| Applicability (`supports`) for Performance-relevant evidence | Mastery / Knowledge beliefs |
| Structural append of `assessment_ids` | Retention / Memory clocks or beliefs |
| Create/extend scoped `performance_summaries` from stored facts | Behaviour adherence / consistency metrics |
| `last_updated` materialisation | Readiness composite / pass probability |
| Preservation of unknown summary fields | Next-action selection / mission generation |
| Returning a **new** Twin snapshot | Persistence, HTTP, Flask, ORM |
| Audit contribution via stable strategy `name` | Curriculum structure or weights |
| Condition tagging when present on evidence | Confidence self-report channel or calibration math ownership |
| | Inventing syllabus topics or scopes without evidence |
| | Item bank content or analytics formula forks |

## 4.2 Write-path exclusivity

```
Learning Evidence → Twin Update Pipeline → PerformanceUpdateStrategy → new PerformanceState in new Twin snapshot
```

No quiz service, mock scorer, analytics dashboard, recommendation packager, or coach may write Performance “truth” outside that path. Graders and assessment producers emit **Learning Evidence**; they do not mutate Twin domains directly.

## 4.3 Strategy contract alignment

Same architectural contract as Knowledge/Memory/Behaviour strategies:

1. Stable `name` for `UpdateResult` audit.  
2. `supports(context)` based on evidence types and required fields (topic/scope identity required for topic-scoped summaries; assessment-instance scopes may not need `topic_id`).  
3. `apply(context)` returns a **new** Twin snapshot.  
4. Framework-free pure domain logic.  
5. Preserve unknown summary/belief fields; do not invent scoring prematurely.

## 4.4 Downstream consumers (read-only)

| Consumer | Uses Performance for |
|---|---|
| **KnowledgeUpdateStrategy** | Assessed outcomes strongly inform mastery (same evidence batch; separate ownership) |
| **Readiness Aggregation** | Assessment strength / weakness factors |
| **Decision Engine** | Assessment weakness; prefer assessment-shaped actions when evidence is thin or weak |
| **Confidence path** | Measured pole for over/under-confidence calibration |
| **Mission Generation Intelligence** | Weak-area practice targets without treating missions as score stores |
| **Predictions (later)** | Mock / exam-condition features for pass-probability and readiness snapshots |
| **Analytics / Insight / Coach (later)** | Narrate assessment trends with Twin+evidence lineage — never fork Performance formulas |

---

# 5. Structural update rules

Capability 2.6 targets **structural Performance only** — mirror Knowledge/Memory/Behaviour discipline.

## 5.1 Intended structural behaviours

1. **Applicability** — run when the context contains at least one Performance-primary evidence type, or an explicitly documented Performance-secondary type allowed for weak updates.  
2. **Assessment lineage** — append assessment / attempt ids (deduped) for applicable evidence.  
3. **Scoped summaries** — create or extend `performance_summaries` when evidence supplies a usable `scope_id` and optional stored facts; merge into existing scope by identity rather than duplicating unbounded copies.  
4. **Fact bag preservation** — leave unknown summary keys/values unchanged unless the evidence (or a later scoring engine through an approved extension) supplies them; structural strategy must not invent accuracy engines.  
5. **Condition honesty** — when evidence carries formative / exam-condition / diagnostic / incomplete metadata, store it as structural fact/tag; do not narrate formative success as exam-condition readiness.  
6. **Timestamp** — set `PerformanceState.last_updated` to the latest processed applicable evidence timestamp.  
7. **Immutability** — return a new Twin; never mutate the input aggregate.  
8. **No ownership theft** — secondary question attempts may append weak references; Knowledge remains primary for attempt-type evolution.

## 5.2 Explicit non-computations (structural phase)

The structural strategy must **not**:

- Compute accuracy trends, strength scores, or IRT / partial-credit models  
- Emit readiness composites or pass probabilities  
- Infer mistake taxonomies as scored beliefs (structural aggregates later only)  
- Grant or revoke Knowledge/Memory beliefs  
- Absorb Behaviour adherence into “study quality” Performance  
- Select recommendations or generate missions  
- Persist Twin or evidence  
- Fabricate High Performance from Goals, Behaviour, or empty cold start  

## 5.3 Primary evidence type set (architecture)

Fix `supports` types explicitly in implementation notes; this architecture locks the educational set:

**Primary (must support)**

- Quiz outcome  
- Mock / timed mock outcome  
- Past-paper outcome  
- Diagnostic assessment outcome  
- Post-exam outcome  

**Secondary (optional weak updates — documented only)**

- Question attempt / correct / incorrect (weak assessment reference; Knowledge primary)  
- Incomplete / abandoned assessment attempt as incomplete Performance signal (Behaviour remains primary for abandon)

## 5.4 Idempotence and determinism

- Dedupe id appends so replaying the same evidence id does not grow unbounded duplicates.  
- Scope merge by `scope_id` must be deterministic for the same Twin + ordered evidence batch.  
- Same Twin + same ordered evidence batch → same structural Performance outcome (deterministic core).  
- No required network LLM calls on the write path.

## 5.5 Structural vs derived boundary

| Structural (Capability 2.6) | Derived (deferred) |
|---|---|
| Assessment id references | Accuracy / strength trends |
| Scoped summary slots (facts stored or preserved) | Exam-condition vs formative delta scores |
| Timestamps / optional condition tags | Mistake taxonomy beliefs |
| Incomplete-assessment lineage | Item / objective grain models; partial credit |
| | Pass-probability features (Predictions consume Performance) |
| | Learning velocity (assessment-adjusted; cross-domain) |

Derived Performance must remain factorable and must **not** become a second readiness composite or a second Knowledge mastery store. Vanity accuracy percentages without scope, lineage, or condition context fail educational fidelity.

---

# 6. Interaction with Knowledge

## 6.1 Complementary questions

| Domain | Question |
|---|---|
| **Knowledge** | What does the student know *now*? |
| **Performance** | How does the student perform when assessed? |

## 6.2 Pipeline interaction

- Strategies do not share mutable bags. Each returns a new Twin; the pipeline chains via context.  
- A mixed batch (quiz / mock / diagnostic) may apply Knowledge **and** Performance in one pipeline run — shared primary evidence is intentional.  
- Post-exam: Performance primary; Knowledge may take a secondary update without Performance absorbing mastery ownership.  
- Mission completion must not overwrite or replace quiz-driven Knowledge/Performance updates.

## 6.3 Allowed

- Assessed outcomes strongly inform mastery beliefs (Knowledge’s concern) while Performance keeps assessment trends visible as a distinct factor.  
- Performance summaries supply Decision Engine “assessment weakness” while Knowledge supplies “mastery gap” — often correlated, sometimes divergent (e.g. untimed quiz vs timed mock).  
- Cold-start diagnostics feed both domains; both must mark low confidence when diagnostic is skipped.

## 6.4 Forbidden

| Anti-pattern | Why |
|---|---|
| Performance stores `mastery_belief` as its only truth | Domain collapse |
| Knowledge strategy absorbs all Performance summary ownership | Hides assessment trends as a distinct factor |
| One strong mock → permanent High mastery with no decay/context | Overclaim; ignores Memory/time and evidence quality |
| Treating Performance accuracy % as syllabus coverage | Coverage is Knowledge/Curriculum-weighted; accuracy ≠ coverage |
| Knowledge strategy owns post-exam as primary | Steals Performance primary ownership |

## 6.5 Educational takeaway

Strong Performance with thin Knowledge structure means assessed signals exist but mastery slots may still be incomplete or low-confidence.  
Strong Knowledge claims with thin Performance mean the Twin may be over-trusting non-assessed or sparse channels — Decision Engine should favour assessment-shaped actions. Keep both visible so explanations stay honest (“mock weakness on Topic T” vs “mastery belief still low on Topic T”).

---

# 7. Interaction with Memory

## 7.1 Complementary questions

| Domain | Question |
|---|---|
| **Memory** | Will the student still know it when it matters? |
| **Performance** | How does the student perform when assessed (now / under conditions)? |

## 7.2 Pipeline interaction

- Correct assessed outcomes may update Memory’s retention structure **via MemoryUpdateStrategy** when evidence is topic-scoped — Performance does not store retention clocks.  
- Revision / flashcard evidence remains Memory-primary; it must not be reclassified as Performance merely because it feels “test-like.”  
- A strong past mock can coexist with high Memory risk if reinforcement is stale — Readiness must see both factors.

## 7.3 Allowed

- Dual explanation: Performance (“timed mock weak on Topic T”) and Memory (“Topic T last reinforced 28 days ago”).  
- Decision may recommend exam-condition rehearsal for high-weight weak slices without Performance rewriting Memory decay math.  
- Post-exam and mock lineage remain Performance history even when Memory clocks continue independently.

## 7.4 Forbidden

| Anti-pattern | Why |
|---|---|
| Performance stores `retention_belief` / `last_reinforced` | Domain collapse |
| Flashcard correctness treated as full exam-condition Performance | Wrong reliability class; Memory primary |
| Old high mock freezes retention forever | High past scores do not freeze Retention |
| Skipping Memory update because a Performance summary exists | Complementary domains; both may need evolution |

## 7.5 Educational takeaway

Performance describes assessed competence under observed conditions; Memory describes durability toward the sitting. A student can mock well in March and still face retention risk in June. Explain both — do not merge into one “they’re fine” score.

---

# 8. Interaction with Behaviour

## 8.1 Distinct questions

| Domain | Question |
|---|---|
| **Performance** | How does the student perform when assessed? |
| **Behaviour** | How does the student actually study day to day? |

## 8.2 Pipeline interaction

- Quizzes/mocks: Performance (+ Knowledge) primary; Behaviour may record secondary session engagement.  
- Abandoned assessments: Behaviour (abandon) + incomplete Performance signal — dual update is valid; ownership stays split.  
- Mission completed + embedded quiz: Behaviour primary for mission; Knowledge + Performance primary for quiz — dual/triple strategy application is valid.  
- `BehaviourUpdateStrategy` must not absorb score summaries; `PerformanceUpdateStrategy` must not invent adherence strength from missions alone.

## 8.3 Allowed

- Decision Engine uses Performance for *what* to practise and Behaviour for *how hard / how soon* is feasible (read-side).  
- Sparse strong mocks + irregular adherence: both factors remain visible separately.  
- When Behaviour is strong and Performance is thin, prefer assessment-shaped next actions within Behaviour feasibility.

## 8.4 Forbidden

| Anti-pattern | Why |
|---|---|
| High mission adherence → “strong Performance” | Adherence ≠ assessed accuracy |
| Collapse Performance into Behaviour “study quality” | Hides assessment trends — the reason Performance is distinct |
| Behaviour owns mock score summaries | Performance domain exists to prevent that collapse |
| Treating time-on-task as Performance accuracy | Time ≠ assessed outcome |
| Mission completion overwrites quiz-driven Performance | Mixed-batch ownership violation |

## 8.5 Educational takeaway

A student can complete every mission and still fail mocks (activity without assessed learning).  
A student can score well on sparse assessments and still show fragile Behaviour (unsustainable practice). Both must remain separate Twin factors.

---

# 9. Explainability

## 9.1 Place in the mandatory chain

```
Curriculum factor (when topic/weight/condition relevant)
    → Learning Evidence (quiz/mock/diagnostic/post-exam ids)
        → PerformanceState factor(s) (assessment lineage / scoped summaries)
            → Readiness factor (assessment strength/weakness — when relevant)
                → Decision Engine reason code(s) (assessment-shaped action / remediation)
                    → Recommendation explanation
```

Performance contributes **assessment-strength and assessment-weakness factors**, not mastery claims, retention clocks, or adherence scores.

## 9.2 Explainable Performance factors (structural era)

Even before scoring, explanations can cite structural facts:

| Factor class | Example citation |
|---|---|
| **Assessment event** | “Mock M scored outcome recorded for scope S (evidence id …).” |
| **Scoped weakness lineage** | “Topic T appears in weak mock/quiz summary references.” |
| **Condition gap** | “Untimed quiz strong on T; timed mock weak on T — conditions diverge.” |
| **Sparse assessment** | “Few assessment evidence ids — assessment confidence low.” |
| **Incomplete attempt** | “Assessment A abandoned mid-attempt — incomplete Performance signal only.” |
| **Cold start** | “No Performance evidence yet — assessment confidence low.” |
| **Post-exam lineage** | “Sitting outcome referenced; prior mock history preserved.” |

## 9.3 Separation rules for honest narration

1. Never equate “you completed the mission” with “you demonstrated assessed competence.”  
2. Never narrate formative quiz success as exam-condition readiness.  
3. When timed mock weakness and strong Behaviour co-occur, explain **both** — do not merge into one opaque score.  
4. When Confidence self-report conflicts with dense Performance, explain both poles — Confidence is down-weighted.  
5. Coach/Insight may narrate Twin + evidence only; no fabricated weak areas or invented scores.  
6. Derived accuracy/strength scores (later) must remain named, factorable, evidence-linked, and condition-aware.

## 9.4 Forbidden explanation patterns

- Opaque “performance score” as readiness or pass probability  
- Single-mock “you’re ready” claims  
- UI accuracy badges cited as Twin authority when they disagree with Twin lineage  
- LLM rationales that invent assessment trends  
- Treating hinted quiz success as exam strength without independence context  

---

# 10. Pipeline registration

## 10.1 Pipeline position

```
Learning Evidence (append-only)
      → UpdateContext (Twin + evidence + metadata)
            → TwinUpdatePipeline
                  → registered Update Strategies (registration order)
                        → KnowledgeUpdateStrategy
                        → MemoryUpdateStrategy
                        → BehaviourUpdateStrategy
                        → PerformanceUpdateStrategy   ← Capability 2.6
                        → … future strategies
                  → UpdateResult (original Twin, updated Twin, applied_strategies, …)
```

The pipeline remains an orchestration shell. It must not hard-code Performance algorithms. Registration is via constructor list or `register` — same extension point as Knowledge/Memory/Behaviour.

## 10.2 Recommended registration order (structural phase)

| Order | Strategy | Rationale |
|---|---|---|
| 1 | `KnowledgeUpdateStrategy` | Existing; assessment/attempt primary |
| 2 | `MemoryUpdateStrategy` | Existing; revision primary |
| 3 | `BehaviourUpdateStrategy` | Practice/adherence; secondary on assessment/revision |
| 4 | `PerformanceUpdateStrategy` | Assessment summaries; structural phase after Behaviour |

**Why Performance after Knowledge/Memory/Behaviour in structural phase**

1. Preserves the already-shipped Knowledge → Memory order and the Behaviour architecture’s recommended slot.  
2. Performance structural updates do not require prior Behaviour mutation to be correct; dual updates on mixed batches remain valid either way once order is fixed.  
3. Mixed batches remain reproducible when order is fixed and documented.  
4. Knowledge already receives assessment evidence independently; structural Performance does not need to precede Knowledge to materialise summaries.

**Belief-enrichment caveat (deferred)**

Educational Intelligence Architecture notes that once Knowledge *and* Performance both compute beliefs, ordering may need Performance before Knowledge so mastery enrichment can read refreshed assessment structure in the same batch. That reorder is **not** required for structural Capability 2.6. If later belief enrichment needs it, revise order in a dedicated architecture note — do not silently reorder in product code.

## 10.3 Invocation rules

1. Invoke every registered strategy where `supports(context)` is true, in registration order.  
2. Each `apply` receives a context whose Twin reflects prior strategies.  
3. Multiple strategies may apply to one batch; ownership matrix prevents domain theft.  
4. No strategies registered → no-op success with explanatory messages (existing pipeline semantics).  
5. `UpdateResult.applied_strategies` must include Performance’s stable name when it ran.

## 10.4 Decision Engine loop closure

Assessment outcomes and accept/dismiss/complete events become Learning Evidence and re-enter this pipeline. Decision Engine must **not** mutate Performance in place.

```
Decision Engine (read Twin)
      → Recommendation / Mission projection
            → Student assessment / complete / abandon
                  → Learning Evidence
                        → TwinUpdatePipeline (incl. PerformanceUpdateStrategy when assessment-typed)
```

---

# 11. Future scoring hooks

## 11.1 Structural hooks reserved now

| Hook | Structural home | Future filler |
|---|---|---|
| `performance_summaries[].summary` bag | Scoped summaries | Named accuracy/strength/condition facts from a later engine |
| `assessment_ids` lineage | `PerformanceState` | Audit for derived metrics and density warrant |
| Optional condition tags | Summaries / evidence metadata | Exam-condition vs formative delta |
| Optional per-scope evidence ids | Nested summaries | Provenance for contradiction-aware scoring |
| Incomplete-assessment flags | Summary facts | Reduced-warrant handling for partial attempts |

## 11.2 Deferred derived concepts

| Derived concept | Likely future owner | Constraint |
|---|---|---|
| Accuracy / strength trends | Performance enrichment | Per topic/objective/scope windows; condition-aware |
| Mistake taxonomy aggregates | Performance enrichment | Conceptual taxonomies may evolve; keep lineage |
| Exam-condition vs formative delta | Performance / Predictions | Timed mock may diverge from untimed mastery |
| Item / objective grain models | Performance + richer banks | Partial credit, multi-part items |
| Cross-sitting baselines | Predictions / Analytics (read Twin) | Privacy-preserving; no peer exposure requirement in Epic 2 |
| Pass-probability features | Predictions consuming Performance | Performance supplies inputs; does not own the composite |
| Learning velocity (assessment-adjusted) | Cross-domain derivation | Must not redefine mastery or Behaviour consistency |
| Calibration gap features | Confidence path reading Performance | Confidence owns the gap *concept*; Performance supplies measured pole |

## 11.3 Scoring extension rules

1. Prefer filling reserved summary slots over inventing parallel Performance stores.  
2. Derived engines may **read** Performance structure and **emit** new evidence or write beliefs via strategy extension — not via Flask services mutating Twin.  
3. Derived Performance must not emit the overall readiness composite or pass probability.  
4. Numeric engines remain unlocked (Educational Intelligence Architecture §11.3) beyond ownership.  
5. Confidence remains separable; calibration engines consume Performance as the measured pole only.  
6. Analytics projections must share metric definitions with Twin — never fork.

---

# 12. Risks

| Risk | Impact | Architectural mitigation |
|---|---|---|
| **Domain collapse into Knowledge** | Unexplainable dual mastery; lost assessment-condition nuance | Complementary questions; ownership matrix; separate `PerformanceState` |
| **Domain collapse into Behaviour** | Assessment trends hidden as “study quality” | Distinct domain; Behaviour never owns mock summaries |
| **Single-mock overclaim** | False readiness / pass narratives | Factorable Readiness; evidence quality principles; mocks outweigh quizzes but do not alone equal pass probability |
| **Mission completion as Performance** | Activity theatre replaces assessed learning | Ownership matrix; mixed-batch rules |
| **Analytics formula fork** | Divergent dashboards vs Twin | Analytics reads Twin; shared metric definitions |
| **Confidence overrides Performance** | Optimistic false readiness | Confidence separable; down-weighted vs assessed Performance |
| **Hinted success as exam strength** | Inflated Performance warrant | Independence / scaffolding metadata on evidence |
| **Unmapped practice as topic Performance** | Invented syllabus signal | Curriculum identity mandatory for topic scopes |
| **Strategy order hazards** | Non-reproducible updates on mixed batches | Fixed registration order (§10.2); document in capability review |
| **Premature scoring complexity** | Unmaintainable IRT/accuracy math before structure settles | Structural strategy first; hooks only |
| **Partial attempts treated as full mocks** | Misleading exam-condition beliefs | Incomplete-assessment warrant rules (§3.6) |
| **LLM-invented scores / weak areas** | Fabricated Performance | Coach narrates Twin+evidence only |
| **V1/V2 breakage** | Section-required Performance logic | Nullable sections; canonical traversal; never invent topics |
| **Parallel Performance stores in quiz services** | Divergent learner state | Evidence → strategy → Twin only |
| **Post-exam erasure of history** | Broken calibration / audit | Append-only evidence; preserve Performance lineage across re-sits |
| **In-place Twin mutation** | Broken snapshot audit | Immutable snapshots only |
| **Silent belief-phase reorder** | Non-auditable update differences | Reorder only via dedicated architecture note |

---

# 13. Extensibility

## 13.1 Safe extension points

| Extension | How to extend safely |
|---|---|
| **Register `PerformanceUpdateStrategy`** | Pipeline registration; framework-free; immutable snapshots |
| **Richer scoped summaries** | Fill `performance_summaries` facts via later engines; keep structural slots stable |
| **New Assessment evidence types** | Evidence catalogue + ownership matrix primary/secondary assignment |
| **Objective / item grain** | Additive scopes referencing Learning Objectives / items; Curriculum remains authority |
| **Partial-credit / multi-part items** | Derived enrichment; structural summaries remain additive |
| **Exam-style item types** | Evidence metadata + Performance interpretation; no Twin syllabus invention |
| **Mistake taxonomy** | Structural aggregates with lineage; taxonomies may evolve without breaking snapshots |
| **Cross-sitting baselines** | Prediction/Analytics features reading Performance; privacy-preserving aggregates only |
| **Confidence calibration engines** | Consume Performance as measured pole; Confidence remains separable |
| **Prediction features** | Pass probability / readiness snapshots read Performance; write via Prediction path only |
| **Belief-enrichment reorder** | Dedicated architecture note if Performance must precede Knowledge |

## 13.2 Compatibility guarantees

1. Curriculum V1 and V2 remain loadable; Performance must not require Sections globally.  
2. Structural Twin fields prefer additive optional fields over breaking renames.  
3. Evidence append-only semantics remain permanent.  
4. Deterministic cores remain free of required network LLM calls.  
5. Knowledge and Memory remain complementary mastery/retention stores — Performance must not become a third mastery store.  
6. Behaviour remains the study-practice domain — Performance must not absorb adherence.  
7. Existing Knowledge → Memory → Behaviour registration continues to work when Performance is added after Behaviour.

## 13.3 Deliberately unlocked

- Exact accuracy / strength formulas  
- IRT / BKT / heuristic mastery bridges from Performance → Knowledge  
- Mistake taxonomy schemes  
- Partial-credit models  
- Numeric readiness weights on assessment factors  
- Pass-probability models  
- Cohort benchmarking bands  
- Final Decision Engine scoring function  

---

# 14. Architecture diagrams

## 14.1 Write path

```
Student / system assessment occurrence
      │
      ▼
Learning Evidence (append-only, typed, attributable)
      │
      ▼
UpdateContext (DigitalTwin + evidence + metadata)
      │
      ▼
TwinUpdatePipeline
      │
      ├─ KnowledgeUpdateStrategy    (if supports)
      ├─ MemoryUpdateStrategy       (if supports)
      ├─ BehaviourUpdateStrategy    (if supports)
      └─ PerformanceUpdateStrategy  (if supports)  ← this capability
      │
      ▼
UpdateResult
  ├── original_twin
  ├── updated_twin          (new snapshot; PerformanceState evolved when applicable)
  ├── applied_strategies
  └── processing_messages
```

## 14.2 Performance domain focus

```
┌─────────────────────────────────────────────────────────────┐
│                     DigitalTwin snapshot                      │
│  Identity · Goals · Knowledge · Memory · Behaviour · …        │
│                              ▲                                │
│                              │ structural write only          │
│                   PerformanceUpdateStrategy                   │
│                              ▲                                │
│         Performance-primary / secondary assessment evidence   │
└─────────────────────────────────────────────────────────────┘

PerformanceState (structural)
  ├── assessment_ids              (lineage)
  ├── performance_summaries[]     (scope_id + facts bag; not scored here)
  │     ├── scope_id
  │     └── summary (preserved / stored facts)
  ├── last_updated
  └── optional additive lineage / condition tags
```

## 14.3 Cross-domain ownership (mixed batch)

```
Mission completed + embedded quiz on Topic T
                │
                ▼
        TwinUpdatePipeline
                │
    ┌───────────┼───────────┬────────────────┐
    ▼           ▼           ▼                ▼
 Knowledge   Memory     Behaviour      Performance
 (quiz)     (no-op)   (mission prim.;   (quiz prim.)
                       quiz secondary)
```

Mission completion must not replace quiz-driven Knowledge/Performance updates.

## 14.4 Abandoned mid-assessment

```
Timed mock started → abandoned halfway
                │
                ▼
        TwinUpdatePipeline
                │
    ┌───────────┴───────────┐
    ▼                       ▼
 Behaviour              Performance
 (abandon primary)      (incomplete assessment
                         reference / reduced warrant;
                         never invent full-mock strength)
```

## 14.5 Read-side consumption (not write)

```
PerformanceState
      │
      ├─► Knowledge belief enrichment   (same evidence; separate ownership)
      ├─► Readiness Aggregation         (assessment strength/weakness)
      ├─► Decision Engine               (assessment-shaped actions)
      ├─► Confidence calibration        (measured pole)
      ├─► Mission Generation            (weak-area targets)
      └─► Predictions / Coach           (features / narration)
```

Read consumers must not write Performance truth.

## 14.6 Recommendation / assessment loop

```
Decision Engine ──► Recommendation / assessment-shaped mission
                         │
              attempt / complete / abandon / score
                         │
                         ▼
              Learning Evidence
                         │
                         ▼
         TwinUpdatePipeline (+ Performance primary
              for scored assessment; Behaviour for
              mission/abandon; Knowledge for attempts/quizzes)
```

---

# 15. Recommendations

## 15.1 For the next implementation milestone

1. Treat [`CAPABILITY_2_6_PERFORMANCE_DOMAIN_ANALYSIS.md`](CAPABILITY_2_6_PERFORMANCE_DOMAIN_ANALYSIS.md) plus **this document** as the charter for `PerformanceUpdateStrategy`.  
2. Implement **structural-only** Performance updates — `assessment_ids`, scoped `performance_summaries`, timestamps, preserve unknown summary fields, no scoring.  
3. Fix `supports` types explicitly to the primary set in §5.3; document any secondary weak updates (question attempts; incomplete abandons).  
4. Register after Knowledge, Memory, and Behaviour (§10.2); do not hard-code Performance inside the pipeline class.  
5. Require curriculum identity for topic-scoped summaries; allow assessment-instance scopes without inventing topics.  
6. Prefer additive optional fields / condition tags over breaking `PerformanceState` renames.  
7. Keep missions as projections; Mission Generation consumes Performance weakness and emits evidence — it does not own Performance.  
8. Keep Confidence separable — Performance supplies measured calibration facts only.  
9. Do not expand Performance into Knowledge, Memory, Behaviour, or Readiness ownership.  
10. Defer belief-enrichment reorder (Performance before Knowledge) to a dedicated note if/when both domains compute beliefs.

## 15.2 Educational design recommendations

1. Prefer **condition-aware explanations** (“timed mock” vs “practice quiz”) over a single accuracy number.  
2. Always separate “you showed up” (Behaviour), “you demonstrated assessed competence” (Performance), and “you likely still know it” (Memory).  
3. Use Performance to **reveal assessment risk**, not to inflate readiness from one good day.  
4. When Behaviour is strong and Performance is thin, recommend **assessment-shaped** next actions — fidelity over completion theatre.  
5. When Performance is strong and Behaviour is fragile, protect the assessment signal while constraining intensity — do not erase mocks because adherence slipped.  
6. Cold start: explicit low assessment confidence — never fabricate High Performance from Goals alone.

## 15.3 Architecture compliance checklist

| Invariant | Status for this architecture |
|---|---|
| Twin is sole educational state authority | PerformanceState lives only in Twin |
| Evidence is only legitimate belief input | Required |
| Strategies own domain evolution | `PerformanceUpdateStrategy` defined |
| Pipeline only coordinates | Registration; no hard-coded Performance math |
| Performance ≠ Knowledge store; Performance ≠ Behaviour; Activity ≠ readiness | Binding |
| Knowledge/Memory complementary stores preserved | Performance must not become a third mastery store |
| V1/V2 curriculum compatibility | Performance must not invent syllabus or require V2-only structure |
| Structural before scoring | Explicit |
| Registration order documented before coding | §10.2 |
| No implementation in this milestone | Satisfied by architecture-only deliverable |

## 15.4 Explicit stop line

This milestone delivers **architecture only**.

**Do not proceed in this milestone to:** code, tests, database changes, services, scoring formulas, or UI.

Next engineering step (separate milestone): structural `PerformanceUpdateStrategy` implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Host aggregate and registration shell |
| 2.3–2.4 | Knowledge / Memory strategies | Structural precedents Performance must follow |
| 2.5 | Behaviour Update Strategy | Prior domain; secondary session signals only for assessments |
| 2.6 prior | Performance Domain Analysis | Domain charter this architecture implements |
| **2.6** | **Performance Update Strategy** | **This architecture** |
| 2.7 | Readiness | Consumes Performance as assessment strength/weakness factor |
| 2.8–2.10 | Decision / Recommendation / Missions | Read Performance for assessment weakness; write back via evidence |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.6 — Performance Update Strategy Architecture |
| Nature | Architecture only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required going forward; no traversal changes |
| Application code intentionally untouched | Yes |
| Preceded by | Performance Domain Analysis (approved); Behaviour Update Strategy Architecture |
| Next | Structural `PerformanceUpdateStrategy` implementation (separate milestone) |

---

*End of Capability 2.6 Performance Update Strategy Architecture.*
