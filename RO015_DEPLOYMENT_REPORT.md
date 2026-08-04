# RO-015 — Deployment Report

**Programme:** RO-015 — Wave 15 LIVE Release Operations  
**Authority:** EP-001 Wave 15 / HR-015 Publication APPROVED · EF-001 · FP-01  
**Date:** 2026-08-04  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Rho / CS1-017 (CR-D1…CR-R1) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. Continuity wiring registers CR-D1…CR-R1 and prefers the CR chain after CP-/CR- so shared topic codes do not divert onto Opening Front Alpha/Beta honesty-gap inventory. LIVE CP-R1 handoff updated WAVE0 → CR-D1. Tip-complete post-tip front continuity (`pending_post_tip_front_package`) keeps enrolment open for pending CR packages after Memory Front close. LIVE fingerprint matches tip `272a0950ca1a65df01badf5e180c3c06a41681e7`. Inventory hard-assert confirms **130** `publication_approved` CS1 packages including **10** Rho days, with handoff **CP-R1 → CR-D1** and Trust Front / Opening Front cold entries preserved. After LIVE verification PASS, CE-001 Approver credit for 1.1.1–2.1.2 advances Published Coverage to **72 / 72 (100% Approver numerator)** without claiming “100% CS1” product/trust or until-exam trust. Student Reliance remains through Topic **5.1**.

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1 | `CS1-EP001-PKG-CR-1.1-AIMS-ANALYSIS` | CR-D1 | `educational_packages/cs1/cr-1.1.1-aims-analysis-cs1017.json` | `publication_approved` |
| 2 | `CS1-EP001-PKG-CR-1.1-STAGES-TOOLS` | CR-D2 | `…/cr-1.1.2-stages-tools-cs1017.json` | `publication_approved` |
| 3 | `CS1-EP001-PKG-CR-1.1-DATA-SOURCES` | CR-D3 | `…/cr-1.1.3-data-sources-cs1017.json` | `publication_approved` |
| 4 | `CS1-EP001-PKG-CR-1.1-REPRODUCIBLE` | CR-D4 | `…/cr-1.1.4-reproducible-cs1017.json` | `publication_approved` |
| 5 | `CS1-EP001-PKG-CR-1.2-EDA-SUMMARIES` | CR-D5 | `…/cr-1.2.1-eda-summaries-cs1017.json` | `publication_approved` |
| 6 | `CS1-EP001-PKG-CR-1.2-CORRELATION` | CR-D6 | `…/cr-1.2.2-correlation-cs1017.json` | `publication_approved` |
| 7 | `CS1-EP001-PKG-CR-1.2-PCA` | CR-D7 | `…/cr-1.2.3-pca-cs1017.json` | `publication_approved` |
| 8 | `CS1-EP001-PKG-CR-2.1-DISCRETE` | CR-D8 | `…/cr-2.1.1-discrete-cs1017.json` | `publication_approved` |
| 9 | `CS1-EP001-PKG-CR-2.1-CONTINUOUS` | CR-D9 | `…/cr-2.1.2-continuous-cs1017.json` | `publication_approved` |
| 10 | `CS1-EP001-PKG-REV-PUBLICATION-FRONT-RHO` | CR-R1 | `…/cr-revision-publication-front-cs1017.json` | `publication_approved` |

**FP-01:** All **10** activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-rho-cs1017/packages/` remain `campaign_member_certified` (educational fields byte-identical).  
**Campaign status:** `campaign.json` → `released`.  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CR-D1…CR-R1 (121–130); CP-R1 LIVE `tomorrow_preview.next_topic_code` → `CR-D1`; successor preference for CR when last day is `CP-`/`CR-`; post-tip enrolment held open while CR pending.

Activation field changes on live Rho copies only: `status`, `publication_version` (`cs1017-live-1.0.0`), `published_at`.  
LIVE filenames use `cr-` prefix so soft `find_educational_package` first-match does not steal Opening Front cold entries.

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Activation tip (LIVE) | `272a0950ca1a65df01badf5e180c3c06a41681e7` |
| Activation deploy | `dep-d9outfnqj5pc738dl8og` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Trigger | API `clearCache` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health` commit field | `272a0950ca1a…` | match | **PASS** |
| `/health/live` | ok + matching commit | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Evidence: `knowledge/evidence/releases/RO015/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9ov1bfqj5pc738dt4g0` **succeeded**. Tip-matched local loader assert confirms:

- `len(all_approved()) == 130`
- Rho `campaign_day` prefix `CR-` count **10**
- Pi **10** / Omicron **10** / Xi **11** / Nu **6** / Mu **6** / Lambda **9** / Kappa **7** / Iota **7** / Theta **3** / Eta **3** / Zeta **3** / Epsilon **5** / Gamma **5** / Delta **27** unchanged
- No duplicate package IDs
- Opening Front cold entry `syllabus_topic_code=1.1` → **CA-D1** (not Rho)
- Opening Front cold entry `syllabus_topic_code=2.1` → **CB-D2** (not Pi/Rho)
- Trust Front cold entry `syllabus_topic_code=5.1` → **CD-D16**
- Trust Front cold entry `syllabus_topic_code=4.2` → **CD-D6**
- After simulated CP-R1 completion → **CR-D1** / `CS1-EP001-PKG-CR-1.1-AIMS-ANALYSIS`

Evidence: `knowledge/evidence/releases/RO015/inventory_assert_local.txt`, `inventory_payload.json`, `inventory_job_final.json`, `inventory_assert.json`.

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged; live Rho copies metadata-only |
| Wave 16 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — CR day-order + CP/CR successor preference + post-tip Publication Front reachability continuity only |
| Recommendation logic unmodified | **Met** |
| Student Twin unmodified | **Met** |
| PB-017 not executed | **Met** — authorised only on PASS exit |

---

## Deployment verdict

# **PASS — Wave 15 Rho inventory jointly LIVE**

Companion verification: `RO015_LIVE_VERIFICATION_REPORT.md` (**PASS WITH RESIDUAL** — package path).  
Release decision: `RO015_RELEASE_DECISION.md` (authorises PB-017; does not execute it).

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/cr-*-cs1017.json` (10)
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-rho-cs1017/` (authored inventory + `released` campaign status)

## Files Modified

- `app/application/educational_packages/selection.py` — CR-D1…CR-R1 day order + CP/CR → CR successor preference + `pending_publication_front_package` / `pending_post_tip_front_package`
- `app/application/educational_runtime_engine/service.py` — tip-complete post-tip front continuity (CP/CR)
- `app/application/educational_experience/service.py` — allow mission generation when post-tip front pending
- `app/presentation/student/educational_view_models.py` — do not blank post-tip front start when mission open
- `app/curriculum/data/educational_packages/cs1/cp-revision-spine-memory-cs1016.json` — CP-R1 LIVE handoff → CR-D1
- Campaign `campaign.json` status → `released`
- Tests updated for Rho chain / CP-R1 handoff / inventory 130

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 220 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only. PB-002 selection extended for Rho campaign days and Opening Front coexistence on shared topic codes. Educational Framework frozen (EF-001). No Student Twin / recommendation engine changes. Alpha/Beta package bodies unmodified.

## Technical Debt

None introduced by activation itself. Soft title-keyword / Home chrome may still soft-match Opening Front titles while package path delivers Rho (tracked residual). First sitting before Rho chain engagement can briefly deliver non-Rho inventory if mission/regeneration race occurs (RO15-R1). Tip-complete natural students require post-tip continuity wiring for Publication Front.

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification. Seeded Memory Front package history used for Publication Front package-path verification. Student Reliance remains through Topic **5.1** (Publication Front does not invent Topic 5.2 or until-exam trust). Approver numerator may read 72/72 without authorizing a “100% CS1” commercial/trust slogan.

---

### Student Impact Assessment

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Assessment |
|-------|------------|
| **Student problem** | After Memory Front tip at CP-R1, Publication Front / Wave 0 Approver-path LOs 1.1.1–2.1.2 remained unpublished — Day-1 Approver-credit honesty gap stayed open. |
| **Student benefit** | Diligent students finishing CP-R1 can now receive jointly activated CR-D1…CR-R1 Publication Front packages on LIVE (package path). |
| **Learning benefit** | Contiguous CMP-partnered study of aims → stages/tools → sources → reproducibility → EDA → correlation → PCA → discrete → continuous + Revision under one Sensei. |
| **Success metrics** | Inventory 130 approved / 10 Rho; CP-R1→CR-D1 selection; package-path sittings without fallback; Coverage Approver numerator 72/72 after LIVE verify; Reliance held through 5.1. |
| **Risks** | Home chrome soft-match residual; first-sitting race residual; Wave 0 Alpha/Beta honesty-gap packages remain unmodified inventory. |
| **Assumptions** | HR-015 APPROVE; FP-01 joint activation; CE-001 Approver credit after LIVE Verified; no until-exam / spine PASS / 100% CS1 slogan claims. |

### Estimated KSI contribution

ΔKSI = **0** — operations activation / LIVE verify; no validated product-success metric change claimed beyond educational inventory LIVE + Approver numerator honesty.

### Evidence collected

- `knowledge/evidence/releases/RO015/`
- `RO015_LIVE_VERIFICATION_REPORT.md` · `RO015_RELEASE_DECISION.md`

### Lessons learned for student value

Publication Front after Memory Front tip is unreachable if enrolment closes on syllabus_complete without post-tip continuity. Approver credit for opening LOs is lawful only after LIVE Verified package-path evidence — catalogue APPROVE alone must not move the numerator.

### Explainability Review

N/A — ops continuity / inventory; no new opaque recommendation scores.

### Recommendation Quality Review

N/A — no recommendation ranking redesign.

### Version 1 readiness residual

N/A for V1 production-ready declaration. Gate G1 not closed by Wave 15 alone.

### CRI domains improved

None validated.

### Estimated CRI delta

ΔCRI = **0**.
