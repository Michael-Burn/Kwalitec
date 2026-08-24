# RO-014 — Deployment Report

**Programme:** RO-014 — Wave 14 LIVE Release Operations  
**Authority:** EP-001 Wave 14 / HR-014 Publication APPROVED · EF-001 · FP-01  
**Date:** 2026-08-04  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Pi / CS1-016 (CP-D1…CP-R1) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. Continuity wiring registers CP-D1…CP-R1 and prefers the CP chain after CO-/CP- so shared topic codes do not divert onto Opening/Trust Front inventory. A tip-complete Memory Front reachability continuity fix (`4ff8c95…`) keeps enrolment open for pending CP packages. LIVE fingerprint matches tip `4ff8c95d2b853114f0b99ba2d7d23ea847c62819`. Inventory hard-assert confirms **120** `publication_approved` CS1 packages including **10** Pi days, with handoff **CO-R1 → CP-D1** and Trust Front cold entries preserved. Published Coverage remains **63 / 72 (87.5%)**.

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1 | `CS1-EP001-PKG-CP-2.1-PROB-QUANTILES` | CP-D1 | `educational_packages/cs1/cp-2.1.3-prob-quantiles-cs1016.json` | `publication_approved` |
| 2 | `CS1-EP001-PKG-CP-2.2-MARGINAL-CONDITIONAL` | CP-D2 | `…/cp-2.2.1-marginal-conditional-cs1016.json` | `publication_approved` |
| 3 | `CS1-EP001-PKG-CP-2.5-CLT` | CP-D3 | `…/cp-2.5.1-clt-cs1016.json` | `publication_approved` |
| 4 | `CS1-EP001-PKG-CP-2.6-RANDOM-SAMPLES` | CP-D4 | `…/cp-2.6.1-random-samples-cs1016.json` | `publication_approved` |
| 5 | `CS1-EP001-PKG-CP-3.1-ESTIMATORS` | CP-D5 | `…/cp-3.1.1-estimators-cs1016.json` | `publication_approved` |
| 6 | `CS1-EP001-PKG-CP-3.2-CI-SAMPLE` | CP-D6 | `…/cp-3.2.1-ci-sample-cs1016.json` | `publication_approved` |
| 7 | `CS1-EP001-PKG-CP-3.3-HYPOTHESIS-TESTING` | CP-D7 | `…/cp-3.3.1-hypothesis-testing-cs1016.json` | `publication_approved` |
| 8 | `CS1-EP001-PKG-CP-4.1-LINEAR-REGRESSION` | CP-D8 | `…/cp-4.1.1-linear-regression-cs1016.json` | `publication_approved` |
| 9 | `CS1-EP001-PKG-CP-5.1-BAYES-THEOREM` | CP-D9 | `…/cp-5.1.1-bayes-theorem-cs1016.json` | `publication_approved` |
| 10 | `CS1-EP001-PKG-REV-SPINE-MEMORY-PI` | CP-R1 | `…/cp-revision-spine-memory-cs1016.json` | `publication_approved` |

**FP-01:** All **10** activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-pi-cs1016/packages/` remain `campaign_member_certified` (educational fields byte-identical).  
**Campaign status:** `campaign.json` → `released`.  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CP-D1…CP-R1 (111–120); CO-R1 LIVE `tomorrow_preview.next_topic_code` → `CP-D1`; successor preference for CP when last day is `CO-`/`CP-`; tip-complete enrolment held open while CP pending.

Activation field changes on live Pi copies only: `status`, `publication_version` (`cs1016-live-1.0.0`), `published_at`.  
LIVE filenames use `cp-` prefix so soft `find_educational_package` first-match does not steal Opening/Trust Front cold entries.

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Activation tip | `667784f6811e3d7bb322f375928646d3382d40bd` |
| Continuity tip (LIVE) | `4ff8c95d2b853114f0b99ba2d7d23ea847c62819` |
| Activation deploy | `dep-d9oq45flk1mc739pad60` |
| Continuity deploy | `dep-d9oqhe0ae00c73b55i7g` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Trigger | API `clearCache` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health` commit field | `4ff8c95d2b85…` | match | **PASS** |
| `/health/live` | ok + matching commit | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Evidence: `knowledge/evidence/releases/RO014/health.json`, `health_ready.json`, `health_live.json`, `deploy_status2.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9oqa91t0dsc73blb8o0` **succeeded**. Tip-matched local loader assert confirms:

- `len(all_approved()) == 120`
- Pi `campaign_day` prefix `CP-` count **10**
- Omicron **10** / Xi **11** / Nu **6** / Mu **6** / Lambda **9** / Kappa **7** / Iota **7** / Theta **3** / Eta **3** / Zeta **3** / Epsilon **5** / Gamma **5** / Delta **27** unchanged
- No duplicate package IDs
- Trust Front cold entry `syllabus_topic_code=5.1` → **CD-D16**
- Trust Front cold entry `syllabus_topic_code=4.2` → **CD-D6**
- After simulated CO-R1 completion → **CP-D1** / `CS1-EP001-PKG-CP-2.1-PROB-QUANTILES`
- Opening Front cold entry `2.1` does **not** resolve to Pi

Evidence: `knowledge/evidence/releases/RO014/inventory_assert_local.txt`, `inventory_payload.json`, `inventory_job_final.json`, `inventory_assert.json`.

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged; live Pi copies metadata-only |
| Wave 15 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — CP day-order + CO/CP successor preference + tip-complete Memory Front reachability continuity only |
| Recommendation logic unmodified | **Met** |
| Student Twin unmodified | **Met** |
| PB-016 not executed | **Met** — authorised only on PASS exit |

---

## Deployment verdict

# **PASS — Wave 14 Pi inventory jointly LIVE**

Companion verification: `RO014_LIVE_VERIFICATION_REPORT.md` (**PASS WITH RESIDUAL** — package path).  
Release decision: `RO014_RELEASE_DECISION.md` (authorises PB-016; does not execute it).

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/cp-*-cs1016.json` (10)
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-pi-cs1016/` (authored inventory + `released` campaign status)
- `scripts/generate_cs1016_campaign.py`

## Files Modified

- `app/application/educational_packages/selection.py` — CP-D1…CP-R1 day order + CO/CP → CP successor preference + `pending_memory_front_package`
- `app/application/educational_runtime_engine/service.py` — tip-complete Memory Front continuity
- `app/application/educational_experience/service.py` — allow mission generation when Memory Front pending
- `app/presentation/student/educational_view_models.py` — do not blank Memory Front start when mission open
- `app/curriculum/data/educational_packages/cs1/revision-bayesian-cs1015.json` — CO-R1 LIVE handoff → CP-D1
- Campaign `campaign.json` status → `released`
- Tests updated for Pi chain / CO-R1 handoff / inventory 120

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py \
       tests/certification/test_cs09_journey_e2e.py -q
→ 212 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only. PB-002 selection extended for Pi campaign days and Opening/Trust Front coexistence on shared topic codes. Educational Framework frozen (EF-001). No Student Twin / recommendation engine changes.

## Technical Debt

None introduced by activation itself. Soft title-keyword / Home chrome may still soft-match Opening Front titles while package path delivers Pi (tracked residual). Tip-complete natural students required continuity fix `4ff8c95…` before Memory Front missions regenerate.

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification. Seeded Continuity Front package history used for Memory Front package-path verification. Published Coverage remains **63 / 72** (hinges already counted). Student Reliance remains through Topic **5.1** (Memory Front does not invent Topic 5.2).

---

### Student Impact Assessment

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Assessment |
|-------|------------|
| **Student problem** | After Continuity Front tip at 5.1, Memory Front spine re-audit was unpublished — hinge retrieval risked decay without a lawful CP path. |
| **Student benefit** | Diligent students finishing CO-R1 can now receive jointly activated CP-D1…CP-R1 Memory Front packages on LIVE (package path). |
| **Learning benefit** | Contiguous CMP-partnered retrieval across Opening→joint→CLT→sampling→estimators→CI→HT→regression→Bayes hinges + Revision under one Sensei. |
| **Success metrics** | Inventory 120 approved / 10 Pi; CO-R1→CP-D1 selection; package-path sittings without fallback; Coverage held 63/72; Reliance held through 5.1. |
| **Risks** | Home chrome soft-match residual; tip-complete path needed continuity fix; Wave 0 honesty gap remains. |
| **Assumptions** | HR-014 APPROVE; FP-01 joint activation; CE-001 forbids Approver double-count of hinges. |

### Estimated KSI contribution

ΔKSI = **0** — operations activation / LIVE verify; no validated product-success metric change claimed beyond educational inventory LIVE.

### Evidence collected

- `knowledge/evidence/releases/RO014/`
- `RO014_LIVE_VERIFICATION_REPORT.md` · `RO014_RELEASE_DECISION.md`

### Lessons learned for student value

Memory Front after tip close is unreachable if enrolment is closed on syllabus_complete. Continuity wiring must keep Memory Front sittings reachable without inventing Topic 5.2 or claiming spine PASS.

### Explainability Review

N/A — ops continuity / inventory; no new opaque recommendation scores.

### Recommendation Quality Review

N/A — no recommendation ranking redesign.

### Version 1 readiness residual

N/A for V1 production-ready declaration. Gate G1 not closed by Wave 14 alone.

### CRI domains improved

None validated.

### Estimated CRI delta

ΔCRI = **0**.
