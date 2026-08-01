# EA-003 — Mission Blueprint

**Programme:** Educational Excellence Programme EA-003 — Mission Architecture & Authoring Blueprint  
**Status:** Binding — permanent Mission specification for Version 1 onward  
**Effective:** 2026-08-01  
**Authority:** EA-001 PASS · EA-002 PASS · EV-001 · `PRODUCT_BLUEPRINT.md` · Educational Constitution · Study Sensei Philosophy · Guidance Over Content  
**Nature:** Architecture and authoring law — not educational content, not application code  
**Parents:** `EA001_MISSION_PHILOSOPHY.md` · `EA001_QUALITY_GATES.md` (Gate MG) · `EA002_EDUCATIONAL_AUTHORING_FRAMEWORK.md` (AF-MS)  

---

## 1. Purpose of this Blueprint

Define exactly how every Kwalitec Daily Mission must be conceived, authored, reviewed, and certified **before** educational content creation begins.

When EA-003 is complete, different educational authors must independently produce Missions that students immediately recognise as coming from the same Study Sensei.

> **The Mission is the primary educational artefact in Kwalitec. Everything else supports the Mission.**

This Blueprint does **not** rewrite CS1, generate Missions, or modify application code.

---

## 2. What a Mission is (architectural definition)

A **Mission** is the authorised primary educational focus for a day (or study period). It is a **tutor brief**, not a syllabus checkbox.

| The Mission answers | The Mission does not answer |
|---------------------|----------------------------|
| What deserves attention **now** | The full Session teaching sequence (that is Session/Episodes) |
| **Why** it deserves attention now | Opaque ranking theatre alone |
| What **benefit** the student should expect | Mastery claims from one pass |
| **How** study will be executed (Session intent pointer) | CMP textbook prose |
| What **success** looks like today | Platform / engineering meta |

### Architectural position

```text
Syllabus + CMP + Twin evidence
            ↓
     ┌──────────────┐
     │   MISSION    │  ← primary educational artefact (tutor brief)
     └──────┬───────┘
            ↓
   Session Overview + Learning Episodes
            ↓
   Reflection → Summary → Tomorrow Preview
            ↓
   History / Decision Journal / Revision signals
```

- **Mission ≠ Session.** Mission decides the day; Session executes it.  
- **Mission ≠ Recommendation.** A Recommendation may inform composition; the Mission is the certified student-facing brief.  
- **Mission ≠ Syllabus heading.** Correct topic selection with a weak brief is still a fail (EA-001).  

Under Learning Mode (Version 1 default), topic selection follows Current Learning Topic in official syllabus order (Constitution Article VI). Authoring quality is independent of that selection rule.

---

## 3. Governing design rules

| ID | Rule |
|----|------|
| MB-01 | Every Mission has a complete educational blueprint (all §4 fields populated or lawfully deferred). |
| MB-02 | **Tutor Intent is mandatory.** No Mission may ship without an explicit tutor intent statement. |
| MB-03 | **Educational continuity is mandatory.** Bridge from prior learning and Tomorrow Bridge (or honest absence) are required. |
| MB-04 | Mission multiplies CMP value; it never replaces CMP content (EP-01, Guidance Over Content). |
| MB-05 | Mission PASS requires linked Session/Episodes PASS **or** honest unavailable state — never a beautiful brief over empty stages. |
| MB-06 | Lifecycle green ≠ educational PASS. Certification under EA-003 + Gate MG is required before student exposure. |
| MB-07 | Authors execute one Study Sensei voice (`EA002_TUTOR_VOICE_GUIDE.md`); personal brand dialects are forbidden. |
| MB-08 | Failed field resolution blocks publication — never degrade to placeholders. |

---

## 4. Permanent Mission specification

Every Mission authoring pack **must** define the following fields. Field IDs are stable for schema, review, and certification evidence.

### 4.1 Mission Purpose

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `mission_purpose` |
| **Definition** | One sentence stating why this Mission exists as today’s primary focus. |
| **Standard** | Educational purpose, not product purpose. Must name the skill or coverage step the day advances. |
| **Fail if** | Vague (“help the student study”); platform-centric; duplicates syllabus heading alone. |
| **Maps to** | EA-001 M4/M9 spirit; Foundation §4.5 |

**Example (illustrative pattern only):**  
> Today’s Mission exists to extend yesterday’s linear-model fluency into GLM structure so the candidate can choose a link with intent.

---

### 4.2 Educational Intent

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `educational_intent` |
| **Definition** | What learning change this Mission is designed to produce in the candidate. |
| **Standard** | States the intended cognitive move (e.g. connect, distinguish, apply, justify). Distinct from Session stage list. |
| **Fail if** | “Cover the chapter”; “complete the Mission”; engagement-only intent. |
| **Principle** | EP-03 Deliberate Study · EP-01 Educational Leverage |

---

### 4.3 Tutor Intent

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `tutor_intent` |
| **Definition** | What the Study Sensei is trying to achieve as a tutor in this brief — the coaching move. |
| **Standard** | **Mandatory.** Written as an IFoA tutor’s private note to self: “Today I will… so that the candidate…” Must be specific enough that two different Missions cannot share identical Tutor Intent. |
| **Fail if** | Missing; generic (“guide the student”); interchangeable across topics. |
| **Principle** | EP-09 Tutor Voice — this field is the non-negotiable proof that a human tutor designed the day. |

**Example (illustrative pattern only):**  
> Today I will force the candidate to name the exponential-family → linear predictor → link chain aloud before reading deep, so they enter CMP with a mental map instead of page-turning.

---

### 4.4 Learning Objective

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `learning_objective` |
| **Definition** | One student-facing learning objective with an actionable verb. |
| **Standard** | ≤160 characters preferred (V1 E2 spirit). **Must not** equal the syllabus heading string. Assessable. |
| **Fail if** | Title = objective = narrative; passive “understand topic X”. |
| **Maps to** | EA-001 M2 |

---

### 4.5 CMP Reading Scope

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `cmp_reading_scope` |
| **Definition** | Exact locus and bounds of today’s CMP (or authorised materials) work. |
| **Standard** | Named chapter/section/example + stop condition. Never “the material” alone. Must state what *not* to read today when a larger chapter exists. |
| **Fail if** | Whole-chapter dump instruction; no open point; CMP paraphrase pasted into Mission body. |
| **Maps to** | EA-001 M8 · EP-04 Guided Reading |

---

### 4.6 Syllabus Coverage

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `syllabus_coverage` |
| **Definition** | Official syllabus node(s) this Mission advances, and the coverage claim for today. |
| **Standard** | Topic code + accurate human title. State whether first-pass Learning Mode, revision of prior node, or lawful exception. Coverage claim must be honest (progress, not mastery). |
| **Fail if** | Contaminant / metadata nodes; inventing coverage beyond today’s scope; silent mode mismatch. |
| **Maps to** | EA-001 M1 · Constitution Article VI |

---

### 4.7 Prerequisite Knowledge

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `prerequisite_knowledge` |
| **Definition** | What the candidate is assumed to already hold for this Mission to be educationally safe. |
| **Standard** | Name prior topics/skills. Cold start: state enrolment/chapter prerequisites explicitly. If prerequisites are incomplete, Tutor Intent must address remediation or HOLD. |
| **Fail if** | Assumed blank; contradicts Twin/History without disclosure. |
| **Principle** | EP-02 · EP-06 |

---

### 4.8 Concept Focus

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `concept_focus` |
| **Definition** | The single idea or skill that defines the day. |
| **Standard** | Concrete chain or concept name (e.g. “exponential family → linear predictor → link”), not “Today’s topic”. |
| **Fail if** | Placeholder; multi-chapter grab-bag; syllabus restatement without conceptual centre. |
| **Maps to** | EA-001 M5 |

---

### 4.9 Common Misconceptions

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `common_misconceptions` |
| **Definition** | 1–3 misconceptions the Tutor expects at this topic — used to shape focus prompts and Reflection. |
| **Standard** | Educationally accurate; examinable where relevant. Each misconception should imply a corrective study move. |
| **Fail if** | Empty when topic is known-risk; inventing false misconceptions; textbook dumps of error lists without tutor use. |
| **Principle** | EP-03 · EP-08 |

---

### 4.10 Study Strategy

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `study_strategy` |
| **Definition** | How the candidate should study today — method, not content. |
| **Standard** | Names the Session intent structure (e.g. Guided Reading → Worked Example → Practice → Reflection) and the leverage move (extract, compare, justify, rework). Must match real Episode design. |
| **Fail if** | “Read and understand”; advertises stages with no authored episodes; engagement bait. |
| **Maps to** | EA-001 M7 · EP-01 · EP-05 |

---

### 4.11 Reflection Goal

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `reflection_goal` |
| **Definition** | What Reflection should accomplish after today’s study — the residual-uncertainty harvest. |
| **Standard** | Topic-specific. Names the gap or clarity the student should articulate. Feeds Tomorrow Bridge and Revision Signals. |
| **Fail if** | Generic “what is clearer…” with “Today’s topic”; missing when Session includes Reflection. |
| **Principle** | EP-07 Reflection |

---

### 4.12 Success Criteria

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `success_criteria` |
| **Definition** | What the student should be able to explain or do after the Session — countable, assessable. |
| **Standard** | Prefer closed-book demonstrations. 1–3 criteria for the Mission brief; Session Episodes may expand with 2–4 per stage (Gate LE). Language: Study Progress, never mastery theatre. |
| **Fail if** | Unassessable; readiness ±N% as sole outcome; completion checkbox as success. |
| **Maps to** | EA-001 M6 · EP-03 · EP-06 |

---

### 4.13 Tomorrow Bridge

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `tomorrow_bridge` |
| **Definition** | Continuity toward the next lawful focus — skill bridge, not unlock theatre. |
| **Standard** | When next focus known: topic title + educational continuity line agreeing with Gate TP and next Home assignment. When unknown: honest absence (one sentence). Must not assign heavy new teaching after Reflection. |
| **Fail if** | Contaminant next node; contradicts Mission handoff; fabricated preview. |
| **Maps to** | EA-001 M10 · Gate TP · EP-02 |

---

### 4.14 Estimated Cognitive Load

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `estimated_cognitive_load` |
| **Definition** | Tutor judgement of mental demand for a typical prepared candidate on this day. |
| **Standard** | Use scale: **Light · Moderate · Heavy · Very Heavy**. Justify in one line (new concept density, calculation load, abstraction). Must be consistent with Study Strategy and time. |
| **Fail if** | Missing; “Heavy” with empty reading shell; Light while dumping a full chapter. |
| **Principle** | EP-03 duration honesty |

---

### 4.15 Estimated Study Time

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `estimated_study_time` |
| **Definition** | Honest total duration budget for the linked Session (including CMP reading + recall + reflection). |
| **Standard** | Minutes range (e.g. 45–60). Must match Episode depth (Gate LE-10 / SS-06). Prefer candidate-realistic over aspirational. |
| **Fail if** | Unbounded; 15 minutes for chapter-scale work; time box that contradicts CMP Reading Scope. |

---

### 4.16 Revision Signals

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `revision_signals` |
| **Definition** | What evidence from today should later trigger or shape revision. |
| **Standard** | Name expected soft/hard signals: weak success-check, named misconception, Reflection residual, exam-weight cue. May be empty only if Tutor Intent documents “no special revision flag beyond normal decay.” |
| **Fail if** | Silent on high-risk exam topics; invents revision without evidence path; claims “Nothing to revise” logic in authoring. |
| **Principle** | EP-06 · Gate RV (downstream) |

---

### 4.17 Dependencies

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `dependencies` |
| **Definition** | Upstream and co-requisite artefacts this Mission cannot publish without. |
| **Standard** | Must list: prior Mission/topic (or cold-start); linked Session ID; Episode IDs; CMP edition/version; curriculum package version. Optional: Twin evidence keys consumed. |
| **Fail if** | Orphan Mission; Session intent without Episode IDs at certification; package version omitted. |
| **Maps to** | EA-002 joint publication rule |

---

### 4.18 Certification Evidence

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `certification_evidence` |
| **Definition** | Pointers and outcomes proving this Mission passed review. |
| **Standard** | Record Educational Review, Tutor Review, Gate MG checklist, scoring rubric result, reviewer IDs, dates, PASS/FAIL/HOLD. See `EA003_MISSION_CERTIFICATION.md`. |
| **Fail if** | Empty at Publication Approval; automation-only PASS for Tutor Voice in Version 1. |

---

### 4.19 Publication Metadata

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `publication_metadata` |
| **Definition** | Identity and lifecycle metadata for publication and maintenance. |
| **Standard** | Minimum: `mission_id`, subject ID, package version, syllabus topic code, mode (Learning/Revision), author ID, created/updated timestamps, certification status, publication status, retirement status, CMP edition pin. |
| **Fail if** | Unversioned publish; missing subject/package; retired Mission still marked student-reachable. |

---

## 5. Field completeness rule

| Status | Meaning |
|--------|---------|
| **Complete** | All §4 fields populated to standard (Revision Signals may use lawful empty with Tutor Intent note). |
| **Incomplete** | Any mandatory field missing, placeholder, or interchangeable boilerplate. |
| **HOLD-deferred** | Named field deferred only with Board HOLD, expiry, and student-visible honesty where exposure would otherwise mislead. |

**Publication rule:** Incomplete Missions do not reach students. HOLD-deferred fields do not silently count as Complete.

---

## 6. Relationship to EA-001 Mission elements (M1–M12)

EA-003 **extends** EA-001; it does not weaken it.

| EA-001 | EA-003 field(s) |
|--------|-----------------|
| M1 Topic identity | Syllabus Coverage · Publication Metadata |
| M2 Distinct objective | Learning Objective |
| M3 Bridge from prior | Prerequisite Knowledge · Mission Purpose (bridge clause) · see Continuity pack in Schema |
| M4 Why now | Educational Intent · Mission Purpose · Explainability (Schema) |
| M5 Concept focus | Concept Focus |
| M6 Success criterion | Success Criteria |
| M7 Session intent | Study Strategy |
| M8 Material locus | CMP Reading Scope |
| M9 Expected benefit | Educational Intent · Success Criteria |
| M10 Handoff / Tomorrow | Tomorrow Bridge |
| M11 Explainability | Educational Intent + why-now evidence (Schema `why_now`) |
| M12 Voice | Tutor Intent + Tutor Voice Guide compliance |

**New mandatory architecture fields beyond M1–M12:** Tutor Intent · Common Misconceptions · Reflection Goal · Estimated Cognitive Load · Estimated Study Time · Revision Signals · Dependencies · Certification Evidence · Publication Metadata.

---

## 7. Continuity architecture (built into every Mission)

Every Mission authoring pack must include a **Continuity Bundle**:

1. **Yesterday / prior bridge** — explicit arc from prior Mission/topic or lawful cold-start.  
2. **Today centre** — Concept Focus + Learning Objective + Success Criteria.  
3. **Tomorrow Bridge** — next lawful focus or honest absence.  
4. **Truth alignment** — why-now text unique enough that two Missions cannot share identical rationale; agrees with Decision Journal / Home / Tomorrow Preview when published.

Continuity is not optional colour. Absence of continuity is an automatic quality-gate fail (`EA003_MISSION_CERTIFICATION.md`).

---

## 8. Reject classes (architectural)

Missions that are any of the following are **architecturally unfit** and must not enter certification as Complete:

| Reject class | Definition |
|--------------|------------|
| Generic | Could apply to any topic without edit |
| Template driven | Mechanical fragment concatenation; stamp fields only |
| CMP paraphrases | Mission body restates CMP paragraphs |
| Syllabus restatements | Title = objective = narrative = heading |
| Disconnected | No prior bridge, no tomorrow, no Session link |
| Educationally purposeless | No Educational Intent / Tutor Intent |
| Lacking continuity | Continuity Bundle incomplete |
| Lacking Tutor Intent | `tutor_intent` missing or interchangeable |

Full measurable criteria: quality gates + scoring rubric companion documents.

---

## 9. Hierarchy and authority

| Rank | Authority |
|------|-----------|
| Superior | Educational Constitution · Vision 2030 · Product Blueprint |
| 3a | EA-001 teaching constitution (principles, Mission Philosophy, Gate MG) |
| 3b | EA-002 production framework (AF-MS, Voice, Style, Certification, Publication) |
| **3c** | **EA-003 Mission Blueprint / Schema / Authoring / Certification / Rubric** |

Where EA-003 specialises Mission architecture, it is binding. Where conflict appears with EA-001 gates, **stricter student-protection rule wins**; amend via Board — do not silently weaken Gate MG.

---

## 10. Closing rule

> A Mission without a complete educational blueprint is not a Mission — it is a label.

Labels do not reach students under EA-003.

Different authors, one Sensei: complete fields, Tutor Intent mandatory, continuity built in, certification before content creation begins.
