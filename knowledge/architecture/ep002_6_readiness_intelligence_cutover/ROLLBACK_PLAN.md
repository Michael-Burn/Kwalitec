# EP-002.6 — Rollback Plan

**Milestone:** EP-002.6 — Readiness Intelligence Dual-Run & Gated HTTP Cutover  
**Date:** 2026-07-26  
**Kill-switch first:** Yes

---

## 1. Intent

Restore legacy-only readiness on dashboard/analytics within one process restart
(or immediate env flip + restart), without schema rollback or code revert.

---

## 2. Primary kill switches (preferred order)

| Order | Action | Effect |
|---|---|---|
| 1 | Set `KWALITEC_READINESS_INTELLIGENCE_CUTOVER=0` (or unset) | Cutover attempts stop; dual-run may continue if Twin ON non-prod |
| 2 | Set `KWALITEC_DIGITAL_TWIN=0` (or unset) | Twin OFF; cutover ineligible; Authority forced OFF |
| 3 | Ensure `APP_ENV=production` processes never have cutover ON | Production remains ineligible by design |

Restart web processes after env change.

---

## 3. Verification checklist

After kill switch:

1. Confirm flag resolve: `ENABLE_READINESS_INTELLIGENCE_CUTOVER is False` (and/or Twin OFF).  
2. Hit `/dashboard` and `/analytics` as a test student → readiness score and topic lists match legacy path.  
3. Confirm cutover telemetry shows `cutover_served=False` (or no readiness cutover events).  
4. Confirm collectors still call pure `get_overall_readiness` (no Foundation recursion).  
5. Optional: re-enable dual-run observation with Twin ON + Cutover OFF in staging.

---

## 4. Drill expectations

| Drill | Expected |
|---|---|
| Cutover ON → OFF mid-staging | Next requests serve legacy; no exception |
| Twin ON → OFF while Cutover ON | Legacy; Authority resolves OFF |
| Twin exception injection | Fail-open legacy for that request |
| Blocking limitation fixture | Fail-open legacy for that request |
| Collector path under Twin ON | Unchanged legacy getters |

---

## 5. What not to do

- Do not drop tables or run reverse migrations (none exist for this milestone).  
- Do not delete dual-run, cutover, or Twin packages as “rollback.”  
- Do not force-push or revert EP-002.1–5 observability as part of cutover rollback.  
- Do not enable production Twin / Cutover to “test rollback.”  
- Do not wrap `get_overall_readiness` with intelligence during rollback testing.

---

## 6. Escalation

If kill switches do not restore legacy behaviour, treat as ownership / wiring defect:
disable Twin process-wide, capture cutover correlation ids, and revert the
dashboard/analytics surface facade wiring — not the EP-001.3 assessment package.
