# Version 1.0 Exit Criteria (EP-001)

**Programme:** EP-001 — Workstream 8  
**Version:** 1.0  
**Status:** Active gate list  
**Updated:** 2026-07-23  
**Tracker:** `knowledge/VERSION_1_READINESS.md` (operational board)

Kwalitec 1.0 is released **only if** all rows below are COMPLETE with linked evidence. No exceptions.

---

## Gate list

| # | Criterion | Evidence location (expected) | Status |
|---|---|---|---|
| 1 | Architecture stable | Consolidation / System Architecture; sole runtime | COMPLETE (see V1 readiness) |
| 2 | Educational validation complete | Framework frozen + Phase 1 metrics reporting + exploratory Phase 2 where claimed | IN PROGRESS — framework done; measurement pending |
| 3 | Recommendation engine validated | WS4 effectiveness report with ≥ Framework sample floor | NOT STARTED |
| 4 | Private beta successful | 20–50 IFoA cohort; observe / measure / interview cycle documented; privacy signed | IN PROGRESS — prep docs; cohort pending |
| 5 | Security approved | `docs/ga/SECURITY_REVIEW.md` + Quality Manual checklist | IN PROGRESS |
| 6 | Accessibility approved | Accessibility audit residuals closed or accepted with owners | IN PROGRESS |
| 7 | Performance approved | Soft CI budgets + staging baseline; production load as required | IN PROGRESS |
| 8 | Support ready | Private beta support workflow + staffed rota for cohort size | IN PROGRESS |
| 9 | Documentation complete | Vision, Blueprint, Governance, Standards, Quality, Playbook, EP-001 | IN PROGRESS |
| 10 | Monitoring operational | Release health signals + Phase 1 analytics integrity checks | NOT STARTED |

---

## Educational validation “complete” means

1. `EDUCATIONAL_VALIDATION_FRAMEWORK.md` active (done).
2. Phase 1 events live and validated (PRD-001).
3. At least one private-beta cohort window reported against O1, O2, O3, O7, O8 (acceptance).
4. No V1 marketing claim cites O9 pass-rate unless O9 methodology PRD is approved and evidence exists.

---

## Private beta “successful” means

- Cohort size in 20–50 IFoA students (invite-only).
- Measurement loop using Framework outcomes (not feature-request backlog as success).
- Interviews mapped to outcome IDs or quality defects.
- Support issues triaged per private beta workflow.
- No public registration / public launch.

---

## How to use

Update **Status** only when evidence paths exist. Mirror major changes into `VERSION_1_READINESS.md`.
