# EP-004.1 — Learning Profile Gap Analysis

**Programme:** EP-004.1 — Personal Learning Profile  
**Date:** 2026-07-26  

---

## 1. Required capability (programme brief)

| Requirement | Needed for |
|---|---|
| Persistent evidence-based behavioural profile | Future personalisation without guessing |
| Attributes from observed evidence only | Educational honesty / constitution |
| Confidence per attribute | Under-claim / explainability |
| Fail-open consumption by Rec / Readiness / Planning | Preserve student path + ownership |
| Explicit observed / derived / unsupported | Prevent invented state |

## 2. Pre-EP-004.1 gaps

| Gap | Current state | Risk if ignored |
|---|---|---|
| No stable long-term profile contract | Only raw feedback events + Twin facets | Future personalisation invents ad-hoc summaries |
| No confidence model on behavioural rates | Quality contracts explain tips/plans, not habit rates | Over-claim K4 |
| No Port for services | Services cannot lawfully consume a profile view | Coupling to Twin or feedback internals |
| Candidate attributes without evidence | Duration / windows not in feedback payloads | Fabricated preferences |
| Feedback loop not closed into profile | EP-003.4 explicit non-goal | Observations unused for personalisation substrate |

## 3. Closure in EP-004.1

| Gap | Resolution |
|---|---|
| Stable contract | `PersonalLearningProfile` + `ProfileAttribute` |
| Confidence | Deterministic sample-size mapping |
| Service Port | `PersonalLearningProfilePort` + `consume_personal_learning_profile` |
| Missing evidence | `unsupported` / `unavailable` statuses |
| Aggregation | Aggregator over Learning Feedback events |

## 4. Remaining gaps (honest)

| Residual | Follow-on |
|---|---|
| Process-local only | Durable profile / Longitudinal Evidence publish |
| No measured session duration in feedback | Optional session telemetry programme |
| No study-window evidence | Explicit time-preference capture (settings) |
| Profile not yet changing readiness | Separate architecture review before readiness loop |
| Recommendation closed-loop | **Closed in EP-004.2** — bounded RecommendationService personalisation using profile evidence (authority preserved) |
| Planning closed-loop | **Closed in EP-004.3** — bounded PlanningService personalisation using profile evidence (educational priorities preserved) |
