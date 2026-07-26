# MIG-003 — Head Alignment Matrix

**Programme:** MIG-003 — Migration Contract Alignment  
**Date:** 2026-07-27  
**Authoritative production head:** `202607260001`  
**Search term:** `202607230002`

Every repository occurrence of `202607230002` was classified. Category A items were updated to `202607260001`. Categories B–D were left unchanged.

---

## Classification legend

| Cat | Meaning | Action |
|---|---|---|
| **A** | Current operational expectation (CI, startup/ops validation, test helper, checklist) | **Updated** |
| **B** | Historical documentation | Unchanged |
| **C** | Migration history (revision id / `down_revision` / file presence) | Unchanged |
| **D** | Archived programme reports | Unchanged (none claimed the *current* head is still `202607230002` as live truth after MIG-002; residual “still assert” notes describe pre-MIG-003 debt) |

---

## Complete inventory

### Category A — updated

| File | Role | Previous | New | Reason |
|---|---|---|---|---|
| `tests/operational/helpers.py` | Operational test constant `ALEMBIC_HEAD` | `202607230002` | `202607260001` | Single-head pin used by alpha configuration tests and checklist needle |
| `.github/workflows/ci.yml` | CI “Migration scripts load” assert | `assert head == "202607230002"` | `assert head == "202607260001"` | CI must accept the unique Alembic tip |
| `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md` | D8 head requirement | Head must be `202607230002` | Head must be `202607260001` | Live alpha/deploy checklist |
| `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md` | `flask db current` comment | expect `202607230002` | expect `202607260001` | Same operational contract |
| `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md` | Operational caveats | upgrade to `202607230002` | upgrade to `202607260001` | Same operational contract |

### Category B — historical documentation (unchanged)

| File | Context |
|---|---|
| `knowledge/product/mig001/*` | Forensic dual-head investigation; cites then-stale CI pin and chain parentage |
| `knowledge/product/mig002/*` | Graph repair reports; documents residual stale pin as follow-up for MIG-003 |
| `knowledge/product/analytics/PHASE_A_IMPLEMENTATION_REPORT.md` | Records analytics revision revises `202607230002` |

### Category C — migration history (unchanged)

| File | Context |
|---|---|
| `migrations/versions/202607230002_pr001_rbac_identity.py` | Revision identity for PR-001 RBAC |
| `migrations/versions/202607240001_prd001_analytics_event_infrastructure.py` | `down_revision = "202607230002"` (correct parent link) |
| `tests/operational/test_alpha_configuration.py` L168 | Asserts RBAC migration **file exists** on disk (history presence), not that it is the tip. Tip assertion uses `ALEMBIC_HEAD` (Category A, updated via helper). |

### Category D — archived / programme reports (unchanged)

MIG-001 and MIG-002 reports under `knowledge/product/mig001/` and `knowledge/product/mig002/` document the historical stale pin and call out the follow-up. They do not redefine the post-MIG-003 live contract. Left as written.

### Non-contract fixture (unchanged)

| File | Context | Classification note |
|---|---|---|
| `tests/ga/test_failure_modes.py` | Mock `meta={"current": "old", "head": "202607230002"}` for degraded migration health | Not an operational head pin; asserts only `status == "degraded"`. Left per “do not fix unrelated tests”. |

---

## Explicit non-updates (scanned, no Category A pin)

| Location | Finding |
|---|---|
| `docs/production/RUNBOOK.md` | Says `expect head` without a revision id |
| `.cursor/RELEASE_CHECKLIST.md` | Says `expect head` without a revision id |
| `knowledge/release/VERSION1_RC1.md` | Historical RC pin `202607160003` — not this programme’s obsolete tip |
| `app/services/startup_service.py` | Resolves head dynamically; no hard-coded `202607230002` |
| Migration graph files under `migrations/versions/` | **Not modified** by MIG-003 |

---

## Post-update contract

| Component | Expected head |
|---|---|
| Alembic script directory | `202607260001` (unique) |
| `ALEMBIC_HEAD` | `202607260001` |
| CI Migration scripts load | `202607260001` |
| Internal Alpha checklist | `202607260001` |
