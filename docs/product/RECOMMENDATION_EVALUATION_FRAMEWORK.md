# Recommendation Evaluation Framework

**Product:** Kwalitec Educational Intelligence  
**Epic:** Epic 4 — Capability 4.1  
**Version:** 1.0  
**Status:** Evaluation framework only  
**Audience:** Internal Alpha operator and product reviewers  
**Companions:**
- Operating manual — [`INTERNAL_ALPHA_PLAYBOOK.md`](INTERNAL_ALPHA_PLAYBOOK.md)
- Daily journal — [`docs/journal/001_INTERNAL_ALPHA_WEEK.md`](../journal/001_INTERNAL_ALPHA_WEEK.md)

This document does **not** specify architecture, algorithms, implementation, or Educational Intelligence redesign. It defines how Internal Alpha evaluates whether recommendations help students learn.

---

# 1. Purpose

## Why recommendation quality must be measured

Epic 3 made recommendations generable from a persistent Digital Twin. That proves the platform can produce guidance. It does not prove the guidance helps a student learn.

Internal Alpha exists to answer a different question:

> Did today’s recommendation improve study — calmly, honestly, and in a way worth trusting again tomorrow?

Without a shared evaluation frame, daily notes stay anecdotal. Soft discomfort looks like a bug. One good day looks like product success. Patterns never become backlog with clear ownership.

This framework exists so that:

1. **Educational value is judged separately from technical reliability.** A correct twin and a poor suggestion are different findings.  
2. **Student perception and developer observation stay distinct.** Feeling wrong is not the same as logging wrong.  
3. **Failures are classified before they are “fixed.”** Poor explanation is not the same backlog shape as poor calibration or a platform bug.  
4. **Improvement is deliberate.** Findings become backlog only after evidence and classification — not after a single uncomfortable session.  
5. **Version 1.0 has a minimum quality bar.** “Shipable enough for careful peers” is defined, not vibes.

The objective of Capability 4.1 is evaluation discipline — not smarter ranking, denser scores, or a new recommendation engine.

---

# 2. Educational dimensions

Evaluate every recommendation against these six dimensions. Score lightly if useful (for example: strong / acceptable / weak / failed), but always write one concrete sentence of evidence per dimension that matters that day.

Do not invent composite scores. Do not average dimensions into a single “quality %.” Patterns across days matter more than any single number.

## 2.1 Relevance

**Question:** Was this the right kind of work for where the student actually is?

Evaluate whether the suggested focus matched declared preparation, recent study, and syllabus reality — not whether it matched a private wish list.

| Strong | Acceptable | Weak / failed |
|---|---|---|
| A thoughtful tutor would likely suggest something similar | Close enough to act without fighting the product | Wrong topic family, ignores obvious posture, or feels random |

## 2.2 Timing

**Question:** Was this the right work *now*?

Evaluate urgency and sequence: too early, too late, premature depth, or repeating work that should wait.

| Strong | Acceptable | Weak / failed |
|---|---|---|
| Fits today’s available energy and study window | Slightly early/late but still usable | Clearly mistimed relative to exam proximity, fatigue, or unfinished prerequisites |

## 2.3 Workload

**Question:** Was the implied effort honest and doable?

Evaluate duration, intensity, and cognitive load. A relevant topic with impossible scope still fails workload.

| Strong | Acceptable | Weak / failed |
|---|---|---|
| Scope matches a real session | Slightly heavy/light but adjustable by the student | Overwhelming, trivial, or silently assumes more time than available |

## 2.4 Progression

**Question:** Did the recommendation move learning forward?

Evaluate continuity across days: building on prior work, creating useful evidence, avoiding idle loops or fake advancement.

| Strong | Acceptable | Weak / failed |
|---|---|---|
| Clear next step on a coherent learning path | Neutral day — not harmful, limited growth | Regressive, circular, or theatrical progress that does not change readiness |

## 2.5 Clarity

**Question:** Could the student understand what to do without decoding the product?

Evaluate suggestion wording, explanation honesty, and whether next action is obvious.

| Strong | Acceptable | Weak / failed |
|---|---|---|
| One clear action; explanation makes acceptance/rejection easy | Understandable after a short re-read | Jargon-heavy, ambiguous, contradictory, or unexplained |

## 2.6 Trust

**Question:** Would the student rely on tomorrow’s guidance without first second-guessing the system?

Evaluate honesty about uncertainty, absence of preparedness theatre, and whether guidance felt supportive rather than manipulative.

| Strong | Acceptable | Weak / failed |
|---|---|---|
| Guided with confidence proportional to warrant | Mild doubt but still usable | Misleading, overconfident, hollow, or trust-breaking |

### Dimension discipline

- Judge dimensions from **lived study**, not from reading architecture docs.  
- A recommendation can fail one dimension and still be usable overall — record which one.  
- If several dimensions fail together, note the cluster; do not force a single root cause in the moment.

---

# 3. Student observations

Internal Alpha records how the recommendation landed for the learner. Capture these as student-facing outcomes — not as engineering hypotheses.

Primary home: the daily journal ([`001_INTERNAL_ALPHA_WEEK.md`](../journal/001_INTERNAL_ALPHA_WEEK.md)), under Recommendation / Educational Value / Reflection as appropriate.

## 3.1 Observation labels

Use **one primary student outcome** per recommendation day:

| Label | Meaning | Record when |
|---|---|---|
| **Matched expectations** | The suggestion aligned with what a prepared student reasonably expected next | You would have chosen something similar without the product |
| **Was useful** | You followed it (fully or partly) and study improved, or decision load dropped | The session was better *because* of the guidance |
| **Was ignored** | You saw it and chose not to follow it | Skip was deliberate — note why (wrong focus, timing, energy, distrust) |
| **Felt wrong** | The guidance produced discomfort, disbelief, or active resistance | Even if you later studied something else — the product’s advice felt incorrect or dishonest |

These labels are not mutually exclusive in lived experience, but the journal should still name a **primary** outcome. Secondary nuance belongs in the free-text note.

Examples of primary choice:

- Matched expectations *and* was useful → primary **Was useful** (expectation match is supporting evidence).  
- Matched expectations but you still ignored it → primary **Was ignored** (and say why).  
- Felt wrong even if you forced yourself to follow it → primary **Felt wrong**.

## 3.2 What to write (minimum)

For each study day that surfaces a recommendation, record:

1. **Date and study context** — subject/syllabus posture, available time, energy.  
2. **What was recommended** — the suggestion as shown (not a reconstructed ideal).  
3. **Primary student outcome** — one of the four labels above.  
4. **One evidence sentence** — what happened in study, not what should be rebuilt.  
5. **Dimensions touched** — which of relevance / timing / workload / progression / clarity / trust were notably strong or weak.

## 3.3 What not to do in student observations

- Do not convert “felt wrong” into an immediate redesign proposal.  
- Do not invent reasons the system “must have used.” Record perception.  
- Do not skip a day and backfill with reconstructed memory days later.  
- Do not treat a single ignored recommendation as proof the engine failed.

Student observations answer: *How did this land for learning?*

---

# 4. Developer observations

Developer observations are logged **separately** from student perception. They describe what the platform did, showed, or failed to do — not whether the student liked the advice.

Keep them in distinct journal fields or clearly marked technical notes (see playbook Section 4). Never merge “I didn’t trust it” with “state was lost after restart” into one sentence.

## 4.1 What belongs in developer observations

| Area | Capture |
|---|---|
| **Surface correctness** | Did dashboard / recommendation / explanation show consistent content for the same session? |
| **Persistence continuity** | Did twin/recommendation context survive leave-and-return and restart as expected for daily use? |
| **Timing of presentation** | Was the recommendation available when study started, or missing/stale/empty? |
| **Explainability artefacts** | Were reasons / warrant / honesty signals present, absent, contradictory, or clearly outdated? |
| **Reproducibility notes** | Same posture, same day context — same recommendation story, or surprising flip? |
| **Errors and anomalies** | Failures, blank states, contradictory panels, unexpected resets |
| **Operator workarounds** | Anything you did outside the intended student path to make study possible |

## 4.2 What does *not* belong here

- Educational taste (“I would have preferred topic X”).  
- Speculative root-cause architecture theories.  
- Implementation plans or patch sketches.  
- Re-scoring student outcomes as if they were telemetry.

## 4.3 Separation rule

| If the note is about… | Put it under… |
|---|---|
| Learning value, trust, usefulness, ignore/feel-wrong | Student observations |
| Correctness, persistence, errors, empty/stale UI, reproducibility | Developer observations |
| Both | Two notes — same day, two labels |

Developer observations answer: *Did the product behave as a dependable instrument while guidance was shown?*

---

# 5. Failure categories

When something is wrong or surprising beyond a soft reflection, classify with **one primary failure category**. Classification happens after the observation is written — not instead of it.

| Category | Use when | Typical signals | Not this if… |
|---|---|---|---|
| **Poor recommendation** | The suggested next work itself is educationally weak | Wrong relevance, bad timing, absurd workload, no progression | The suggestion was fine but the copy or UI confused you |
| **Poor explanation** | The suggestion might be defensible, but the narrative fails | Unclear why; overconfident warrant; contradictory reasons; missing honesty | You simply disagree with a clear, honest explanation |
| **Poor UX** | Interaction or presentation friction blocks use without proving bad educational logic | Hard to start, ambiguous layout, unfinished-feeling surface, copy noise | The advice is clearly wrong even when UX is calm |
| **Poor calibration** | Early priors or declared history are ignored, overstated, or theatrical | Starts from zero when it shouldn’t; false mastery; posture mismatch that tracks Calibration, not later evidence | Later evidence-based guidance is simply disagreeable |
| **Platform bug** | Behaviour is incorrect, broken, or inconsistent with expected product behaviour | Errors, lost state, wrong/stale recommendation shown, non-reproducible flips from glitches | You dislike a stable, consistently shown suggestion |

### Classification discipline

1. Write what happened.  
2. Choose the narrowest honest primary category.  
3. Note secondaries only if they are real and distinct (for example: Poor recommendation + Poor UX).  
4. Prefer **Platform bug** when correctness fails; prefer **Poor recommendation** when correctness holds but educational value fails.  
5. Prefer **Poor calibration** only when the failure tracks birth priors / declared history — not every disliked first recommendation.  
6. Do not file the same soft feeling under every category.

Aligned playbook classes map approximately as:

- Platform bug → Bug  
- Poor recommendation / Poor explanation / Poor calibration → Educational issue (with finer subtype here)  
- Poor UX → UX issue  

This framework’s categories are the recommendation-specific lens; the playbook remains the daily operating manual.

---

# 6. Improvement loop

Findings become product backlog only through a deliberate loop. Internal Alpha is an observation programme first.

```
Daily study
    ↓
Student + developer observations
    ↓
Failure classification (when needed)
    ↓
Pattern detection across days
    ↓
Candidate backlog item
    ↓
Prioritised review
    ↓
Scoped work (later epics / fixes)
```

## 6.1 From note to candidate

A finding may become a **candidate backlog item** only when at least one of the following is true:

- It **recurs** across multiple study days or contexts, **or**  
- It **blocks study** on a single day in a way that would block other careful users the same way, **and**  
- It **survives re-check** (not a misread UI, one-time environment glitch, or mood-only reaction).

Until then: journal, classify, continue. Do not optimise early (playbook Section 6).

## 6.2 Backlog item shape

When promoting a pattern, write a backlog candidate with:

| Field | Content |
|---|---|
| **Title** | Short, outcome-oriented (what fails for the student) |
| **Evidence** | Dates / journal references / recurrence count |
| **Primary failure category** | One of Section 5 |
| **Dimensions hit** | From Section 2 |
| **Student outcome pattern** | Matched / useful / ignored / felt wrong trend |
| **Developer notes** | Only facts that support reproducibility or correctness |
| **Proposed intent** | What “better” would mean educationally — not a design dump |
| **Non-goals** | Explicitly exclude algorithm rewrites unless evidence demands them later |

## 6.3 What the loop must not do

- Turn Day 1 discomfort into an epic.  
- Collapse student perception into “fix the model.”  
- Skip classification and jump to implementation.  
- Use backlog creation as a substitute for finishing the Alpha week.  
- Redesign Educational Intelligence selection while evaluation evidence is still thin.

## 6.4 Ownership of the loop

- **Operator** records daily observations and classifications.  
- **Week Summary / Alpha review** groups patterns.  
- **Product review** accepts or rejects backlog candidates.  
- **Engineering** receives only accepted, scoped items — outside this framework’s deliverable.

The improvement loop answers: *How does measured weakness become deliberate work — without burning the experiment?*

---

# 7. Version 1.0 recommendations

## Minimum acceptable recommendation quality

Version 1.0 does not require perfect tutoring. It requires guidance that a careful student can trust enough to study with, most days.

A recommendation set (across a representative Internal Alpha week) meets the **Version 1.0 minimum** when all of the following hold:

### 7.1 Educational floor

1. **Relevance is mostly acceptable or better** across the week — not routinely wrong or random.  
2. **Timing and workload are usable** on ordinary study days — recommendations may be imperfect, but they must not systematically demand impossible sessions or mistimed depth.  
3. **Progression is net-positive or neutral** — the week does not feel like a circular loop or fake advancement.  
4. **Clarity is good enough to act** without operator decoding for a peer user.  
5. **Trust is net-positive** — uncertainty is honest; no preparedness theatre as the normal mode; you would rely on tomorrow’s guidance without first assuming the product is bluffing.

### 7.2 Outcome floor

Across the week:

- **Was useful** (or matched expectations and led to productive study) is the common case — not the exception.  
- **Felt wrong** is rare, explained, and classified — not the default emotional response.  
- **Was ignored** may happen; repeated ignore for the same failure category is a pattern, not noise.  
- Student observations and developer observations both exist; educational judgment is not inferred only from uptime.

### 7.3 Failure floor

- **Platform bugs** that block study are identified and either resolved or explicitly documented as temporary operator-only limitations before inviting additional alpha users.  
- Recurring **Poor recommendation**, **Poor explanation**, **Poor UX**, or **Poor calibration** patterns are named in the Week Summary as candidates — not silently tolerated as “personality of the product.”  
- No silent rewrite of Educational Intelligence mid-Alpha disguised as evaluation.

### 7.4 What Version 1.0 does *not* require

- Optimal topic selection every day.  
- Dense analytics or composite quality scores.  
- Zero ignores.  
- Perfect explanations under thin warrant.  
- Algorithmic improvement as the definition of progress.

### 7.5 Gate statement (use at review)

At Alpha review, record one explicit statement:

> Recommendation quality for Version 1.0 is **acceptable** / **not yet acceptable**  
> because: \<pattern evidence from dimensions, outcomes, and failure categories\>.

If **not yet acceptable**, list the blocking patterns. Do not substitute a feature wishlist for that list.

---

# Relationship to other documents

| Document | Role |
|---|---|
| This framework | *How* recommendation quality is evaluated |
| [`INTERNAL_ALPHA_PLAYBOOK.md`](INTERNAL_ALPHA_PLAYBOOK.md) | *How* daily Alpha is operated |
| [`docs/journal/001_INTERNAL_ALPHA_WEEK.md`](../journal/001_INTERNAL_ALPHA_WEEK.md) | *Where* daily evidence is written |

Conflict rule: if operating steps disagree with evaluation labels, follow the playbook for daily routine and this framework for recommendation quality judgment and backlog promotion.

---

**End of Recommendation Evaluation Framework (Version 1.0).**  
Measure whether guidance helps learning. Classify failures. Promote patterns — not moods — into backlog.
