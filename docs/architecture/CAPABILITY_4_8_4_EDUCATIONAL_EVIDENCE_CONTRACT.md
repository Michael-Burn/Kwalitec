# Capability 4.8.4 — Educational Evidence Contract

**Status:** Contract only — no implementation  
**Epic:** Epic 4 — Educational Intelligence Evolution (Internal Alpha active)  
**Capability:** 4.8.4 Educational Evidence Contract (immutable Presentation → Application handoff for educational observations)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Upstream Evidence architecture:** [`CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md)  
**Upstream educational analysis:** [`CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md`](CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md)  
**Upstream product flow:** [`CAPABILITY_4_8_3_EDUCATIONAL_EVIDENCE_PRODUCT_FLOW.md`](../product/CAPABILITY_4_8_3_EDUCATIONAL_EVIDENCE_PRODUCT_FLOW.md)  
**Contract companions:** [`CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md`](CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md), [`CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md`](CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md), [`CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md`](CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Evidence companion (Epic 0 catalogue):** [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md)  
**Scope:** Closed, immutable Application Contract for Version 1.0 Educational Evidence observations leaving Presentation — **no Flask, ORM, persistence, Twin Update, Educational Intelligence reasoning, or implementation**

---

## Document purpose

Capabilities 4.8.1–4.8.3 established:

- **Architecture** — Educational Evidence is the sole educational input that may evolve a Digital Twin; observations never conclusions.  
- **Educational analysis** — activity ≠ Evidence; observation ≠ interpretation; declared ≠ observed provenance.  
- **Product flow** — study ends; optional light reflection; observational Evidence emerges as a by-product of finishing study.

This milestone defines the **immutable Educational Evidence Contract**.

It answers:

> What exact observational artefact does Presentation hand to the Application Layer so Educational Evidence can be created consistently — and nothing else?

It is the sole Presentation → Application boundary for Version 1.0 educational observations after a study session ends.

**Governing principle (binding):**

> **The contract carries what was observed or declared about study. It never becomes educational meaning.**

**Architectural restatement:**

> **Presentation gathers observations. Application validates structure. Educational Evidence is created consistently. Educational Intelligence never receives Presentation objects. Twin Update never consumes this contract as belief algebra. The contract is the stable Application boundary — and it stops there.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Educational Evidence Contract** | Immutable closed observation handoff artefact (this document) — Version 1.0 |
| **Educational Evidence** | Permanent educational observation memory created after structural acceptance (architecture 4.8.1) — not this contract itself |
| **Observed event** | A system-recorded or student-confirmed educational fact carried in the contract |
| **Declared event** | A student self-report carried in the contract with explicit declared provenance |
| **Evidence creation** | Application construction of Educational Evidence from a structurally valid contract — conceptual; not implemented here |
| **Student Calibration Contract** | Birth declaration handoff (3.6.4) — priors only; never this Evidence contract |

**Non-goals of this document**

- Implementation types, dataclasses, JSON schemas, ORM, or API payloads  
- Flask routes, forms, templates, or UI design  
- Evidence Repository / persistence schemas or recorder classes  
- Twin Update Strategy algorithms or Pipeline redesign  
- Educational Intelligence reasoning, readiness, mastery, Decision, Recommendation, or Mission  
- Assessment engines, AI observation pipelines, or tutor tooling  

---

# 1. Purpose

## 1.1 Why the contract exists

Without a closed Presentation → Application contract for educational observations:

- end-of-session UI and Application invent incompatible observation shapes;  
- Presentation objects (session scraps, form drafts, mission UI state) leak into Educational Intelligence;  
- validation drifts into educational judgement (“did they really learn?”);  
- Evidence creation becomes inconsistent across complete / abandon / timeout paths;  
- Twin Update is tempted to read product events directly as Twin-mutation authority.

The **Educational Evidence Contract** exists so that:

1. **Presentation gathers observations** — mission outcome, duration, practice posture, optional reflection, identities, timestamps — into one closed handoff.  
2. **Application validates structure only** — required presence, identity integrity, timestamp legality, structural consistency — never educational truth.  
3. **Educational Evidence is created consistently** — the same Version 1.0 shape yields the same observational memory posture whenever the contract is accepted.  
4. **Educational Intelligence never receives Presentation objects** — Intelligence consumes Twins; it must not consume session UI cargo disguised as Evidence.  
5. **The contract becomes the stable Application boundary** — everything educational about “what happened in this study ending” crosses here or does not cross at all.

It is the lawful answer to:

> “What educational observations is Presentation authorised to hand Application after a study session ends?”

It is **not** the answer to:

> “What does the student know?” / “How ready are they?” / “What should they study next?” / “Should the Twin change?”

## 1.2 Relationship to Product Flow

Capability 4.8.3 defines the student journey:

```
Mission → study → End Session → optional light reflection
        ↓
Educational Evidence Contract   ← this document (Presentation → Application handoff)
        ↓
Application structural validation → Educational Evidence creation
        ↓
Session closes → student leaves
```

Product Flow owns *when* and *how calmly* observations are gathered.  
This Contract owns *what* must be present at the handoff after the closing moment emits observations.

| Product Flow concern | Contract concern |
|---|---|
| Entry at session end (complete / abandon / manual / timeout) | Contract carries ending outcome as observed events |
| Optional light reflection ≪ 1 minute | Reflection is Optional; omission is lawful |
| Skip reflection still records observed activity | Required observed events may still form a valid contract |
| No mastery / readiness questions | Forbidden fields rejected if smuggled as contract authority |
| Evidence as by-product of finishing study | Contract freezes observations — not conclusions |

Governing restatement:

> **Product Flow gathers and closes. The Contract freezes what was observed or declared. Application validates structure and creates Evidence. Meaning waits downstream.**

## 1.3 Relationship to Educational Evidence architecture

```
Educational Evidence Contract (immutable, Version 1.0)
              ↓
     Application (structural validation + Evidence creation)
              ↓
   Educational Evidence (permanent observational memory)
              ↓
   (Later) Evidence Repository → Twin Update → Successor Twin
              ↓
   (Later) Educational Intelligence consumes Twin
```

Rules:

1. **This contract is the sole Presentation → Application observation input** for Version 1.0 end-of-session Evidence.  
2. **Application creates Evidence from the contract** — it does not invent observations the contract omitted.  
3. **Educational Intelligence never reads this contract** as educational authority.  
4. **Twin Update never receives Presentation objects** — it consumes Educational Evidence (and prior Twin), not UI session state.  
5. **Calibration Contract remains a different artefact** — birth priors are not session Evidence and must not be rewritten into this contract.

Governing restatement:

> **No valid Educational Evidence Contract ⇒ no Evidence creation from that handoff. Never invent the missing observation.**

---

# 2. Ownership

Ownership is absolute. The contract is a handoff artefact, not a shared editable worksheet.

| Actor | Owns | Must never |
|---|---|---|
| **Presentation** | **Gather** educational observations from the ended study session; emit the contract after the closing moment (with or without optional reflection) | Perform educational math; invent mastery / readiness; write Twin beliefs; author Twin Update; mutate the contract after emit; send Presentation objects to Intelligence |
| **Application (validation)** | **Validate structure** of the emitted contract — required fields, identity integrity, timestamps, structural consistency | Infer mastery, readiness, pass probability, learning quality, or recommendations; “fix” educational coherence by inventing events |
| **Application (Evidence creation)** | **Create Educational Evidence** from a structurally accepted contract — observational memory only | Derive educational conclusions; call Twin Update as part of contract acceptance; fabricate optional fields |
| **Educational Intelligence** | Consume *Twins* later for judgement (Readiness / Decision / Recommendation / Mission) | **Own** this contract; consume Presentation objects; treat the contract as a live questionnaire to re-score |
| **Twin Update** | Interpret *Educational Evidence* later into successor Twin authorship | **Own** this contract; invent observations; treat contract validation as belief change |
| **Evidence Repository** (future) | Store immutable Educational Evidence after creation | Author observations; reinterpret declared as observed; invent missing Required cargo |
| **Student Calibration** | Birth priors via Calibration Contract | Write session Evidence; convert this contract into birth autobiography |

## 2.1 Presentation owns

| Responsibility | Meaning |
|---|---|
| **Mission completion / abandonment posture** | Gather ending outcome as an observation when known |
| **Study duration** | Gather system-observed and/or student-confirmed duration as observation cargo |
| **Reflection** | Gather optional self-report when the student provides it |
| **Practice information** | Gather practice attempted / completed posture as observed and/or declared |
| **Identity and scope anchors** | Carry authorised student, Study Plan, curriculum, topic (when scoped), and mission identity (when applicable) |
| **Evidence timestamp and source** | Emit when the observation handoff occurred and from which Version 1.0 source class |

## 2.2 Application owns

| Responsibility | Meaning |
|---|---|
| **Structural validation** | Accept or reject based on contract shape — never educational worth |
| **Evidence creation** | Produce Educational Evidence consistently from accepted contracts |
| **Provenance preservation** | Keep observed vs declared tags intact into Evidence memory |

## 2.3 What owns nothing here

| Actor | Owns in this capability |
|---|---|
| **Educational Intelligence** | **Nothing** — no judgement, no recommendation, no readiness from this contract |
| **Twin Update** | **Nothing** — no interpretation, no successor Twin authorship at the contract boundary |

### Ownership invariants

1. **Presentation gathers — it does not educate.** Collection ends at contract emission.  
2. **Application validates structure — it does not educate.** Pass/fail is structural legality, not learning worth.  
3. **Application creates Evidence — it does not interpret.** Evidence remains observational.  
4. **Educational Intelligence owns nothing here.** Judgement applies later to Twin state.  
5. **Twin Update owns nothing here.** Interpretation applies later to Evidence + prior Twin.  
6. **Calibration never writes this contract.** Birth priors remain a separate handoff.

Governing restatement:

> **Gather → validate → create Evidence. No owner at this boundary may invent learning or rewrite educational meaning.**

---

# 3. Required Fields

Version **1.0** of the Educational Evidence Contract is intentionally small.  
Required fields are the minimum anchors and observation spine without which Evidence creation is not meaningful.

Fields are classified as:

| Class | Meaning |
|---|---|
| **Required** | Must be present for a valid contract that may proceed to Evidence creation |
| **Optional** | May be absent without invalidating the contract |
| **Derived (forbidden in handoff)** | Must not be sent by Presentation as educational conclusions (Section 5) |

## 3.1 Required identity and scope anchors

These are not educational beliefs. Without them, Evidence is not attributable or syllabus-safe.

| Field | Meaning | Class |
|---|---|---|
| **authorised_student_identity** | The student whose study produced the observations; ownership already established | Required |
| **study_plan_identity** | The Study Plan scope under which the session occurred | Required |
| **curriculum_identity** | Canonical curriculum / exam (paper) identity for syllabus-scoped observations | Required |
| **evidence_timestamp** | When the observation handoff was emitted (product clock of the ended session / closing moment) | Required |
| **evidence_source** | Version 1.0 source class of the handoff (e.g. end-of-session study close) | Required |
| **contract_version** | Contract version identity — `1.0` for this milestone | Required |

## 3.2 Required contextual identities (when applicable)

| Field | Meaning | Class |
|---|---|---|
| **mission_identity** | Canonical mission identity when the ended session was mission-scoped | Required when applicable |
| **topic_identity** | Canonical curriculum topic identity when the session / mission was topic-scoped | Required when applicable |

### Applicability honesty

- When a session was mission-scoped, `mission_identity` must be present — silence is not a substitute.  
- When a session was topic-scoped, `topic_identity` must resolve to a **canonical curriculum identifier** (V1 or V2 via Curriculum authority) — never free-text syllabus invention.  
- When a session was not mission-scoped or not topic-scoped, those fields are omitted honestly — not filled with invented ids.

## 3.3 Required observed events

| Field | Meaning | Class |
|---|---|---|
| **observed_events** | Non-empty closed set of Version 1.0 educational observations arising from the ended session | Required |

### Version 1.0 observed-event vocabulary (closed)

Each item in `observed_events` is an **observation**, never a conclusion. At least one must be present.

| Observation token | Meaning |
|---|---|
| `mission_completed` | Mission reached a completed observation |
| `mission_abandoned` | Mission left incomplete / abandoned |
| `study_duration` | Study duration was recorded (system-observed and/or student-confirmed) |
| `topic_studied` | Syllabus-scoped topic engagement was recorded |
| `practice_completed` | Practice block / practice attempt completed was recorded |
| `practice_attempted` | Practice was attempted (lighter posture than completed, when that is what is known) |
| `session_ended_manual` | Student ended study manually |
| `session_ended_timeout` | Session ended by timeout / window |
| `system_timestamp` | System timing fact accompanying the session ending |

A single ending may lawfully carry multiple tokens (e.g. `mission_completed` + `study_duration` + `topic_studied`).

### Required-field honesty rule

Required means **structurally present**, not educationally dense. A sparse but honest `observed_events` set (e.g. abandoned mission + timestamps) is valid. Inventing completion, practice, or reflection to “fill” Required cargo is forbidden.

### Curriculum identity rule

All topic / section / syllabus references inside the contract use **canonical curriculum identifiers** only. Presentation must not promote free-text names into Required topic identity.

### Closed Required invariant

> **Version 1.0 Evidence creation accepts only this Required spine. Everything else is Optional, forbidden, or out of contract.**

---

# 4. Optional Fields

Optional fields enrich observational memory when present. Their omission is educationally acceptable.

| Field | Meaning | Class |
|---|---|---|
| **reflection** | Short student self-report about how the study felt (closed options preferred) | Optional |
| **declared_duration** | Student-confirmed / approximate duration when distinct from or confirming system observation | Optional |
| **practice_count** | Count of practice questions / attempts when known | Optional |
| **assessment_result** | Observed scored / judged outcome against syllabus scope when an assessment completed in the session | Optional |
| **session_notes** | Free-text student remark, if Presentation collects any | Optional |

## 4.1 Why omission is educationally acceptable

| Optional field | Why absence is honest |
|---|---|
| **reflection** | Skip is first-class in Product Flow 4.8.3. Missing reflection means no self-report Evidence — not failure, not invented voice. |
| **declared_duration** | System-observed duration may already sit in `observed_events`. Student confirmation is enrichment, not a Required autobiography. |
| **practice_count** | Practice may be known only as attempted/completed posture. Exact count is useful when available; unknown count must remain unknown. |
| **assessment_result** | Many Version 1.0 sessions have no scored assessment. Absence is normal, not incomplete Evidence. |
| **session_notes** | Notes are non-authoritative. Absence never blocks Evidence creation. |

## 4.2 Optional field rules

1. **Omitted Optional fields must not be invented** during validation or Evidence creation.  
2. **`reflection` is always declared provenance** when present (self-report).  
3. **`session_notes` are non-authoritative.** They must never become syllabus identities, mastery, readiness, practice counts, or assessment results. Evidence creation **ignores notes for observational authority**.  
4. **`assessment_result` remains observational** — a recorded outcome, never pass probability or mastery.  
5. **Optional enrichment must not redefine Required meaning** — e.g. presence of reflection must not rewrite `mission_abandoned` into completion theatre.

### Optional invariant

> **Sparse Optional cargo is lawful. Completeness theatre is not.**

---

# 5. Derived Fields

Presentation does **not** send educational conclusions. Application does **not** derive educational meaning at the contract boundary.

## 5.1 Values Presentation must never send as contract authority

| Forbidden derived / judgement field | Why forbidden |
|---|---|
| **Readiness** | Preparedness aggregation — Educational Intelligence / Readiness |
| **Mastery** | Knowledge belief — Twin Update Strategies |
| **Confidence** (as validated judgement) | Confidence domain truth — not session-end cargo |
| **Pass probability** | Forecast — Predictions / later calibrated forecasting |
| **Knowledge state** | Twin Knowledge domain — not an observation handoff |
| **Difficulty interpretation** | Educational interpretation — not observed fact |
| **Learning quality** | Ranking / diagnosis — not Evidence |

## 5.2 What Application derives at this boundary

| Application may | Application must not |
|---|---|
| Confirm structural acceptance / rejection | Derive readiness, mastery, confidence, or pass probability |
| Preserve provenance tags into Evidence | “Upgrade” declared reflection into assessed truth |
| Create observational Educational Evidence | Author Twin beliefs or Intelligence judgements |
| Attach contract_version / acceptance metadata | Invent missing Optional observations |

### Derivation firewall

```
Presentation sends observations (+ optional declarations)
        ↓
Application validates structure only
        ↓
Educational Evidence (observational)
        ↓
(Later) Twin Update derives educational meaning
        ↓
(Later) Successor Twin → Educational Intelligence judges
```

Governing restatement:

> **Application derives nothing educationally at the contract boundary. Twin Update derives meaning later. Educational Intelligence judges later still.**

---

# 6. Observed versus Declared

Provenance is immutable cargo of every event that crosses this contract.

## 6.1 Provenance classes (Version 1.0)

| Provenance | Meaning |
|---|---|
| **observed** | System-recorded educational fact (within measurement limits) |
| **declared** | Student self-report recorded as such |

## 6.2 Frozen examples

| Cargo | Provenance | Rule |
|---|---|---|
| **Mission completed** | **Observed** | Completion marked / reached as session ending is system-observed educational fact |
| **Mission abandoned** | **Observed** | Abandon / unfinished ending is observed, not a motivation diagnosis |
| **Reflection** | **Declared** | Always self-report; never promoted to assessed understanding |
| **Practice questions** | **Observed** *or* **Declared** | System-recorded practice activity is observed; student-only practice posture without system record is declared |
| **Study duration** | **Observed** and/or **Declared** | System timing is observed; student approximate confirmation is declared when sent as `declared_duration` |
| **Assessment result** | **Observed** | Scored outcome recorded as observation — not forecast |
| **Session notes** | **Declared** (non-authoritative) | Never syllabus authority |

## 6.3 Provenance immutability

1. **Evidence provenance is immutable** once the contract is accepted — Application must not rebrand declared as observed to densify warrant.  
2. **Twin Update may interpret differently by provenance** later — it must not rewrite the historical provenance tag.  
3. **Declared and observed may co-exist** for the same session (e.g. observed duration + declared duration confirmation) — they remain distinct.  
4. **Calibration self-declared priors are not this provenance system** — birth autobiography remains outside Educational Evidence.

Governing restatement:

> **Observed stays observed. Declared stays declared. Provenance is frozen at the handoff.**

---

# 7. Validation

Application validates **structure only**.

It answers:

> “Is this observation artefact well-formed, attributable, and syllabus-legal?”

It never answers:

> “Did the student learn / are they ready / will they pass / was the reflection true?”

## 7.1 Structural validation rules

| Check | Pass condition |
|---|---|
| **Required presence** | All Required anchors present; `observed_events` non-empty with recognised Version 1.0 tokens |
| **Identity integrity** | `authorised_student_identity` and `study_plan_identity` are authorised and consistent with each other for the handoff |
| **Curriculum identity** | `curriculum_identity` resolves to a loadable canonical curriculum (V1 or V2) |
| **Topic identity (when present)** | `topic_identity` is canonical for that curriculum via Curriculum authority — no free-text nodes |
| **Mission identity (when applicable)** | `mission_identity` present and consistent with the Study Plan / session scope when the session was mission-scoped |
| **Timestamp validity** | `evidence_timestamp` is a well-formed, plausible emission time for the ended session (not future-impossible under product clock rules; not absent) |
| **Structural consistency** | Observed-event tokens do not contradict each other structurally (e.g. both `mission_completed` and `mission_abandoned` for the same mission identity without an explicit correction event model — Version 1.0 rejects that contradiction) |
| **Provenance presence** | Every event / Optional declaration carries observed or declared provenance as required by Section 6 |
| **Version** | `contract_version` is a known contract version the Application accepts |
| **Closed set** | No forbidden judgement fields offered as contract authority (Section 5) |

## 7.2 What validation must never do

| Forbidden validation behaviour | Why |
|---|---|
| Score whether the student “really studied” | Educational / psychological judgement |
| Infer mastery from mission completed | Observation ≠ mastery |
| Infer readiness from duration or practice count | Readiness Aggregation only |
| Judge reflection accuracy | Self-report warrant remains thin |
| Auto-invent missing Optional reflection / practice | Honesty — no invented observations |
| Coerce unknown topic free-text into nearest canonical id | Curriculum-unsafe |
| Author Twin beliefs or Intelligence outputs during validation | Wrong owners |
| Treat `session_notes` as Required observations | Non-authoritative |

### Validation outcome (conceptual)

| Outcome | Meaning |
|---|---|
| **Accepted** | Structurally valid; Application may create Educational Evidence |
| **Rejected** | Structurally unlawful; Evidence must not be created from this artefact |
| **Requires clarification** | Structural conflict returnable to Presentation — do not invent a reconciled fiction |

Governing restatement:

> **Validate identity of fields — never the educational truth of the student.**

---

# 8. Failure Behaviour

Product-level contract behaviour only — no routes, UI, or persistence mechanics.

**Binding rule:**

> **No invented observations. Sparse honesty beats complete fiction.**

## 8.1 Missing required field

```
Missing required field
        ↓
Reject
```

| Condition | Contract behaviour |
|---|---|
| Required anchor absent (student, plan, curriculum, timestamp, source, version) | **Rejected** — do not create Evidence |
| `observed_events` empty or missing | **Rejected** — do not invent a default observation |
| Mission-scoped session missing `mission_identity` | **Rejected** |
| Topic-scoped session missing canonical `topic_identity` | **Rejected** |

**Forbidden:** Filling missing Required cargo with Mid defaults, average sessions, or LLM guesses.

## 8.2 Unknown curriculum identity

```
Unknown curriculum identity
        ↓
Reject
```

| Condition | Contract behaviour |
|---|---|
| `curriculum_identity` does not resolve | **Rejected** |
| `topic_identity` not canonical for the curriculum | **Rejected** — no silent nearest-id coercion |

## 8.3 Missing optional reflection

```
Missing optional reflection
        ↓
Accept
```

| Condition | Contract behaviour |
|---|---|
| Reflection omitted / skipped | **Accepted** when Required spine is valid — create Evidence without reflection |
| Other Optional fields omitted | **Accepted** — omit from Evidence; do not fabricate |

Aligned with Product Flow 4.8.3: skip reflection still leaves observed activity.

## 8.4 Impossible educational claim

```
Impossible educational claim
        ↓
Store only if structurally valid and marked declared
```

| Condition | Contract behaviour |
|---|---|
| Student declares something educationally implausible as self-report (e.g. extreme duration claim) but shape is lawful | **Accepted as declared** if structural rules pass — Application does **not** rewrite educational truth; Twin Update may later interpret warrant cautiously |
| Claim smuggled as observed when only declared | **Rejected** or corrected only by returning to Presentation — Application must not silently re-tag provenance |
| Judgement payload (mastery / readiness / pass %) offered as observation | **Rejected** — out of closed set |
| Notes promoted as topic ids or assessment results | **Rejected** if Presentation tried to promote notes into authoritative fields |

**Forbidden:** Inventing compensating observed events to “balance” a strange declaration. Educating the student via rejection copy that implies mastery bands.

## 8.5 Other structural failures

| Condition | Contract behaviour |
|---|---|
| Structural contradiction in `observed_events` | **Rejected** or **Requires clarification** — never merge into hybrid fiction |
| Invalid timestamp | **Rejected** |
| Unrecognised observation token | **Rejected** — do not coerce into nearest token |
| Presentation draft emitted without session ending | **Rejected** — drafts are not contracts |

## 8.6 Failure summary

| Failure | Contract posture |
|---|---|
| Missing Required field | Reject |
| Unknown curriculum / non-canonical topic | Reject |
| Missing optional reflection | Accept |
| Impossible educational claim (structurally valid declared) | Accept as declared only |
| Judgement fields / invented observations | Reject |
| Provenance rebrand attempted | Reject |

Governing restatement:

> **Validity means structurally honest and provenance-true — not educationally flattering or complete as a learning story.**

---

# 9. Versioning

## 9.1 Freeze Version 1.0

This document freezes **Educational Evidence Contract Version 1.0**.

Version 1.0 is intentionally small: identity anchors, timestamps, source, and a closed observational event vocabulary plus a thin Optional set.

## 9.2 Additive future versions

Future versions may add observation classes **without breaking Version 1.0**:

| Future addition | How it evolves |
|---|---|
| **Assessment evidence** (richer) | Additive Optional / event tokens under a new contract version; Version 1.0 assessment_result meaning unchanged |
| **AI observations** | New provenance class + event tokens — explicit AI provenance; never silent Twin authorship |
| **Tutor observations** | New actor-scoped observation class — additive |
| **Behaviour observations** | Broader behavioural observation catalogue — still observational; Strategies still interpret |

## 9.3 Evolution rules

1. **Additive by default.** Future versions may add Optional fields or new recognised observation tokens under a new `contract_version`. Version 1.0 consumers ignore unknown optional fields.  
2. **Never silently redefine Version 1.0 meaning.** Changing what `mission_completed` *means* (e.g. into mastery) is a breaking change — forbidden without a major contract version and architecture revision.  
3. **Required fields cannot be removed** from the Version 1.0 closed set without a breaking version.  
4. **New Required fields** belong only in a new major version; Version 1.0 emitters must remain valid without them.  
5. **Provenance law is permanent.** Future versions must not collapse declared into observed.  
6. **Application accepts a version window.** Unknown newer optional fields are ignored; unknown required meaning changes are rejected — never partially guessed.  
7. **Educational Intelligence and Twin Update contracts remain separate.** Growing this handoff must not move judgement into Presentation cargo.

### Compatibility posture

| Change type | Breaking for Version 1.0? | Example |
|---|---|---|
| Add optional AI observation token in `1.1` | No (additive), if ignored by V1.0 Evidence creation | New Optional / event class |
| Add tutor observation provenance | No if V1.0 provenance meanings unchanged | Additive |
| Remove `observed_events` | Yes | Breaks observational spine |
| Treat reflection as mastery | Yes | Educational meaning change — forbidden |
| Make reflection Required for all sessions | Yes for emitters that lawfully omit | Breaking major version |

Governing restatement:

> **Contract evolves additively. Version 1.0 remains lawful forever as history. Never version away observation-only honesty.**

---

# 10. Relationship with Future Capabilities

## 10.1 Downstream pipeline

The Educational Evidence Contract is the Presentation → Application freeze. Downstream capabilities continue after Application accepts and creates Evidence:

```
Presentation
      ↓
Educational Evidence Contract   ← this document (ends Application-boundary handoff)
      ↓
Application
      ↓
Educational Evidence
      ↓
Evidence Repository
      ↓
Twin Update
      ↓
Successor Twin
```

| Stage | Role relative to this contract |
|---|---|
| **Presentation** | Gathers observations; emits contract |
| **Educational Evidence Contract** | Immutable handoff shape (this document) |
| **Application** | Validates structure; creates Educational Evidence |
| **Educational Evidence** | Permanent observational memory |
| **Evidence Repository** | Future durable store of Evidence — not defined here |
| **Twin Update** | Future interpretation of Evidence into successor Twin — owns nothing at this boundary |
| **Successor Twin** | Immutable Twin snapshot after Strategy authorship |
| **Educational Intelligence** | Later consumes Twin — never this contract |

## 10.2 Where the contract ends

**The contract ends at the Application boundary.**

It does **not** continue into:

- Evidence Repository schemas;  
- Twin Update Strategy inputs as belief algebra;  
- Educational Intelligence Experience composition;  
- TwinRepository persistence operations.

Those remain separate contracts / capabilities. Consistency with Student Calibration Contract (Presentation → Application birth handoff) and Twin Repository Contract (Application ↔ Persistence for Twins) is intentional: each freezes one boundary without absorbing the next.

## 10.3 Consistency with companion contracts

| Companion | Shared discipline |
|---|---|
| **Student Calibration Contract (3.6.4)** | Closed Version 1.0 field set; structural validation only; Presentation gathers; Application validates; no Intelligence ownership; additive versioning |
| **Twin Repository Contract (3.7.3)** | Immutable educational artefacts; honest failure; no educational reasoning inside the boundary adapter |
| **Educational Experience Contract (3.2)** | Product-facing experience remains downstream of Twin / Intelligence — not fed by this Evidence handoff directly |
| **Educational Intelligence architecture** | Evidence → Strategies → Twin → Intelligence chain preserved; this contract only freezes the first Presentation → Application step for session observations |

Governing restatement:

> **The Educational Evidence Contract freezes observations at the Application door. Everything after Evidence creation is a different capability.**

---

# 11. Contract Compliance Summary

| Invariant | Status under this contract |
|---|---|
| Closed Version 1.0 observation handoff | Defined — Required / Optional / forbidden derived |
| Presentation gathers; Application validates; Evidence created consistently | Affirmed |
| Educational Intelligence owns nothing here | Affirmed |
| Twin Update owns nothing here | Affirmed |
| Structural validation only | Affirmed — no educational truth scoring |
| Observed vs declared provenance immutable | Affirmed |
| Canonical curriculum identifiers only | Affirmed |
| Failure: reject Required gaps; accept missing reflection; no invented observations | Affirmed |
| Additive versioning without breaking 1.0 | Affirmed |
| Pipeline ends at Application boundary for this artefact | Affirmed |
| Consistent with Calibration / TwinRepository / Intelligence contract discipline | Affirmed |
| No Flask / ORM / persistence / Twin Update / Intelligence reasoning | Honoured — contract only |

---

# 12. STOP

This document defines the **Educational Evidence Contract** only.

It does **not** authorise:

- Implementation  
- Flask routes or forms  
- ORM models, schemas, or migrations  
- Evidence Repository / EvidenceRecorder implementation  
- Twin Update Strategy algorithms  
- Educational Intelligence reasoning or redesign  
- Persistence technology choices  
- UI / reflection wizard design  

**STOP.**

---

# References

| Artefact | Role |
|---|---|
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Governing ADR; Educational Evidence Principle |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Platform educational chain; Evidence → Twin → Intelligence |
| [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md) | Application Layer boundary law |
| [`CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md`](CAPABILITY_4_8_1_EDUCATIONAL_EVIDENCE_ARCHITECTURE.md) | Evidence architecture law |
| [`CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md`](CAPABILITY_4_8_2_EDUCATIONAL_EVIDENCE_ANALYSIS.md) | Observation vs interpretation; declared vs observed |
| [`CAPABILITY_4_8_3_EDUCATIONAL_EVIDENCE_PRODUCT_FLOW.md`](../product/CAPABILITY_4_8_3_EDUCATIONAL_EVIDENCE_PRODUCT_FLOW.md) | End-of-session journey that emits this contract |
| [`CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md`](CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md) | Companion Presentation → Application contract (birth) |
| [`CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md`](CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md) | Companion Application ↔ Persistence contract (Twins) |
| [`CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md`](CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md) | Downstream experience contract — Intelligence-facing |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Canonical Twin domain law |
| [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md) | Epic 0 Evidence catalogue companion |
| [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md) | Shared educational vocabulary |
