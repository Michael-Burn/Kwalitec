# EP-004.2 — Personalisation Gap Analysis

**Programme:** EP-004.2 — Adaptive Recommendation Personalisation  
**Date:** 2026-07-26  

---

## 1. Required capability

| Requirement | Needed for |
|---|---|
| Profile-informed ordering (bounded) | K4 personalisation without second brain |
| Recovery / revision preference within bands | Habit-aware repair |
| Session sizing guidance | Declared preference honesty |
| Cadence awareness | Tip fatigue / dismiss patterns |
| Confidence-aware degrade | Trust / under-claim |
| Explainable personalisation trail | P-001.2 / K8 |
| Constitutional ownership preserved | STOP criteria |

---

## 2. Pre-EP-004.2 gaps

| Gap | State | Risk if ignored |
|---|---|---|
| Profile unused for ranking | Consume discarded | Profile substrate wasted; K4 stuck |
| No personalisation decision record | No factors on rows | Opaque adaptation later |
| No confidence gate for influence | N/A | Over-claim on thin samples |
| Accept rate easily misused | Preference journal exists | Constitutional violation (mastery) |
| Session duration rarely available | Unsupported without declaration | Fabricated minutes risk |
| Study windows always unsupported | No lawful evidence | Must remain no-op |

---

## 3. Closure in EP-004.2

| Gap | Resolution |
|---|---|
| Unused profile | Consumed in `_finalise_recommendations` → quality contract |
| Ordering | Tie-break after ladder + priority (`personalisation_tie_break`) |
| Recovery / revision | Confidence-gated within-band preference |
| Session sizing | Annotate next action when declared minutes available |
| Cadence | Soft limit + drop motivation tips on high dismiss rate |
| Explainability | `personalisation_factors` + supporting evidence lines |
| Ownership | Profile never owns ladder class; presentation pass-through |

---

## 4. Remaining gaps (honest)

| Residual | Follow-on |
|---|---|
| Category-specific responsiveness | Richer preference journal payloads |
| Live duration from sessions | Session telemetry programme |
| Study windows | Explicit preference capture |
| Durable profile | Cross-process store |
| Scorecard instrumentation | Private beta / K2 live re-score |
| Readiness / Planning loops | Separate EP programmes |
