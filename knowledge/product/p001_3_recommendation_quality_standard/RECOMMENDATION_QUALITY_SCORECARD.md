# Recommendation Quality Scorecard

**Programme:** P-001.3 — Recommendation Quality Standard  
**Version:** 1.0  
**Status:** Active — permanent measurement companion for K2 Recommendation usefulness  
**Effective:** 2026-07-26  
**Companion:** [`RECOMMENDATION_QUALITY_STANDARD.md`](RECOMMENDATION_QUALITY_STANDARD.md)  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs; does not lift EP-001 / EP-003 effectiveness marketing freezes  

---

## 1. Purpose

Define **measurable quality criteria** so future implementation programmes can improve Recommendation usefulness (K2) with evidence — not vibes.

The scorecard supports:

- programme Estimated KSI contribution claims for K2;
- dogfood / private-beta evaluation;
- governance review of whether recommendation changes improved educational usefulness.

**Marketing of recommendation effectiveness remains frozen** until EP-001 O8 / approved PRD evidence exists. Internal scoring and KSI re-scoring may use this scorecard without public effectiveness claims.

---

## 2. Baseline and targets

| Measure | Value | Authority |
|---|---|---|
| K2 baseline | **48** (Weak) | `../p001_1_ksi_baseline/BASELINE_KSI_ASSESSMENT.md` |
| Immediate floor (V1-K2) | Category ≥ **50** | Product Success Framework |
| Version 1 usefulness target for K2 | **≥ 70** (aspirational pillar lift) | Baseline opportunity table |
| Net KSI weight | 15% | Product Success Framework |

Closing K2 from 48 → 70 is approximately **+3.3 weighted KSI points** if other categories hold — material, but insufficient alone for KSI ≥ 80.

---

## 3. Scorecard metrics

Evaluate recommendation quality on these six criteria. Prefer under-claiming; do not invent instrumentation that does not exist yet — mark **Not yet instrumented** and use qualitative proxies.

### 3.1 Precision

| Attribute | Definition |
|---|---|
| **Question** | Of recommendations shown as primary, what share were educationally correct / relevant for that student’s state? |
| **Numerator** | Primary recommendations judged Correct + Relevant (quality dimensions) by review, dogfood, or labelled evaluation |
| **Denominator** | Primary recommendations shown in the evaluation window |
| **Student-safe interpretation** | “Did we suggest the right kind of work?” |
| **Version 1 directional target** | ≥ **70%** strong/acceptable precision in reviewed samples; **0** hard-gate failures (wrong topic family / plan fight) in production defaults |
| **Evidence sources** | Blind-review codes; Internal Alpha evaluation framework; support tickets for contradictory guidance; future labelled eval sets |

### 3.2 Acceptance rate

| Attribute | Definition |
|---|---|
| **Question** | When shown a primary recommendation, how often does the student start the suggested action (or explicitly accept)? |
| **Numerator** | Accepted / started recommended actions |
| **Denominator** | Primary recommendations presented |
| **Caveats** | Acceptance ≠ educational value; pair with completion and effectiveness. Do not optimise acceptance by making tips trivially easy. |
| **Version 1 directional target** | Establish baseline under approved PRD instrumentation; then lift without harming precision |
| **Evidence sources** | Future KPI under approved PRD; session start from recommendation CTA; interview “would you follow this?” |

### 3.3 Completion rate

| Attribute | Definition |
|---|---|
| **Question** | Of accepted recommendations, how often does the student complete the suggested scope (or an honest adjusted scope)? |
| **Numerator** | Completed recommended sessions / missions / practice blocks |
| **Denominator** | Accepted recommendations |
| **Caveats** | Low completion with high acceptance signals proportionality failure (effort mismatch). |
| **Version 1 directional target** | Completion not materially worse than plan-started sessions (M2 / M4 peers); investigate large gaps |
| **Evidence sources** | EP-003 M2 / M4 analogues; mission completion; dogfood notes on scope honesty |

### 3.4 Educational effectiveness

| Attribute | Definition |
|---|---|
| **Question** | Did following recommendations improve learning signals (weak-topic repair, coverage progress, readiness honesty, revision timing) vs activity vanity? |
| **Measurement posture** | Qualitative + bounded quantitative; **no public effectiveness marketing** until freeze lifted |
| **Positive signals** | Weak-topic practice followed by improved practice results; plan adherence with fewer contradictory tips; readiness unpackable and moving for right reasons |
| **Negative signals** | Streak theatre; topic thrash; readiness inflation; students retaining full external stacks *because* tips feel useless |
| **Version 1 directional target** | Blind-review / interview shift from “generic highest-value” to “I’d follow this”; K2 ≥ 50 then toward 70 |
| **Evidence sources** | EP-004 themes; EP-001 validation framework; IA-001 integrity lessons; future approved outcome studies |

### 3.5 Student satisfaction

| Attribute | Definition |
|---|---|
| **Question** | Do students trust and value recommendations as study companions? |
| **Proxies** | “Would you rely on tomorrow’s tip?”; support themes; NPS-like study-companion items; Coach usefulness codes |
| **Caveats** | Satisfaction without educational honesty is failure (praise for motivational fluff). |
| **Version 1 directional target** | Material reduction in opacity / conflict themes; satisfaction rising *with* precision |
| **Evidence sources** | Blind reviews; interviews; private-beta feedback; support taxonomy |

### 3.6 Explainability compliance

| Attribute | Definition |
|---|---|
| **Question** | Do shown recommendations satisfy P-001.2 Mandatory Explanation Schema at the declared level? |
| **Numerator** | Recommendations / surfaces Pass Explainability Review Checklist (R1–R5 + applicable S-items) |
| **Denominator** | In-scope recommendation surfaces reviewed |
| **Version 1 directional target** | **100%** of new/changed student-facing recommendation programmes Pass checklist before claiming K2/K8 gains |
| **Evidence sources** | Explainability Review artefacts; Runtime A consistency audits; copy reviews |

---

## 4. Scoring bands (portfolio)

Use bands for programme reviews and KSI evidence packs — not for student-facing scores.

| Band | Guidance |
|---|---|
| **Strong** | Metric meets directional target; no hard-gate incidents; explainability compliance Pass |
| **Acceptable** | Metric near target; issues classified and owned; no silent plan conflicts |
| **Weak** | Below target; generic tips; low trust themes persist |
| **Failed** | Hard-gate violations in production defaults; fabricated certainty; effectiveness theatre |

Do **not** average the six metrics into one public “recommendation quality %.” Report them separately; map to K2 narrative in the KSI re-score.

---

## 5. Mapping to K2

| Scorecard criterion | Primary K2 contribution |
|---|---|
| Precision | Correctness + personal relevance |
| Acceptance rate | Actionability + trust (partial) |
| Completion rate | Proportionality + timeliness |
| Educational effectiveness | Educational value (core) |
| Student satisfaction | Trust / willingness to rely |
| Explainability compliance | Non-conflicting, understandable guidance (shared with K8) |

A K2 claim of “+N points” must cite which criteria moved and how they were measured (or explicitly mark qualitative-only with confidence **Low/Medium**).

---

## 6. Instrumentation rules

1. Prefer EP-003 Educational Metrics and approved PRDs over ad-hoc event soup.  
2. Separate **technical success** (tip generated) from **educational success** (tip helped learning).  
3. Cold-start cohorts must not be pooled silently with dense-history cohorts.  
4. A/B or dual-run comparison of recommenders must preserve Educational Constitution honesty and plan coherence.  
5. Until effectiveness marketing freeze lifts, external communications must not claim pass-rate or “proven recommendation lift.”

---

## 7. Review cadence

| Cadence | Action |
|---|---|
| Per in-scope EP/P completion | Attach scorecard status (which metrics moved / unchanged) |
| Private beta / dogfood weeks | Sample precision + explainability compliance |
| KSI re-score | Update K2 with cited scorecard evidence |
| End of major release | Revisit directional targets; amend version if needed |

---

## 8. Relationship to Internal Alpha evaluation

`docs/product/RECOMMENDATION_EVALUATION_FRAMEWORK.md` remains the day-to-day dogfood evaluation companion (Relevance, Timing, Workload, Progression, Clarity, Trust). This scorecard is the **product measurement law** for programme and KSI reporting. Prefer aligning dogfood notes to both.

---

**End of RECOMMENDATION_QUALITY_SCORECARD**
