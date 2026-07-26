# Session Explainability

**Programme:** VI — Workstream 2 — Daily Coach  
**Milestone:** MS002 — Learning Session Model  
**Classification:** Explainability contract for Learning Session structure and activities  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how Kwalitec explains **why a study session is structured as it is**, **why activities appear in this order**, and **how each activity contributes to long-term learning**.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` (EIP-003)
3. `EDUCATIONAL_LOGIC_REGISTRY.md` (especially EL-008, EL-010)
4. `LEARNING_SESSION_MODEL.md`
5. `SESSION_OBJECTIVES.md`
6. `SESSION_STRUCTURE.md`
7. `SESSION_TRANSITIONS.md`
8. `SESSION_ADAPTATION.md`
9. `../daily_coach/DAILY_COACH_EXPLAINABILITY.md`
10. `../EDUCATIONAL_EVIDENCE_MODEL.md`

> **Every material session-structure decision must reference today’s Daily Coach objective and the educational purpose of the phases.  
> Explainability improves understanding of guidance already authorised. It never invents educational certainty or redefines the day.**

---

## 1. Purpose

Students should never have to guess why this sitting looks the way it does.

Session explainability exists so that every material phase composition, ordering choice, and adaptation answers — in plain educational language — what is known, what is estimated, why this structure serves today’s objective, and how the activities build long-term learning.

Without session explainability:

- phases feel like arbitrary product steps;
- retrieval feels like testing rather than learning;
- adaptation feels like the system changing its mind about the day;
- completion is mistaken for mastery.

With session explainability:

- the student trusts the tutor method;
- today’s Daily Coach objective remains visible inside the sitting;
- long-term learning contribution is intelligible;
- claim types stay honest.

---

## 2. Traceability Obligation (Architectural)

Every material Learning Session structure decision must be traceable through:

| Trace link | Student-facing role |
|------------|---------------------|
| **Daily Coach primary objective** | “Today’s focus is… so this session is for…” |
| **Day posture / mode disclosure** | “Because today is revision / recovery / first-pass…” |
| **Session aim cluster** | “In this sitting we are aiming to…” |
| **Phase composition** | “That is why we start with… then…” |
| **Ordering rationale** | “We practise after examples so that…” |
| **Long-term contribution** | “This helps later because…” |
| **Adaptation / escalation (when present)** | “We adjusted how we’re studying because… / We need to revisit today’s plan because…” |

Internal IDs (LSO-XX, LSP-XX, LST-XX, LSA-XX, DCO-XX) may exist for algorithms and audits. They must not appear as student-facing jargon.

A session structure with no Daily Coach objective warrant is invalid — even if the explanation sounds motivating.

---

## 3. Explainability Principles

1. **Day + session.** Tie structure to today’s objective before describing techniques.
2. **Purpose of each phase.** Name the educational job of preparation, retrieval, practice, reflection — not only the UI label.
3. **Order is educational.** Explain sequence as learning logic (encode → exemplify → retrieve → practise → reflect), when that logic applies.
4. **Long-term thread.** Connect activities to durable competence, not only to finishing the sitting.
5. **Facts and estimates stay distinct.** Attempt outcomes are not mastery.
6. **Adaptation is disclosed.** Material mid-session changes say *what changed in method* and *what did not change in today’s job*.
7. **Escalation is plain.** When the day must be revisited, say so without blame theatre.
8. **Internal machinery stays invisible.** No Twin facets, optimiser names, or registry IDs.
9. **Uncertainty is named** when progress signals are thin.
10. **No new algorithms in speech.** Copy narrates authorised structure; it does not invent scores.

---

## 4. Three Mandatory Explanation Duties

Beyond EIP-003’s four questions, every material session must be able to explain:

### Duty A — Why the session is structured this way

Answer in plain language:

- what today’s Daily Coach objective is;
- which session aims that implies (learn / retrieve / practise / revise / recover…);
- which phases were selected to serve those aims;
- which phases were lawfully omitted and why.

**Good shape:**  
“Today’s focus is consolidating Topic T. So this session emphasises recall and targeted questions rather than learning brand-new material.”

**Bad shape:**  
“Next up: Activity 3 of 7.” (structure without purpose)

---

### Duty B — Why activities appear in this order

Answer in plain language:

- what educational dependency the order respects (e.g. examples before independent practice);
- what signal would have justified a different order;
- why any regress (back to examples) is helpful, not failure.

**Good shape:**  
“We’ll walk one worked example before timed questions so the method decisions are clear — then you’ll try without the solution in view.”

**Bad shape:**  
“The workflow always does examples before questions.” (template absolutism without today’s reason)

---

### Duty C — How each activity contributes to long-term learning

Answer in plain language:

- what durable educational good the activity builds (accurate representation, usable memory, exam method, calibrated confidence, honest residue);
- what it does *not* prove (mastery, exam mark, readiness certainty);
- how it supports later revision/practice under the Study Plan.

**Good shape:**  
“Closed-book recall now makes it more likely you’ll still be able to produce this method in a week — recognition alone usually fades.”

**Bad shape:**  
“Complete this to unlock mastery.” (mastery minting)

---

## 5. Four-Question Framework (Session Specialisation)

Every material session-structure recommendation must answer EIP-003’s four questions, specialised for the sitting:

### Q1 — What do we objectively know?

Examples:

- Today’s Daily Coach objective is practice on Topic T.
- Available remaining time is short.
- The student just failed a closed-book reconstruction of the method.
- An interruption suspended the sitting at the practice phase.

### Q2 — What do we estimate?

Examples:

- The core idea appears provisionally formed (label as estimate / check — not mastery).
- Fatigue seems to be reducing attempt quality.
- If estimation is not yet lawful: say it cannot yet be estimated.

### Q3 — Why are we recommending this structure / next phase?

One educational explanation tying **today’s objective** to **session method**.

Examples:

- “Because today is first-pass learning, we start with a short orientation and focused explanation before any heavy question set.”
- “Your recall slipped on the triggering conditions, so we’re returning to a worked contrast before more practice.”
- “Time is short, so we’re keeping the same practice goal with a smaller complete arc and a brief reflection.”

### Q4 — What should the student do next?

One clear educational action consistent with the current lawful phase.

---

## 6. Explanation Catalogue (LSE)

| ID | Explanation kind | Must make clear |
|----|------------------|-----------------|
| **LSE-01** | Session purpose statement | Link to DCO-01 + session aim cluster |
| **LSE-02** | Phase inclusion rationale | Why this phase serves today’s job |
| **LSE-03** | Phase omission rationale | Why a catalogue phase is not needed now |
| **LSE-04** | Ordering rationale | Why this sequence (Duty B) |
| **LSE-05** | Activity → long-term learning | Durable contribution without mastery theatre (Duty C) |
| **LSE-06** | Transition rationale | Why advancing / holding / regressing now |
| **LSE-07** | Adaptation disclosure | What method changed; what day’s job did not |
| **LSE-08** | Escalation explanation | Why Daily Coach must revisit the day |
| **LSE-09** | Honest close summary | What the sitting advanced vs what remains — no readiness theatre |

Minimum for an ordinary study sitting: **LSE-01, LSE-04, LSE-05, LSE-09**, plus **LSE-07/LSE-08** when adaptation or escalation occurs.

---

## 7. Student Language Rules (Session)

Prefer:

- “today’s focus,” “this sitting,” “recall,” “worked example,” “practice,” “check your understanding,” “what still feels shaky”
- “we’re adjusting *how* we study this — today’s goal stays the same”
- “finishing this sitting means we completed today’s study work, not that the topic is mastered”

Avoid:

- Twin / optimiser / registry vocabulary
- “mastered,” “proven ready,” “guaranteed” from phase completion
- implying the clock alone decided the next step
- implying mid-session topic hopping is normal coaching

Align confidence messages with Daily Coach DCO-05 honesty rules.

---

## 8. Good and Bad Examples

### Structure

| Good | Bad |
|------|-----|
| “Today is revision for Topic T, so we’ll emphasise closed-book recall and a few exam-style questions — not new reading.” | “Here’s your content playlist.” |
| “We’re skipping a long lecture block because you already met this material; recall will tell us what’s actually usable.” | “Module 2 unlocked.” |

### Order

| Good | Bad |
|------|-----|
| “Example first, then you try — so the legal steps are visible before independent work.” | “Step 2 of 5.” |
| “We’re going back to the example because the last two attempts used the wrong condition — that’s how we fix it.” | “Failed — restart mission.” |

### Long-term contribution

| Good | Bad |
|------|-----|
| “Short reflection now helps you notice what is still uncertain before next revision.” | “Reflect to earn mastery points.” |
| “Targeted practice on this weak step beats doing ten mixed questions you already get right.” | “More questions = more progress.” |

### Adaptation / escalation

| Good | Bad |
|------|-----|
| “You’re fading, so we’ll close with a brief summary of what we covered and leave heavier practice for when focus returns — today’s goal isn’t changing mid-sitting by stealth.” | Silent switch to a random easier topic. |
| “We can’t honestly continue today’s dense practice in the time left — we’ll ask today’s coaching to reshape the day.” | Pretend the day completed as planned. |

---

## 9. Relationship to Daily Coach Explainability

| Layer | Explains |
|-------|----------|
| **Daily Coach explainability** | Why *this* is today’s educational priority under the Study Plan |
| **Session explainability (this doc)** | Why *this sitting* is composed, ordered, and adapted to pursue that priority |

Session speech must not contradict Daily Coach rationale. It **specialises** it into method.

---

## 10. Cross References

| Document | Relationship |
|----------|----------------|
| [`LEARNING_SESSION_MODEL.md`](LEARNING_SESSION_MODEL.md) | Constitutional overview |
| [`SESSION_STRUCTURE.md`](SESSION_STRUCTURE.md) | Phases being explained |
| [`SESSION_TRANSITIONS.md`](SESSION_TRANSITIONS.md) | Transition warrants to narrate |
| [`SESSION_ADAPTATION.md`](SESSION_ADAPTATION.md) | Adaptation / escalation disclosure duties |
| [`../daily_coach/DAILY_COACH_EXPLAINABILITY.md`](../daily_coach/DAILY_COACH_EXPLAINABILITY.md) | Parent day explainability |
| [`../EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../EDUCATIONAL_EXPLAINABILITY_STANDARD.md) | EIP-003 four-question framework |
