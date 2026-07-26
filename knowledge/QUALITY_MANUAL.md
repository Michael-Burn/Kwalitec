# Kwalitec Quality Manual

**Version:** 1.0  
**Status:** Active  
**Related:** `knowledge/ENGINEERING_STANDARDS.md`, `docs/ga/`, `knowledge/RELEASE_PLAYBOOK.md`

Defines quality targets and policies for the post-consolidation product.  
No application redesign; no educational algorithm changes.

---

## 1. Accessibility targets

| Target | Standard |
|---|---|
| Shells | Skip link, main landmark, visible focus |
| Keyboard | Primary actions reachable without pointer |
| Motion | Honour `prefers-reduced-motion` |
| Charts | Text alternative when charts convey meaning |
| Contrast | Spot-check brand tokens for small text |

**Gate:** No production release of UI-impacting changes without the Engineering Standards accessibility checklist.

Evidence: `docs/production/ACCESSIBILITY_AUDIT.md`.

**Status:** Baseline present; residual gaps tracked (wizard inline handlers, chart alternatives, contrast spot-checks).

---

## 2. Performance budgets

Canonical soft CI budgets: `docs/ga/PERFORMANCE_BASELINE.md`.

| Policy | Rule |
|---|---|
| CI | Soft budgets enforced via `tests/ga/test_performance_benchmarks.py` |
| Staging | Operator sampling with `PROFILE_SQL` before large cohort expansion |
| Regression | Unjustified hot-path regression → fix or accept as Technical Debt with owner |
| Production SLO | Not identical to CI budgets — record staging measurements separately |

**Open:** Production cohort load test before high-traffic marketing launch.

---

## 3. Security checklist

Before release tag / production deploy:

- [ ] AuthN/AuthZ: login-required surfaces; no public registration
- [ ] Open redirect hardening intact
- [ ] CSRF enabled outside tests
- [ ] Security headers / CSP behaviour preserved
- [ ] Secrets via env; production rejects default insecure `SECRET_KEY`
- [ ] No new raw SQL concatenation
- [ ] Dependency scan (`pip-audit`) reviewed — criticals not silently ignored
- [ ] CSP `'unsafe-inline'` residual risk acknowledged if still present

Evidence: `docs/ga/SECURITY_REVIEW.md`.

---

## 4. Testing strategy

| Layer | Purpose | Location (examples) |
|---|---|---|
| Architecture | Layering / dependency / sole-runtime guards | `tests/architecture/`, `tests/education_os/` |
| Domain / application | Deterministic educational cores | `tests/application/`, domain packages |
| Presentation | Student routes, language, navigation | `tests/presentation/` |
| Operational / alpha | Smoke and sole-runtime protection | `tests/operational/` |
| GA | Release gates (perf, security-related, workflow) | `tests/ga/` |

**Principles:** curriculum-first; deterministic cores; no weakening of educational honesty tests.

---

## 5. Regression policy

1. Failures on `main` / release branches are **stop-ship** until classified.
2. Flaky tests must be fixed or quarantined with an explicit debt entry — not ignored.
3. Educational behaviour regressions require educational governance awareness.
4. Snapshot / copy tests protect Product Language; do not “fix” by loosening language rules without Product approval.
5. Known accepted residuals (e.g. CSP) must remain documented, not silently expanded.

---

## 6. Release policy

1. Classify release type per `docs/process/RELEASE_PROTOCOL.md`.
2. Follow `knowledge/RELEASE_PLAYBOOK.md` for operator steps.
3. Architecture Consolidation posture: EOS is canonical runtime — do not reintroduce dual educational brains.
4. No public launch from private-beta preparation alone (see Private Beta docs).
5. Version 1 readiness tracked in `knowledge/VERSION_1_READINESS.md`.
6. Educational validation (EP-001): releases that claim learning improvement must cite Validation Framework outcome IDs and sample thresholds — no exceptions.

---

## 7. Release quality gates (mandatory)

Every release must satisfy:

| Gate | Evidence |
|---|---|
| Regression | Pytest green on required suites; failures classified |
| Performance | Soft CI budgets; unjustified hot-path regressions fixed or debt-owned |
| Accessibility | Engineering Standards a11y checklist for UI-impacting changes |
| Security | Quality Manual §3 checklist |
| Documentation | User-facing / operator docs updated when behaviour changes |
| Educational validation | No new educational claim without Framework mapping; Twin/algorithm changes need EP-001 + governance |

---

## 8. Quality evidence map

| Concern | Primary artefact |
|---|---|
| GA certification | `docs/ga/CERTIFICATION_REPORT.md` |
| Performance | `docs/ga/PERFORMANCE_BASELINE.md` |
| Security | `docs/ga/SECURITY_REVIEW.md` |
| Accessibility | `docs/production/ACCESSIBILITY_AUDIT.md` |
| Educational governance | `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` |
| Educational validation | `knowledge/product/ep001_product_validation/EDUCATIONAL_VALIDATION_FRAMEWORK.md` |
| V1 exit (EP-001) | `knowledge/product/ep001_product_validation/V1_EXIT_CRITERIA.md` |
| Technical debt | `docs/TECHNICAL_DEBT_REGISTER.md` |

---

**Status:** Active  
**Next review:** End of next major release
