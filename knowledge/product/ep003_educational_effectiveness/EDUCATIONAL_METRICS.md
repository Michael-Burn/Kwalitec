# Educational Metrics (Canonical KPIs)

**Programme:** EP-003 — Workstream 1  
**Version:** 1.0  
**Status:** Active — definitions frozen for private-beta measurement  
**Updated:** 2026-07-24  
**Authority:** Product + Educational governance  
**Does not:** Change Twin, Educational State, analytics infrastructure, or recommendation behaviour

---

## 1. Purpose

Define the **canonical educational KPIs** used to decide whether Kwalitec improves learning.

Every metric below has:

| Field | Meaning |
|---|---|
| **Definition** | Precise, reproducible meaning |
| **Formula** | How to compute |
| **Data Source** | Authoritative system of record (and analytics observation where applicable) |
| **Owner** | Role accountable for definition integrity and review |
| **Review Frequency** | How often the metric is reviewed for product decisions |
| **Target** | Private-beta / V1 educational target (provisional until baseline week 0–2) |

Aligned with Vision 2030 Success Metrics and EP-001 Educational Validation Framework (O1–O9). Overlapping formulae **must match** EP-001; this catalogue adds operational governance fields.

Terminology: domain **Mission** = learner-facing **Session** (Product Language Guide). Learner reports use Session; event names may use `mission_*` / `session_*`.

---

## 2. Metric catalogue

### M1 — Weekly Active Learners (WAL)

| Field | Spec |
|---|---|
| **Definition** | Distinct students with ≥1 *productive* Session completion in the ISO week. Login alone does not count. |
| **Formula** | `WAL_week = COUNT(DISTINCT user_id)` where `session.completed` has `completion_status=completed` and `occurred_at` ∈ week |
| **Data Source** | Analytics event `session.completed` (PRD-001 / EVENT_CATALOGUE); authority = Mission / Session execution |
| **Owner** | Product (Founder until Product Analytics role exists) |
| **Review Frequency** | Weekly during private beta; monthly thereafter |
| **Target** | ≥70% of invited active cohort retain WAL in weeks 3–6 of their personal start (directional for N≥20) |
| **EP-001 link** | Supports O1 / O2 population denominator |
| **Anti-patterns** | Counting page views, dashboard opens, or abandoned-after-start as “active learning” |

---

### M2 — Study Sessions per Week

| Field | Spec |
|---|---|
| **Definition** | Mean number of completed productive Sessions per Weekly Active Learner in the week. |
| **Formula** | `sessions_per_WAL = COUNT(completed Sessions in week) / WAL_week` (report median as secondary) |
| **Data Source** | `session.completed` with `completion_status=completed` |
| **Owner** | Product |
| **Review Frequency** | Weekly (beta); monthly (steady state) |
| **Target** | Cohort median ≥2 completed Sessions / WAL / week by week 4 of personal start |
| **EP-001 link** | O2 intensity companion |
| **Anti-patterns** | Inflating by counting starts; celebrating duration without completion |

---

### M3 — Reflection Completion Rate

| Field | Spec |
|---|---|
| **Definition** | Share of required reflections that reach completed processing after a Session that required reflection. |
| **Formula** | `reflection_completion = completed_required / required` where required = Sessions that entered reflection step; completed = paired `reflection.completed` with `processing_status=completed` |
| **Data Source** | `reflection.submitted` + `reflection.completed` (Phase C); Reflection workflow authority — **body text never stored in analytics** |
| **Owner** | Educational Product + Reflection domain owner |
| **Review Frequency** | Weekly (beta) |
| **Target** | ≥80% reflection completion among Sessions that require reflection (N≥20 students, ≥4 weeks) |
| **EP-001 link** | O7 |
| **Anti-patterns** | Counting skip-through; storing free-text in analytics; quality = length alone |

---

### M4 — Mission / Session Completion Rate

| Field | Spec |
|---|---|
| **Definition** | Authoritative study commitments completed vs assigned (or started, when assignment not yet durable) for the period. |
| **Formula** | Primary: `completion_rate = completed_sessions / assigned_sessions`. Secondary (until assignment events exist): `completed / (completed + abandoned_after_start)` among started Sessions. Always report abandon rate separately. |
| **Data Source** | Mission / Session execution; analytics `session.started` / `session.completed` |
| **Owner** | Product + Learning Session Experience owner |
| **Review Frequency** | Weekly (beta) |
| **Target** | Completed / started ≥75% by week 4; abandon investigation mandatory if &lt;60% |
| **EP-001 link** | O2 |
| **Anti-patterns** | Auto-complete without educational outcome; counting UI navigations |

---

### M5 — Curriculum Progress Velocity

| Field | Spec |
|---|---|
| **Definition** | Rate of meaningful curriculum progression (topic / node transitions with educational evidence), not page browsing. |
| **Formula** | `progress_velocity = COUNT(distinct curriculum_node_id with ≥1 successful progression event) / active_learner_weeks` for the cohort window. Report per-student median. Until Journey production emit is live (ADR-026), use Educational State / Twin evolution observation + Session topic metadata as **provisional** sources, labelled provisional. |
| **Data Source** | Preferred: `journey.progressed` (when production emit enabled). Provisional: Session topic on `session.completed` + `educational_state.snapshot` / `twin.evolved` hash change cadence (observation only) |
| **Owner** | Product + Learning Journey owner |
| **Review Frequency** | Bi-weekly (beta); monthly steady state |
| **Target** | Establish baseline in weeks 1–2; directional improvement or stable sustainable pace by week 6 (no thrashing). Exact numeric target locked after baseline report. |
| **EP-001 link** | Supports O1 / O4 leading indicator |
| **Anti-patterns** | Counting syllabus views; gaming by micro-node spam |

---

### M6 — Study Consistency

| Field | Spec |
|---|---|
| **Definition** | Presence of ≥1 productive Session completion in the student’s planned study window across weeks. |
| **Formula** | `consistency_week = 1` if ≥1 completed Session with educational outcome in planned days that week; else `0`. Rolling 4-week rate = mean of weekly flags. |
| **Data Source** | Session completions + study plan windows (plan adherence). Phase 1 events + plan data; Phase 2 full adherence when revision/plan PRDs exist. |
| **Owner** | Product |
| **Review Frequency** | Weekly (beta) |
| **Target** | Rolling 4-week consistency mean ≥0.60 for active cohort (N≥20) |
| **EP-001 link** | O1 |
| **Anti-patterns** | Login streaks; minutes online without completion |

---

### M7 — Learning Continuity

| Field | Spec |
|---|---|
| **Definition** | Absence of harmful study gaps among previously active learners — continued engagement after activation without multi-week dropout. |
| **Formula** | `continuity_k = share of students with WAL in week W who also have WAL in week W+1` (week-over-week retention of productive learners). Report also 2-week and 4-week continuity. |
| **Data Source** | Derived from M1 (WAL) time series |
| **Owner** | Product |
| **Review Frequency** | Weekly (beta) |
| **Target** | Week-over-week continuity ≥70% among students past onboarding week 1 |
| **EP-001 link** | O1 companion (retention of productive behaviour) |
| **Anti-patterns** | Treating any login as continuity; hiding churn behind new invites |

---

### M8 — Time to Readiness

| Field | Spec |
|---|---|
| **Definition** | Elapsed calendar time from first productive Session to first sustained readiness band that the product treats as “exam-proximate” for the student’s exam scope (Twin / readiness authority — analytics summarises only). |
| **Formula** | Per student: `t_ready = date(first sustained readiness band ≥ target_band for exam scope) − date(first completed Session)`. Cohort: median `t_ready` among students who reach the band. Students not reaching band within window = censored (report separately). |
| **Data Source** | Twin / readiness estimates (authority); observation via Educational State / Twin snapshot events (hash + metadata). **Never recompute readiness in analytics.** |
| **Owner** | Educational governance + Twin owner (definition); Product (reporting) |
| **Review Frequency** | Monthly; per cohort window at Go / No-Go |
| **Target** | Baseline only in first private-beta cohort; no marketing claim. Directional: shorter median vs dogfood baseline is exploratory until N and confounding rules met (EP-001 §5). |
| **EP-001 link** | O6 leading indicator |
| **Anti-patterns** | Optimising readiness display without evidence; claiming exam readiness from completion metrics alone |

---

### M9 — Curriculum Completion

| Field | Spec |
|---|---|
| **Definition** | Share of syllabus scope (exam / subject plan) marked complete under educational authorities — not UI checkbox theatre. |
| **Formula** | `curriculum_completion = completed_in_scope_nodes / in_scope_nodes` per student plan. Cohort: median completion among students with ≥4 active weeks. |
| **Data Source** | Curriculum graph + Learning Journey / Educational State progression authorities; Journey events when available |
| **Owner** | Curriculum / Journey product owner |
| **Review Frequency** | Monthly; per cohort at Go / No-Go |
| **Target** | Cohort-dependent (exam date proximity). Private beta: track trend; do not set absolute % until exam-dated cohort plan exists. |
| **EP-001 link** | Progress toward O9 proxies |
| **Anti-patterns** | Self-mark mastered without evidence; treating open rate as complete |

---

## 3. Supporting context metrics (not success alone)

| Metric | Use | Label |
|---|---|---|
| Mean Session duration | Ops / UX load | **Context only** |
| Support tickets / WAL | Support load | **Ops** |
| Recommendation acceptance | Future PRD only | **Excluded until PRD** |

Per Vision Never-Build and EP-001 §8: page views, streaks, time-on-task without outcome, and feature count are **not** success metrics.

---

## 4. Sample thresholds (claims)

Inherited from EP-001 §5 — claims in product, marketing, or V1 educational Go require:

| Claim type | Minimum |
|---|---|
| Directional internal trend (founder) | ≥10 active students, ≥2 weeks |
| Product decision / beta improvement claim | ≥20 active students, ≥4 weeks, pre-registered metric |
| Readiness calibration | ≥50 paired (prediction, outcome) observations |
| Pass-rate association | Pre-registered plan + privacy sign-off |

Below threshold: **exploratory**, not validated.

---

## 5. Freeze & change control

1. M1–M4, M6–M7 formulae are frozen for private-beta reporting against PRD-001 Phase B/C events.
2. M5 Journey-preferred formula activates when `journey.progressed` production emit is enabled (ADR-026); until then provisional sources must be labelled.
3. M8–M9 remain measurement designs — no Twin/ESS algorithm change under EP-003.
4. Changing a frozen formula requires a PRD amendment and version bump of this document.
5. Recommendation-influenced metrics remain out of scope until a future approved PRD.

---

## 6. Exit criteria (WS1)

| Criterion | Status |
|---|---|
| Canonical KPIs defined with all required fields | COMPLETE |
| Mapped to data sources / EP-001 outcomes | COMPLETE |
| Targets set (provisional where baseline-dependent) | COMPLETE |
| Anti-patterns documented | COMPLETE |

---

## References

- [`../ep001_product_validation/EDUCATIONAL_VALIDATION_FRAMEWORK.md`](../ep001_product_validation/EDUCATIONAL_VALIDATION_FRAMEWORK.md)
- [`../analytics/EVENT_CATALOGUE.md`](../analytics/EVENT_CATALOGUE.md)
- [`../../prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md`](../../prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md)
- Vision 2030 — Success Metrics
- [`PRODUCT_SCORECARD.md`](PRODUCT_SCORECARD.md)
