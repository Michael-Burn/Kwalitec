# EP-002.6 — Risk Assessment

**Milestone:** EP-002.6 — Readiness Intelligence Dual-Run & Gated HTTP Cutover  
**Date:** 2026-07-26  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Risk register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Collector recursion if intelligence wraps `get_overall_readiness` | Low | High | Facade-only cutover; architecture tests assert getters remain pure |
| R2 | Premature production cutover | Medium | High | Production env hard gate; flag default OFF |
| R3 | Score divergence confuses staging reviewers | Medium | Medium | Semantic alignment reporting; score tolerance ≤ 10 |
| R4 | Double Twin assemble with Study Insights + readiness | Medium | Low | Independent ContextVars; request caches; shared Foundation DI from EP-002.2 |
| R5 | Explainability double-narration | Medium | Low | Skip EducationalExplainability when `source_authority=readiness_intelligence` |
| R6 | Template breakage from projection shape drift | Low | Medium | Project into legacy field names; HTTP integration tests |
| R7 | Operator confusion between Insights and Readiness flags | Medium | Low | Distinct env names; docs kill-switch order |
| R8 | Scope creep into Experience `/student` TwinPort | Medium | Medium | Explicit out-of-scope; Runtime A surfaces only |
| R9 | Treating milestone as Twin Ready (T7) | Low | High | Explicit non-claim in completion report |
| R10 | Mission/plan cutover accidentally bundled | Low | High | EP-002.7 remains separate |

---

## 2. Residual risks after mitigations

| Residual | Acceptance |
|---|---|
| Staging students may see Twin readiness scores that differ from legacy | Accepted for gated soak |
| Dual Twin assemble cost on pages serving both Insights + Readiness cutover | Accepted; Foundation DI shared; measure via telemetry |
| Alignment mismatches do not auto-block serve | Accepted — report only; blocking limited to limitation codes |

---

## 3. Explicit non-risks (out of scope)

- Schema / Alembic changes
- New readiness engine
- Twin redesign
- Production-wide activation
- Education OS readiness stack

---

## 4. Verdict

**O:** Highest constitutional risk is collector recursion.  
**E:** Design keeps legacy getters untouched; cutover lives in surface facades.  
**C:** Risks are manageable under Study Insights-proven pattern.  
**R:** Proceed with implementation; require collector regression tests as exit gate.
