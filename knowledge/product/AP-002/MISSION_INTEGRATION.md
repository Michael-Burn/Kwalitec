# AP-002 — Mission Integration

**Programme:** AP-002 — Educational Assessment Engine  
**Status:** Design  

---

## 1. Principle

The Adaptive Mission Engine schedules **what to do**. Assessment is one activity class missions may include.

Missions consume Twin decisions and Learning Graph structure. They never invent assessment grades or Twin inferences. Assessment evidence influences future missions **only** after Reasoning updates the Twin (same law as AP-001).

---

## 2. When assessments are triggered

| Trigger type | When | Educational goal | Typical mission framing |
|---|---|---|---|
| **Diagnostic** | Thin Twin, new topic entry, unclear gap locus | Locate unknowns | “Quick check so we know where to focus” |
| **Revision** | Spaced revisit due / stability uncertain | Test durability | “See what still feels solid” |
| **Checkpoint** | Mid-objective or after study block | Formative progress evidence | “Short check on today’s idea” |
| **Adaptive** | Reasoning flags unstable mastery or conflicting signals | Reduce specific uncertainty | “Clarify this uncertain concept” |
| **Recovery** | After recovery path steps | Verify gap closure attempt | “Check whether the foundation holds” |
| **Mastery verification** | Twin/Reasoning requests stronger evidence before higher mastery language | Evidence density for mastery confidence | “Confirm this understanding with a careful check” |

Triggers are policy inputs to Mission construction — explainable, deterministic, workload-aware.

---

## 3. Trigger eligibility gates

Before inserting an assessment step:

1. Twin decision or gap justifies the intent
2. Curriculum entity retrievable
3. Prerequisites respected (or diagnostic-at-boundary explicitly framed)
4. Time budget fits mission duration
5. Recent assessment density below over-assessment threshold
6. Burnout / pacing constraints not violated

If gates fail: schedule study/practice/recovery instead; do not force a quiz for product theatre.

---

## 4. How missions use assessment evidence

```
Mission includes assessment activity
        ↓
Learner completes Assessment Engine session
        ↓
AP-001 emits observations + learning feedback
        ↓
Reasoning updates Twin decisions / gaps / mastery confidence
        ↓
Optional mission refresh / next-day generation uses new Twin state
```

Mission progress/completion hooks from AME-001 already emit assessment events for abstract activities. AP-002 deepens those activities from abstract placeholders into real instruments — without changing the law that mission success does not short-circuit Twin authority.

### Uses of post-assessment Twin state

| Twin output | Mission use |
|---|---|
| Persistent gap with misconception tag | Prefer recovery path on that misconception |
| Stronger mastery confidence | Reduce redundant probes; advance Learning Mode sequence lawfully |
| Calibration issues | Prefer confidence-aware practice + Tutor encouragement |
| Unchanged uncertainty | Avoid declaring success; schedule alternate evidence or teaching |

---

## 5. Mission activity mapping (design)

| Abstract AME activity | Assessment Engine intent |
|---|---|
| practice | checkpoint / adaptive probe |
| recovery | recovery check |
| review / revision | revision stability |
| reflection | reflection |
| verify / confirm (future label) | mastery verification |
| diagnose (future label) | diagnostic |

Exact activity enums remain an implementation concern for AP-002E; design requires labels stay educational, not exam-like.

---

## 6. Student-facing mission copy

Prefer:

- “We’ll check understanding so today’s plan stays accurate.”
- “This helps the study plan adapt to you.”

Avoid:

- “Test time”
- “You must pass to continue”
- Hidden surprise exams mid-mission without framing

---

## 7. Non-interference rules

1. Learning Mode syllabus authority remains intact for daily topic selection.
2. Assessment steps must not yank the learner off Current Learning Topic without explainable advisory disclosure when advisory focus differs.
3. Assessment failure (incorrect answers) never “punishes” with blocked progress theatre; it informs recovery.
4. Mission Engine must not re-score Assessment inside prioritisation math.

---

## 8. Founder diagnostics

Future Founder views should show:

- missions that triggered assessment
- intents used
- observation yield
- whether Reasoning ran
- whether mission refreshed

Not student ranking.
