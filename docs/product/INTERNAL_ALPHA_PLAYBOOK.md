# Internal Alpha Playbook

**Product:** Kwalitec Educational Intelligence  
**Epic:** Epic 4 — Capability 4.1  
**Status:** Product operations only  
**Audience:** Primary Internal Alpha operator (dogfooding)  
**Nature:** Operating manual — how to use Kwalitec daily, what to evaluate, and how to record findings  
**Journal:** [`docs/journal/001_INTERNAL_ALPHA_WEEK.md`](../journal/001_INTERNAL_ALPHA_WEEK.md)

This document does **not** specify architecture, implementation, or feature work. It explains how Internal Alpha should be run.

---

# 1. Purpose

## Why Internal Alpha exists

Epic 3 delivered the Educational Intelligence Platform foundations: Canonical Curriculum, Student Calibration, Birth Digital Twin, Durable Twin Persistence, Twin Retrieval, Educational Orchestrator, and Dashboard Integration.

Infrastructure alone does not prove the product. Internal Alpha exists to validate Kwalitec through **daily real-world study** — using the product as a student would, under ordinary conditions, and recording what is true in practice.

The goal is not to invent the next capability. The goal is to learn whether the product already helps a real learner study better, more calmly, and with greater trust.

## Two kinds of proof (keep them separate)

| Proving technology | Proving educational value |
|---|---|
| Does the system start, persist, retrieve, and present correctly? | Does the recommendation improve today's study? |
| Does the twin survive restart? | Does Calibration feel honest rather than theatrical? |
| Does the dashboard show the expected state? | Is the study flow clear enough to act without hesitation? |
| Is the product reliable enough to use every day? | Would you trust this guidance again tomorrow? |

Both matter. Neither replaces the other.

- A reliable system that gives poor guidance has not earned educational trust.  
- Excellent guidance that disappears after restart has not earned operational trust.

Internal Alpha must prove **both** — and must record them as distinct findings.

---

# 2. Daily workflow

Use Kwalitec as part of a real study day. Prefer consistency over intensity. One honest session beats several rushed ones.

## Recommended routine

```
Open Dashboard
        ↓
Review Recommendation
        ↓
Study Session
        ↓
Record observations
        ↓
Journal
        ↓
Repeat
```

### Open Dashboard

Start from the Educational Dashboard. Treat it as the day's entry point — not a debug console.

Note the recommendation, explanation, and any twin/calibration signals the product surfaces. Ask: *Does this look like a calm start to study?*

### Review Recommendation

Before studying, judge the recommendation on its face:

- Does it name a sensible next focus?  
- Does the explanation make the choice understandable?  
- Does it respect what you already know about your own preparation?

Do not “fix” the recommendation by hunting for the answer you wanted. Record what the product actually offered.

### Study Session

Study for a planned duration using the recommendation as the day's guide. Prefer real syllabus work over product exploration.

Note friction that appears while studying: uncertainty about what to do next, loss of trust mid-session, or the need to leave the product to decide for yourself.

### Record observations

Immediately after the session — while memory is fresh — capture educational and technical notes (Sections 3 and 4). Separate facts from opinions. Prefer short, concrete sentences.

### Journal

Write the day's entry in [`docs/journal/001_INTERNAL_ALPHA_WEEK.md`](../journal/001_INTERNAL_ALPHA_WEEK.md). Fill Study Context, Recommendation, Study Flow, Educational Value, UI / Experience, and Reflection.

Blank fields mean the day was not recorded. Do not invent entries after the fact.

### Repeat

Return the next study day and run the same loop. Continuity is the experiment. Patterns only appear across days.

---

# 3. Educational observations

Evaluate the product as a learner, not as a builder.

## Recommendation quality

- Was today's recommendation appropriate for where you actually are?  
- Would a thoughtful tutor have suggested something similar?  
- Did the explanation help you accept or reject the advice with clear reasons?

## Calibration accuracy

- Did early guidance respect declared history (not starting from zero when you are not)?  
- Did Calibration feel like priors — or like the product claiming false certainty?  
- After a few days, does the product still feel aligned with your real preparation posture?

## Study flow

- Was it easy to move from recommendation into actual study?  
- Where did friction appear: deciding, starting, continuing, or finishing?  
- Did the product reduce decision load, or add it?

## Clarity

- Did you understand what to do next without decoding jargon?  
- Were explanations honest about uncertainty?  
- Anything confusing that should have been obvious?

## Trust

- Did you feel guided, or managed?  
- Did anything feel misleading, overconfident, or hollow?  
- Would you rely on tomorrow's recommendation without second-guessing the system first?

## Usefulness

- Did using Kwalitec improve today's study compared with studying without it?  
- What would you miss if the product were unavailable tomorrow?  
- What would you ignore even if it remained available?

Record educational observations as lived experience. Do not convert them into redesign proposals in the journal.

---

# 4. Technical observations

Evaluate whether the platform behaves as a dependable daily tool. Keep these notes separate from educational judgment.

## Persistence

- After studying or calibrating, does state remain available later the same day?  
- After leaving and returning, does the twin / recommendation context still reflect prior work?

## Restart behaviour

- After stopping and restarting the app (or the machine), does the product recover sensibly?  
- Does cold start feel honest, or does something silently reset?

## Responsiveness

- Do dashboard and recommendation surfaces feel fast enough for daily use?  
- Any waits that break study momentum?

## Reliability

- Did anything fail, error, or behave inconsistently during the session?  
- Same action, same inputs — same result?

## Dashboard correctness

- Does the dashboard show what you expect given today's twin and recommendation?  
- Any stale, missing, contradictory, or empty states that undermine trust?

Technical observations should describe what happened and when. Severity can be noted; solutions should not.

---

# 5. Recording findings

## Primary capture

Daily lived experience goes in:

[`docs/journal/001_INTERNAL_ALPHA_WEEK.md`](../journal/001_INTERNAL_ALPHA_WEEK.md)

Use that journal for session context, recommendation judgment, study flow, educational value, UI notes, and one key reflection per day. At week's end, complete the Week Summary.

## Classification when something is wrong or surprising

When an observation is more than a soft reflection, classify it so later review stays clean. Use **one primary class** per finding.

| Class | Use when | Example shape |
|---|---|---|
| **Bug** | Behaviour is incorrect, broken, or inconsistent with known expected behaviour | Persistence lost after restart; dashboard shows the wrong recommendation |
| **Educational issue** | Guidance, Calibration honesty, or learning value is weak or misleading | Recommendation ignores declared Core Reading; explanation feels overconfident |
| **UX issue** | Flow, clarity, or interaction friction hurts use without proving a logic failure | Hard to start the session; wording is ambiguous; unfinished-feeling surface |
| **Architecture issue** | A structural limitation repeatedly blocks educational or operational trust | Same class of failure across days that cannot be explained as a single defect |

## Recording discipline

- Write the observation first; classify second.  
- Prefer evidence over speculation (“what I saw” before “why I think”).  
- Note date, study context, and whether the issue blocked study.  
- Do not turn the journal into a backlog. Directions may appear in the Week Summary only as ideas worth exploring later — not as tasks.  
- Do not file the same soft feeling four times under different classes.

If unsure between classes, choose the narrowest honest label (usually Bug, Educational issue, or UX issue). Reserve Architecture issue for recurring structural patterns, not first impressions.

---

# 6. Do NOT optimise too early

A single uncomfortable session is data. It is not a mandate to redesign the platform.

## Why restraint matters

- Early use is noisy: familiarity, mood, and syllabus pressure all colour judgment.  
- One-off bugs can look like deep design flaws until reproduced.  
- Immediate “fixes” burn attention that should stay on daily learning and pattern detection.  
- Architecture change during Alpha converts an observation programme into a rebuild programme.

## What to do instead

1. Record the observation accurately.  
2. Continue the daily workflow.  
3. Watch for recurrence across days and contexts.  
4. At week summary (and later Alpha reviews), group findings by pattern — not by emotion.

## Pattern threshold (practical rule)

Treat something as a candidate for later product attention only when it:

- appears more than once across days, **or**  
- clearly blocks study on a single day and would block others the same way, **and**  
- remains after honest re-check (not a misread of the UI or a one-time environment glitch).

Until then: journal, classify, continue.

Internal Alpha succeeds when learning compounds. Premature optimisation resets the experiment.

---

# 7. Exit criteria

Do **not** invite additional alpha users until the following are true.

## Educational readiness

- At least one full week of daily journal entries exists (`001_INTERNAL_ALPHA_WEEK.md` complete through Day 7 and Week Summary).  
- Recommendation quality is mostly appropriate across the week (not perfect — but not routinely wrong or misleading).  
- Calibration feels honest: priors respected; no false mastery theatre.  
- Study flow is usable without constant operator interpretation.  
- Trust is net-positive: you would recommend a careful peer try the product for real study.

## Operational readiness

- Persistence and restart behaviour are good enough for another person to return day-to-day without losing critical state.  
- Dashboard correctness is stable enough that wrong or empty states are rare, understood, and recorded — not the normal experience.  
- Known Bugs that block study have been identified and either resolved or clearly documented as temporary operator-only limitations.  
- Findings from the week are classified (Bug / Educational / UX / Architecture) so onboarding others does not rely on tribal memory.

## Process readiness

- This playbook has been followed for daily use (not only read once).  
- Week Summary names biggest strengths, pain points, and surprises without converting them into an implementation plan.  
- There is a clear statement that Internal Alpha is ready for a small additional cohort — or an explicit statement that it is not, with the blocking patterns listed.

## What exit criteria are not

Exit criteria are **not** “feature complete,” “architecture redesigned,” or “all journal pain points fixed.”

They are the minimum conditions under which inviting another person is responsible: the product is educationally useful enough, operationally stable enough, and observationally documented enough that new users add signal instead of noise.

---

**End of Internal Alpha Playbook.**  
Operate the product. Record the truth. Optimise only after patterns are clear.
