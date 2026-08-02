# RO-005 — Deployment Report

**Programme:** RO-005 — Wave 5 LIVE Release Operations  
**Authority:** EP-001 Wave 5 / HR-005 Publication APPROVED · EF-001  
**Date:** 2026-08-01 / 2026-08-02  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Eta / CS1-007 (CH-D1…CH-R1) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. LIVE fingerprint matches tip `40c487e54c73d98a95e8ebfe4b4fbee5c2c52c8d`. Inventory hard-assert confirms **51** `publication_approved` CS1 packages including **3** Eta days, with Continuity Front handoff **CZ-R1 → CH-D1** and cold entry at **2.4 → CH-D1**. Continuity wiring extends `_CAMPAIGN_DAY_ORDER` with CH-D1…CH-R1 (indices 49–51) — same class of ops prerequisite as RO-001…RO-004 day-order registration, not a Runtime redesign. Zeta (3), Epsilon (5), Gamma (5), and Delta (27) inventory counts unchanged.

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1 | `CS1-EP001-PKG-2.4-MGF-CGF` | CH-D1 | `educational_packages/cs1/2.4.1-mgf-cgf-cs1007.json` | `publication_approved` |
| 2 | `CS1-EP001-PKG-2.4-MOMENT-VIA-GF` | CH-D2 | `…/2.4.2-moment-via-gf-cs1007.json` | `publication_approved` |
| 3 | `CS1-EP001-PKG-REV-GENERATING-FUNCTIONS` | CH-R1 | `…/revision-generating-functions-cs1007.json` | `publication_approved` |

**FP-01:** All **3** activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-eta-cs1007/packages/` remain `campaign_member_certified` (bodies untouched).  
**Campaign status:** `campaign.json` → `released`.  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CH-D1…CH-R1 (49–51).

Activation field changes on live copies only: `status`, `publication_version` (`cs1007-live-1.0.0`), `published_at`.

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Tip | `40c487e54c73d98a95e8ebfe4b4fbee5c2c52c8d` |
| Push | `b9a27b0..40c487e` → `origin/main` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9n5qnflk1mc73dpl100` |
| Trigger | API `clearCache` |
| Status progression | `build_in_progress` → `pre_deploy_in_progress` → `update_in_progress` → `live` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health.commit` | `40c487e54…` | match | **PASS** |
| `/health/live` | ok | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Evidence: `knowledge/evidence/releases/RO005/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9n5rru417fc73cnsoug` **succeeded**. Tip-matched local loader assert confirms:

- `len(all_approved()) == 51`
- Eta `campaign_day` prefix `CH-` count **3**
- Zeta **3** / Epsilon **5** / Gamma **5** / Delta **27** unchanged
- Cold entry `syllabus_topic_code=2.4` → **CH-D1**
- After simulated CZ-R1 completion → **CH-D1** / `CS1-EP001-PKG-2.4-MGF-CGF`
- Zeta regression: `2.3` → **CZ-D1**
- Epsilon regression: `2.2` → **CE-D1**
- Trust Front regression: `4.1` → **CD-D1**

Evidence: `knowledge/evidence/releases/RO005/inventory_assert.json`.

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged; live copies metadata-only |
| Wave 6 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — only CH day-order registration |
| Recommendation logic unmodified | **Met** |

---

## Deployment verdict

# **PASS — Wave 5 Eta inventory jointly LIVE**

Companion verification: `RO005_LIVE_VERIFICATION_REPORT.md`.  
Progressive confidence: `PB007_PROGRESSIVE_CONFIDENCE_REPORT.md`.  
Release decision: `RO005_RELEASE_DECISION.md`.

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/2.4.*-cs1007.json` (2)
- `app/curriculum/data/educational_packages/cs1/revision-generating-functions-cs1007.json`
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-eta-cs1007/` (authored inventory + `released` campaign status)

## Files Modified

- `app/application/educational_packages/selection.py` — CH-D1…CH-R1 day order
- Campaign `campaign.json` status → `released`
- Tests updated for Eta chain / CZ-R1 handoff / topic 2.4 entry

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 119 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only. PB-002 selection extended for Eta campaign days only.

## Technical Debt

None introduced by activation itself. Soft title-keyword package resolution remains ambiguous across large inventory (pre-existing). Observed Continuity Front label desync during multi-day ops walks (expected labels briefly ahead of true package) — same class as RO-004; package path verified by continuation. Topic-code `2.4` Home collision class (RO4-R1 analogue) tracked as residual RO5-R1.

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification; students in production still face one-mission-per-calendar-day pacing. Published Baseline picker offers section codes only — Continuity Front LIVE entry uses section **2** (natural CB→CG→CE→CZ→CH chain).
