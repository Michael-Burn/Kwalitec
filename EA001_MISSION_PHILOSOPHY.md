# EA-001 — Mission Philosophy

**Programme:** Educational Excellence Programme EA-001  
**Status:** Binding — Mission authoring constitution  
**Effective:** 2026-08-01  
**Parent:** `EA001_EDUCATIONAL_FOUNDATION.md` · `EA001_EDUCATIONAL_PRINCIPLES.md`  
**Related:** Canonical Educational Lexicon · Educational Constitution Article IV §4 & Article VI · EV-001 Mission Quality Report  

---

## 1. Purpose

Define how a Mission must be authored so that every daily focus feels like a tutor brief — never a syllabus checkbox.

EV-001 scored Mission Quality **2/10**: titles, objectives, and narratives collapsed to the same syllabus heading; explainability was boilerplate; platform meta replaced teaching voice.

This document is the permanent authoring law. Successor programmes may implement generators or human authoring workflows; they may not weaken these requirements.

---

## 2. What a Mission is

A **Mission** is the authorised primary educational focus for a day (or study period):

- **What** deserves attention now  
- **Why** it deserves attention now (one educational reason)  
- **What benefit** the student should expect if they complete it  
- **How** it will be executed (Session structure pointer — not the Session itself)

Mission ≠ Session.  
Mission ≠ Recommendation (Recommendation may underlie Mission composition).  
Mission ≠ Syllabus heading.

Under Learning Mode (Version 1 default), Mission topic follows Current Learning Topic in official syllabus order (Constitution Article VI). Authoring quality is independent of that selection rule — correct topic + weak brief is still a fail.

---

## 3. Authoring standard — Tutor Brief

Every Mission must be writable as a short tutor brief a human IFoA tutor would send the night before.

### Mandatory educational elements

| Element | Requirement |
|---------|-------------|
| **M1 Topic identity** | Official topic code + accurate human title. Never placeholder. Never contaminant string. |
| **M2 Distinct objective** | One learning objective with an actionable verb; **not** identical to the syllabus heading string. ≤160 characters preferred (aligns V1 E2 spirit). |
| **M3 Bridge from prior learning** | Explicit continuity from the previous Mission/topic when history exists (“Yesterday… Today…”). Cold start: bridge from enrolment goal or chapter purpose. |
| **M4 Why now** | Educational reason grounded in syllabus order, prerequisite readiness, exam skill/weight, or disclosed mode (Learning / Revision). Not “highest-value next step” alone. |
| **M5 Concept focus** | The single idea or skill that defines the day (e.g. “exponential family + linear predictor,” not “Today’s topic”). |
| **M6 Success criterion** | What the student should be able to explain or do after the Session — countable, assessable. |
| **M7 Session intent** | Named structure (e.g. Guided Reading → Worked Example → Practice → Reflection) matching real episodes. |
| **M8 Material locus** | Where to open the CMP (or authorised materials) for today’s work. |
| **M9 Expected benefit** | Plain educational benefit (skill, coverage step, evidence creation) — not opaque readiness ±N% as the sole outcome. |
| **M10 Handoff / Tomorrow** | Continuity toward the next lawful focus when known; honest absence when not. |
| **M11 Explainability** | “Why this guidance?” cites specific prior topic, prerequisite, or exam-skill gap — unique enough that two different missions cannot share identical rationale text. |
| **M12 Voice** | Tutor Voice (EP-09). Study Sensei tone. No platform essays on the hero surface. |

### Optional but encouraged

- Exam cue (“Examiners often ask…”) when accurate  
- Time box consistent with Session Philosophy duration honesty  
- Link to residual uncertainty from prior Reflection when available

---

## 4. Prohibited patterns

The following are **forbidden** in any Mission that reaches students:

| ID | Prohibited pattern | EV-001 / principle link |
|----|--------------------|-------------------------|
| P1 | Syllabus-heading-only Mission (title = objective = narrative) | TB-002; EP-09 |
| P2 | Placeholder strings (“Today’s topic”, “Strengthen today’s focus topic”) | TB-001 |
| P3 | Raw CMP paste or syllabus dump as narrative body | E1; EP-01 |
| P4 | Publisher metadata / addresses / boilerplate as topic identity | TB-003 |
| P5 | Identical explainability boilerplate across missions | TB-004; EP-10 |
| P6 | Platform meta as hero narrative (“Mission ≠ mastery”, runtime names, milestone IDs) | Experience Guidelines; EP-09 |
| P7 | Mission that advertises stages with no authored episodes behind them | TB-007/008 |
| P8 | Claiming Mission completed while Home still assigns the same Mission (truth split) | TB-005; EP-10 |
| P9 | Treating Mission completion language as mastery | Constitution VIII |
| P10 | Silent topic replacement of Learning Mode focus by advisory ranking | Constitution VI |
| P11 | Mechanically concatenated template fragments | Episode audit flags |
| P12 | Engagement bait unrelated to exam preparation | EP-08 |

---

## 5. Worked authoring example (illustrative)

**Unfit (EV-001 pattern):**

> Study 4.2 — Understand and use generalised linear models  
> Objective: Study 4.2 — Understand and use generalised linear models  
> Why: highest-value next step toward exam readiness  

**Fit (EA-001 pattern):**

> **Mission:** Extend linear models to GLMs  
> **Objective:** Explain how a GLM uses a linear predictor and link function for a non-normal response.  
> **Bridge:** Yesterday you finished classical linear models. Today the same linear machinery expands to responses that are not Normal.  
> **Why now:** Next incomplete syllabus unit after 4.1; exam questions frequently require choosing and justifying a link.  
> **Focus:** Exponential family → linear predictor → link.  
> **Success:** Closed-book, name one response distribution and its canonical link; point to where it sits in the CMP example.  
> **Materials:** CMP §4.2 (GLM setup) through first worked example.  
> **Structure:** Guided Reading → Worked Example pause → Recall → Reflection.  
> **Tomorrow:** Bayesian foundations (5.1) — likelihood thinking carries forward.

---

## 6. Relationship to Session and Episodes

| Artefact | Authoring dependency |
|----------|----------------------|
| Mission | May ship to Home only if M1–M12 satisfied **and** linked Session/Episodes pass their gates (or Mission is honestly marked unavailable). |
| Session Overview | Inherits topic/objective/focus from Mission; must not invent a second story. |
| Learning Episodes | Implement Mission’s Session intent; Guided Reading must reference Mission’s material locus. |
| Tomorrow Preview | Must agree with Mission M10 / Summary. |

A beautiful Mission brief with empty episodes is still a **student-facing fail**. Certification is joint (see Quality Gates).

---

## 7. Generation vs human authoring

Whether a Mission is human-written, template-filled with certified fields, or composition-engine assembled:

1. Output must satisfy M1–M12 and avoid P1–P12.  
2. Generative AI may polish wording only behind ports that cannot invent syllabus order, mastery, or rankings (Study Sensei / Vision AI philosophy).  
3. Failed field resolution → block publication / block student open — never degrade to placeholders.  
4. Educational Authoring composes; it does not silently reschedule Learning Mode authority (V1 A8 spirit).

---

## 8. Mission quality score (review rubric)

For human or Board review (aligned with EV-001 dimensions):

| Dimension | Fail signals | Pass signals |
|-----------|--------------|--------------|
| Narrative | Syllabus paste; platform meta | Tutor bridge + purpose |
| Objective | Duplicate of title | Distinct actionable verb |
| Continuity | No yesterday/tomorrow | Explicit arc |
| Explainability | Identical boilerplate | Specific educational reason |
| Executability | No CMP locus; empty episodes | Clear materials + real stages |
| Honesty | Mastery theatre; dual truth | Study Progress language; aligned surfaces |

**Minimum bar:** An IFoA tutor would send this brief to a candidate. Below that → do not certify.

---

## 9. Closing rule

> A Mission must never simply restate a syllabus heading.

If removing the topic code would leave no educational guidance, the Mission is not yet a Mission — it is a label. Labels do not reach students under EA-001.
