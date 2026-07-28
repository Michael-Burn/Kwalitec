# Adaptive Assessment Vision

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Version:** 1.0  
**Status:** Design — product experience authority for Adaptive Assessment  
**Effective:** 2026-07-28  
**Authority:** Product design (subordinate to ILE-000 strategy, Educational Constitution, Vision 2030)  
**Depends on:** Certified Educational Intelligence Platform; AP-002 Assessment Engine design; AP-001 Assessment Pipeline  

---

## Purpose

Define why Adaptive Assessment exists as a **learner experience**, not merely as a question-selection algorithm.

This vision governs ILE-001 design. It does not change Educational Intelligence authorities, Twin inference rules, Mission scheduling math, or Tutor explanation law.

---

## One-line thesis

> **Adaptive Assessment helps the student and the system know what is understood — calmly, honestly, and only when evidence is needed.**

---

## Why Adaptive Assessment exists

Professional candidates prepare for months across dense syllabuses. They need more than “another quiz.” They need timely, explainable checks that:

1. Reduce uncertainty about what they actually understand.
2. Correct false confidence before it becomes exam risk.
3. Feed one coherent Educational State so tomorrow’s mission stays accurate.
4. Feel like study support — never like a surprise exam.

Without Adaptive Assessment, Kwalitec can plan and recommend from thin or stale evidence. With it, daily guidance becomes more trustworthy because it rests on fresher, purpose-built observations.

Adaptive Assessment is the student-facing expression of assessment-as-evidence (Educational Philosophy; AP-002). It sits in the **Intelligent Learning Experience** layer: it surfaces the certified platform; it does not invent a second educational brain.

---

## Problems it solves

| Student problem | How Adaptive Assessment helps |
|---|---|
| **False confidence** | Short, framed checks reveal gaps between feeling ready and showing understanding. |
| **Unknown unknowns** | Diagnostic and exploration checks locate thin Twin evidence before weeks are wasted. |
| **Decision overload** | The product chooses *when* and *why* a check appears — the student does not invent a quiz plan. |
| **Opaque “adaptivity”** | Every check explains purpose, evidence use, and next step in plain language. |
| **Stale study plans** | Fresh observations update Twin belief via Reasoning so Missions stay aligned with reality. |
| **Anxiety from “testing”** | Experience design rejects marks theatre, rankings, and surprise exams. |
| **Repetitive questioning** | Selection respects recent evidence, available time, and trust — not volume for engagement. |
| **Return after inactivity** | Recovery checks re-establish state gently without pretending nothing changed. |

---

## Student value

| Value | Meaning in practice |
|---|---|
| **Clarity** | “I know what this check is for and what happens with my answers.” |
| **Honesty** | Outcomes talk about evidence and next study — not identity-defining scores. |
| **Progress that feels real** | Completing a check visibly informs what Kwalitec believes and what to do next. |
| **Protected motivation** | Mistakes are fuel for recovery; exits and pauses are allowed. |
| **Fewer wasted hours** | Checks target uncertainty and weak topics rather than random drills. |
| **Exam-honest readiness** | Pre-exam confidence checks calibrate belief without promising a pass. |

Success is not “more questions answered.” Success is **better-calibrated learning decisions** and **sustained trust**.

---

## Relationship with Missions

| Role | Owner |
|---|---|
| **What to do today** | Adaptive Mission Engine (Mission / Session) |
| **Whether a check belongs in today** | Mission construction using Twin decisions + eligibility gates |
| **How the check feels** | Adaptive Assessment experience (this programme) |
| **What the check produces** | Observations → AP-001 → Reasoning → Twin |

**Principles**

- Assessment is an **activity class** inside or beside a Mission — not a parallel “do this instead of your session” product.
- Mission owns *Next*; assessment must not spawn competing CTAs of equal weight on Home.
- Checks appear with framing (“why this learning check exists”) — never as surprise pop exams.
- Over-assessment is a Mission failure mode: if density, burnout, or time gates fail, prefer study/practice/recovery over forcing a check.
- After assessment, Mission refresh (same day or next day) consumes **updated Twin state**, not Engine-local grades.

Learner language: prefer **learning check**, **Quick Check**, **session step** over “test” or “exam.”

---

## Relationship with Tutor

| Role | Owner |
|---|---|
| **Explain what the check meant** | Intelligent Tutor |
| **Decide mastery / gaps / next action** | Educational Reasoning → Twin |
| **Deliver the instrument** | Assessment experience / Engine |
| **Narrate without re-scoring** | Tutor |

**Principles**

- Tutor explains decisions already made; it does not grade, re-score, or invent mastery.
- Immediate post-check feedback is short and deterministic; deeper “Explain this” is Tutor-on-request.
- Tutor copy must preserve psychological safety and Educational Honesty (no pass/fail identity, no peer ranking).
- Assessment must not depend on chat as a second reasoning path.

---

## Relationship with the Student Digital Twin

| Role | Owner |
|---|---|
| **Sole learner-state source of truth** | Student Digital Twin |
| **Produce observations** | Adaptive Assessment → Assessment Pipeline |
| **Interpret observations** | `StudentReasoningService` / Educational Reasoning |
| **Store revised belief** | Twin (mastery confidence, gaps, uncertainty, recommendations) |

**Principles**

- Adaptive Assessment exists to **reduce Twin uncertainty** where evidence is thin, unstable, conflicting, or stale — not to decorate the UI with quiz chrome.
- A single check never declares mastery as fact.
- Incomplete or interrupted sessions must not invent confidence; they leave evidence incomplete and uncertainty honest.
- Personalisation of *which* check appears is Twin- and curriculum-bound; the Twin is never rewritten by the experience layer.

**Student-facing speech:** talk about “what we know so far about your understanding” — not “Digital Twin update.”

---

## Relationship with certified Educational Intelligence

Canonical chain (unchanged):

```
Evidence (assessment observations)
  → Interpretation
  → Decision
  → Twin update
  → Graph projection
  → Mission planning
  → Tutor explanation
```

ILE-001 designs how students **enter, feel, and understand** the assessment segment of that chain. It must not bypass Reasoning, create shadow recommendations, or add LLM authority into selection or scoring.

---

## Non-goals

- High-stakes exam simulation as the default Adaptive Assessment experience  
- Marks, percentages-as-identity, leaderboards, or competitive ranking  
- Engagement maximisation via endless questions  
- Opaque adaptive algorithms presented as “AI knows you” without explainable intent  
- Redesign of Educational Intelligence authorities or educational reasoning rules  
- Replacing Missions or Tutor as the student’s primary daily companion  

---

## Design success (vision level)

A serious candidate should be able to say:

> “Those checks help me see what I actually understand, and my study plan feels more accurate — without feeling like I’m sitting an exam.”

If they feel judged, surprised, or scored into an identity, the experience has failed this vision even if observations were technically perfect.

---

## Governing references

| Document | Role |
|---|---|
| `PRODUCT_STRATEGY.md` / `PRODUCT_PRINCIPLES.md` | ILE-000 product law |
| `EDUCATIONAL_PHILOSOPHY.md` / `USER_EXPERIENCE_PHILOSOPHY.md` | Learning & UX philosophy |
| `PRODUCT_ROADMAP.md` | ILE-001 programme intent |
| `AP-002/PRODUCT_SPECIFICATION.md` | Assessment Engine product thesis |
| Educational Constitution | Binding educational law |

---

**End of ADAPTIVE_ASSESSMENT_VISION**
