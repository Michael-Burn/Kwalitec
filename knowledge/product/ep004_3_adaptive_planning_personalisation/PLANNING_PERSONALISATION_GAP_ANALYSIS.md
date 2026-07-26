# EP-004.3 — Planning Personalisation Gap Analysis

**Programme:** EP-004.3 — Adaptive Planning Personalisation  
**Date:** 2026-07-26  

---

## 1. Required capability (programme brief)

| Requirement | Needed for |
|---|---|
| Profile-driven session duration | Completable days matching declared preference |
| Workload pacing from behaviour | Avoid chronic over-planning |
| Recovery sequencing emphasis | Proportionate repair after misses |
| Revision timing protection | Spaced repetition adherence |
| Equivalent slot selection | Recoverability among revision-pool alternatives |
| Explainable adaptations | Trust / P-001.2 |
| Educational priorities unchanged | Constitution / K1 integrity |

## 2. Pre-EP-004.3 gaps

| Gap | Current state | Risk if ignored |
|---|---|---|
| Profile consumed then discarded | EP-004.1 Port wired; no plan influence | K4 planning loop remains open |
| No confidence-gated plan adaptations | EP-003.3 uses Twin/miss signals only | Habit evidence unused |
| No personalisation trail on plans | Schema explains structure, not habit influence | Opaque if habits later influence quietly |
| EP-004.2 closed tips only | Planning residual called out in EP-004.1 | Uneven personalisation across Runtime A |

## 3. Closure in EP-004.3

| Gap | Resolution |
|---|---|
| Discarded profile view | Passed into quality → personalisation |
| Bounded adaptations | `planning_personalisation.py` rules P1–P5 |
| Confidence / unsupported | Same gates as EP-004.2 (0.3 / sample ≥ 3; declared duration exception) |
| Explainability | `personalisation_factors` + evidence lines |
| Educational order | Hard check; abort personalisation on violation |

## 4. Remaining gaps (honest)

| Residual | Follow-on |
|---|---|
| Process-local profile store | Durable profile programme |
| Preferred study windows unsupported | Lawful time-preference capture |
| No per-topic behavioural rates | Limits equivalent selection precision |
| Readiness personalisation still open | Separate programme |
| Declared session minutes need settings hand-off | Settings → consume declared minutes |
