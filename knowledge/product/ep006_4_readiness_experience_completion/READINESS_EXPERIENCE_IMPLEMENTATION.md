# EP-006.4 — Readiness Experience Implementation

**Programme:** EP-006.4 — Readiness Experience Completion  
**Date:** 2026-07-26  
**Status:** Implemented  
**Constraint:** Presentation delivery only — no readiness scoring / authority changes  
**Addresses:** EP-006.3 residual **PERC-01** (Home `readiness_drivers` empty); EP-005.2 **REM-05**; EP-006.1 **MES-05** Home residual

---

## 1. Design principles

1. **Same Runtime A surface as Analytics** — Home loads `ReadinessService.get_dashboard_readiness_surface` and maps via `RuntimeAPresentationAdapter.readiness_narrative` (pass-through when schema-complete).
2. **No second narrator** — presentation maps authored fields; does not invent drivers, scores, or why-copy.
3. **Fail-open** — if the readiness surface is unavailable or `student_id` is non-numeric, Home continues with score/trend + recommendation cue fallbacks (EP-006.2 interim behaviour).
4. **No ReadinessService decision changes** — quality contract and scoring paths untouched.
5. **Preserve recommendation MES** — Coach / recommendation explanation path from EP-006.2 remains intact; readiness card prefers dedicated readiness MES when present.

---

## 2. Complete readiness explanation flow

```
ReadinessService.get_dashboard_readiness_surface (authored MES)
  → RuntimeAPresentationAdapter.readiness_narrative (pass-through / twin / legacy)
  → readiness_explanation_from_narrative → ReadinessExplanationSnapshot
  → HomeService.home attaches snapshot (fail-open)
  → home_vm / ReadinessCardViewModel
  → student/home.html
       L1: why_this_estimate + suggested_next_action (+ score / trend / confidence cue)
       L2 (≤1 disclosure “Why this estimate?”):
         readiness_drivers ≤4
         supporting_evidence
         confidence_label + confidence_basis
         review_point
```

### Field map (Home)

| MES field | L1 (always when present) | L2 (disclosure) | Source |
|---|---|---|---|
| Judgement (band / %) | **M** | **M** | Twin score / label on HomeSnapshot |
| Why this estimate | **M** | **M** | `why_this_estimate` |
| Confidence | **O** lexical on body | **M** + basis | `confidence_label` / `confidence_basis` |
| Suggested next action | **M** | **M** | `suggested_next_action` |
| Readiness drivers | — | **M** ≤4 ordered | `readiness_drivers` |
| Supporting evidence | — | **M** | `supporting_evidence` |
| Review point | — | **M** | `review_point` |
| Expected benefit | **O** | **O** | `expected_benefit` |
| Cannot yet estimate | **M** when applicable | **M** | `can_estimate=False` / honest refusal surface |

### Fallback behaviour

| Condition | Home behaviour |
|---|---|
| Schema-complete readiness surface | Full MES on readiness card |
| Surface raises / unavailable | `readiness_explanation=None`; score/trend still show; next/review may fall back to recommendation explanation cues |
| Incomplete schema (no drivers) | Partial narrative; `is_complete=False`; empty driver list; no invented drivers |
| Non-numeric student_id (unit fakes) | Skip surface load; no crash |

---

## 3. Explicit non-changes

- ReadinessService scoring / weights / aggregation math  
- `apply_readiness_quality_contract` educational authorship rules  
- RecommendationService / PlanningService authority  
- Product Constitution (advice remains advisory)  
- P-001.2 field definitions (delivery only)

**STOP check:** No duplicated educational reasoning. Home consumes the same surface Analytics already uses.

---

## 4. Work landed

| ID | Change | Paths |
|---|---|---|
| RDX-01 | `ReadinessExplanationSnapshot` DTO | `dto/readiness_explanation_snapshot.py`, `home_snapshot.py` |
| RDX-02 | Pass-through loader + narrative mapper | `readiness_explanation.py` |
| RDX-03 | HomeService attaches readiness MES fail-open | `home_service.py` |
| RDX-04 | `home_vm` prefers readiness MES; disclosure flags | `view_models.py` |
| RDX-05 | Home template L2 drivers / evidence / confidence / review | `student/home.html` |
| RDX-06 | Adapter `confidence_basis` pass-through | `adapter.py`, `ReadinessNarrative` |
| RDX-07 | Regression tests | `test_readiness_experience_delivery.py` |

---

## 5. Validation status

| Check | Result |
|---|---|
| Driver delivery | Pass (automated) |
| Explanation completeness | Pass (automated) |
| Home rendering | Pass (template smoke) |
| Fallback behaviour | Pass (automated) |
| Tier B readiness re-perception | **Ready for successor** — not executed in this programme |

---

## References

- [`READINESS_TRACEABILITY.md`](READINESS_TRACEABILITY.md)  
- EP-006.1 `MES_DELIVERY_SPECIFICATION.md` §3.3  
- EP-006.3 `MES_PERCEPTION_REPORT.md` PERC-01  
- EP-005.2 REM-05  

---

**End of READINESS_EXPERIENCE_IMPLEMENTATION**
