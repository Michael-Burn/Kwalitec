# Capability 2.5 — Behaviour Update Strategy Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 2 – Educational Intelligence  
**Capability:** 2.5 Behaviour Update Strategy  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Domain charter:** [`CAPABILITY_2_5_BEHAVIOUR_DOMAIN_ANALYSIS.md`](CAPABILITY_2_5_BEHAVIOUR_DOMAIN_ANALYSIS.md)  
**Companions:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md), [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md), [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md), [`docs/epics/EPIC_2_KICKOFF.md`](../epics/EPIC_2_KICKOFF.md), Twin domain README (`app/domain/twin/README.md`)  
**Scope:** Structural write-path architecture for `BehaviourUpdateStrategy` — **no code, services, tests, schemas, or scoring formulas**

---

## Document purpose

This milestone defines **how** Behaviour evolves inside the Student Digital Twin when Learning Evidence arrives.

It follows Capability 2.3 (Knowledge) and 2.4 (Memory): **structure first, beliefs later**. It translates the approved Behaviour Domain Analysis into update-strategy architecture that can be implemented in a later milestone without redesigning Twin, Evidence, or Curriculum contracts.

**Non-goals of this document**

- Code, pseudocode algorithms, or package layouts beyond conceptual names  
- Database schemas, Alembic migrations, or ORM layouts  
- Concrete adherence / consistency / burnout / velocity formulas  
- UI, gamification, notifications, or social features  
- Replacement of Curriculum Engine, Evidence Model, Twin aggregate, or Twin Update Pipeline contracts  

**Hard educational rule (binding):** Behaviour never grants or revokes mastery by itself.  
**Governing principle:** Behaviour is not learning; Activity is not readiness.

---

# 1. BehaviourState

## 1.1 Position

`BehaviourState` is the Twin domain that answers:

> **How does the student actually study?**

It sits beside Knowledge, Memory, Performance, Confidence (separable), Goals, Identity, and Prediction snapshots inside the immutable `DigitalTwin` aggregate.

## 1.2 Architectural properties

| Property | Requirement |
|---|---|
| **Evidence-backed** | Evolves only from Learning Evidence via `BehaviourUpdateStrategy` |
| **Immutable per snapshot** | Updates produce a new Twin snapshot; never mutate in place |
| **Structural-first** | References, lineage, timestamps, and metric *slots* before scoring |
| **Curriculum-optional** | Many facts are session/mission scoped; topic tags allowed when evidence carries them |
| **Non-authoritative for learning** | Completion and effort do not certify Knowledge or Memory |

## 1.3 Structural shape (conceptual contract)

Prefer the existing Twin vocabulary. Capability 2.5 must not redesign Behaviour for scoring. Additive optional fields are allowed if lineage requires them (same discipline as Knowledge/Memory).

| Structural field | Educational role | Structural strategy duty |
|---|---|---|
| **consistency_metrics** | Named bag for later adherence/consistency values | **Preserve** unknown keys/values; do **not** compute scores |
| **session_history_ids** | Lineage to session / activity history or session-shaped evidence | Append (dedupe) when primary/secondary session evidence applies |
| **study_pattern_ids** | Lineage to pattern aggregates (cadence, skip clusters, timing) | Append when pattern references are supplied; do **not** invent clusters |
| **last_updated** | Materialisation timestamp for this Behaviour snapshot | Set from latest processed applicable evidence timestamp |
| **Optional additive lineage** (if required) | e.g. state-level `evidence_ids`, nested `BehaviourRecord` map | Prefer additive optional fields over breaking renames |

## 1.4 What BehaviourState is not

- A dashboard cache of “hours this week”  
- A competing store of mission rows  
- A readiness composite or pass probability  
- A mutable streak counter that bypasses evidence  
- A Motivation domain or personality taxonomy  

## 1.5 Cold start

Empty references and empty metric bags are valid. Consumers (Decision Engine, Planning, Readiness) must treat missing Behaviour as **explicit low confidence / default feasibility** — never as perfect adherence or hopeless inconsistency.

---

# 2. BehaviourRecord

## 2.1 Purpose

`BehaviourRecord` is the **nested structural unit** for Behaviour lineage — analogous to Knowledge’s topic mastery slot and Memory’s retention slot, but **practice-scoped** rather than mastery/retention-scoped.

It answers structurally: *What discrete practice/adherence unit has been observed and linked?*

It does **not** answer: *Is the student consistent enough?*

## 2.2 When nested records are warranted

Knowledge and Memory need per-topic slots because syllabus identity is the primary key of those domains.

Behaviour’s primary key is usually a **practice unit** (session, mission window, adherence event cluster), not a topic. Architecture therefore allows either:

1. **Id-list-only structural phase** — `session_history_ids` / `study_pattern_ids` (and optional state-level evidence ids) without nested records; or  
2. **Additive nested `BehaviourRecord`s** — when implementation needs stable per-unit metadata beyond opaque ids.

Both remain architecture-compliant if lineage stays evidence-backed and immutable.

## 2.3 Conceptual fields (nested record, if introduced)

| Field | Role |
|---|---|
| **record_id** | Stable identity for the practice unit (session id, mission instance id, or synthetic adherence unit id) |
| **kind** | Structural event class tag (e.g. completed, missed, skipped, abandoned, time_on_task, study_break, preference_signal) — classification only, not a score |
| **evidence_ids** | Append-only references to Learning Evidence supporting this unit |
| **optional mission_id / plan_id** | Projection references — never mission authority |
| **optional topic_id / curriculum refs** | When evidence is topic-tagged; must not invent syllabus identity |
| **optional timing metadata** | Start/end or duration references as structural facts when present on evidence |
| **optional attribution** | User vs system vs interrupt provenance when present on evidence |
| **last_observed** | Latest applicable evidence timestamp for this unit |

Belief/scoring fields (adherence quality, consistency contribution, burnout contribution) remain **absent or preserved-unknown** in the structural strategy — same discipline as `mastery_belief` / `retention_belief`.

## 2.4 Relationship to state-level id lists

| State field | Record relationship |
|---|---|
| `session_history_ids` | May list record ids or external session history ids |
| `study_pattern_ids` | May list pattern aggregate ids derived later; structural strategy does not invent patterns |
| Optional `evidence_ids` on state | Deduped union of evidence applied to Behaviour |

Records must not diverge into a private mission store. Mission rows remain **projections**; Behaviour references evidence *about* them.

---

# 3. Behaviour evidence ownership

## 3.1 Ownership relative to Learning Evidence

Learning Evidence is the immutable history. `BehaviourState` is derived Twin state.

From the Educational Intelligence **Evidence Ownership Matrix**:

| Evidence type (illustrative) | Behaviour role | Structural effect (architecture) |
|---|---|---|
| Mission completed / missed | **Primary** | Session/adherence lineage; `last_updated` |
| Skipped / abandoned session | **Primary** | Slip lineage; attribution preserved when present |
| Time on task / study break | **Primary** | Capacity/load/structure references |
| Recommendation accept / dismiss | **Secondary** | Preference/compliance signal only; Decision State remains primary |
| Plan reschedule / goal change | **Secondary** when slip/capacity-related | Weak adherence/flexibility signal; Goals primary for goal facts |
| Question attempt / quiz / mock | **Secondary** | Activity presence only; Knowledge/Performance primary |
| Revision / flashcard | **Secondary** | Revision adherence presence; Memory primary |
| Confidence rating / readiness self-review | **Secondary** | Weak; Confidence primary |
| Post-exam outcome | **—** | Not Behaviour-owned |

## 3.2 Primary vs secondary rules

1. **Primary** evidence **must** evolve Behaviour when `supports` matches.  
2. **Secondary** evidence **may** append weak session/preference references; it must **not** steal primary ownership from Knowledge, Memory, Performance, Confidence, Goals, or Decision State.  
3. Mixed batches are valid (e.g. mission completed + embedded quiz).  
4. Domains reference evidence ids; they never rewrite the evidence log.  
5. Incomplete topic mapping does not block Behaviour updates when Behaviour does not require `topic_id`.

## 3.3 Evidence quality principles (update path)

1. **Pattern over anecdote** — structural updates may append early; derived consistency later requires multi-event context.  
2. **Completion ≠ learning** — mission completed is strong for adherence, weak for Knowledge unless assessment evidence also arrives.  
3. **Time ≠ mastery** — duration validates capacity/load only.  
4. **Attribution matters** — user skip vs system expiry vs interrupt improves interpretation without changing ownership.  
5. **Secondary never steals primary.**  
6. **Append-only evidence ids** with dedupe.

## 3.4 Categories feeding Behaviour

| Evidence category | Relevance to strategy |
|---|---|
| **Behaviour** | Core primary set |
| **Time** | Capacity, load, break structure |
| **Learning Activity** | Engagement/adherence; weak for Knowledge alone |
| **Engagement** | Weak consistency aggregates |
| **Planning** | Secondary when user-initiated slip |
| **System Events** | Slip with `system` provenance (e.g. mission expired) |
| **Assessment / Revision** | Secondary session signals only |

## 3.5 Non-events (must not drive Behaviour ownership)

- Dashboard views without study action evidence  
- Opening a recommendation without accept/dismiss evidence  
- Cosmetic streak increments without underlying evidence  
- Coach narration without confirmed student action  

---

# 4. Update responsibilities

## 4.1 Strategy charter

`BehaviourUpdateStrategy` owns **structural evolution of `BehaviourState`** from Learning Evidence inside the Twin Update Pipeline.

| Owns | Does not own |
|---|---|
| Applicability (`supports`) for Behaviour-relevant evidence | Mastery / Knowledge beliefs |
| Structural append of session / pattern / evidence lineage | Retention / Memory clocks or beliefs |
| Optional nested `BehaviourRecord` materialisation | Performance score summaries |
| `last_updated` materialisation | Readiness composite / pass probability |
| Preservation of unknown `consistency_metrics` | Next-action selection / mission generation |
| Returning a **new** Twin snapshot | Persistence, HTTP, Flask, ORM |
| Audit contribution via stable strategy `name` | Curriculum structure or weights |
| | Motivation domain wholesale; Confidence calibration math |
| | Inventing syllabus topics or pattern clusters without evidence |

## 4.2 Write-path exclusivity

```
Learning Evidence → Twin Update Pipeline → BehaviourUpdateStrategy → new BehaviourState in new Twin snapshot
```

No mission service, dashboard, recommendation packager, analytics job, or coach may write Behaviour “truth” outside that path.

## 4.3 Strategy contract alignment

Same architectural contract as Knowledge/Memory strategies:

1. Stable `name` for `UpdateResult` audit.  
2. `supports(context)` based on evidence types and required fields (Behaviour often **does not** require `topic_id`).  
3. `apply(context)` returns a **new** Twin snapshot.  
4. Framework-free pure domain logic.  
5. Preserve unknown metric/belief fields; do not invent scoring prematurely.

## 4.4 Downstream consumers (read-only)

| Consumer | Uses Behaviour for |
|---|---|
| Goals / Planning | Capacity realism; rebalance on adherence slips |
| Decision Engine | Feasibility, intensity demotion, skip/burnout flags |
| Readiness Aggregation | Pace / consistency factor (one factor among many) |
| Mission Generation Intelligence | Load tuning against observed reliability |
| Predictions (later) | Completion forecast; burnout risk **features** |
| Insight / Coach (later) | Narrate habits with evidence lineage |

---

# 5. Structural update rules

Capability 2.5 targets **structural Behaviour only** — mirror Knowledge/Memory discipline.

## 5.1 Intended structural behaviours

1. **Applicability** — run when the context contains at least one Behaviour-primary evidence type, or an explicitly documented Behaviour-secondary type allowed for weak updates.  
2. **Session lineage** — append session / history ids (deduped) for session-shaped evidence.  
3. **Pattern lineage** — append pattern ids only when evidence or prior Twin already supplies them; do not invent skip clusters in the structural strategy.  
4. **Optional BehaviourRecord** — create or extend nested records for practice units when the additive design chooses nested records; append evidence ids; never regress timestamps on older evidence.  
5. **State evidence references** — if additive state-level `evidence_ids` exist, append deduped ids for applied evidence.  
6. **Timestamp** — set `BehaviourState.last_updated` to the latest processed applicable evidence timestamp.  
7. **Metric bag preservation** — leave `consistency_metrics` unchanged unless a later scoring engine supplies values through an approved extension; structural strategy must not invent keys/values.  
8. **Immutability** — return a new Twin; never mutate the input aggregate.

## 5.2 Explicit non-computations (structural phase)

The structural strategy must **not**:

- Compute consistency scores, adherence ratios, or streak lengths as Twin authority  
- Infer burnout risk or motivation state  
- Compute learning velocity or exam readiness  
- Collapse Performance accuracy into “study quality”  
- Grant or revoke Knowledge/Memory beliefs  
- Select recommendations or generate missions  
- Persist Twin or evidence  

## 5.3 Primary evidence type set (architecture)

Fix `supports` types explicitly in implementation notes; this architecture locks the educational set:

**Primary (must support)**

- Mission completed  
- Mission missed / expired  
- Skipped session  
- Abandoned session  
- Study session started/completed (when typed as Behaviour/Learning Activity for adherence)  
- Time on task  
- Study break  

**Secondary (optional weak updates — documented only)**

- Recommendation accept / dismiss  
- Plan reschedule (user-initiated slip)  
- Assessment / revision sessions as activity presence  
- Engagement check-ins / notification responses (aggregate consistency only)

## 5.4 Idempotence and determinism

- Dedupe id appends so replaying the same evidence id does not grow unbounded duplicates.  
- Same Twin + same ordered evidence batch → same structural Behaviour outcome (deterministic core).  
- No required network LLM calls on the write path.

## 5.5 Structural vs derived boundary

| Structural (Capability 2.5) | Derived (deferred) |
|---|---|
| Evidence / session / pattern references | Consistency score / quality |
| Timestamps | Adherence ratio over windows |
| Metric bag slots (empty or preserved) | Skip/abandon pattern clusters |
| Optional BehaviourRecord lineage | Learning velocity; burnout risk; preferred windows |

Derived Behaviour must remain factorable and must **not** become a second readiness composite. Gamified streaks, if ever productised, remain projections — never Twin authority.

---

# 6. Interaction with Knowledge

## 6.1 Complementary questions

| Domain | Question |
|---|---|
| **Knowledge** | What does the student know *now*? |
| **Behaviour** | How does the student actually study? |

## 6.2 Pipeline interaction

- Strategies do not share mutable bags. Each returns a new Twin; the pipeline chains via context.  
- A mixed batch (mission completed + quiz) may apply Knowledge **and** Behaviour in one pipeline run.  
- Mission completion must not overwrite or replace quiz-driven Knowledge updates.

## 6.3 Allowed

- Behaviour explains slow coverage (chronic skips) without changing mastery.  
- Assessment-shaped sessions: Knowledge primary; Behaviour may record secondary activity presence.  
- Decision Engine may constrain Knowledge-building actions by Behaviour feasibility (read-side).

## 6.4 Forbidden

| Anti-pattern | Why |
|---|---|
| Mission completed → raise mastery | Completion ≠ assessed knowing |
| Time on task → mastery belief | Time ≠ learning |
| Behaviour streak → Knowledge “coverage complete” | Activity ≠ syllabus mastery |
| Knowledge strategy owns mission miss types | Steals Behaviour primary ownership |

## 6.5 Educational takeaway

Strong Behaviour + weak Knowledge = shows up without demonstrated learning.  
Strong Knowledge + weak Behaviour = assessed competence at risk from irregular practice — a Readiness/Decision concern, not a Knowledge rewrite by Behaviour.

---

# 7. Interaction with Memory

## 7.1 Complementary questions

| Domain | Question |
|---|---|
| **Memory** | Will the student still know it when it matters? |
| **Behaviour** | How does the student actually study (including revision discipline as practice)? |

## 7.2 Pipeline interaction

- Revision / flashcard evidence: **MemoryUpdateStrategy** primary; Behaviour secondary (session adherence) only.  
- Skipping a revision mission: Behaviour records the slip; Memory decay/clock math remains Memory’s concern when revision evidence arrives (or fails to).  
- Behaviour must never store `retention_belief` or `last_reinforced`.

## 7.3 Allowed

- Chronic Friday revision skips as Behaviour adherence facts for Decision feasibility.  
- Dual explanation: Behaviour (“Friday revision often skipped”) and Memory (“Topic T last reinforced 28 days ago”).  
- Decision may move revision to a historically completed window without inventing mastery loss from the skip alone.

## 7.4 Forbidden

| Anti-pattern | Why |
|---|---|
| Behaviour stores retention clocks/beliefs | Domain collapse |
| Skip directly decays Memory without Memory strategy | Bypasses ownership |
| Flashcard reviews treated as Behaviour-only | Memory must remain primary |

## 7.5 Educational takeaway

Behaviour describes whether revision *happens*; Memory describes what revision *does* to retention structure.

---

# 8. Interaction with Performance

## 8.1 Distinct questions

| Domain | Question |
|---|---|
| **Performance** | How does the student perform when assessed? |
| **Behaviour** | How does the student actually study day to day? |

## 8.2 Pipeline interaction

- Quizzes/mocks: Performance (+ Knowledge) primary; Behaviour secondary activity presence only.  
- Abandoned assessments: Behaviour (abandon) + incomplete Performance signal — dual update is valid; ownership stays split.  
- `PerformanceUpdateStrategy` (Capability 2.6) remains a separate write owner; Behaviour must not absorb score summaries.

## 8.3 Allowed

- Decision Engine uses Performance for *what* to practise and Behaviour for *how hard / how soon* is feasible (read-side).  
- Sparse strong mocks + irregular adherence: both factors remain visible separately.

## 8.4 Forbidden

| Anti-pattern | Why |
|---|---|
| High mission adherence → “strong Performance” | Adherence ≠ assessed accuracy |
| Collapse Performance into Behaviour “study quality” | Hides assessment trends |
| Behaviour owns mock score summaries | Performance domain exists to prevent that collapse |

## 8.5 Educational takeaway

A student can complete every mission and still fail mocks.  
A student can score well on sparse assessments and still show fragile Behaviour. Both must remain separate Twin factors.

---

# 9. Explainability

## 9.1 Place in the mandatory chain

```
Curriculum factor (when topic/weight relevant)
    → Learning Evidence (mission/skip/time/accept ids)
        → BehaviourState factor(s) (session/pattern/adherence lineage)
            → Readiness factor (pace/consistency — when relevant)
                → Decision Engine reason code(s) (feasibility / intensity)
                    → Recommendation explanation
```

Behaviour contributes **practice-feasibility and pace factors**, not mastery claims.

## 9.2 Explainable Behaviour factors (structural era)

Even before scoring, explanations can cite structural facts:

| Factor class | Example citation |
|---|---|
| **Adherence event** | “Mission M missed on date D (evidence id …).” |
| **Skip pattern lineage** | “Multiple Friday revision skips referenced in session history.” |
| **Effort structure** | “Time-on-task evidence present; no assessment evidence in the same window.” |
| **Preference loop** | “Recommendation for Topic T dismissed (Decision State primary; Behaviour secondary).” |
| **Cold start** | “No Behaviour evidence yet — feasibility confidence low.” |

## 9.3 Separation rules for honest narration

1. Never equate “you completed the mission” with “you demonstrated learning.”  
2. When Friday skips and stale Memory co-occur, explain **both** — do not merge into one opaque score.  
3. Coach/Insight may narrate Twin + evidence only; no fabricated skip reasons.  
4. Derived consistency scores (later) must remain named, factorable, and evidence-linked.

## 9.4 Forbidden explanation patterns

- Opaque “engagement score” as readiness  
- UI streak badges cited as Twin authority  
- LLM rationales that invent Behaviour patterns  
- Treating accept/dismiss as Knowledge change  

---

# 10. Registration within Twin Pipeline

## 10.1 Pipeline position

```
Learning Evidence (append-only)
      → UpdateContext (Twin + evidence + metadata)
            → TwinUpdatePipeline
                  → registered Update Strategies (registration order)
                        → KnowledgeUpdateStrategy
                        → MemoryUpdateStrategy
                        → BehaviourUpdateStrategy   ← Capability 2.5
                        → PerformanceUpdateStrategy ← Capability 2.6 (later)
                        → … future strategies
                  → UpdateResult (original Twin, updated Twin, applied_strategies, …)
```

The pipeline remains an orchestration shell. It must not hard-code Behaviour algorithms. Registration is via constructor list or `register` — same extension point as Knowledge/Memory.

## 10.2 Recommended registration order (structural phase)

| Order | Strategy | Rationale |
|---|---|---|
| 1 | `KnowledgeUpdateStrategy` | Existing; assessment/attempt primary |
| 2 | `MemoryUpdateStrategy` | Existing; revision primary |
| 3 | `BehaviourUpdateStrategy` | Practice/adherence; often independent of topic slots; secondary on assessment/revision |
| 4 | `PerformanceUpdateStrategy` (2.6) | Assessment summaries; register when Capability 2.6 lands |

**Why Behaviour after Knowledge/Memory in structural phase**

1. Preserves the already-shipped Knowledge → Memory order.  
2. Behaviour structural updates do not require prior Knowledge/Memory mutation to be correct.  
3. Mixed batches remain reproducible when order is fixed and documented.  
4. Future belief enrichment that *reads* other domains from the Twin can rely on Knowledge/Memory already refreshed in the same batch if needed — without Behaviour needing that today.

If a later capability proves Performance must precede Knowledge for belief enrichment, revisit order in a dedicated architecture note; do not silently reorder in product code.

## 10.3 Invocation rules

1. Invoke every registered strategy where `supports(context)` is true, in registration order.  
2. Each `apply` receives a context whose Twin reflects prior strategies.  
3. Multiple strategies may apply to one batch; ownership matrix prevents domain theft.  
4. No strategies registered → no-op success with explanatory messages (existing pipeline semantics).  
5. `UpdateResult.applied_strategies` must include Behaviour’s stable name when it ran.

## 10.4 Decision Engine loop closure

Accept/dismiss outcomes become Learning Evidence and re-enter this pipeline. Decision Engine must **not** mutate Behaviour in place.

```
Decision Engine (read Twin)
      → Recommendation / Mission projection
            → Student accept/dismiss/complete
                  → Learning Evidence
                        → TwinUpdatePipeline (incl. BehaviourUpdateStrategy)
```

---

# 11. Future scoring hooks

## 11.1 Structural hooks reserved now

| Hook | Structural home | Future filler |
|---|---|---|
| `consistency_metrics` bag | `BehaviourState` | Named adherence/consistency values from a later engine |
| Session / pattern id lineage | `BehaviourState` | Pattern inference ids with evidence provenance |
| Optional `BehaviourRecord` fields | Nested records | Soft scores per unit — preserved-unknown until computed |
| Evidence id lineage | State and/or records | Audit for derived metrics |

## 11.2 Deferred derived concepts

| Derived concept | Likely future owner | Constraint |
|---|---|---|
| Consistency score / quality | Behaviour enrichment or Prediction features | Sustainable regularity ≠ streak length |
| Adherence ratio | Planning / Behaviour metrics | Windowed; pattern-over-anecdote |
| Skip/abandon clusters | Pattern inference | Multi-event; store references not opaque blobs without lineage |
| Learning velocity (effort-adjusted) | Cross-domain derivation | Must not redefine mastery |
| Burnout risk | Motivation / Predictions consuming Behaviour | Behaviour supplies volume/load facts only |
| Preferred study windows | Notifications / Decision feasibility | Timing personalisation |

## 11.3 Scoring extension rules

1. Prefer filling reserved slots over inventing parallel Behaviour stores.  
2. Derived engines may **read** Behaviour structure and **emit** new evidence or write beliefs via strategy extension — not via Flask services mutating Twin.  
3. Derived Behaviour must not emit the overall readiness composite.  
4. Numeric engines remain unlocked (Educational Intelligence Architecture §11.3) beyond ownership.  
5. Confidence remains separable even if some ratings appear as secondary Behaviour signals.

---

# 12. Risks

| Risk | Impact | Architectural mitigation |
|---|---|---|
| **Equating Behaviour with learning** | False mastery; broken trust | Hard rule; ownership matrix; strategy non-goals |
| **Equating Behaviour with readiness** | Mission theatre replaces exam preparedness | Readiness derived multi-factor; Behaviour is one input |
| **Domain collapse into Motivation** | Unexplainable “engagement score” | Behaviour holds practice facts; Motivation separable |
| **Streak / gamification capture** | Unsustainable intensity rewarded | Consistency ≠ streak; streaks are projections |
| **Mission rows as Behaviour authority** | Stale private state | Missions are projections; evidence → strategy → Twin |
| **Single-skip overreaction** | Noisy coaching and plan thrash | Pattern-over-anecdote for derived metrics |
| **Secondary evidence theft** | Behaviour absorbs quizzes/revisions | Primary columns stay Knowledge/Memory/Performance |
| **Strategy order hazards** | Non-reproducible updates | Fixed registration order (§10.2); document in capability review |
| **Premature scoring complexity** | Unmaintainable adherence math | Structural strategy first; hooks only |
| **Confidence/Behaviour conflation** | Self-report treated as habit truth | Confidence separable; ratings Confidence-primary |
| **Parallel learner-state in analytics** | Divergent “engagement readiness” | Analytics read Twin; no forked Behaviour formulas |
| **LLM habit invention** | Fabricated skip reasons | Coach narrates Twin + evidence only |
| **topic_id over-requirement** | Missed Behaviour updates on mission-only evidence | Behaviour `supports` must not mandate topic identity |
| **V1/V2 mistaken exemption** | Inventing topic trees for Behaviour | Curriculum-referenced when tagged; never invents syllabus |
| **In-place Twin mutation** | Broken snapshot audit | Immutable snapshots only |

---

# 13. Extensibility

## 13.1 Safe extension points

| Extension | How to extend safely |
|---|---|
| **Register `BehaviourUpdateStrategy`** | Pipeline registration; framework-free; immutable snapshots |
| **Richer consistency metrics** | Fill `consistency_metrics` via later engines; keep structural slots stable |
| **New Behaviour evidence types** | Evidence catalogue + ownership matrix primary/secondary assignment |
| **Nested BehaviourRecord** | Additive optional nested structure; freeze records; prefer tuples/id lists |
| **Pattern inference** | Derive pattern ids from evidence aggregates; store references with lineage |
| **Context tags** | Commute vs deep work; device — additive metadata on evidence |
| **Collaboration attendance** | Optional Behaviour evidence; Knowledge remains individual |
| **Notification engagement** | Behaviour secondary; never Knowledge |
| **Burnout / Motivation models** | Consume Behaviour volume/load; do not overwrite Knowledge/Memory |
| **Prediction features** | Completion/burnout forecasts read Behaviour; write via Prediction snapshot path only |
| **Performance strategy (2.6)** | Register after Behaviour (or revise order via architecture note); dual updates remain valid |

## 13.2 Compatibility guarantees

1. Curriculum V1 and V2 remain loadable; Behaviour must not require Sections globally.  
2. Structural Twin fields prefer additive optional fields over breaking renames.  
3. Evidence append-only semantics remain permanent.  
4. Deterministic cores remain free of required network LLM calls.  
5. Knowledge and Memory remain complementary mastery/retention stores — Behaviour must not become a third.  
6. Existing Knowledge → Memory registration continues to work when Behaviour is added.

## 13.3 Deliberately unlocked

- Exact adherence ratios and windows  
- Burnout probability models  
- Learning velocity formulas  
- Preferred-hour personalisation algorithms  
- Any gamification surface  
- Final Decision Engine scoring function  

---

# 14. Architecture diagrams

## 14.1 Write path

```
Student / system occurrence
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
      ├─ KnowledgeUpdateStrategy   (if supports)
      ├─ MemoryUpdateStrategy      (if supports)
      ├─ BehaviourUpdateStrategy   (if supports)  ← this capability
      └─ PerformanceUpdateStrategy (later)
      │
      ▼
UpdateResult
  ├── original_twin
  ├── updated_twin          (new snapshot; BehaviourState evolved when applicable)
  ├── applied_strategies
  └── processing_messages
```

## 14.2 Behaviour domain focus

```
┌─────────────────────────────────────────────────────────────┐
│                     DigitalTwin snapshot                      │
│  Identity · Goals · Knowledge · Memory · Behaviour · …        │
│                              ▲                                │
│                              │ structural write only          │
│                     BehaviourUpdateStrategy                   │
│                              ▲                                │
│              Behaviour-primary / secondary evidence           │
└─────────────────────────────────────────────────────────────┘

BehaviourState (structural)
  ├── consistency_metrics     (slots; not computed here)
  ├── session_history_ids     (lineage)
  ├── study_pattern_ids       (lineage; no invented clusters)
  ├── last_updated
  └── optional BehaviourRecord[] / evidence_ids (additive)
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

## 14.4 Read-side consumption (not write)

```
BehaviourState
      │
      ├─► Readiness Aggregation   (pace / consistency factor)
      ├─► Decision Engine         (feasibility / intensity)
      ├─► Mission Generation      (load tuning)
      ├─► Planning rebalance      (capacity realism)
      └─► Predictions / Coach     (features / narration)
```

Read consumers must not write Behaviour truth.

## 14.5 Recommendation loop

```
Decision Engine ──► Recommendation
                         │
              accept / dismiss / complete
                         │
                         ▼
              Learning Evidence
                         │
                         ▼
         TwinUpdatePipeline (+ Behaviour secondary
              for accept/dismiss; Decision State primary)
```

---

# 15. Recommendations

## 15.1 For the next implementation milestone

1. Treat [`CAPABILITY_2_5_BEHAVIOUR_DOMAIN_ANALYSIS.md`](CAPABILITY_2_5_BEHAVIOUR_DOMAIN_ANALYSIS.md) plus **this document** as the charter for `BehaviourUpdateStrategy`.  
2. Implement **structural-only** Behaviour updates — references, timestamps, preserve `consistency_metrics`, no scoring.  
3. Fix `supports` types explicitly to the primary set in §5.3; document any secondary weak updates.  
4. Register after Knowledge and Memory (§10.2); do not hard-code Behaviour inside the pipeline class.  
5. Do **not** require `topic_id` for Behaviour applicability.  
6. Prefer additive optional fields / optional `BehaviourRecord` over breaking `BehaviourState` renames.  
7. Keep missions as projections; Mission Generation consumes Behaviour and emits evidence — it does not own Behaviour.  
8. Do not expand Confidence into Behaviour ownership.  
9. Defer Performance registration details to Capability 2.6, while preserving dual-update validity for abandoned assessments and quizzes.

## 15.2 Educational design recommendations

1. Prefer explainable patterns over punitive single-event messaging.  
2. Always separate “you showed up” from “you demonstrated learning.”  
3. Use Behaviour to **constrain ambition**, not to inflate readiness.  
4. When Behaviour slips and Memory risk co-occur, explain both factors.  
5. Cold start: explicit low confidence — never optimistic perfection or punitive unreliability.

## 15.3 Architecture compliance checklist

| Invariant | Status for this architecture |
|---|---|
| Twin is sole educational state authority | BehaviourState lives only in Twin |
| Evidence is only legitimate belief input | Required |
| Strategies own domain evolution | `BehaviourUpdateStrategy` defined |
| Pipeline only coordinates | Registration; no hard-coded Behaviour math |
| Behaviour ≠ learning; activity ≠ readiness | Binding |
| Knowledge/Memory complementary stores preserved | Behaviour must not become a third mastery store |
| V1/V2 curriculum compatibility | Behaviour must not invent syllabus or require V2-only structure |
| Structural before scoring | Explicit |
| No implementation in this milestone | Satisfied by architecture-only deliverable |

## 15.4 Explicit stop line

This milestone delivers **architecture only**.

**Do not proceed in this milestone to:** code, tests, database changes, services, scoring formulas, or UI.

Next engineering step (separate milestone): structural `BehaviourUpdateStrategy` implementation → tests → capability review — following Epic 2 engineering standards.

---

# Appendix A — Capability map

| ID | Capability | Relation to this document |
|---|---|---|
| 2.1–2.2 | Twin + Pipeline | Host aggregate and registration shell |
| 2.3–2.4 | Knowledge / Memory strategies | Structural precedents Behaviour must follow |
| **2.5** | **Behaviour Update Strategy** | **This architecture** |
| 2.5 prior | Behaviour Domain Analysis | Domain charter this architecture implements |
| 2.6 | Performance | Distinct assessment domain; secondary Behaviour only |
| 2.7 | Readiness | Consumes Behaviour as pace/consistency factor |
| 2.8–2.10 | Decision / Recommendation / Missions | Read Behaviour for feasibility; write back via evidence |

---

# Appendix B — Document control

| Field | Value |
|---|---|
| Milestone | Capability 2.5 — Behaviour Update Strategy Architecture |
| Nature | Architecture only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility required going forward; no traversal changes |
| Application code intentionally untouched | Yes |
| Preceded by | Behaviour Domain Analysis (approved) |
| Next | Structural `BehaviourUpdateStrategy` implementation (separate milestone) |

---

*End of Capability 2.5 Behaviour Update Strategy Architecture.*
