# EP-006.2 — MES Delivery Implementation Notes

**Programme:** EP-006.2 — MES Delivery Implementation  
**Date:** 2026-07-26  
**Status:** Implemented against [`../ep006_1_mes_end_to_end_delivery/MES_DELIVERY_SPECIFICATION.md`](../ep006_1_mes_end_to_end_delivery/MES_DELIVERY_SPECIFICATION.md)  
**Constraint:** Presentation delivery only — no educational reasoning changes

---

## 1. Design principles applied

1. **Pass-through first** — when schema-complete MES exists, map authored fields 1:1.  
2. **Re-narration is fallback only** — reason-code synthesis only for incomplete / cold-start payloads.  
3. **Widen before render** — DTOs widened before template claims.  
4. **Reuse macros** — `explanation_card`, `learn_more`, `explainability_block`.  
5. **No educational math in presentation**.

---

## 2. Work packages landed (MES-01…08)

| ID | Change | Primary paths |
|---|---|---|
| **MES-01** | Widen `ExplanationSnapshot`, domain `RecommendationExplanation`, `JourneyContext`, Home VMs | `dto/explanation_snapshot.py`, `recommendation_explanation.py`, `unified_journey/contracts.py`, `view_models.py` |
| **MES-02** | Pass-through authored MES in bridge mapper + `ExplanationService.from_opaque` | `recommendation_mapper.py`, `explanation_service.py`, `home_service.py` |
| **MES-03** | Wire `explanation_card` on Home; L1 why + next always visible | `student/home.html`, `explanation_card.html` |
| **MES-04** | Relax Coach hard clip when L2 disclosure exists | `view_models._compose_coach_insight` |
| **MES-05** | Restore readiness drivers + review_point on Analytics / schema path | `RuntimeAPresentationAdapter._schema_readiness_narrative`, `analytics/index.html`, Home readiness disclosure |
| **MES-06** | Restore plan drivers + review_point on Mission | `RuntimeAPresentationAdapter._schema_mission_narrative`, `mission/index.html`, JourneyContext MES slots |
| **MES-07** | Presentation contract tests | `tests/presentation/student/test_mes_delivery_contract.py`, `test_home_template_mes.py` |
| **MES-08** | Dual-home MES parity smoke | `tests/presentation/test_dual_home_mes_parity.py` |

**Deferred (by design):** MES-09 Tier B perception pack; MES-10 personalisation factor disclosure (flag OFF).

---

## 3. Field delivery map (Home path)

```
RecommendationService (schema-complete MES)
  → recommendation_mapper (MES keys preserved on projection + explanation)
  → HomeService (merge top-level + nested explanation)
  → ExplanationService.from_opaque (authored why / evidence / next / review)
  → ExplanationSnapshot (widened DTO)
  → home_vm / ExplanationViewModel
  → home.html L1 (why + next) + explanation_card L2
```

---

## 4. Explicit non-changes

- RecommendationService decision-making / ranking  
- PlanningService authority / plan optimisation  
- ReadinessService authority / readiness weights  
- Product Constitution (advice remains advisory)  
- P-001.2 field definitions (delivery only)

**STOP check:** No duplicated educational reasoning introduced. Presentation maps and layouts only.

---

## 5. Validation status

| Check | Result |
|---|---|
| Automated contract tests | Pass |
| Dual-home parity smoke | Pass |
| Home template smoke (L1 + card) | Pass |
| Dogfood checklist | Ready for internal use (criteria in EP-006.1 Spec §6.1) |
| Tier B blind re-review | **Not run** — successor / MES-09 |
| Validated K8 ≥ 70 | **Not claimed** — EP-005.1 remains authoritative until re-score |

---

## References

- EP-006.1 Delivery Spec + Traceability + K8 Remediation Plan  
- P-001.2 Explainability Standard  
- EP-003.1–.3 service-layer schema completeness  

---

**End of MES_DELIVERY_IMPLEMENTATION**
