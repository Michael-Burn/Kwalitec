# EI-001.2 — Completion Report

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.2 — Dependency Assurance & Security Controls  
**Date:** 2026-07-28  
**Status:** Complete  
**Commit:** (see git — `chore(ei-001.2): strengthen dependency assurance and engineering security controls`)  
**Governance stance:** Educational baselines frozen — no educational / product behaviour changes  
**Findings closed:** ER-RB-07

---

## Summary

EI-001.2 replaces the soft `pip-audit` CI gate with an explicit Dependency Assurance Policy, a Security HOLD / accepted-findings register, and a reproducible `scripts/dependency_audit.sh` hard gate wired into `production-gates` and `release-build`. Known Medium/Low advisories ship only under documented HOLD; unaccepted advisories fail CI. No application behaviour, schema, UI, or educational systems were changed.

---

## Files Created

- `docs/security/DEPENDENCY_ASSURANCE_POLICY.md`
- `docs/security/DEPENDENCY_ACCEPTED_FINDINGS.md`
- `docs/security/dependency_accepted_vulns.txt`
- `scripts/dependency_audit.sh`
- `tests/architecture/test_dependency_assurance.py`
- `knowledge/release/EI-001/EI001_2_DESIGN_REPORT.md`
- `knowledge/release/EI-001/EI001_2_IMPLEMENTATION_REPORT.md`
- `knowledge/release/EI-001/EI001_2_TRACEABILITY_MATRIX.md`
- `knowledge/release/EI-001/EI001_2_TEST_REPORT.md`
- `knowledge/release/EI-001/EI001_2_COMPLETION_REPORT.md` (this report)

---

## Files Modified

- `.github/workflows/ci.yml`
- `tests/architecture/test_ci_integrity.py`
- `docs/release/DEPENDENCY_AUDIT_V2.md`
- `docs/production/RELEASE_PROCESS.md`
- `docs/production/RELEASE_CANDIDATE_FINGERPRINT.md`
- `docs/process/RELEASE_PROTOCOL.md`
- `docs/release/V2_RELEASE_CHECKLIST.md`
- `docs/ga/CERTIFICATION_REPORT.md`
- `docs/ga/SECURITY_REVIEW.md`
- `knowledge/QUALITY_MANUAL.md`
- `knowledge/RELEASE_PLAYBOOK.md`
- `knowledge/release/RELEASE_CHECKLIST.md`
- `knowledge/VERSION_1_READINESS.md`
- `CONTRIBUTING.md`
- `knowledge/release/ER-001/ER001_1_RELEASE_BLOCKERS.md`
- `knowledge/release/ER-001/ER001_1_RISK_REGISTER.md`
- `knowledge/release/ER-001/ER001_1_TECHNICAL_DEBT_REGISTER.md`

---

## Tests Executed

```bash
./scripts/dependency_audit.sh
.venv/bin/python -m pytest \
  tests/architecture/ \
  tests/application/educational_intelligence_pipeline/test_health_and_ci.py::TestCiIntegration \
  -v --tb=line -q
.venv/bin/ruff check \
  tests/architecture/test_dependency_assurance.py \
  tests/architecture/test_ci_integrity.py \
  --ignore=F401
```

**Outcome:** dependency audit exit 0 (4 ignored HOLDs); **2129 passed**; ruff clean. Details in `EI001_2_TEST_REPORT.md`.

---

## Migration Impact

None.

---

## Architecture Compliance

- Layering unchanged; no blueprint/service/model educational edits.  
- Curriculum V1/V2 invariants untouched; architecture suite green.  
- Dependency assurance enforced as an architecture + CI gate.  
- Educational governance not reopened.

---

## Technical Debt

- Flask pin ≥3.1.3 bump remains **ER-TD-M04** (HOLD-accepted Mediums).  
- ER-RB-04 privacy pack residual remains (G10 partial).  
- ER-RB-02 / 03 / 06 remain open.  
- Dependabot still enhancement (ER-TD-E04).

---

## Known Limitations

- Does not declare Version 1 production-ready.  
- Does not eliminate Flask advisories (documents Security HOLD instead).  
- Local architecture green is WP regression evidence; tagged SHA Actions green remains G11 claim source of truth.

---

## Acceptance Criteria

| Criterion | Met? |
|-----------|------|
| Dependency audit policy explicit and enforceable | Yes |
| Release security evidence reproducible | Yes — `./scripts/dependency_audit.sh` |
| Dependency verification integrated with engineering release docs | Yes |
| Regression testing passes | Yes — 2129 passed |
| No application behaviour changes | Yes |

---

## Student Impact Assessment

N/A — engineering controls / documentation only; no student-facing behaviour, recommendations, planning, readiness, or copy changes. Template authority: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md` (not applicable).

| Section | Assessment |
|---------|------------|
| Student problem | Unchanged |
| Student benefit | Indirect — safer release dependency signal |
| Learning benefit | None (no delivery) |
| Success metrics | Hard audit green; architecture tests green |
| Risks | None student-facing from this WP |
| Assumptions | Educational governance remains approved baseline |

---

## Estimated KSI contribution

**ΔKSI = 0**

Rationale: infra/docs engineering controls only; K1–K8 educational usefulness surfaces unchanged.

---

## Evidence collected

| Evidence | Path |
|----------|------|
| Design | `knowledge/release/EI-001/EI001_2_DESIGN_REPORT.md` |
| Implementation | `knowledge/release/EI-001/EI001_2_IMPLEMENTATION_REPORT.md` |
| Traceability | `knowledge/release/EI-001/EI001_2_TRACEABILITY_MATRIX.md` |
| Test report | `knowledge/release/EI-001/EI001_2_TEST_REPORT.md` |
| Policy | `docs/security/DEPENDENCY_ASSURANCE_POLICY.md` |
| HOLD register | `docs/security/DEPENDENCY_ACCEPTED_FINDINGS.md` |
| Audit script | `scripts/dependency_audit.sh` |
| Architecture tests | `tests/architecture/test_dependency_assurance.py` |
| Upstream blockers | `knowledge/release/ER-001/ER001_1_RELEASE_BLOCKERS.md` |

---

## Lessons learned for student value

Students never see dependency advisories directly, but a soft security gate can green-wash a release that later forces emergency bumps. Making HOLDs explicit and new findings hard-fail preserves the ability to ship educational improvements without surprise supply-chain risk.

---

## Explainability Review

N/A — no student-facing intelligence surfaces changed.

---

## Recommendation Quality Review

N/A — no recommendation ranking/selection surfaces changed.

---

## Version 1 readiness residual

| Gate | Residual after EI-001.2 |
|------|-------------------------|
| G10.5 | Dependency policy + hard gate closed (ER-RB-07). Flask bump residual ER-TD-M04 under HOLD. |
| G10 (broader) | Privacy pack residual keeps ER-RB-04 open |
| G11 | Unchanged process from EI-001.1; formal RC tag still Release operator |
| G7–G8, G12 | Unchanged (ER-RB-02, 03, 06) |
| G1–G6 | Educational / Product — not in scope |

---

**End of EI-001.2 Completion Report**
