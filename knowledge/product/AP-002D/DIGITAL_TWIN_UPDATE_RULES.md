# AP-002D — Digital Twin Update Rules

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration  
**Status:** Design (authoritative)  
**Related:** [`AP-002/DIGITAL_TWIN_INTEGRATION.md`](../AP-002/DIGITAL_TWIN_INTEGRATION.md), [`REASONING_CONTRACT.md`](REASONING_CONTRACT.md)

---

## 1. Purpose

Define which Twin educational state may change when assessment evidence arrives, which state must never change directly, and how cold-start, accumulation, and uncertainty are handled.

---

## 2. What may change (via Reasoning only)

| Twin facet | May change? | How |
|---|---|---|
| Observations (facts) | Append only | `ObservationService` / pipeline — never mutate/delete |
| Mastery map | Yes | `StudentReasoningService` applying `ReasoningResult.mastery` |
| Knowledge gaps | Yes | Reasoning |
| Confidence state | Yes | Reasoning |
| Learning-state snapshot | Yes | Reasoning |
| Recommendations | Yes | Reasoning |
| Predictions (scaffolds) | Yes | Existing scaffold path after engine result |
| Reasoning history / timeline | Yes | Append records for the run |

---

## 3. What must never change directly from Assessment

| Twin facet | Forbidden writer |
|---|---|
| Mastery / Estimated Knowledge | Assessment Engine, packaging, Tutor, Mission, Graph adapters |
| Gaps / recommendations / confidence | Same |
| Observation rewrite / delete | Anyone (append-only law) |
| Fabricated observations | Assessment “filling in” what the learner did not do |
| Competing long-term learner store | Presentation, Tutor memory, Mission cache treated as SoT |

**Rule:** Assessment may cause Twin updates only by producing facts that cross the Evidence Boundary and then triggering the lawful Reasoning path.

---

## 4. Cold-start behaviour

When observation density is thin:

1. Twin remains honest about uncertainty (no fake readiness / mastery theatre).
2. Assessment prioritises **diagnostic** intent (evidence locating unknowns).
3. Reasoning must not promote high-mastery language from thin / heavily scaffolded evidence.
4. Recommendations may favour short probes or teaching over confident advancement.
5. UX / Tutor copy avoids “you are behind” framing from empty belief.

Cold-start honesty is an educational integrity requirement (Invariant: evidence before inference).

---

## 5. Evidence accumulation

| Principle | Meaning |
|---|---|
| Append-only facts | New assessment sessions add observations; they do not rewrite history |
| Accumulation ≠ automatic certainty | More observations enable stronger inferences only when quality/consistency rules say so |
| Spaced stability | Later revision/verification intents matter for durable mastery inferences |
| Consistency over lucky hits | Single correct items under heavy hints remain weak evidence |
| Bundle strength as gate | `thin` / `moderate` / `strong` quality bands inform Reasoning gates — they are not mastery scores |

Idempotent ingress: replaying the same evidence reference must not invent a second educational fact.

---

## 6. Uncertainty handling

| Situation | Twin / Reasoning behaviour |
|---|---|
| Conflicting signals | Preserve or widen uncertainty; prefer diagnostic / adaptive follow-up decisions |
| Soft signals only (confidence, time) | May affect tone / calibration analysis; must not alone author high mastery |
| Thin evidence strength | Block or damp high-mastery promotions; keep gaps explicit |
| Missing curriculum refs | Do not invent syllabus claims; defer specific gap tagging |
| Partial session abandonment | Record what happened; do not invent completions |

Uncertainty is a first-class educational state, not a failure to paper over.

---

## 7. Update sequencing (normative)

```
Append observations (facts)
        ↓
StudentReasoningService.reason
        ↓
Replace Twin inference fields atomically (as existing persistence model)
        ↓
Append ReasoningRecord + timeline
        ↓
Refresh Learning Graph projections
```

Never: mutate mastery mid-session from Engine evaluation.

---

## 8. Compatibility

- SDT-001 → SDT-003 remain intact.
- Prefer mapping onto existing `ObservationKind` values.
- New kinds require a Twin/Observation additive milestone coordinated with Reasoning — not an Assessment-only fork.
- No Twin aggregate redesign in AP-002D.
