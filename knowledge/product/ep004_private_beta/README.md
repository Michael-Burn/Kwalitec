# EP-004 — Private Beta Execution

**Programme ID:** EP-004  
**Status:** AUTHORIZED — Stage 0 executed; Stage 1–2 gated on privacy sign-off + monitoring  
**Started:** 2026-07-24  
**Authority:** Product (subordinate to Vision 2030 + Product Blueprint + Educational Constitution)  
**Platform baseline:** Version 1 Platform Baseline (GA operational readiness + Education OS canonical runtime)  
**Does not:** Redesign product, open public registration, change Twin / Educational State / recommendation algorithms, or alter M1–M9 definitions

---

## Mission

Execute a **controlled Version 1 private beta**: prepare the cohort, activate analytics in stages, measure educational outcomes (EP-003 M1–M9), collect qualitative feedback, protect platform stability, and produce a Version 1 Go / No-Go recommendation with evidence.

---

## Programme objectives

| ID | Objective | Primary deliverable |
|---|---|---|
| O1 | Prepare the beta cohort | [`BETA_COHORT.md`](BETA_COHORT.md) |
| O2 | Execute staged analytics activation | [`ANALYTICS_ACTIVATION.md`](ANALYTICS_ACTIVATION.md) + EP-002 flag strategy |
| O3 | Collect educational evidence | [`WEEKLY_SCORECARD.md`](WEEKLY_SCORECARD.md) (M1–M9 unchanged) |
| O4 | Collect qualitative feedback | [`FEEDBACK_REGISTER.md`](FEEDBACK_REGISTER.md) |
| O5 | Produce Version 1 Go / No-Go | [`VERSION_1_BETA_REPORT.md`](VERSION_1_BETA_REPORT.md) · [`GO_NO_GO_DECISION.md`](GO_NO_GO_DECISION.md) |

Supporting: [`ROLLOUT.md`](ROLLOUT.md) · [`OPERATIONS_MONITORING.md`](OPERATIONS_MONITORING.md) · [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md)

Blind review research infrastructure (permanent): [`reviewer_framework/`](reviewer_framework/) — run any SV-001–SV-020 reviewer with `Run reviewer SV-XXX` (see [`reviewer_framework/REVIEW_EXECUTION_GUIDE.md`](reviewer_framework/REVIEW_EXECUTION_GUIDE.md)).

---

## Workstreams

| WS | Name | Status |
|---|---|---|
| 1 | Cohort management | **COMPLETE** (registry live; Stage 0 participants recorded; Stage 1–2 slots reserved) |
| 2 | Staged rollout | **IN PROGRESS** — Stage 0 GO; Stage 1–2 HOLD pending privacy |
| 3 | Analytics activation | **IN PROGRESS** — OFF → Internal only authorized; Pilot/Private beta HOLD |
| 4 | Educational evidence | **IN PROGRESS** — Week 0 scorecard filed (exploratory N); weekly cadence defined |
| 5 | Qualitative feedback | **COMPLETE** (register + Stage 0 themes coded) |
| 6 | Operations | **COMPLETE** (monitoring baseline + rollback readiness) |
| 7 | Go / No-Go | **COMPLETE** — see [`GO_NO_GO_DECISION.md`](GO_NO_GO_DECISION.md) |

---

## Quality gates (mandatory)

| Gate | Rule | EP-004 posture |
|---|---|---|
| Educational behaviour | Unchanged | Pass — no algorithm / ESS / Twin / recommendation changes |
| Analytics healthy | Per EP-002 monitoring when flag ON | Pass for Stage 0 dark/internal path; Pilot+ require go-live checklist |
| Privacy compliant | Invite-only; Privacy Review before expanded cohort | Pass Stage 0; **OPEN** for Stage 1–2 |
| Operational readiness | EP-002 READY; GA certification retained | Pass |
| Platform Baseline | Preserved | Pass |
| Metric freeze | M1–M9 exactly as EP-003 | Pass — no formula changes |

---

## Relationship to prior programmes

| Programme | Role |
|---|---|
| **EP-001** | Outcome catalogue O1–O9; V1 exit criteria |
| **EP-002** | Analytics durability, privacy ops, feature-flag staged activation |
| **EP-003** | M1–M9 definitions, Private Beta Protocol, scorecard layout, educational Go / No-Go framework |
| **EP-004** | **Execution** of private beta: cohort, rollout, measurement fill, feedback, decision |

EP-004 does **not** redefine metrics. It fills evidence against EP-003 definitions and records the Version 1 beta decision.

---

## Governing references

| Authority | Path |
|---|---|
| Private Beta Protocol | `../ep003_educational_effectiveness/PRIVATE_BETA_PROTOCOL.md` |
| Educational Metrics | `../ep003_educational_effectiveness/EDUCATIONAL_METRICS.md` |
| Product Scorecard | `../ep003_educational_effectiveness/PRODUCT_SCORECARD.md` |
| EP-003 Go / No-Go framework | `../ep003_educational_effectiveness/GO_NO_GO_REPORT.md` |
| Feature flag strategy | `../analytics/ep002/FEATURE_FLAG_STRATEGY.md` |
| Go-live checklist | `../analytics/ep002/GO_LIVE_CHECKLIST.md` |
| Private beta ops | `../private_beta/` |
| GA certification | `docs/ga/CERTIFICATION_REPORT.md` |
| Version 1 readiness | `knowledge/VERSION_1_READINESS.md` |

---

## Exit criteria

| Criterion | Status |
|---|---|
| Private beta programme executed (staged; Stage 0 complete) | **COMPLETE** — Stage 1–2 authorized only after conditions |
| Evidence collected (scorecard + feedback + ops) | **COMPLETE** for Stage 0 / Week 0; ongoing for later stages |
| Educational KPIs measured (M1–M9 formulae applied) | **COMPLETE** (values exploratory / insufficient N — correctly labelled) |
| Operational stability verified | **COMPLETE** (baseline; flag OFF / internal path) |
| Go / No-Go decision documented | **COMPLETE** — **GO WITH CONDITIONS** |

---

## How to update

1. Append cohort rows only with invite + consent evidence — no fabricated PII.
2. Fill weekly scorecard values from analytics / Session authorities; label below-threshold cells **exploratory**.
3. Advance Stage 1–2 only after Privacy Review signatures + monitoring report GO.
4. Mirror major status into `knowledge/VERSION_1_READINESS.md`.
5. Do not change M1–M9 under EP-004 authority.
