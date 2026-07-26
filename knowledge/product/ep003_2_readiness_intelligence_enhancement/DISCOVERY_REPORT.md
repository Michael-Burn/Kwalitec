# EP-003.2 — Discovery Report

**Programme:** EP-003.2 — Readiness Intelligence Enhancement  
**Date:** 2026-07-26  
**Phase:** Discovery  

---

## 1. Sources reviewed

| Authority | Path | Relevance |
|---|---|---|
| P-001.1 KSI Framework | `knowledge/product/p001_1_ksi_baseline/` | K3 baseline **52**; readiness usefulness Partial |
| P-001.2 Explainability Standard | `knowledge/product/p001_2_explainability_standard/` | Mandatory Explanation Schema for readiness assessments |
| Product Constitution | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Final Test; honest, explainable guidance |
| Governance | `knowledge/GOVERNANCE.md` §4.2 | Explainability Review Checklist mandate |
| EP-002.9 baseline | `knowledge/architecture/ep002_9_programme_exit_certification/` | Ownership: Readiness evaluates; presentation does not |
| EP-003.1 outputs | `knowledge/product/ep003_1_recommendation_engine_enhancement/` | Quality-contract pattern to mirror |
| ReadinessService | `app/services/readiness_service.py` | Runtime A readiness authority |
| Readiness intelligence | `app/infrastructure/adapters/readiness_intelligence/` | EP-001.3 drivers / confidence / next actions |
| RuntimeAPresentationAdapter | `app/presentation/intelligence_surface/adapter.py` | Presentation selection only |
| Subsystem doc | `knowledge/subsystems/readiness.md` | Coverage vs composite coexistence |

---

## 2. Current Runtime A behaviour (pre-EP-003.2)

1. **Legacy composite** (`get_overall_readiness`): coverage 50% + mastery 30% + review 20% — no student confidence, drivers, or mandatory schema.
2. **Coverage-only** (`calculate_readiness`): syllabus weight completed — separate Learning Progress narrative on dashboard.
3. **Twin intelligence** (`build_readiness_intelligence`): named drivers, internal confidence bands (`very_low`…`high`), planner next actions — schema not student-safe / not P-001.2 complete.
4. **HTTP facade** (`get_dashboard_readiness_surface`): EP-002.6 cutover or legacy; empty drivers on legacy path.
5. **Presentation** re-narrates Twin shallowly (`_twin_readiness_narrative`) and legacy via EIP-003 — compensating for missing service schema (same defect EP-003.1 fixed for tips).

---

## 3. Discovery conclusions

| Finding | Implication |
|---|---|
| K3 = 52 (Partial) | Prefer interpretable, evidence-bound readiness over calm opaque composites |
| Twin intelligence already has drivers | Enhance communication quality; do not invent a new score formula |
| Legacy surface lacks drivers/schema | Attach explicit drivers from composite components at service layer |
| Internal confidence bands leak | Map to student-safe High / Moderate / Low / Cannot yet be estimated |
| No score-change reasoning | Add driver-based change narrative (+ optional previous score) |
| Presentation re-narrates | Move schema into ReadinessService; adapter pass-through when complete |
| Ownership settled (EP-002.9) | Enhance inside ReadinessService only; never select tips or invent plans |

---

## 4. Recommended implementation shape

1. Add `app/services/readiness_quality.py` as the quality contract module **owned and called only by** `ReadinessService`.
2. Apply mandatory explanation schema, student-safe confidence, explicit drivers, evidence, change reasoning, and primary next action on dashboard surfaces and intelligence assessments.
3. Keep `get_overall_readiness` bare (collector recursion safety).
4. Keep `RuntimeAPresentationAdapter` presentation-only: pass through when readiness schema complete.
5. Preserve fail-open dual-run / cutover flags.

---

## 5. Out of scope (explicit)

- Reopening EP-001.1–4 ownership or Twin Ready (T7) claims.
- Merging Epic structural `ReadinessAggregation` posture with Runtime A % (forbidden hybrid).
- Changing the 50·30·20 composite weights (calibration honesty via explanation, not silent reweight).
- Recommendation ranking / Planning mission generation.
- Full readiness history store for deltas — optional `previous_score` only in this programme.
