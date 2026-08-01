# EA-004 — Study Session Blueprint

**Programme:** Educational Excellence Programme EA-004 — Study Session Architecture & Educational Flow  
**Status:** Binding — permanent Study Session specification for Version 1 onward  
**Effective:** 2026-08-01  
**Authority:** EA-001 PASS · EA-002 PASS · EA-003 PASS · EV-001 · `PRODUCT_BLUEPRINT.md` · Educational Constitution · Study Sensei Philosophy · Guidance Over Content  
**Nature:** Architecture and educational-flow law — not educational content, not application code  
**Parents:** `EA001_SESSION_PHILOSOPHY.md` · `EA001_QUALITY_GATES.md` (Gate SS / Gate LE) · `EA002_EDUCATIONAL_AUTHORING_FRAMEWORK.md` (AF-SS) · `EA003_MISSION_BLUEPRINT.md`  

---

## 1. Purpose of this Blueprint

Define exactly how every Kwalitec Study Session must be conceived, staged, and certified **before** educational content creation begins.

When EA-004 is complete, different educational authors must independently produce Sessions that students immediately recognise as being guided by the same excellent tutor — while the CMP remains the authoritative learning material and Kwalitec remains the educational guide.

> **The Mission decides the day. The Study Session delivers it.**

This Blueprint does **not** rewrite CS1, generate Sessions, amend EA-001 Session Philosophy, or modify application code.

---

## 2. What a Study Session is (architectural definition)

A **Study Session** is the focused educational experience in which the learner **executes** today’s Mission. It is the practice workflow — not the Mission brief, not the textbook, and not a navigation shell.

| The Session answers | The Session does not answer |
|---------------------|----------------------------|
| How study will feel **from begin to close** | What the day’s primary focus *is* (that is the Mission) |
| When Kwalitec guides vs when the student works in the CMP | Full CMP exposition |
| What cognitive work converts exposure into evidence | Opaque readiness theatre |
| What Reflection harvests and what Tomorrow inherits | Mastery from one sitting |
| Whether the Mission’s success criteria were stress-tested | Syllabus inventory browsing |

### Architectural position

```text
Mission (tutor brief — EA-003)
            ↓
   ┌────────────────────┐
   │  STUDY SESSION     │  ← educational experience that delivers the Mission
   │  (this Blueprint)  │
   └─────────┬──────────┘
             ↓
   Learning Episodes (Gate LE)
             ↓
   Reflection → Wrap-up → Tomorrow → Completion
             ↓
   History / Journey / Revision signals / Twin soft evidence
```

- **Session ≠ Mission.** Mission decides; Session executes.  
- **Session ≠ CMP.** CMP holds authoritative content; Session directs engagement with it.  
- **Session ≠ Episode.** Episodes are composable stages inside the Session arc.  
- **Session ≠ Recommendation.** Ranking may inform Mission composition; the Session is the certified student experience.

**Premium standard:** An experienced IFoA tutor would be willing to assign this Session as the student’s primary study block for the hour (`EA001_SESSION_PHILOSOPHY.md` §1).

---

## 3. Governing design rules

| ID | Rule |
|----|------|
| SB-01 | Every Session has a complete educational blueprint (all §5 components populated or lawfully deferred). |
| SB-02 | **Educational rhythm is mandatory.** Guide → CMP study → return → reflect → tomorrow — without continuous interruption. |
| SB-03 | **Reading Guidance is deliberate.** Uninterrupted CMP reading is a designed phase, not an empty shell and not a chatbot monologue. |
| SB-04 | Session multiplies CMP value; it never replaces CMP content (EP-01, EP-04, Guidance Over Content). |
| SB-05 | Session PASS requires parent Mission PASS (Gate MG + EA-003 MX) **and** constituent Episodes PASS Gate LE — never a beautiful Overview over empty stages. |
| SB-06 | Lifecycle green ≠ educational PASS. Certification under EA-004 + Gate SS is required before student exposure. |
| SB-07 | Authors execute one Study Sensei voice (`EA002_TUTOR_VOICE_GUIDE.md`); personal brand dialects are forbidden. |
| SB-08 | Failed topic/locus resolution blocks opening — never degrade to “Today’s topic” placeholders (EV-001 TB-001). |
| SB-09 | Mission information is **oriented once**, then executed — not restacked at every stage. |
| SB-10 | Completion ≠ Mastery. Session finish completes the Session; Topic Complete and Estimated Mastery remain separately governed. |

---

## 4. Session stages (mandatory arc)

Every premium Study Session implements the following stages in educational order. Stage names in product UI may vary; educational jobs may not.

```text
1.  Session Entry
2.  Mission Orientation
3.  Reading Preparation
4.  CMP Reading Guidance
5.  Reading Pause Points          (optional density; 0–N designed pauses)
6.  Knowledge Checks              (after reading — Active Recall / Practice / Checkpoint)
7.  Reflection
8.  Confidence Assessment
9.  Session Wrap-up
10. Tomorrow Preparation
11. Session Completion
```

Detailed rhythm and handoffs: `EA004_STUDY_SESSION_FLOW.md`.  
Reading-specific law: `EA004_READING_GUIDANCE_ARCHITECTURE.md`.

### 4.1 Stage catalogue

| Stage | Educational job | Tutor job | Student action |
|-------|-----------------|-----------|----------------|
| **Session Entry** | Admit only when topic + Mission bind lawfully | Refuse fake Sessions | Confirm ready to begin (or recover honestly) |
| **Mission Orientation** | Connect today’s block to the Mission brief without duplicating Home | One short orientation — purpose, objective, why now | Absorb the brief; begin |
| **Reading Preparation** | Create selective attention before CMP opens | Focus questions, locus, stop condition, duration honesty | Know what they are hunting for |
| **CMP Reading Guidance** | Direct engagement with authoritative material | Set objectives, misconceptions to watch, exit into reading | Open CMP; study under guidance |
| **Reading Pause Points** | Sparse accountability without continuous interruption | At most a few designed checkpoints | Answer/note, then resume CMP |
| **Knowledge Checks** | Convert exposure into retrieval/performance | Closed-book or reduced-cue demand + feedback | Explain / solve / identify / justify |
| **Reflection** | Harvest residual uncertainty (EP-07) | Topic-specific prompts | Student-authored clarity + gaps |
| **Confidence Assessment** | Soft metacognitive signal — not mastery | Honest confidence probe tied to today’s criteria | Self-rate with warrant awareness |
| **Session Wrap-up** | Summarise what was studied and evidenced | Truthful close — no mastery theatre | See Study Progress language |
| **Tomorrow Preparation** | Continuity handoff (EP-02) | Tomorrow Preview + optional light prep | Know how the story continues |
| **Session Completion** | Lawful close; update history/journey inputs | One Educational Truth across surfaces | Leave able to stop without anxiety |

### 4.2 Stage composition note

Stages 4–6 map to Learning Episodes (Guided Reading · Worked Example · Practice · Checkpoint as needed). Advertised “Activity N of M” must be reachable (EV-001 TB-008; Gate LE-08).

Reading Pause Points are **not** a separate continuous chat layer. They are authored sparse checkpoints inside Guided Reading (see Reading Guidance Architecture).

---

## 5. Permanent Session specification (mandatory components)

Every Session authoring pack **must** define the following components. Component IDs are stable for review, certification evidence, and joint Mission-bundle publication.

### 5.1 Educational Purpose

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `session_educational_purpose` |
| **Definition** | One sentence stating why this Session exists as today’s primary study block. |
| **Standard** | Educational purpose aligned to parent Mission Purpose / Educational Intent. Names the cognitive move the Session will execute. |
| **Fail if** | Vague (“help the student study”); platform-centric; restates Mission title alone without execution intent. |
| **Principles** | EP-01 · EP-03 |

---

### 5.2 Tutor Purpose

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `session_tutor_purpose` |
| **Definition** | What the Study Sensei is trying to achieve as a tutor **during the Session** — the coaching sequence. |
| **Standard** | **Mandatory.** Written as an IFoA tutor’s private note: “In this hour I will… so that the candidate…” Must extend (not copy-paste) Mission `tutor_intent`. Must specify when guidance yields to uninterrupted CMP work. |
| **Fail if** | Missing; identical to Mission Tutor Intent without Session-specific moves; interchangeable across Sessions. |
| **Principles** | EP-09 · SB-02 |

**Example (illustrative pattern only):**  
> In this hour I will set three focus questions, exit while the candidate works Example 2 alone, then force a closed-book linear-predictor explanation — so today’s Mission success criterion is stress-tested, not merely claimed.

---

### 5.3 Student Actions

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `student_actions` |
| **Definition** | Ordered list of what the student must *do* (not merely see) across the Session. |
| **Standard** | Each action is a cognitive verb: open, extract, annotate, attempt, explain, solve, reflect, rate. Passive “read everything” alone is insufficient. |
| **Fail if** | Empty; only navigation clicks; no post-reading retrieval action. |
| **Principles** | EP-03 · EP-05 |

---

### 5.4 CMP Interaction

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `cmp_interaction` |
| **Definition** | How the Session uses the CMP: open locus, stop condition, out-of-scope, pause points, return cue. |
| **Standard** | Must implement Mission `cmp_reading_scope`. Must define **exit into reading** and **re-entry after reading**. Must not paste CMP prose into Session body. |
| **Fail if** | “Read the material” with no locus (TB-007); CMP dump; no return path. |
| **Principles** | EP-01 · EP-04 · Guidance Over Content |
| **Detail** | `EA004_READING_GUIDANCE_ARCHITECTURE.md` |

---

### 5.5 Expected Outputs

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `expected_outputs` |
| **Definition** | Artefacts the student produces during the Session (notes, answers, reflection text, confidence mark). |
| **Standard** | Named and countable. Aligns to Mission Success Criteria and Episode success criteria. |
| **Fail if** | No student-produced evidence path; “answer recorded” with nowhere to go (TB-008 pattern). |

---

### 5.6 Success Evidence

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `success_evidence` |
| **Definition** | What counts as evidence that today’s success criteria were attempted and feedbacked. |
| **Standard** | Prefer closed-book / reduced-cue checks. Language: Study Progress / Educational Evidence candidates — never Estimated Mastery from one soft check alone. |
| **Fail if** | Reading completion treated as proof of retention; readiness ±N% as sole success; mastery theatre. |
| **Principles** | EP-05 · EP-06 · Constitution VIII |

---

### 5.7 Reflection Evidence

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `reflection_evidence` |
| **Definition** | What Reflection must capture for continuity and revision fuel. |
| **Standard** | Implements Mission `reflection_goal`. Topic-specific prompts. Student-authored (or structured student decisions). Required before educational close. |
| **Fail if** | Generic placeholders; system-written reflection attributed to student; skip Reflection while marking complete. |
| **Principles** | EP-07 · Gate SS-04 |

---

### 5.8 Revision Signals

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `session_revision_signals` |
| **Definition** | What from this Session should later shape revision (weak check, named misconception hit, Reflection residual). |
| **Standard** | Aligns to Mission `revision_signals`. Soft/hard signal paths named. May note “normal decay only” when Tutor Purpose documents no special flag. |
| **Fail if** | Silent on high-risk exam topics; invents revision without evidence path. |
| **Principles** | EP-06 · Gate RV (downstream) |

---

### 5.9 Continuity Evidence

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `continuity_evidence` |
| **Definition** | Proof the Session preserves yesterday → today → tomorrow without truth splits. |
| **Standard** | Prior bridge (or cold-start) visible at Orientation; Tomorrow Preparation agrees with Mission Tomorrow Bridge and Gate TP; completion updates History/Journey consistently (EP-10). |
| **Fail if** | Contaminant tomorrow; Home/History contradiction by design; fabricated next topic. |
| **Principles** | EP-02 · EP-10 |

---

### 5.10 Publication Metadata

| Attribute | Requirement |
|-----------|-------------|
| **Field ID** | `session_publication_metadata` |
| **Definition** | Package identity, versions, certification outcomes, joint Mission-bundle linkage. |
| **Standard** | Subject/package version; CMP edition pin; parent Mission ID; Episode IDs; Gate SS/LE outcomes; Rubric score; reviewer IDs; dates; status (`draft` / `certified` / `published` / `retired`). |
| **Fail if** | Orphan Session; missing joint links at Publication Approval; automation-only Tutor Voice PASS in Version 1. |

---

### 5.11 Supporting fields (required for certification)

| Field ID | Requirement |
|----------|-------------|
| `parent_mission_id` | Linked certified or co-certifying Mission |
| `learning_objective` | Session-facing objective — may equal Mission objective if identical; must not collapse to syllabus heading |
| `concept_focus` | Single idea/skill centre for the block |
| `stage_plan` | Ordered stage list matching §4; Episode type per stage |
| `duration_budget` | Honest minutes consistent with Mission `estimated_study_time` and depth (SS-06) |
| `cognitive_load` | Light · Moderate · Heavy · Very Heavy — consistent with Mission load |
| `knowledge_check_design` | At least one Active Recall / Practice / Checkpoint after reading |
| `confidence_assessment_design` | Soft probe design; must not claim mastery |
| `interruption_budget` | Max designed pause points during CMP reading (see Flow / Reading Guidance) |
| `unavailable_policy` | Honest recovery when topic/locus cannot resolve — never placeholders |

---

## 6. Division of labour — Kwalitec vs CMP (Session-level)

| Phase | Inside Kwalitec | Inside the CMP |
|-------|-----------------|----------------|
| Entry / Orientation | Bind Mission; orient; Begin | — |
| Reading Preparation | Objective, focus questions, misconceptions watch-list, stop, duration | — |
| During Reading | Sparse guidance + pause points + return cue | Authoritative exposition, definitions, worked theory, full examples |
| Knowledge Checks | Recall / practice / feedback / advance | Reference only after attempt (if needed) |
| Reflection / Confidence | Topic-specific prompts; soft signals | — |
| Wrap-up / Tomorrow / Completion | Truthful summary; continuity; history inputs | Optional skim-ahead locus if named |

**Hard rule:** Kwalitec never pretends the CMP chapter lives inside the Learning Episode.  
**Hard rule:** The CMP never decides today’s Mission, never holds Twin state, and never replaces Reflection.

---

## 7. Relationship to superior law

| Authority | Relationship |
|-----------|--------------|
| EA-001 Session Philosophy | **Extended, not amended.** EA-004 supplies field-level architecture, rhythm engineering, Reading Guidance law, and Session certification deepening. |
| EA-001 Gate SS / Gate LE | Remain mandatory. EA-004 adds Session Certification Gate SX + Rubric threshold. |
| EA-002 AF-SS | Production process for Session class; EA-004 is architecture specialisation (rank **3d**). |
| EA-003 Mission Blueprint | Parent Mission fields (Tutor Intent, CMP scope, Reflection Goal, Continuity Bundle, Revision Signals) are **inputs** to Session design. Session must not contradict them. |
| Guidance Over Content | Session guides into CMP; does not become a second textbook. |
| Educational Constitution | Completion ≠ Mastery; evidence ranks; Learning Mode topic law preserved. |

---

## 8. Fitness test (Academic Board)

A Session is premium only if all are true:

1. An IFoA tutor would assign it as today’s primary block.  
2. CMP and Kwalitec roles are unmistakable.  
3. Educational rhythm is felt: guidance yields to study, then returns for recall and reflection.  
4. No placeholders, dumps, excessive interruption, or stuck advances.  
5. Reflection and Tomorrow Preparation preserve continuity.  
6. Surfaces agree on what was completed.  
7. Rubric ≥ publication threshold with no automatic reject class (`EA004_SESSION_CERTIFICATION.md`, `EA004_SESSION_SCORING_RUBRIC.md`).

Fail any → fail Gate SS / EA-004 certification → must not reach students.

---

## 9. Explicit non-goals

EA-004 does **not**:

- Author CS1 or any subject Session content  
- Rewrite Missions, Episodes, or CMP materials  
- Modify application code, templates, or runtime behaviour  
- Amend EA-001 / EA-002 / EA-003 text  
- Claim EV-001 FAIL resolved  
- Declare Version 1 production-ready or KSI ≥ 80  

---

## 10. Stop

This Blueprint is architecture. Successor programmes may author Session packs under this Blueprint and submit them through `EA004_SESSION_CERTIFICATION.md` (within `EA002_CERTIFICATION_WORKFLOW.md`) → joint Mission-bundle `EA002_PUBLICATION_WORKFLOW.md`.
