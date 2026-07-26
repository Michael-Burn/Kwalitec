# Product Scorecard

**Programme:** EP-003 — Workstream 5  
**Version:** 1.0  
**Status:** Active scorecard definitions — values filled during private beta  
**Updated:** 2026-07-24  
**Audience:** Founder / Product (not learner-facing)  
**Does not:** Implement dashboards or change educational behaviour

---

## 1. Purpose

One **product scorecard** that translates educational effectiveness and product health into decision-ready KPIs.

Rules:

- Educational rows use [`EDUCATIONAL_METRICS.md`](EDUCATIONAL_METRICS.md) formulae — no private founder scoring of mastery.
- Activity vanity metrics are context or forbidden.
- Empty / below-threshold cells must say **exploratory** or **insufficient N**, never greenwashed.

---

## 2. Scorecard layout

Update the **Value** and **Status** columns after each review window. Status: `On track` | `Watch` | `Off track` | `Baseline` | `N/A` | `Excluded`.

### 2.1 Activation

| KPI | Definition | Formula / source | Target | Value | Status | Owner | Cadence |
|---|---|---|---|---|---|---|---|
| Invite → first Session | Share of invited students with ≥1 completed Session within 7 days | Completions / accepted invites | ≥70% | — | Baseline | Product | Weekly |
| Time to first Session | Median days invite → first completion | Calendar delta | ≤3 days | — | Baseline | Product | Weekly |

### 2.2 Retention / Continuity

| KPI | Definition | Formula / source | Target | Value | Status | Owner | Cadence |
|---|---|---|---|---|---|---|---|
| Learning Continuity (WoW) | M7 | EDUCATIONAL_METRICS M7 | ≥70% post week 1 | — | Baseline | Product | Weekly |
| 4-week continuity | Share of week-1 WAL still WAL in week 4 | Derived from WAL | ≥50% (directional) | — | Baseline | Product | Monthly |

### 2.3 Completion

| KPI | Definition | Formula / source | Target | Value | Status | Owner | Cadence |
|---|---|---|---|---|---|---|---|
| Session Completion Rate | M4 | EDUCATIONAL_METRICS M4 | ≥75% completed/started by week 4 | — | Baseline | Product | Weekly |
| Curriculum Completion | M9 | EDUCATIONAL_METRICS M9 | Trend / exam-dated plan | — | Baseline | Product | Monthly |

### 2.4 Engagement (productive only)

| KPI | Definition | Formula / source | Target | Value | Status | Owner | Cadence |
|---|---|---|---|---|---|---|---|
| Weekly Active Learners | M1 | EDUCATIONAL_METRICS M1 | ≥70% of active cohort retain WAL weeks 3–6 | — | Baseline | Product | Weekly |
| Sessions per WAL | M2 | EDUCATIONAL_METRICS M2 | Median ≥2 / week by week 4 | — | Baseline | Product | Weekly |

### 2.5 Consistency

| KPI | Definition | Formula / source | Target | Value | Status | Owner | Cadence |
|---|---|---|---|---|---|---|---|
| Study Consistency (4-week) | M6 | EDUCATIONAL_METRICS M6 | ≥0.60 | — | Baseline | Product | Weekly |

### 2.6 Readiness

| KPI | Definition | Formula / source | Target | Value | Status | Owner | Cadence |
|---|---|---|---|---|---|---|---|
| Time to Readiness (median) | M8 | Twin authority; analytics summarise | Baseline first; no marketing claim | — | Baseline | Educational + Product | Monthly |
| Readiness claim safety | No O9/pass or “exam ready” marketing without gates | Go / No-Go | Pass | — | Watch | Product | Per release |

### 2.7 Learner Satisfaction

| KPI | Definition | Formula / source | Target | Value | Status | Owner | Cadence |
|---|---|---|---|---|---|---|---|
| Educational satisfaction | Share of interviewees answering Yes to Vision Final Test framing (“helped you study like a professional?”) | Interview protocol | ≥70% of interviewed (N≥8) | — | Baseline | Product | Per cohort |
| Support friction | P1 open &gt;48h | Support workflow | 0 | — | Watch | Ops | Weekly |

### 2.8 Educational Confidence

| KPI | Definition | Formula / source | Target | Value | Status | Owner | Cadence |
|---|---|---|---|---|---|---|---|
| Trust in guidance | Interview: “Did you trust why the product guided you?” (Yes / Partial / No) | Interview codes | ≥70% Yes or Partial with clear Why | — | Baseline | Product | Per cohort |
| Calibration posture | Prefer calibration improvement over raw confidence inflation (EP-001 O5) | Deferred until pairing events | N/A until PRD | — | Excluded | Educational | — |
| Recommendation benefit | EP-001 O8 | Future PRD | — | — | Excluded | Product | — |

### 2.9 Reflection & progress (educational)

| KPI | Definition | Formula / source | Target | Value | Status | Owner | Cadence |
|---|---|---|---|---|---|---|---|
| Reflection Completion | M3 | EDUCATIONAL_METRICS M3 | ≥80% | — | Baseline | Product | Weekly |
| Curriculum Progress Velocity | M5 | EDUCATIONAL_METRICS M5 | Baseline then stable sustainable | — | Baseline | Product | Bi-weekly |

---

## 3. How to score a review window

1. Confirm N and weeks against sample thresholds.
2. Fill Values from analytics projections + interview tallies only.
3. Set Status using targets; if below N → `Baseline` or note exploratory.
4. Record decisions: ship / hold / experiment PRD / rollback.
5. Attach evidence path (cohort report, export, interview notes ID).

---

## 4. Decision uses

| If scorecard shows… | Then… |
|---|---|
| Completion + consistency On track; trust Watch | Prioritise explainability / Coach cohesion — not new features |
| Activation Off track | Fix onboarding / invite ops before metric claims |
| Continuity Off track | Interview dropout; do not buy vanity engagement |
| Satisfaction high but completion low | Investigate busywork vs learning |
| Any readiness marketing pressure | Block until Go / No-Go readiness gates pass |

---

## 5. Exit criteria (WS5)

| Criterion | Status |
|---|---|
| Activation, Retention, Completion, Engagement, Consistency, Readiness, Satisfaction, Educational Confidence covered | COMPLETE |
| Linked to Educational Metrics IDs | COMPLETE |
| Recommendation rows excluded | COMPLETE |
| Fill process defined | COMPLETE |

---

## References

- [`EDUCATIONAL_METRICS.md`](EDUCATIONAL_METRICS.md)
- [`PRIVATE_BETA_PROTOCOL.md`](PRIVATE_BETA_PROTOCOL.md)
- [`EXECUTIVE_DASHBOARD_SPEC.md`](EXECUTIVE_DASHBOARD_SPEC.md)
- Vision 2030 Success Metrics
