# RO-001 — Deployment Report

**Programme:** RO-001 — Wave 1 LIVE Release Operations  
**Authority:** EP-001 Wave 1 Publication APPROVED · HR-001 COMPLETE · EF-001  
**Date:** 2026-08-01  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Gamma / CS1-004 (CG-D1…CG-R1) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. LIVE fingerprint matches tip `f1ff5dc5dd5aca9987c48a6731f3888fdf2295a1`. Inventory hard-assert confirms **14** `publication_approved` CS1 packages including **5** Gamma days, with CB-R1 → CG-D1 chain resolution. PB-002 continuity/withhold wiring required for natural campaign_day selection was included in the same release tip (prerequisite for Wave 1 continuity exit — not a Runtime redesign).

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1 | `CS1-EP001-PKG-2.1-PROB-QUANTILES` | CG-D1 | `educational_packages/cs1/2.1.3-prob-quantiles-cs1004.json` | `publication_approved` |
| 2 | `CS1-EP001-PKG-2.1-POISSON-PROCESS` | CG-D2 | `…/2.1.4-poisson-process-cs1004.json` | `publication_approved` |
| 3 | `CS1-EP001-PKG-2.1-INVERSE-TRANSFORM` | CG-D3 | `…/2.1.5-inverse-transform-cs1004.json` | `publication_approved` |
| 4 | `CS1-EP001-PKG-2.1-SOFTWARE-GENERATION` | CG-D4 | `…/2.1.6-software-generation-cs1004.json` | `publication_approved` |
| 5 | `CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION` | CG-R1 | `…/revision-distributions-generation-cs1004.json` | `publication_approved` |

**FP-01:** All five activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-gamma-cs1004/packages/` remain `campaign_member_certified` (bodies untouched).  
**Campaign status:** `campaign.json` → `released`.  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CG-D1…CG-R1 (9–13) so tomorrow_preview / campaign_day selection preserves CB-R1 → Gamma.

Activation field changes on live copies only: `status`, `publication_version` (`cs1004-live-1.0.0`), `published_at`.

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Tip | `f1ff5dc5dd5aca9987c48a6731f3888fdf2295a1` |
| Push | `94e02f5..f1ff5dc` → `origin/main` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9mtte5aeets73apso4g` |
| Trigger | API `clearCache` |
| Status progression | `build_in_progress` → `pre_deploy_in_progress` → `update_in_progress` → `live` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health.commit` | `f1ff5dc5…` | match | **PASS** |
| `/health/live` | ok | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Evidence: `knowledge/evidence/releases/RO001/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9mu0brl550s738vdui0` **succeeded** with hard asserts:

- `len(all_approved()) == 14`
- Gamma `campaign_day` prefix `CG-` count **5**
- After simulated CB-R1 completion → `resolve_active_educational_package` → **CG-D1** / `CS1-EP001-PKG-2.1-PROB-QUANTILES`

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged |
| Wave 2 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — PB-002 selection already authored; only CG day-order registration added for continuity |

---

## Deployment verdict

# **PASS — Wave 1 Gamma inventory jointly LIVE**

Companion verification: `RO001_LIVE_VERIFICATION_REPORT.md`.  
Release decision: `RO001_RELEASE_DECISION.md`.

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/2.1.3-prob-quantiles-cs1004.json`
- `app/curriculum/data/educational_packages/cs1/2.1.4-poisson-process-cs1004.json`
- `app/curriculum/data/educational_packages/cs1/2.1.5-inverse-transform-cs1004.json`
- `app/curriculum/data/educational_packages/cs1/2.1.6-software-generation-cs1004.json`
- `app/curriculum/data/educational_packages/cs1/revision-distributions-generation-cs1004.json`
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-gamma-cs1004/` (authored inventory + `released` campaign status)
- Continuity prerequisite modules/tests from PB-002 included on the same tip (see commit)

## Files Modified

- `app/application/educational_packages/selection.py` — CG-D1…CG-R1 day order
- Campaign `campaign.json` status → `released`
- PB-002 continuity/withhold wiring paths (see commit `f1ff5dc`)

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 62 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only.

## Technical Debt

Finish/Home `tomorrow_preview` UI for shared `topic_code` multi-day packages remains syllabus-stale (see verification residual). Not introduced by Gamma JSON content.

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification; students in production still face one-mission-per-calendar-day pacing.
