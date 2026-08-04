# P-002.1 — Gate Scorecard (G1–G12)

**Programme:** P-002.1 — Version 1 Release Readiness Validation  
**Date:** 2026-08-04  
**Authority:** `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md`  
**Claim tip:** `272a0950ca1a65df01badf5e180c3c06a41681e7`  
**Verdict scale:** PASS · PASS WITH RESIDUAL · HOLD · FAIL  

---

## Board summary

| Gate | Verdict | Hard blocker? |
|------|---------|---------------|
| G1 Validated KSI | **FAIL** | **Yes** |
| G2 Constitutional compliance | **PASS WITH RESIDUAL** | No (claim-class residual) |
| G3 Explainability | **PASS WITH RESIDUAL** | No |
| G4 Recommendation quality | **PASS WITH RESIDUAL** | No |
| G5 Planning quality | **PASS WITH RESIDUAL** | No |
| G6 Readiness quality | **PASS WITH RESIDUAL** | No |
| G7 Performance | **HOLD** | Claim-restricted |
| G8 Reliability | **PASS WITH RESIDUAL** | No |
| G9 Production telemetry | **PASS WITH RESIDUAL** | No (flag OFF honesty) |
| G10 Security / privacy | **PASS WITH RESIDUAL** | Stage-1 cohort residual |
| G11 Regression coverage | **PASS WITH RESIDUAL** | Stale-test debt |
| G12 Feature-flag readiness | **PASS WITH RESIDUAL** | Invite-only claim class |

**Overall declaration posture:** **NO-GO** — G1 FAIL blocks Version 1 production-ready declaration.

---

## G1 — Validated KSI — FAIL

| Criterion | Result | Evidence |
|-----------|--------|----------|
| G1.1 KSI ≥ 80 | **FAIL** | Latest validated composite **64** (EP-008.1B); gap ~16 pts — `knowledge/product/ep008_1b_recommendation_trust_validation/KSI_IMPACT_REPORT.md` · `knowledge/VERSION_1_READINESS.md` |
| G1.2 Confidence Medium/High | **PASS** | Medium |
| G1.3 ≤ 90 days | **PASS** | Assessment chain 2026-07-26; within window on 2026-08-04 |
| G1.4 No category &lt; 50 | **PASS** | Floors held |
| G1.5 K8 ≥ 70 | **PASS** | K8 **72** |
| G1.6 Evidence paths | **PASS** | EP-005.1 register + revalidation chain |
| G1.7 Independent re-score ±3 | **HOLD** | Second assessor not filed |
| G1.8 Claim language | **PASS** | No pass-rate claim |
| G1.9 Effectiveness not NO-GO | **FAIL** | `…/ep007_3_…/G1_9_STATUS.md` — effectiveness **NO-GO / PENDING EVIDENCE** |
| G1.10 Honesty incident clear | **PASS** | No open P1 honesty incident |

**Notes:** PB-017 Progressive Confidence PASS and Premium Conditional PASS do **not** satisfy G1. Estimated ΔKSI programmes do **not** satisfy G1.

---

## G2 — Constitutional compliance — PASS WITH RESIDUAL

| Check | Result | Evidence |
|-------|--------|----------|
| Educational Content Freeze held | **Pass** | Working-tree freeze check clean on package/campaign trees; PB-017 freeze; this programme docs-only |
| EF-001 unchanged | **Pass** | No EA/EO/TV/EJ/EW law change |
| One Education OS runtime | **Pass** | Sole runtime production-ON (`VERSION_1_FLAG_MATRIX.md`); PX-007 I-8 Pass |
| Curriculum V1/V2 loadable | **Pass** | `tests/test_curriculum_engine_v2.py` · `tests/test_curriculum_load_auto.py` green in P002.1 pack |
| Vision Never-Build defaults | **Pass** | No public registration / mastery theatre introduced this programme |
| EVF APPROVED for V1 claim class | **Residual** | Educational trust for package path held (PB-017); **full V1 declaration EVF APPROVED** not filed for production-ready claim class |
| SIA / ADR currency board | **Residual** | Prior programmes filed; claim-window memo not re-signed as declaration package |

---

## G3 — Explainability — PASS WITH RESIDUAL

| Check | Result | Evidence |
|-------|--------|----------|
| EP-003.1–.3 Explainability Review | **Pass** | Checklists Pass |
| K8 ≥ 70 | **Pass** | K8 **72** |
| Spot-check pack G3.4 (all surfaces) | **Residual** | Declaration spot-check pack not refiled this exit |
| Open P1 explainability honesty | **Pass** | None open |

---

## G4 — Recommendation quality — PASS WITH RESIDUAL

| Check | Result | Evidence |
|-------|--------|----------|
| Recommendation Review Checklist | **Pass** | EP-003.1 / EP-008.1 |
| K2 ≥ 50 floor | **Pass** | K2 **68** |
| Ranking / engine unchanged this programme | **Pass** | Validation-only; no ranking edits by P-002.1 |
| Scorecard precision sample G4.4 | **Residual** | Marketing freeze remains; scorecard evaluation incomplete |
| Effectiveness marketing | **Frozen** | EP-001 O8 freeze held |

---

## G5 — Planning quality — PASS WITH RESIDUAL

| Check | Result | Evidence |
|-------|--------|----------|
| Automated planning quality tests | **Pass** | `tests/services/test_planning_quality_ep003_3.py` — **14 passed** (P002.1 run) |
| K1 contribution | **Pass** | K1 **72** (prior validated) |
| Duration conflict dogfood pack G5.3 | **Residual** | PX-007 walkthrough Conditional notes; packaged declaration smoke residual |

---

## G6 — Readiness quality — PASS WITH RESIDUAL

| Check | Result | Evidence |
|-------|--------|----------|
| Automated readiness quality tests | **Pass** | `tests/services/test_readiness_quality_ep003_2.py` — **17 passed** |
| Honest refusal path | **Pass** | Prior EP-003.2 / EP-006.4 |
| Exam Ready marketing | **Blocked** | Not claimed |
| Claim-window spot-check | **Residual** | Packaged declaration spot-check open |

---

## G7 — Performance — HOLD

| Check | Result | Evidence |
|-------|--------|----------|
| G7.1 CI soft budgets | **Pass** | `tests/ga/test_performance_benchmarks.py` — **13 passed** |
| G7.2 Operator sample / concurrency | **HOLD** | `docs/production/G7_PERFORMANCE_HOLD.md` still in force |
| LIVE Core Web Vitals | **Not measured** | Residual **PX7-R5 / P0021-R5** |
| Asset baseline | **Pass** | tokens 12016 · student.css 46466 · student.js 5814 — unchanged vs PX-007 |
| LIVE health timings | **Sampled** | `knowledge/evidence/releases/P002_1/performance/live_health_timings.txt` (not CWV) |

**Claim restriction:** No high-traffic marketing until HOLD lifted.

---

## G8 — Reliability — PASS WITH RESIDUAL

| Check | Result | Evidence |
|-------|--------|----------|
| LIVE `/health/live` | **Pass** | HTTP 200 · commit `272a095…` · `…/P002_1/health/health_live.json` |
| LIVE `/health/ready` | **Pass** | ready=true · migrations at head · `…/health_ready.json` |
| Sev-1 open | **Pass** | None recorded for claim window |
| Rollback / backup posture | **Pass** | `docs/production/G8_RELIABILITY_EVIDENCE.md` |
| Continue contention LIVE re-measure | **Residual** | **PX7-R6 / P0021-R6** |
| Live restore drill | **Residual** | Optional before GA marketing |

---

## G9 — Production telemetry — PASS WITH RESIDUAL

| Check | Result | Evidence |
|-------|--------|----------|
| Analytics emit flag | **OFF** | `ANALYTICS_EVENTS_V1` OFF in `VERSION_1_FLAG_MATRIX.md` |
| Operational logs | **Pass** | GA observability suite green |
| Live metrics marketing | **Forbidden while OFF** | Claim-safe residual |
| Stale Alpha telemetry allowlist test | **Residual** | `P0021-T3` test debt (not a live-metrics claim) |

---

## G10 — Security / privacy — PASS WITH RESIDUAL

| Check | Result | Evidence |
|-------|--------|----------|
| GA security review | **Pass** | `docs/ga/SECURITY_REVIEW.md` |
| Security automated suite | **Pass** | `tests/ga/test_security_review.py` — **10 passed** |
| Secrets / CSRF / ownership | **Pass** | `docs/production/G10_OPERATIONAL_EVIDENCE.md` |
| Dependency policy | **Pass** | Hard audit + accepted HOLD register |
| Privacy signatures (Stage 1) | **Open residual** | Blocks Stage 1 / expanded cohort — not invite-only Alpha alone |
| CSP `unsafe-inline` | **Accepted residual** | Documented |

---

## G11 — Regression coverage — PASS WITH RESIDUAL

| Pack | Result | Log |
|------|--------|-----|
| Quality + curriculum + GA docs/obs/perf/security | **239 passed** | `regression/pytest_quality_curriculum_ga.txt` |
| Premium core (PX-003 session + PX-004…007) | **72 passed** | `regression/pytest_premium_core.txt` |
| Session / nav / a11y / e2e / recovery | **148 passed · 1 failed** | `regression/pytest_session_nav_a11y.txt` |
| Broader premium+alpha aggregate | **163 passed · 2 failed** | `regression/pytest_premium_aggregate.txt` |

Failures classified as **stale-test debt** (not product Critical/Major): see `P002_1_RESIDUAL_REGISTER.md` P0021-T1…T3.

---

## G12 — Feature-flag readiness — PASS WITH RESIDUAL

| Check | Result | Evidence |
|-------|--------|----------|
| Published matrix | **Pass** | `docs/production/VERSION_1_FLAG_MATRIX.md` |
| Sole runtime ON | **Pass** | Production-ON flags match invite-only claim |
| Twin / Journey / analytics OFF | **Pass** | Must not market as live |
| Product/Release ack for V1 declaration | **Residual** | Required at GO; not sought this exit |

---

## Sign-off (validation)

| Capacity | Decision |
|----------|----------|
| Validation (P-002.1) | Gate board scored with evidence; **NO-GO** for production-ready declaration |
| Founder | **Awaiting review** of scorecard + `P002_1_RELEASE_RECOMMENDATION.md` |

**End of scorecard**
