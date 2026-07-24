# EP-003 — Educational Effectiveness Validation

**Programme ID:** EP-003  
**Status:** AUTHORIZED — documentation complete; cohort measurement pending  
**Started:** 2026-07-24  
**Authority:** Product (subordinate to Vision 2030 + Product Blueprint + Educational Constitution)  
**Platform baseline:** Version 1 Platform Baseline (GA operational readiness + Education OS canonical runtime)

---

## Mission

Validate that Kwalitec **measurably improves student learning outcomes**.

This programme introduces **no architectural changes**. It defines success metrics, private-beta protocol, experiment governance, product scorecard, executive dashboard specification, educational review criteria, and Version 1 educational Go / No-Go gates — using the Version 1 Platform Baseline as the evaluation subject.

---

## Programme objectives

| ID | Objective | Primary deliverable |
|---|---|---|
| O1 | Educational Success Metrics | [`EDUCATIONAL_METRICS.md`](EDUCATIONAL_METRICS.md) |
| O2 | Private Beta Validation | [`PRIVATE_BETA_PROTOCOL.md`](PRIVATE_BETA_PROTOCOL.md) |
| O3 | Evidence-Based Product Decisions | Scorecard + Go / No-Go + experiment PRD gate |
| O4 | Experiment Framework | [`EXPERIMENT_FRAMEWORK.md`](EXPERIMENT_FRAMEWORK.md) |
| O5 | Version 1 Educational Readiness | [`VERSION_1_EDUCATIONAL_REVIEW.md`](VERSION_1_EDUCATIONAL_REVIEW.md) · [`GO_NO_GO_REPORT.md`](GO_NO_GO_REPORT.md) |

---

## Workstreams

| WS | Name | Deliverable | Status |
|---|---|---|---|
| 1 | Success Metrics | [`EDUCATIONAL_METRICS.md`](EDUCATIONAL_METRICS.md) | **COMPLETE** (definitions) |
| 2 | Private Beta | [`PRIVATE_BETA_PROTOCOL.md`](PRIVATE_BETA_PROTOCOL.md) | **COMPLETE** (protocol; cohort pending) |
| 3 | Experiment Framework | [`EXPERIMENT_FRAMEWORK.md`](EXPERIMENT_FRAMEWORK.md) | **COMPLETE** |
| 4 | Educational Review | [`VERSION_1_EDUCATIONAL_REVIEW.md`](VERSION_1_EDUCATIONAL_REVIEW.md) | **COMPLETE** (qualitative baseline) |
| 5 | Product KPIs | [`PRODUCT_SCORECARD.md`](PRODUCT_SCORECARD.md) | **COMPLETE** |
| 6 | Executive Dashboard | [`EXECUTIVE_DASHBOARD_SPEC.md`](EXECUTIVE_DASHBOARD_SPEC.md) | **COMPLETE** (spec only) |
| 7 | Go / No-Go Review | [`GO_NO_GO_REPORT.md`](GO_NO_GO_REPORT.md) | **COMPLETE** (framework; decision pending evidence) |

---

## Quality gates (mandatory)

| Gate | Rule |
|---|---|
| Architecture | No architecture changes |
| Educational State | No Educational State contract or algorithm changes |
| Twin | No Twin algorithm or persistence redesign |
| Analytics infrastructure | No analytics collector / outbox / schema changes |
| Recommendations | No recommendation-behaviour changes; recommendations remain **excluded** from effectiveness claims until a future approved PRD |
| Platform Baseline | Version 1 Platform Baseline preserved |

---

## Relationship to EP-001 / EP-002

| Programme | Role |
|---|---|
| **EP-001** | Outcome catalogue (O1–O9), instrumentation PRD-001, Twin expansion design, recommendation validation framework |
| **EP-002** | Analytics operational readiness (durable outbox, privacy, runbooks); flag OFF until go-live |
| **EP-003** | Canonical KPI catalogue for effectiveness, private-beta protocol, experiment governance, scorecard, dashboard spec, educational usefulness review, V1 educational Go / No-Go |

EP-003 **does not replace** EP-001. Metric formulae that overlap with EP-001 must remain consistent; EP-003 adds operational fields (Owner, Review Frequency, Target) and product/executive surfaces.

---

## Governing references

| Authority | Path |
|---|---|
| Vision 2030 | `knowledge/product/vision/PRODUCT_VISION_2030.md` |
| Product Blueprint | `PRODUCT_BLUEPRINT.md` |
| Educational Constitution | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` |
| EP-001 Validation Framework | `knowledge/product/ep001_product_validation/EDUCATIONAL_VALIDATION_FRAMEWORK.md` |
| Private beta prep | `knowledge/product/private_beta/` |
| Analytics events | `knowledge/product/analytics/EVENT_CATALOGUE.md` |
| Version 1 readiness | `knowledge/VERSION_1_READINESS.md` |
| PRD template | `knowledge/prd/PRD_TEMPLATE.md` |
| GA certification | `docs/ga/CERTIFICATION_REPORT.md` |

---

## Exit criteria (programme)

| Criterion | Status |
|---|---|
| Educational KPIs defined | COMPLETE |
| Private Beta protocol approved (document) | COMPLETE — cohort ops still pending privacy sign-off |
| Experiments governed | COMPLETE |
| Executive scorecard complete | COMPLETE |
| Go / No-Go framework complete | COMPLETE |
| Version 1 educational readiness documented | COMPLETE (decision = PENDING EVIDENCE) |

**Not claimed by this programme alone:** measured learning-outcome improvement in a live cohort. That requires private-beta execution + analytics activation under EP-002 go-live + measurement reports against these definitions.

---

## How to update

1. Change KPI formulae only via PRD amendment (see Experiment Framework + Metrics freeze rules).
2. Update Go / No-Go statuses only when evidence paths exist.
3. Mirror major readiness changes into `knowledge/VERSION_1_READINESS.md`.
4. Do not implement dashboard, Twin, or educational behaviour changes under EP-003 authority.
