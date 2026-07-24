# Educational Validation Framework

**Programme:** EP-001 — Product Validation & Intelligence  
**Deliverable:** Workstream 1  
**Version:** 1.0  
**Status:** Active — metric definitions frozen for Phase 1 instrumentation  
**Updated:** 2026-07-23  

**Authority:** Product + Educational governance  
**Does not:** Change Twin algorithms, Educational State contracts, or ship collectors.

---

## 1. Purpose

Prove that Kwalitec **improves learning**, not merely that students click through the product.

This framework defines:

1. Which educational outcomes matter.
2. How each outcome is measured.
3. What evidence is required before claiming improvement.
4. What is explicitly **not** a success metric.

Aligned with Vision 2030 Success Metrics and Product Analytics Architecture.

---

## 2. North star and validation hierarchy

| Level | Question | Owner |
|---|---|---|
| **North star** | Does consistent use materially raise exam pass probability? | Vision 2030 |
| **Platform outcomes** | Do students study consistently, complete Sessions, revise on schedule, accept guidance, retain knowledge, and calibrate readiness? | This framework |
| **Operational health** | Is the release safe, accessible, performant, supportable? | Quality Manual / WS6 |

Pass-rate is the ultimate educational claim. Until external exam outcomes can be ingested ethically and privately, Kwalitec validates **leading indicators** that Vision and Educational Constitution treat as lawful proxies for better learning decisions.

---

## 3. Outcome catalogue

Each outcome has:

- **Definition** — precise, reproducible
- **Primary evidence** — where truth comes from (authority, not dashboard math)
- **Formula / rule** — how to compute or classify
- **Validation method** — how we prove the product helped
- **Phase** — when instrumentation / reporting is required
- **Anti-patterns** — what must not count as success

Terminology: domain **Mission** = learner-facing **Session** (Product Language Guide). Metrics use Session in learner reports; event names may use `mission_*` where domain entities are Missions.

---

### O1 — Study consistency

| Field | Spec |
|---|---|
| **Definition** | Presence of at least one *productive* study commitment completion in a planned study window, across weeks. |
| **Primary evidence** | Mission/Session completion evidence + study plan windows (plan adherence). Behaviour evidence only — not page views. |
| **Formula** | `consistency_week = 1` if ≥1 completed Session with educational outcome in the student's planned days that week; else `0`. Rolling 4-week rate = mean of weekly flags. |
| **Validation method** | Cohort: compare 4-week consistency before vs after sustained product use (≥3 weeks). Qualitative: interview whether plan felt sustainable. |
| **Phase** | Phase 1 (events) + Phase 2 (adherence vs plan) |
| **Anti-patterns** | Login streaks; minutes online without completion; opening Home without Session outcome. |

---

### O2 — Mission / Session completion

| Field | Spec |
|---|---|
| **Definition** | Authoritative study commitment completed vs assigned for the period. |
| **Primary evidence** | Mission / Session execution + Educational Evidence of completion quality (not “started” alone). |
| **Formula** | `completion_rate = completed_sessions / assigned_sessions` over period. Report separately: started-but-abandoned. |
| **Validation method** | Track trend by cohort week. Correlate with consistency (O1). Investigate abandonment reasons in beta interviews. |
| **Phase** | Phase 1 |
| **Anti-patterns** | Counting navigations to Session UI; auto-complete without educational outcome. |

---

### O3 — Revision adherence

| Field | Spec |
|---|---|
| **Definition** | Completed revision windows vs planned revision windows. |
| **Primary evidence** | Revision planner + revision completion evidence. |
| **Formula** | `revision_adherence = completed_revision_windows / planned_revision_windows` (window-level, not topic-count gaming). |
| **Validation method** | Compare adherence weeks with subsequent recall/practice outcomes (O4) when available. |
| **Phase** | Phase 1 events when revision PRD approved; Phase 2 effectiveness |
| **Anti-patterns** | Marking revision done without retrieval/practice evidence; inflating planned windows to improve rate. |

---

### O4 — Knowledge retention

| Field | Spec |
|---|---|
| **Definition** | Durability of topic capability over time — evidence of successful recall/practice after a gap, vs decay signal. |
| **Primary evidence** | Twin Retention estimates + recall/practice evidence events. Analytics **summarises**; Twin owns belief. |
| **Formula** | Per topic: retention score/band from Twin; cohort metric = share of topics with retention band ≥ medium among topics with ≥N evidence events. Decay incidents = drop in retention band after gap without successful recall. |
| **Validation method** | Within-subject: topics revised on schedule (O3) vs neglected — compare later recall success. |
| **Phase** | Phase 1 snapshots; Phase 2 decay analysis |
| **Anti-patterns** | Self-certification alone; treating “covered in curriculum” as retained. |

---

### O5 — Confidence improvement

| Field | Spec |
|---|---|
| **Definition** | Movement of explicit learner confidence toward better calibration (not mere higher self-rating). |
| **Primary evidence** | Confidence ratings / Twin ConfidenceState; compared with mastery/assessment outcomes. |
| **Formula** | Calibration gap = |self_confidence − demonstrated_performance| (normalised). Improvement = reduction in mean absolute calibration gap over 4+ weeks with ≥M paired observations. |
| **Validation method** | Prefer calibration improvement over raw confidence inflation. Report both; success requires calibration or stable-high with evidence, not unearned confidence rise. |
| **Phase** | Phase 2 (requires paired confidence + outcome events) |
| **Anti-patterns** | Celebrating higher confidence without performance evidence; gamified confidence prompts. |

---

### O6 — Readiness prediction accuracy

| Field | Spec |
|---|---|
| **Definition** | Agreement between predicted readiness and later demonstrated outcomes (practice/assessment/exam proxy). |
| **Primary evidence** | Twin / readiness estimates at time T; outcomes at T+Δ. |
| **Formula** | For each readiness snapshot with later outcome: classify predicted band vs observed band; report accuracy, over-prediction rate, under-prediction rate. Brier/calibration curve when sample ≥ threshold (see §5). |
| **Validation method** | Holdout by time (never train evaluation on same window used for informal tuning notes). Private beta: mock exam or structured assessment proxies until real pass rates available. |
| **Phase** | Phase 2; north-star linkage when exam results available |
| **Anti-patterns** | Tuning readiness to look accurate on the same cohort without out-of-time validation; using analytics store to overwrite Twin readiness. |

---

### O7 — Reflection quality

| Field | Spec |
|---|---|
| **Definition** | Completion of required reflections **and** structured usefulness (not empty text). |
| **Primary evidence** | Reflection workflow completion + structured fields / rated usefulness where product requires them. |
| **Formula** | `reflection_completion = completed_required / required`. Quality flag = completed with all mandatory structured fields non-empty (free-text length alone is insufficient). |
| **Validation method** | Beta: sample review of whether reflections change subsequent study choices; correlate quality-flagged reflections with recommendation acceptance (O8) and revision adherence (O3). |
| **Phase** | Phase 1 completion; quality rubric Phase 2 |
| **Anti-patterns** | Counting skip-through; storing full free-text in analytics without privacy review. Prefer structured codes + hashes. |

---

### O8 — Recommendation acceptance & benefit

| Field | Spec |
|---|---|
| **Definition** | Whether the student accepted, ignored, or completed the recommended next action — and whether benefit followed. |
| **Primary evidence** | Recommendation shown/accepted/dismissed/completed events; Decision Journal where authoritative; Twin recommendation rationale fields. |
| **Formula** | Acceptance rate = accepted / shown (excl. expired). Completion among accepted. Educational benefit = positive evidence event on recommended topic within benefit window (default 14 days) vs matched ignored recommendations (see WS4). |
| **Validation method** | See [`RECOMMENDATION_VALIDATION.md`](RECOMMENDATION_VALIDATION.md). Every recommendation must expose Why / Evidence / Expected outcome / Confidence. |
| **Phase** | Future recommendation PRD for acceptance events; Phase 2 benefit |
| **Anti-patterns** | Optimising accept rate without benefit; opaque scores; pressuring accept. |

---

### O9 — Pass-rate correlation (north-star proxy)

| Field | Spec |
|---|---|
| **Definition** | Association between sustained product use (O1–O8 composite) and exam pass / score outcomes when ethically available. |
| **Primary evidence** | Voluntary, consented exam outcome reporting or provider-mediated results — **never** scraped or coerced. |
| **Formula** | Pre-registered analysis plan before cohort exam sitting: compare pass probability for consistent users (≥ threshold on O1+O2) vs less consistent users, with confounders noted (prior attempts, study hours outside product). |
| **Validation method** | Privacy review + PRD for any ingestion path. Until then: status = **NOT MEASUREABLE** (instrument leading indicators only). |
| **Phase** | Post Phase 2 / multi-cohort; methodology TBD (open question from Analytics Architecture §9) |
| **Anti-patterns** | Claiming pass-rate improvement from completion metrics alone; selection bias unacknowledged. |

---

## 4. Outcome → analytics / Twin map

| Outcome | Analytics event / aggregate | Educational authority |
|---|---|---|
| O1 Consistency | Session completions + plan windows | Mission execution + plan |
| O2 Completion | `session.started` / `session.completed` | Mission / Evidence |
| O3 Revision | `revision.planned` / `revision.completed` | Revision planner |
| O4 Retention | Twin retention + `educational_state.snapshot` | Twin Retention |
| O5 Confidence | Confidence ratings + mastery pairing | Twin Confidence |
| O6 Readiness accuracy | Snapshot readiness vs later outcomes | Twin Readiness |
| O7 Reflection | `reflection.completed` (+ quality flags) | Reflection workflow |
| O8 Recommendations | `recommendation.*` + Decision Journal | Twin / Recommendation engine |
| O9 Pass rate | Consented outcome records (future) | External + privacy |

One Educational Truth: analytics **never** invents mastery, readiness, or next action.

---

## 5. Evidence thresholds (minimum samples)

Claims in product, marketing, or V1 exit must meet sample floors:

| Claim type | Minimum |
|---|---|
| Directional internal trend (founder) | ≥10 active students, ≥2 weeks |
| Product decision / beta improvement claim | ≥20 active students, ≥4 weeks, pre-registered metric |
| Readiness calibration curve | ≥50 paired (prediction, outcome) observations |
| Pass-rate association | Pre-registered plan + privacy sign-off; cohort size per analysis plan |

Below threshold: report as **exploratory**, not validated.

---

## 6. Validation study designs (private beta)

| Design | Use for |
|---|---|
| **Within-subject trend** | Consistency, completion, acceptance over weeks for same student |
| **Matched ignore vs accept** | Recommendation educational benefit (O8) |
| **Interview protocol** | Why abandon Session; whether recommendation Why was clear; trust |
| **Time-holdout calibration** | Readiness prediction accuracy (O6) |

Do **not** chase feature requests. Interview themes must map to an outcome ID (O1–O9) or a quality-gate defect (WS6).

---

## 7. Reporting cadence

| Audience | Cadence | Surface |
|---|---|---|
| Founder / product | Weekly | Product Dashboard (WS7) — same definitions |
| Release gate | Per tag | Educational validation checklist (WS6) |
| V1.0 exit | Once | WS8 criteria + this framework’s Phase 2 bar |

---

## 8. Explicit non-metrics (alone)

Per Vision Never-Build and Analytics Architecture:

- Raw page views / undifferentiated engagement
- Gamification streaks as success
- Time-on-task without educational outcome
- Feature count shipped
- Recommendation accept rate without benefit analysis

Supporting context metrics (e.g. session duration) may appear on dashboards labelled **context only**.

---

## 9. Freeze & change control

1. **PRD-001 instrumentation freeze (v1.1):** outcome definitions for **O1, O2, O7** (plus journey milestone and Educational State / Twin evolution *observation* via hash snapshots) are frozen for collectors under [`PRD-001`](../../prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md).
2. **Deferred (require a future approved PRD):** **O3** revision adherence events; **O8** recommendation acceptance events; O5/O6 pairing; O9 pass-rate ingestion.
3. Changing a frozen formula requires a PRD amendment and version bump of this document.
4. Twin / EducationalStateService contract changes require explicit EP-001 programme authority **and** educational governance review.
5. Pass-rate methodology (O9) remains open until a dedicated PRD closes Analytics Architecture open question on exam outcomes.

---

## 10. Exit criteria for Workstream 1

| Criterion | Status |
|---|---|
| Measurable outcomes defined (O1–O9) | COMPLETE |
| Mapped to authorities / analytics | COMPLETE |
| Anti-patterns documented | COMPLETE |
| Sample thresholds set | COMPLETE |
| Linked to beta + V1 exit | COMPLETE (see programme README) |

Implementation of collectors, Twin expansions, and dashboards is owned by WS2–WS7 — not this document.

---

## References

- Vision 2030 — Success Metrics  
- `knowledge/product/analytics/PRODUCT_ANALYTICS_ARCHITECTURE.md`  
- `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`  
- `knowledge/educational/EDUCATIONAL_EVIDENCE_MODEL.md`  
- `knowledge/version2/STUDENT_DIGITAL_TWIN.md`  
- `knowledge/product/private_beta/`  
