# PI-001D — Runtime Parity Report

**Programme:** PI-001D — Educational Platform Certification  
**Status:** Complete  
**Date:** 2026-07-27  

---

## Summary

This report compares Runtime A and Runtime C for the existing `IFoA CS1` subject at the educational-structure level. The goal is not to prove that both runtimes are identical implementations, but to verify that Runtime C preserves the same curriculum truth where equivalence is expected before any cutover decision.

Parity evidence was executed through `tests/certification/test_runtime_parity.py`.

---

## Scope of comparison

Compared surfaces:

- section count
- section codes and order
- topic count
- topic codes and order
- topic titles
- objective count
- study plan topic coverage
- mission template topic coverage
- progress model topic coverage

Not compared in this report:

- weekly scheduling behaviour
- recommendation ranking
- full readiness scoring
- mastery / estimated knowledge scoring
- student UI rendering

Those are either intentionally different or not yet implemented in Runtime C.

---

## Evidence executed

```bash
python3 -m pytest tests/certification/test_runtime_parity.py -q
# 9 passed in 0.71s
```

---

## Parity results

| Dimension | Runtime A | Runtime C | Result |
|---|---|---|---|
| Section count | Bundled CS1 V2 sections | Derived published sections | PASS |
| Section order | `display_order` from engine | Derived section order | PASS |
| Topic count | Flat topic list from engine | Derived topic artefacts | PASS |
| Topic code order | Engine topic sequence | Derived topic sequence | PASS |
| Topic titles | Bundled JSON titles | Derived titles | PASS |
| Objective count | Learning objectives under engine topics | Derived objective artefacts | PASS |
| Study plan coverage | All engine topics present | All topics in template | PASS |
| Mission coverage | Topic-level mission expectation | One template per topic | PASS |
| Progress denominator coverage | Engine topic count | Progress model topic ids | PASS |

---

## Interpretation

Runtime C is structurally equivalent to Runtime A for the CS1 curriculum package on the dimensions tested above.

That means:

- Runtime C preserves the same syllabus structure for an existing subject.
- Runtime C does not lose sections, topics, or objectives during derivation.
- Runtime C can support plan, mission, and progress instantiation over the same topic universe as Runtime A.

This does **not** yet mean Runtime C is cutover-ready. Structural parity is necessary but insufficient.

---

## Residual parity gaps

The following areas remain outside strict parity:

1. **Weekly planning shape**  
   Runtime A creates `StudyPlan` and `WeekPlan` records with exam-date scheduling. Runtime C currently instantiates a curriculum-sequenced plan instance without time-boxed week planning.

2. **Mission sophistication**  
   Runtime A planning includes broader mission behaviours, including lifecycle-aware and revision-oriented logic. Runtime C currently provides deterministic topic-bound learning missions.

3. **Readiness outputs**  
   Runtime A computes full readiness intelligence. Runtime C exposes readiness inputs only.

4. **Estimated Knowledge outputs**  
   Runtime A has broader learning-state infrastructure. Runtime C exposes placeholder EK inputs without mastery claims.

5. **Student entry points**  
   Runtime A is wired into live user-facing flows. Runtime C remains application-service level and coexistence-gated.

---

## Verdict

**Parity verdict: PASS for curriculum structure and educational artefact coverage.**

Runtime C matches Runtime A where equivalence is currently required by PI-001D: curriculum representation, topic coverage, and derived learning artefact completeness for CS1.
