# RO-003 — Deployment Report

**Programme:** RO-003 — Wave 3 LIVE Release Operations  
**Authority:** EP-001 Wave 3 / HR-003 Publication APPROVED · EF-001  
**Date:** 2026-08-01  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Epsilon / CS1-005 (CE-D1…CE-R1) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. LIVE fingerprint matches tip `efe18ad7b6384f48e06190fd576c5240b704dfec`. Inventory hard-assert confirms **45** `publication_approved` CS1 packages including **5** Epsilon days, with Continuity Front handoff **CG-R1 → CE-D1** and cold entry at **2.2 → CE-D1**. Continuity wiring extends `_CAMPAIGN_DAY_ORDER` with CE-D1…CE-R1 (indices 41–45) — same class of ops prerequisite as RO-001 / RO-002 day-order registration, not a Runtime redesign. Gamma (5) and Delta (27) inventory counts unchanged.

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1 | `CS1-EP001-PKG-2.2-MARGINAL-CONDITIONAL` | CE-D1 | `educational_packages/cs1/2.2.1-marginal-conditional-cs1005.json` | `publication_approved` |
| 2 | `CS1-EP001-PKG-2.2-INDEPENDENCE` | CE-D2 | `…/2.2.2-independence-cs1005.json` | `publication_approved` |
| 3 | `CS1-EP001-PKG-2.2-COV-CORR-EXPECTATION` | CE-D3 | `…/2.2.3-cov-corr-expectation-cs1005.json` | `publication_approved` |
| 4 | `CS1-EP001-PKG-2.2-LINEAR-COMBINATIONS` | CE-D4 | `…/2.2.4-linear-combinations-cs1005.json` | `publication_approved` |
| 5 | `CS1-EP001-PKG-REV-JOINT-DISTRIBUTIONS` | CE-R1 | `…/revision-joint-distributions-cs1005.json` | `publication_approved` |

**FP-01:** All **5** activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-epsilon-cs1005/packages/` remain `campaign_member_certified` (bodies untouched).  
**Campaign status:** `campaign.json` → `released`.  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CE-D1…CE-R1 (41–45).

Activation field changes on live copies only: `status`, `publication_version` (`cs1005-live-1.0.0`), `published_at`.

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Tip | `efe18ad7b6384f48e06190fd576c5240b704dfec` |
| Push | `b99b0a8..efe18ad` → `origin/main` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9n3ggfqj5pc73e5bm0g` |
| Trigger | API `clearCache` |
| Status progression | `build_in_progress` → `pre_deploy_in_progress` → `update_in_progress` → `live` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health.commit` | `efe18ad7…` | match | **PASS** |
| `/health/live` | ok | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Evidence: `knowledge/evidence/releases/RO003/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9n3iltaeets73b5aakg` **succeeded**. Tip-matched local loader assert confirms:

- `len(all_approved()) == 45`
- Epsilon `campaign_day` prefix `CE-` count **5**
- Gamma **5** / Delta **27** unchanged
- Cold entry `syllabus_topic_code=2.2` → **CE-D1**
- After simulated CG-R1 completion → **CE-D1** / `CS1-EP001-PKG-2.2-MARGINAL-CONDITIONAL`
- Trust Front regression: `4.1` → **CD-D1**

Evidence: `knowledge/evidence/releases/RO003/inventory_assert.json`.

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged |
| Wave 4 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — only CE day-order registration |
| Recommendation logic unmodified | **Met** |

---

## Deployment verdict

# **PASS — Wave 3 Epsilon inventory jointly LIVE**

Companion verification: `RO003_LIVE_VERIFICATION_REPORT.md`.  
Progressive confidence: `PB005_PROGRESSIVE_CONFIDENCE_REPORT.md`.  
Release decision: `RO003_RELEASE_DECISION.md`.

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/2.2.*-cs1005.json` (4)
- `app/curriculum/data/educational_packages/cs1/revision-joint-distributions-cs1005.json`
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-epsilon-cs1005/` (authored inventory + `released` campaign status)

## Files Modified

- `app/application/educational_packages/selection.py` — CE-D1…CE-R1 day order
- Campaign `campaign.json` status → `released`
- Tests updated for Epsilon chain / CG-R1 handoff / topic 2.2 entry

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 107 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only. PB-002 selection extended for Epsilon campaign days only.

## Technical Debt

None introduced by activation. Soft title-keyword package resolution remains ambiguous across large inventory (pre-existing).

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification; students in production still face one-mission-per-calendar-day pacing. Published Baseline picker offers section codes only — Continuity Front LIVE entry uses section **2** (natural CB→CG→CE chain).
