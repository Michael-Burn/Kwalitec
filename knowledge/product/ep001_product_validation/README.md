# EP-001 — Product Validation & Intelligence

**Programme ID:** EP-001  
**Status:** Active  
**Started:** 2026-07-23  
**Authority:** Product (subordinate to Vision 2030 + Product Blueprint)  
**Constraint:** No architectural rewrites. No speculative features. Evidence-driven only.

---

## Mission

Transform Kwalitec from a well-engineered application into a **measurably effective** educational platform.

The platform is judged by **student outcomes**, not feature count.

---

## Governing references

| Authority | Path |
|---|---|
| Vision 2030 | `knowledge/product/vision/PRODUCT_VISION_2030.md` |
| Product Blueprint | `PRODUCT_BLUEPRINT.md` |
| Analytics architecture (design) | `knowledge/product/analytics/PRODUCT_ANALYTICS_ARCHITECTURE.md` |
| Quality Manual | `knowledge/QUALITY_MANUAL.md` |
| Version 1 readiness | `knowledge/VERSION_1_READINESS.md` |
| Private beta prep | `knowledge/product/private_beta/` |
| Educational Constitution | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` |
| Student Digital Twin | `knowledge/version2/STUDENT_DIGITAL_TWIN.md` |

---

## Workstreams

| WS | Name | Objective | Primary deliverable | Status |
|---|---|---|---|---|
| 1 | Educational Validation | Define measurable learning outcomes | [`EDUCATIONAL_VALIDATION_FRAMEWORK.md`](EDUCATIONAL_VALIDATION_FRAMEWORK.md) | **COMPLETE (framework)** |
| 2 | Learning Analytics | Instrument Phase 1 → Phase 2 events | [`PRD-001`](../../prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md) · [`Review`](../../prd/PRD_001_REVIEW.md) · [`Revision`](../../prd/PRD_001_REVISION_SUMMARY.md) | **Approved** v1.1 — impl milestone not started |
| 3 | Student Digital Twin V2 | Expand Twin with evidence-backed dimensions | [`TWIN_V2_METRIC_EXPANSION.md`](TWIN_V2_METRIC_EXPANSION.md) | Design |
| 4 | Recommendation Validation | Prove recommendations help learning | [`RECOMMENDATION_VALIDATION.md`](RECOMMENDATION_VALIDATION.md) | Framework |
| 5 | Private Beta | 20–50 IFoA students; observe / measure / interview | Existing `private_beta/` + cohort ops | Prep ready; cohort pending privacy |
| 6 | Quality Gates | Every release: regression, perf, a11y, security, docs, educational validation | Quality Manual § update | In progress |
| 7 | Product Dashboard | Executive outcome dashboard | [`PRODUCT_DASHBOARD_SPEC.md`](PRODUCT_DASHBOARD_SPEC.md) | Spec |
| 8 | Version 1.0 Exit Criteria | Release only when outcome bar is met | `VERSION_1_READINESS.md` + [`V1_EXIT_CRITERIA.md`](V1_EXIT_CRITERIA.md) | Tracker active |

---

## Sequencing (mandatory)

```text
WS1 Framework
    │
    ▼
WS2 Phase 1 instrumentation  ──►  WS7 Product Dashboard (reads same definitions)
    │
    ├──────────────────────────────►  WS4 Recommendation tracking
    │
    ▼
WS3 Twin metric expansion (only metrics with evidence + explainability)
    │
    ▼
WS2 Phase 2 + WS5 Private Beta measurement loop
    │
    ▼
WS6 Quality gates (every release) + WS8 V1.0 exit
```

**Do not** implement Twin algorithm changes or analytics collectors before:

1. WS1 outcome definitions are frozen for the metric in question.
2. A PRD is approved where behaviour or persistence changes.
3. Privacy review is satisfied for any new event retention.

---

## Non-goals

- Architectural rewrites of Educational OS / Flask layering.
- Parallel educational scoring brains outside Twin / Educational State.
- Vanity engagement metrics as success criteria.
- Public launch or open registration.
- Chasing beta feature requests that do not improve learning outcomes.

---

## Success definition

EP-001 succeeds when product decisions and release readiness are driven by **validated educational outcomes** (framework metrics + beta evidence), not by shipping more surface area.

---

## How to update

1. Change workstream status only when evidence exists (doc path, PR, test, cohort report).
2. Link artefacts in the Status column Notes via git history / PR.
3. Review at each tagged release against WS6 and WS8.
