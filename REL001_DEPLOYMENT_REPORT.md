# REL-001 — Deployment Report

**Programme:** REL-001 — Early Access Baseline Release  
**Authority:** PB-017 PASS · Educational Content Freeze · EF-001 · PX-007 Premium Conditional PASS · P-002.1 Release Readiness · OP-001 · OP-002 · EA-001  
**Date:** 2026-08-04  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operational release only — no new features; educational packages / Runtime redesign / Recommendation / Twin / Curriculum / EF unchanged under this programme  

---

## Summary

REL-001 committed the validated Premium Experience + Early Access ops baseline on `main`, tagged `rel-001`, and deployed to the production Render service. LIVE fingerprint matches tip `95a82b04ae50d32003add3a2f5e6789005a4c962`. Health / ready / migrations gates passed. LIVE smoke walkthrough **PASS** (19/19). Early Access invitations remain **stopped** pending Founder approval.

---

## Pre-release verification

| Check | Result |
|-------|--------|
| Educational Content Freeze | **Held** — no `educational_packages` / campaign JSON in release commit |
| Unintended package modifications | **None** |
| Unfinished experimental work | **Excluded** — campaign generator scripts and unrelated CS wave paperwork left unstaged |
| Application starts | **PASS** (`create_app()`) |
| Migrations at head (repo + LIVE) | **PASS** — `202607310002` |
| Release test suites | **PASS** — architecture, student workflow, alpha smoke, PX packs |
| Legacy `tests/test_smoke.py` wizard | **Residual** — fails on prior tip `272a095` as well; not introduced by REL-001; not fixed (no opportunistic code changes) |

---

## Git

| Field | Value |
|-------|--------|
| Branch | `main` |
| Release commit | `95a82b04ae50d32003add3a2f5e6789005a4c962` |
| Message | `REL-001: Early Access Baseline Release` |
| Tag | `rel-001` (annotated) |
| Prior tip (rollback) | `272a0950ca1a65df01badf5e180c3c06a41681e7` |

---

## Deployment

| Field | Value |
|-------|--------|
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Trigger | API `clearCache` |
| Deploy ID | `dep-d9p4a85bedkc73e3aa9g` |
| Status | `live` |
| Finished (UTC) | `2026-08-04T20:06:12.278143Z` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health` commit | `95a82b04ae50…` | match | **PASS** |
| `/health/live` | ok + matching commit | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Evidence: `knowledge/evidence/releases/REL001/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Smoke test summary

| Area | Result |
|------|--------|
| Login | **PASS** |
| Student Home | **PASS** |
| Mission flow (`POST /student/session/start`) | **PASS** |
| Continue Session (overview) | **PASS** |
| Session completion surface | **PASS** |
| Educational package loading (activity) | **PASS** |
| Dashboard surfaces (history/journey/profile/settings) | **PASS** |
| Critical regressions | **None observed** |
| Overall | **PASS** (19/19) |

Detail: `REL001_SMOKE_TEST_REPORT.md` · `knowledge/evidence/releases/REL001/smoke_results.json`.

---

## Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| No new features under REL-001 | **Met** — ship of already-validated WT only |
| Educational packages unmodified | **Met** |
| Runtime redesign | **Not performed** — prior PX continuity/presentation fixes only in baseline |
| Recommendation Engine unmodified | **Met** |
| Student Twin unmodified | **Met** |
| Curriculum unmodified | **Met** |
| Educational Framework unmodified | **Met** |
| No code changes solely to green deploy | **Met** |

---

## Known residuals

1. Version 1 production-ready **not declared** (P-002.1 G1 FAIL · G7 HOLD).  
2. PX-007 Premium Experience remains **Conditional PASS** (LIVE CWV / screenshot gallery / AT recording residuals).  
3. KSI-003 educational effectiveness remains **NO-GO / Pending Evidence**.  
4. Legacy wizard smoke tests fail on both prior and new tips (test hygiene residual).  
5. EA-001 Invited / Accepted / Activated remain **0** until Founder-authorised sends.  

---

## Rollback reference

Redeploy commit `272a0950ca1a65df01badf5e180c3c06a41681e7` (RO-015 LIVE). No Alembic reverse required for REL-001. Confirm `/health/ready` + commit before any invite traffic.

---

## Deployment verdict

# **PASS — Early Access Baseline LIVE**

**STOP.** Await Founder approval before sending the first Early Access invitations.

---

## Files Created

- `REL001_DEPLOYMENT_REPORT.md` (this file)
- `REL001_RELEASE_NOTES.md`
- `REL001_SMOKE_TEST_REPORT.md`
- `REL001_BASELINE_FINGERPRINT.md`
- `knowledge/evidence/releases/REL001/` (health, deploy, smoke evidence)

## Files Modified

Application / ops / Premium evidence shipped in release commit `95a82b0` (see that commit). Report commit may add only REL001 artefacts.

## Tests Executed

- Local: architecture + student workflow + alpha smoke + PX packs — **PASS**
- LIVE: health/ready/fingerprint — **PASS**
- LIVE: student smoke journey — **PASS** (19/19)

## Migration Impact

None (no new Alembic revisions).

## Architecture Compliance

Layering preserved. Curriculum V1/V2 untouched. Educational Content Freeze held. EF-001 held.

## Technical Debt

Legacy `tests/test_smoke.py` wizard assertions stale relative to current wizard validation — residual only.

## Student Impact Assessment

| Dimension | Assessment |
|-----------|------------|
| Student problem | External Early Access students need a single stable LIVE baseline |
| Student benefit | Premium Conditional PASS experience + full CS1 Approver inventory on production |
| Learning benefit | Unlocks ops enrolment under OP-001 without product churn mid-cohort |
| Success metrics | Health/ready green; smoke PASS; fingerprint matches tag |
| Risks | Invites before Founder approval; over-claiming Version 1 readiness |
| Assumptions | Founder will gate invites; content freeze remains held during cohort |

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`.

## Estimated KSI contribution

ΔKSI = **0** — operational release of already-validated capability; no new educational-effectiveness evidence.

## Evidence collected

- `knowledge/evidence/releases/REL001/`
- Prior: `PX007/`, `P002_1/`, `PB017/`, `OP001/`, `EA001/`, `RO015/`

## Lessons learned for student value

A frozen educational inventory plus Premium Conditional PASS can be operated as an Early Access baseline without declaring Version 1 production-ready — ops readiness ≠ effectiveness GO.

## Explainability Review

N/A — no student-facing intelligence ranking/prediction changes in REL-001 programme execution.

## Recommendation Quality Review

N/A — Recommendation Engine unmodified.

## Version 1 readiness residual

G1 FAIL · G7 HOLD remain (per P-002.1). REL-001 does **not** claim Version 1 production-ready.

## CRI domains improved

None (ops release; ΔCRI = 0).

## Estimated CRI delta

ΔCRI = **0**.

## Evidence supporting the increase

N/A.

## Remaining blockers

G1 validated KSI; G7 LIVE performance sample; Founder invite gate.

## Provisional or validated

Fingerprint and smoke are **validated** LIVE. Version 1 declaration remains **not authorised**.
