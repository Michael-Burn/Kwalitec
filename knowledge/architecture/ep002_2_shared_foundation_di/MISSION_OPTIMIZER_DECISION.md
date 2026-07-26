# EP-002.2 — MissionOptimizer Architectural Decision

**Milestone:** EP-002.2  
**Date:** 2026-07-26  
**Subject:** `MissionOptimizer.generate_balanced_mission`  
**Status:** **Accepted** — Deprecate and quarantine (do not wire to production)

Legend: **Observation** · **Evidence** · **Conclusion** · **Recommendation**

---

## 1. Question

Should `MissionOptimizer.generate_balanced_mission`:

1. remain and be wired into production,  
2. be deprecated,  
3. be retired (deleted), or  
4. be absorbed elsewhere?

---

## 2. Observation

`MissionOptimizer` produces a balanced dict of review / weak / progression topics. EP-001.2 taught its Twin-ON path to reshape `PlanningService.build_daily_study_plan` slots. Educational governance has long treated it as latent dual-authority risk (V1-TD-003 / GAP-005).

---

## 3. Evidence

| Check | Result |
|---|---|
| Callers under `app/` | **None** (definition site only) |
| Dashboard / templates | **No** references (grep 2026-07-26) |
| Dedicated tests | **None** |
| Twin ON behaviour | Thin reshape of EP-001.2 `today_missions` |
| Twin OFF behaviour | AdaptiveLearning + CurriculumService dict helper |
| Parallel capability | `build_daily_study_plan` already owns balanced slots |
| Educational debt ID | V1-TD-003 / EIP-007 / ES-H-002 |
| EP-001.5 finding | IF-09 / TD-ARCH-03 — orphaned API |
| EP-002 programme | WS0 fate decision before WS6 mission cutover |

---

## 4. Options evaluated

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| Wire to production | Surfaces balanced missions | Dual-authority vs Learning Mode `generate_today_mission`; contradicts governance quarantine | **Reject** |
| Soft deprecate + quarantine | Formalises status; warns callers; preserves behaviour for accidental scripts | Code remains until EP-002.7 cleanup | **Accept** |
| Hard delete now | Removes orphan | Risk of unknown external/script callers; not required for DI milestone | **Defer** to EP-002.7 |
| Absorb into PlanningService | Conceptually already absorbed via `today_missions` | Further code move adds churn without student value | **Already absorbed functionally** |

---

## 5. Conclusion

**MissionOptimizer should be deprecated and quarantined — not wired into production.**

Functional planning authority for Twin-gated balanced slots already lives in `PlanningService.build_daily_study_plan`. Keeping the module soft-deprecated avoids accidental dual-authority while preserving behaviour until EP-002.7 mission-surface cutover can delete or permanently archive it.

---

## 6. Recommendation

| Action | Owner milestone |
|---|---|
| Module docstring + `DeprecationWarning` on `generate_balanced_mission` | **EP-002.2 (this)** |
| Do not add HTTP / template callers | Binding now |
| Prefer `build_daily_study_plan` for any future mission dual-run | EP-002.7 |
| Consider hard delete after WS6 dual-run proves no need | EP-002.7 / WS8 |

**Recommendation for EP-002.7:** treat MissionOptimizer as out of scope for student cutover; dual-run `build_daily_study_plan` vs `generate_today_mission` only.

---

## 7. Behaviour preservation

Direct calls to `generate_balanced_mission` still return the same dict shapes (Twin ON / OFF paths unchanged aside from optional Foundation DI kwargs and deprecation warning). No student-facing path is affected because none exist.
