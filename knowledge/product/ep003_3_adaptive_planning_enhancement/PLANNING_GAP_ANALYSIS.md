# EP-003.3 — Planning Gap Analysis

**Programme:** EP-003.3 — Adaptive Planning Enhancement  
**Date:** 2026-07-26  

---

## Audit dimensions

| Dimension | Pre-EP-003.3 | Gap | Post-EP-003.3 |
|---|---|---|---|
| Daily workload allocation | Capacity + preferred minutes + light-load heuristic | No per-slot balance; missed sessions ignored | Balanced `allocated_minutes`; recovery lightening |
| Weak-topic prioritisation | Mastery &lt; 60% weak slot | OK for Twin path; unused missed signal | Recovery slot after misses; progression deferred when recovering |
| Revision balance | Review + weak + progression (or revision lifecycle) | Could overload after misses | Recovery mode caps progression |
| Recommendation integration | None (one-way: Recs → Plan) | No alignment labels / ladder-aware order | Ladder-aligned order + title alignment labels |
| Readiness integration | Twin mastery only | No readiness composite consumption | `get_overall_readiness` labels + light workload note |
| Explainability | Slot `reason` + informal dict | No P-001.2 schema | Mandatory schema + plan drivers |
| Plan stability / recovery | Same-day mission idempotency only | `mission_missed_count` unused | Adaptive recovery mode |

## Duplicated educational reasoning

- Recommendation and Planning both prefer review → weak → progression — **intentional alignment**, not duplication of ranking maths. Planning owns slots; Recommendation owns tip ranking.
- Readiness next-action previously mirrored planner missions — Planning now labels readiness alignment outward without absorbing readiness evaluation.

## Unnecessary complexity avoided

- Did not wire MissionOptimizer.
- Did not call `get_dashboard_readiness_surface` or `build_study_insights` from planning quality (recursion / ownership).
- Did not add new feature flags.

## Student usefulness opportunities addressed

1. Clear why-this-plan speech on Today’s Mission surfaces.
2. Completable days after missed sessions.
3. Minute allocation visible per slot.
4. Honest refusal when no plan/mission exists.
