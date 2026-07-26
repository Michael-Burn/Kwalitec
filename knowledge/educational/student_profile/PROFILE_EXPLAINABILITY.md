# Profile Explainability

**Programme:** VI — Master Planner  
**Milestone:** MS002 — Student Educational Profile Model  
**Classification:** Explainability contract for educational diagnosis  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how future versions of Kwalitec must explain the **Student Educational Profile** in plain language.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` (EIP-003)
3. `STUDENT_EDUCATIONAL_PROFILE.md`
4. `PROFILE_STATES.md`
5. `PROFILE_DIMENSIONS.md`
6. `planning/PLANNING_EXPLAINABILITY.md` (sibling contract for plans — do not collapse)

> **Explainability improves understanding of diagnosis already authorised.  
> It never invents educational certainty.**

Students should understand **why Kwalitec believes they are in a particular educational state**.

---

## 1. Purpose

A Profile that cannot be explained is not fit for a trust-based coach.

Diagnosis explainability ensures that state labels, risk language, and dimension summaries remain intelligible, honest about claim types, and free of internal machinery.

Planning explainability (MS001) justifies *what the plan asks*.  
Profile explainability (MS002) justifies *who the system thinks the student is educationally*.

---

## 2. Profile Explainability Principles

1. **Every material state assignment explains itself.** Primary states and At Risk overlays are material.
2. **One primary educational reason** per diagnosis surface — not a dump of every dimension.
3. **Facts and estimates stay distinct.** Coverage and calendar are plain; understanding and readiness are estimated or provisional.
4. **Soft signals are labelled subjective** when used.
5. **Uncertainty is named** under thin evidence or assumption-reliant profiles.
6. **Internal machinery stays invisible.** No twin facets, score vectors, registry IDs, or optimiser names.
7. **Non-punitive tone** for Recovering, Returning After Break, and At Risk.
8. **Growth is narratable.** Material evolution answers “what changed?”
9. **Advice does not masquerade as diagnosis.** “We recommend X” is planning/guidance; “You are in Revising” is diagnosis.
10. **Silence beats theatre.** Prefer understated states when warrant is thin.

---

## 3. Four-Question Contract (Profile)

Every material Profile diagnosis surface must answer:

| # | Question | Profile-specific guidance |
|---|----------|---------------------------|
| 1 | **What** do we believe educationally? | Named state + one-sentence posture (e.g. “You’re building foundations on CM1”) |
| 2 | **Why** do we believe it? | One primary reason tied to dimensions/inputs (coverage level, practice evidence, runway, recovery) |
| 3 | **What does this mean for you next?** | Diagnostic implication only — not a full plan (e.g. “Focus stays on first-pass learning before heavy revision claims”) |
| 4 | **Known vs estimated?** | What is observed/derived vs provisional |

Optional fifth when relevant:

| # | Question | When required |
|---|----------|---------------|
| 5 | **What changed?** | After material evolution (mock, gap, recovery, date change, capacity re-intake) |

---

## 4. Claim Types in Profile Speech

| Claim type | Profile examples | Student cue |
|------------|------------------|-------------|
| Observed Fact | Exam date; declared weekly hours; topic marked studied; leave dates | Plain factual language |
| Derived Fact | Coverage %; days remaining; missed-week count | Plain derived measure |
| Evidence-backed Estimate | “Estimated weaker on topic X from recent practice”; provisional Exam Ready | *Estimated* / *Provisional* / *Suggested* |
| Soft / Subjective | “You reported low confidence”; motivation check-in | *You reported* / *It sounds like* |
| Educational Advice | Optional next emphasis (belongs more to guidance/planning) | *Recommended* / *Optional* — must not rewrite state as command |

Forbidden speech patterns:

- “You have mastered this” from coverage alone
- “You are ready” without provisional/estimate framing when warrant is incomplete
- “Our model scored you 0.73” or twin/optimiser jargon
- “You failed because you lack discipline” for At Risk / missed study
- Presenting assumptions as observed facts

---

## 5. State Explanation Templates

Templates are educational contracts for future copy — not final UI strings.

### Beginning Study

- **What:** You’re at the start of preparation for [exam].
- **Why:** Little or no syllabus coverage is recorded yet for this sitting.
- **Next meaning:** We’ll establish foundations before treating practice or revision as the main story.
- **Known vs estimated:** Starting position known from intake; understanding not yet evidenced.

### Building Foundation

- **What:** You’re building foundations through first-pass study.
- **Why:** Coverage is growing on early/core syllabus units; learning posture still dominates.
- **Next meaning:** Keep sequential study honest; practice may appear, but coverage isn’t competence yet.
- **Known vs estimated:** Coverage observed/derived; understanding estimates thin unless practice evidence exists.

### Practising

- **What:** You’re practising applying what you’ve studied.
- **Why:** Recent study includes meaningful question practice on covered material.
- **Next meaning:** Results help us estimate strengths and weaknesses — still provisional.
- **Known vs estimated:** Practice outcomes observed; understanding estimated from them.

### Strengthening

- **What:** You’re strengthening areas that look shaky.
- **Why:** Practice evidence or foundation checks show uneven understanding on important topics.
- **Next meaning:** Reinforcement comes before treating progress as secure.
- **Known vs estimated:** Weaknesses estimated from evidence (or declared until evidenced).

### Revising

- **What:** You’re revising material you’ve already studied.
- **Why:** You’re returning to earlier topics to protect retention and deepen application.
- **Next meaning:** Revision consolidates — it doesn’t invent coverage you never studied.
- **Known vs estimated:** Revision activity observed; retention improvement estimated.

### Exam Preparation

- **What:** You’re in exam preparation — stabilising for the sitting.
- **Why:** Time remaining and revision substance point to final-approach posture.
- **Next meaning:** New first-pass expansion should stay tightly limited; focus on high-value consolidation.
- **Known vs estimated:** Calendar derived; readiness still provisional until Exam Ready warrant exists.

### Recovering

- **What:** You’re recovering your study trajectory.
- **Why:** Study was interrupted or intensity broke; you’re re-establishing a sustainable pace.
- **Next meaning:** Restart that still counts — we won’t pretend nothing was learned before.
- **Known vs estimated:** Gap and return observed; confidence/motivation may be subjective.

### Returning After Break

- **What:** You’re returning after a break.
- **Why:** A significant gap in study ended and you’re re-engaging.
- **Next meaning:** We’ll re-orient to your recorded coverage and check what may need refreshing.
- **Known vs estimated:** Gap observed; “rust” estimated until practice evidence updates.

### At Risk

- **What:** Your current path looks at risk for honest exam readiness under present time and capacity.
- **Why:** [One primary driver: remaining syllabus vs runway / reliability vs declared hours / foundation gaps / etc.].
- **Next meaning:** Strategy needs adjustment — this is a diagnosis, not a judgement of character.
- **Known vs estimated:** Calendar and coverage derived/observed; outcome risk is diagnostic posture, not a pass probability.

### Exam Ready

- **What:** On present evidence, preparation looks provisionally exam-ready.
- **Why:** Coverage, revision substance, and practice/assessment exposure support that judgement for now.
- **Next meaning:** Maintain revision and exam behaviour; readiness can change if evidence or time shifts.
- **Known vs estimated:** Always provisional / estimated — never a guarantee.

---

## 6. Dimension Explainability (When Surfaced)

If product surfaces individual dimensions, each material dimension needs a plain reason:

| Dimension | Good explanation pattern |
|-----------|--------------------------|
| Coverage | “You’ve marked X of Y syllabus units as studied.” |
| Understanding | “Estimated from recent practice on these topics — not from reading alone.” |
| Available time | “Based on the weekly hours you provided.” |
| Planning reliability | “Your completed study has been running below the hours you set — we should recalibrate.” |
| Educational confidence | “We have [limited/strong] practice evidence behind these estimates.” |
| Felt confidence | “You reported feeling … — separate from what practice shows.” |

---

## 7. Evolution Explainability (“What Changed?”)

When primary state or risk overlay changes materially, include:

1. **Trigger** — what educational event occurred (mock, missed weeks, recovery, date change).
2. **Before → after** — previous posture vs new posture in plain words.
3. **What did not change** — e.g. “Your earlier coverage still counts.”
4. **Claim hygiene** — restate known vs estimated after the change.

Example:

> “After three weeks without study, we’ve moved you to *Returning After Break*. Your earlier topic coverage still counts. We don’t yet have fresh practice evidence, so understanding estimates stay cautious until you practise again.”

---

## 8. Separation from Planning Speech

| Profile speech | Planning speech |
|----------------|-----------------|
| “You’re in Revising.” | “This month protects a revision window.” |
| “You’re At Risk because runway is short for remaining first-pass.” | “We recommend reducing new topics and extending revision — or changing sitting.” |
| “Understanding is estimated thin on Topic X.” | “The plan emphasises practice on Topic X in weeks 4–5.” |

Do not replace diagnosis with a schedule dump. Do not replace a plan explanation with only a state badge.

---

## 9. Accessibility of Diagnosis

Explainability requires that students can obtain:

1. Current primary educational state + plain meaning
2. Primary reason for that state
3. Clear known vs estimated distinction on readiness/understanding language
4. After material change — what changed

Internal dashboards for founders/ops may show richer dimension grids; student speech remains plain.

---

## 10. Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| State badge with no reason | Attach four-question contract |
| Readiness % without claim type | Use provisional language + drivers |
| Blaming tone for At Risk | Name capacity/time/evidence drivers |
| Soft confidence presented as proof | Label “you reported” |
| Plan copy pasted as profile diagnosis | Separate contracts |
| Machinery leaks | Rewrite in educational English |

---

## 11. Success Test

Profile explainability is compliant when a student can answer, without seeing internal scores:

1. What educational state does Kwalitec believe I’m in?
2. Why, in one clear reason?
3. What is known vs only estimated?
4. If my state changed recently — what changed, and what still counts?

---

## 12. Cross References

- `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` — platform speech law
- `planning/PLANNING_EXPLAINABILITY.md` — plan speech sibling
- `PROFILE_STATES.md` — state meanings
- `PROFILE_EVOLUTION.md` — change events
- `KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md` — student communication ladder
