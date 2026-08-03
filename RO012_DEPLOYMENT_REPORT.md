# RO-012 — Deployment Report

**Programme:** RO-012 — Wave 12 LIVE Release Operations  
**Authority:** EP-001 Wave 12 / HR-012 Publication APPROVED · EF-001 · FP-01  
**Date:** 2026-08-03  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Xi / CS1-014 (CX-D1…CX-R1) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. LIVE fingerprint matches tip `a800c85f602b68d1380ae355c0d2839403018995`. Inventory hard-assert confirms **100** `publication_approved` CS1 packages including **11** Xi days, with Continuity Front handoff **CN-R1 → CX-D1** and Trust Front cold entry at **4.2 → CD-D6** preserved. Continuity wiring extends `_CAMPAIGN_DAY_ORDER` with CX-D1…CX-R1 (indices 90–100) and prefers the CX chain when journey last day is Nu/Xi so shared topic_code `4.2` does not divert onto Trust Front Delta — same class of ops prerequisite as RO-001…RO-011 day-order registration, not a Runtime redesign. Nu (6), Mu (6), Lambda (9), Kappa (7), Iota (7), Theta (3), Eta (3), Zeta (3), Epsilon (5), Gamma (5), and Delta (27) inventory counts unchanged.

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1 | `CS1-EP001-PKG-CX-4.2-EXPONENTIAL-FAMILY` | CX-D1 | `educational_packages/cs1/4.2.1-exponential-family-cs1014.json` | `publication_approved` |
| 2 | `CS1-EP001-PKG-CX-4.2-MEAN-VARIANCE` | CX-D2 | `…/4.2.2-mean-variance-cs1014.json` | `publication_approved` |
| 3 | `CS1-EP001-PKG-CX-4.2-LINK-CANONICAL` | CX-D3 | `…/4.2.3-link-canonical-cs1014.json` | `publication_approved` |
| 4 | `CS1-EP001-PKG-CX-4.2-FACTORS-INTERACTIONS` | CX-D4 | `…/4.2.4-factors-interactions-cs1014.json` | `publication_approved` |
| 5 | `CS1-EP001-PKG-CX-4.2-LINEAR-PREDICTOR` | CX-D5 | `…/4.2.5-linear-predictor-cs1014.json` | `publication_approved` |
| 6 | `CS1-EP001-PKG-CX-4.2-DEVIANCE-ESTIMATION` | CX-D6 | `…/4.2.6-deviance-estimation-cs1014.json` | `publication_approved` |
| 7 | `CS1-EP001-PKG-CX-4.2-MODEL-CHOICE` | CX-D7 | `…/4.2.7-model-choice-cs1014.json` | `publication_approved` |
| 8 | `CS1-EP001-PKG-CX-4.2-RESIDUALS` | CX-D8 | `…/4.2.8-residuals-cs1014.json` | `publication_approved` |
| 9 | `CS1-EP001-PKG-CX-4.2-GOODNESS-TESTS` | CX-D9 | `…/4.2.9-goodness-tests-cs1014.json` | `publication_approved` |
| 10 | `CS1-EP001-PKG-CX-4.2-FIT-INTERPRET` | CX-D10 | `…/4.2.10-fit-interpret-cs1014.json` | `publication_approved` |
| 11 | `CS1-EP001-PKG-REV-GLM-XI` | CX-R1 | `…/revision-glm-cs1014.json` | `publication_approved` |

**FP-01:** All **11** activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-xi-cs1014/packages/` remain `campaign_member_certified` (bodies untouched).  
**Campaign status:** `campaign.json` → `released`.  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CX-D1…CX-R1 (90–100); CN-R1 LIVE `tomorrow_preview.next_topic_code` → `CX-D1`; successor preference for CX when last day is `CN-`/`CX-`.

Activation field changes on live Xi copies only: `status`, `publication_version` (`cs1014-live-1.0.0`), `published_at`.  
CN-R1 LIVE handoff update is ops continuity metadata only (catalogue Nu remains as authored stop audit until this activation superseded it on the live path).

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Tip | `a800c85f602b68d1380ae355c0d2839403018995` |
| Push | `bd5090e..a800c85` → `origin/main` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9o0dnu7bikc73cnt8o0` |
| Trigger | API `clearCache` |
| Status progression | `build_in_progress` → `update_in_progress` → `live` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health` commit field | `a800c85f602b…` | match | **PASS** |
| `/health/live` | ok + matching commit | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Evidence: `knowledge/evidence/releases/RO012/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9o0fnm7bikc73co0fi0` **succeeded**. Tip-matched local loader assert confirms:

- `len(all_approved()) == 100`
- Xi `campaign_day` prefix `CX-` count **11**
- Nu **6** / Mu **6** / Lambda **9** / Kappa **7** / Iota **7** / Theta **3** / Eta **3** / Zeta **3** / Epsilon **5** / Gamma **5** / Delta **27** unchanged
- No duplicate package IDs
- Trust Front cold entry `syllabus_topic_code=4.2` → **CD-D6**
- Trust Front cold entry `syllabus_topic_code=4.1` → **CD-D1**
- After simulated CN-R1 completion → **CX-D1** / `CS1-EP001-PKG-CX-4.2-EXPONENTIAL-FAMILY`

Evidence: `knowledge/evidence/releases/RO012/inventory_assert_local.txt`, `inventory_payload.json`, `inventory_job_final.json`.

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged; live Xi copies metadata-only |
| Wave 13 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — only CX day-order + Nu/Xi–Delta coexistence successor preference |
| Recommendation logic unmodified | **Met** |
| Student Twin unmodified | **Met** |
| PB-014 not executed | **Met** — authorised only on PASS exit |

---

## Deployment verdict

# **PASS — Wave 12 Xi inventory jointly LIVE**

Companion verification: `RO012_LIVE_VERIFICATION_REPORT.md` (**PASS WITH RESIDUAL** — package path).  
Release decision: `RO012_RELEASE_DECISION.md` (authorises PB-014; does not execute it).

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/4.2.*-cs1014.json` (10)
- `app/curriculum/data/educational_packages/cs1/revision-glm-cs1014.json`
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-xi-cs1014/` (authored inventory + `released` campaign status)

## Files Modified

- `app/application/educational_packages/selection.py` — CX-D1…CX-R1 day order + CN/CX → CX successor preference
- `app/curriculum/data/educational_packages/cs1/revision-linear-regression-cs1013.json` — CN-R1 LIVE handoff → CX-D1
- Campaign `campaign.json` status → `released`
- Tests updated for Xi chain / CN-R1 handoff / Trust Front 4.2 cold entry

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 184 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only. PB-002 selection extended for Xi campaign days and Nu/Xi–Delta coexistence on shared topic_code `4.2`. Educational Framework frozen (EF-001). No Student Twin / recommendation engine changes.

## Technical Debt

None introduced by activation itself. Soft title-keyword package resolution remains ambiguous across large inventory (pre-existing). Observed Continuity Front label desync during multi-day ops walks (expected labels briefly ahead of true package) — same class as RO-004…RO-011; package path verified by syllabus-code / Topic–Mission continuation.

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification; students in production still face one-mission-per-calendar-day pacing. Published Baseline picker offers section codes — Continuity Front LIVE entry for Topic 4.2 CF-join uses section **3** natural progression through 3.1→3.2→3.3→4.1 then Xi. Trust Front cold entry at **4.2** remains Delta CD-D6 by design.

---

## Student Impact Assessment

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Assessment |
|-------|------------|
| **Student problem** | Continuity Front after Nu stopped at 4.1 / CN-R1; CF-native Topic 4.2 unpublished LIVE while Trust Front Delta held independent 4.2 inventory. |
| **Student benefit** | Diligent students can study approved Xi days with CMP partnership on LIVE after Nu, without Isolated Golden Day or Trust Front absorb of 5.1. |
| **Learning benefit** | Contiguous CMP-partnered exponential family → moments → link → factors → η → deviance → model choice → residuals → tests → fit/interpret → Revision under one Sensei (CF-join). |
| **Success metrics** | Deploy PASS · LIVE verify (companion) · 0 fallback on true Xi path · coverage **63 / 72 held** · reliance through Topic **4.2**. |
| **Risks** | Over-claiming until-exam trust or 100% Approver coverage; label desync residual; chrome / Q6 residual; double-count of 4.2 Approver credit. |
| **Assumptions** | Continuity Front entry via continue at section 3; CMP remains external authority; Trust Front Delta remains independent. |

## Estimated KSI contribution

ΔKSI = **0** (ops release + validation evidence; no new educational product behaviour beyond inventory activation).

## Evidence collected

`knowledge/evidence/releases/RO012/` · deploy `dep-d9o0dnu7bikc73cnt8o0` · assert job `job-d9o0fnm7bikc73co0fi0` · student provision `job-d9o0fvrm8hqs73f7rtgg`.

## Lessons learned for student value

Joint activation of a Continuity Front join onto geography already published via Trust Front works when FP-01 is held, CN-R1 → CX-D1 is explicit, and successor selection prefers CX after Nu/Xi so shared `4.2` topic_code does not divert onto Delta. Progressive confidence must stay scoped to LIVE-certified inventory and run as PB-014. Approver coverage must not double-count Topic 4.2.

## Explainability Review

N/A — no intelligence change.

## Recommendation Quality Review

N/A — no ranking change.

## Version 1 readiness residual

Until-exam / Gate G1 not cleared. Wave 0 Approver gap open. PB-014 not yet executed. No 100% Approver-credit claim (Alpha/Beta honesty gap remains).

## CRI domains / ΔCRI

ΔCRI = 0 (ops validation; board not updated on provisional evidence alone).

---

Signed: Release Ops · RO-012 · 2026-08-03  
**Wave 12 LIVE status:** Deployment **PASS** · companion LIVE verification required for release acceptance
