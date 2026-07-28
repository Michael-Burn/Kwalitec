# Session Types — Adaptive Assessment

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Version:** 1.0  
**Status:** Design  
**Effective:** 2026-07-28  

---

## Purpose

Define **learner-facing** Adaptive Assessment session types: when each appears, how it feels, and what success looks like for the student.

Session types are product labels. Internal activity enums may differ; student speech uses these names (or softer synonyms such as “learning check”).

---

## Shared properties (all types)

| Property | Rule |
|---|---|
| Framing | Purpose visible before first item |
| Effort estimate | Shown (e.g. minutes or item count band) |
| Exit | Pause / leave allowed; incomplete ≠ delinquency |
| Scoring culture | Evidence + next action — no identity marks |
| Authority | Observations only; Reasoning interprets; Twin stores belief |
| Chrome | Study-session continuity — not exam invigilation |

---

## 1. Quick Check

**Student meaning:** A short formative probe to keep today’s plan accurate.

| Aspect | Design |
|---|---|
| **Typical length** | ~3–8 minutes; few items |
| **Primary intents** | Daily checkpoint; light diagnostic; clarify a single uncertain idea |
| **When it appears** | Mid-mission; end of a study block; when time is tight but evidence is needed |
| **When it must not appear** | As a substitute for teaching when the student has never studied the topic; when assessment density is already high |
| **Feeling** | Lightweight, optional-within-mission, low stakes |
| **Success** | Student finishes without anxiety; Twin gains usable observation(s); next action clear |

**Illustrative frame:** “Quick check — helps keep today’s plan accurate.”

---

## 2. Deep Check

**Student meaning:** A careful confirmation of understanding — still formative, not an exam.

| Aspect | Design |
|---|---|
| **Typical length** | ~10–20 minutes; more items or richer items |
| **Primary intents** | Knowledge confirmation; resolve conflicting evidence; stronger evidence before firmer language |
| **When it appears** | After substantial study on an objective; when Twin requests denser evidence; when Mission time budget explicitly allows |
| **When it must not appear** | On return-from-gap day one; under burnout flags; when only a Quick Check is needed |
| **Feeling** | Focused, respectful of effort, still non-punitive |
| **Success** | Clearer belief about solidity vs remaining uncertainty; no “pass/fail” identity |

**Illustrative frame:** “Careful check on this topic — no grades, clearer next steps.”

---

## 3. Recovery Check

**Student meaning:** A gentle re-entry or foundation check after struggle or time away.

| Aspect | Design |
|---|---|
| **Typical length** | Short to moderate; cognitive load kept low |
| **Primary intents** | Post-inactivity reorientation; verify recovery path foundation; soft diagnostic after setback |
| **When it appears** | Long study gap; after recovery teaching steps; when Twin evidence is stale |
| **When it must not appear** | As a high-pressure readiness battery; immediately after a failed Deep Check without teaching in between |
| **Feeling** | Welcoming, patient, dignity-preserving |
| **Success** | Honest restart; Mission prioritises re-orientation; motivation protected |

**Illustrative frame:** “Gentle check to restart accurately — take your time.”

---

## 4. Confidence Check

**Student meaning:** A check that pays special attention to how sure you feel versus what you show.

| Aspect | Design |
|---|---|
| **Typical length** | Short; confidence prompts are first-class but optional where anxiety risk is high |
| **Primary intents** | Confidence calibration; surface over/under-confidence |
| **When it appears** | Calibration mismatch signals; student-requested; companion to pre-exam focus (with honest bounds) |
| **When it must not appear** | Every daily session by default; as a forced psychometric battery |
| **Feeling** | Curious, non-judgemental |
| **Success** | Student understands alignment/misalignment and what evidence would change it |

**Illustrative frame:** “Confidence check — helps align how sure you feel with what the evidence shows.”

---

## 5. Revision Check

**Student meaning:** See what still holds from earlier learning.

| Aspect | Design |
|---|---|
| **Typical length** | Short to moderate; spaced items across due topics (breadth-aware) |
| **Primary intents** | Durability / forgetting-risk verification |
| **When it appears** | Revision due; stability uncertain; scheduled revisit in Mission |
| **When it must not appear** | As first contact with never-studied material; as last-minute cram theatre without syllabus honesty |
| **Feeling** | Normalised forgetting; professional spaced practice |
| **Success** | Clear hold / reinforce / recover bridge; revision adherence without shame |

**Illustrative frame:** “Revision check — see what still feels solid.”

---

## 6. Readiness Check

**Student meaning:** An honest sample to guide remaining study — not a predicted exam result.

| Aspect | Design |
|---|---|
| **Typical length** | Moderate; syllabus-weighted within time budget |
| **Primary intents** | Pre-exam focus; topic-scoped readiness honesty; optional confirmation at sitting-phase gates |
| **When it appears** | Near exam date; student requests readiness insight; Mission offers bounded readiness activity |
| **When it must not appear** | Early first-learn phase as “are you exam ready?”; with pass-guarantee language |
| **Feeling** | Serious, calm, bounded honesty |
| **Success** | Prioritised focus list; explicit non-guarantee; trust preserved |

**Illustrative frame:** “Readiness check — guides what to study next; it does not predict your result.”

---

## Appearance matrix (summary)

| Session type | Daily Mission | After gap | Near exam | Weak topic | Revision due |
|---|---|---|---|---|---|
| Quick Check | Common | Rare (prefer Recovery) | Possible (micro) | Common | Possible |
| Deep Check | Occasional | Avoid early | Possible (topic) | Occasional | Rare |
| Recovery Check | If recovering | Common | Rare | If verifying repair | Rare |
| Confidence Check | Occasional | Optional soft | Companion | Optional | Optional |
| Revision Check | When due | After re-entry stabilises | Possible | If weak+due | Common |
| Readiness Check | Rare | Avoid | Common | Topic-scoped possible | Possible |

---

## Naming and synonyms

Prefer in UI: **Quick Check**, **learning check**, **today’s check**.  
Avoid: quiz bowl, pop quiz, exam mode, mock exam (unless a future consented exam-simulation programme).

Internal Founder analytics may retain engineering names; students should not see them.

---

## Mixing types

Do not chain multiple session types in one sitting unless Mission explicitly sequences them with clear frames (e.g. short teaching → Recovery Check). Default: **one type per assessment segment**.

---

**End of SESSION_TYPES**
