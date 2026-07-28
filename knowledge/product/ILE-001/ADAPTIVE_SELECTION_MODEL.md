# Adaptive Selection Model

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Version:** 1.0  
**Status:** Design  
**Effective:** 2026-07-28  

---

## Purpose

Describe how the **certified Educational Intelligence Platform** informs *what kind of check* and *what educational intent* selection should serve.

This document specifies **educational intent and product behaviour**. It does **not** specify implementation algorithms, scoring formulas, item-response models, or ranking math.

Selection remains deterministic and explainable at the product layer: same educational inputs → same lawful intent. Engineering milestones may implement policy behind services without inventing a second reasoning authority.

---

## Core idea

Adaptive Assessment does not “pick hard questions because AI said so.”

It **targets uncertainty and learning need** already visible (or legally inferable) in Educational State, then delivers an instrument whose observations can lawfully update that state.

```
Twin belief + curriculum position + mission context + time budget
        ↓
Educational intent (why check)
        ↓
Session type (how the check feels)
        ↓
Question selection policy (what items, within bounds)
        ↓
Observations → Reasoning → Twin (platform path)
```

Experience owns framing and delivery quality. **Reasoning** owns educational meaning of outcomes. **Mission** owns whether a check belongs in today’s commitment.

---

## Inputs the platform already provides (conceptual)

| Input family | What it informs | Student-facing translation |
|---|---|---|
| **Thin / missing evidence** | Diagnostic or exploration need | “We don’t have much evidence yet on this.” |
| **Unstable or provisional mastery confidence** | Confirmation / verification need | “This still looks uncertain — a careful check helps.” |
| **Gaps / misconception tags** | Weak-topic or recovery need | “We’ll check the idea that needs rebuilding.” |
| **Conflicting evidence** | Clarifying check; avoid overclaim | “Recent signals disagree — let’s clarify.” |
| **Spaced revision due / decay risk** | Revision verification | “Time to see what still holds.” |
| **Study gap / stale evidence** | Recovery after inactivity | “After a break, we restart gently.” |
| **Exam proximity + readiness uncertainty** | Readiness / confidence check | “Guides last focus — not a result prediction.” |
| **Plan / Mission time budget** | Session length and depth | “Fits today’s available time.” |
| **Recent assessment density** | Whether to suppress another check | “We’ll study instead of another check today.” |
| **Curriculum order & prerequisites** | Lawful topic scope | Syllabus-honest scope, not a private syllabus |
| **Burnout / pacing signals** | Soften or defer assessment | Protect sustainable progress |

The experience layer **consumes** these signals as product context. It must not re-implement Educational Reasoning to invent alternate mastery conclusions.

---

## Educational intents (selection goals)

| Intent | Goal | Typical session type |
|---|---|---|
| **Locate unknowns** | Find where understanding is thin | Quick Check / Recovery Check |
| **Confirm understanding** | Strengthen evidence before firmer language | Deep Check |
| **Test durability** | Check retention after time | Revision Check |
| **Clarify conflict** | Resolve disagreeing signals | Quick or Deep Check (narrow scope) |
| **Calibrate confidence** | Align feeling vs evidence | Confidence Check |
| **Verify recovery** | See if foundation repair held | Recovery Check |
| **Guide final focus** | Honest pre-exam prioritisation | Readiness Check |

One session, one primary intent. Secondary intents (e.g. light calibration) may appear only if they do not confuse the frame.

---

## Adaptation dimensions (product behaviour)

Adaptation means adjusting along these **explainable** dimensions — not opaque difficulty churn:

1. **Whether** a check appears (Mission eligibility + density + burnout gates).  
2. **Why** it appears (intent above — shown to the student).  
3. **How long** it runs (session type + time budget).  
4. **Where** in the syllabus it focuses (Twin + curriculum constraints).  
5. **Mix** of confirmation vs exploration (policy — see `QUESTION_SELECTION_POLICY.md`).  
6. **When to stop** early (enough evidence for the intent, time exhausted, or student exits).

Difficulty may vary **within** an intent only when it serves evidence quality (e.g. confirmation needs careful items). Difficulty must never be used as punishment or engagement bait.

---

## What “adaptive” must never mean here

| Forbidden meaning | Why |
|---|---|
| Hidden LLM chooses items without explainable intent | Deterministic cores; educational honesty |
| Endless personalisation of tone that changes educational authority | Fairness and predictability |
| Adaptive = always harder after mistakes | Motivation harm; confuses recovery with penalty |
| Adaptive = maximise questions until fatigue | Quality over quantity |
| Experience layer writes mastery directly | Twin / Reasoning authority |

---

## Explainability contract for selection

Every Adaptive Assessment session must be able to answer:

| Question | Source of answer |
|---|---|
| What should I do? | Session type + start CTA |
| Why this, now? | Educational intent tied to Twin/Mission context |
| What happens next? | Continue Mission / recovery / revise — from decided next action |
| What is uncertain? | Stated before and after; never erased by a decorative score |

Internal engine ids, graph jargon, and pipeline names stay out of student speech.

---

## Relationship to AP-002 triggers

AP-002 Mission Integration already names trigger classes (diagnostic, revision, checkpoint, adaptive, recovery, mastery verification). ILE-001 maps those to **learner journeys and session types** without changing trigger authority:

| AP-002-oriented trigger | ILE session emphasis |
|---|---|
| Diagnostic | Quick / Recovery Check — locate unknowns |
| Checkpoint | Daily learning check — Quick Check |
| Adaptive (unstable / conflict) | Clarifying Quick/Deep Check |
| Revision | Revision Check |
| Recovery | Recovery Check |
| Mastery verification | Deep / Readiness Check (confirmation) |

---

## Stopping rules (product)

Selection should prefer **enough evidence for the stated intent** over exhausting an item bank.

Stop or offer stop when:

- Intent satisfied (e.g. confirmation still uncertain → bridge to recovery rather than more identical probes)
- Time budget reached
- Student pauses or exits
- Over-assessment or burnout gate fires mid-construction (prefer study activity)

Incomplete sessions: see `FAILURE_AND_RECOVERY.md`.

---

## Implementation note (non-normative)

Future engineering milestones may encode these intents as deterministic policies and item filters. Those implementations must remain subordinate to Educational Reasoning and must not introduce a parallel “adaptive scorer” that contradicts Twin belief.

---

**End of ADAPTIVE_SELECTION_MODEL**
