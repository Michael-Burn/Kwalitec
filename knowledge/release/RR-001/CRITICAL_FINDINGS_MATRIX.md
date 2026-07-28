# RR-001.1 — Critical Findings Matrix

**Programme:** RR-001 — Alpha Readiness Remediation Register  
**Work Package:** RR-001.1 — Critical Findings Resolution  
**Date:** 2026-07-28  
**Companion:** `ALPHA_REMEDIATION_REGISTER.md`

---

## Gate rule

RP-001.4 must not begin while any **Critical product defect** remains Open. Operational Criticals may remain Contained with explicit ops ownership.

---

## Critical product defects (implementation)

| ID | Finding | Sources | Root cause | Remediation | Verification | Status |
|----|---------|---------|------------|-------------|--------------|--------|
| RR-C01 | Session completion must complete Mission commitment lifecycle | JR-01 · T-47 · DP-22 · ST-07/09 | `mark_completed()` only called from legacy `app/mission/routes.py`; V2 `session.finish` omitted it | Call `RecommendationCommitmentService.mark_completed` from `complete_and_return` in `app/presentation/session/views.py` (fail-open, mirrors mission helper) | `tests/presentation/session/test_commitment_completion_link.py` — finish advances C2→C3; fail-open without commitment | **Resolved** |
| RR-C02 | False interactive reflection controls | JR-06 · JR-PREVIEW · IR-03 · SS-10 · T-59 · DP-38 | Home guided-reflection preview showed “Done reflecting” / “Skip for today” as control-like spans with no persistence | Remove fake controls; keep prompts as preview-only with honest “nothing recorded” disclaimer | `tests/presentation/student/test_rr001_1_critical_remediation.py::test_guided_reflection_preview_has_no_false_controls` | **Resolved** |
| RR-C03 | Revision acknowledgement unreachable under sole runtime | JR-07 · JR-REV-01 · T-64 · DP-37 · SS-29 | Ack UI only on legacy `dashboard/index.html`; sole runtime redirects `/dashboard/` → EOS Home | Surface same lifecycle acknowledgement on Student Home; keep POST `dashboard.acknowledge_revision` (already redirects to canonical home). **Rationale:** restore conscious syllabus-complete transition on the sole runtime journey without inventing a new educational stage or capability | `test_student_home_shows_revision_acknowledgement` + existing lifecycle service tests | **Resolved** |

---

## Critical operational (non-code)

| ID | Finding | Sources | Status | Ownership |
|----|---------|---------|--------|-----------|
| RR-C04 | Sole-runtime misconfiguration reintroduces competing homes | R-01 · JR-17 | **Contained** | Protect Render `KWALITEC_V2_SOLE_RUNTIME`; operational sole-runtime tests |
| RR-C05 | Public registration accidentally exposed | R-25 | **Contained** | Keep auth login/logout only; no public register in Alpha |

---

## Severity elevation notes

| Finding | RP-001.2 severity | RR-001.1 severity | Why elevated |
|---------|-------------------|-------------------|--------------|
| JR-01 | High | **Critical** | Breaks post-session educational arc on the *canonical* Alpha path |
| JR-06 / IR-03 | High / Critical | **Critical** | Direct Sensei honesty failure (fake listening) |
| JR-07 | High | **Critical** | Lifecycle milestone invisible under production sole-runtime posture |

No additional Critical product defects were discovered during RR-001.1 implementation beyond the three candidates named in the work package and the two pre-existing operational Criticals (R-01 / R-25).

---

## Traceability (code → finding)

| Change | Finding |
|--------|---------|
| `app/presentation/session/views.py` — `_link_commitment_completion` + call from `complete_and_return` | RR-C01 / JR-01 |
| `app/templates/student/home.html` — remove reflection control spans; honesty disclaimer | RR-C02 / JR-06 / IR-03 |
| `app/presentation/student/routes.py` — resolve lifecycle for Home | RR-C03 / JR-07 |
| `app/templates/student/home.html` — revision ack section | RR-C03 / JR-07 |

---

## Residual after RR-001.1

- **No open Critical product defects.**  
- Highest remaining for later packages: RR-H04 (empty Home), RR-H08 (cohort validation), RR-H11/H12 (narrator / noun identity), RR-H06 (notifications copy).  
- Dual chrome (RR-H02) remains accepted Alpha Stage 1 Deferred.

---

**End of CRITICAL_FINDINGS_MATRIX**
