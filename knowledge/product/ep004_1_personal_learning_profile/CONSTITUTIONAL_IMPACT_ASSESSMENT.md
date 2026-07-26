# EP-004.1 — Constitutional Impact Assessment

**Programme:** EP-004.1 — Personal Learning Profile  
**Date:** 2026-07-26  
**Phase:** Pre-implementation  

---

## 1. Ownership map (baseline)

| Concern | Required owner | Must not |
|---|---|---|
| Recommendation ranking / guidance | RecommendationService | Profile adapter, presentation, Twin |
| Readiness score / drivers | ReadinessService | Profile recalculating readiness |
| Daily plan / mission persistence | PlanningService | Profile planning |
| Presentation speech selection | RuntimeAPresentationAdapter | Invent profile attributes |
| Observed behavioural feedback | LearningFeedbackRecorder | Make educational decisions |
| Long-term behavioural profile summary | PersonalLearningProfileStore / Port | Make educational decisions; own Twin writes |
| Twin synthesis | Digital Twin adapters | Write Runtime A facts from profile |

## 2. Proposed change impact

| Change | Ownership risk | Mitigation |
|---|---|---|
| Profile contracts + aggregator | Low — summary only | Epistemic kinds; forbidden inference keys; no decision APIs |
| Process-local store | Low — replace snapshots | Immutable profiles; fail-open resolve |
| Service consume helpers | Low — optional inputs | Port typing; no ranking/plan/score mutation |
| Declared session minutes | Low — observed preference | Labelled observed fact; not measured duration |
| Unsupported study windows | None | Explicit unsupported — no invention |

## 3. STOP criteria review

Would this create a second educational brain? **No** — profile has no decision authority.

Would services delegate constitutional ownership to the profile? **No** — consume returns optional attributes; authorities unchanged.

Would presentation start evaluating / inventing profile claims? **No** — not wired.

Would preference rates become mastery evidence? **No** — claim boundaries + limitations.

Would Twin Knowledge State be written? **No** — out of scope.

**STOP not triggered.** Proceed.

## 4. Feature flags

New flag: `KWALITEC_PERSONAL_LEARNING_PROFILE` / `ENABLE_PERSONAL_LEARNING_PROFILE` (default OFF).  
Independently controllable from Learning Feedback and Twin flags; fail-open dual-run visibility.
