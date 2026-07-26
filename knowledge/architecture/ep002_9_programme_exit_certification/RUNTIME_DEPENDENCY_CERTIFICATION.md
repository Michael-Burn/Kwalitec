# EP-002.9 — Runtime Dependency Certification

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.9  
**Date:** 2026-07-26

Legend: **O** · **E** · **C** · **R**

---

## 1. Intended dependency direction (certified)

```
Curriculum Engine
        ↓
Runtime A writes / facts
        ↓
MS-004 collectors → TwinRuntimeEvidence
        ↓
EP-001.1 CanonicalLearnerState (Foundation.assemble)
        ↓
   ┌────┴────┬────────────┐
   ↓         ↓            ↓
EP-001.2   EP-001.3     Insight inputs
Planner    Readiness
   ↓         ↓
   └────┬────┘
        ↓
     EP-001.4 Insight
        ↓
Consumer Chain (observe / dual-run / cutover)
        ↓
RuntimeAPresentationAdapter
        ↓
Blueprints → Templates
```

**Forbidden reverse edges**

| Edge | Status |
|---|---|
| Twin packages → planner / readiness / insight for authority | **Forbidden — not introduced** |
| Insight → invent readiness / plans when Twin OFF | **Forbidden — not introduced** |
| Foundation inside `get_overall_readiness` | **Forbidden — not introduced** |
| Presentation / templates → evaluation maths | **Forbidden — not introduced** |
| Process-global Foundation / CLS cache | **Forbidden — composition-local only** |

---

## 2. Runtime A composition edges (post EP-002)

| From | To | Edge type | Certified? |
|---|---|---|---|
| `consumer_chain.foundation_di` | Foundation resolve + CLS assemble | DI helper | Yes |
| Planning / Readiness / Recommendation `build_*` | Foundation + optional `canonical_state=` | Composition | Yes |
| Readiness → Planning | Nested compose with forwarded CLS | Nested | Yes |
| Insight → Planning / Readiness | Nested compose with forwarded CLS | Nested | Yes |
| Cutover modules → `build_*` + legacy getters | Selection / projection | Gate | Yes |
| Dual-run modules → Twin sidecar + legacy | Diagnostic compare | Observe | Yes |
| Blueprints → cutover facades / presentation adapter | HTTP composition | Surface | Yes |
| Presentation adapter → Insight fields / EIP-003 | Narration selection | Presentation | Yes |
| Experience composition → Foundation Authority | Separate DI root (gated) | Experience | Yes (orthogonal) |
| Collectors → `get_overall_readiness` | Legacy fact path | Collector | Yes (must remain) |

---

## 3. Quarantined / non-edges

| Candidate edge | Posture | Evidence |
|---|---|---|
| HTTP → `MissionOptimizer.generate_balanced_mission` | **No production callers** | EP-002.2 decision; EP-002.7 verification |
| Cutover → Experience bridges (MissionStart / Recommendation) | **Not inherited** | Bridges remain legacy |
| Twin → ORM mission write | **Forbidden** | EP-002.7 constitutional pack |
| EducationalExplainability → Twin evaluation | **Not present** | Outcome B legacy adapter only |

---

## 4. Collector recursion invariant

**O:** Foundation assemble still reaches collectors that call legacy readiness getters.  
**E:** EP-001.5 / EP-002.2 / EP-002.6 invariants.  
**C:** Certified safe because readiness cutover never wraps `get_overall_readiness` with Foundation; collectors remain on pure legacy getters.

---

## 5. Dependency certification statement

| Criterion | Result |
|---|---|
| Dependency direction intact after EP-002 | **Certified** |
| Circular import risk managed | **Low** (lazy resolves in `consumer_chain`) |
| Ownership violation via dependency | **None certified** |
| Global mutable Twin state | **Absent** |
| MissionOptimizer reintroduced as dependency | **No** |

**Verdict: Runtime dependency graph is certified intact.**

**R:** Successor programmes must not add Twin→service authority edges or collector wraps without a constitutional STOP review.
