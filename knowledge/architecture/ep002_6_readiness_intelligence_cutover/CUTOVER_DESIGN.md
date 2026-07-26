# EP-002.6 — Cutover Design

**Milestone:** EP-002.6 — Readiness Intelligence Dual-Run & Gated HTTP Cutover  
**Date:** 2026-07-26  
**Status:** Binding design for implementation  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Intent

```
Dashboard / Analytics readiness request
        │
        ▼
ReadinessService.get_dashboard_readiness_surface()
        │
        ├─ cutover ineligible
        │       ├─ legacy surface (score + weak/strong)
        │       └─ dual-run side-car when Twin ON ∧ non-prod
        │
        └─ cutover eligible
                │
                ├─ compute legacy surface (fail-open + alignment baseline)
                ├─ build_readiness_intelligence()  (fail-open)
                │
                ├─ Twin None / exception / blocking limitation
                │         └──► return legacy surface
                │
                └─ Twin success + non-blocking
                          └──► project → surface DTO
                               record semantic alignment
                               return projection (influences_student=True)
```

Student always receives a valid surface dict (legacy or projected). Dual-run never changes student payloads.

---

## 2. Dual-run (diagnostic)

| Rule | Behaviour |
|---|---|
| Eligibility | Twin ON ∧ non-production `APP_ENV` |
| Host | Surface facade when cutover **not** eligible/active |
| Compare | Legacy surface vs `build_readiness_intelligence` |
| Capture | Fingerprints, score delta, confidence, limitation codes, area topic ids, latencies |
| Influence | `influences_student=False` always |
| Fail-open | Twin exceptions swallowed |
| Dedupe | Request-scoped; nested ContextVar guard |
| Skip when | Readiness cutover eligible or active |

---

## 3. Cutover eligibility (request attempt)

All required before Twin may influence the HTTP response:

| Condition | Required |
|---|---|
| `ENABLE_DIGITAL_TWIN` | True |
| `ENABLE_READINESS_INTELLIGENCE_CUTOVER` | True |
| `APP_ENV` / `FLASK_ENV` | Not `production` / `prod` |

Authority flag is **recorded**, not required for this Runtime A Foundation path.

Post-Twin serving gates:

| Condition | Required |
|---|---|
| Twin response | Non-`None` dict |
| Exceptions | None (caught → fallback) |
| Blocking limitation | Absent |
| Projection | Non-empty readiness score present |

---

## 4. Fallback rules

Immediately return legacy surface when:

| Trigger | Fallback reason code |
|---|---|
| Twin OFF | `twin_off` |
| Cutover flag OFF | `cutover_flag_off` |
| Production env | `production_env` |
| Configuration / flag resolve failure | `configuration_failure` |
| `build_readiness_intelligence` returns `None` | `twin_unavailable` |
| Twin raises | `twin_exception` |
| Blocking limitation | `blocking_limitation` |
| Projection missing score | `projection_empty` |

---

## 5. Blocking limitations

```
BLOCKING_CODES = {
  "twin_foundation_flag_off",
  "canonical_learner_state_unavailable",
  "invalid_student_id",
}
```

Also blocking when:

- `readiness_score` is `None`
- `availability` is present and not `available`

Non-blocking alone: `planner_outputs_unavailable`, sparse-evidence style codes.

---

## 6. Projection contract

Twin assessment → surface DTO:

| Twin field | Surface field |
|---|---|
| `readiness_score` | `readiness["score"]` |
| Drivers `curriculum_coverage` / `knowledge_strength` / `mission_discipline` | `coverage_pct` / `avg_mastery` / `review_discipline` |
| Legacy baseline fill | `total_topics`, `topics_started`, `topics_mastered` when Twin omits |
| `weakest_areas` | `weakest_topics` rows (`topic_id`, `topic_name`, `mastery_score`, …) |
| `strongest_areas` | `strongest_topics` rows |
| `confidence_level` | top-level + on readiness dict |
| `limitations_codes` | top-level |
| `readiness_drivers` / `recommended_next_actions` | optional extras |
| constant | `source_authority="readiness_intelligence"` |

Templates continue to consume `readiness`, `weakest_topics`, `strongest_topics`.

---

## 7. Semantic alignment

Not fingerprint equality. Capture:

| Status | Meaning |
|---|---|
| `aligned` | Score agreement ∧ (area overlap or both empty) |
| `mismatched` | Twin served but score/area disagreement |
| `twin_unavailable` | Pre-attempt or Twin failure fallback |
| `limitation_fallback` | Blocking limitation / empty projection |

Score agreement: `|legacy.score − twin.readiness_score| ≤ 10`.  
Confidence agreement recorded as boolean field (Twin confidence present when score served).  
Limitation agreement: blocking codes ↔ limitation_fallback status.

---

## 8. HTTP wiring

| Location | Change |
|---|---|
| `ReadinessService` | Add `get_dashboard_readiness_surface`; dual-run hook when cutover ineligible |
| `dashboard/routes.py` | Call surface facade; skip explainability enrich when Twin authority |
| `analytics/routes.py` | Same surface facade (limits 5/5) |
| Legacy getters | **Unchanged** (collectors / bridges / settings) |
| Templates | Unchanged |

---

## 9. Module layout

| Module | Role |
|---|---|
| `consumer_chain/readiness_dual_run.py` | Side-car compare |
| `consumer_chain/readiness_cutover.py` | Eligibility, projection, orchestration |
| `consumer_chain/readiness_dual_run_health.py` | Dual-run metrics |
| `consumer_chain/readiness_cutover_health.py` | Cutover metrics |
| `v2_flags.py` | `ENABLE_READINESS_INTELLIGENCE_CUTOVER` |

---

## 10. Coordination with Study Insights

Readiness and Study Insights cutovers are independent flags and ContextVars.  
A request may serve Study Insights recommendations and legacy readiness (or both Twin) depending on each flag.  
Neither cutover wraps the other's legacy builder.

---

## 11. Rollback

Kill switches: Cutover OFF → Twin OFF → production env. See `ROLLBACK_PLAN.md`.
