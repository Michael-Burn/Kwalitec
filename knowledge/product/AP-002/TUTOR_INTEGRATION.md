# AP-002 — Tutor Integration

**Programme:** AP-002 — Educational Assessment Engine  
**Status:** Design  

---

## 1. Authority reminder

Per `ARCHITECTURE_INVARIANTS.md` and TUTOR-001:

- Tutor explains decisions already produced
- Tutor must not become a second reasoning engine
- Tutor must not mutate Twin inferences
- Assessment feedback in Tutor context is summary/explanation — not re-scoring

---

## 2. Tutor must

| Duty | Meaning |
|---|---|
| **Explain** | Clarify what the assessment was checking and what evidence was collected |
| **Encourage** | Keep psychological safety; normalise struggle as learning data |
| **Interpret results** | Translate Twin/Reasoning outcomes and Learning Feedback into plain language |
| **Point next** | Surface the next action already decided (mission / Twin recommendation) |

---

## 3. Tutor must never

| Prohibition | Why |
|---|---|
| **Grade** | No marks, pass/fail identity, or ranking language |
| **Replace Reasoning** | No alternate mastery/gap conclusions |
| **Re-score silently** | No second evaluation path that diverges from Engine/Pipeline |
| **Invent curriculum** | Retrieval remains the evidence interface |
| **Write Twin state** | Conversation memory ≠ learner SoT |

---

## 4. Evidence assembly for assessment conversations

When a student asks about a recent assessment, Tutor assembles:

1. Twin learning state / relevant mastery & gaps
2. Reasoning outputs already on Twin (run id, recommendations)
3. Learning Graph recovery/prerequisite context if relevant
4. AP-001 LearningFeedback + Assessment Result summaries
5. Curriculum Retrieval (`RetrievalProfile.TUTOR`) for the objective
6. Active mission context

Then builds a `ResponseBlueprint` and generates prose via `TutorGenerationPort` (deterministic V1 / future LLM behind the port only for prose).

---

## 5. Interpretive patterns (allowed)

| Pattern | Example framing |
|---|---|
| Evidence summary | “We collected a short check on X; here’s what it showed.” |
| Uncertainty honesty | “We still don’t have enough evidence to call this solid.” |
| Misconception gentle name | “One common mix-up showed up — let’s rebuild that idea.” |
| Calibration support | “You were unsure but got it — that knowledge may still feel fragile.” |
| Next action | “Today’s mission already adjusted toward recovery on …” |

Forbidden framings: “You scored 40%”, “Failed”, “Top quartile”, “AI thinks you mastered this” without Twin evidence.

---

## 6. Relationship to Assessment Engine

| Component | Role |
|---|---|
| Assessment Engine | Delivers instruments; emits evidence dimensions |
| AP-001 | Persists events/feedback; Twin observations |
| Reasoning / Twin | Infers meaning |
| Tutor | Narrates meaning already inferred |

Tutor may request Founder-safe summaries of recent assessment feedback (as TUTOR-001 already does) but must not call Engine scoring APIs to invent new conclusions.

---

## 7. Encouragement without false praise

Encouragement is evidence-aware:

- Effort and honesty of attempt can be acknowledged
- Correctness is not exaggerated into mastery
- Incorrectness is framed as useful information for the plan

This aligns with Product Communication / educational messaging standards: student-centred, non-engineering jargon, no Twin vocabulary leakage.

---

## 8. Session memory boundary

Tutor session memory may remember:

- that an assessment was discussed
- referenced concepts
- active mission id

It must not store durable mastery claims that Twin does not hold.
