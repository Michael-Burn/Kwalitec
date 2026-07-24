# Product Dashboard Specification

**Programme:** EP-001 — Workstream 7  
**Version:** 1.0  
**Status:** Spec — implementation after PRD-001 Approved and Phase 1 events land  
**Updated:** 2026-07-23  
**Audience:** Founder / executive (not learner analytics surface)

---

## 1. Purpose

One executive dashboard that tracks **student outcomes and release health** using Educational Validation Framework definitions — not a second educational brain.

Learner-facing analytics remain Student History / Educational State projections.

---

## 2. Metrics (required)

| Metric | Definition source | Notes |
|---|---|---|
| Weekly active students | Distinct users with ≥1 productive Session completion in week | Not mere login |
| Mission / Session completion | Framework O2 | |
| Study consistency | Framework O1 | Rolling 4-week rate |
| Recommendation acceptance | Framework O8 | After recommendation events exist |
| Average study time | Context only — Session duration mean | Label as context |
| Readiness distribution | Twin / Educational State bands histogram | Summarise; do not recompute |
| Retention | Twin retention band distribution / Framework O4 | |
| Support issues | Private beta issue intake counts by severity | From support workflow |
| Release health | Last tag: pytest/ruff, open P0 bugs, gate checklist | Quality Manual / GA |

---

## 3. Architecture rules

- Read models only — projections from event store + educational authorities.
- Same metric formulae as Validation Framework (no private founder scoring of mastery).
- Admin / founder auth only.
- No new third-party dashboard SDK without Security + Privacy review.
- Prefer extending Founder observability surfaces over inventing a parallel app.

---

## 4. Acceptance criteria (implementation milestone)

- [ ] Each tile cites outcome ID or “context” / “ops”
- [ ] Empty states when below sample thresholds (Framework §5)
- [ ] Week selector + export of aggregate CSV (no free-text PII)
- [ ] Tests for aggregation purity (no Twin calculator imports for mastery rewrite)
- [ ] Linked from Release Playbook as optional founder check

---

## 5. Non-goals

- Student-facing redesign of History
- Real-time clickstream vanity charts
- Public marketing metrics site

---

## References

- `EDUCATIONAL_VALIDATION_FRAMEWORK.md`  
- `knowledge/product/analytics/PRODUCT_ANALYTICS_ARCHITECTURE.md`  
- Founder dashboard blueprint (`app/founder/dashboard`)  
