# RC2_SPRINT_D_DEPLOYMENT_REPORT.md

**Programme:** VERSION1-RC2 — Sprint D — LIVE Educational Trust Verification  
**Authority:** EF-001 · EC-001 PASS · RC2 Sprint C1 PASS  
**Classification:** PI-S1  
**Date:** 2026-08-01  
**Host:** https://kwalitec.onrender.com  
**Nature:** Deployment and verification only — educational content, Educational Framework, Runtime, SCI, and recommendation engine unmodified  

---

## Summary

Sprint C1 tip `94e02f57669831ff6af4e6f6bf87a727ca0cfe38` was pushed to `origin/main`, deployed to Render service `kwalitec`, and fingerprint-matched on LIVE. Migrations remain at head `202607310002`. Health endpoints PASS. LIVE loader inventory asserts **9** `publication_approved` CS1 packages. Fresh-student Reading verification (companion `PB001A_LIVE_VERIFICATION_REPORT.md`) confirms certified EC-001 Guided Reading on published spine topics. PB-001 findings F1 and F2 are closable; full PB-001 rerun is authorised.

---

## Phase 1 — Deployment

### Repository

| Field | Value |
|-------|-------|
| Branch | `main` |
| Sprint C1 feature commit | `afa0010d27dbb43d3491cc7f305e8cb1334f9d18` |
| Tip (docs hash record) | `94e02f57669831ff6af4e6f6bf87a727ca0cfe38` |
| Push | `d8670d5..94e02f5` → `origin/main` |
| Application version | `2.0.0-beta.1` |
| Alembic head | `202607310002` (unchanged; no new migrations) |

Sprint C1 was already committed locally before this sprint; Phase 1 committed no additional application change beyond that tip. Untracked prior audit/evidence docs were left unstaged.

### Render deploy

| Field | Value |
|-------|-------|
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9ms5o6417fc73c3v1h0` |
| Trigger | Manual API `clearCache` deploy of latest `main` |
| Deploy commit | `94e02f57669831ff6af4e6f6bf87a727ca0cfe38` |
| Status progression | `build_in_progress` → `pre_deploy_in_progress` → `update_in_progress` → `live` |

### Fingerprint and health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health.commit` | `94e02f57669831ff6af4e6f6bf87a727ca0cfe38` | match | **PASS** |
| `/health/live` | `status=ok` | ok | **PASS** |
| `/health/ready` | `ready=true` | true | **PASS** |
| `/health` | `status=ok`, DB connected, `environment=production` | ok | **PASS** |
| Migrations | `current=head=202607310002` | match | **PASS** |
| Version | `2.0.0-beta.1` | match | **PASS** |

Evidence: `knowledge/evidence/releases/RC2_SPRINT_D/health.json`, `health_ready.json`.

### LIVE publication inventory (ops assert)

Render one-off job `job-d9ms9qu417fc73c487p0` **succeeded** asserting:

- `EducationalPackageLoader().all_approved()` length **9**
- `find_educational_package` non-None for `1.1`, `1.2`, `2.1`, `4.2`, `CA-R1`, `CB-R1`
- `find_educational_package` **None** for control `4.1`

---

## Phase 2 — Educational delivery (summary)

Full student-path matrix: `PB001A_LIVE_VERIFICATION_REPORT.md`.  
Evidence root: `knowledge/evidence/releases/RC2_SPRINT_D/`.

| Published topic | LIVE Reading | Verdict |
|-----------------|--------------|---------|
| 1.1 | EC-001 Guided Reading package (natural cold-start) | **PASS** |
| 1.2 | EC-001 Guided Reading (first-match summaries; KI-H4) | **PASS** |
| 2.1 | EC-001 Guided Reading (first-match discrete; KI-H4) | **PASS** |
| 4.2 | EC-001 remediated Guided Reading | **PASS** |
| CA-R1 / CB-R1 | Loader inventory resolve (campaign day codes) | **PASS** |
| 4.1 control | Fallback LO shell (correct) | **PASS** |

---

## Phase 3 — Decision

| Gate | Result |
|------|--------|
| LIVE commit matches Git tip | **PASS** |
| Migrations current | **PASS** |
| Health PASS | **PASS** |
| Published Reading = certified package (not fallback) | **PASS** |
| Close PB-001 F1 / F2 | **YES** |
| Authorise full PB-001 rerun | **YES** |

See `EDUCATIONAL_TRUST_RELEASE_DECISION.md`.

---

## Files Created

- `RC2_SPRINT_D_DEPLOYMENT_REPORT.md`
- `PB001A_LIVE_VERIFICATION_REPORT.md`
- `EDUCATIONAL_TRUST_RELEASE_DECISION.md`
- `knowledge/evidence/releases/RC2_SPRINT_D/**`

## Files Modified

None (application / curriculum / Runtime intentionally untouched under this mission).

## Tests Executed

- LIVE `/health`, `/health/live`, `/health/ready` probes — PASS  
- Render inventory assert job — succeeded  
- Fresh Internal Alpha Reading walks (browserless) — PASS (see verification report)  
- No pytest re-run required (deploy/verify only; tip already green under Sprint C1)

## Migration Impact

None.

## Architecture Compliance

- No Runtime / blueprint / template / SCI / recommendation / Educational Framework edits.  
- Curriculum V1/V2 discovery unchanged.  
- EA-006 live loader contract observed on LIVE (only `educational_packages/` + `publication_approved`).

## Technical Debt

- KI-H4 residual: shared `topic_code` `1.2` / `2.1` still first-match only on LIVE (association/PCA/continuous packs jointly registered but not selected on bare code).  
- Revision packs `CA-R1` / `CB-R1` are loader-reachable but not Baseline-seedable as curriculum leaves; student path requires campaign progression.

## Known Limitations

- Screenshot PNGs not generated (Playwright/Chrome unavailable); HTML captures are authoritative.  
- One early Study 1.1 capture during a delayed batch walk showed empty mission title / fallback; fresh natural cold-start (`study11c`) and seeded 1.1 (`study11b`) both PASS — authoritative evidence is the fresh captures.

---

## Student Impact Assessment

- **Student problem:** Prior LIVE tip served fallback / pre-EC-001 Reading on published topics.  
- **Student benefit:** Diligent students on LIVE now receive EC-001 CMP partnership Guided Reading on published packages.  
- **Learning benefit:** Official CMP use is instructed by certified packages on the production host.  
- **Success metrics:** Fingerprint match; 9 live packs; Reading checklist PASS on 1.1/1.2/2.1/4.2; F1/F2 closed.  
- **Risks:** KI-H4 day-key selection; campaign revision days not exercisable via Baseline seed.  
- **Assumptions:** CS1 CMP remains authoritative external text; PB-001 full cohort will re-test the trust claim on this tip.

### Estimated KSI contribution

ΔKSI = 0 (deploy/verify). Enables subsequent validated KSI movement once PB-001 rerun completes.

### Evidence collected

- `knowledge/evidence/releases/RC2_SPRINT_D/`  
- Deploy `dep-d9ms5o6417fc73c3v1h0`  
- Inventory job `job-d9ms9qu417fc73c487p0`

### Lessons learned for student value

Publication activation only changes student Reading after the tip is on LIVE. Fingerprint + fresh-student HTML are the trust bar; tip-local audits alone are insufficient.

### Explainability Review

N/A — no intelligence change.

### Recommendation Quality Review

N/A — no ranking/selection change.

### Version 1 readiness residual

Educational LIVE delivery gate advanced; full adversarial claim re-test (PB-001 rerun) remains. KI-H4 day-key support still open.

### CRI domains / ΔCRI

ΔCRI = 0 provisional pending PB-001 rerun evidence package.

---

## Stop

Sprint D deployment complete. Do not modify educational content or Runtime under this mission ID.
