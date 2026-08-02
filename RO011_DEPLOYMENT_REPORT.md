# RO-011 — Deployment Report

**Programme:** RO-011 — Wave 11 LIVE Release Operations  
**Authority:** EP-001 Wave 11 / HR-011 Publication APPROVED · EF-001 · FP-01  
**Date:** 2026-08-02  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Nu / CS1-013 (CN-D1…CN-R1) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. LIVE fingerprint matches tip `a0d8df665fa826343579529956728ae493cf5f97`. Inventory hard-assert confirms **89** `publication_approved` CS1 packages including **6** Nu days, with Continuity Front handoff **CM-R1 → CN-D1** and Trust Front cold entry at **4.1 → CD-D1** preserved. Continuity wiring extends `_CAMPAIGN_DAY_ORDER` with CN-D1…CN-R1 (indices 84–89) and prefers the CN chain when journey last day is Mu/Nu so shared topic_code `4.1` does not divert onto Trust Front Delta — same class of ops prerequisite as RO-001…RO-010 day-order registration, not a Runtime redesign. Mu (6), Lambda (9), Kappa (7), Iota (7), Theta (3), Eta (3), Zeta (3), Epsilon (5), Gamma (5), and Delta (27) inventory counts unchanged.

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1 | `CS1-EP001-PKG-CN-4.1-RESPONSE-EXPLANATORY` | CN-D1 | `educational_packages/cs1/4.1.1-response-explanatory-cs1013.json` | `publication_approved` |
| 2 | `CS1-EP001-PKG-CN-4.1-SIMPLE-MULTIPLE` | CN-D2 | `…/4.1.2-simple-multiple-cs1013.json` | `publication_approved` |
| 3 | `CS1-EP001-PKG-CN-4.1-LEAST-SQUARES` | CN-D3 | `…/4.1.3-least-squares-cs1013.json` | `publication_approved` |
| 4 | `CS1-EP001-PKG-CN-4.1-SOFTWARE-FIT` | CN-D4 | `…/4.1.4-software-fit-cs1013.json` | `publication_approved` |
| 5 | `CS1-EP001-PKG-CN-4.1-VARIABLE-SELECTION` | CN-D5 | `…/4.1.5-variable-selection-cs1013.json` | `publication_approved` |
| 6 | `CS1-EP001-PKG-REV-LINEAR-REGRESSION-NU` | CN-R1 | `…/revision-linear-regression-cs1013.json` | `publication_approved` |

**FP-01:** All **6** activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-nu-cs1013/packages/` remain `campaign_member_certified` (bodies untouched).  
**Campaign status:** `campaign.json` → `released`.  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CN-D1…CN-R1 (84–89); CM-R1 LIVE `tomorrow_preview.next_topic_code` → `CN-D1`; successor preference for CN when last day is `CM-`/`CN-`.

Activation field changes on live Nu copies only: `status`, `publication_version` (`cs1013-live-1.0.0`), `published_at`.  
CM-R1 LIVE handoff update is ops continuity metadata only (catalogue Mu remains as authored stop audit).

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Tip | `a0d8df665fa826343579529956728ae493cf5f97` |
| Push | `2429313..a0d8df6` → `origin/main` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9nq43m1egvs738jn2c0` |
| Trigger | API `clearCache` |
| Status progression | `build_in_progress` → `pre_deploy_in_progress` → `update_in_progress` → `live` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health` commit field | `a0d8df665fa…` | match | **PASS** |
| `/health/live` | ok + matching commit | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Note: Dedicated `/health.commit` route is not registered in this build; fingerprint is taken from `/health` and `/health/live` JSON `commit` fields (same practice as prior RO evidence packs).

Evidence: `knowledge/evidence/releases/RO011/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9nq5nm417fc73duc2jg` **succeeded**. Tip-matched local loader assert confirms:

- `len(all_approved()) == 89`
- Nu `campaign_day` prefix `CN-` count **6**
- Mu **6** / Lambda **9** / Kappa **7** / Iota **7** / Theta **3** / Eta **3** / Zeta **3** / Epsilon **5** / Gamma **5** / Delta **27** unchanged
- No duplicate package IDs
- Trust Front cold entry `syllabus_topic_code=4.1` → **CD-D1**
- After simulated CM-R1 completion → **CN-D1** / `CS1-EP001-PKG-CN-4.1-RESPONSE-EXPLANATORY`
- Mu regression: `3.3` → **CM-D1**
- Lambda regression: `3.2` → **CL-D1**
- Kappa regression: `3.1` → **CK-D1**
- Iota regression: `2.6` → **CI-D1**
- Theta regression: `2.5` → **CT-D1**
- Eta regression: `2.4` → **CH-D1**
- Zeta regression: `2.3` → **CZ-D1**
- Epsilon regression: `2.2` → **CE-D1**

Evidence: `knowledge/evidence/releases/RO011/inventory_assert.json`.

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged; live Nu copies metadata-only |
| Wave 12 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — only CN day-order + Nu/Delta coexistence successor preference |
| Recommendation logic unmodified | **Met** |
| Student Twin unmodified | **Met** |
| PB-013 not executed | **Met** — authorised only on PASS exit |

---

## Deployment verdict

# **PASS — Wave 11 Nu inventory jointly LIVE**

Companion verification: `RO011_LIVE_VERIFICATION_REPORT.md` (**PASS WITH RESIDUAL** — package path).  
Release decision: `RO011_RELEASE_DECISION.md` (authorises PB-013; does not execute it).

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/4.1.*-cs1013.json` (5)
- `app/curriculum/data/educational_packages/cs1/revision-linear-regression-cs1013.json`
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-nu-cs1013/` (authored inventory + `released` campaign status)

## Files Modified

- `app/application/educational_packages/selection.py` — CN-D1…CN-R1 day order + CM/CN → CN successor preference
- `app/curriculum/data/educational_packages/cs1/revision-hypothesis-testing-cs1012.json` — CM-R1 LIVE handoff → CN-D1
- Campaign `campaign.json` status → `released`
- Tests updated for Nu chain / CM-R1 handoff / Trust Front 4.1 cold entry

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 171 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only. PB-002 selection extended for Nu campaign days and Nu/Delta coexistence on shared topic_code `4.1`. Educational Framework frozen (EF-001). No Student Twin / recommendation engine changes.

## Technical Debt

None introduced by activation itself. Soft title-keyword package resolution remains ambiguous across large inventory (pre-existing). Observed Continuity Front label desync during multi-day ops walks (expected labels briefly ahead of true package) — same class as RO-004…RO-010; package path verified by syllabus-code / Topic–Mission continuation.

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification; students in production still face one-mission-per-calendar-day pacing. Published Baseline picker offers section codes — Continuity Front LIVE entry for Topic 4.1 CF-join uses section **3** natural progression through 3.1→3.2→3.3 then Nu. Trust Front cold entry at **4.1** remains Delta CD-D1 by design.

---

## Student Impact Assessment

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Assessment |
|-------|------------|
| **Student problem** | Continuity Front after Mu stopped at 3.3 / CM-R1; CF-native Topic 4.1 unpublished LIVE while Trust Front Delta held independent 4.1 inventory. |
| **Student benefit** | Diligent students can study approved Nu days with CMP partnership on LIVE after Mu, without Isolated Golden Day or Trust Front absorb. |
| **Learning benefit** | Contiguous CMP-partnered response/explanatory → simple/multiple → least squares → software fit → variable selection → Revision under one Sensei (CF-join). |
| **Success metrics** | Deploy PASS · LIVE verify (companion) · 0 fallback on true Nu path · coverage **63 / 72 held** · reliance through Topic **4.1**. |
| **Risks** | Over-claiming until-exam trust; label desync residual; chrome / Q6 residual; double-count of 4.1 Approver credit. |
| **Assumptions** | Continuity Front entry via continue at section 3; CMP remains external authority; Trust Front Delta remains independent. |

## Estimated KSI contribution

ΔKSI = **0** (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

## Evidence collected

`knowledge/evidence/releases/RO011/` · deploy `dep-d9nq43m1egvs738jn2c0` · assert job `job-d9nq5nm417fc73duc2jg` · student provision `job-d9nq6rlbedkc738h7ulg`.

## Lessons learned for student value

Joint activation of a Continuity Front join onto geography already published via Trust Front works when FP-01 is held, CM-R1 → CN-D1 is explicit, and successor selection prefers CN after Mu/Nu so shared `4.1` topic_code does not divert onto Delta. Progressive confidence must stay scoped to LIVE-certified inventory and run as PB-013.

## Explainability Review

N/A — no intelligence change.

## Recommendation Quality Review

N/A — no ranking change.

## Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. Wave 12 geography still unpublished. PB-013 not yet executed.

## CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-011 · 2026-08-02  
**Wave 11 LIVE status:** Deployment **PASS** · companion LIVE verification required for release acceptance
