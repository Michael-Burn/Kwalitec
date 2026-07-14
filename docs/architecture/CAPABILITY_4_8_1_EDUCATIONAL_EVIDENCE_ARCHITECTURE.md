# Capability 4.8.1 — Educational Evidence Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 4 — Educational Intelligence Evolution (Internal Alpha active)  
**Capability:** 4.8.1 Educational Evidence (first-class educational observation layer preceding Twin Update, Evidence contracts, and persistence)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Evidence companion (Epic 0 catalogue):** [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md)  
**Upstream Calibration:** [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md)  
**Upstream Twin Persistence:** [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md)  
**Upstream Twin retrieval:** [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md)  
**Scope:** Structural architecture for Educational Evidence as the sole educational input that may evolve a Digital Twin — **no code, Flask, ORM, contracts, persistence schemas, product flows, UI, migrations, or tests**

---

## Document purpose

Epic 3 completed the Birth Twin architecture. Internal Alpha is now active. The next phase of Educational Intelligence is allowing the Digital Twin to evolve.

That evolution has a hard educational law:

> **The Digital Twin must NEVER evolve directly from student activity.**  
> **It evolves only through Educational Evidence.**

Mission completion is an event. A study session is transient. A button click is product interaction. A student declaration at birth is Calibration prior — not Evidence.

**Educational Evidence** is the permanent educational observation that may lawfully drive Twin Update Strategies. Educational Intelligence must never reason directly from raw activity; it reasons from Twins that Evidence has earned the right to evolve.

**Governing principle (binding):**

> **Evidence records observations. It never records conclusions. The Twin evolves from Evidence — never from activity.**

**Architectural restatement:**

> **Educational Evidence is the sole educational input that may evolve a Digital Twin. Twin Update Strategies interpret Evidence and author successor Twins. Educational Intelligence consumes Twins. Neither Educational Intelligence nor the Twin owns Evidence. Evidence remains independent, immutable, observational educational memory.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Educational Evidence** | First-class educational observation that may lawfully drive Twin evolution (this capability) |
| **Learning Evidence** | Epic 0 catalogue / companion model in [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md) — deeper type catalogue; this document establishes Twin-evolution law and Version 1.0 boundaries |
| **Student activity** | Transient product events (missions, sessions, clicks, UI actions) — never Twin-mutation authority |
| **Calibration declaration** | Self-declared history at Twin birth — priors only; **not** Educational Evidence |
| **Twin Update Strategy** | Lawful interpreter of Evidence that authors a successor Twin snapshot |
| **Educational judgement** | Mastery, readiness, pass probability, recommendations — never stored as Evidence |

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Flask routes, forms, templates, or product UX flows  
- Database schemas, Alembic migrations, ORM models, or Evidence persistence technology  
- Evidence contracts, APIs, or recorder implementations  
- Twin Update Pipeline redesign or Strategy algorithms  
- Readiness, Decision, Recommendation, Mission, or dashboard logic  
- Assessment interpretation engines or AI observation pipelines  

---

# 1. Purpose

## 1.1 Why Educational Evidence exists

Without Educational Evidence as a first-class concept:

- Twin Update Strategies would be pressured to read missions, sessions, and clicks as if they were educational truth.  
- Educational Intelligence would reason from transient product activity instead of durable educational memory.  
- Completion theatre would masquerade as learning (“mission done ⇒ mastery”).  
- Birth Twin honesty (Calibration priors, thin warrant) would collapse the moment Internal Alpha records activity without an observational layer.  
- Audit and explainability would break — recommendations could not cite what was *observed*, only what the UI happened to do.

**Educational Evidence** exists to:

1. **Separate observation from interpretation** — record what was educationally observed; leave judgement to Twin Update Strategies and Educational Intelligence.  
2. **Make student activity durable as educational memory** — transient events may *generate* Evidence; they do not themselves evolve the Twin.  
3. **Protect Twin immutability and succession law** — Evidence feeds Strategies; Strategies author successor Twins; Evidence never edits a Twin.  
4. **Protect Educational Intelligence honesty** — Intelligence consumes Twins, never raw activity streams.  
5. **Preserve educational honesty** — observations remain observations; they do not smuggle mastery, readiness, or pass probability into the history log.

It is the lawful answer to:

> “What educational observation may the platform remember so the Twin can evolve truthfully?”

It is **not** the answer to:

> “What does the student know?”  
> “How ready are they?”  
> “What should they study next?”

```
Student activity (transient)
              ↓
   Educational Evidence          ← permanent educational observation (this document)
              ↓
   Twin Update Strategies        ← interpret Evidence; author successor Twin
              ↓
   Digital Twin (immutable snapshot)
              ↓
   Educational Intelligence      ← consumes Twin; never consumes raw activity
```

Governing restatement:

> **Mission completion is an event. Educational Evidence is an educational observation. Student activity is transient. Evidence becomes permanent educational memory.**

## 1.2 Relationship with Birth Twin and Internal Alpha

| Concern | Owner |
|---|---|
| Birth Twin from self-declared history | **Student Calibration** (Capability 3.6) |
| Durable storage of Twin snapshots | **Twin Persistence** (Capability 3.7) |
| Sole educational input that may evolve the Twin after birth | **Educational Evidence** (this document) |
| Interpretation of Evidence into successor Twins | **Twin Update Strategies / Pipeline** |
| Educational judgement from Twin state | **Educational Intelligence** |

**Rules:**

1. **Calibration births; Evidence evolves.** Declarations at birth are priors, not Evidence.  
2. **Activity does not mutate Twins.** Only Evidence → Strategies → successor Twin is lawful evolution.  
3. **Internal Alpha activity without Evidence remains educationally inert** for Twin evolution — recorded product behaviour must not silently become mastery.  
4. **Absence of Evidence is not permission to invent Mid beliefs.** Thin warrant and cold-start honesty survive until Evidence densifies.

---

# 2. Educational philosophy

These principles bind Educational Evidence. They extend ADR-002’s Educational Evidence Principle, Twin law, and Epic 3 honesty into Twin evolution.

### Evidence records observations

Educational Evidence states what was observed: a mission completed, a session lasted N minutes, a topic was studied, a practice block finished, a reflection was given, an assessment result was recorded, a system observation was noted. It does not state what those observations *mean* educationally.

### Evidence never records conclusions

Mastery, readiness, pass probability, preparedness bands, confidence scores as judgements, recommendation quality, motivation diagnoses, and learning-style labels are **not** Evidence. Writing conclusions into Evidence poisons the audit spine and collapses observation into judgement.

### Evidence is immutable

Once written, an Evidence record is never edited in place. Corrections are new compensating Evidence (e.g. voided attempt, corrected attribution). History is append-only educational memory.

### Evidence does not estimate readiness

Preparedness belongs to Readiness Aggregation consuming Twin state. Evidence may later *inform* Strategies that change Twin domains Readiness reads — Evidence itself never emits readiness %.

### Evidence does not estimate mastery

Knowledge beliefs evolve only through Twin Update Strategies interpreting Evidence. Evidence never stores mastery percentages or “now Mid” claims.

### Evidence does not predict success

Pass probability and predicted marks belong to Predictions / later calibrated forecasting. Evidence records outcomes and observations; it does not forecast.

### Evidence is educationally honest

Sparse Evidence remains sparse. Weak observations remain weak. Self-report reflections remain tagged as self-report. System observations remain system observations. Honesty is structural, not rhetorical.

### Evidence separates observation from interpretation

| Layer | Role |
|---|---|
| **Educational Evidence** | Observes and remembers |
| **Twin Update Strategies** | Interpret Evidence; author successor Twin |
| **Educational Intelligence** | Judges from Twin; recommends next action |

Crossing these roles recreates study-planner pathology: activity mistaken for learning, completion mistaken for mastery.

### Evidence is attributable

Every Evidence record must be able to answer, architecturally: who (student), what (observation type), when (time), whence (source), and — when syllabus-scoped — which curriculum identity. Attribution enables explainability without implementing schemas here.

### Curriculum identity remains canonical

Topic-scoped Evidence references official syllabus entities. Evidence never invents parallel topics or free-text syllabus truth.

Governing restatement:

> **Observe honestly. Remember permanently. Interpret elsewhere. Never smuggle judgement into the observation log.**

---

# 3. Ownership

## 3.1 Ownership chain (binding)

```
Student
   ↓
Study Session
   ↓
Educational Evidence
   ↓
Twin Update Strategy
   ↓
Digital Twin
   ↓
Educational Intelligence
```

| Stage | Owns | Does not own |
|---|---|---|
| **Student** | Lived study behaviour and declarations | Twin beliefs; Evidence authorship policy |
| **Study Session** | Transient activity container (time, topic engagement, mission attempts) | Permanent educational memory; Twin mutation |
| **Educational Evidence** | Immutable educational observations derived from (or about) study | Twin snapshots; readiness; mastery; recommendations |
| **Twin Update Strategy** | Interpretation of Evidence into successor Twin authorship | Evidence content; Educational Intelligence selection |
| **Digital Twin** | Authoritative learner-state snapshot (immutable) | Evidence log; raw activity streams |
| **Educational Intelligence** | Judgement from Twin (Readiness → Decision → Recommendation → Mission) | Evidence ownership; Twin authorship from activity |

## 3.2 Educational Evidence owns

| Responsibility | Meaning |
|---|---|
| **Observation capture law** | Define which educational observations may enter the Evidence spine in Version 1.0. |
| **Independence** | Evidence exists as educational memory independent of Twin and Intelligence ownership. |
| **Immutability / append-only posture** | Records are permanent; corrections are new records. |
| **Non-judgemental content** | Evidence payload remains observational — no mastery, readiness, or recommendation fields as authority. |
| **Provenance of observation** | Source class (student action, reflection, assessment result, system observation) remains explicit. |
| **Syllabus-safe scoping** | When topic-scoped, reference canonical curriculum identities only. |

## 3.3 Educational Evidence never owns

| Forbidden ownership | Why |
|---|---|
| **Digital Twin snapshots** | Twin Persistence / TwinRepository store Twins; Strategies author them. |
| **Twin mutation** | Evidence never edits a Twin; Strategies produce successors. |
| **Educational Intelligence judgements** | Readiness, Decision, Recommendation, Mission remain downstream of Twin. |
| **Calibration** | Self-declared birth history is prior construction, not Evidence. |
| **Mission generation** | Missions are consequences of Intelligence, not Evidence content. |
| **Dashboard / product analytics as second truth** | Product metrics may *mirror* Evidence; they must not become a competing learner model. |

## 3.4 Independence invariants

1. **Educational Intelligence never owns Evidence.** It consumes Twins.  
2. **The Twin never owns Evidence.** It may carry Evidence lineage ids as hooks; it is not the Evidence log.  
3. **Evidence is independent.** Deleting or ignoring a Twin snapshot must not rewrite Evidence history; Evidence history must not silently rewrite past Twin snapshots.  
4. **Study Sessions do not own Evidence.** Sessions may produce Evidence; they are not themselves Evidence.  
5. **Product activity is not Twin authority.** Missions, clicks, and UI state never mutate Twin domains.

### Owner map (no duplication)

| Concept | Layer | Relation to Educational Evidence |
|---|---|---|
| **Educational Evidence** | Domain / educational memory | Sole Twin-evolution input (this document) |
| **Student Calibration** | Application | Birth priors only; never Evidence authorship |
| **Twin Update Pipeline / Strategies** | Domain | Sole lawful Evidence interpreters → successor Twins |
| **Twin Persistence / TwinRepository** | Application | Stores Twin snapshots — not Evidence catalogue ownership |
| **TwinProvider** | Application | Retrieves Twin; never invents Evidence |
| **EvidenceRecorder** (future) | Application | Write-path bridge from product events → Evidence — not defined here |
| **Educational Orchestrator** | Application | Composes Intelligence from Twin; never consumes raw activity as Twin substitute |
| **Readiness / Decision / Recommendation / Mission** | Domains | Downstream of Twin; never Evidence authors or Twin mutators via activity |

Governing restatement:

> **Evidence answers only: “What educational observation was recorded?” It never answers preparedness, mastery, or next action. It never owns the Twin.**

---

# 4. What IS Educational Evidence

Version 1.0 Educational Evidence is a closed set of **observations**. Each item below is an observation. None are interpretations.

## 4.1 Version 1.0 observation classes

| Observation | What is recorded (observational) | What is *not* recorded |
|---|---|---|
| **Mission completed** | That a mission was completed, with scope and time context | That the student mastered the topic |
| **Mission abandoned** | That a mission was abandoned / left incomplete | That the student lacks motivation or will fail |
| **Study duration** | Duration of study observed in a session | That time-on-task equals learning |
| **Topic studied** | That a syllabus-scoped topic was studied | Coverage %, mastery, or readiness |
| **Practice completed** | That a practice block / practice attempt completed | That practice proves exam readiness |
| **Student reflection** | What the student reported about their study (self-report) | Validated confidence, learning style, or motivation diagnosis |
| **Assessment result** | Observed scored / judged outcome against syllabus scope | Pass probability, predicted mark, or readiness band |
| **System observation** | Platform-observed educational fact that is not student-declared judgement (e.g. session timing anomaly recorded as observation) | Product heuristic conclusions disguised as “system insight” |

## 4.2 Observation invariant

> **If it concludes, diagnoses, ranks, forecasts, or recommends — it is not Educational Evidence.**

## 4.3 Relationship to student activity

Student activity may **give rise** to Educational Evidence:

```
Mission marked complete (activity)
        ↓
Mission completed (Educational Evidence observation)
        ↓
Twin Update Strategy may interpret
        ↓
Successor Twin (if Strategy warrants change)
```

The activity record and the Evidence observation are not the same artefact. Product may keep operational mission state for UX; Educational Evidence is the educational memory spine.

## 4.4 Calibration is not Evidence

Self-declared Core Reading, prior attempts, and declared completed sections at Twin birth remain **Calibration priors** under Capability 3.6. They must not be rewritten as Educational Evidence to “bootstrap density.” Fabricating Evidence from declarations poisons Evidence sovereignty.

---

# 5. What is NOT Educational Evidence

The following belong elsewhere. They must never be stored as Educational Evidence authority.

| Concept | Why it is not Evidence | Lawful owner |
|---|---|---|
| **Mastery** | Belief / estimate about knowledge | Knowledge domain via Twin Update Strategies |
| **Readiness** | Preparedness judgement | Readiness Aggregation |
| **Pass probability** | Forecast | Predictions / later calibrated forecasting |
| **Preparedness** | Product/UX restatement of readiness | Readiness / Experience honesty — not Evidence |
| **Confidence score** (as judgement) | Domain belief or measured-vs-felt calibration | Confidence domain (separable); self-report *reflection* may be Evidence, the score-as-truth is not |
| **Recommendation quality** | Evaluation of Decision / Recommendation outputs | Evaluation frameworks / product review — not learner Evidence |
| **Motivation** (as diagnosis) | Interpretive Behaviour / Motivation belief | Twin domains via Strategies — not raw Evidence payload |
| **Learning style** | Unsupported educational stereotype / opaque profile | Out of Version 1.0 Evidence; not Twin-evolution authority |

### Anti-pattern restatement

> **Do not promote Intelligence outputs, Twin beliefs, or product scores into Evidence so that they can later “prove” themselves.** That circularity destroys educational honesty.

---

# 6. Relationship with the Digital Twin

## 6.1 Evolution chain (binding)

```
Birth Twin
     ↓
Educational Evidence
     ↓
Twin Update Strategy
     ↓
Successor Twin
```

| Step | Law |
|---|---|
| **Birth Twin** | Authored by Student Calibration (priors + Identity / Goals); not Evidence-backed belief density |
| **Evidence accumulates** | Append-only educational observations after birth |
| **Strategies interpret** | Twin Update Strategies consume prior Twin + Evidence and author a new snapshot |
| **Successor Twin** | New immutable Twin; prior Twin remains historical truth of what the product believed before |

## 6.2 Evidence never edits a Twin

Educational Evidence does not patch Knowledge, Memory, Behaviour, Performance, Confidence, or Goals fields. It does not call Persistence as a belief editor. It does not “apply itself” to a live Twin object.

Only Twin Update Strategies (via the Twin Update Pipeline) may produce educational change — and only as **successor snapshots**.

## 6.3 Twin snapshots remain immutable

| Rule | Meaning |
|---|---|
| **No in-place mutation** | Evidence-driven change replaces the current Twin with a successor whole |
| **History retained** | Prior snapshots remain valid history of past beliefs |
| **Provenance survives** | Calibration `self_declared` markers are not rebranded as Evidence-backed by Evidence arrival alone; Strategies must make warrant changes explicit when beliefs evolve |
| **Lineage hooks allowed** | Twins may reference Evidence ids that justified succession — hooks are not Evidence ownership |

## 6.4 Twin never owns Evidence

The Twin is authoritative *state*. Educational Evidence is authoritative *observation history* that may evolve that state. Conflating them recreates planner-first pathology (state without audit spine, or activity log mistaken for learner model).

Governing restatement:

> **Evidence never edits a Twin. Twin Update Strategies interpret Evidence. Twin snapshots remain immutable.**

---

# 7. Relationship with Educational Intelligence

## 7.1 Consumption firewall (binding)

| Consumer | Consumes | Must not consume as educational authority |
|---|---|---|
| **Twin Update Strategies** | Educational Evidence (+ prior Twin) | Raw missions / clicks as silent Twin writes |
| **Educational Intelligence** (Readiness → Decision → Recommendation → Mission) | Digital Twin (+ Curriculum + Goals / constraints as applicable) | Raw student activity; Evidence as a substitute Twin; dashboard metrics as Twin |
| **Educational Orchestrator** | Twin via TwinProvider; composed Intelligence outputs | Direct Evidence reasoning that bypasses Twin |

## 7.2 Two write/read worlds

```
WRITE path (evolution):
  Activity → Educational Evidence → Twin Update Strategies → Successor Twin → Twin Persistence

READ path (guidance):
  Twin Persistence → TwinProvider → Orchestrator → Educational Intelligence → Mission / Plan consequences
```

**Rules:**

1. **Educational Intelligence consumes Twins.**  
2. **Twin Update consumes Evidence.**  
3. **Educational Intelligence never consumes raw student activity** as if it were Twin state or Evidence authority.  
4. **Evidence is not a back door into recommendations.** Citing Evidence in explanations is lawful only as lineage through Twin / Decision explainability — not as “mission completed yesterday ⇒ recommend X” without Twin mediation.

## 7.3 Why the firewall exists

If Educational Intelligence read missions and sessions directly:

- completion would masquerade as readiness;  
- ephemeral UI state would drive educational selection;  
- Twin domains would become optional theatre;  
- explainability would cite product events instead of educational state.

Evidence → Twin → Intelligence preserves ADR-002’s chain and Internal Alpha honesty.

Governing restatement:

> **Update Strategies write from Evidence. Educational Intelligence reads from Twins. Activity never shortcuts either path.**

---

# 8. Educational boundaries

Educational Evidence remains **observational only**. Version 1.0 architecture forbids the following inside Evidence ownership:

| Boundary | Forbidden inside Evidence |
|---|---|
| **No recommendation generation** | Evidence must not select next actions or package Missions |
| **No readiness reasoning** | Evidence must not compute preparedness bands or overall readiness % |
| **No assessment interpretation beyond observation** | Recording an assessment result is lawful; inferring mastery maps, grade curves, or pass forecasts inside Evidence is not |
| **No mission generation** | Missions remain Intelligence consequences |
| **No dashboard logic** | Analytics / dashboard aggregates are not Evidence authority and must not write Twin beliefs |
| **No Twin authorship** | Evidence does not create Birth or Successor Twins |
| **No Calibration substitution** | Evidence does not replace or silently re-enact Calibration priors |
| **No Educational Intelligence judgement storage** | Storing Decision outcomes as Evidence “to close the loop” without a distinct evaluation model is out of scope and dangerous |

### Boundary invariant

> **Evidence observes. Strategies interpret. Intelligence judges. Product displays. Those verbs do not commute.**

---

# 9. Version 1.0

Version 1.0 is deliberately simple. Educational Evidence must support Twin evolution for Internal Alpha honesty without opening an unbounded observation catalogue.

## 9.1 Supported Version 1.0 surfaces

| Surface | Version 1.0 posture |
|---|---|
| **Calibration** | Remains birth priors — **not** Evidence; Evidence architecture respects Calibration sovereignty and does not seed fake Evidence from declarations |
| **Mission completion** | Observation: completed / abandoned |
| **Study sessions** | Observation: duration, topic studied (syllabus-scoped) |
| **Practice** | Observation: practice completed (and assessment result when scored practice exists) |
| **Reflection** | Observation: student reflection (self-report tagged) |

## 9.2 Explicitly out of Version 1.0 Evidence scope

- Tutor observations  
- AI / LLM observations as Twin-evolution authority  
- Rich assessment analytics beyond recording results  
- Behavioural evidence catalogues beyond mission/session/practice/reflection observations named above  
- Motivation engines, learning-style profiles, engagement theatre scores  
- Recommendation-quality Evidence loops  
- Contracts, persistence schemas, recorder implementations  

## 9.3 Version 1.0 success criteria (architectural)

Version 1.0 succeeds when:

1. Twin evolution has a lawful observational input that is not raw activity.  
2. Birth Twin honesty is preserved until Evidence densifies.  
3. Strategies have something educationally honest to interpret (when product records observations).  
4. Educational Intelligence still consumes only Twins.  
5. The catalogue remains small enough to implement later without redesigning Twin or Intelligence law.

Governing restatement:

> **Version 1.0 Evidence is enough to evolve the Twin honestly — and nothing more.**

---

# 10. Future evolution

Later versions may deepen Educational Evidence **without redesigning Version 1.0**.

## 10.1 Additive evolution principle

| Future class | How it extends Version 1.0 | What must not change |
|---|---|---|
| **Tutor observations** | New observation class with explicit tutor provenance | Must remain observational; tutor opinion ≠ automatic mastery |
| **AI observations** | New observation class with explicit AI provenance and lower/conditional warrant | Must never own Twin mutation or Educational Intelligence selection; no black-box core path |
| **Assessment analytics** | Derived *views* or richer assessment Evidence types | Analytics must not overwrite raw assessment result observations; judgement stays in Strategies / Intelligence |
| **Behavioural evidence** | Broader Behaviour observation catalogue (skips, reschedules, adherence patterns) | Behaviour observations ≠ learning; Strategies still interpret |

## 10.2 Compatibility law

1. **Additive observation classes** — prefer new types over rewriting Version 1.0 meanings.  
2. **Version 1.0 records remain valid history** — future loaders must not reinterpret “mission completed” as mastery.  
3. **Warrant remains explicit** — self-report, tutor, AI, and assessed sources stay distinguishable.  
4. **Twin Update Strategies absorb new interpretation** — Evidence catalogue growth does not move judgement into Evidence payloads.  
5. **Educational Intelligence chain unchanged** — Evidence → Strategies → Twin → Intelligence remains the only evolution/guidance chain.  
6. **No redesign debt for simplicity** — Version 1.0’s narrowness is intentional; future richness is extension, not apology.

## 10.3 Future non-goals that remain forbidden

Even in later versions:

- Evidence must not store readiness, mastery conclusions, or recommendations as authority.  
- Evidence must not edit Twins in place.  
- Educational Intelligence must not consume raw activity.  
- AI observations must not become silent Twin authors.

Governing restatement:

> **Grow the observation catalogue. Do not grow Evidence into Intelligence. Version 1.0 remains lawful forever as history.**

---

# 11. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **Activity → Twin shortcut** | Missions / sessions mutate Twin without Evidence | Enforce Evidence → Strategies → successor Twin only |
| **Conclusions in Evidence** | Mastery / readiness / pass % written as Evidence | Closed observational payload; review rejects judgement fields |
| **Fake Evidence from Calibration** | Declarations seeded as Evidence density | Hard ban; Calibration remains priors-only |
| **Intelligence reads activity** | Orchestrator / Decision bypass Twin | Read-path Twin-only educational authority |
| **Evidence edits Twin** | Recorder patches Twin fields | Immutability + Strategy authorship only |
| **Dashboard as second Evidence** | Analytics store becomes learner truth | Evidence independence; dashboards mirror, do not author |
| **Unbounded V1 catalogue** | Premature tutor/AI/behavioural sprawl | Version 1.0 closed surfaces only |
| **Completion = mastery theatre** | Mission completed Evidence treated as Mid Knowledge | Strategies + Intelligence thin-warrant honesty; Evidence stays observational |

### Risk restatement

The primary danger is not missing Evidence types. It is **Evidence that starts concluding** — or **activity that evolves the Twin without Evidence** — recreating planner pathology inside Educational Intelligence.

---

# 12. Architecture Compliance Summary

| Invariant | Status under this architecture |
|---|---|
| Twin never evolves from raw student activity | Required — Evidence is sole evolution input |
| Evidence is observational only | Required — no conclusions in Evidence |
| Evidence is immutable / append-only | Required |
| Twin snapshots remain immutable; succession via Strategies | Preserved |
| Educational Intelligence consumes Twins only | Preserved |
| Calibration ≠ Evidence | Preserved |
| Curriculum V1/V2 identity safety for topic-scoped Evidence | Required |
| No Flask / ORM / contracts / persistence / product flow in this milestone | Honoured — architecture only |

---

# 13. STOP

This document defines **Educational Evidence architecture only**.

It does **not** authorise:

- Implementation  
- Flask routes or services  
- ORM models, schemas, or migrations  
- Evidence contracts or recorder APIs  
- Twin Update Strategy algorithms  
- Persistence of Evidence  
- Product flows, dashboards, or UI  
- Educational Intelligence redesign  

**STOP.**

---

# References

| Artefact | Role |
|---|---|
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Governing ADR; Educational Evidence Principle |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Platform educational chain; Evidence → Twin → Intelligence |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Canonical Twin domain law; immutable snapshots |
| [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md) | Epic 0 Evidence catalogue companion |
| [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md) | Birth Twin priors; not Evidence |
| [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md) | Twin snapshot storage; not Evidence ownership |
| [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md) | Twin retrieval honesty on read path |
| [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md) | Shared educational vocabulary |
