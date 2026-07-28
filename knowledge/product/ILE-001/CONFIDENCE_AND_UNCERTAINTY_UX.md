# Confidence and Uncertainty UX

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Version:** 1.0  
**Status:** Design  
**Effective:** 2026-07-28  
**Related programme:** ILE-005 (deeper Confidence & Uncertainty Experience) — ILE-001 defines assessment-time contracts that ILE-005 may extend globally  

---

## Purpose

Define how Adaptive Assessment communicates **uncertainty** and works with **learner confidence** so students understand:

- Why Kwalitec is unsure  
- How uncertainty can be reduced  
- What evidence is missing  

**Never overstate confidence.**

---

## Product stance

Confidence labels and provisional knowledge estimates are **features**, not defects (Product Principles — Respect uncertainty).

Coverage ≠ understanding. A completed check ≠ mastery. A high feeling of readiness ≠ exam guarantee.

---

## What students should always be able to see

| Question | UX obligation |
|---|---|
| **Why is Kwalitec unsure?** | Name the cause in plain language (examples below) |
| **How can uncertainty shrink?** | Point to a lawful next action (study, recovery, another check later, revision) |
| **What evidence is missing?** | Say what kind of evidence would help — not a vague “do more” |
| **How sure are we right now?** | Bounded language: provisional / emerging / stronger evidence — never fake precision |

---

## Why we might be unsure (student language)

| Cause | Plain framing |
|---|---|
| Thin evidence | “We haven’t seen much from you on this yet.” |
| Single check only | “One check isn’t enough to call this solid.” |
| Conflicting signals | “Recent answers point in different directions.” |
| Time since last evidence | “It’s been a while — this may have faded.” |
| Assisted success (hints) | “Hints were used — we’ll treat this carefully.” |
| Incomplete session | “This check wasn’t finished, so evidence is partial.” |
| Prerequisite doubt | “A foundation idea still looks shaky.” |

Avoid internal labels: thin_evidence_flag, ObservationKind, etc.

---

## How uncertainty can be reduced (student language)

| Path | Framing |
|---|---|
| Focused study / practice | “Study this idea, then we can check again.” |
| Recovery path | “Rebuild the foundation, then verify gently.” |
| Spaced revision | “Revisit after some time to test durability.” |
| Confirmation check later | “A careful check after practice strengthens evidence.” |
| Clarifying check | “A short check can resolve mixed signals.” |

Never: “Answer more questions until the score turns green.”

---

## Confidence prompts (self-report)

### When to use

- Confidence Check sessions (primary)  
- Sparse optional prompts in Deep / Readiness when pedagogically useful  
- Avoid forcing on every Quick Check item by default  

### Interaction rules

| Rule | Detail |
|---|---|
| Optional | Skip without penalty |
| Simple scale | Small discrete scale or plain labels (e.g. unsure / somewhat sure / sure) |
| Timing | Before answer, after answer, or both — choose one pattern per session type and keep it stable |
| Non-theatrical | No dramatic “confidence meter” gamification |

### Calibration outcomes (narrative, not scores-as-identity)

| Pattern | Student framing |
|---|---|
| Aligned | “Your confidence matched what this check showed.” |
| Overconfident | “You felt sure; the evidence looks weaker — useful to know before the exam.” |
| Underconfident | “You felt unsure; the evidence looks stronger — the knowledge may still feel fragile.” |

Follow with: what would reduce remaining uncertainty.

---

## System confidence (product belief)

Separate **student-felt confidence** from **system provisional belief**.

| Do | Do not |
|---|---|
| Say “evidence is limited / mixed / stronger” | Show pseudo-precise 73.2% mastery as fact |
| Tie language to Explainability Standard honesty | Claim “Exam Ready” from formative checks |
| Update belief only via Reasoning path | Let the assessment UI invent a second confidence number |

Visualisations, if any, must encode bands and uncertainty — not false precision. Prefer words + simple ordinal cues over dashboard gauges during the check itself.

---

## Never overstate confidence — hard rules

1. Do not declare mastery from a single Adaptive Assessment session.  
2. Do not hide conflict or incompleteness behind a cheerful summary.  
3. Do not imply human invigilation or credential value for formative checks.  
4. Do not convert readiness checks into pass predictions.  
5. Do not use green UI states that students will read as “guaranteed competence.”  
6. Marketing and in-product speech must match Learning Mode truth.

---

## Placement in the check flow

| Phase | Uncertainty UX |
|---|---|
| Before | Why we need evidence now; what is currently unsure |
| During | Optional confidence; calm progress; no precision theatre |
| Immediately after | What we learned; what remains unsure; how to reduce it; next action |
| Long after | Readiness / insights remain labelled provisional where appropriate |

---

## Emotional register

| Context | Tone |
|---|---|
| Overconfidence discovery | Matter-of-fact and protective — not “gotcha” |
| Underconfidence | Encouraging without inventing mastery |
| High uncertainty early on | Orient and invite evidence — never invent competence |
| Pre-exam | Honest and bounded — no false reassurance |

---

## Relationship to ILE-005

ILE-001 owns assessment-time confidence/uncertainty contracts.  
ILE-005 may generalise patterns across Home, readiness, and timeline. Until then, Adaptive Assessment must already obey “never overstate confidence.”

---

## Success criterion

A student can say:

> “I know what Kwalitec is still unsure about, why, and what would make it clearer — and it didn’t pretend to be more certain than it is.”

---

**End of CONFIDENCE_AND_UNCERTAINTY_UX**
