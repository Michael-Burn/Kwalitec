# IA-004 — Truthful Learning Progress

**Capability ID:** IA-004  
**Programme:** Internal Alpha Stabilization  
**Priority:** P0  
**Status:** Implemented — pending Architecture Review  
**Date:** 2026-07-15

---

## Educational Philosophy

Kwalitec must communicate the truth of a student's educational state.

Students may declare what they have **studied**.  
Kwalitec may estimate what they **know**.  
Neither screen nor student may declare **Mastery** by checkbox.

Mastery is inferred from accumulated educational evidence by the Digital Twin
(and related estimation paths). Completing a topic records Study Progress
only. Completing a topic must never be presented as mastering it.

---

## Domain Model

| Concept | Question answered | Owner | Editable by student? |
|---------|-------------------|-------|----------------------|
| **Study Progress** | What have I studied? | Student | Yes |
| **Learning Progress** | How far through the syllabus have I progressed? | Application | Derived |
| **Knowledge State** | How well do I currently understand this topic? | Digital Twin | Evidence-derived |
| **Mastery / Estimated Mastery** | How confident is Kwalitec that I have mastered this topic? | Digital Twin | Estimated only — never manually editable |

These concepts must never be conflated in UI copy, progress writes, or mission selection.

---

## Terminology

### Preferred (student-facing)

- Completed / Completed Study
- Continue Learning
- Study Progress
- Learning Progress
- Estimated Knowledge
- Estimated Mastery

### Avoid (student-facing)

- Mastered (as a completion checkbox or badge for study completion)
- Fully Learned
- Finished Learning Forever
- Evidence Creating / pipeline / Twin jargon on student surfaces
- System identifiers

Internal engineering fields may still say `mastery_score` or stage
`Mastered` where Adaptive Learning already computes estimates. Presentation
must map those values to estimated language, and never invent scores from
completion alone.

---

## Student Mental Model

1. I mark topics I have **completed studying**.
2. Kwalitec advances my **Current Learning Topic** through the syllabus.
3. Today's Mission follows that learning sequence (**Learning Mode**).
4. Estimated Mastery appears only after study evidence exists.
5. Review suggestions may appear as recommendations — they do not silently
   replace today's learning mission in v1.0.

---

## Before / After Examples

### Study Plan completion

| | Before | After |
|---|---|---|
| Edit copy | “check topics you've already **mastered**” | “check topics you have already **completed studying**” |
| Wizard init | `completed=True`, `mastery_score=100`, `confidence=Mastered` | `completed=True`, `mastery_score=0`, `confidence=High` |
| Roadmap metric | “Mastery 100%” from completion | No Estimated Mastery until attempt evidence; badge remains **Completed** |

### Mission completion

| | Before | After |
|---|---|---|
| Progress write | `completed=True` **and** floor `mastery_score` to 70 | `completed=True` only — mastery score unchanged |
| Meaning | Completion looked like partial mastery | Completion = Study Progress |

### Today's Mission topic

| | Before | After |
|---|---|---|
| Selection | Review due → weak topics → next incomplete | **Learning Mode:** Current Learning Topic (next incomplete) only |
| Result | Completed weak topic 2.6 could replace learning topic 4.2 | Mission stays on the planned learning topic |
| Why copy | Generic “recommended focus” | Explains Learning Mode + Study Progress vs Estimated Mastery |

---

## Mission Strategy (Learning Mode)

Version 1.0 default study strategy is **Learning Mode**:

- Today's Mission always follows the **Current Learning Topic** within the
  active Study Plan (first incomplete syllabus leaf).
- Adaptive interruption (review / weak topics / spaced repetition) is
  **deferred** to Educational Intelligence Phase 1.
- Review recommendations may still appear on advisory surfaces, but must
  **never silently replace** Today's Learning Mission.

---

## Relationship to Digital Twin

IA-004 does **not** redesign Digital Twin mathematics, evidence extraction,
or Educational Intelligence algorithms.

It aligns:

- product terminology,
- progress persistence behaviour,
- mission strategy defaults,

with the Educational Intelligence architecture already documented for the Twin:

- declarations ≠ mastery beliefs
- completion ≠ knowledge growth
- mastery remains estimated from evidence

Legacy `TopicProgress.mastery_score` remains the presentation-facing estimate
when attempt-derived accuracy exists (`has_estimated_mastery`). Twin belief
surfaces stay on their existing paths.

---

## Future Educational Intelligence

Phase 1 may introduce:

- explained review interruptions,
- weak-topic missions with student-visible reasons,
- spaced repetition scheduling that does not quietly override Learning Mode
  without disclosure.

Until then, Learning Mode remains the sole mission topic authority.

---

## Out of Scope

- Redesigning Digital Twin or Twin update strategies
- Changing evidence extraction / EI ranking math
- Implementing adaptive interruption or spaced repetition in mission generation
- Introducing AI / LLM calls

---

## Verification

Regression suite: `tests/test_ia004_truthful_learning_progress.py`

- Completing a topic records completion only
- Completing a topic does not set mastery
- Study Plan labels use truthful terminology
- Dashboard labels match underlying data
- Mission generation follows Current Learning Topic
- Review topics never silently replace Learning Mode
- Student-facing wording contains no false mastery claims
