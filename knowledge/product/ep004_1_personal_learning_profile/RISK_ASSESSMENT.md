# EP-004.1 — Risk Assessment

**Programme:** EP-004.1 — Personal Learning Profile  
**Date:** 2026-07-26  

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Profile treated as educational brain | Medium | High | No decision APIs; constitutional docs; ownership tests |
| R2 | Accept-rate used as mastery | Medium | High | `preference_summary` claim; forbidden keys; limitations text |
| R3 | Invented duration / windows | Medium | Medium | Explicit unsupported without lawful evidence |
| R4 | Service coupling to aggregator | Low | Medium | Port / consumer helpers only |
| R5 | Fail-closed breaks student path | Low | High | Fail-open resolve; service try/except |
| R6 | Twin write-back creep | Low | High | Explicit non-goal; verification checklist |
| R7 | Over-claimed KSI from infra alone | Medium | Medium | Under-claim in KSI assessment; gated OFF |
| R8 | Recovery “effectiveness” over-read | Medium | Medium | Limitation: follow-through proxy ≠ fixed deficit |
| R9 | Process-local loss on restart | High | Low | Documented; durable store deferred |
| R10 | Closed-loop adaptation without review | Low | High | STOP condition in architecture §0 |

**Overall residual risk:** Acceptable for gated, observational profile infrastructure.
