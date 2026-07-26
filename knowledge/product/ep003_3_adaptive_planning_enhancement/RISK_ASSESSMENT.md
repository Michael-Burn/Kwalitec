# EP-003.3 — Risk Assessment

**Programme:** EP-003.3 — Adaptive Planning Enhancement  
**Date:** 2026-07-26  

---

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Recursion: Planning quality → Recommendations → mission surface → Planning | Medium | High | Thread-local reentrancy depth; skip sibling lookups when nested; fail-open |
| R2 | Planning absorbs readiness evaluation | Low | High | Only `get_overall_readiness`; never recalculate score |
| R3 | Planning re-ranks recommendations | Low | High | Titles for alignment labels only; assembler uses Decision Framework order without calling tip engine for ranking |
| R4 | Presentation invents plan rationale | Low | Medium | Schema-complete pass-through in adapter |
| R5 | Recovery mode feels punishing | Medium | Medium | Lighten load + prefer consolidation; keep review when due; under-claim in copy |
| R6 | Legacy / Twin divergence remains | Medium | Medium | Documented limitation; cutover overlay unchanged in scope |
| R7 | Extra latency from recommendation lookup | Medium | Low | Limit 3 titles; fail-open; nested depth skips lookup |
| R8 | Test / cutover regressions | Low | Medium | Extended unit + cutover suites |

**Residual risk:** Legacy Learning Mode still does not interrupt for weak topics (intentional V1.0 constraint). EP-003.3 improves Twin adaptive plan path and mission-surface explainability.
