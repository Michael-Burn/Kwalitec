# Version 1 Private Beta Report

**Programme:** EP-004 — Workstream 7  
**Version:** 1.0  
**Date:** 2026-07-24  
**Subject:** Controlled Version 1 private beta — evidence pack  
**Companion decision:** [`GO_NO_GO_DECISION.md`](GO_NO_GO_DECISION.md)  
**Does not:** Change Platform Baseline, educational algorithms, or M1–M9 definitions

---

## 1. Executive summary

EP-004 authorized and executed the **controlled start** of Version 1 private beta:

- Cohort registry live; **Stage 0 (internal)** populated and monitoring **GREEN**.
- Analytics activation follows EP-002: default **OFF**; **internal-only** authorized; Pilot / Private beta **HOLD** pending Privacy Review.
- Educational KPIs **M1–M9** applied without change; Week 0 values correctly labelled **exploratory / insufficient N** (external N = 0).
- Qualitative feedback register seeded from educational review + Stage 0 dogfood and coded to Bug / UX / Educational / Operational / Future PRD.
- Platform stability and GA operational posture retained.

**Recommendation:** **GO WITH CONDITIONS** — continue Stage 0; advance to Stage 1 only after Privacy Review signatures and Pilot analytics checklist; do **not** claim educational effectiveness or commercial V1 launch.

---

## 2. Educational KPIs

Authority: EP-003 `EDUCATIONAL_METRICS.md`. Full fill: [`WEEKLY_SCORECARD.md`](WEEKLY_SCORECARD.md).

| ID | Metric | Result (Week 0) | Against target |
|---|---|---|---|
| M1 | WAL | External 0 | Insufficient N |
| M2 | Sessions / WAL | Not reported | Insufficient N |
| M3 | Reflection completion | Not reported | Insufficient N |
| M4 | Session completion | Not reported | Insufficient N |
| M5 | Progress velocity | Provisional N/A | Baseline (Journey emit deferred) |
| M6 | Consistency | Not reported | Insufficient N |
| M7 | Continuity | Not reported | Insufficient N |
| M8 | Time to readiness | N/A / censored | Baseline only — no claim |
| M9 | Curriculum completion | N/A | Baseline only — no claim |

**Interpretation:** Measurement **machinery and freeze** are ready. Live external effectiveness evidence is **not yet available**. This is expected at Stage 0 and must not be spun as success or failure of the product’s educational value.

Recommendations remain **excluded** from effectiveness claims (EP-003 / EP-001).

---

## 3. Operational KPIs

| Area | Result | Evidence |
|---|---|---|
| Dispatch latency | Healthy on dark path | [`OPERATIONS_MONITORING.md`](OPERATIONS_MONITORING.md) |
| Outbox health | Idle / empty expected while OFF | Same |
| Worker health | Not required while OFF; cron required before Pilot ON | EP-002 runbooks |
| Failures / DLQ | None attributed to EP-004 | Same |
| Replay | None | Same |
| Retention | Not due while external dark | Privacy ops guide |
| Privacy requests | None open | Same |
| Stage 0 monitoring | **GREEN** | Rollout log |
| P0 / P1 study blockers | None open from this programme | Support workflow |
| Analytics flag default | OFF | Feature flag strategy |
| GA residuals | Accepted with owners (CSP, load test open) | `docs/ga/CERTIFICATION_REPORT.md` |

**Operational verdict:** Stable for continued closed beta ops. Expand only under staged gates.

---

## 4. User feedback

See [`FEEDBACK_REGISTER.md`](FEEDBACK_REGISTER.md).

| Theme | Headline finding |
|---|---|
| Usability / navigation | Orientation still needed (Journey / History / Revision) |
| Trust | Coach–Session naming cohesion; Twin “made up” risk if overclaimed |
| Coach | Measure qualitatively; no algorithm change |
| Mission / Session | Primary learning object fit for validation |
| Reflection | Completion measurable; privacy invariant holds |
| Journey | Useful qualitatively; M5 provisional until ADR-026 emit |
| Confusion | Naming + orientation dominate over functional Stage 0 bugs |
| Feature requests | Recommendation effectiveness → Future PRD / declined here |

No Stage 0 **BUG** P0/P1 filed under EP-004.

---

## 5. Risk assessment

| Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|
| Expanding cohort without Privacy Review signatures | High | Medium if rushed | Hard HOLD on Stage 1 |
| Enabling analytics on shared prod with external users too early | High | Medium | Pilot checklist + internal-only boundary |
| Greenwashing Week 0 empty KPIs as “on track” | High (trust) | Medium | Scorecard labels enforced |
| Claiming Twin / readiness / pass outcomes | High | Medium under launch pressure | M8 baseline-only; Vision / Go–No-Go forbid |
| Journey M5 treated as definitive | Medium | Medium | Provisional label until emit |
| Silent educational behaviour change to “fix metrics” | High | Low if governance held | Experiment Framework + EP-004 quality gates |
| Support capacity at Stage 2 | Medium | High when N grows | Founder SLA; staff rota still open on readiness board |

---

## 6. Known issues

1. **Privacy Review unsigned** — blocks Stage 1–2 (`../private_beta/PRIVACY_REVIEW.md`).  
2. **External cohort N = 0** — EP-003 exit criterion #1 open.  
3. **Analytics production default OFF** — correct; Pilot ON not yet authorized.  
4. **Journey production emit deferred** (ADR-026) — M5 provisional.  
5. **GA residuals** — CSP `'unsafe-inline'`; production cohort load test open.  
6. **Support not staffed as a function** — founder-operated (acceptable for Stage 0–1; watch Stage 2).  
7. **Recommendation effectiveness** — explicitly out of scope / no-claim.

---

## 7. Rollout & analytics status

| Stream | Status |
|---|---|
| Stage 0 | **GO** — executed |
| Stage 1 | **HOLD** — privacy |
| Stage 2 | **HOLD** — Stage 1 |
| Flag OFF | Active default |
| Flag Internal only | Authorized |
| Flag Pilot / Private beta | HOLD |

Details: [`ROLLOUT.md`](ROLLOUT.md), [`ANALYTICS_ACTIVATION.md`](ANALYTICS_ACTIVATION.md).

---

## 8. Quality gates

| Gate | Result |
|---|---|
| Educational behaviour unchanged | **Pass** |
| Analytics healthy (for current stage) | **Pass** |
| Privacy compliant (Stage 0; expanded open) | **Pass / Open** |
| Operational readiness maintained | **Pass** |
| Platform Baseline preserved | **Pass** |
| M1–M9 freeze | **Pass** |

---

## 9. Recommendation

**GO WITH CONDITIONS**

See signed decision record: [`GO_NO_GO_DECISION.md`](GO_NO_GO_DECISION.md).

---

## 10. Exit criteria (report)

| Criterion | Status |
|---|---|
| Educational KPIs section | COMPLETE |
| Operational KPIs section | COMPLETE |
| User feedback section | COMPLETE |
| Risk assessment | COMPLETE |
| Known issues | COMPLETE |
| Recommendation | COMPLETE |
