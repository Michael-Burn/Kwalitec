# RO-002 — Deployment Report

**Programme:** RO-002 — Wave 2 LIVE Release Operations  
**Authority:** EP-001 Wave 2 / HR-002 Publication APPROVED · EF-001  
**Date:** 2026-08-01  
**Host:** https://kwalitec.onrender.com  
**Nature:** Operations only — educational package bodies unmodified; Educational Framework / Runtime redesign not in scope  

---

## Summary

Campaign Delta / CS1-003 (CD-D1…CD-R3) was jointly activated on the EA-006 live publication path, committed, pushed to `main`, and deployed to Render. LIVE fingerprint matches tip `b99b0a8f445d96ea9d700dc8f6276898460562b6`. Inventory hard-assert confirms **40** `publication_approved` CS1 packages including **27** Delta days, with Trust Front entry at **4.1 → CD-D1** and CD-R1 → **CD-D6** (EA-006 orphan superseded). Continuity wiring extends `_CAMPAIGN_DAY_ORDER` with CD-D1…CD-R3 (indices 14–40) — same class of ops prerequisite as RO-001 Gamma day-order registration, not a Runtime redesign.

---

## Phase 1 — Activation (joint inventory)

| # | Package | campaign_day | Live path | Status |
|---|---------|--------------|-----------|--------|
| 1–5 | 4.1.1…4.1.5 Learning | CD-D1…CD-D5 | `educational_packages/cs1/4.1.*-cs1003.json` | `publication_approved` |
| 6 | Linear models Revision | CD-R1 | `…/revision-linear-models-cs1003.json` | `publication_approved` |
| 7–16 | 4.2.1…4.2.10 Learning | CD-D6…CD-D15 | `…/4.2.*-cs1003.json` | `publication_approved` |
| 17 | Regression/GLM Revision | CD-R2 | `…/revision-regression-glm-cs1003.json` | `publication_approved` |
| 18–26 | 5.1.1…5.1.9 Learning | CD-D16…CD-D24 | `…/5.1.*-cs1003.json` | `publication_approved` |
| 27 | Mid-spine Revision | CD-R3 | `…/revision-midspine-cs1003.json` | `publication_approved` |

**FP-01:** All **27** activated together — no Isolated Golden Day.  
**Catalogue originals** under `educational_campaigns/.../campaign-delta-cs1003/packages/` remain `campaign_member_certified` (bodies untouched).  
**Campaign status:** `campaign.json` → `released`.  
**Orphan supersession:** `4.2-glm-structure-ea006.json` status → `superseded_by_campaign_delta` (removed from live loader admission).  
**Continuity wiring:** `_CAMPAIGN_DAY_ORDER` extended CD-D1…CD-R3 (14–40).

Activation field changes on live copies only: `status`, `publication_version` (`cs1003-live-1.0.0`), `published_at`.

---

## Phase 2 — Git + Render deploy

| Field | Value |
|-------|--------|
| Branch | `main` |
| Tip | `b99b0a8f445d96ea9d700dc8f6276898460562b6` |
| Push | `a2adf49..b99b0a8` → `origin/main` |
| Service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy ID | `dep-d9n1qi2jnfac73a7d9l0` |
| Trigger | API `clearCache` |
| Status progression | `build_in_progress` → `pre_deploy_in_progress` → `update_in_progress` → `live` |
| Application version | `2.0.0-beta.1` |
| Alembic | `202607310002` (unchanged) |

### Fingerprint / health (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health.commit` | `b99b0a8f…` | match | **PASS** |
| `/health/live` | ok | ok | **PASS** |
| `/health/ready` | ready | ready | **PASS** |
| `/health` | production / DB connected | ok | **PASS** |
| Migrations | current=head=`202607310002` | match | **PASS** |

Evidence: `knowledge/evidence/releases/RO002/health.json`, `health_ready.json`, `health_live.json`, `deploy_status.json`.

---

## Phase 3 — LIVE inventory assert

Render one-off `job-d9n1rotaeets73b1td3g` **succeeded** with hard asserts:

- `len(all_approved()) == 40`
- Delta `campaign_day` prefix `CD-` count **27**
- Orphan `CS1-EA005-PKG-4.2-GLM-STRUCTURE` **not** in approved inventory
- Cold entry `syllabus_topic_code=4.1` → **CD-D1**
- After simulated CD-R1 completion → **CD-D6** / `CS1-EP001-PKG-4.2-EXPONENTIAL-FAMILY`

---

## Phase 4 — Scope lock confirmation

| Constraint | Observed |
|------------|----------|
| Educational package bodies unmodified | **Met** — catalogue JSON educational fields unchanged |
| Wave 3 not started | **Met** |
| Educational Framework unmodified | **Met** |
| No Isolated Golden Day | **Met** |
| Runtime redesign | **Not performed** — only CD day-order registration + orphan disposition |
| Recommendation logic unmodified | **Met** |

---

## Deployment verdict

# **PASS — Wave 2 Delta inventory jointly LIVE**

Companion verification: `RO002_LIVE_VERIFICATION_REPORT.md`.  
Progressive confidence: `PB004_PROGRESSIVE_CONFIDENCE_REPORT.md`.  
Release decision: `RO002_RELEASE_DECISION.md`.

---

## Files Created (activation)

- `app/curriculum/data/educational_packages/cs1/4.1.*-cs1003.json` (5)
- `app/curriculum/data/educational_packages/cs1/4.2.*-cs1003.json` (10)
- `app/curriculum/data/educational_packages/cs1/5.1.*-cs1003.json` (9)
- `app/curriculum/data/educational_packages/cs1/revision-*-cs1003.json` (3)
- Catalogue tree `app/curriculum/data/educational_campaigns/cs1/campaign-delta-cs1003/` (authored inventory + `released` campaign status)

## Files Modified

- `app/application/educational_packages/selection.py` — CD-D1…CD-R3 day order
- `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json` — superseded
- Campaign `campaign.json` status → `released`
- Tests updated for Delta supersession of orphan / 4.1 live inventory

## Tests Executed

```text
pytest tests/application/educational_packages/ \
       tests/domain/session_experience/test_pb002_reflection_packages.py \
       tests/domain/session_experience/test_terminology.py -q
→ 99 passed
```

LIVE inventory assert job succeeded.

## Migration Impact

None.

## Architecture Compliance

EA-006 live loader contract preserved (`educational_packages/` + `publication_approved`). Curriculum V1/V2 loaders untouched. Campaign catalogue remains audit trail; student path uses live copies only. PB-002 selection extended for Delta campaign days only.

## Technical Debt

None introduced by activation. Soft title-keyword package resolution remains ambiguous across large inventory (pre-existing; RO1-R1 already prefers package-id / journey state for chrome).

## Known Limitations

Ops calendar backdating used between study days for same-session multi-day LIVE verification; students in production still face one-mission-per-calendar-day pacing. Delta is an independent Trust Front (not Continuity Front successor of Gamma).
