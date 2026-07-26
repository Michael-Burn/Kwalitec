# EP-002.5 — Cutover Design

**Milestone:** EP-002.5 — Study Insights Gated HTTP Cutover  
**Date:** 2026-07-26  
**Status:** Binding design for implementation  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Intent

```
Dashboard / Home request
        │
        ▼
RecommendationService.get_dashboard_recommendations()
        │
        ├─ cutover ineligible ──► generate_recommendations() ──► legacy list
        │
        └─ cutover eligible
                │
                ├─ compute legacy (fail-open ready + alignment baseline)
                ├─ build_study_insights()  (fail-open)
                │
                ├─ Twin None / exception / blocking limitation
                │         └──► return legacy
                │
                └─ Twin success + non-blocking
                          └──► project Study Insights → list[dict]
                               record alignment
                               return projected rows (influences_student=True)
```

Student always receives a valid recommendation list (possibly empty only when legacy is empty).

---

## 2. Eligibility (request attempt)

All required before Twin may influence the HTTP response:

| Condition | Required |
|---|---|
| `ENABLE_DIGITAL_TWIN` | True |
| `ENABLE_STUDY_INSIGHTS_CUTOVER` | True |
| `APP_ENV` / `FLASK_ENV` | Not `production` / `prod` |

Authority flag is **recorded**, not required for this Runtime A Foundation path.

Post-Twin serving gates (must also pass):

| Condition | Required |
|---|---|
| Twin response | Non-`None` dict |
| Exceptions | None (caught → fallback) |
| Blocking limitation | Absent |

---

## 3. Fallback rules

Immediately return legacy `generate_recommendations` when:

| Trigger | Fallback reason code |
|---|---|
| Twin OFF | `twin_off` |
| Cutover flag OFF | `cutover_flag_off` |
| Production env | `production_env` |
| Configuration / flag resolve failure | `configuration_failure` |
| `build_study_insights` returns `None` | `twin_unavailable` |
| Twin raises | `twin_exception` |
| Blocking limitation codes | `blocking_limitation` |
| Projection yields empty actionable rows | `projection_empty` |

---

## 4. Blocking limitations

```
BLOCKING_CODES = {
  twin_foundation_flag_off,
  canonical_learner_state_unavailable,
  invalid_student_id,
}
```

Also blocking when **both** actionable fields are missing:

- `todays_key_focus` is None **and** `recommended_next_action` is None  
- or both `todays_key_focus_unavailable` and `recommended_next_action_unavailable` appear in `limitations_codes`

Non-blocking examples: `sparse_evidence`, single field unavailable with another actionable field present.

---

## 5. HTTP projection

Project `StudyInsightGuidance.to_dict()` into legacy-compatible rows:

| Twin field | Row mapping |
|---|---|
| `todays_key_focus` | Primary row: `title`/`reason` from field; `category=Study Focus`; `priority=High` |
| `recommended_next_action` | `next_action` on primary (or dedicated row if focus absent) |
| `greatest_risk` | Optional High/Critical risk row |
| `strongest_area` | Optional Low informational row |
| `workload_explanation` / `readiness_explanation` | Folded into `educational_advice` / `reason` on primary when present |
| `limitations_codes` | Copied onto each projected row as `limitations_codes` |
| — | `source_authority="study_insights"` |

Template contract preserved: `title`, `priority`, `category`, `reason`, `expected_benefit`, `next_action`, explainability fields.

Dashboard skips `EducationalExplainabilityService.enrich_recommendations` when `source_authority == "study_insights"`.

---

## 6. Alignment analysis

Lightweight semantic compare (not fingerprint equality):

| Signal | Method |
|---|---|
| Twin topic ids | Extract `topic_id` from InsightField dicts |
| Legacy topic tokens | Normalise legacy `title` / `reason` strings; match topic_id substrings / known labels |
| Category overlap | Legacy categories vs Twin field presence (focus→Study Focus, risk→risk language) |
| Outcomes | `aligned` · `mismatched` · `twin_unavailable` · `limitation_fallback` |

Alignment never blocks serving when Twin is otherwise eligible; it is an ops quality signal for Architecture Metrics.

---

## 7. Dual-run coexistence

When cutover flag is eligible (Twin ON ∧ Cutover ON ∧ non-prod):

- `_maybe_study_insights_dual_run` **skips** — cutover owns the Twin invocation  
- Alignment + cutover telemetry replace dual-run for that request path  

When cutover flag OFF and Twin ON non-prod:

- EP-002.4 dual-run behaviour unchanged  

---

## 8. Wiring points

| Layer | Change |
|---|---|
| `consumer_chain/cutover.py` | Eligibility, blocking check, projection, alignment, orchestrator |
| `consumer_chain/cutover_health.py` | In-process Architecture Metrics |
| `consumer_chain/telemetry.py` | `emit_cutover` |
| `RecommendationService` | `get_dashboard_recommendations` / `get_dashboard_today_recommendation` |
| `dashboard/routes.py` | Call dashboard methods; conditional enrich skip |
| `v2_flags.py` | `ENABLE_STUDY_INSIGHTS_CUTOVER` |

No schema migrations. No new recommendation engine. No ownership changes.

---

## 9. Telemetry

| Field | Meaning |
|---|---|
| `cutover_attempted` | Eligibility passed for attempt |
| `cutover_served` | Twin projection returned to student |
| `fallback_reason` | Why legacy was returned |
| `alignment_status` | aligned / mismatched / unavailable / limitation_fallback |
| `influences_student` | True only when Twin projection served |
| latencies | legacy + Twin |
| flags | twin / authority / cutover |
| limitation_codes | From Twin payload |

---

## 10. Out of scope

- Production-wide activation  
- Readiness / mission cutover (EP-002.6–7)  
- Presentation consolidation (WS7)  
- MissionOptimizer un-quarantine  
- Template redesign beyond enrich skip  
- New Twin / planner / readiness engines  
