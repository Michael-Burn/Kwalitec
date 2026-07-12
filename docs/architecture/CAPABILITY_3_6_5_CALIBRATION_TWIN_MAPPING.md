# Capability 3.6.5 — Student Calibration → Digital Twin Mapping

**Status:** Mapping only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.6.5 Calibration → Twin Mapping (structural translation of the immutable Student Calibration Contract into the Version 1.0 birth Twin)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Upstream Calibration architecture:** [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md)  
**Upstream educational analysis:** [`CAPABILITY_3_6_2_STUDENT_CALIBRATION_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_3_6_2_STUDENT_CALIBRATION_EDUCATIONAL_ANALYSIS.md)  
**Upstream product flow:** [`CAPABILITY_3_6_3_STUDENT_CALIBRATION_PRODUCT_FLOW.md`](../product/CAPABILITY_3_6_3_STUDENT_CALIBRATION_PRODUCT_FLOW.md)  
**Upstream contract:** [`CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md`](CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Scope:** Exact structural field mapping from Student Calibration Contract Version 1.0 into the Version 1.0 Digital Twin — **no Flask, persistence, UI, Twin redesign, educational algorithms, or implementation**

---

## Document purpose

Capabilities 3.6.1–3.6.4 established:

- **Architecture** — Calibration captures self-declared history into Twin *priors*; it never reasons.  
- **Educational analysis** — self-report establishes priors; Evidence establishes truth.  
- **Product flow** — declarations are collected and confirmed before Twin birth.  
- **Contract** — a closed, immutable declaration artefact is the sole Application input to Calibration Twin birth.

This milestone defines the **Calibration → Twin Mapping**.

It answers:

> Exactly how does every Student Calibration Contract field land in the Version 1.0 Digital Twin — and which Twin fields must remain empty?

**Governing principle (binding):**

> **Self-report establishes priors. Evidence establishes truth.**

**Architectural restatement:**

> **Mapping places declared facts into Twin structure. It never interprets those facts educationally. It never invents belief, warrant density, or judgement.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Student Calibration Contract** | Immutable closed declaration artefact (Capability 3.6.4) |
| **Calibration Builder** | Future Application consumer that applies this mapping (conceptual; not implemented here) |
| **Calibrated birth Twin** | Version 1.0 Digital Twin snapshot after lawful mapping — priors + anchors; empty where mapping forbids fill |
| **Prior** | Structural self-declared marker with thin warrant — not assessed educational belief |
| **Confidence calibration** | Separable / deferred Confidence domain — **not** this mapping |

**Non-goals of this document**

- Implementation types, dataclasses, JSON schemas, ORM, or API payloads  
- Flask routes, forms, templates, wizard wireframes, or UI design  
- Twin Persistence / TwinRepository design  
- Redesign of the Digital Twin, Evidence, Twin Update Strategies, Readiness, Decision, Recommendation, or Mission  
- Educational algorithms, mastery inference, readiness scoring, recommendation selection, or predictions  
- Changing Contract Version 1.0 field meanings  

---

# 1. Purpose

## 1.1 Why mapping exists

Without an exact Contract → Twin mapping:

- Calibration Builder invents incompatible Twin shapes from the same contract;  
- declaration fields quietly become mastery, readiness, or predicted marks;  
- optional notes or derived posture tokens leak into belief domains;  
- Twin domains that must stay empty get filled “for completeness”;  
- Persistence and Educational Intelligence cannot tell prior from Evidence-backed truth.

The mapping exists so that:

1. **Every Contract field has one lawful destination** (or an explicit *no Twin state* rule).  
2. **Twin birth is deterministic from a valid Contract** — same declarations → same structural Twin posture.  
3. **Educational interpretation is forbidden at birth** — placement only.  
4. **Unknowns remain empty on purpose** — silence is honesty, not incompleteness to fix.  
5. **Provenance travels with every prior** — self-declared lineage cannot be stripped or rebranded as observation.

It is the lawful answer to:

> “Where does each confirmed declaration live inside the Version 1.0 Twin?”

It is **not** the answer to:

> “What does Educational Intelligence believe?” / “What should the student study next?” / “How ready are they?”

## 1.2 Relationship between Contract and Twin birth

```
Student Calibration Contract (immutable, Version 1.0)
              ↓
     This mapping (structural placement rules)
              ↓
     Calibration Builder (Application — future)
              ↓
   Calibrated birth Twin (priors + Identity / Goals anchors)
              ↓
   Twin Persistence (future) stores the Twin snapshot
              ↓
   TwinProvider → Educational Intelligence (consumes Twin, not Contract)
```

| Artefact | Role at birth |
|---|---|
| **Contract** | Frozen *what the student declared* |
| **Mapping** | Closed rules for *where declarations sit in Twin structure* |
| **Birth Twin** | Authoritative learner-state snapshot after placement — still thin warrant |
| **Evidence** | Not present at Calibration birth; later establishes truth |

Rules:

1. **The Contract is the sole self-declared educational-history input** to this mapping.  
2. **Mapping does not reopen or edit the Contract.**  
3. **Mapping does not redesign Twin domains** — it fills only Version 1.0 slots that Calibration may lawfully initialise.  
4. **No valid Contract ⇒ no calibrated Twin birth from declarations.**  
5. **Educational Intelligence reads the birth Twin**, never rewrites autobiography into the Contract.

Governing restatement:

> **Contract freezes autobiography. Mapping places it. Twin holds priors. Evidence later earns truth.**

---

# 2. Mapping philosophy

## 2.1 Structural mapping only

Mapping is **structural placement**:

- copy recognised identity / goal anchors into Identity and Goals;  
- attach history prior markers into Knowledge and Performance *as priors*;  
- attach calibration metadata / provenance to the birth snapshot lineage;  
- leave every other Twin belief slot empty.

Mapping is **not**:

- educational interpretation of what declarations “mean for preparedness”;  
- inference of missing syllabus coverage, weak topics, or retention;  
- scoring, ranking, banding, or forecasting;  
- averaging, coercing, or Mid-defaulting unknown fields.

## 2.2 Never educational interpretation

| Allowed | Forbidden |
|---|---|
| “Student declared Core Reading complete for section X” → Knowledge prior marker for X | “Therefore section X is mastered / ready / skippable” |
| “Student declared `resit` objective” → Goals posture token | “Therefore High urgency readiness band” |
| “Student declared two prior sittings” → Performance attempt-history prior | “Therefore expected mark / pass probability” |

## 2.3 Never inference

Mapping must not invent:

- section ids the student did not declare;  
- mastery beliefs for undeclared or declared nodes;  
- Memory decay / retention from “I studied before”;  
- Behaviour adherence from declared study capacity;  
- Predictions from attempts or objectives;  
- Mid beliefs where the Contract holds explicit empties.

## 2.4 Never scoring

Mapping must not produce:

- mastery percentages;  
- readiness % or preparedness bands;  
- confidence scores;  
- coverage weights as educational truth;  
- recommendation scores or next-action ranks.

Governing restatement:

> **Place what was declared. Do not explain the student. Do not complete the Twin by guessing.**

---

# 3. Field-by-field mapping

For every Student Calibration Contract Version 1.0 field, this section defines:

- **Destination Twin component**  
- **Reason**  
- **Provenance**  
- **Establishes** — one of: Identity · Goals · Knowledge prior · Performance prior · Behaviour · Memory · Metadata · **no Twin state**

Version 1.0 Twin components referenced here are the aggregate domains under Twin law / domain model: **Identity**, **Goals**, **Knowledge**, **Memory**, **Behaviour**, **Performance**, **Predictions**, plus **calibration metadata / lineage** carried with the birth snapshot (not a belief domain).

---

## 3.1 Required anchors

### `authorised_student_identity`

| | |
|---|---|
| **Destination** | **Identity** — `student_id` (stable learner reference) |
| **Reason** | Twin birth is meaningless without the authorised owner; Identity scopes every domain. |
| **Provenance** | Application-authorised identity already established before Calibration; not Learning Evidence. Carries contract lineage (`contract_version`, birth event) as metadata, not as educational warrant. |
| **Establishes** | **Identity** |

### `curriculum_exam_scope`

| | |
|---|---|
| **Destination** | **Identity** — `curriculum_id` and `current_exam` (canonical curriculum / paper scope) |
| **Reason** | All history priors and Goals are syllabus-scoped; Curriculum remains syllabus truth. |
| **Provenance** | Scope from plan creation / recognised curriculum identity; tagged with Calibration birth lineage. Not Evidence. |
| **Establishes** | **Identity** |

### `contract_version`

| | |
|---|---|
| **Destination** | **Calibration metadata / lineage** on the birth Twin (not a belief domain) |
| **Reason** | Twin lineage must record which Contract version birthed priors so future consumers ignore or migrate correctly. |
| **Provenance** | Derived contract constant / identity (`1.0`); mandatory cargo of birth metadata. |
| **Establishes** | **Metadata** |

### `declaration_confirmation`

| | |
|---|---|
| **Destination** | **Calibration metadata / lineage** — confirmation flag + confirmed emission posture |
| **Reason** | Proves Review confirm occurred; drafts must never birth. Not an educational belief. |
| **Provenance** | Student-confirmed at Contract emission; retained as birth metadata. |
| **Establishes** | **Metadata** |

---

## 3.2 Required educational-history and objective declarations

### `previously_studied`

| | |
|---|---|
| **Destination** | **Knowledge** — coarse paper/syllabus-scope **exposure prior marker** (self-declared). Does **not** write `mastery_belief`. |
| **Reason** | Returning vs first-time exposure must be structurally visible so Educational Intelligence is not forced into beginner falsehood — without claiming mastery. |
| **Provenance** | `source = self_declared`, `warrant = thin`, `contract_version` retained. Explicitly non-Evidence. |
| **Establishes** | **Knowledge prior** |

When value is explicit first-time / none: Knowledge exposure prior is an **explicit empty-history posture**, not omitted silence.

### `core_reading_completed`

| | |
|---|---|
| **Destination** | **Knowledge** — declared Core Reading **coverage / exposure prior** (whole paper and/or canonical section-scoped ids). Does **not** write mastery, retention, or Confidence. |
| **Reason** | Declared Core Reading is history of engagement, not assessed ability. |
| **Provenance** | `self_declared` / thin warrant; section ids remain Curriculum-canonical. |
| **Establishes** | **Knowledge prior** |

### `previous_attempts`

| | |
|---|---|
| **Destination** | **Performance** — **attempt-history prior markers** (none / count / recognised sitting labels / declared outcome *only if* stated as history fact). Alternatively held as Calibration metadata bag that Performance strategies may later read as prior — never as Assessment Performance warrant. |
| **Reason** | Prior sittings are declared history of exam-condition exposure; they are not mock scores or pass probability. |
| **Provenance** | `self_declared` / thin warrant; never Evidence ids; never invented marks. |
| **Establishes** | **Performance prior** |

### `study_objective`

| | |
|---|---|
| **Destination** | **Goals** — structural objective posture / recognised token (`first_sit` \| `revision` \| `finish_remaining` \| `resit`) |
| **Reason** | Objective is what the student is trying to achieve now; it is not readiness or Decision selection. |
| **Provenance** | Self-declared; thin; retained as Goals anchor from Contract. |
| **Establishes** | **Goals** |

### `intended_sitting`

| | |
|---|---|
| **Destination** | **Identity** (`target_sitting`) and/or **Goals** (`target_completion_date` / sitting anchor as declared) |
| **Reason** | Sitting is a scope and goal deadline anchor, not a completion forecast or risk score. |
| **Provenance** | Self-declared (or plan-confirmed) sitting fact; not Evidence. |
| **Establishes** | **Identity** and **Goals** |

### `beginner_or_history_posture`

| | |
|---|---|
| **Destination** | **Calibration metadata** (explicit empty-history vs history-present posture) **and** corresponding empty or non-empty history prior slots in Knowledge / Performance |
| **Reason** | Distinguishes lawful beginner Twin birth from returning history without creating a readiness band. |
| **Provenance** | Derived from / consistent with closed declarations; `self_declared` lineage; thin warrant. |
| **Establishes** | **Metadata** (and constrains Knowledge / Performance prior emptiness — does not establish Behaviour or Memory) |

---

## 3.3 Optional declarations

### `declared_completed_sections`

| | |
|---|---|
| **Destination** | **Knowledge** — structural “declared complete” **prior markers** keyed by canonical section/topic ids (V2 sections or V1-safe groupings via Curriculum authority). Does **not** write mastery map, weighted coverage %, or Confidence. |
| **Reason** | Declared syllabus position without assessed belief. Absent/empty is lawful on beginner path. |
| **Provenance** | `self_declared` / thin; Curriculum-validated ids only. |
| **Establishes** | **Knowledge prior** |

### `declared_study_capacity`

| | |
|---|---|
| **Destination** | **Goals** — `planned_study_hours_per_week` (or equivalent capacity commitment) when present |
| **Reason** | Capacity is a goal/constraint commitment already collected by Study Plan — not Behaviour adherence or burnout judgement. |
| **Provenance** | Self-declared / plan-carried; not Evidence; must not upgrade Behaviour. |
| **Establishes** | **Goals** |

Absent capacity ⇒ Goals capacity slot remains empty — lawful.

### `optional_notes`

| | |
|---|---|
| **Destination** | **no Twin state** for educational domains. Notes must **not** map into Identity, Goals, Knowledge, Memory, Behaviour, Performance, or Predictions. |
| **Reason** | Free text is non-authoritative (Contract 3.6.4). Promoting notes would invent syllabus ids or beliefs. |
| **Provenance** | If Presentation retains notes outside Twin truth, they remain non-educational cargo — never prior warrant. |
| **Establishes** | **no Twin state** |

Calibration Builder **ignores notes for Twin prior construction**.

---

## 3.4 Derived Contract fields

### `declared_posture`

| | |
|---|---|
| **Destination** | **Calibration metadata** — coarse posture token (first-time \| returning \| revision-framed \| repeat-attempt-framed) |
| **Reason** | Structural honesty label derived only from closed declarations; not a readiness band. |
| **Provenance** | Derived from Contract Required/Optional fields; thin; self_declared lineage. |
| **Establishes** | **Metadata** |

### `warrant_posture`

| | |
|---|---|
| **Destination** | **Calibration metadata / provenance** attached to every history prior — always `thin` / `self_declared` for Version 1.0 history fields |
| **Reason** | Prevents downstream collapse of priors into Evidence-dense beliefs. |
| **Provenance** | Contract-derived constant for V1.0; mandatory on Knowledge and Performance priors. |
| **Establishes** | **Metadata** (governs warrant of Knowledge prior and Performance prior — does not create Behaviour or Memory) |

### `source`

| | |
|---|---|
| **Destination** | **Calibration metadata / provenance** — always `self_declared` / Initial Student Calibration |
| **Reason** | Distinguishes autobiography from Learning Evidence forever until supersession rules apply. |
| **Provenance** | Contract-derived constant. |
| **Establishes** | **Metadata** |

### `emitted_at`

| | |
|---|---|
| **Destination** | **Calibration metadata / lineage** — conceptual emission time of the confirmed Contract |
| **Reason** | Audit of when autobiography froze for this birth event. |
| **Provenance** | Product clock at emission; not Evidence timestamp theatre. |
| **Establishes** | **Metadata** |

---

## 3.5 Mapping summary table

| Contract field | Destination | Establishes |
|---|---|---|
| `authorised_student_identity` | Identity | Identity |
| `curriculum_exam_scope` | Identity | Identity |
| `contract_version` | Birth metadata / lineage | Metadata |
| `declaration_confirmation` | Birth metadata / lineage | Metadata |
| `previously_studied` | Knowledge prior marker | Knowledge prior |
| `core_reading_completed` | Knowledge prior marker | Knowledge prior |
| `previous_attempts` | Performance prior marker (or metadata bag for Performance) | Performance prior |
| `study_objective` | Goals | Goals |
| `intended_sitting` | Identity and/or Goals | Identity · Goals |
| `beginner_or_history_posture` | Birth metadata (+ empty/non-empty history priors) | Metadata |
| `declared_completed_sections` | Knowledge prior markers | Knowledge prior |
| `declared_study_capacity` | Goals (if present) | Goals |
| `optional_notes` | — | **no Twin state** |
| `declared_posture` | Birth metadata | Metadata |
| `warrant_posture` | Provenance on priors + metadata | Metadata |
| `source` | Provenance on priors + metadata | Metadata |
| `emitted_at` | Birth metadata / lineage | Metadata |

### Domains this mapping never establishes at birth

| Twin component | Established by Calibration mapping? |
|---|---|
| **Behaviour** | **No** — remains empty |
| **Memory** | **No** — remains empty |
| **Predictions** | **No** — remains empty |
| **Readiness / Planning / Motivation** (Twin law companions) | **No** — not authored by Calibration |
| **Mastery beliefs / Confidence** | **No** — forbidden |

Governing restatement:

> **Every Contract field maps exactly once: to Identity, Goals, Knowledge prior, Performance prior, Metadata — or explicitly to no Twin state.**

---

# 4. Unknown preservation

After lawful Calibration mapping, the following Version 1.0 Twin fields / domains must **intentionally remain empty** (or unset). Emptiness is correct, not a defect to fill.

## 4.1 Domains that stay empty

| Twin domain / companion | Must remain empty after Calibration | Why |
|---|---|---|
| **Memory** | Entire domain empty | Declared history ≠ retention schedule, decay, or strength |
| **Behaviour** | Entire domain empty | Declared capacity ≠ adherence, streaks, burnout, or session habits |
| **Predictions** | Entire domain empty | Attempts / objectives ≠ pass probability or forecast snapshots |
| **Readiness** (if represented as Twin companion state) | Empty / unset | Preparedness is Readiness Aggregation only |
| **Planning artefacts** | Not Twin birth authority | Plans are consequences of intelligence + constraints |
| **Motivation** | Empty / unset | Calibration does not author motivation theatre |

## 4.2 Belief slots that stay empty inside initialised domains

| Slot / belief | Must remain empty | Why |
|---|---|---|
| Knowledge `mastery_belief` (any topic/section) | Empty / unset | Prior markers ≠ mastery |
| Knowledge Confidence / felt-vs-measured Confidence | Empty | Separable Confidence domain; not Calibration |
| Knowledge Evidence references as if observed | Empty | No Learning Evidence authored |
| Performance marks, grade beliefs, accuracy trends | Empty | Attempt history prior ≠ measured Performance summary warrant |
| Performance Evidence / assessment ids fabricated from declarations | Empty | Evidence sovereignty |
| Goals `target_pass_probability` invented from objective/attempts | Empty unless separately declared as Goals ambition outside Calibration history (Version 1.0 Calibration does not map Contract fields into pass probability) | Predictions / ambition scoring forbidden here |
| Behaviour adherence derived from `declared_study_capacity` | Empty | Capacity is Goals only |
| Any Mid/High default where Contract holds explicit none / first-time | Forbidden fill | Explicit empty-history must stay empty |

## 4.3 Optional Contract absences

| Absent optional Contract field | Twin consequence |
|---|---|
| No `declared_completed_sections` | No section-level Knowledge prior markers — lawful |
| No `declared_study_capacity` | Goals capacity unset — lawful |
| `optional_notes` present or absent | No Twin educational state either way |

## 4.4 Unknown preservation invariant

> **If Calibration did not lawfully receive a declaration for a Twin belief, the Twin must leave that belief empty. Mapping never invents Mid density to look complete.**

---

# 5. Provenance

## 5.1 How self-declared provenance is attached

Every history prior placed by this mapping carries mandatory provenance cargo from the Contract:

| Provenance element | Attachment rule |
|---|---|
| **source** | `self_declared` (Initial Student Calibration) on every Knowledge prior and Performance prior |
| **warrant** | `thin` for all Version 1.0 history priors |
| **contract_version** | Retained on birth lineage (`1.0` or later additive identity) |
| **confirmation** | Birth metadata records student confirmation at emission |
| **non-Evidence** | Explicit: priors are not Learning Evidence and must not gain Evidence ids from Calibration |
| **field lineage** | Each prior remains traceable to the Contract field that produced it (e.g. Core Reading prior ← `core_reading_completed`) |

Identity and Goals anchors also retain Calibration birth lineage (scope and objective came from the confirmed Contract) without pretending those anchors are assessed beliefs.

### Attachment law

```
Contract field (confirmed)
        ↓
Structural Twin slot
        ↓
Provenance bag: source=self_declared, warrant=thin, contract_version, field lineage
```

Stripping provenance, or rebranding priors as Evidence-backed mastery at store or read time, is a Calibration law violation — even if Persistence is the later storage owner.

## 5.2 How later Evidence supersedes priors

Architectural expectation (no algorithms specified here):

1. **Birth** — Twin holds self-declared priors under thin warrant.  
2. **Observation** — Real study / assessment produces Learning Evidence.  
3. **Update** — Twin Update Pipeline / Twin Update Strategies evolve Knowledge, Memory, Behaviour, and Performance beliefs from Evidence.  
4. **Supersession for judgement** — Where Evidence-backed state conflicts with self-declared priors, **Evidence dominates educational judgement**.  
5. **Lineage retention** — Priors may remain visible as audit autobiography (“student declared Core Reading complete at birth”) without continuing to act as mastery or Assessment Performance.  
6. **No Contract mutation** — Contradicting Evidence updates Twin beliefs; it does not rewrite the immutable Contract freeze. History correction, if product allows later, is a **new** Calibration event / new contract instance.

### Supersession invariant

> **Self-report starts the Twin. Evidence earns the right to overwrite belief authority. Autobiography lineage is not deleted by truth — it is demoted as judgement warrant.**

Governing restatement:

> **Provenance keeps priors honest at birth. Evidence keeps beliefs honest thereafter.**

---

# 6. Educational safeguards

Mapping never creates the following — by structural prohibition, not by later policy patch.

## 6.1 Never creates mastery

| Why forbidden | Mapping consequence |
|---|---|
| Mastery is Evidence-weighted belief about what the student can *do now* | Knowledge receives **prior markers only**; `mastery_belief` stays empty |
| Declared Core Reading / sections answer engagement history, not ability | No coverage % → mastery collapse |

## 6.2 Never creates confidence

| Why forbidden | Mapping consequence |
|---|---|
| Confidence calibration is a separable / deferred domain | No Confidence ratings from Calibration history fields |
| Felt confidence ≠ declared syllabus history | `optional_notes` and objectives cannot become Confidence |

## 6.3 Never creates readiness

| Why forbidden | Mapping consequence |
|---|---|
| Preparedness belongs solely to Readiness Aggregation | No readiness %, bands, or “how ready” from objective / attempts / coverage |
| `declared_posture` is structural honesty, not Mid/High theatre | Posture stays metadata |

## 6.4 Never creates recommendations

| Why forbidden | Mapping consequence |
|---|---|
| Next-action selection belongs to Decision / Recommendation / Mission | Birth Twin contains no recommendation artefacts |
| Mapping ends at Twin structure | No “skip foundations” policy authored inside Calibration |

## 6.5 Never creates predictions

| Why forbidden | Mapping consequence |
|---|---|
| Forecasts belong to Predictions / later calibrated forecasting | Predictions domain stays empty |
| Prior attempts ≠ pass probability | Performance priors carry history facts only |

### Safeguard restatement

> **If a Twin write would answer “how mastered / confident / ready / what next / will they pass?”, it is outside this mapping.**

---

# 7. Future compatibility

This mapping is designed so later Persistence, Evidence, and Twin Update Strategies attach without Twin redesign.

## 7.1 Twin Persistence

| Persistence concern | Why no Twin redesign is required |
|---|---|
| Store birth Twin snapshot | Mapping already targets Version 1.0 Twin domains |
| Preserve provenance | Provenance is mandatory cargo of priors + metadata — Persistence must retain, not invent new belief shapes |
| Load via TwinProvider | Provider retrieves DigitalTwin \| TwinAbsent; calibrated birth is just a Twin snapshot with thin priors |
| E2-PE-01 debt | Persistence changes *where* the birth Twin lives, not *what* Calibration may write |

**Rule:** TwinRepository stores what mapping produced. It does not author declarations or fill empty Memory / Behaviour / Predictions to satisfy schema completeness.

## 7.2 Evidence

| Evidence concern | Why no Twin redesign is required |
|---|---|
| Evidence remains sovereign for belief evolution | Birth Twin already leaves belief slots empty for Evidence to fill |
| No fake Evidence seeding | Mapping forbids Evidence ids from declarations |
| Audit spine | Contract lineage + Evidence log remain distinct authorities |

**Rule:** EvidenceRecorder never writes the Contract; Calibration never writes Evidence. Twin structure already separates prior markers from Evidence-backed beliefs.

## 7.3 Twin Update Strategies

| Update Strategies concern | Why no Twin redesign is required |
|---|---|
| Strategies evolve Knowledge / Memory / Behaviour / Performance from Evidence | Empty domains and empty mastery slots are lawful Strategy inputs |
| Evidence supersedes priors | Thin `self_declared` warrant is already the signal Strategies / Intelligence must respect |
| No second write authority | Calibration mapping is birth-only; ongoing mutation remains Pipeline / Strategies |

**Rule:** Update Strategies do not need new Twin domains to understand Calibration — they need to honour provenance and leave autobiography lineage intact while updating beliefs.

## 7.4 Compatibility invariant

> **Version 1.0 Twin shape is sufficient. Calibration adds priors and metadata into existing domains. Persistence stores. Evidence densifies. Strategies update. No redesign of Twin aggregate boundaries is required for Calibration birth.**

---

# 8. Mapping Compliance Summary

| Invariant | Status under this mapping |
|---|---|
| Every Contract field has a destination or explicit no Twin state | Defined — Section 3 |
| Structural placement only — no interpretation / inference / scoring | Affirmed — Section 2 |
| Self-report → priors; Evidence → truth | Affirmed — Sections 1, 5 |
| Memory, Behaviour, Predictions intentionally empty | Affirmed — Section 4 |
| Provenance mandatory on history priors | Affirmed — Section 5 |
| No mastery / confidence / readiness / recommendations / predictions | Affirmed — Section 6 |
| Twin Persistence / Evidence / Update Strategies compatible without Twin redesign | Affirmed — Section 7 |
| No Flask / UI / persistence / algorithms / Twin redesign in this milestone | Honoured — mapping only |

---

# 9. STOP

This document defines the **Calibration → Digital Twin Mapping** only.

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
