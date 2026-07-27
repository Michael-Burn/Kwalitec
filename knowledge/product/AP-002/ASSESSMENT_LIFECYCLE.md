# AP-002 — Assessment Lifecycle

**Programme:** AP-002 — Educational Assessment Engine  
**Status:** Design  

---

## 1. Lifecycle overview

```
Intent
  ↓
Eligibility & Trigger
  ↓
Instrument Selection
  ↓
Session Construction
  ↓
Delivery
  ↓
Response Capture
  ↓
Observation Emission (AP-001)
  ↓
Reasoning / Twin Update
  ↓
Learning Feedback
  ↓
Downstream Consumers (Mission refresh · Tutor · Graph projection)
  ↓
Closure & Audit
```

Each stage is deterministic given the same Twin state, curriculum retrieval results, and instrument definitions.

---

## 2. Stages

### 2.1 Intent

Declare *why* evidence is needed:

- diagnostic
- checkpoint
- adaptive probe
- recovery check
- mastery verification
- revision stability
- reflection

Intent is set by Mission Engine policy or Founder diagnostic tooling — not by the student inventing a high-stakes exam.

### 2.2 Eligibility & Trigger

Before constructing a session, verify:

| Check | Fail behaviour |
|---|---|
| Twin exists | Defer; honest cold-start messaging |
| Curriculum entity resolvable via Retrieval | Do not invent content |
| Learning Graph prerequisites allow probe (when required) | Prefer prerequisite recovery mission first |
| Evidence density rules (not over-assessing) | Skip or shorten session |
| Student workload / burnout constraints | Defer assessment activity |

Triggers are described in `MISSION_INTEGRATION.md`.

### 2.3 Instrument Selection

Select questions/prompts from the assessment instrument catalogue by:

- learning objective / curriculum entity
- intent
- knowledge level / difficulty band
- estimated time budget
- evidence types still needed by Twin (e.g. misconception vs confidence calibration)
- prerequisites satisfied

Selection is rule-based and explainable. No random “challenge mode”.

### 2.4 Session Construction

Build an `AssessmentSession` with:

- session id
- twin / student ids
- intent
- ordered items (questions / reflections)
- time budget
- mission link (optional)
- success criteria framed as *evidence goals*, not pass marks
- feedback policy (what Tutor/Pipeline may say)

### 2.5 Delivery

Present one item at a time (preferred) or a short quiz bundle when intent requires.

UX constraints (see `UX_PRINCIPLES.md`):

- no countdown punishment theatre by default
- confidence prompts invited, never forced as grading
- hints allowed according to policy (hint usage becomes evidence)
- exit without shame (“pause / resume later”)

### 2.6 Response Capture

For each item, capture raw response plus behavioural metadata:

- selected answer(s) / numeric / text / formula payload
- confidence rating (optional)
- response time
- hint usage
- retry count
- abandoned / skipped flags

Raw responses are immutable once committed.

### 2.7 Observation Emission (AP-001)

Map session outcomes to Assessment Pipeline events:

| Engine outcome | Typical AP-001 event | Twin ObservationKind |
|---|---|---|
| Single item attempt | `question_attempt` | `question_answered` |
| Multi-item quiz close | `quiz_submission` | `quiz_completed` |
| Reflection item | `reflection_submission` | `study_session_completed` (or future kind) |
| Formula recall item | `formula_recall` | `formula_reviewed` |
| Worked solution review | `worked_example_completion` | `study_session_completed` |

Provenance must encode Assessment Engine session/item ids so Founder diagnostics can audit the chain.

Assessment Engine **does not** call Reasoning directly in the preferred architecture; it emits through AP-001 so event immutability and feedback generation stay single-pathed.

### 2.8 Reasoning / Twin Update

AP-001 creates Observations and invokes `StudentReasoningService`. Educational Reasoning updates mastery, confidence, gaps, recommendations. Learning Graph mastery projections refresh as today.

### 2.9 Learning Feedback

Deterministic educational feedback (AP-001 `LearningFeedback` + Tutor narration):

- what evidence was collected
- what remains uncertain (honest)
- suggested next action (from Twin decisions / mission — not invented grades)

Never: percentage as identity, class rank, pass/fail badge for formative runs.

### 2.10 Downstream consumers

| Consumer | Action |
|---|---|
| Adaptive Mission Engine | May refresh today’s mission from updated Twin decisions |
| Intelligent Tutor | Explains results and encourages next step |
| Learning Graph | Reflects updated mastery projections on nodes |
| Founder analytics | Aggregates evidence density / instrument quality |

### 2.11 Closure & Audit

Persist session closure status:

- completed
- paused
- abandoned
- invalidated (structural validation failure)

Append-only audit: intent → items → responses → event ids → observation ids → reasoning run id.

---

## 3. State machine (conceptual)

```
draft → ready → in_progress → submitted → observed → reasoned → closed
                 ↓
               paused
                 ↓
             abandoned
```

Invalid transitions must be rejected (e.g. submitted → in_progress).

---

## 4. Idempotency

- Replaying the same committed response must not duplicate Observations.
- Mission-triggered sessions use stable keys (`mission_id` + `intent` + `day` + `objective`) where appropriate.
- Pipeline emission remains opt-compatible with AP-001’s existing mission hooks.

---

## 5. Failure modes

| Failure | Educational handling |
|---|---|
| Retrieval miss | Do not invent question content; fail closed with explainable deferral |
| Partial submit | Emit observations only for committed items; mark session incomplete |
| Reasoning unavailable | Keep events/observations durable; queue reasoning retry — do not invent Twin state |
| Over-assessment | Prefer mission study/recovery activities; protect learner trust |

---

## 6. Non-goals for lifecycle

- Live human invigilation
- Timed high-stakes exam protocols as default
- Auto-advancing mastery without Reasoning
- Silent background quizzes that surprise the learner without mission context
