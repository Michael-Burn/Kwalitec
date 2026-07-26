# EP-002.4 — Dual-Run Design

**Milestone:** EP-002.4 — Study Insights Dual-Run  
**Date:** 2026-07-26  
**Status:** Binding design for implementation  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Intent

```
Student request (non-prod, Twin ON)
        │
        ▼
generate_recommendations()  ──►  legacy list  ──►  HTTP / templates (unchanged)
        │
        └── (diagnostic side-car, fail-open)
                build_study_insights()
                structured comparison → telemetry / in-process metrics
```

Student-visible behaviour must be identical to Twin OFF / dual-run skipped.

---

## 2. Eligibility (no new flag)

Reuse `is_dual_run_diagnostics_eligible`:

| Condition | Required |
|---|---|
| `ENABLE_DIGITAL_TWIN` | True |
| `APP_ENV` / `FLASK_ENV` | Not `production` / `prod` |

Authority flag is **recorded**, not required. Authority ON/OFF must not change the student response.

---

## 3. Execution sequence

1. Time and compute legacy `generate_recommendations` body exactly as today.  
2. If ineligible → return legacy (no Twin call).  
3. If request-scoped dual-run already ran for this `user_id` → return legacy.  
4. Else invoke `build_study_insights(user_id)` inside try/except (fail-open).  
5. Extract structured comparison fields; emit telemetry; record metrics.  
6. Return **legacy list unchanged** (identity of list contents; no merge).

Twin exceptions, `None`, or limitation-heavy payloads never alter the return.

---

## 4. Wiring point

| Option | Verdict |
|---|---|
| Dashboard route only | Incomplete — misses bridges / other callers |
| Inside `build_study_insights` | Wrong — would couple observation to Twin API consumers only |
| **After legacy compute in `generate_recommendations`** | **Selected** — single authoritative student path; covers dashboard today+list (with dedupe) |

`generate_today_recommendation` inherits dual-run via `generate_recommendations(limit=1)`; request dedupe prevents a second Twin call when the list API also runs.

---

## 5. Comparison methodology

### 5.1 Fields captured (required)

| Field | Source |
|---|---|
| `legacy_latency_ms` | Wall time of legacy path segment for this invocation |
| `twin_latency_ms` | Wall time of `build_study_insights` call |
| `legacy_unavailable` | True when legacy list is empty |
| `twin_unavailable` | True when Twin result is `None` |
| `limitation_codes` | From Twin guidance (`limitations_codes`) |
| `confidence_level` / `confidence_available` | From Twin guidance when present |
| `legacy_categories` | Sorted unique `category` values from legacy rows |
| `twin_field_ids` | Present Insight field ids (e.g. `todays_key_focus`, `recommended_next_action`) when non-null |
| `correlation_id` / `causation_id` | `CorrelationContext.current()` |
| `twin_enabled` / `authority_enabled` | `resolve_v2_feature_flags` |
| `legacy_fingerprint` / `twin_fingerprint` | Existing opaque SHA helpers |
| `fingerprints_match` | Equality of fingerprints (expected often false) |
| `diagnostic_only` / `influences_student` | Always `True` / `False` |

### 5.2 What comparison must **not** do

- Rank, reorder, or filter legacy rows using Twin output  
- Expose comparison payloads in templates / JSON student APIs  
- Persist comparison rows to educational schema  
- Invent a third recommendation engine  

### 5.3 Divergence semantics

**O:** Payload shapes differ by design (list vs guidance dict).  
**C:** `fingerprints_match=false` is normal. Treat **category / focus / next-action topical alignment** as qualitative evidence for EP-002.5, not a hard pass/fail of EP-002.4.  
**R:** Report divergence rate + limitation-code frequency in the completion report metrics.

---

## 6. Telemetry & metrics

| Channel | Use |
|---|---|
| `ConsumerChainTelemetry.emit_dual_run` (extended) | Structured log + `CONSUMER_CHAIN_DUAL_RUN` event |
| Existing `observe_build_api` on Twin call | Twin outcome / latency (nested) |
| In-process dual-run health aggregator | Architecture metrics for COMPLETION_REPORT |

No PresentationTelemetry / analytics catalogue changes (EP-002 Analytics remains separate).

---

## 7. Flag matrix (expected behaviour)

| Twin | Authority | `APP_ENV` | Dual-run executes? | Student response |
|---|---|---|---|---|
| OFF | OFF | any | No | Legacy only |
| OFF | ON (env) | any | No (Authority forced OFF) | Legacy only |
| ON | OFF | non-prod | **Yes** | Legacy only |
| ON | ON | non-prod | **Yes** | Legacy only |
| ON | * | production | No | Legacy only |

---

## 8. Rollback (summary)

Kill switch: `KWALITEC_DIGITAL_TWIN=0` (Authority auto-clears). Dual-run eligibility fails closed. Full plan: [`ROLLBACK_PLAN.md`](ROLLBACK_PLAN.md).

---

## 9. Out of scope (EP-002.5+)

- Serving Twin insights in HTTP responses  
- Template copy changes  
- Production Twin ON  
- Readiness / mission dual-run surfaces  
- MissionOptimizer un-quarantine  

---

## 10. Design conclusions

**Observation:** EP-002.1 left an unwired fingerprint helper; EP-002.3 authorised planning.  
**Evidence:** Discovery of call sites + flag composition.  
**Conclusion:** Service-level fail-open dual-run with structured compare meets all EP-002.4 objectives without new flags or schema.  
**Recommendation:** Implement exactly this design; verify with Twin OFF/ON × Authority OFF/ON × production-ineligible tests.
