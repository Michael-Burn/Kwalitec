# EP-003.4 — Constitutional Impact Assessment

**Programme:** EP-003.4 — Learning Feedback Loop  
**Date:** 2026-07-26  
**Phase:** Pre-implementation  

---

## 1. Ownership map (baseline)

| Concern | Required owner | Must not |
|---|---|---|
| Recommendation ranking / guidance | RecommendationService | Feedback recorder, presentation, Twin |
| Readiness score / drivers | ReadinessService | Feedback recorder recalculating readiness |
| Daily plan / mission persistence | PlanningService | Feedback recorder planning |
| Presentation speech selection | RuntimeAPresentationAdapter | Emit educational feedback; evaluate |
| Observed behavioural feedback buffer | LearningFeedbackRecorder | Make educational decisions |
| Twin synthesis | Digital Twin adapters | Write Runtime A facts from feedback |

## 2. Proposed change impact

| Change | Ownership risk | Mitigation |
|---|---|---|
| Feedback contracts + recorder | Low — observational only | Forbidden inference keys; no decision APIs |
| Recommendation emit on `record_decision` | Low — preference journal | Claim boundary `preference_journal`; fail-open |
| Planning emit on plan build / completion | Low — plan interaction | Emit after planning already decided |
| Readiness emit streak observation | Low — habit signal | Dashboard/intelligence only; collectors untouched |
| MissionService calls Planning emit | Low — Planning owns claim | MissionService does not interpret educationally |

## 3. STOP criteria review

Would this create a second educational brain? **No** — recorder has no decision authority.

Would presentation start evaluating / emitting educational conclusions? **No** — not an allowed source.

Would feedback mutate Recommendation / Readiness / Planning outputs? **No** — fail-open side effect only.

Would acceptance become mastery evidence? **No** — preference-journal claim; constitutionally labelled.

**STOP not triggered.** Proceed.

## 4. Feature flags

New flag: `KWALITEC_LEARNING_FEEDBACK` / `ENABLE_LEARNING_FEEDBACK` (default OFF).  
Inherits fail-open dual-run visibility; independently controllable from Experience Feedback and Longitudinal Evidence.
