# EP-002.5 — Rollback Plan

**Milestone:** EP-002.5 — Study Insights Gated HTTP Cutover  
**Date:** 2026-07-26  
**Kill-switch first:** Yes

---

## 1. Intent

Restore legacy-only student recommendations on dashboard/home within one process restart (or immediate env flip + restart), without schema rollback or code revert.

---

## 2. Primary kill switches (preferred order)

| Order | Action | Effect |
|---|---|---|
| 1 | Set `KWALITEC_STUDY_INSIGHTS_CUTOVER=0` (or unset) | Cutover attempts stop; dual-run may continue if Twin ON non-prod |
| 2 | Set `KWALITEC_DIGITAL_TWIN=0` (or unset) | Twin OFF; cutover ineligible; Authority forced OFF |
| 3 | Ensure `APP_ENV=production` processes never have cutover ON | Production remains ineligible by design |

Restart web processes after env change.

---

## 3. Verification checklist

After kill switch:

1. Confirm flag resolve: `ENABLE_STUDY_INSIGHTS_CUTOVER is False` (and/or Twin OFF).  
2. Hit `/dashboard` as a test student → recommendation cards match legacy shape / content path.  
3. Confirm cutover telemetry shows `cutover_served=False` (or no cutover events).  
4. Confirm no template errors / empty-only regressions beyond pre-existing empty legacy cases.  
5. Optional: re-enable dual-run observation with Twin ON + Cutover OFF in staging.

---

## 4. Drill expectations

| Drill | Expected |
|---|---|
| Cutover ON → OFF mid-staging | Next requests serve legacy; no exception |
| Twin ON → OFF while Cutover ON | Legacy; Authority resolves OFF |
| Twin exception injection | Fail-open legacy for that request |
| Blocking limitation fixture | Fail-open legacy for that request |

---

## 5. What not to do

- Do not drop tables or run reverse migrations (none exist for this milestone).  
- Do not delete dual-run or Twin packages as “rollback.”  
- Do not force-push or revert EP-002.1–4 observability as part of cutover rollback.  
- Do not enable production Twin / Cutover to “test rollback.”  

---

## 6. Escalation

If kill switch does not restore legacy behaviour:

1. Confirm process actually restarted with new env.  
2. Confirm dashboard path is not serving EI card exclusively (separate flag).  
3. Inspect `CONSUMER_CHAIN_CUTOVER` / application logs for unexpected `cutover_served=True`.  
4. Code-level: ensure deploy matches commit with fail-open cutover; hot-patch only if env flip insufficient.  
