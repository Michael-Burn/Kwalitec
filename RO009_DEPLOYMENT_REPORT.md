# RO-009 — Deployment Report

**Programme:** RO-009 — Wave 9 LIVE Release Operations  
**Authority:** EP-001 Wave 9 / HR-009 Publication APPROVED · EF-001  
**Date:** 2026-08-02  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Lambda / CS1-011 (CL-D1…CL-R1) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. LIVE fingerprint matches tip `518467508e27b609c60e4eb5fe0410ea5c868314`. Inventory hard-assert confirms **77** `publication_approved` CS1 packages including **9** Lambda days, with Continuity Front handoff **CK-R1 → CL-D1** and cold entry at **3.2 → CL-D1**. Continuity wiring extends `_CAMPAIGN_DAY_ORDER` with CL-D1…CL-R1 (indices 69–77) — same class of ops prerequisite as RO-001…RO-008 day-order registration, not a Runtime redesign. Kappa (7), Iota (7), Theta (3), Eta (3), Zeta (3), Epsilon (5), Gamma (5), and Delta (27) inventory counts unchanged.

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1 | `CS1-EP001-PKG-3.2-CONFIDENCE-INTERVAL-PARAMETER` | CL-D1 | `educational_packages/cs1/3.2.1-confidence-interval-parameter-cs1011.json` | `publication_approved` |
| 2 | `CS1-EP001-PKG-3.2-PREDICTION-INTERVAL` | CL-D2 | `…/3.2.2-prediction-interval-cs1011.json` | `publication_approved` |
| 3 | `CS1-EP001-PKG-3.2-CI-GIVEN-SAMPLING-DISTRIBUTION` | CL-D3 | `…/3.2.3-ci-given-sampling-distribution-cs1011.json` | `publication_approved` |
| 4 | `CS1-EP001-PKG-3.2-CI-NORMAL-MEAN-VARIANCE` | CL-D4 | `…/3.2.4-ci-normal-mean-variance-cs1011.json` | `publication_approved` |
| 5 | `CS1-EP001-PKG-3.2-CI-BINOMIAL-POISSON` | CL-D5 | `…/3.2.5-ci-binomial-poisson-cs1011.json` | `publication_approved` |
| 6 | `CS1-EP001-PKG-3.2-CI-TWO-SAMPLE` | CL-D6 | `…/3.2.6-ci-two-sample-cs1011.json` | `publication_approved` |
| 7 | `CS1-EP001-PKG-3.2-CI-PAIRED-MEANS` | CL-D7 | `…/3.2.7-ci-paired-means-cs1011.json` | `publication_approved` |
| 8 | `CS1-EP001-PKG-3.2-BOOTSTRAP-CONFIDENCE-INTERVAL` | CL-D8 | `…/3.2.8-bootstrap-confidence-interval-cs1011.json` | `publication_approved` |
| 9 | `CS1-EP001-PKG-REV-CONFIDENCE-INTERVALS` | CL-R1 | `…/revision-confidence-intervals-cs1011.json` | `publication_approved` |

**FP-01:** All **9** activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-lambda-cs1011/packages/` remain `campaign_member_certified` (bodies untouched).  
**Campaign status:** `campaign.json` → `released`.  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CL-D1…CL-R1 (69–77).

Activation field changes on live copies only: `status`, `publication_version` (`cs1011-live-1.0.0`), `published_at`.

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Tip | `518467508e27b609c60e4eb5fe0410ea5c868314` |
| Push | `17edcdc..5184675` → `origin/main` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9njjqm7bikc73c2i86g` |
| Trigger | API `clearCache` |
| Status progression | `build_in_progress` → … → `live` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health.commit` | `518467508e27b609…` | match | **PASS** |
| `/health/live` | ok | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Evidence: `knowledge/evidence/releases/RO009/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9njlr5aeets73c3bihg` **succeeded**. Tip-matched local loader assert confirms:

- `len(all_approved()) == 77`
- Lambda `campaign_day` prefix `CL-` count **9**
- Kappa **7** / Iota **7** / Theta **3** / Eta **3** / Zeta **3** / Epsilon **5** / Gamma **5** / Delta **27** unchanged
- No duplicate package IDs
- Cold entry `syllabus_topic_code=3.2` → **CL-D1**
- After simulated CK-R1 completion → **CL-D1** / `CS1-EP001-PKG-3.2-CONFIDENCE-INTERVAL-PARAMETER`
- Kappa regression: `3.1` → **CK-D1**
- Iota regression: `2.6` → **CI-D1**
- Theta regression: `2.5` → **CT-D1**
- Eta regression: `2.4` → **CH-D1**
- Zeta regression: `2.3` → **CZ-D1**
- Epsilon regression: `2.2` → **CE-D1**
- Trust Front regression: `4.1` → **CD-D1**

Evidence: `knowledge/evidence/releases/RO009/inventory_assert.json`.

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged; live copies metadata-only |
| Wave 10 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — only CL day-order registration |
| Recommendation logic unmodified | **Met** |
| RO1-R1 tomorrow chrome path preserved | **Met** — chrome binding unchanged; residuals tracked as presentation |
| PB-011 not executed | **Met** — authorised only on PASS exit |

---

## Deployment verdict

# **PASS — Wave 9 Lambda inventory jointly LIVE**

Companion verification: `RO009_LIVE_VERIFICATION_REPORT.md`.  
Release decision: `RO009_RELEASE_DECISION.md` (authorises PB-011; does not execute it).

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/3.2.*-cs1011.json` (8)
- `app/curriculum/data/educational_packages/cs1/revision-confidence-intervals-cs1011.json`
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-lambda-cs1011/` (authored inventory + `released` campaign status)

## Files Modified

- `app/application/educational_packages/selection.py` — CL-D1…CL-R1 day order
- Campaign `campaign.json` status → `released`
- Tests updated for Lambda chain / CK-R1 handoff / topic 3.2 entry

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 155 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only. PB-002 selection extended for Lambda campaign days only. Educational Framework frozen (EF-001). No Student Twin / recommendation engine changes.

## Technical Debt

None introduced by activation itself. Soft title-keyword package resolution remains ambiguous across large inventory (pre-existing). Observed Continuity Front label desync during multi-day ops walks (expected labels briefly ahead of true package) — same class as RO-004…RO-008; package path verified by syllabus-code / Topic-Mission continuation.

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification; students in production still face one-mission-per-calendar-day pacing. Published Baseline picker offers section codes — Continuity Front LIVE entry for Topic 3.2 uses section **3** (natural progression through 3.1 then 3.2).

---

## Student Impact Assessment

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Assessment |
|-------|------------|
| **Student problem** | Continuity Front after Kappa stopped at 3.1 / CK-R1; intervals (3.2) unpublished LIVE. |
| **Student benefit** | Diligent students can study approved Lambda days with CMP partnership on LIVE after Kappa. |
| **Learning benefit** | Contiguous CMP-partnered parameter CI → prediction → given sampling distribution → Normal mean/var → binomial/Poisson → two-sample → paired → bootstrap CI → Revision under one Sensei. |
| **Success metrics** | Deploy PASS · LIVE verify PASS WITH RESIDUAL · 0 fallback on true Lambda path · coverage **58 / 72**. |
| **Risks** | Over-claiming until-exam trust; label desync RO9-R1; chrome / Q6 residual. |
| **Assumptions** | Continuity Front entry via continue at section 3; CMP remains external authority. |

## Estimated KSI contribution

ΔKSI = **0** (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

## Evidence collected

`knowledge/evidence/releases/RO009/` · deploy `dep-d9njjqm7bikc73c2i86g` · assert job `job-d9njlr5aeets73c3bihg` · student provision `job-d9njlglaeets73c3auvg`.

## Lessons learned for student value

Joint activation of a Continuity Front extension works when FP-01 is held and CK-R1 → CL-D1 selection is explicit after Kappa. Ops label desync can mislabel expected-day detectors without corrupting session substance — keep those residuals separate from package-path trust. Progressive confidence must stay scoped to LIVE-certified inventory and run as PB-011.

## Explainability Review

N/A — no intelligence change.

## Recommendation Quality Review

N/A — no ranking change.

## Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. Wave 10 geography still unpublished. RO9-R1 open (PI). PB-011 not yet executed.

## CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-009 · 2026-08-02  
**Wave 9 LIVE status:** Deployment **PASS** · companion LIVE verification required for release acceptance
