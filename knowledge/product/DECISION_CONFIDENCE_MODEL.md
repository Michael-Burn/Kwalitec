# Decision Confidence Model

**Programme:** ILE-011 — Student Decision Framework  
**Version:** 1.0  
**Status:** Active — permanent evidence-before-guidance model  
**Effective:** 2026-07-28  
**Companion:** [`STUDENT_DECISION_FRAMEWORK.md`](STUDENT_DECISION_FRAMEWORK.md), [`DECISION_CATALOGUE.md`](DECISION_CATALOGUE.md)  
**Related:** ILE-001 [`CONFIDENCE_AND_UNCERTAINTY_UX.md`](ILE-001/CONFIDENCE_AND_UNCERTAINTY_UX.md); P-001.2 Explainability Standard  

---

## Purpose

Define **how much evidence is required** before Kwalitec offers guidance, and how the product should behave at each level.

This is a product confidence model for *decision support*. It does **not** specify internal score formulas, Twin mathematics, or UI widgets.

**Hard rule:** Never expose internal confidence mathematics, raw model scores, or engineering labels to learners.

---

## Levels

| Level | Intent | Guidance stance |
|---|---|---|
| **Insufficient evidence** | Cannot warrant educational advice | Silence, wait, or ask a clarifying question |
| **Observation only** | System is watching; no interpretive claim yet | No recommendation; optional neutral status (“we’re still gathering evidence”) |
| **Emerging confidence** | Soft signal exists; still provisional | Soft tips, questions, labelled uncertainty — not firm primary commands |
| **Reliable guidance** | Evidence supports a primary recommendation | Single explainable primary tip allowed |
| **High confidence** | Strong, consistent evidence; still not certainty | Strong recommendation / firm honesty allowed; never guarantee outcomes |

Levels are **qualitative product states**, not percentages. Implementation programmes may map internal signals onto these levels later without changing this document’s learner-facing contracts.

---

## Level definitions

### Insufficient evidence

**When:** Missing plan inputs, no relevant attempts, conflicting signals unresolved, stale state with no recovery observation, or decision out of educational scope.

**Learner-facing behaviour:**

- Do not invent a primary recommendation.
- Prefer silence or “not enough yet” with what evidence would help.
- May ask one clarifying question if it unlocks lawful guidance (e.g. exam date, available time).
- Never imply certainty by filling the screen with tips.

### Observation only

**When:** Lawful instruments are collecting data (session in progress, first check incomplete, new topic just opened) and interpretation would overclaim.

**Learner-facing behaviour:**

- Support the authorised activity without competing advice.
- Optional quiet status: evidence is being gathered.
- No ranking claims, readiness grades, or revision urgency.
- Waiting is respect (ILE-010).

### Emerging confidence

**When:** Some relevant evidence exists (partial coverage, single check, early Twin provisional state) but uncertainty remains high.

**Learner-facing behaviour:**

- Soft suggestions with explicit provisional language.
- Prefer questions when alternatives are close.
- Explain what is uncertain and how to strengthen evidence.
- Do **not** use “strongly recommend” framing.
- Suitable for gentle pacing tips, optional checks, reflective summaries.

### Reliable guidance

**When:** Evidence is coherent enough for a primary next action: plan focus, curriculum position, and recent observations align; explainability can be satisfied.

**Learner-facing behaviour:**

- One primary recommendation (what / why / what next / what is uncertain).
- Student may accept, defer, or dismiss without penalty.
- Secondary tips only if lawfully labelled and non-conflicting.
- Default level for Daily Mission and “study next” craft.

### High confidence

**When:** Multiple consistent observations support the same educational conclusion (e.g. clear prerequisite blocker; sustained overload; strong spacing warrant on a studied high-weight topic). Uncertainty is still acknowledged.

**Learner-facing behaviour:**

- Firm, calm language (“this should be today’s focus”).
- Still no pass/fail guarantees, career decisions, or exam booking.
- Still show what could change the conclusion.
- Use sparingly — overuse destroys trust.

---

## Evidence before guidance (minimums)

Guidance strength may not exceed evidence strength.

| Desired behaviour | Minimum level |
|---|---|
| Neutral observation / wait | Observation only or Insufficient |
| Clarifying question | Insufficient or Emerging |
| Soft tip / optional alternative | Emerging |
| Primary recommendation | Reliable |
| Strong recommendation | High (or Reliable + wellbeing/safety urgency per Responsibility Matrix) |
| Outcome guarantee | **Never** — no level authorises this |

When catalogue entries require a threshold, they refer to these levels.

---

## Learner-facing language (patterns)

Use bounded, human language. Examples — not copy-locked strings:

| Level | Pattern |
|---|---|
| Insufficient | “We don’t have enough yet to recommend a focus.” |
| Observation only | “Finish this check — then we can update what we know.” |
| Emerging | “Early signs point to Topic X, but this is still provisional.” |
| Reliable | “Today’s highest-value focus is Topic X because …” |
| High | “The evidence is consistent: rebuild foundation Y before moving on.” |

Avoid: fake percentages, “99% ready,” green/red destiny meters as sole guidance, internal enum names.

---

## Relationship to explainability

| Level | Explainability obligation |
|---|---|
| Insufficient / Observation | Explain *why* guidance is withheld or deferred |
| Emerging | Explain provisional basis + uncertainty |
| Reliable / High | Full what / why / next / uncertain (P-001.2 default) |

If explainability cannot be met, **downgrade** the effective level (speak less), never invent prose to cover missing warrant.

---

## Relationship to Educational Intelligence

This model constrains *when* to speak. It does **not** create a second educational brain.

- Ranking, mastery, and readiness meaning remain owned by certified Educational Intelligence.
- Product surfaces map intelligence outputs onto confidence levels for guidance behaviour.
- Docs-only until implementation programmes wire mappings under existing architecture.

---

## Evaluation questions

1. What level does the evidence actually support — not what the empty UI wants?
2. Are we about to speak stronger than the level allows?
3. Would admitting uncertainty build more trust than a tip?

---

**End of DECISION_CONFIDENCE_MODEL**
