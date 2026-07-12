# Capability 3.6.4 — Student Calibration Contract

**Status:** Contract only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.6.4 Student Calibration Contract (immutable Presentation → Application boundary for Twin-birth declarations)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Upstream Calibration architecture:** [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md)  
**Upstream educational analysis:** [`CAPABILITY_3_6_2_STUDENT_CALIBRATION_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_3_6_2_STUDENT_CALIBRATION_EDUCATIONAL_ANALYSIS.md)  
**Upstream product flow:** [`CAPABILITY_3_6_3_STUDENT_CALIBRATION_PRODUCT_FLOW.md`](../product/CAPABILITY_3_6_3_STUDENT_CALIBRATION_PRODUCT_FLOW.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Scope:** Closed, immutable Application Contract for Initial Student Calibration — **no Flask, routes, persistence, UI design, Twin redesign, educational algorithms, or implementation**

---

## Document purpose

Capabilities 3.6.1–3.6.3 established:

- **Architecture** — Calibration captures self-declared history into Twin *priors*; it never reasons.  
- **Educational analysis** — self-report establishes priors; Evidence establishes truth; closed minimum information set.  
- **Product flow** — Calibration begins after Study Plan creation; stages collect history; Review confirms; Twin birth precedes the first Educational Intelligence recommendation.

This milestone defines the **immutable Student Calibration Contract**.

It answers:

> What exact declaration artefact does Presentation hand to the Application Layer so Calibration Builder can birth the first Digital Twin — and nothing else?

It is the sole Application input to Twin birth from Initial Student Calibration.

**Governing principle (binding):**

> **The contract carries what the student declared. It never becomes educational judgement.**

**Architectural restatement:**

> **Presentation collects. Application validates structure. Calibration Builder consumes the contract and emits Twin priors. Educational Intelligence never edits the contract. Twin Persistence never authors it. Learning Evidence never writes it.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Student Calibration Contract** | Immutable closed declaration artefact (this document) — Version 1.0 |
| **Calibration Builder** | Future Application Twin-birth constructor that *consumes* this contract (named conceptually; not implemented here) |
| **Initial Student Calibration** | Capability family 3.6 — history → priors at Twin birth |
| **Confidence calibration** | Separable / deferred Confidence domain — **not** this contract |

**Non-goals of this document**

- Implementation types, dataclasses, JSON schemas, ORM, or API payloads  
- Flask routes, forms, templates, wizard wireframes, or UI design  
- Twin Persistence / TwinRepository design  
- Redesign of the Digital Twin, Evidence, Readiness, Decision, Recommendation, or Mission  
- Educational algorithms, mastery inference, readiness scoring, or recommendation selection  
- Product copy decks beyond contract field meaning  

---

# 1. Purpose

## 1.1 Why the contract exists

Without a closed Presentation → Application contract:

- wizard stages and Application constructors invent incompatible field sets;  
- free-text or ad-hoc “extra” questions quietly become Twin truth;  
- validation drifts into educational judgement (“does this student look ready?”);  
- Twin birth receives partial, conflicting, or platform-private declarations;  
- Educational Intelligence, Persistence, or Evidence are tempted to *fill in* what the form did not say.

The **Student Calibration Contract** exists so that:

1. **Presentation and Application share one closed declaration shape** for Version 1.0.  
2. **Twin birth has exactly one authorised self-declaration input** — this contract — for Initial Student Calibration.  
3. **Structural validation has a fixed target** — recognised ids, sittings, objectives — never educational scoring.  
4. **Downstream owners cannot edit autobiography** — Intelligence judges later; Persistence stores Twin snapshots; Evidence observes study.  
5. **Immutability and provenance are mandatory cargo** — once confirmed, the declaration snapshot does not morph into mastery.

It is the lawful answer to:

> “What did this student declare, in closed form, immediately before Twin birth?”

It is **not** the answer to:

> “What should the student study next?” / “How ready are they?” / “What have they mastered?”

## 1.2 Relationship to Product Flow

Capability 3.6.3 defines the student journey:

```
Study Plan successfully created
        ↓
Calibration stages (history → attempts → objective → sections → sitting → Review)
        ↓
Student confirms declarations
        ↓
Student Calibration Contract   ← this document (Presentation → Application handoff)
        ↓
Calibration Builder → Twin birth priors
        ↓
First dashboard → first Educational Intelligence recommendation
```

Product Flow owns *when* and *how calmly* declarations are collected.  
This Contract owns *what* must be present at the handoff after Review confirm.

| Product Flow concern | Contract concern |
|---|---|
| Entry after Study Plan creation | Contract requires plan-scoped curriculum / exam identity |
| Progressive stages and beginner shortcuts | Contract still closes the same Version 1.0 field set (empty-history path fills emptiness explicitly) |
| Review confirm / correct | Contract is emitted only after student confirmation of the closed set |
| Skip / abandon / conflict behaviour | Contract failure postures (Section 6) — product-level, not UI mechanics |
| First recommendation after Twin birth | Out of contract scope — Educational Intelligence consumes the birth Twin, not this contract |

Governing restatement:

> **Product Flow collects and confirms. The Contract freezes what was confirmed. Calibration Builder reads only the freeze.**

## 1.3 Relationship to Twin birth

Twin birth for Initial Student Calibration has a single declaration input:

```
Student Calibration Contract (immutable, Version 1.0)
              ↓
     Calibration Builder (Application)
              ↓
   Calibrated birth Twin (priors + Identity / Goals anchors)
              ↓
   Twin Persistence (future) stores the Twin snapshot
```

Rules:

1. **This contract is the sole self-declared educational-history input to Twin birth** on the Calibration path.  
2. **Calibration Builder may also require non-declaration Application facts already established by plan creation** (authorised student identity, curriculum scope) — those appear *inside* the closed contract as Required anchors, not as parallel side channels.  
3. **Twin birth does not read Presentation session scraps, wizard draft state, or Evidence.** Incomplete drafts are not Twin birth inputs.  
4. **Educational Intelligence begins after birth**, reading the Twin (via TwinProvider), not rewriting this contract.  
5. **Absence of a valid contract means no calibrated returning Twin** — cold-start / empty-history honesty, never Mid fabrication from silence.

Governing restatement:

> **No valid Student Calibration Contract ⇒ no calibrated Twin birth from declarations. Never invent the missing autobiography.**

---

# 2. Ownership

Ownership is absolute. The contract is a handoff artefact, not a shared editable worksheet.

| Actor | Owns | Must never |
|---|---|---|
| **Presentation** | **Collect** closed declarations from the student after Study Plan creation; present Review; emit the contract only after student confirmation | Perform educational math; invent mastery / readiness; write Twin beliefs; author Evidence; mutate the contract after emit |
| **Application (validation)** | **Validate structure** of the emitted contract against recognised curriculum ids, sittings, and objectives; accept, reject, or degrade honestly | Infer mastery, readiness, predicted marks, or recommendations; “fix” educational coherence by inventing fields |
| **Calibration Builder** | **Consume** a structurally valid contract; map declarations into Twin priors with provenance; emit birth Twin (+ calibration metadata) | Edit student autobiography; call EvidenceRecorder to seed fake events; emit readiness / Decision / Recommendation |
| **Educational Intelligence** | Consume the *birth Twin* later for judgement (Readiness / Decision / Recommendation / Mission) | **Edit** the Student Calibration Contract; treat the contract as a live questionnaire to re-score |
| **Twin Persistence** | Store the calibrated *Twin snapshot* (future) | **Author** the Student Calibration Contract; invent declarations to fill storage gaps |
| **Learning Evidence** | Observe study / assessment events after product use | **Write** Calibration declarations; convert declarations into Evidence rows |

### Ownership invariants

1. **Presentation collects — it does not calibrate.** Collection and confirm end at contract emission.  
2. **Application validates structure — it does not educate.** Pass/fail is structural legality, not educational worth.  
3. **Calibration Builder consumes — it does not reopen the form.** Mapping is prior construction from the closed set only.  
4. **Educational Intelligence never edits the contract.** Judgement applies to Twin state under thin warrant, not to rewriting what the student said.  
5. **Twin Persistence never authors declarations.** Persistence may retain contract lineage with the birth Twin; it does not invent history fields.  
6. **Evidence never writes the contract.** Declared history ≠ observed Evidence.

Governing restatement:

> **Collect → validate → consume → birth. No owner downstream may rewrite the student's declaration artefact.**

---

# 3. Closed Inputs

Version **1.0** of the Student Calibration Contract is a **closed** field set.  
If the student did not declare it here, Calibration must not invent it.

Fields are classified as:

| Class | Meaning |
|---|---|
| **Required** | Must be present for a valid contract that may proceed to Twin birth |
| **Optional** | May be absent without invalidating the contract when posture allows |
| **Derived** | Must not be student-authored as free invention; computed only from closed Required/Optional declarations (or fixed contract constants) |

## 3.1 Required anchors (identity and scope)

These are not educational beliefs. Without them, Twin birth is not meaningful.

| Field | Meaning | Class |
|---|---|---|
| **authorised_student_identity** | The student whose Twin is being born; ownership already established before Calibration | Required |
| **curriculum_exam_scope** | Canonical curriculum / exam (paper) identity the Twin and declarations are scoped to | Required |
| **contract_version** | Contract version identity — `1.0` for this milestone | Required |
| **declaration_confirmation** | Explicit student confirmation that the closed declarations are what they intend to submit (Review confirm) | Required |

## 3.2 Required educational-history and objective declarations

Aligned with Capability 3.6.1 §4.2 and 3.6.2 §3.2. All are self-declared.

| Field | Meaning | Class |
|---|---|---|
| **previously_studied** | Coarse declaration: first-time / starting from scratch, **or** previously studied this paper / syllabus | Required |
| **core_reading_completed** | Declared Core Reading completion posture (none / whole paper / section-scoped where syllabus supports it) | Required |
| **previous_attempts** | Declared prior sitting attempts: none, or count and/or sitting labels; pass/fail only if explicitly declared as history fact | Required |
| **study_objective** | Current objective posture from the recognised Version 1.0 objective set (Section 4.2) | Required |
| **intended_sitting** | Target exam sitting / date anchor for this journey (may confirm a sitting already collected at Study Plan creation) | Required |
| **beginner_or_history_posture** | Explicit empty-history / starting-from-scratch confirmation **when** `previously_studied` asserts first-time; otherwise returning/history-present posture consistent with declarations | Required |

### Required-field honesty rule

For a true beginner path, Required history fields are still present — they hold **explicit empty / none / first-time values**, not omitted silence that later becomes Mid theatre.

## 3.3 Optional declarations

| Field | Meaning | Class |
|---|---|---|
| **declared_completed_sections** | Canonical section ids (V2) or V1-safe topic groupings via Curriculum authority that the student marks as already covered | Optional |
| **declared_study_capacity** | Hours / availability already collected by Study Plan, carried structurally if present — Goals capacity only | Optional |
| **optional_notes** | Free-text student remark, if Presentation collects any | Optional |

### Optional field rules

1. **`declared_completed_sections`** may be absent or empty when `previously_studied` / beginner posture is empty-history. It becomes expected depth when the student declared prior coverage and chooses to mark sections — still Optional, never mastery.  
2. **`declared_study_capacity`** is not required for educational-history honesty. If present, it must not become Behaviour adherence or burnout judgement.  
3. **`optional_notes` are non-authoritative.** They must **never** become syllabus identities, completed-section ids, mastery, readiness, attempt history, or prior markers. Calibration Builder **ignores notes for Twin prior construction**. Notes exist only if Presentation needs a calm remark channel; they are not Twin truth.

## 3.4 Derived fields (contract metadata, not student invention)

| Field | Meaning | Class |
|---|---|---|
| **declared_posture** | Coarse posture derived only from closed declarations: first-time \| returning \| revision-framed \| repeat-attempt-framed — **not** a readiness band | Derived |
| **warrant_posture** | Always `thin` / `self_declared` for all history priors in Version 1.0 | Derived (constant for V1.0 history fields) |
| **source** | Always `self_declared` / Initial Student Calibration | Derived (constant) |
| **emitted_at** | Conceptual emission time of the confirmed contract (product clock) | Derived |

Derived posture must follow declarations; Application must not “upgrade” posture into Mid readiness.

## 3.5 Forbidden inputs (must be rejected if offered as contract authority)

| Forbidden | Why |
|---|---|
| Mastery percentages / topic mastery ratings | Educational belief — not declaration |
| Readiness %, preparedness bands, “how ready” as readiness | Educational Intelligence judgement |
| Predicted marks / pass probability | Predictions — not history |
| Confidence ratings as Calibration history | Separable Confidence domain |
| Fabricated Learning Evidence seed events | Evidence sovereignty |
| LLM-inferred syllabus completion without explicit closed-field confirmation | Opaque inference |
| Legacy `TopicProgress` / heuristic composites as birth authority | Dual-truth debt |
| Free-text section names treated as canonical curriculum ids | Curriculum-unsafe |
| Diagnostic scores inside this contract | Diagnostics are Evidence paths |

### Closed-set invariant

> **Version 1.0 Calibration Twin birth accepts only this field set. Everything else is out of contract.**

---

# 4. Validation

Validation is **structural only**.

It answers:

> “Is this declaration artefact well-formed and syllabus-legal?”

It never answers:

> “Is this student prepared / mastered / likely to pass?”

## 4.1 Structural validation rules

| Check | Pass condition |
|---|---|
| **Required presence** | All Required fields present (empty-history values allowed where they are explicit empties) |
| **Recognised curriculum scope** | `curriculum_exam_scope` resolves to a loadable canonical curriculum identity (V1 or V2) |
| **Recognised section ids** | Every id in `declared_completed_sections` is canonical for that curriculum via Curriculum authority — no free-text nodes |
| **Recognised sitting** | `intended_sitting` is a recognised sitting label / date form the product accepts for this exam scope |
| **Recognised objective** | `study_objective` is one of the Version 1.0 recognised objectives (Section 4.2) |
| **Attempt shape** | `previous_attempts` uses allowed shapes (none / count / recognised sitting labels / optional declared outcome as history fact only) |
| **Core Reading shape** | `core_reading_completed` uses allowed shapes (none / whole paper / recognised section-scoped ids only) |
| **Confirmation** | `declaration_confirmation` is true — unconfirmed drafts are not valid contracts |
| **Version** | `contract_version` is a known contract version the Application accepts |

## 4.2 Recognised Version 1.0 study objectives

Closed recognised set (product labels may vary; meaning must not):

| Objective token | Meaning |
|---|---|
| `first_sit` | First learning / first sit for this scope |
| `revision` | Revision after declared coverage / Core Reading |
| `finish_remaining` | Finish remaining sections |
| `resit` | Re-sit / another attempt |

Unrecognised objective tokens fail structural validation.

## 4.3 What validation must never do

| Forbidden validation behaviour | Why |
|---|---|
| Score “how believable” the history is | Educational / psychological judgement |
| Infer mastery from Core Reading or sections | Prior ≠ mastery |
| Infer readiness from objective or attempts | Readiness Aggregation only |
| Auto-reconcile conflicts into Mid beliefs | Conflicts are failure / clarify posture (Section 6) |
| Invent missing section ids or sittings | Closed honesty |
| Treat `optional_notes` as syllabus completion | Non-authoritative |
| Author Evidence or Twin beliefs during validation | Wrong owners |

### Validation outcome (conceptual)

| Outcome | Meaning |
|---|---|
| **Accepted** | Structurally valid; Calibration Builder may consume |
| **Rejected** | Structurally unlawful; Twin birth from this artefact must not proceed |
| **Requires clarification** | Structural conflict or incomplete confirm — return to Presentation / Review; do not birth |

Governing restatement:

> **Validate identity of fields — never the educational worth of the student.**

---

# 5. Output

## 5.1 What Calibration Builder receives

Calibration Builder receives **exactly one** artefact:

| Output to Builder | Meaning |
|---|---|
| **Student Calibration Contract (Version 1.0)** | The immutable, structurally accepted, student-confirmed closed declaration set defined in Section 3 |

It does **not** receive:

- Presentation draft / in-progress wizard state  
- Educational Experience Contract components  
- Learning Evidence batches  
- Readiness / Decision / Recommendation / Mission artefacts  
- Twin Persistence load results as a substitute for missing declarations  

### Builder consumption law

```
Valid Student Calibration Contract
        ↓
Calibration Builder maps → Twin priors + Identity / Goals anchors
        ↓
Calibrated birth Twin (+ calibration metadata)
```

Mapping law remains Capability 3.6.1: priors only; thin warrant; no mastery / readiness / Evidence authorship. This contract does not redefine Twin shape — it only freezes declaration inputs.

## 5.2 Immutability

Once Presentation emits the contract after Review confirm, and Application accepts it:

1. **The contract snapshot is immutable** for that Twin-birth event.  
2. **Presentation must not silently patch fields** after emit to “improve” Twin birth.  
3. **Calibration Builder must not rewrite declarations** while mapping — map what was declared; leave unknowns empty.  
4. **Educational Intelligence must not edit the contract** when later Evidence contradicts priors — Evidence updates Twin beliefs; autobiography lineage remains what was declared.  
5. **History correction** (if product later allows) is a **new** explicit Calibration event producing a **new** contract version/instance — not mutation of the original freeze.

Governing restatement:

> **Confirmed declarations freeze. Correction is a new event, not an in-place edit.**

## 5.3 Provenance

Provenance is mandatory cargo of the contract and of every prior mapped from it.

| Provenance element | Value / rule |
|---|---|
| **source** | `self_declared` (Initial Student Calibration) |
| **warrant** | `thin` for all history priors in Version 1.0 |
| **contract_version** | `1.0` (or later additive version identity) |
| **confirmation** | Student-confirmed at emission |
| **non-Evidence** | Explicit: this artefact is not Learning Evidence |

Downstream Twin Persistence (future) must preserve that calibrated priors originated from this contract lineage. Stripping provenance or rebranding priors as Evidence-backed mastery is a contract violation of Calibration law (3.6.1), even though Persistence is not the author of this artefact.

Governing restatement:

> **Every field that becomes a Twin prior remains traceable to this self-declared contract — never to pretended observation.**

---

# 6. Failure Behaviour

Product-level contract behaviour only — no routes, UI, or persistence mechanics.

**Binding rule:**

> **When the contract cannot be validly completed, stay honest and empty — never invent a confident student.**

## 6.1 Missing fields

| Condition | Contract behaviour |
|---|---|
| Required field absent or silent (not an explicit empty) | **Rejected** or **Requires clarification** — do not Twin-birth |
| Optional field absent | Allowed when posture permits (e.g. no section list on beginner path) |
| Derived field cannot be computed because Required inputs conflict | **Requires clarification** — do not invent posture |

**Forbidden:** Filling missing Required history with Mid defaults, average students, or LLM guesses.

## 6.2 Invalid values

| Condition | Contract behaviour |
|---|---|
| Unrecognised section id, sitting, or objective | **Rejected** (or clarify) — do not coerce into nearest id |
| Free-text syllabus treated as section completion | **Rejected** |
| Mastery / readiness / predicted-mark payloads smuggled in | **Rejected** — out of closed set |
| Notes containing purported section lists used as ids | Ignore notes for priors; still **Rejected** if Presentation tried to promote notes into section fields without canonical ids |

**Forbidden:** Silent coercion of invalid ids into Twin truth.

## 6.3 Skipped calibration

| Condition | Contract behaviour |
|---|---|
| Student explicitly skips and confirms starting from scratch | Emit a **valid empty-history contract** (Required fields present with explicit first-time / none values) — lawful Twin birth with empty history priors |
| Student skips without confirming empty-history posture | **No calibrated returning contract** — no Twin birth from declarations; cold-start / TwinAbsent honesty as architecture allows |

**Forbidden:** Interpreting skip silence as Mid returning student.

## 6.4 Cancelled calibration

| Condition | Contract behaviour |
|---|---|
| Student cancels before Review confirm | **No contract emission** — drafts are not contracts |
| Twin birth must not proceed from cancelled flow | Study Plan may remain created; Calibration incomplete |

**Forbidden:** Auto-emitting a contract from last partial page. Shame copy is a Presentation concern; contract law is simply: no confirm ⇒ no contract.

## 6.5 Partial completion

| Condition | Contract behaviour |
|---|---|
| Stages started; Review not confirmed | **No valid contract** — partial answers are not Twin birth inputs |
| Conflicting declarations unresolved | **Requires clarification** — prefer Review reconcile; else degrade to thinner/empty honest posture only if student confirms that posture; never average into mastery |
| Curriculum scope missing / unresolvable | **Rejected** — cannot validate sections or birth a scoped Twin |

**Forbidden:** Half-written Twin priors from incomplete forms. Auto-confirming guessed remaining answers.

## 6.6 Failure summary

| Failure | Contract posture |
|---|---|
| Missing Required fields | Reject / clarify — no birth |
| Invalid recognised values | Reject / clarify — no coercion |
| Skip with beginner confirm | Valid empty-history contract |
| Skip without beginner confirm | No declaration contract |
| Cancelled | No emission |
| Partial / conflict unresolved | No birth until clarify or confirmed conservative empty |

Governing restatement:

> **Validity means structurally honest and student-confirmed — not educationally flattering or complete as biography.**

---

# 7. Versioning

The contract must evolve without breaking consumers that already understand Version 1.0.

## 7.1 Evolution rules

1. **Additive by default.** Future versions may add **Optional** fields or new recognised tokens under a new `contract_version` identity. Version 1.0 consumers ignore unknown optional fields.  
2. **Never silently redefine Version 1.0 meaning.** Changing what `core_reading_completed` or `study_objective` *means* educationally is a breaking change — requires a new major contract version and architecture revision.  
3. **Required fields cannot be removed** from the Version 1.0 closed set without a breaking version and migration story.  
4. **New Required fields** belong only in a new major version; Version 1.0 emitters must remain valid without them.  
5. **Derived posture tokens** may grow additively only if Version 1.0 tokens remain interpretable; do not rename first-time/returning meanings in place.  
6. **`optional_notes` must remain non-authoritative** across versions unless an explicit architecture revision promotes a new closed structured field (never promote free text into syllabus ids quietly).  
7. **Calibration Builder accepts a version window.** Unknown newer optional fields are ignored; unknown required meaning changes are rejected — never partially guessed.  
8. **Provenance always carries `contract_version`.** Twin lineage must record which contract version birthed priors.

## 7.2 Compatibility posture

| Change type | Breaking for Version 1.0? | Example |
|---|---|---|
| Add optional structured field (e.g. declared tuition provider) | No (additive), if ignored by V1.0 Builder | New Optional field in `1.1` |
| Add recognised objective token | No if old tokens unchanged; document additive set | New objective in `1.1` |
| Remove `previous_attempts` | Yes | Breaks closed minimum set |
| Treat notes as completed sections | Yes | Violates non-authoritative law |
| Redefine `revision` as High readiness | Yes | Educational meaning change — forbidden |
| Make `declared_completed_sections` Required for all students | Yes for emitters that lawfully omit on beginner path | Breaking major version |

Governing restatement:

> **Version additively. Never version away the prior/truth distinction or the closed honesty of Version 1.0.**

---

# 8. Contract Compliance Summary

| Invariant | Status under this contract |
|---|---|
| Closed Version 1.0 declaration set | Defined — Required / Optional / Derived |
| Presentation collects; Application validates; Builder consumes | Affirmed |
| Educational Intelligence never edits | Affirmed |
| Twin Persistence never authors | Affirmed |
| Evidence never writes | Affirmed |
| Structural validation only | Affirmed — no educational algorithms |
| Sole Application input to Calibration Twin birth | Affirmed |
| Immutability + self_declared provenance | Affirmed |
| Failure stays honest (skip / cancel / partial) | Affirmed |
| Additive versioning without breaking 1.0 | Affirmed |
| No Flask / UI / persistence / Twin redesign | Honoured — contract only |

---

# 9. STOP

This document defines the **Student Calibration Contract** only.

It does **not** authorise:

- Implementation  
- Flask routes or forms  
- UI / wizard design  
- Database tables or migrations  
- Twin Persistence implementation  
- Twin redesign  
- Evidence seeding  
- Educational algorithms or Intelligence changes  

**STOP.**
