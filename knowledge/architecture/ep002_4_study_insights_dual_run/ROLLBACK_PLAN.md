# EP-002.4 — Rollback Plan

**Milestone:** EP-002.4 — Study Insights Dual-Run  
**Goal:** Stop Twin Study Insights dual-run immediately without changing student-visible behaviour (student path was always legacy).

---

## 1. Kill switch (binding)

```
Dual-run active (Twin ON, non-prod)
        │
        ▼
KWALITEC_DIGITAL_TWIN=0
        │  • build_study_insights → None / unavailable
        │  • is_dual_run_diagnostics_eligible → False
        │  • Authority auto-resolves OFF
        ▼
Legacy generate_recommendations only (pre-dual-run posture)
```

Optional belt-and-braces: set `KWALITEC_DIGITAL_TWIN_AUTHORITY=0`.

Production: dual-run is **already ineligible** when `APP_ENV`/`FLASK_ENV` is `production`/`prod`, even if Twin were mistakenly ON.

---

## 2. What rollback restores

| Concern | After Twin OFF |
|---|---|
| Student HTTP recommendations | Unchanged (always legacy) |
| `build_study_insights` | Returns `None` |
| Dual-run telemetry | Stops emitting comparison events |
| Experience TwinPort | ExperienceTwinAdapter (Authority OFF) |
| Schema / data | Unchanged (no Twin writes; no migrations) |

---

## 3. Verification steps

1. With Twin ON (non-prod), invoke `generate_recommendations` → confirm dual-run telemetry / metrics increment; response equals legacy-only control.  
2. Set Twin OFF; invoke again → confirm no dual-run emission; response still equals control.  
3. With Twin ON + `APP_ENV=production` (test environ override) → confirm dual-run skipped.  
4. Confirm templates / route return shapes unchanged.  
5. Record rollback success only when student payload identity and dual-run cessation both hold.

Automated coverage: feature-flag / rollback validation tests under `tests/infrastructure/adapters/consumer_chain/`.

---

## 4. Emergency (non-prod ops)

| Symptom | Action |
|---|---|
| Twin dual-run latency pressure | Twin OFF immediately |
| Unexpected comparison noise | Twin OFF; dual-run is diagnostic only |
| Suspected student payload change | Compare response to Twin OFF control; Twin OFF; open incident — dual-run must never merge |

---

## 5. What rollback does **not** require

- Database restore  
- Schema reverse migration  
- Code redeploy beyond env flag flip (for ops kill switch)  
- Clearing student educational facts  

---

## 6. Success definition

Rollback succeeds when Twin OFF (or production env) yields:

1. No Study Insights dual-run comparison emissions for new requests  
2. Identical student-facing recommendation payloads vs a legacy-only baseline  
3. Zero ownership / schema side effects  

**Observation:** Dual-run is fail-open and non-authoritative by design.  
**Evidence:** Eligibility gate + return-path identity.  
**Conclusion:** Twin OFF is a complete dual-run kill switch.  
**Recommendation:** Keep production Twin OFF; treat any production dual-run as a configuration incident.
