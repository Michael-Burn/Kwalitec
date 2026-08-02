# RO-008 — Deployment Report

**Programme:** RO-008 — Wave 8 LIVE Release Operations  
**Authority:** EP-001 Wave 8 / HR-008 Publication APPROVED · EF-001  
**Date:** 2026-08-02  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Kappa / CS1-010 (CK-D1…CK-R1) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. LIVE fingerprint matches tip `28a06b176cd1ca1249cc74de0726e5d8c46f5982`. Inventory hard-assert confirms **68** `publication_approved` CS1 packages including **7** Kappa days, with Continuity Front handoff **CI-R1 → CK-D1** and cold entry at **3.1 → CK-D1**. Continuity wiring extends `_CAMPAIGN_DAY_ORDER` with CK-D1…CK-R1 (indices 62–68) — same class of ops prerequisite as RO-001…RO-007 day-order registration, not a Runtime redesign. Iota (7), Theta (3), Eta (3), Zeta (3), Epsilon (5), Gamma (5), and Delta (27) inventory counts unchanged.

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1 | `CS1-EP001-PKG-3.1-METHOD-OF-MOMENTS` | CK-D1 | `educational_packages/cs1/3.1.1-method-of-moments-cs1010.json` | `publication_approved` |
| 2 | `CS1-EP001-PKG-3.1-MAXIMUM-LIKELIHOOD` | CK-D2 | `…/3.1.2-maximum-likelihood-cs1010.json` | `publication_approved` |
| 3 | `CS1-EP001-PKG-3.1-EFFICIENCY-BIAS-CONSISTENCY-MSE` | CK-D3 | `…/3.1.3-efficiency-bias-consistency-mse-cs1010.json` | `publication_approved` |
| 4 | `CS1-EP001-PKG-3.1-COMPARISON-MSE` | CK-D4 | `…/3.1.4-comparison-mse-cs1010.json` | `publication_approved` |
| 5 | `CS1-EP001-PKG-3.1-ASYMPTOTIC-MLE` | CK-D5 | `…/3.1.5-asymptotic-mle-cs1010.json` | `publication_approved` |
| 6 | `CS1-EP001-PKG-3.1-BOOTSTRAP-ESTIMATOR` | CK-D6 | `…/3.1.6-bootstrap-estimator-cs1010.json` | `publication_approved` |
| 7 | `CS1-EP001-PKG-REV-ESTIMATORS` | CK-R1 | `…/revision-estimators-cs1010.json` | `publication_approved` |

**FP-01:** All **7** activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-kappa-cs1010/packages/` remain `campaign_member_certified` (bodies untouched).  
**Campaign status:** `campaign.json` → `released`.  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CK-D1…CK-R1 (62–68).

Activation field changes on live copies only: `status`, `publication_version` (`cs1010-live-1.0.0`), `published_at`.

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Tip | `28a06b176cd1ca1249cc74de0726e5d8c46f5982` |
| Push | `1c747f3..28a06b1` → `origin/main` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9nhl65aeets73bvaabg` |
| Trigger | API `clearCache` |
| Status progression | `build_in_progress` → … → `live` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health.commit` | `28a06b176cd1…` | match | **PASS** |
| `/health/live` | ok | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Evidence: `knowledge/evidence/releases/RO008/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9nhpfajnfac73b47gv0` **succeeded**. Tip-matched local loader assert confirms:

- `len(all_approved()) == 68`
- Kappa `campaign_day` prefix `CK-` count **7**
- Iota **7** / Theta **3** / Eta **3** / Zeta **3** / Epsilon **5** / Gamma **5** / Delta **27** unchanged
- Cold entry `syllabus_topic_code=3.1` → **CK-D1**
- After simulated CI-R1 completion → **CK-D1** / `CS1-EP001-PKG-3.1-METHOD-OF-MOMENTS`
- Iota regression: `2.6` → **CI-D1**
- Theta regression: `2.5` → **CT-D1**
- Eta regression: `2.4` → **CH-D1**
- Zeta regression: `2.3` → **CZ-D1**
- Epsilon regression: `2.2` → **CE-D1**
- Trust Front regression: `4.1` → **CD-D1**

Evidence: `knowledge/evidence/releases/RO008/inventory_assert.json`.

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged; live copies metadata-only |
| Wave 9 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — only CK day-order registration |
| Recommendation logic unmodified | **Met** |
| RO1-R1 tomorrow chrome path preserved | **Met** — chrome binding unchanged; residuals tracked as presentation |

---

## Deployment verdict

# **PASS — Wave 8 Kappa inventory jointly LIVE**

Companion verification: `RO008_LIVE_VERIFICATION_REPORT.md`.  
Release decision: `RO008_RELEASE_DECISION.md` (authorises PB-010; does not execute it).

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/3.1.*-cs1010.json` (6)
- `app/curriculum/data/educational_packages/cs1/revision-estimators-cs1010.json`
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-kappa-cs1010/` (authored inventory + `released` campaign status)

## Files Modified

- `app/application/educational_packages/selection.py` — CK-D1…CK-R1 day order
- Campaign `campaign.json` status → `released`
- Tests updated for Kappa chain / CI-R1 handoff / topic 3.1 entry

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 144 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only. PB-002 selection extended for Kappa campaign days only.

## Technical Debt

None introduced by activation itself. Soft title-keyword package resolution remains ambiguous across large inventory (pre-existing). Observed Continuity Front label desync during multi-day ops walks (expected labels briefly ahead of true package) — same class as RO-004…RO-007; package path verified by syllabus-code continuation.

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification; students in production still face one-mission-per-calendar-day pacing. Published Baseline picker offers section codes — Continuity Front LIVE entry for Topic 3.1 uses section **3**.
