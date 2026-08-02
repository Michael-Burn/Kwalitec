# RO-010 — Deployment Report

**Programme:** RO-010 — Wave 10 LIVE Release Operations  
**Authority:** EP-001 Wave 10 / HR-010 Publication APPROVED · EF-001  
**Date:** 2026-08-02  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Mu / CS1-012 (CM-D1…CM-R1) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. LIVE fingerprint matches tip `c409ad29871d7845f8d9d832776168142d40fad7`. Inventory hard-assert confirms **83** `publication_approved` CS1 packages including **6** Mu days, with Continuity Front handoff **CL-R1 → CM-D1** and cold entry at **3.3 → CM-D1**. Continuity wiring extends `_CAMPAIGN_DAY_ORDER` with CM-D1…CM-R1 (indices 78–83) — same class of ops prerequisite as RO-001…RO-009 day-order registration, not a Runtime redesign. Lambda (9), Kappa (7), Iota (7), Theta (3), Eta (3), Zeta (3), Epsilon (5), Gamma (5), and Delta (27) inventory counts unchanged.

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1 | `CS1-EP001-PKG-3.3-HYPOTHESIS-CONCEPTS` | CM-D1 | `educational_packages/cs1/3.3.1-hypothesis-concepts-cs1012.json` | `publication_approved` |
| 2 | `CS1-EP001-PKG-3.3-BASIC-TESTS` | CM-D2 | `…/3.3.2-basic-tests-cs1012.json` | `publication_approved` |
| 3 | `CS1-EP001-PKG-3.3-PERMUTATION-TESTS` | CM-D3 | `…/3.3.3-permutation-tests-cs1012.json` | `publication_approved` |
| 4 | `CS1-EP001-PKG-3.3-CHI-SQUARE-GOF` | CM-D4 | `…/3.3.4-chi-square-gof-cs1012.json` | `publication_approved` |
| 5 | `CS1-EP001-PKG-3.3-CONTINGENCY-INDEPENDENCE` | CM-D5 | `…/3.3.5-contingency-independence-cs1012.json` | `publication_approved` |
| 6 | `CS1-EP001-PKG-REV-HYPOTHESIS-TESTING` | CM-R1 | `…/revision-hypothesis-testing-cs1012.json` | `publication_approved` |

**FP-01:** All **6** activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-mu-cs1012/packages/` remain `campaign_member_certified` (bodies untouched).  
**Campaign status:** `campaign.json` → `released`.  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CM-D1…CM-R1 (78–83).

Activation field changes on live copies only: `status`, `publication_version` (`cs1012-live-1.0.0`), `published_at`.

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Tip | `c409ad29871d7845f8d9d832776168142d40fad7` |
| Push | `42f0b72..c409ad2` → `origin/main` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9nmclp42hec73fueteg` |
| Trigger | API `clearCache` |
| Status progression | `build_in_progress` → `pre_deploy_in_progress` → `update_in_progress` → `live` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health` commit field | `c409ad29871d…` | match | **PASS** |
| `/health/live` | ok + matching commit | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Note: Dedicated `/health.commit` route is not registered in this build; fingerprint is taken from `/health` and `/health/live` JSON `commit` fields (same practice as prior RO evidence packs).

Evidence: `knowledge/evidence/releases/RO010/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9nmerijnfac73bcvrs0` **succeeded**. Tip-matched local loader assert confirms:

- `len(all_approved()) == 83`
- Mu `campaign_day` prefix `CM-` count **6**
- Lambda **9** / Kappa **7** / Iota **7** / Theta **3** / Eta **3** / Zeta **3** / Epsilon **5** / Gamma **5** / Delta **27** unchanged
- No duplicate package IDs
- Cold entry `syllabus_topic_code=3.3` → **CM-D1**
- After simulated CL-R1 completion → **CM-D1** / `CS1-EP001-PKG-3.3-HYPOTHESIS-CONCEPTS`
- Lambda regression: `3.2` → **CL-D1**
- Kappa regression: `3.1` → **CK-D1**
- Iota regression: `2.6` → **CI-D1**
- Theta regression: `2.5` → **CT-D1**
- Eta regression: `2.4` → **CH-D1**
- Zeta regression: `2.3` → **CZ-D1**
- Epsilon regression: `2.2` → **CE-D1**
- Trust Front regression: `4.1` → **CD-D1**

Evidence: `knowledge/evidence/releases/RO010/inventory_assert.json`.

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged; live copies metadata-only |
| Wave 11 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — only CM day-order registration |
| Recommendation logic unmodified | **Met** |
| Student Twin unmodified | **Met** |
| PB-012 not executed | **Met** — authorised only on PASS exit |

---

## Deployment verdict

# **PASS — Wave 10 Mu inventory jointly LIVE**

Companion verification: `RO010_LIVE_VERIFICATION_REPORT.md` (**PASS WITH RESIDUAL** — package path).  
Release decision: `RO010_RELEASE_DECISION.md` (authorises PB-012; does not execute it).

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/3.3.*-cs1012.json` (5)
- `app/curriculum/data/educational_packages/cs1/revision-hypothesis-testing-cs1012.json`
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-mu-cs1012/` (authored inventory + `released` campaign status)

## Files Modified

- `app/application/educational_packages/selection.py` — CM-D1…CM-R1 day order
- Campaign `campaign.json` status → `released`
- Tests updated for Mu chain / CL-R1 handoff / topic 3.3 entry

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 163 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only. PB-002 selection extended for Mu campaign days only. Educational Framework frozen (EF-001). No Student Twin / recommendation engine changes.

## Technical Debt

None introduced by activation itself. Soft title-keyword package resolution remains ambiguous across large inventory (pre-existing). Observed Continuity Front label desync during multi-day ops walks (expected labels briefly ahead of true package) — same class as RO-004…RO-009; package path verified by syllabus-code / Topic-Mission continuation.

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification; students in production still face one-mission-per-calendar-day pacing. Published Baseline picker offers section codes — Continuity Front LIVE entry for Topic 3.3 uses section **3** (natural progression through 3.1 then 3.2 then 3.3).

---

## Student Impact Assessment

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Assessment |
|-------|------------|
| **Student problem** | Continuity Front after Lambda stopped at 3.2 / CL-R1; hypothesis testing (3.3) unpublished LIVE. |
| **Student benefit** | Diligent students can study approved Mu days with CMP partnership on LIVE after Lambda. |
| **Learning benefit** | Contiguous CMP-partnered HT concepts → basic tests → permutation → chi-square GOF → contingency independence → Revision under one Sensei. |
| **Success metrics** | Deploy PASS · LIVE verify (companion) · 0 fallback on true Mu path · coverage **63 / 72** after LIVE verify success. |
| **Risks** | Over-claiming until-exam trust; label desync residual; chrome / Q6 residual. |
| **Assumptions** | Continuity Front entry via continue at section 3; CMP remains external authority. |

## Estimated KSI contribution

ΔKSI = **0** (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

## Evidence collected

`knowledge/evidence/releases/RO010/` · deploy `dep-d9nmclp42hec73fueteg` · assert job `job-d9nmerijnfac73bcvrs0` · student provision `job-d9nmh06417fc73dn15rg`.

## Lessons learned for student value

Joint activation of a Continuity Front extension works when FP-01 is held and CL-R1 → CM-D1 selection is explicit after Lambda. Progressive confidence must stay scoped to LIVE-certified inventory and run as PB-012.

## Explainability Review

N/A — no intelligence change.

## Recommendation Quality Review

N/A — no ranking change.

## Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. Wave 11 geography still unpublished. PB-012 not yet executed.

## CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-010 · 2026-08-02  
**Wave 10 LIVE status:** Deployment **PASS** · companion LIVE verification required for release acceptance
